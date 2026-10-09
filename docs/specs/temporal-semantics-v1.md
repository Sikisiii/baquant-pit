# Temporal semantics v1

Format: `baquant-pit-temporal-v1`. Contract: `baquant-pit-minimal-primitives`,
version 1. Status: `PRIVATE_REVIEW_CANDIDATE`. This document is normative for
the private design; no runtime primitive is provided.

## Instant and normalization

A valid instant is an explicitly aware datetime. The Python binding accepts an
exact built-in datetime, not a date, string, subclass or implicit conversion.
Its tzinfo must be present and its utcoffset() for that value must be non-null.
The supplied resolved offset must be a duration strictly between -24 and +24
hours, with integer-microsecond precision. Custom tzinfo is allowed only when it
provides that stable valid offset. The caller supplies any fold/zone resolution;
this layer does not resolve ambiguous local times, load named business zones or
certify that a supplied local timestamp is historically correct.

Normalize the represented absolute instant to UTC, without rounding. Normalized
Gregorian years must be 0001 through 9999. Overflow during UTC conversion fails.
Offset-equivalent values yield identical UTC values and text. There are no
wall-clock defaults, zone-name defaults, date-to-midnight conversions, hidden
end-of-day conversions or market-time rules. This is market-neutral design and
does not expand any originating project's market authorization.

Canonical instant text is exactly `YYYY-MM-DDTHH:MM:SS.ffffffZ`: four-digit year,
two-digit month/day/hour/minute/second, uppercase T/Z, dot followed by exactly six
fractional digits. Zero fractions use `.000000`; trailing zeros are retained.
Precision is integer microseconds, with neither truncation nor rounding. Leap
seconds (second 60) are unsupported and rejected. A future text-input adapter,
if separately designed, must not silently accept a leap second; v1 supplies no
datetime string parser. Gregorian date and clock validity are prerequisites.

## Dates and windows

A date is an exact built-in date, excluding datetime even though Python relates
the types by inheritance. It is a proleptic Gregorian calendar date in years
0001..9999, represented `YYYY-MM-DD`, and has no timezone or implied instant.

The window has start and end dates with start <= end. Both endpoints are
inclusive. Equal dates denote a valid one-date window. The window carries a
required aware decision cutoff, normalized to UTC on construction. Its three
values are immutable: no assignment or in-place mutation after successful
construction. No default value is allowed for cutoff, including None. It has
no exchange-calendar, session, open-day, coverage, security or universe meaning.
There is no implied relation between either date and the cutoff's UTC date.

Where a caller compares an explicit knowledge instant with the cutoff, the
inclusive relation is instant <= cutoff, so equality qualifies for that relation.
This is a boundary convention, not an additional reader API or a claim of
historical availability, vintage acceptance, truth or authorization. The window
object is not an accepted canonicalization input type; callers must provide an
explicit supported value if they later require a content digest.

## Errors and deterministic validation order

Semantic identifiers are independent of future Python exception class names.
For an instant: invalid input type -> TEMPORAL_INVALID_TYPE; absent tzinfo ->
TEMPORAL_NAIVE_DATETIME; null offset -> TEMPORAL_NULL_OFFSET; invalid/throwing
offset -> TEMPORAL_INVALID_OFFSET; conversion outside supported UTC range ->
TEMPORAL_INSTANT_OUT_OF_RANGE. TEMPORAL_LEAP_SECOND_UNSUPPORTED covers the
conceptual non-representable second-60 value, not a promised string parser.

For a window: validate start then end as exact valid dates
(TEMPORAL_INVALID_DATE), then their order (TEMPORAL_WINDOW_REVERSED), then the
required cutoff (TEMPORAL_CUTOFF_REQUIRED for omission/None), then its instant
rules. Date-only cutoff is TEMPORAL_INVALID_TYPE. No source-project exceptions
are imported. No failed result or silently substituted time is returned.

## Normative examples

`2032-04-05T06:07:08+00:00`, `2032-04-05T14:07:08+08:00` and
`2032-04-05T01:07:08-05:00` all produce `2032-04-05T06:07:08.000000Z`.
`.123400` retains all six digits. The date `2032-04-05` remains a date, never
midnight. Newly authored positive/negative records are in
`tests/fixtures/golden/temporal-v1.json` with format `baquant-pit-temporal-v1`.
These are declarative design vectors, not executed runtime conformance results.
