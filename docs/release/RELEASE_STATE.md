# Current release state

**PRIVATE RELEASE CANDIDATE PREPARATION / PRE-RELEASE**

This is the current user-facing implementation/status guide. It is non-normative:
it does not define new semantics, grant a license or authorize publication.
The repository remains PRIVATE and the package version remains `0.0.0.dev0`.

## What is implemented

- Minimal primitives v1: explicit aware-datetime normalization/fixed UTC text,
  immutable inclusive date windows with mandatory cutoff, bounded typed canonical
  bytes/text/SHA-256, exact bytes SHA-256 and streamed regular-file content SHA-256.
- Exactly twelve package exports, using only the Python standard library.
- Synthetic golden conformance with explicit conceptual/platform accounting.
  Windows and Ubuntu/Linux validation covers Python 3.12; `>=3.12` is the package's
  minimum-version constraint, not evidence that later Python versions were tested.
- An example-local [minimal as-of demo](../demos/minimal-asof-demo-v1.md) with an
  explicit synthetic cutoff, inclusive visibility, ambiguous-maximum failure and
  deterministic output. It adds no production reader API.

Public API compatibility is **NOT_ESTABLISHED**. BAquant compatibility is
**NOT_CLAIMED**. There is no production PIT reader, vintage engine, PIT grade,
TrustSnapshot, applicability classification, database/provider adapter, manifest
registry, broker or trading functionality. Passing tests does not establish
production readiness, scientific acceptance or source authenticity.

## Frozen semantics and historical wording

The [minimal contract](../../contracts/minimal-primitives-v1.json),
[v1 specifications](../specs/compatibility-and-versioning-v1.md) and synthetic
goldens remain the frozen semantic authorities. Their types, formats, expected
bytes, error IDs and resource limits are unchanged.

Some prose and status fields record the original private design-time state,
including statements that runtime implementation was deferred or absent. Those
historical statements are not evidence that today's runtime is missing. The
current package and implementation documentation describe implementation presence;
this guide explains that distinction without overriding or silently rewriting v1.
Historical receipt statuses and test totals describe their recorded scope.

The completed [public-release readiness audit](public-release-audit-v1.md) and
[audit JSON](public-release-audit-v1.json) describe their stated historical SHA.
They remain unchanged assessments, not today's publication state or a release
authorization. The non-normative [preparation receipt](release-preparation-v1.json)
records the scope and observed acceptance of this preparation work.

## Source and package workflows

The repository and coherent source distribution contain the complete tests,
support module, synthetic fixtures, contract, specifications, examples and linked
documentation. From either source root, use the
[documented environment/install/validation workflow](../../README.md). The source
distribution must run its shipped tests and both demo commands without reaching
back to another checkout.

The wheel contains runtime modules and package metadata. It supports ordinary
library import from outside the source tree and does not bundle tests, docs,
examples or contracts as runtime assets. The current version is identical for
editable, ordinary, wheel and source-distribution installation.

README links intentionally resolve in the GitHub repository and complete source
bundle. **PYPI_DOCUMENT_RENDERING_NOT_YET_ACCEPTED**: the embedded README retains
repository-relative links, whose rendering on a package index has not been
accepted. PyPI publication is optional, separately scoped and is not part of the
first public-repository preparation acceptance. No package-index publication is
authorized by removing the private-upload classifier.

## Decisions and final actions still pending

| Gate | Current state |
| --- | --- |
| OWNER_LICENSE_DECISION | OWNER_DECISION_PENDING: no open-source redistribution license selected. |
| OWNER_VERSION_DECISION | OWNER_DECISION_PENDING: the actual version stays `0.0.0.dev0`. |
| OWNER_IDENTITY_ACCEPTANCE | OWNER_REVIEW_REQUIRED / OWNER_IDENTITY_ACCEPTANCE_PENDING: historical commit identity exposure requires acceptance; no values are reproduced here. |
| FINAL_RELEASE_AUTHORIZATION | Separate explicit Owner authorization required. |
| PUBLIC_VISIBILITY_ACTION | Repository remains PRIVATE; a separately authorized final action is required. |

Private repository access does not itself grant redistribution rights. Once the
Owner makes the exact license/version decisions, a separately authorized final
release step must apply them consistently to the license file, package metadata,
version and user-facing status. No license, final version or identity decision is
selected by this preparation. Historical commit metadata is not rewritten.

## Documentation map

Current guides: [architecture](../ARCHITECTURE.md),
[origin and authority](../ORIGIN_AND_AUTHORITY.md),
[content boundary](../PUBLIC_PRIVATE_BOUNDARY.md),
[implementation](../implementation/minimal-primitives-v1.md) and
[cross-platform conformance](../implementation/cross-platform-conformance-v1.md).

Historical context, not product instructions:
[original development/extraction plan](../history/BAQUANT-PIT-PUBLIC-EXTRACTION-PLAN-V1.md)
and [original release-audit checklist](../history/PUBLIC_RELEASE_AUDIT_CHECKLIST.md).
These preserve development history without defining current authority or runtime
behavior. Moving them does not remove their prior Git history.
