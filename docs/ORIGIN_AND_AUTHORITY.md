# Origin and authority

baquant-pit originated from reusable temporal-grounding work developed while
building the private BAquant research system. It is an independent repository
and infrastructure library informed by those research lessons. Its minimal
runtime was independently written from the baquant-pit contract, specifications
and synthetic golden vectors; the private BAquant implementation was not
consulted or copied. Private implementation and source-inspection evidence are
outside this repository's distributable content.

## Independent scope

The originating research project had a narrower market scope. baquant-pit is
market-neutral: these primitives imply no support for a particular exchange,
security market, asset class or provider. Market-specific rules belong in
downstream consumers. This library does not change the origin project's scope.

BAquant compatibility is **NOT_CLAIMED**. Public API compatibility is
**NOT_ESTABLISHED**. Origin business acceptance and consumer qualifications are
not inherited. Tests establish only their declared technical scope and do not
grant redistribution rights, scientific acceptance or permission to trade.

## Semantic authority and current status

The [v1 contract](../contracts/minimal-primitives-v1.json),
[normative specifications](specs/compatibility-and-versioning-v1.md) and synthetic
golden expectations define the minimal primitive semantics. Their frozen text
preserves design-time implementation/status statements. Current implementation
and release status are explained in [RELEASE_STATE](release/RELEASE_STATE.md),
a non-normative guide that does not override the semantic authorities.

The runtime, synthetic conformance suite and example-local as-of demonstration
exist. Production readers, vintage qualification, PIT grades and other consumer
policies remain outside the implemented scope.

## Publication boundary

The repository is PRIVATE during release candidate preparation and remains
pre-release at `0.0.0.dev0`. No open-source redistribution license has yet been
selected; private access alone grants no redistribution rights. License selection,
first public version and historical identity acceptance remain Owner decisions.
Any publication requires separate final authorization. The completed
[readiness audit](release/public-release-audit-v1.md) records evidence at its
stated historical commit, not a legal guarantee or publication authorization.
