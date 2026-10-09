# baquant-pit

Point-in-Time and Temporal Grounding Infrastructure for AI Financial Research.

**Current status: PRIVATE IMPLEMENTATION CANDIDATE / PRE-RELEASE.**

The minimal primitive runtime implements the private v1 semantics: explicit aware
datetime normalization and fixed UTC text, immutable inclusive date windows with
mandatory cutoffs, bounded typed canonical bytes/text and SHA-256, exact bytes
SHA-256, and streamed regular-file content SHA-256. Runtime code uses Python's
standard library only. Python 3.12 or newer is required; version remains
`0.0.0.dev0`.

The implementation is independently written from the merged baquant-pit contract,
normative specifications and synthetic golden vectors. The private BAquant source
implementation was neither consulted nor copied. BAquant compatibility is
NOT_CLAIMED, and public API compatibility is NOT_ESTABLISHED.

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

Run local validation in a virtual environment:

```sh
python -m venv .venv
# Activate the virtual environment using your platform's standard command.
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

Tests distinguish declarative asset consistency from execution of real APIs
against unchanged golden expectations. Every golden vector is accounted for in
the [runtime coverage table](docs/implementation/golden-runtime-coverage-v1.json).
Conceptual leap seconds and pre-construction duplicate keys are not fabricated
as Python inputs. Native FIFO and symlink tests run only where supported; controlled
permission and read failures exercise the actual file API. Only synthetic values
and temporary files are used. See the [implementation status](docs/implementation/minimal-primitives-v1.md).

The [minimal contract](contracts/minimal-primitives-v1.json) records runtime
implementation presence after successful conformance. The frozen [specifications](docs/specs/compatibility-and-versioning-v1.md)
and golden assets retain their design-time status wording and input descriptors;
their semantics and expected outputs are unchanged. The original design-scope
exclusion of runtime implementation describes the specification task, while the
implementation-presence flag and current status document describe this task.

There is no PIT reader, vintage engine, PIT grade, TrustSnapshot, applicability
classification, database, provider adapter, manifest registry, safe-root policy,
atomic publication, brokerage or trading functionality. File hashing follows
links to regular files and hashes only content; it provides no locking, immutable
snapshot, TOCTOU protection or authenticity guarantee. This candidate establishes
no production readiness, scientific acceptance or public API stability.

baquant-pit is market-neutral infrastructure. Its primitives do not authorize or
imply support for any specific exchange, security market, asset class or provider.
Market-specific rules belong in downstream consumers, outside this core library.
Private market data, proprietary strategies and competition assets are excluded.
Historical origin scope is recorded in [origin and authority](docs/ORIGIN_AND_AUTHORITY.md).

The same frozen v1 tests run on Windows and Ubuntu/Linux with Python 3.12. See the
[portability coverage and host boundaries](docs/implementation/cross-platform-conformance-v1.md).
Native symlinks and FIFO creation are conditional on host capability; core
canonical, temporal and hash semantics must pass on both platforms.

See the [extraction plan](docs/BAQUANT-PIT-PUBLIC-EXTRACTION-PLAN-V1.md),
[boundary](docs/PUBLIC_PRIVATE_BOUNDARY.md),
[architecture](docs/ARCHITECTURE.md),
[origin and authority](docs/ORIGIN_AND_AUTHORITY.md) and
[future release checklist](docs/PUBLIC_RELEASE_AUDIT_CHECKLIST.md).

No redistribution or open-source license is granted. The repository remains
private, the license is unchanged, and no release or package publication is
authorized. Merge and any future publication need separate Owner authorization.
