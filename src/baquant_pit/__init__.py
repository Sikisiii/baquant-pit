"""Private implementation candidate for market-neutral temporal primitives."""

from .canonical import canonical_bytes, canonical_sha256, canonical_text
from .errors import (
    BaquantPITError,
    CanonicalizationError,
    RawIntegrityError,
    TemporalError,
)
from .integrity import sha256_bytes, sha256_file
from .temporal import DateWindow, format_utc_instant, normalize_utc_instant

__version__ = "0.0.0.dev0"

__all__ = [
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
]
