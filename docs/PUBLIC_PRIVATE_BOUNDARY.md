# Current content boundary

This non-normative guide describes the finalized 0.1.0 content scope.
Source is licensed under [Apache-2.0](../LICENSE); the repository remains PRIVATE
until the separately authorized final publication action. See
[current release state and publication gates](release/RELEASE_STATE.md).

## Included in the release candidate source

- Independently implemented generic temporal, canonicalization and raw/file
  integrity primitives with the existing twelve-name package API.
- Frozen v1 contract/specifications and newly authored synthetic golden vectors.
- Standalone tests, synthetic input helpers and explicit cross-platform accounting.
- The example-local synthetic as-of demo and its deterministic receipt.
- Current product documentation and clearly labelled historical development/audit
  material.

The wheel is a compact runtime distribution. The complete source distribution
includes test helpers, fixtures, contracts, examples and documentation required
for the source workflow; these are not runtime dependencies.

## Excluded content and capabilities

- Private BAquant implementation, coupled database models, migrations, writers,
  operational configuration and private source adapters.
- Credentials, environment secrets, private provider outputs and private logs.
- Licensed/private market datasets, paid research and copied financial statements.
- Proprietary strategies, portfolio data, prompts and competition assets.
- Production PIT readers, vintage engines, PIT grades, TrustSnapshot, consumer
  qualification, database/provider services, brokerage and trading.

Generic market-neutral primitives confer no exchange, market, asset-class or
provider support. Hash identity establishes neither source truth, historical
knowledge, native vintage, completeness nor redistribution rights. File integrity
provides no safe-root policy, locking or immutable snapshot guarantee.

The [frozen semantic authorities](specs/compatibility-and-versioning-v1.md) define
the existing implementation scope. The [origin guide](ORIGIN_AND_AUTHORITY.md)
explains independent authority. New inputs or functionality require separate
scope, provenance and semantic review; no automatic origin-project inheritance
or bulk implementation transfer is permitted by this document.
