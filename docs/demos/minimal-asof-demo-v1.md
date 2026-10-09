# Minimal as-of demo v1

Suppose an observation is revised tomorrow. A historical decision made today
must not see tomorrow's observation. This fully synthetic example prevents one
form of look-ahead bias by enforcing explicit knowledge-time visibility.

After installing from the complete repository or source distribution, run
from that source root:

```sh
python examples/minimal_asof_demo.py
python examples/minimal_asof_demo.py --json
```

## Synthetic timeline

| Observation | Value | available_at, UTC |
| --- | --- | --- |
| obs-001 | synthetic-a | 2032-04-05 09:00 |
| obs-002 | synthetic-b | 2032-04-05 12:00 |
| obs-003 | synthetic-c | 2032-04-06 09:00 |

```text
2032-04-05                                      2032-04-06
09:00          10:30          12:00              09:00
obs-001 -------| as_of |------obs-002 -----------obs-003
visible        |             future            future
```

At the explicit cutoff 2032-04-05T10:30:00+00:00, obs-001 is visible;
obs-002 and obs-003 are future excluded. Naive latest sees the full dataset and
chooses obs-003, leaking later knowledge backward into the earlier cutoff.

The example-local rule is visible iff normalized available_at <= normalized
as_of, including equality. It then selects the visible observation with greatest
available_at. This latest-visible rule is pedagogical, not production vintage
acceptance. No visible observation yields null, without inventing a default.
Different records tied at the latest visible instant fail closed with the local
DemoAmbiguousObservationError. A tied full-dataset maximum also refuses to name an
arbitrary naive latest. ID ordering is only for stable presentation/hashing,
never a tie-resolution rule. Neither error nor selection model enters the package API.

| Case | Explicit as_of, UTC | pit_as_of | future excluded |
| --- | --- | --- | --- |
| A, before first | 04-05 08:59:59.999999 | null | obs-001, obs-002, obs-003 |
| B, exact first | 04-05 09:00 | obs-001 | obs-002, obs-003 |
| C, between first/second | 04-05 10:30 | obs-001 | obs-002, obs-003 |
| D, exact second | 04-05 12:00 | obs-002 | obs-003 |
| E, after all | 04-06 09:00:00.000001 | obs-003 | none |

## Actual fixed example result

```text
baquant-pit minimal as-of demo
as_of: 2032-04-05T10:30:00.000000Z
naive latest: obs-003
point-in-time visible: obs-001
future observations excluded: obs-002, obs-003
result: LOOK_AHEAD_PREVENTED
input_digest: 8b09f590f49b975f53a1ca630657664269553bcc8a44f8265cf4c140862ac926
result_digest: 06c1a9e28c235f375ad7f78f76a6fa769655ad9f06c10abdd9d1684dbd9438b2
```

--json emits UTF-8 with sorted keys and an explicit LF, with no host paths,
wall-clock values or platform-specific variants. The
[non-normative receipt](../implementation/minimal-asof-demo-v1.json) records all
five cutoff expectations and the same fixed primary output/digests for both CI
platforms. Reordering source records or supplying an offset-equivalent cutoff
does not change that result. Tests run both the human command and actual JSON
subprocess twice, comparing complete bytes to the shared receipt.

## Primitives, validation and digest meaning

DemoObservation and its parser/selection helpers live only in examples/. ISO
parsing is an example adapter; every parsed available_at and explicit as_of is
validated/normalized by the existing normalize_utc_instant. format_utc_instant
provides the fixed UTC display. Naive timestamps retain the primitive semantic
error ID. Malformed fields/types, empty primary observations, missing cutoff or
duplicate observation IDs fail closed with fixed demo-local input errors.

Both hashes use the existing canonical_sha256. input_digest covers demo_id,
explicit UTC as_of and the normalized observations sorted by available_at/ID.
result_digest covers the displayed result fields before either digest is added.
Presentation JSON is not a second canonicalizer and is not the hash input.
The hashes prove deterministic content identity only. They do not prove truth,
authenticity, source authority, historical capture or accepted vintage.

This example only asks: was this synthetic observation available by this cutoff?
It does not solve source truth, provenance qualification, native-versus-
reconstructed vintage classification, acceptance authority, revision causality,
consumer-specific version policy, full PIT database access or backtest correctness.
It is not a production PIT reader, vintage acceptance engine, source authority
framework, database, adapter or trading system. There are no automatic decisions,
new runtime modules/public exports/dependencies or primitive semantic changes
introduced by the example. Package release metadata does not alter its payload.
Source is licensed under [Apache-2.0](../../LICENSE); version 0.1.0 remains PRIVATE
until separately authorized final publication. See
[current release state](../release/RELEASE_STATE.md).
