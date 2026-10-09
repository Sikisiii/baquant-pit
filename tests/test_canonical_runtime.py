"""Exact rendering, closed domain, resource boundaries and traversal gates."""

import json
import sys
from datetime import UTC, date, datetime
from decimal import Decimal, localcontext
from enum import Enum, IntEnum, StrEnum
from hashlib import sha256

import pytest
from runtime_support import envelope_input, nested

from baquant_pit import (
    BaquantPITError,
    DateWindow,
    canonical_bytes,
    canonical_sha256,
    canonical_text,
)


def node(value):
    return json.loads(canonical_bytes(value))[1]


def fails(value, error):
    for operation in (canonical_bytes, canonical_text, canonical_sha256):
        with pytest.raises(BaquantPITError) as caught:
            operation(value)
        assert caught.value.error_id == str(caught.value) == error


@pytest.mark.parametrize("code", range(32))
def test_every_control_escape_exact(code):
    named = {8: r"\b", 9: r"\t", 10: r"\n", 12: r"\f", 13: r"\r"}
    escaped = named.get(code, f"\\u{code:04x}")
    expected = ('["baquant-pit-canonical-v1",["str","' + escaped + '"]]').encode()
    assert canonical_bytes(chr(code)) == expected


def test_literal_scalars_and_quote_backslash_slash():
    value = '"\\/\x7f\u2028\u2029\U0001f9ea'
    expected = (
        '["baquant-pit-canonical-v1",["str","\\"\\\\/\x7f\u2028\u2029\U0001f9ea"]]'
    ).encode("utf-8")
    assert canonical_bytes(value) == expected
    assert canonical_text(value).encode() == expected
    assert canonical_sha256(value) == sha256(expected).hexdigest()
    assert not expected.endswith(b"\n") and not expected.startswith(b"\xef\xbb\xbf")


def test_scalar_type_tags_and_unicode_identity():
    values = [
        None,
        False,
        0,
        "0",
        Decimal(0),
        date(2032, 4, 5),
        datetime(2032, 4, 5, tzinfo=UTC),
        [],
        {},
    ]
    assert len({canonical_bytes(v) for v in values}) == len(values)
    assert canonical_bytes("é") != canonical_bytes("e\u0301")
    assert canonical_bytes("Ａ") != canonical_bytes("A")
    assert canonical_bytes("A") != canonical_bytes("a")
    assert canonical_bytes(["date", "2032-04-05"]) != canonical_bytes(date(2032, 4, 5))


def test_unicode_map_sort_and_insertion_order():
    keys = ["\U00010000", "\ue000", "é", "e\u0301", "aa", "a", "A", ""]
    expected = ["", "A", "a", "aa", "e\u0301", "é", "\ue000", "\U00010000"]
    value = dict.fromkeys(keys)
    assert [key for key, _ in node(value)[1]] == expected
    assert canonical_bytes(value) == canonical_bytes(
        dict(reversed(list(value.items())))
    )
    assert canonical_bytes([1, 2]) != canonical_bytes([2, 1])


@pytest.mark.parametrize(
    "base,value",
    [
        (int, 1),
        (str, "x"),
        (float, 1.0),
        (list, []),
        (dict, {}),
        (Decimal, "1"),
        (date, (2032, 4, 5)),
        (datetime, (2032, 4, 5)),
    ],
)
def test_all_subclasses_rejected(base, value):
    cls = type("SyntheticSubclass", (base,), {})
    subject = cls(*value) if base in (date, datetime) else cls(value)
    fails(subject, "CANONICAL_UNSUPPORTED_TYPE")


@pytest.mark.parametrize("base,value", [(Enum, "x"), (IntEnum, 1), (StrEnum, "x")])
def test_enum_rejected(base, value):
    fails(base("SyntheticEnum", {"X": value}).X, "CANONICAL_UNSUPPORTED_TYPE")


@pytest.mark.parametrize(
    "value",
    [
        (),
        b"x",
        bytearray(b"x"),
        memoryview(b"x"),
        {1},
        frozenset({1}),
        object(),
        DateWindow(
            date(2032, 4, 5), date(2032, 4, 5), datetime(2032, 4, 5, tzinfo=UTC)
        ),
    ],
)
def test_other_types_rejected(value):
    fails(value, "CANONICAL_UNSUPPORTED_TYPE")


@pytest.mark.parametrize("value", [1.5, float("nan"), float("inf"), float("-inf")])
def test_all_float_rejected(value):
    fails(value, "CANONICAL_FLOAT_FORBIDDEN")


@pytest.mark.parametrize("text", ["NaN", "sNaN", "Infinity", "-Infinity", "NaN123"])
def test_nonfinite_decimal_rejected(text):
    fails(Decimal(text), "CANONICAL_NONFINITE_DECIMAL")


def test_decimal_scale_sign_and_context():
    with localcontext() as context:
        context.prec = 1
        assert node(Decimal("1.00")) == ["decimal", "0", "100", "-2"]
        assert node(Decimal("1.0")) == ["decimal", "0", "10", "-1"]
        assert node(Decimal("-0.00")) == ["decimal", "1", "0", "-2"]
        assert node(Decimal("0.00")) == ["decimal", "0", "0", "-2"]
        assert node(Decimal("1.20E-3")) == ["decimal", "0", "120", "-5"]
        assert node(Decimal("1E+3")) == ["decimal", "0", "1", "3"]


def test_ancestor_cycles_and_repeated_alias_nodes():
    child = []
    assert node([child, child]) == ["list", [["list", []], ["list", []]]]
    child.append(child)
    fails(child, "CANONICAL_CYCLE_DETECTED")
    mapping = {}
    mapping["x"] = [mapping]
    fails(mapping, "CANONICAL_CYCLE_DETECTED")
    shared = [None]
    canonical_bytes([shared] * 511)  # 1 + 511 * 2 = 1023, occurrences not identities.
    fails([shared] * 512, "CANONICAL_RESOURCE_LIMIT")


def test_depth_and_node_inclusive_boundaries():
    canonical_bytes(nested(16))
    fails(nested(17), "CANONICAL_RESOURCE_LIMIT")
    canonical_bytes([None] * 1023)
    fails([None] * 1024, "CANONICAL_RESOURCE_LIMIT")
    # Mapping keys contribute neither depth nor node occurrences.
    canonical_bytes({f"k{i}": None for i in range(1023)})
    fails({f"k{i}": None for i in range(1024)}, "CANONICAL_RESOURCE_LIMIT")


@pytest.mark.parametrize("value", ["x" * 4096, "é" * 2048, "\U00010000" * 1024])
def test_text_and_key_byte_limits(value):
    canonical_bytes(value)
    canonical_bytes({value: None})
    fails(value + "x", "CANONICAL_RESOURCE_LIMIT")
    fails({value + "x": None}, "CANONICAL_RESOURCE_LIMIT")


@pytest.mark.parametrize(
    "value", ["\ud800", "\udfff", "\ud800\udc00", "x" * 4097 + "\ud800"]
)
def test_surrogates_rejected_before_length(value):
    fails(value, "CANONICAL_INVALID_UNICODE")
    fails({value: None}, "CANONICAL_INVALID_UNICODE")


def test_integer_digits_independent_of_process_conversion_limit():
    original = sys.get_int_max_str_digits()
    try:
        sys.set_int_max_str_digits(640)
        value = 10**1023
        assert node(value) == ["int", "1" + "0" * 1023]
        assert node(-value) == ["int", "-1" + "0" * 1023]
        fails(10**1024, "CANONICAL_RESOURCE_LIMIT")
        fails(-(10**1024), "CANONICAL_RESOURCE_LIMIT")
    finally:
        sys.set_int_max_str_digits(original)


def test_decimal_coefficient_exponent_boundaries():
    assert node(Decimal((0, (1,) * 1024, 0)))[2] == "1" * 1024
    fails(Decimal((0, (1,) * 1025, 0)), "CANONICAL_RESOURCE_LIMIT")
    for exponent in (-1024, 1024):
        assert node(Decimal((0, (1,), exponent)))[3] == str(exponent)
    for exponent in (-1025, 1025):
        fails(Decimal((0, (1,), exponent)), "CANONICAL_RESOURCE_LIMIT")


def test_complete_envelope_inclusive_byte_limit():
    value = envelope_input(65536)
    assert len(canonical_bytes(value)) == 65536
    fails(envelope_input(65537), "CANONICAL_RESOURCE_LIMIT")
    # Escaping overhead is included even when each unescaped string is in bounds.
    fails(["\x00" * 4096] * 3, "CANONICAL_RESOURCE_LIMIT")


def test_key_validation_and_sorted_traversal_precedence():
    fails({"\ud800": None, 1: None}, "CANONICAL_INVALID_MAPPING_KEY")
    fails({"x" * 4097: None, "\ud800": None}, "CANONICAL_INVALID_UNICODE")
    fails({"z": 1.5, "a": object()}, "CANONICAL_UNSUPPORTED_TYPE")
    fails({"z": object(), "a": 1.5}, "CANONICAL_FLOAT_FORBIDDEN")
    fails({type("StringKey", (str,), {})("x"): None}, "CANONICAL_INVALID_MAPPING_KEY")
    fails([1.5, object()], "CANONICAL_FLOAT_FORBIDDEN")
    fails([object(), 1.5], "CANONICAL_UNSUPPORTED_TYPE")


def test_type_and_cycle_gates_precede_resource_and_envelope_last():
    fails(nested(17, object()), "CANONICAL_UNSUPPORTED_TYPE")
    cycle = []
    cycle.append(cycle)
    fails(nested(16, cycle), "CANONICAL_CYCLE_DETECTED")
    oversized_envelope = envelope_input(65537)
    fails(oversized_envelope + [object()], "CANONICAL_UNSUPPORTED_TYPE")


def test_unsupported_objects_never_format():
    class ForbiddenFormatting:
        def __str__(self):
            raise AssertionError("str fallback")

        def __repr__(self):
            raise AssertionError("repr fallback")

    fails(ForbiddenFormatting(), "CANONICAL_UNSUPPORTED_TYPE")
