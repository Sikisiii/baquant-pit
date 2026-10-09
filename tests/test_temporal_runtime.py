"""Temporal boundary, precision, type and precedence conformance."""

from dataclasses import FrozenInstanceError
from datetime import UTC, date, datetime, timedelta, timezone

import pytest
from runtime_support import Offset

from baquant_pit import (
    BaquantPITError,
    DateWindow,
    format_utc_instant,
    normalize_utc_instant,
)

NOW = datetime(2032, 4, 5, 6, 7, 8, 123400, UTC)
DAY = date(2032, 4, 5)


@pytest.mark.parametrize(
    "offset",
    [timedelta(0), timedelta(hours=8), timedelta(hours=-5), timedelta(microseconds=1)],
)
def test_equivalent_offsets_and_precision(offset):
    source = (NOW + offset).replace(tzinfo=timezone(offset))
    assert normalize_utc_instant(source) == NOW
    assert normalize_utc_instant(source).tzinfo is UTC
    assert format_utc_instant(source) == "2032-04-05T06:07:08.123400Z"


@pytest.mark.parametrize(
    "value,error",
    [
        (None, "TEMPORAL_INVALID_TYPE"),
        (DAY, "TEMPORAL_INVALID_TYPE"),
        ("2032-04-05", "TEMPORAL_INVALID_TYPE"),
        (
            type("DateTimeSubclass", (datetime,), {})(2032, 4, 5, tzinfo=UTC),
            "TEMPORAL_INVALID_TYPE",
        ),
        (datetime(2032, 4, 5), "TEMPORAL_NAIVE_DATETIME"),
        (datetime(2032, 4, 5, tzinfo=Offset()), "TEMPORAL_NULL_OFFSET"),
        (datetime(2032, 4, 5, tzinfo=Offset(throws=True)), "TEMPORAL_INVALID_OFFSET"),
        (datetime(2032, 4, 5, tzinfo=Offset("invalid")), "TEMPORAL_INVALID_OFFSET"),
        (
            datetime(2032, 4, 5, tzinfo=Offset(timedelta(days=1))),
            "TEMPORAL_INVALID_OFFSET",
        ),
        (
            datetime(2032, 4, 5, tzinfo=Offset(timedelta(days=-1))),
            "TEMPORAL_INVALID_OFFSET",
        ),
        (
            datetime.min.replace(tzinfo=timezone(timedelta(microseconds=1))),
            "TEMPORAL_INSTANT_OUT_OF_RANGE",
        ),
        (
            datetime.max.replace(tzinfo=timezone(timedelta(microseconds=-1))),
            "TEMPORAL_INSTANT_OUT_OF_RANGE",
        ),
    ],
)
def test_instant_errors(value, error):
    for operation in (normalize_utc_instant, format_utc_instant):
        with pytest.raises(BaquantPITError) as caught:
            operation(value)
        assert caught.value.error_id == str(caught.value) == error


def test_resolve_once_and_extreme_valid_offsets():
    for delta in (
        timedelta(days=1) - timedelta(microseconds=1),
        -timedelta(days=1) + timedelta(microseconds=1),
    ):
        zone = Offset(delta)
        source = datetime(2032, 4, 5, tzinfo=zone)
        assert normalize_utc_instant(source) == datetime(2032, 4, 5, tzinfo=UTC) - delta
        assert zone.calls == 1


def test_minimum_maximum_year_text_and_fold():
    assert (
        format_utc_instant(datetime.min.replace(tzinfo=UTC))
        == "0001-01-01T00:00:00.000000Z"
    )
    assert (
        format_utc_instant(datetime.max.replace(tzinfo=UTC))
        == "9999-12-31T23:59:59.999999Z"
    )
    assert normalize_utc_instant(NOW.replace(fold=1)) == NOW


@pytest.mark.parametrize("field", ["start", "end", "cutoff"])
def test_window_normalized_immutable_and_inclusive(field):
    window = DateWindow(DAY, DAY, NOW.astimezone(timezone(timedelta(hours=8))))
    assert window.start == window.end == DAY
    assert window.cutoff == NOW and window.cutoff.tzinfo is UTC
    with pytest.raises(FrozenInstanceError):
        setattr(window, field, None)
    with pytest.raises(FrozenInstanceError):
        delattr(window, field)
    assert not hasattr(window, "__dict__")
    assert DateWindow(DAY, DAY, datetime(1990, 1, 1, tzinfo=UTC)).cutoff.year == 1990


@pytest.mark.parametrize(
    "args,error",
    [
        ((NOW, DAY), "TEMPORAL_INVALID_DATE"),
        ((DAY, NOW), "TEMPORAL_INVALID_DATE"),
        ((type("DateSubclass", (date,), {})(2032, 4, 5), DAY), "TEMPORAL_INVALID_DATE"),
        ((DAY, date(2032, 4, 4)), "TEMPORAL_WINDOW_REVERSED"),
        ((DAY, DAY), "TEMPORAL_CUTOFF_REQUIRED"),
        ((DAY, DAY, None), "TEMPORAL_CUTOFF_REQUIRED"),
        ((DAY, DAY, DAY), "TEMPORAL_INVALID_TYPE"),
        ((DAY, DAY, datetime(2032, 4, 5)), "TEMPORAL_NAIVE_DATETIME"),
    ],
)
def test_window_error_precedence(args, error):
    with pytest.raises(BaquantPITError) as caught:
        DateWindow(*args)
    assert caught.value.error_id == error
