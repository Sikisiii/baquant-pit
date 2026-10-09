"""Exact bytes and streamed regular-file content SHA-256, without path policy."""

import errno
import stat
from hashlib import sha256
from pathlib import Path

from .errors import RawIntegrityError

_NATIVE_PATH_TYPE = type(Path())
_CHUNK_BYTES = 64 * 1024


def sha256_bytes(value: bytes) -> str:
    """Hash exact built-in bytes, including empty/binary/NUL/newline bytes."""
    if type(value) is not bytes:
        raise RawIntegrityError("RAW_INVALID_BYTES_TYPE")
    return sha256(value).hexdigest()


def _filesystem_error(error: OSError) -> RawIntegrityError:
    if isinstance(error, (FileNotFoundError, NotADirectoryError)) or error.errno in (
        errno.ENOENT,
        errno.ENOTDIR,
    ):
        return RawIntegrityError("RAW_FILE_NOT_FOUND")
    if isinstance(error, IsADirectoryError) or error.errno == errno.EISDIR:
        return RawIntegrityError("RAW_FILE_NOT_REGULAR_FILE")
    if isinstance(error, PermissionError) or error.errno in (errno.EACCES, errno.EPERM):
        return RawIntegrityError("RAW_FILE_UNREADABLE")
    return RawIntegrityError("RAW_FILE_IO_ERROR")


def sha256_file(path: str | Path) -> str:
    """Follow links to regular files and hash binary content through EOF.

    No metadata/path enters the digest. No snapshot, lock or trusted-root guarantee.
    """
    if type(path) is str:
        if "\x00" in path:
            raise RawIntegrityError("RAW_INVALID_PATH_TYPE")
        target = Path(path)
    elif type(path) is _NATIVE_PATH_TYPE:
        target = path
        if "\x00" in str(target):
            raise RawIntegrityError("RAW_INVALID_PATH_TYPE")
    else:
        raise RawIntegrityError("RAW_INVALID_PATH_TYPE")
    try:
        if not stat.S_ISREG(target.stat().st_mode):
            raise RawIntegrityError("RAW_FILE_NOT_REGULAR_FILE")
        digest = sha256()
        with target.open("rb") as stream:
            while chunk := stream.read(_CHUNK_BYTES):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError as error:
        raise _filesystem_error(error) from None
    except RawIntegrityError:
        raise
    except (UnicodeError, ValueError):
        raise RawIntegrityError("RAW_FILE_IO_ERROR") from None
