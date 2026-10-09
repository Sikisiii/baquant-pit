# baquant-pit

**English** | [简体中文](README.zh-CN.md)

Point-in-Time and Temporal Grounding Infrastructure for AI Financial Research.

**Current status: 0.1.0 RELEASE READY / PRIVATE UNTIL OWNER-APPROVED PUBLICATION.**

The minimal primitives v1 runtime is implemented. It provides explicit aware
datetime normalization and fixed UTC text, immutable inclusive date windows with
mandatory cutoffs, bounded typed canonical bytes/text and SHA-256, exact bytes
SHA-256, and streamed regular-file content SHA-256. Runtime code uses Python's
standard library only. Python 3.12 or newer is required; validation currently
covers Python 3.12 on Windows and Ubuntu/Linux. Current version: `0.1.0` (Alpha).

The [current release state](docs/release/RELEASE_STATE.md) explains implemented
scope, frozen design-time specifications and final publication gates. Public
API compatibility is NOT_ESTABLISHED and BAquant compatibility is NOT_CLAIMED.
The runtime was independently written from the baquant-pit contract,
specifications and synthetic golden vectors; the private BAquant implementation
was neither consulted nor copied.

## Install and validate a source checkout

From the repository root or a complete extracted source distribution, create
and activate a Python 3.12 virtual environment, then install the development tools:

```sh
python -m venv .venv
# Activate the virtual environment using your platform's standard command.
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

For library use, `python -m pip install .` installs normally without editable mode.
A wheel contains the runtime library and metadata; the examples and validation
commands below require the complete source checkout or source distribution.

## Minimal primitives

```python
from datetime import UTC, date, datetime

from baquant_pit import DateWindow, canonical_bytes, canonical_sha256

window = DateWindow(
    date(2032, 4, 4), date(2032, 4, 6), datetime(2032, 4, 5, tzinfo=UTC)
)
payload = {"cutoff": window.cutoff, "label": "synthetic"}
encoded = canonical_bytes(payload)
digest = canonical_sha256(payload)
```

`DateWindow` stores inclusive dates and a normalized UTC cutoff. It is not itself
a canonical input. No calendar, exchange-session or coverage authority follows
from these fields. Canonical inputs are exact supported Python types; there are
no implicit conversions or string/repr fallbacks. `BaquantPITError` exposes a
stable `.error_id` with fixed safe text; small temporal, canonical and raw
integrity subclasses share that binding.

## Minimal as-of demo

Suppose an observation is revised tomorrow. A historical decision made today
must not see tomorrow's observation. After installing from the complete source
bundle above, run:

```sh
python examples/minimal_asof_demo.py
python examples/minimal_asof_demo.py --json
```

With an explicit synthetic cutoff, naive latest chooses obs-003 while as-of sees
obs-001 and excludes the future obs-002/obs-003. See the
[synthetic timeline, inclusive cutoff and demo boundaries](docs/demos/minimal-asof-demo-v1.md).
The selection rule lives in the example; it adds no package reader API.

## Scope and conformance

baquant-pit is market-neutral infrastructure. Its primitives do not authorize or
imply support for any specific exchange, security market, asset class or provider.
Market-specific rules belong in downstream consumers. Private market data,
proprietary strategies and competition assets are excluded.

There is no production PIT reader, vintage engine, PIT grade, TrustSnapshot,
applicability classification, database, provider adapter, manifest registry,
safe-root policy, atomic publication, brokerage or trading functionality. File
hashing follows links to regular files and hashes only content; it provides no
locking, immutable snapshot, TOCTOU protection or authenticity guarantee. This
early Alpha version establishes no production readiness, scientific acceptance or public
API stability.

Tests execute real APIs against the frozen synthetic goldens. Every golden
vector is accounted for in the [runtime coverage table](docs/implementation/golden-runtime-coverage-v1.json).
Conceptual leap seconds and pre-construction duplicate keys are not fabricated
as Python inputs. Native FIFO and symlink tests run only where supported;
controlled permission and read failures exercise the actual file API. Only
synthetic values and temporary files are used.

The same frozen v1 suite runs on Windows and Ubuntu/Linux with Python 3.12. See
[conformance scope and host boundaries](docs/implementation/cross-platform-conformance-v1.md).
Core temporal, canonical and hash semantics must pass on both platforms; native
filesystem capability skips are explicitly accounted for.

Start with [release state](docs/release/RELEASE_STATE.md), then explore the
[architecture](docs/ARCHITECTURE.md), [minimal contract](contracts/minimal-primitives-v1.json),
[specifications](docs/specs/compatibility-and-versioning-v1.md),
[implementation](docs/implementation/minimal-primitives-v1.md),
[content boundary](docs/PUBLIC_PRIVATE_BOUNDARY.md) and
[origin and authority](docs/ORIGIN_AND_AUTHORITY.md).

Licensed under [Apache License 2.0](LICENSE). The Owner has selected Apache-2.0
and version `0.1.0`, and accepted historical commit identity exposure without
history rewrite. These decisions are resolved. The repository remains PRIVATE
until the separately authorized final publication action; the license does not
change repository visibility.

At that future publication, both README current-status lines must change to
`PUBLIC / OPEN SOURCE / 0.1.0` before or together with the visibility change.
That status transition has not been performed. The Chinese README must continue
to contain no ideographic or halfwidth ideographic full stops.
