"""Market-neutral temporal v1 values, with explicit absolute cutoffs."""

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

from .errors import TemporalError

_MISSING = object()


def normalize_utc_instant(value: datetime) -> datetime:
    """Validate an exact aware datetime and preserve its instant in UTC."""
    if type(value) is not datetime:
        raise TemporalError("TEMPORAL_INVALID_TYPE")
    if value.tzinfo is None:
        raise TemporalError("TEMPORAL_NAIVE_DATETIME")
    try:
        resolved = value.utcoffset()
    except Exception:
        raise TemporalError("TEMPORAL_INVALID_OFFSET") from None
    if resolved is None:
        raise TemporalError("TEMPORAL_NULL_OFFSET")
    if not isinstance(resolved, timedelta):
        raise TemporalError("TEMPORAL_INVALID_OFFSET")
    # Read timedelta's intrinsic fields, not user-subclass arithmetic/formatting.
    offset = timedelta(
        days=timedelta.days.__get__(resolved),
        seconds=timedelta.seconds.__get__(resolved),
        microseconds=timedelta.microseconds.__get__(resolved),
    )
    if not -timedelta(days=1) < offset < timedelta(days=1):
        raise TemporalError("TEMPORAL_INVALID_OFFSET")
    try:
        # Use the already-resolved offset exactly once: no second tzinfo callback.
        return value.replace(tzinfo=UTC) - offset
    except OverflowError:
        raise TemporalError("TEMPORAL_INSTANT_OUT_OF_RANGE") from None


def format_utc_instant(value: datetime) -> str:
    """Return fixed six-fraction-digit UTC Z text, including padded year one."""
    instant = normalize_utc_instant(value)
    return (
        f"{instant.year:04d}-{instant.month:02d}-{instant.day:02d}T"
        f"{instant.hour:02d}:{instant.minute:02d}:{instant.second:02d}."
        f"{instant.microsecond:06d}Z"
    )


@dataclass(frozen=True, slots=True, init=False)
class DateWindow:
    """Immutable inclusive dates and mandatory UTC cutoff; no calendar authority."""

    start: date
    end: date
    cutoff: datetime

    def __init__(self, start: date, end: date, cutoff: datetime = _MISSING) -> None:
        # The sentinel permits a stable semantic missing-cutoff error, never a default.
        if type(start) is not date:
            raise TemporalError("TEMPORAL_INVALID_DATE")
        if type(end) is not date:
            raise TemporalError("TEMPORAL_INVALID_DATE")
        if start > end:
            raise TemporalError("TEMPORAL_WINDOW_REVERSED")
        if cutoff is _MISSING or cutoff is None:
            raise TemporalError("TEMPORAL_CUTOFF_REQUIRED")
        normalized = normalize_utc_instant(cutoff)
        object.__setattr__(self, "start", start)
        object.__setattr__(self, "end", end)
        object.__setattr__(self, "cutoff", normalized)
