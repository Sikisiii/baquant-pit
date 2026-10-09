"""Safe Python exception binding for the private v1 semantic identifiers."""

_ERROR_IDS = frozenset(
    {
        "TEMPORAL_INVALID_TYPE",
        "TEMPORAL_NAIVE_DATETIME",
        "TEMPORAL_NULL_OFFSET",
        "TEMPORAL_INVALID_OFFSET",
        "TEMPORAL_INSTANT_OUT_OF_RANGE",
        "TEMPORAL_INVALID_DATE",
        "TEMPORAL_WINDOW_REVERSED",
        "TEMPORAL_CUTOFF_REQUIRED",
        "TEMPORAL_LEAP_SECOND_UNSUPPORTED",
        "CANONICAL_UNSUPPORTED_TYPE",
        "CANONICAL_FLOAT_FORBIDDEN",
        "CANONICAL_NONFINITE_DECIMAL",
        "CANONICAL_INVALID_MAPPING_KEY",
        "CANONICAL_DUPLICATE_MAPPING_KEY",
        "CANONICAL_INVALID_UNICODE",
        "CANONICAL_CYCLE_DETECTED",
        "CANONICAL_RESOURCE_LIMIT",
        "RAW_INVALID_BYTES_TYPE",
        "RAW_INVALID_PATH_TYPE",
        "RAW_FILE_NOT_FOUND",
        "RAW_FILE_NOT_REGULAR_FILE",
        "RAW_FILE_UNREADABLE",
        "RAW_FILE_IO_ERROR",
    }
)


class BaquantPITError(ValueError):
    """Expose an error ID without raw values, paths or underlying exception text."""

    def __init__(self, error_id: str) -> None:
        if type(error_id) is not str or error_id not in _ERROR_IDS:
            raise ValueError("Unknown semantic error ID")
        self._error_id = error_id
        super().__init__(error_id)

    @property
    def error_id(self) -> str:
        return self._error_id


class TemporalError(BaquantPITError):
    """Temporal v1 validation failure."""


class CanonicalizationError(BaquantPITError):
    """Canonical v1 validation failure."""


class RawIntegrityError(BaquantPITError):
    """Raw integrity v1 validation or filesystem failure."""
