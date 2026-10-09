"""Validate declarative assets, never evaluate semantic inputs or PIT algorithms."""

import hashlib
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts/minimal-primitives-v1.json"
HEX_DIGEST = re.compile(r"[0-9a-f]{64}\Z")


def reject_json_constant(value):
    raise ValueError(f"Non-JSON constant in asset: {value}")


def load_asset(relative):
    raw = (ROOT / relative).read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), "Asset must have no BOM"
    return json.loads(raw.decode("utf-8"), parse_constant=reject_json_constant)


CONTRACT = load_asset("contracts/minimal-primitives-v1.json")
FIXTURES = [load_asset(name) for name in CONTRACT["golden_fixtures"]]


def all_records(fixture):
    for key in (
        "vectors",
        "raw_vectors",
        "file_equivalence_vectors",
        "invalid_vectors",
    ):
        yield from fixture.get(key, [])


def test_contract_identity_scope_and_required_fields():
    required = {
        "contract_id",
        "version",
        "status",
        "canonical_format_id",
        "temporal_format_id",
        "raw_integrity_format_id",
        "supported_types",
        "rejected_types",
        "datetime_policy",
        "date_window_policy",
        "decimal_policy",
        "unicode_policy",
        "mapping_policy",
        "sequence_policy",
        "cycle_policy",
        "hashing_policy",
        "raw_bytes_policy",
        "file_policy",
        "error_ids",
        "compatibility",
        "golden_fixtures",
        "explicit_exclusions",
        "resource_policy",
        "byte_format",
        "canonical_representation",
    }
    assert required <= CONTRACT.keys()
    assert CONTRACT["contract_id"] == "baquant-pit-minimal-primitives"
    assert CONTRACT["version"] == CONTRACT["contract_version"] == 1
    assert CONTRACT["status"] == "PRIVATE_REVIEW_CANDIDATE"
    assert CONTRACT["baquant_compatibility"] == "NOT_CLAIMED"
    assert CONTRACT["public_api_compatibility"] == "NOT_ESTABLISHED"
    assert CONTRACT["public_release_authorized"] is False
    assert CONTRACT["runtime_implementation_present"] is False
    assert len(CONTRACT["capabilities"]) == len(set(CONTRACT["capabilities"])) == 7
    assert len(CONTRACT["error_ids"]) == len(set(CONTRACT["error_ids"]))


def test_policy_decisions_are_bounded_and_non_ambiguous():
    assert CONTRACT["datetime_policy"]["text"] == "YYYY-MM-DDTHH:MM:SS.ffffffZ"
    assert CONTRACT["datetime_policy"]["fraction_digits"] == 6
    assert CONTRACT["datetime_policy"]["trailing_zeros"] == "ALWAYS_RETAIN"
    assert CONTRACT["date_window_policy"]["endpoints"] == "INCLUSIVE"
    assert CONTRACT["date_window_policy"]["immutable"] is True
    assert CONTRACT["decimal_policy"]["finite_only"] is True
    assert CONTRACT["decimal_policy"]["preserve_scale"] is True
    assert CONTRACT["unicode_policy"]["normalization"] == "NONE"
    assert CONTRACT["mapping_policy"]["coercion"] == "NONE"
    assert CONTRACT["sequence_policy"]["tuple"] == "REJECT"
    assert CONTRACT["cycle_policy"]["cycles"] == "REJECT"
    assert CONTRACT["resource_policy"]["status"] == "NORMATIVE_V1"
    assert CONTRACT["hashing_policy"]["algorithm"] == "SHA-256"
    assert CONTRACT["hashing_policy"]["salt"] is None
    assert CONTRACT["hashing_policy"]["secret_key"] is None


def test_fixture_paths_exist_and_format_ids_match():
    assert len(CONTRACT["golden_fixtures"]) == 3
    assert len(CONTRACT["specifications"]) == 4
    assert {f["format_id"] for f in FIXTURES} == {
        CONTRACT["canonical_format_id"],
        CONTRACT["temporal_format_id"],
        CONTRACT["raw_integrity_format_id"],
    }
    for fixture in FIXTURES:
        assert fixture["contract_id"] == CONTRACT["contract_id"]
        assert fixture["contract_version"] == CONTRACT["version"]
        assert fixture["status"] == CONTRACT["status"]
        assert fixture["synthetic"] is True
        assert fixture["input_descriptors_executable"] is False
        assert fixture["coverage"]
    for relative in CONTRACT["golden_fixtures"] + CONTRACT["specifications"]:
        assert not Path(relative).is_absolute() and ".." not in Path(relative).parts
        assert (ROOT / relative).is_file()
    for relative in CONTRACT["specifications"]:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert CONTRACT["contract_id"] in text
        assert CONTRACT["status"] in text
    expected_docs = {
        "docs/specs/temporal-semantics-v1.md": "temporal_format_id",
        "docs/specs/canonicalization-v1.md": "canonical_format_id",
        "docs/specs/raw-integrity-v1.md": "raw_integrity_format_id",
    }
    for relative, field in expected_docs.items():
        assert CONTRACT[field] in (ROOT / relative).read_text(encoding="utf-8")


def test_vector_ids_unique_and_invalid_errors_recognized():
    records = [r for fixture in FIXTURES for r in all_records(fixture)]
    ids = [r["vector_id"] for r in records]
    assert len(ids) == len(set(ids))
    for record in records:
        if record.get("valid") is False or "invalid_condition" in record:
            assert record["invalid_condition"]
            assert record["expected_error_id"] in CONTRACT["error_ids"]
            assert "expected_sha256" not in record
        elif "expected_sha256" in record:
            assert HEX_DIGEST.fullmatch(record["expected_sha256"])


CANONICAL = FIXTURES[1]
RAW = FIXTURES[2]


@pytest.mark.parametrize(
    "record",
    [r for r in CANONICAL["vectors"] if r["valid"]],
    ids=lambda r: r["vector_id"],
)
def test_canonical_literal_bytes_text_logical_form_and_digest(record):
    # This compares already-recorded assets. It does not normalize semantic_input.
    literal_bytes = bytes.fromhex(record["canonical_bytes_hex"])
    assert literal_bytes == record["canonical_utf8"].encode("utf-8")
    assert not literal_bytes.startswith(b"\xef\xbb\xbf")
    assert not literal_bytes.endswith(b"\n")
    assert json.loads(literal_bytes.decode("utf-8")) == [
        CONTRACT["canonical_format_id"],
        record["normalized_logical_form"],
    ]
    assert hashlib.sha256(literal_bytes).hexdigest() == record["expected_sha256"]
    assert record["input_description"]


@pytest.mark.parametrize("record", RAW["raw_vectors"], ids=lambda r: r["vector_id"])
def test_raw_recorded_literal_payload_digest(record):
    payload = bytes.fromhex(record["bytes_hex"])
    assert len(payload) == record["byte_length"]
    assert hashlib.sha256(payload).hexdigest() == record["expected_sha256"]


def test_file_equivalence_records_reuse_exact_synthetic_payloads():
    by_id = {r["vector_id"]: r for r in RAW["raw_vectors"]}
    for file_record in RAW["file_equivalence_vectors"]:
        raw_record = by_id[file_record["raw_vector_id"]]
        assert file_record["content_hex"] == raw_record["bytes_hex"]
        assert file_record["expected_sha256"] == raw_record["expected_sha256"]
        assert (
            hashlib.sha256(bytes.fromhex(file_record["content_hex"])).hexdigest()
            == (file_record["expected_sha256"])
        )
    # No file-content runtime function is implemented or invoked by this test.


def test_recorded_equivalence_and_typed_collision_pairs():
    for fixture, collection in ((CANONICAL, "vectors"), (RAW, "raw_vectors")):
        by_id = {r["vector_id"]: r for r in fixture[collection]}
        for a, b in fixture.get("equivalent_pairs", []):
            assert by_id[a]["expected_sha256"] == by_id[b]["expected_sha256"]
            assert by_id[a]["canonical_bytes_hex"] == by_id[b]["canonical_bytes_hex"]
        for a, b in fixture.get("distinct_pairs", []):
            assert by_id[a]["expected_sha256"] != by_id[b]["expected_sha256"]
    by_id = {r["vector_id"]: r for r in RAW["raw_vectors"]}
    assert by_id["R002"]["byte_length"] == by_id["R007"]["byte_length"]


def test_temporal_recorded_examples_and_fixed_text_format():
    records = FIXTURES[0]["vectors"]
    valid = {r["vector_id"]: r for r in records if r["valid"]}
    assert valid["T001"]["expected"] == valid["T002"]["expected"]
    assert valid["T001"]["expected"] == valid["T003"]["expected"]
    text_pattern = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z\Z")
    for record in valid.values():
        for key in ("utc_text", "cutoff_utc"):
            if key in record["expected"]:
                assert text_pattern.fullmatch(record["expected"][key])
    assert valid["T006"]["expected"]["instant_conversion"] is False
    assert valid["T007"]["expected"]["immutable"] is True
    assert valid["T008"]["expected"]["start"] == valid["T008"]["expected"]["end"]
    assert valid["T009"]["expected"]["result"] is True
    assert valid["T011"]["expected"]["result"] is False
    error_ids = {r["expected_error_id"] for r in records if not r["valid"]}
    assert {
        "TEMPORAL_NAIVE_DATETIME",
        "TEMPORAL_NULL_OFFSET",
        "TEMPORAL_WINDOW_REVERSED",
        "TEMPORAL_CUTOFF_REQUIRED",
    } <= error_ids


def test_assets_have_no_private_paths_payload_keys_or_secret_shapes():
    patterns = [
        r"(?i)(?:[a-z]:[\\/]|/(?:Users|home|mnt)/|file:[/]{2})",
        r"(?i)\b\d{6}\.(?:SH|SZ|BJ)\b",
        r"(?i)(?:gh[pousr]_[a-z0-9]{20,}|github_pat_[a-z0-9_]{20,}|sk-[a-z0-9]{20,})",
        r"(?i)(?:postgres(?:ql)?|mysql|mongodb|redis)://",
        r'(?i)"(?:ts_code|access_token|api_key|password|prompt|messages|choices)"\s*:',
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    ]
    for relative in ["contracts/minimal-primitives-v1.json"] + CONTRACT[
        "golden_fixtures"
    ]:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert not any(re.search(pattern, text) for pattern in patterns), relative
