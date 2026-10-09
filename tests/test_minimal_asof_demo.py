"""Shared synthetic expectations, including actual CLI bytes on every CI host."""

import ast
import copy
import inspect
import itertools
import json
import os
import runpy
import subprocess
import sys
from dataclasses import replace
from datetime import datetime
from pathlib import Path

import pytest

import baquant_pit
from baquant_pit import TemporalError, canonical_sha256

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples/minimal_asof_demo.py"
DEMO = runpy.run_path(str(SCRIPT))
demonstrate = DEMO["demonstrate"]
parse_demo = DEMO["parse_demo"]
load_demo = DEMO["load_demo"]
json_bytes = DEMO["json_bytes"]
DemoObservation = DEMO["DemoObservation"]
DemoDataError = DEMO["DemoDataError"]
DemoAmbiguousObservationError = DEMO["DemoAmbiguousObservationError"]
RECEIPT = json.loads(
    (ROOT / "docs/implementation/minimal-asof-demo-v1.json").read_text(encoding="utf-8")
)
EXPECTED = RECEIPT["primary_result"]
DOCUMENT = json.loads(
    (ROOT / "examples/data/minimal_asof_demo.json").read_text(encoding="utf-8")
)


@pytest.mark.parametrize(
    "case", RECEIPT["tested_cutoffs"], ids=lambda case: case["cutoff_id"]
)
def test_five_cutoffs_and_future_exclusion(case):
    observations, _ = parse_demo(DOCUMENT)
    cutoff = datetime.fromisoformat(case["as_of"])
    result = demonstrate(observations, cutoff)
    assert result["naive_latest"] == "obs-003"
    for field in ("pit_as_of", "visible", "future_excluded"):
        assert result[field] == case[field]
    assert result["result"] == (
        "NO_FUTURE_OBSERVATIONS" if case["cutoff_id"] == "E" else "LOOK_AHEAD_PREVENTED"
    )
    assert set(result["visible"]).isdisjoint(result["future_excluded"])
    assert len(result["visible"]) + len(result["future_excluded"]) == 3
    for observation in observations:
        assert (observation.observation_id in result["visible"]) == (
            observation.available_at <= cutoff
        )


def test_primary_result_and_digest_scopes():
    observations, cutoff = parse_demo(DOCUMENT)
    actual = demonstrate(observations, cutoff)
    assert actual == EXPECTED
    assert actual["pit_as_of"] != actual["naive_latest"]
    material = {
        "demo_id": "minimal-asof-v1",
        "as_of": cutoff,
        "observations": [
            {
                "observation_id": row.observation_id,
                "value": row.value,
                "available_at": row.available_at,
            }
            for row in observations
        ],
    }
    assert canonical_sha256(material) == EXPECTED["input_digest"]
    fields = {
        key: value for key, value in actual.items() if not key.endswith("_digest")
    }
    assert canonical_sha256(fields) == EXPECTED["result_digest"]


@pytest.mark.parametrize("order", list(itertools.permutations(range(3))))
def test_input_order_preserves_whole_result_and_digests(order):
    document = copy.deepcopy(DOCUMENT)
    document["observations"] = [document["observations"][i] for i in order]
    observations, cutoff = parse_demo(document)
    assert demonstrate(observations, cutoff) == EXPECTED
    assert json_bytes(demonstrate(observations, cutoff)) == RECEIPT[
        "expected_json_utf8"
    ].encode("utf-8")


@pytest.mark.parametrize(
    "cutoff", ["2032-04-05T18:30:00+08:00", "2032-04-05T05:30:00-05:00"]
)
def test_offset_equivalent_cutoff(cutoff):
    observations, _ = parse_demo(DOCUMENT)
    assert demonstrate(observations, datetime.fromisoformat(cutoff)) == EXPECTED


def test_offset_equivalent_availability():
    document = copy.deepcopy(DOCUMENT)
    times = [
        "2032-04-05T17:00:00+08:00",
        "2032-04-05T07:00:00-05:00",
        "2032-04-06T18:00:00+09:00",
    ]
    for row, timestamp in zip(document["observations"], times, strict=True):
        row["available_at"] = timestamp
    observations, cutoff = parse_demo(document)
    assert demonstrate(observations, cutoff) == EXPECTED


@pytest.mark.parametrize("field", ["demonstration_as_of", "available_at"])
def test_naive_input_rejected_by_existing_primitive(field):
    document = copy.deepcopy(DOCUMENT)
    location = (
        document if field == "demonstration_as_of" else document["observations"][0]
    )
    location[field] = "2032-04-05T09:00:00"
    with pytest.raises(TemporalError, match="TEMPORAL_NAIVE_DATETIME"):
        parse_demo(document)


def test_direct_naive_cutoff_and_availability_rejected():
    observations, cutoff = parse_demo(DOCUMENT)
    with pytest.raises(TemporalError, match="TEMPORAL_NAIVE_DATETIME"):
        demonstrate(observations, datetime(2032, 4, 5, 10, 30))
    observations[0] = replace(observations[0], available_at=datetime(2032, 4, 5, 9))
    with pytest.raises(TemporalError, match="TEMPORAL_NAIVE_DATETIME"):
        demonstrate(observations, cutoff)


def test_cutoff_is_required_and_none_is_not_a_default():
    observations, _ = parse_demo(DOCUMENT)
    assert (
        inspect.signature(demonstrate).parameters["as_of"].default
        is inspect.Parameter.empty
    )
    with pytest.raises(TypeError):
        demonstrate(observations)
    with pytest.raises(TemporalError, match="TEMPORAL_INVALID_TYPE"):
        demonstrate(observations, None)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("observation_id", "obs-002"),
        ("observation_id", ""),
        ("observation_id", 1),
        ("value", 1),
        ("available_at", "invalid"),
        ("available_at", None),
    ],
)
def test_malformed_observation_rejected(field, value):
    document = copy.deepcopy(DOCUMENT)
    document["observations"][0][field] = value
    with pytest.raises(DemoDataError, match="^DEMO_INVALID_DATA$"):
        parse_demo(document)


@pytest.mark.parametrize(
    "document",
    [
        None,
        [],
        {},
        {key: value for key, value in DOCUMENT.items() if key != "demonstration_as_of"},
        DOCUMENT | {"extra": True},
        DOCUMENT | {"demo_id": "other-demo"},
        DOCUMENT | {"observations": []},
        DOCUMENT | {"observations": {}},
        DOCUMENT | {"observations": [None]},
        DOCUMENT | {"observations": [DOCUMENT["observations"][0] | {"extra": True}]},
        DOCUMENT | {"demonstration_as_of": "invalid"},
    ],
)
def test_malformed_document_rejected(document):
    with pytest.raises(DemoDataError, match="^DEMO_INVALID_DATA$"):
        parse_demo(document)


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("tied_index", [0, 2], ids=["visible-maximum", "naive-maximum"])
def test_latest_tie_fails_closed_for_both_input_orders(reverse, tied_index):
    observations, cutoff = parse_demo(DOCUMENT)
    tied = replace(
        observations[tied_index],
        observation_id="obs-tied",
        available_at=datetime.fromisoformat(
            "2032-04-05T17:00:00+08:00"
            if tied_index == 0
            else "2032-04-06T17:00:00+08:00"
        ),
    )
    observations.append(tied)
    if reverse:
        observations.reverse()
    with pytest.raises(
        DemoAmbiguousObservationError, match="^DEMO_AMBIGUOUS_OBSERVATION$"
    ):
        demonstrate(observations, cutoff)


def test_older_tie_does_not_override_unique_visible_maximum():
    observations, _ = parse_demo(DOCUMENT)
    observations.append(replace(observations[0], observation_id="obs-older-tie"))
    result = demonstrate(observations, observations[1].available_at)
    assert result["pit_as_of"] == "obs-002"
    assert result["future_excluded"] == ["obs-003"]


@pytest.mark.parametrize("content", [b"{", b'{"demo_id":1,"demo_id":2}', b"\xff"])
def test_invalid_json_reports_fixed_error_without_path(tmp_path, content):
    path = tmp_path / "malformed-demo.json"
    path.write_bytes(content)
    with pytest.raises(DemoDataError, match="^DEMO_INVALID_DATA$"):
        load_demo(path)


def test_missing_file_reports_fixed_error_without_path(tmp_path):
    with pytest.raises(DemoDataError, match="^DEMO_INVALID_DATA$"):
        load_demo(tmp_path / "missing-demo.json")


def test_no_wall_clock_defaults_or_package_api_expansion():
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    assert not any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"now", "today", "time", "utcnow"}
        for node in ast.walk(tree)
    )
    assert set(baquant_pit.__all__) == {
        "BaquantPITError",
        "CanonicalizationError",
        "DateWindow",
        "RawIntegrityError",
        "TemporalError",
        "canonical_bytes",
        "canonical_sha256",
        "canonical_text",
        "format_utc_instant",
        "normalize_utc_instant",
        "sha256_bytes",
        "sha256_file",
    }
    assert len(baquant_pit.__all__) == 12
    assert baquant_pit.__version__ == "0.1.0"
    assert not hasattr(baquant_pit, "DemoObservation")
    assert not hasattr(baquant_pit, "DemoAmbiguousObservationError")


def test_cli_json_repeated_bytes_match_shared_receipt(tmp_path):
    outputs = []
    for cwd, timezone in [(ROOT, "UTC"), (tmp_path, "Pacific/Honolulu")]:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--json"],
            cwd=cwd,
            env=dict(os.environ, TZ=timezone, PYTHONIOENCODING="ascii"),
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0
        assert completed.stderr == b""
        assert completed.stdout == RECEIPT["expected_json_utf8"].encode("utf-8")
        assert b"\r" not in completed.stdout
        assert json.loads(completed.stdout.decode("utf-8")) == EXPECTED
        outputs.append(completed.stdout)
    assert outputs[0] == outputs[1]


def test_cli_default_human_output():
    completed = subprocess.run(
        [sys.executable, "examples/minimal_asof_demo.py"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0
    assert completed.stderr == b""
    assert completed.stdout.decode("utf-8").splitlines() == [
        "baquant-pit minimal as-of demo",
        "as_of: 2032-04-05T10:30:00.000000Z",
        "naive latest: obs-003",
        "point-in-time visible: obs-001",
        "future observations excluded: obs-002, obs-003",
        "result: LOOK_AHEAD_PREVENTED",
        "input_digest: " + EXPECTED["input_digest"],
        "result_digest: " + EXPECTED["result_digest"],
    ]
    assert b"\r" not in completed.stdout
