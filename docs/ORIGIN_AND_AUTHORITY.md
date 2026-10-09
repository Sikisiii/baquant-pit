# Origin and authority

baquant-pit originated from reusable temporal-grounding work developed while
building the private BAquant research system. It is an independent infrastructure
library informed by those research lessons. Its current minimal runtime was
independently written from the merged baquant-pit contract, specifications and
synthetic golden vectors; the private BAquant implementation was not consulted
or copied. Source inspection details remain outside distributable package content.

## Historical research scope

BAquant itself had a narrower Shanghai/Shenzhen China A-share research scope
(`.SH` / `.SZ`), permanently excluding `.BJ`. That originating scope is not
inherited by baquant-pit. baquant-pit is intentionally market-neutral: no support
for any exchange, security market, asset class or provider follows merely from
these library primitives. Market-specific rules belong in downstream consumers.
This distinction does not expand BAquant's own permissions or research scope.

## Independent semantics and bounded authority

BAquant historical implementation is not automatically the public API. Public
API semantics require independent review. Origin business status and consumer
qualifications remain with the private origin project. Tests establish only
their declared technical scope; they do not authorize business acceptance,
redistribution, release or market support.

The merged private v1 contract, normative specifications and synthetic golden
expectations define the minimal primitives here. Cross-platform conformance
tests validate that existing scope; they do not redesign it or authorize new
runtime functionality. Public API stability and BAquant compatibility are not
established. Evolving identity/classification, applicability and consumer-specific
vintage semantics require independent decisions and explicit authorization.

No redistribution or open-source license is granted. The repository remains
private. Any merge, visibility change, release or package publication requires
separately scoped Owner authorization and applicable audits.
