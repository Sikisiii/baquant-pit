# Raw integrity v1

Format: `baquant-pit-raw-integrity-v1`. Contract: `baquant-pit-minimal-primitives`,
version 1. Status: `PRIVATE_REVIEW_CANDIDATE`. There is no runtime hash API here.
Canonical hashing additionally uses `baquant-pit-canonical-v1`; raw bytes do not.

## Three distinct digest inputs

Every digest uses unkeyed, unsalted SHA-256 and yields exactly 64 lowercase hex
ASCII characters. Canonical hashing consumes the canonical UTF-8 format envelope.
Raw hashing consumes only supplied bytes. File hashing consumes only content
bytes. Raw/file inputs have no added format prefix, JSON envelope, namespace,
encoding marker, path, filename, stat fields or metadata. A digest does not prove
truth, authenticity, historical availability, native vintage, authority or completeness.

## Exact bytes

The Python binding accepts exact bytes only; bytearray, memoryview, strings,
subclasses and arbitrary buffers fail RAW_INVALID_BYTES_TYPE. Another language
may supply an equivalent immutable byte sequence. Empty input is valid. NUL
and arbitrary binary are ordinary bytes. No decoding, Unicode normalization,
newline conversion or JSON wrapping is performed. LF and CRLF differ; same-size
different content is separately hashed. No raw-content size limit is part of v1;
operational memory/resource errors never produce a partial successful digest.

## File content

The path input is native filesystem path text or a standard pathlib.Path;
arbitrary object coercion, bytes paths and embedded NUL fail RAW_INVALID_PATH_TYPE.
Only regular files are accepted; directories, sockets, devices and FIFO inputs
fail RAW_FILE_NOT_REGULAR_FILE without intentionally consuming their content.
Empty regular files are valid. Symlinks are FOLLOWED to a regular-file target,
including parent-component links; broken links fail RAW_FILE_NOT_FOUND, links
to directories/special files fail RAW_FILE_NOT_REGULAR_FILE. v1 does not implement
an allowlist, trusted root, safe path or no-follow security policy.

File content SHA-256 is conceptually identical to raw bytes SHA-256 of exactly
that content. Neither Windows separators/case rules nor file mtime/permissions,
filename/path/size enter the digest. Open in binary mode and never translate LF.
Streaming is recommended for bounded memory; any chunk size must yield the
same content digest as a whole-buffer read. It changes no semantic format.

The file primitive does NOT guarantee an immutable snapshot, absence of TOCTOU,
path safety, locking or authenticity. A concurrent modification can change the
sequence read; there is no promised before/after transaction. Callers needing
an immutable snapshot must establish it separately. A successful digest commits
to the bytes actually read through EOF, not an independently proved stable file.

## Errors

Semantic IDs do not dictate Python exception classes. Invalid path type/NUL:
RAW_INVALID_PATH_TYPE. ENOENT/ENOTDIR (at any stage): RAW_FILE_NOT_FOUND.
Nonregular target/EISDIR: RAW_FILE_NOT_REGULAR_FILE. Access denial EACCES/EPERM:
RAW_FILE_UNREADABLE. Other read/stat/open errors: RAW_FILE_IO_ERROR. Validate input
first, inspect target type, then consume bytes; if host access fails before type
inspection its access error is reported. A failed or incomplete read returns no
successful digest. Looping symlinks or concurrent host changes may cause an I/O
failure rather than a security classification. Details must not expose private
paths, secrets or raw payloads by default.

## Synthetic assets

`tests/fixtures/golden/raw-integrity-v1.json` records literal hex payloads and
expected raw SHA-256 for empty, one byte, non-ASCII UTF-8, LF, CRLF, NUL and
same-length distinct bytes. Its file cases reference those exact payloads and
the same expected digest: they express content equivalence without constructing
or hashing files in this task. File error cases are conceptual requirements,
not assertions about this machine's permissions or symlinks. No runtime file
hash function or platform experiment is hidden in the asset tests.
