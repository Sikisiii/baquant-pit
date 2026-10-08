# Compatibility and versioning v1

Contract: `baquant-pit-minimal-primitives`, version 1.
Status: `PRIVATE_REVIEW_CANDIDATE`.

| Statement | Value |
| --- | --- |
| baquant_compatibility | NOT_CLAIMED |
| public_api_compatibility | NOT_ESTABLISHED |
| public_release_authorized | false |
| canonical_format_id | baquant-pit-canonical-v1 |
| temporal_format_id | baquant-pit-temporal-v1 |
| raw_integrity_format_id | baquant-pit-raw-integrity-v1 |

This is independently authored CLEAN_REIMPLEMENTATION design inspired by a
read-only inventory of seven source symbols. No source implementation, source
tests, production fixtures or private payloads have been copied. Existing private
BAquant identities remain immutable. They are never retroactively reinterpreted,
converted or recomputed here. No byte compatibility with any existing BAquant
hash is claimed. A future compatibility/migration claim needs its own exhaustive
study, explicit versioned boundaries and separately scoped Owner authorization.

Canonical bytes are identity-critical. Any change in tags, envelope, text,
escaping, Unicode rules, Decimal quantum/sign, ordering or datetime bytes requires
a new canonical format ID and contract version. Changing accepted input domain,
reject behavior, resource bounds or list/tuple/Enum policy also requires a new
affected format ID and contract version, even when some previous bytes coincide.
A temporal rule change requires a new temporal format; if it changes canonical
datetime/date representation or acceptance it also requires a new canonical
format. File/symlink/raw-input/error rule changes require a new raw format and
contract version. A cross-format registry or downgrade fallback is not provided.

Changing only internal chunk size, streaming or allocation strategy while
preserving every accepted input/error/digest semantic does not require a format
bump. Operational failure is not permission to emit different bytes. Runtime API
names, exception class design and packaging for an implementation are deferred;
these gaps do not change the closed semantic input domain or recorded byte rules.

The v1 synthetic golden fixtures are normative for this private contract.
Future implementation must pass all valid/invalid vectors plus the stated full
rules before conformance can be considered. Passing asset-consistency tests
alone does not establish runtime behavior; digest recomputation of literal
bytes does not test a normalizer, time validator or file reader. Normative vector
corrections must be reviewed explicitly with impact on format identity assessed;
they cannot silently alter existing identities.

This remains private and pre-implementation, with no PUBLIC_STABLE,
BAQUANT_COMPATIBLE or PRODUCTION_ACCEPTED status. No public stability promise,
license, release, package publication or merge authorization is granted. No
runtime module is added. PIT grade, vintage acceptance, applicability or
classification, consumer qualification, providers, DB/Alembic/write authority,
TrustSnapshot and full artifact registry/manifest publishing remain excluded.

Machine policy is `contracts/minimal-primitives-v1.json` (not JSON Schema).
Normative specifications are `docs/specs/temporal-semantics-v1.md`,
`docs/specs/canonicalization-v1.md`, `docs/specs/raw-integrity-v1.md` and this file.
On disagreement between these assets, there is no silent winner: review is
blocked until they are reconciled within the authorized scope.
