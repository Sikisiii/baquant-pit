"""Bounded closed tagged canonical v1 representation, bytes and SHA-256."""

import json
from datetime import date, datetime
from decimal import Decimal
from hashlib import sha256

from .errors import CanonicalizationError
from .temporal import format_utc_instant

_FORMAT_ID = "baquant-pit-canonical-v1"
_MAX_DEPTH = 16
_MAX_NODES = 1024
_MAX_TEXT_BYTES = 4096
_MAX_DIGITS = 1024
_MAX_EXPONENT = 1024
_MAX_BYTES = 65536
_INT_BOUND = 10**_MAX_DIGITS
_TYPES = frozenset({type(None), bool, int, str, Decimal, date, datetime, list, dict})


def _resource_failure() -> None:
    raise CanonicalizationError("CANONICAL_RESOURCE_LIMIT")


def _unicode_check(text: str) -> None:
    if any(0xD800 <= ord(char) <= 0xDFFF for char in text):
        raise CanonicalizationError("CANONICAL_INVALID_UNICODE")


def _text_limit(text: str) -> None:
    if len(text) > _MAX_TEXT_BYTES or len(text.encode("utf-8")) > _MAX_TEXT_BYTES:
        _resource_failure()


def _integer_text(value: int) -> str:
    magnitude = abs(value)
    if magnitude >= _INT_BOUND:
        _resource_failure()
    if magnitude == 0:
        return "0"
    # Bounded chunks avoid dependence on Python's process-wide int-string limit.
    parts = []
    while magnitude:
        magnitude, tail = divmod(magnitude, 1_000_000_000)
        parts.append(tail)
    text = str(parts.pop()) + "".join(f"{part:09d}" for part in reversed(parts))
    return "-" + text if value < 0 else text


class _Normalizer:
    def __init__(self) -> None:
        self.nodes = 0
        self.ancestors: set[int] = set()

    def node(self, value: object, depth: int = 0) -> list:
        kind = type(value)
        if kind is float:
            raise CanonicalizationError("CANONICAL_FLOAT_FORBIDDEN")
        if kind not in _TYPES:
            raise CanonicalizationError("CANONICAL_UNSUPPORTED_TYPE")
        container = kind is list or kind is dict
        identity = id(value)
        if container and identity in self.ancestors:
            raise CanonicalizationError("CANONICAL_CYCLE_DETECTED")
        if depth > _MAX_DEPTH:
            _resource_failure()
        self.nodes += 1
        if self.nodes > _MAX_NODES:
            _resource_failure()
        if value is None:
            return ["null"]
        if kind is bool:
            return ["bool", value]
        if kind is int:
            return ["int", _integer_text(value)]
        if kind is str:
            _unicode_check(value)
            _text_limit(value)
            return ["str", value]
        if kind is Decimal:
            if not value.is_finite():
                raise CanonicalizationError("CANONICAL_NONFINITE_DECIMAL")
            sign, digits, exponent = value.as_tuple()
            if (
                len(digits) > _MAX_DIGITS
                or not -_MAX_EXPONENT <= exponent <= _MAX_EXPONENT
            ):
                _resource_failure()
            coefficient = "".join(chr(48 + digit) for digit in digits)
            return ["decimal", str(sign), coefficient, str(exponent)]
        if kind is date:
            return ["date", value.isoformat()]
        if kind is datetime:
            return ["datetime", format_utc_instant(value)]
        self.ancestors.add(identity)
        try:
            if kind is list:
                return ["list", [self.node(child, depth + 1) for child in value]]
            # All key type gates precede Unicode/size, regardless of insertion order.
            keys = list(value)
            if any(type(key) is not str for key in keys):
                raise CanonicalizationError("CANONICAL_INVALID_MAPPING_KEY")
            for key in keys:
                _unicode_check(key)
            # Exact dict has unique strings; upstream duplicates are unrecoverable.
            for key in keys:
                _text_limit(key)
            return [
                "map",
                [[key, self.node(value[key], depth + 1)] for key in sorted(keys)],
            ]
        finally:
            self.ancestors.remove(identity)


def canonical_bytes(value: object) -> bytes:
    """Render the private v1 format envelope after normative type/resource gates."""
    node = _Normalizer().node(value)
    rendered = json.dumps(
        [_FORMAT_ID, node], ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    if len(rendered) > _MAX_BYTES:
        _resource_failure()
    return rendered


def canonical_text(value: object) -> str:
    """Strict UTF-8 text of canonical_bytes, without a terminal newline."""
    return canonical_bytes(value).decode("utf-8")


def canonical_sha256(value: object) -> str:
    """Hash exactly the canonical envelope bytes; add no salt/key/namespace."""
    return sha256(canonical_bytes(value)).hexdigest()
