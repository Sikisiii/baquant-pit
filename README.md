# baquant-pit

**English** | [简体中文](README.zh-CN.md)

**Historical research should only use information available at the time.**

Python building blocks for Point-in-Time financial research.

**Current status: PUBLIC / OPEN SOURCE / 0.1.0** — early Alpha

## Why this exists

A historical strategy can look convincing when it accidentally uses tomorrow's
information. baquant-pit offers time and hashing utilities, plus an offline
example that exposes this mistake.

## A simple example

Consider these **synthetic** company figures:

| Information becomes available | Reported profit |
| --- | --- |
| June 20 | 100 million |
| August 10 | Revised to 70 million |

For a June 30 decision, today's latest value is 70 million; only 100 million
was known then. Using the later revision is *look-ahead bias*, or *future-data
leakage*. This conceptual example is not a supplied financial dataset.

## What Point-in-Time means

Point-in-Time (PIT) asks: **what was available by a historical cutoff?** This is
an *as-of* view. A report about June published in August was unavailable in June.
Callers supply availability times; the library cannot infer them from values.

## Why AI financial research needs this

A research agent can combine documents and latest database values into a plausible
historical answer containing information nobody had then. Explicit availability
times matter even when the answer sounds correct.

This is motivation, not implemented agent, LLM, retrieval or RAG functionality.

## What baquant-pit provides today

- Express timezone-aware timestamps consistently: UTC normalization and fixed text.
- Store inclusive dates with an explicit cutoff: immutable `DateWindow`, without
  record filtering.
- Identify supported inputs reproducibly: typed bytes/text (*canonicalization*)
  and SHA-256, plus raw bytes and file-content hashes.

These primitives are not a production PIT reader or revision database.

## 30-second demo

After [setup](#installation-and-development), compare naive latest across all
observations with selection available by the cutoff, including equality:

```sh
python examples/minimal_asof_demo.py
python examples/minimal_asof_demo.py --json
```

Key output:

```text
as_of: 2032-04-05T10:30:00.000000Z
naive latest: obs-003
point-in-time visible: obs-001
future observations excluded: obs-002, obs-003
```

Selection is example-local, not a package API. See the
[synthetic timeline and ambiguity rules](docs/demos/minimal-asof-demo-v1.md).

## Minimal Python example

Record a cutoff and identify the input, without querying data:

```python
from datetime import UTC, date, datetime

from baquant_pit import DateWindow, canonical_sha256

window = DateWindow(
    date(2032, 4, 4), date(2032, 4, 6), datetime(2032, 4, 5, tzinfo=UTC)
)
payload = {"cutoff": window.cutoff, "label": "synthetic"}
print(canonical_sha256(payload))
```

`DateWindow` is not itself a canonical input. Hashes identify content, not truth,
authenticity or historical availability.

## What this project is not

- No production PIT database, full revision-history (vintage) engine or data provider.
- No backtesting framework, market calendar, portfolio engine, trading system
  or brokerage integration.
- No complete research or AI-agent platform, production readiness or backtest
  correctness guarantee.

Market-neutral primitives confer no exchange, asset-class or provider support.
Private data, strategies and competition assets are excluded.

## Technical guarantees and boundaries

- Standard-library runtime; Python **>=3.12**, tested on **3.12, Windows and
  Ubuntu/Linux**. Later versions are unverified.
- Explicit cutoffs; no implicit current time, calendar or coverage authority.
- Exact supported canonical types, resource limits and stable safe error IDs;
  no implicit conversions or `str()` / `repr()` fallback.
- Raw file hashing follows links to regular files and hashes content only;
  no locking, immutable snapshot, path-safety or TOCTOU protection.
- Real API tests use frozen synthetic expectations (*golden vectors*) and temporary
  files. [Coverage](docs/implementation/golden-runtime-coverage-v1.json) and
  [conformance](docs/implementation/cross-platform-conformance-v1.md) document skips.

## Documentation

- **Start here:** [demo timeline](docs/demos/minimal-asof-demo-v1.md) and
  [current release state](docs/release/RELEASE_STATE.md).
- **Implement:** [architecture](docs/ARCHITECTURE.md),
  [contract](contracts/minimal-primitives-v1.json),
  [specifications](docs/specs/compatibility-and-versioning-v1.md) and
  [implementation details](docs/implementation/minimal-primitives-v1.md).
- **Understand provenance:** [public/private boundary](docs/PUBLIC_PRIVATE_BOUNDARY.md)
  and [origin and authority](docs/ORIGIN_AND_AUTHORITY.md).

Linked guides retain some pre-publication wording; use current release state for
status and frozen specifications for semantics.

## Installation and development

With Python 3.12 or newer:

```sh
git clone https://github.com/Sikisiii/baquant-pit.git
cd baquant-pit
python -m venv .venv
```

Activate with `. .venv/bin/activate` on POSIX or
`.venv\Scripts\Activate.ps1` in Windows PowerShell, then:

```sh
python -m pip install .
```

Examples require the checkout or source distribution; wheels contain runtime and
metadata only. For development, from the source root:

```sh
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

## Status and compatibility

`0.1.0` is early Alpha. Public API compatibility is **NOT_ESTABLISHED**;
BAquant compatibility is **NOT_CLAIMED**. Implementation follows this project's
contract, specifications and synthetic vectors independently, without consulting
or copying private BAquant implementation.

## License

[Apache License 2.0](LICENSE).
