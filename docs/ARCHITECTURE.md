# Current architecture

This non-normative guide describes the implemented minimal primitives v1.
See [release state](release/RELEASE_STATE.md) for current status and the distinction
between frozen semantic authority and historical design-time wording.

## Implemented runtime

The package uses Python's standard library and exports exactly twelve names.

| Component | Implemented responsibility | Boundary |
| --- | --- | --- |
| Temporal | `normalize_utc_instant`, `format_utc_instant`, immutable `DateWindow` | Exact aware datetimes; explicit cutoff; inclusive date endpoints; no parser, implicit clock or calendar authority. |
| Canonicalization | `canonical_bytes`, `canonical_text`, `canonical_sha256` | Frozen bounded tagged representation of exact supported types; no coercion or repr fallback. |
| Raw integrity | `sha256_bytes`, `sha256_file` | Exact bytes and streamed regular-file content; no path/metadata in identity. |
| Errors | `BaquantPITError`, `TemporalError`, `CanonicalizationError`, `RawIntegrityError` | Existing semantic error IDs and fixed safe text. |

```text
Explicit values -> temporal validation / typed canonical representation
                -> canonical bytes / text / content digest
Exact bytes or regular-file content -> raw content digest
Synthetic observations + explicit cutoff -> example-local as-of demonstration
```

Canonical datetime values use the temporal formatter. Raw/file hashing does not
use the canonical envelope. File hashing follows links to regular files and
commits to bytes read through EOF; it does not provide a trusted root, immutable
snapshot, locking, TOCTOU protection or authenticity. A hash establishes content
identity, not truth, historical availability, source authority or accepted vintage.

The [contract](../contracts/minimal-primitives-v1.json) and
[frozen specifications](specs/compatibility-and-versioning-v1.md) define the exact
types, byte formats, limits and error ordering. This architecture guide does not
add or change those rules.

## Validation and example layer

Three synthetic golden fixture files supply 116 versioned vector expectations.
The [coverage table](implementation/golden-runtime-coverage-v1.json) distinguishes
executable vectors from conceptual Python-input exclusions and native platform
conditions. The complete suite runs on Windows and Ubuntu/Linux with Python 3.12;
see [conformance boundaries](implementation/cross-platform-conformance-v1.md).

The [minimal as-of example](demos/minimal-asof-demo-v1.md) normalizes supplied
knowledge times and applies `available_at <= as_of`, selecting a unique latest
visible observation. It rejects ambiguous maxima and keeps parsing/selection
outside the package API. Its synthetic timeline and deterministic receipt do not
establish a production reader or vintage-acceptance policy.

## Future concepts outside the current implementation

Production PIT readers, vintage engines, PIT grades, applicability/classification,
TrustSnapshot, database/provider adapters, manifest registries, atomic publication
and trading are absent. Any future timing model must distinguish effective,
published, available, observed, captured, decision and revision times; these are
discussion concepts, not exported fields or an accepted schema.

The library is market-neutral. It inherits no origin-project business acceptance,
market authorization, provider policy or compatibility guarantee. A future
extension requires its own design and review; this document promises none.
