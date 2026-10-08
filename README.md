# baquant-pit

Point-in-Time and Temporal Grounding Infrastructure for AI Financial Research.

**Current status: PRIVATE STAGING / PRE-EXTRACTION.**

This project originates from lessons and reusable infrastructure developed inside
the private BAquant research system. It is being designed as an independent,
provider-neutral and storage-neutral library.

This repository currently contains repository scaffolding and extraction/release
planning only. It does not yet contain the authoritative BAquant PIT implementation.
The importable package defines a development version; no PIT operations are
implemented, and no public API compatibility or scientific acceptance is claimed.

Future goals include typed temporal semantics, as-of queries, native versus
reconstructed vintages, revision awareness, look-ahead detection, temporal
validation, deterministic grounding, fail-closed unknown handling, synthetic
fixtures and reproducible tests. These are planning goals, not current features.

Out of scope are trading, brokerage, stock recommendations, proprietary BAquant
strategies, the BAquant production database, private market data and competition
assets. The originating research scope remains Shanghai/Shenzhen A shares
(`.SH` / `.SZ`), permanently excluding `.BJ`; this bootstrap adds no market support
and does not authorize expansion into other markets or asset classes.

Python 3.12 or newer is required. Local bootstrap validation:

```sh
python -m venv .venv
# Activate the virtual environment using your platform's standard command.
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

These checks validate packaging, import and specification asset consistency.
They do not execute PIT primitives. They use no market data,
providers, database, BAquant dependency or product LLM calls.

See the [extraction plan](docs/BAQUANT-PIT-PUBLIC-EXTRACTION-PLAN-V1.md),
[boundary](docs/PUBLIC_PRIVATE_BOUNDARY.md),
[architecture](docs/ARCHITECTURE.md),
[origin and authority](docs/ORIGIN_AND_AUTHORITY.md) and
[future release checklist](docs/PUBLIC_RELEASE_AUDIT_CHECKLIST.md).

The [minimal primitive semantics contract](contracts/minimal-primitives-v1.json)
and [versioning specification](docs/specs/compatibility-and-versioning-v1.md)
define a PRIVATE_REVIEW_CANDIDATE using newly authored synthetic vectors.
No runtime primitive is implemented, BAquant hash compatibility is NOT_CLAIMED,
and public API compatibility is NOT_ESTABLISHED.

The [minimal primitive semantics contract](contracts/minimal-primitives-v1.json)
and [versioning specification](docs/specs/compatibility-and-versioning-v1.md)
define a PRIVATE_REVIEW_CANDIDATE using newly authored synthetic vectors.
No runtime primitive is implemented, BAquant hash compatibility is NOT_CLAIMED,
and public API compatibility is NOT_ESTABLISHED.

No public redistribution or open-source license is granted at this stage.
The repository must remain private. Extraction, public visibility, a release and
package publication each require a separately scoped explicit Owner authorization.
