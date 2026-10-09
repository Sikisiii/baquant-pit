# Minimal primitives v1 implementation candidate

Status: PRIVATE IMPLEMENTATION CANDIDATE / PRE-RELEASE. Version: `0.0.0.dev0`.
Authority: merged baquant-pit v1 contract, specifications and synthetic goldens.
This is an independent implementation; private BAquant implementation source was
not consulted or copied. Compatibility is not claimed and no license is added.

## Python binding

| Module | Public binding |
| --- | --- |
| temporal | `normalize_utc_instant`, `format_utc_instant`, `DateWindow` |
| canonical | `canonical_bytes`, `canonical_text`, `canonical_sha256` |
| integrity | `sha256_bytes`, `sha256_file` |
| errors | `BaquantPITError`, `TemporalError`, `CanonicalizationError`, `RawIntegrityError` |

Only these 12 names are in package `__all__`. Internal helpers remain internal.
Every semantic failure exposes an existing contract `error_id`; default text is
only that ID. Underlying offset and filesystem diagnostics are suppressed.

Temporal normalization resolves the explicit offset once, preserves microseconds
and validates UTC overflow. Window endpoints are exact dates, inclusive, ordered
and immutable; cutoff is mandatory and stored in UTC. There is no parser, implicit
clock, calendar authority or date-to-midnight conversion.

Canonical rendering uses the closed positional tagged grammar, exact Python
types, scalar Unicode ordering, preserved Decimal tuple scale/sign, active
ancestor cycle detection and occurrence counting. Exhaustive tests prove all
32 control escapes plus quote, backslash, slash, DEL, U+2028/U+2029 and
supplementary scalar rendering. The complete UTF-8 envelope is hashed unchanged.
Integer conversion uses small decimal chunks so a lower process-wide integer
string conversion setting cannot reduce the normative 1024-digit limit.

Raw hashing accepts exact bytes only. File hashing accepts native path text or
the native standard Path class, rejects arbitrary subclasses/path protocols and
NUL, follows links to regular files and reads binary chunks until EOF. Stat/open/
read failures are classified to existing IDs, with no partial digest or raw path
in public text. File identity contains neither path nor metadata. No safe-root,
snapshot, locking or TOCTOU guarantee is made.

## Conformance accounting

All 116 golden IDs appear exactly once in the
[coverage table](golden-runtime-coverage-v1.json):

| Classification | Count | Treatment |
| --- | ---: | --- |
| RUNTIME_EXECUTABLE | 113 | Real API calls; 66 valid outputs and 47 invalid error IDs |
| CONCEPTUAL_NONEXECUTABLE | 2 | T109: Python datetime cannot represent second 60; C117: duplicate keys lost before dict construction |
| PLATFORM_CONDITIONAL | 1 | F104: actual FIFO where native creation is available |

No IDs are uncovered. Synthetic bounded descriptors are materialized into actual
Python values rather than skipped. T006 tests canonical date identity and instant
rejection. T009-T011 normalize both instants and test the normative inclusive
relation without adding a reader API. F103 uses controlled permission failure;
F105 reads a partial chunk then fails before EOF through the actual file API.
Those injections validate error mapping, not host permissions or durability.

Local validation collects 336 tests: 55 unchanged asset/import test items and
281 new runtime/conformance test items. On Windows, 329 pass and 7 skip: the two
conceptual golden IDs, the conditional FIFO and four native symlink scenarios
when link creation is unavailable. Runtime golden results are 113 passed / 3
accounted skips; generic runtime tests are distinct from asset consistency.
POSIX CI also executes the conditional FIFO and native symlink tests when
supported. Ruff check, Ruff format check, pytest and diff check are required.

Boundary tests prove inclusive depth 16, node count 1024, UTF-8 scalar/key 4096
bytes, integer/Decimal coefficient 1024 digits, Decimal exponent [-1024,1024]
and complete canonical bytes 65536. Tests also prove over-bound rejection,
validation/traversal precedence, alias occurrence counting and final byte-limit
ordering. There are no lower implementation caps.

The implementation-presence flag is set true only after runtime conformance
succeeds. The matching asset status assertion is updated from false to true;
all other old asset assertions are preserved. No golden expected values,
normative specification text, format ID, semantic rule or resource limit changes.
Design-time wording in frozen artifacts remains historical context.

Excluded: PIT grade, vintage selection, applicability/classification, TrustSnapshot,
DB, providers, product LLM calls, manifests, safe-root/atomic publication and
trading. No release, PyPI publication, public visibility or API stability is
established. Review this candidate before any separately authorized merge.
