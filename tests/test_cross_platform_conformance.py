"""Bounded portability gaps; the full frozen golden suite runs on both OSes."""

import errno
import json
import locale
import os
import time
from datetime import UTC, date, datetime
from decimal import ROUND_DOWN, ROUND_UP, localcontext
from pathlib import Path

import pytest
from runtime_support import materialize

import baquant_pit as pit

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = json.loads(
    (ROOT / "tests/fixtures/golden/canonical-v1.json").read_text(encoding="utf-8")
)
BY_ID = {r["vector_id"]: r for r in CANONICAL["vectors"]}
REPRESENTATIVE_IDS = (
    "C001",
    "C002",
    "C003",
    "C006",
    "C008",
    "C009",
    "C010",
    "C011",
    "C012",
    "C014",
    "C016",
    "C019",
    "C020",
    "C021",
    "C022",
    "C025",
    "C026",
    "C027",
    "C032",
    "C033",
    "C034",
    "C035",
    "C036",
    "C038",
)


def test_exact_public_surface_after_install():
    expected = {
        "BaquantPITError",
        "TemporalError",
        "CanonicalizationError",
        "RawIntegrityError",
        "normalize_utc_instant",
        "format_utc_instant",
        "DateWindow",
        "canonical_bytes",
        "canonical_text",
        "canonical_sha256",
        "sha256_bytes",
        "sha256_file",
    }
    assert set(pit.__all__) == expected and len(pit.__all__) == 12
    assert all(callable(getattr(pit, name)) for name in expected)
    assert pit.__version__ == "0.1.0"


@pytest.mark.parametrize("configuration", ["C", ""], ids=["C", "host-default"])
def test_locale_and_decimal_context_preserve_frozen_bytes(configuration):
    original = locale.setlocale(locale.LC_ALL)
    try:
        locale.setlocale(locale.LC_ALL, configuration)
        for precision, rounding in ((1, ROUND_UP), (28, ROUND_DOWN)):
            with localcontext() as context:
                context.prec = precision
                context.rounding = rounding
                for key in REPRESENTATIVE_IDS:
                    record = BY_ID[key]
                    value = materialize(record["semantic_input"])
                    assert pit.canonical_bytes(value) == bytes.fromhex(
                        record["canonical_bytes_hex"]
                    )
                    assert pit.canonical_text(value) == record["canonical_utf8"]
                    assert pit.canonical_sha256(value) == record["expected_sha256"]
                    if type(value) is datetime:
                        utc_value = pit.normalize_utc_instant(value)
                        assert utc_value.tzinfo is UTC
                        assert pit.canonical_bytes(utc_value) == bytes.fromhex(
                            record["canonical_bytes_hex"]
                        )
                        assert (
                            pit.canonical_sha256(utc_value) == record["expected_sha256"]
                        )
    finally:
        locale.setlocale(locale.LC_ALL, original)
    assert locale.setlocale(locale.LC_ALL) == original


def test_explicit_temporal_values_ignore_local_timezone(monkeypatch):
    records = json.loads(
        (ROOT / "tests/fixtures/golden/temporal-v1.json").read_text(encoding="utf-8")
    )["vectors"]
    selected = [
        r for r in records if r["vector_id"] in {"T001", "T002", "T003", "T004", "T012"}
    ]
    try:
        for setting in ("UTC0", "EST5EDT", "JST-9"):
            with monkeypatch.context() as env:
                env.setenv("TZ", setting)
                if hasattr(time, "tzset"):
                    time.tzset()
                for record in selected:
                    value = datetime.fromisoformat(record["semantic_input"]["text"])
                    assert pit.normalize_utc_instant(value).tzinfo is UTC
                    assert (
                        pit.format_utc_instant(value) == record["expected"]["utc_text"]
                    )
                window = pit.DateWindow(date(2032, 4, 5), date(2032, 4, 5), value)
                assert window.cutoff.tzinfo is UTC
    finally:
        # monkeypatch contexts have restored TZ before restoring the native zone.
        if hasattr(time, "tzset"):
            time.tzset()


def test_short_native_unicode_path_is_content_only(tmp_path):
    raw = json.loads(
        (ROOT / "tests/fixtures/golden/raw-integrity-v1.json").read_text(
            encoding="utf-8"
        )
    )["raw_vectors"]
    record = next(r for r in raw if r["vector_id"] == "R008")
    path = tmp_path / "雪.bin"
    payload = bytes.fromhex(record["bytes_hex"])
    path.write_bytes(payload)
    assert (
        pit.sha256_file(path) == pit.sha256_file(str(path)) == record["expected_sha256"]
    )
    renamed = path.with_name("e\u0301.bin")
    path.rename(renamed)
    os.utime(renamed, (100, 200))
    assert pit.sha256_file(renamed) == record["expected_sha256"]


@pytest.mark.parametrize("stage", ["stat", "open", "read"])
def test_host_path_length_os_errors_use_existing_io_id(tmp_path, monkeypatch, stage):
    # Controlled error classification, not a claim about actual host long-path support.
    path = tmp_path / "a"
    path.write_bytes(b"synthetic")

    def fail(*args, **kwargs):
        error = OSError(errno.ENAMETOOLONG, "synthetic path length error")
        error.winerror = 206
        raise error

    class Reader:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        read = fail

    if stage == "read":
        monkeypatch.setattr(type(path), "open", lambda *args, **kwargs: Reader())
    else:
        monkeypatch.setattr(type(path), stage, fail)
    with pytest.raises(pit.BaquantPITError) as caught:
        pit.sha256_file(path)
    assert caught.value.error_id == str(caught.value) == "RAW_FILE_IO_ERROR"
    assert str(path) not in repr(caught.value)
