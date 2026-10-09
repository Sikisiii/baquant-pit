# HISTORICAL DEVELOPMENT PLAN

This document records the original private extraction/bootstrap sequence and is
retained for provenance and development history. It is not current product
documentation and defines neither current authority nor runtime behavior.
The plan below preserves the original planning state; origin-specific process
labels have been generalized without adding implementation or private evidence.
See [current release state](../release/RELEASE_STATE.md) for the implemented scope
and [completed readiness audit](../release/public-release-audit-v1.md) for the
subsequent assessment. No history is erased by this move.

## Original plan (historical)

Status: PRIVATE STAGING / PRE-EXTRACTION. This document is a future plan, not an
authorization or claim of implemented temporal behavior. The bootstrap task stops
at the private repository foundation. BAquant remains private.

The intended route is private BAquant origin, future clean extraction into private
baquant-pit staging, independent public release audit, then an explicitly
authorized reusable public package. No public step is authorized now.

Future sequence:

1. Inventory authoritative BAquant PIT implementation and record its exact source
   commit/ref in private planning evidence.
2. Confirm current semantics, authority and superseded paths. Separate stable
   primitives, evolving PIT policies and consumer-specific qualification.
3. Establish the public/private boundary with rights and dependency review.
4. Run a public release audit of the selected inputs and staging contents.
5. Select the minimum reusable components justified by the reviewed inventory.
6. Reimplement/extract approved components into the clean `baquant_pit` namespace
   and separate repository from the beginning.
7. Remove BAquant coupling: DB models, Alembic, ACL/writers, paths, operational
   configuration, private consumers and proprietary research.
8. Make the selected behavior provider-neutral; keep provider-specific evidence
   assumptions explicit and independently reviewed.
9. Make it storage-neutral without importing a BAquant database/backend.
10. Add newly authored synthetic fixtures with no real source payloads.
11. Add standalone positive and fail-closed tests, deterministic replay and
    semantic compatibility checks for the selected surface.
12. Add minimal docs/demo describing implemented limits and unknown timing.
13. Perform an independent release audit of the working tree, entire Git history,
    metadata, examples, dependencies and generated/CI artifacts.
14. Only after explicit Owner authorization consider public visibility.
15. Only after explicit Owner authorization consider v0.1.0; package publication
    requires its own explicit authorization and distribution review.

This is clean extraction into a separate repository from the beginning. It is
never a bulk copy followed by later cleanup. No BAquant Git history, filtered
history, subtree, fork, template, production code or wholesale contracts are
admitted by this plan. Every future component needs an approved scope and
traceable semantic decision before any implementation transfer.

Versioned baquant-pit contracts and tests must establish independent authority.
Historical BAquant business status is not inherited. Provider-neutral or
storage-neutral design does not authorize broader asset/market support.
