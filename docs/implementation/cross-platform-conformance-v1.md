# Cross-platform conformance v1

This conformance design covers Windows and Ubuntu/Linux on Python 3.12
against the same frozen baquant-pit minimal-primitives contract/version 1.
The runtime is implemented; the repository is in private release candidate
preparation. See [current release state](../release/RELEASE_STATE.md).
Conformance adds no runtime capability, public API, semantic rule or version change.
The [machine-readable coverage design](cross-platform-conformance-v1.json)
describes scope; actual success is demonstrated by the final GitHub Actions
matrix, not asserted by this document or an ephemeral run ID.

## Shared semantic authority

Both clean CI environments install `python -m pip install -e ".[dev]"`, then run
Ruff, format checks and the entire pytest suite. Checkout credentials are not
persisted and workflow permissions are contents-read only. Tests check all 12
existing package exports and the unchanged `0.0.0.dev0` version after installation.
No service containers, secrets, provider/database calls or external data are used.

The entire golden runtime suite executes on both platforms. Each platform must
match the same recorded bytes/text/hash/error IDs; platform output never becomes
an expected value. Existing 116-vector classification and expectations stay
unchanged: 113 executable, T109/C117 conceptual, F104 platform conditional.
Passing asset consistency alone is not runtime conformance.

The bounded additional layer varies C/host-default locale and Decimal context
precision/rounding over 24 representative frozen canonical goldens. These cover
None, booleans, signed/large integers, Decimal scale/negative zero, ASCII and
Unicode composition/decomposition, supplementary scalar, U+2028/U+2029, controls,
date/datetime, nested lists and ordered maps. The full golden suite and existing
offset-equivalence tests prove UTC/+08/negative-offset identity on both hosts.

Existing tests also cover inclusive resource boundaries, Decimal coefficient and
exponent boundaries, all control escapes, no NFC/NFKC/casefold, scalar key ordering,
surrogate rejection, temporal years/microseconds/error IDs, and window immutability.
Additional tests alter process TZ settings and use native tzset where available;
Windows requires no tzset or zone database. All process locale/TZ and Decimal
context changes are restored. Supported local configurations are C and host
default; this does not claim every optional locale is installed or tested.

## Filesystem semantics and capability conditions

Binary regular-file tests cover all frozen raw payloads, LF versus CRLF, empty
files, content equivalence, renaming/mtime independence and same-size changes.
Short native Unicode filenames add a path/text-encoding portability check; all
content hashing remains binary with explicit UTF-8 only for canonical text.
Missing file, directory, invalid path/NUL and stat/open/read error mapping run
on both platforms. Permission/read failures use controlled injections, including
a partial read before failure. These establish semantic classification rather
than native ACL security properties or immutable snapshots.

| Native feature | Ubuntu/Linux | Windows |
| --- | --- | --- |
| Symlink to regular file, broken link, directory, parent component | Real native creation and policy checks where supported | Real checks if host privileges/Developer Mode permit; explicit capability skip on creation failure |
| FIFO, F104 | Actually create using os.mkfifo and reject before reading | PLATFORM_NOT_APPLICABLE when native FIFO construction is unavailable; explicit conditional skip |

No native symlink/FIFO success is emulated. No blanket Windows skip is allowed for
core semantics. CI records each conditional case outcome and every skip reason;
the summary tool rejects unexpected skips outside the two conceptual goldens,
the conditional FIFO and four native symlink cases. Existing golden coverage is
not reduced or reclassified.

## Windows path boundary

Ordinary short native str/Path inputs work. The library does not promise support
for every legacy Win32 path-length environment. An OS path-length failure maps
to RAW_FILE_IO_ERROR unless ENOENT/ENOTDIR/EISDIR/EACCES/EPERM supplies a more
specific existing mapping. Tests inject ENAMETOOLONG/Win32 206 at stat/open/read;
this tests error binding, not native long-path support. No registry/system policy,
LongPathsEnabled, extended-prefix insertion, admin privileges or ACL change is
performed or required.

CI pytest uses a short runner-temporary basetemp. A local Windows run may choose
a short writable task/process-local basetemp and TEMP root without persisting
environment or policy changes. These temporary paths do not enter canonical
bytes, file digest identity or repository artifacts.

No safe-root, locking, TOCTOU, snapshot or authenticity guarantee is made. The
market-neutral core implies no exchange, asset-class or provider support.
Historical origin scope is retained in [origin and authority](../ORIGIN_AND_AUTHORITY.md).
The repository remains PRIVATE during release candidate preparation.
License selection and publication remain pending; current scope and decisions
are recorded in [release state](../release/RELEASE_STATE.md).
