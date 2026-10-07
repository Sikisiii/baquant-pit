# Intended independent architecture

Status: design only. The runtime contains only a package docstring and development
version. There are no readers, stores, trust snapshots, adapters or database
backends. The following pipeline is a prospective mental model, not an API:

```text
Raw Observation
        -> Temporal Metadata
        -> Availability / Knowledge Clock
        -> Vintage Classification
        -> As-Of Selection
        -> Temporal Validation
        -> Consumer-visible Result
```

The intended core would evaluate explicitly supplied observations and timing
evidence, preserve revisions and return deterministically justified results or
unknown/fail-closed outcomes. Provider acquisition and storage would remain
external, separately reviewed concerns. No DB, ORM, Alembic, ACL, writer, broker,
trading decision, production service or BAquant path belongs in the core.

## Candidate vocabulary, not exported fields

| Concept | Question for independent specification |
| --- | --- |
| `effective_time` | When does the described fact apply in its subject domain? |
| `published_at` | What evidence supports the source publication time? |
| `available_at` | When could the relevant consumer legitimately know it? |
| `observed_at` | Which observation process and clock does this timestamp describe? |
| `captured_at` | When were the recorded bytes captured? |
| `decision_time` | What explicit cutoff governs this consumer's query? |
| `revision_at` | What evidence identifies a revision and its knowledge time? |
| Native vintage | Is actual historical version/knowledge lineage established? |
| Reconstructed vintage | Which retrospective assumptions and revision limitations apply? |
| Current snapshot | Which capture does this represent, without assuming past availability? |
| Unknown timing | Which required timing claim lacks evidence? |
| Look-ahead violation | Does selected evidence rely on knowledge after the decision cutoff? |

These clocks must not be conflated. A capture/hash proves neither past knowledge
nor native vintage. Economic effective time need not be knowledge time. Intended
unknown handling is explicit and fail-closed for required timing; a passing
selection must never manufacture missing clock evidence. Exact timezone rules,
ordering, inclusivity, canonical serialization and errors require versioned
contracts and reproducible synthetic tests before implementation.

## Evolving areas

Typed clocks and deterministic hashing are stable origin concepts worth review,
not public compatibility promises. PIT grade policy, provider capture evidence
and market observation/vintage readers remain evolving. Stage63-specific
identity/classification, applicability and consumer-specific vintage qualification
are under redefinition and must not be frozen as generic public API.

Any future public semantics require independent review of scope, native versus
reconstructed lineage, revision preservation and consumer assumptions. BAquant
grades, defaults, acceptance gates or historical Stage outcomes are not inherited.
No algorithm, field schema or policy above has yet been implemented in this package.
