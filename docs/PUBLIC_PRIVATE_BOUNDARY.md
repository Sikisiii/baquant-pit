# Public/private boundary

Status: planning only, private pre-extraction staging. A candidate classification
does not grant extraction or redistribution permission. No source implementation,
production fixture or BAquant contract has been imported into this repository.

## Safe candidates for future extraction

Subject to provenance, rights, semantic and dependency review:

- Generic temporal types and clock semantics.
- Canonical hashing helpers and generic raw artifact integrity primitives.
- Generic as-of rules and vintage models.
- Generic look-ahead validators and temporal validation.
- Provider-neutral interfaces and storage-neutral interfaces.
- Newly authored synthetic fixtures, standalone tests and generic machine contracts.

Hash integrity alone does not establish truth, original knowledge time, native
vintage qualification, completeness or redistribution rights.

## Private / do not extract

- Secrets, API tokens, webhooks, DSNs, credentials and local environment files.
- Real provider credentials and BAquant-specific operational configuration.
- Real database dumps, backup images and production snapshots.
- Licensed market data, paid research and copyrighted reports.
- Real evidence payloads unless independently proven redistributable and explicitly
  admitted by a separate review and authorization.
- Competition submission material and Golden Case.
- Proprietary alpha, strategy members, factor/strategy research and outputs.
- Private portfolio data, private run artifacts and private snapshot identifiers.
- User/personal data and proprietary model prompts.
- BAquant DB models, Alembic/migrations, ACL/writers, deployment paths and private
  source adapters. Their general concepts require a clean independent design.

## Requires case-by-case review

- BAquant contracts and PIT policies; no wholesale copying or automatic adoption.
- Source adapters and provider-specific semantics.
- Evidence manifests and DB-independent validation logic.
- Reconstructed availability rules and consumer-specific vintage qualification.

## Readiness and evolving areas

| Design input class | Planning disposition |
| --- | --- |
| Stable current concepts | Typed clocks, canonical/deterministic hashing and raw artifact integrity are candidates for independent review, not extracted features. |
| Current but evolving | PIT grade policy, provider capture evidence and market observation/vintage readers need semantic and coupling review. |
| Stage63 under redefinition | Identity/classification, applicability and consumer-specific vintage qualification must not be frozen as generic public API. |
| Private coupled | DB models, Alembic, ACL/writers, repository paths, BAquant consumer rules and source adapters remain outside extraction. |
| Public package not yet implemented | Standalone useful PIT functionality, exported operations, public compatibility acceptance and public release remain future work. |

Only the empty package scaffold can presently be installed. Future extraction
must select the smallest justified component, remove coupling from the start and
use synthetic evidence. No historical acceptance, current provider snapshot or
passing bootstrap test upgrades these classifications.
