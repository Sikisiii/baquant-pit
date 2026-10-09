"""Real APIs versus untouched merged golden expectations, one item per vector."""

import json
import os
from dataclasses import FrozenInstanceError
from datetime import date, datetime
from pathlib import Path

import pytest
from runtime_support import instant, materialize

from baquant_pit import (
    BaquantPITError,
    DateWindow,
    canonical_bytes,
    canonical_sha256,
    canonical_text,
    format_utc_instant,
    normalize_utc_instant,
    sha256_bytes,
    sha256_file,
)

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


TEMPORAL = load("tests/fixtures/golden/temporal-v1.json")
CANONICAL = load("tests/fixtures/golden/canonical-v1.json")
RAW = load("tests/fixtures/golden/raw-integrity-v1.json")
COVERAGE = load("docs/implementation/golden-runtime-coverage-v1.json")
RECORDS = [
    *TEMPORAL["vectors"],
    *CANONICAL["vectors"],
    *RAW["raw_vectors"],
    *RAW["file_equivalence_vectors"],
    *RAW["invalid_vectors"],
]
BY_ID = {r["vector_id"]: r for r in RECORDS}
CLASSIFICATION = {r["vector_id"]: r for r in COVERAGE["vectors"]}


def test_every_golden_vector_accounted_once():
    assert len(BY_ID) == len(RECORDS) == 116
    assert len(CLASSIFICATION) == len(COVERAGE["vectors"]) == len(BY_ID)
    assert CLASSIFICATION.keys() == BY_ID.keys()
    for record in CLASSIFICATION.values():
        assert record["classification"] in {
            "RUNTIME_EXECUTABLE",
            "CONCEPTUAL_NONEXECUTABLE",
            "PLATFORM_CONDITIONAL",
        }
        assert record["reason"]
        assert record["test"] == "test_golden_runtime_conformance"


def temporal_call(record):
    d = record["semantic_input"]
    kind = d["kind"]
    if kind == "instant":
        value = instant(d)
        result = normalize_utc_instant(value)
        if record["valid"]:
            assert format_utc_instant(result) == record["expected"]["utc_text"]
            assert format_utc_instant(value) == record["expected"]["utc_text"]
        return
    if kind == "date":
        value = date.fromisoformat(d["text"])
        # The date remains a tagged date; the instant API must reject it.
        assert json.loads(canonical_text(value))[1] == [
            "date",
            record["expected"]["date_text"],
        ]
        with pytest.raises(BaquantPITError, match="^TEMPORAL_INVALID_TYPE$"):
            normalize_utc_instant(value)
        return
    if kind == "window":
        args = [date.fromisoformat(d["start"]), date.fromisoformat(d["end"])]
        if "cutoff" in d:
            args.append(
                None if d["cutoff"] is None else datetime.fromisoformat(d["cutoff"])
            )
        window = DateWindow(*args)
        e = record["expected"]
        assert window.start.isoformat() == e["start"]
        assert window.end.isoformat() == e["end"]
        assert format_utc_instant(window.cutoff) == e["cutoff_utc"]
        assert window.start <= window.start <= window.end
        assert window.start <= window.end <= window.end
        with pytest.raises(FrozenInstanceError):
            window.start = window.end
        assert not hasattr(window, "calendar")
        return
    if kind == "cutoff_relation":
        actual = normalize_utc_instant(datetime.fromisoformat(d["instant_utc"]))
        cutoff = normalize_utc_instant(datetime.fromisoformat(d["cutoff_utc"]))
        assert (actual <= cutoff) is record["expected"]["result"]
        return
    if kind == "cutoff":
        DateWindow(date(2032, 4, 5), date(2032, 4, 5), date.fromisoformat(d["value"]))
        return
    if kind == "window_endpoint":
        DateWindow(datetime(2032, 4, 5), date(2032, 4, 5), datetime(2032, 4, 5))
        return
    raise AssertionError("Unsupported executable temporal descriptor")


def raw_invalid_call(record, tmp_path, monkeypatch):
    key = record["vector_id"]
    if key in ("R101", "R102"):
        sha256_bytes("x" if key == "R101" else bytearray(b"x"))
    elif key == "F101":
        sha256_file(tmp_path / "missing")
    elif key == "F102":
        sha256_file(tmp_path)
    elif key == "F106":
        sha256_file("synthetic\x00path")
    elif key == "F104":
        if not hasattr(os, "mkfifo"):
            pytest.skip("PLATFORM_CONDITIONAL: native FIFO creation unavailable")
        path = tmp_path / "fifo"
        os.mkfifo(path)
        sha256_file(path)
    else:
        path = tmp_path / "regular"
        path.write_bytes(b"synthetic")
        if key == "F103":

            def denied(*args, **kwargs):
                raise PermissionError("synthetic denied path")

            monkeypatch.setattr(type(path), "open", denied)
        elif key == "F105":

            class FailingRead:
                def __enter__(self):
                    self.calls = 0
                    return self

                def __exit__(self, *args):
                    return False

                def read(self, size):
                    self.calls += 1
                    if self.calls == 1:
                        return b"partial"
                    raise OSError("synthetic failure before EOF")

            monkeypatch.setattr(type(path), "open", lambda *a, **k: FailingRead())
        else:
            raise AssertionError("Unaccounted raw error vector")
        sha256_file(path)


@pytest.mark.parametrize("record", RECORDS, ids=lambda r: r["vector_id"])
def test_golden_runtime_conformance(record, tmp_path, monkeypatch):
    key = record["vector_id"]
    coverage = CLASSIFICATION[key]
    if coverage["classification"] == "CONCEPTUAL_NONEXECUTABLE":
        pytest.skip(coverage["reason"])

    def invoke():
        if key.startswith("T"):
            temporal_call(record)
        elif key.startswith("C"):
            value = materialize(record["semantic_input"])
            actual = canonical_bytes(value)
            assert actual == bytes.fromhex(record["canonical_bytes_hex"])
            assert canonical_text(value) == record["canonical_utf8"]
            assert canonical_sha256(value) == record["expected_sha256"]
        elif "bytes_hex" in record:
            assert (
                sha256_bytes(bytes.fromhex(record["bytes_hex"]))
                == record["expected_sha256"]
            )
        elif "content_hex" in record:
            payload = bytes.fromhex(record["content_hex"])
            path = tmp_path / "payload.bin"
            path.write_bytes(payload)
            assert (
                sha256_file(path) == sha256_bytes(payload) == record["expected_sha256"]
            )
        else:
            raw_invalid_call(record, tmp_path, monkeypatch)

    if "expected_error_id" in record:
        with pytest.raises(BaquantPITError) as caught:
            invoke()
        assert caught.value.error_id == record["expected_error_id"]
        assert str(caught.value) == record["expected_error_id"]
    else:
        invoke()
