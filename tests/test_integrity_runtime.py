"""Content identity, streaming, path rejection and safe filesystem errors."""

import errno
import json
import os
from hashlib import sha256
from pathlib import Path, PurePath

import pytest

import baquant_pit
from baquant_pit import BaquantPITError, sha256_bytes, sha256_file
from baquant_pit import integrity as impl


@pytest.mark.parametrize(
    "value", [b"", b"a", b"b", b"\xff\x80\x00", b"\n", b"\r\n", "雪".encode()]
)
def test_raw_exact_content(value):
    assert sha256_bytes(value) == sha256(value).hexdigest()


@pytest.mark.parametrize(
    "value",
    [
        "x",
        bytearray(b"x"),
        memoryview(b"x"),
        type("BytesSubclass", (bytes,), {})(b"x"),
        None,
        object(),
    ],
)
def test_raw_type_gate(value):
    with pytest.raises(BaquantPITError) as caught:
        sha256_bytes(value)
    assert caught.value.error_id == str(caught.value) == "RAW_INVALID_BYTES_TYPE"


@pytest.mark.parametrize("size", [1, 7, 65536])
def test_streaming_chunk_size_does_not_change_identity(tmp_path, monkeypatch, size):
    data = bytes(range(256)) * 513 + b"\x00\r\n"
    path = tmp_path / "content.bin"
    path.write_bytes(data)
    monkeypatch.setattr(impl, "_CHUNK_BYTES", size)
    assert sha256_file(path) == sha256_file(str(path)) == sha256_bytes(data)


def test_empty_renamed_metadata_and_same_length_change(tmp_path):
    first = tmp_path / "first"
    first.write_bytes(b"")
    assert sha256_file(first) == sha256_bytes(b"")
    first.write_bytes(b"a\x00\n")
    expected = sha256_file(first)
    second = tmp_path / "second"
    first.rename(second)
    os.utime(second, (100, 200))
    assert sha256_file(second) == expected
    second.write_bytes(b"b\x00\n")
    assert sha256_file(second) != expected


@pytest.mark.parametrize(
    "value",
    [
        b"path",
        None,
        object(),
        PurePath("synthetic"),
        type("PathSubclass", (type(Path()),), {})("synthetic"),
        "nul\x00path",
        Path("nul\x00path"),
    ],
)
def test_invalid_path_type_and_nul(value):
    with pytest.raises(BaquantPITError) as caught:
        sha256_file(value)
    assert caught.value.error_id == str(caught.value) == "RAW_INVALID_PATH_TYPE"


def test_arbitrary_path_protocol_not_called():
    class Coercion:
        def __fspath__(self):
            raise AssertionError("arbitrary filesystem protocol")

        def __str__(self):
            raise AssertionError("arbitrary str")

    with pytest.raises(BaquantPITError, match="^RAW_INVALID_PATH_TYPE$"):
        sha256_file(Coercion())


def test_missing_and_directory(tmp_path):
    for path, expected in [
        (tmp_path / "missing", "RAW_FILE_NOT_FOUND"),
        (tmp_path, "RAW_FILE_NOT_REGULAR_FILE"),
    ]:
        with pytest.raises(BaquantPITError) as caught:
            sha256_file(path)
        assert caught.value.error_id == str(caught.value) == expected
        assert str(tmp_path) not in repr(caught.value)
    regular = tmp_path / "regular"
    regular.write_bytes(b"x")
    with pytest.raises(BaquantPITError, match="^RAW_FILE_NOT_FOUND$"):
        sha256_file(regular / "child")


@pytest.mark.parametrize("scenario", ["file", "broken", "directory", "parent"])
def test_symlink_policy_when_host_supports_it(tmp_path, scenario):
    regular = tmp_path / "regular"
    regular.write_bytes(b"\xff\x00\n")
    link = tmp_path / "link"
    destination = {
        "file": regular,
        "broken": tmp_path / "missing",
        "directory": tmp_path,
        "parent": tmp_path,
    }[scenario]
    try:
        link.symlink_to(
            destination, target_is_directory=scenario in ("directory", "parent")
        )
    except (OSError, NotImplementedError):
        pytest.skip("Native symlink creation unavailable for this host/user")
    if scenario == "file":
        assert sha256_file(link) == sha256_bytes(regular.read_bytes())
    elif scenario == "parent":
        assert sha256_file(link / "regular") == sha256_bytes(regular.read_bytes())
    else:
        error = (
            "RAW_FILE_NOT_FOUND"
            if scenario == "broken"
            else "RAW_FILE_NOT_REGULAR_FILE"
        )
        with pytest.raises(BaquantPITError, match="^" + error + "$"):
            sha256_file(link)


@pytest.mark.parametrize("stage", ["stat", "open", "read"])
@pytest.mark.parametrize(
    "code,error",
    [
        (errno.ENOENT, "RAW_FILE_NOT_FOUND"),
        (errno.ENOTDIR, "RAW_FILE_NOT_FOUND"),
        (errno.EISDIR, "RAW_FILE_NOT_REGULAR_FILE"),
        (errno.EACCES, "RAW_FILE_UNREADABLE"),
        (errno.EPERM, "RAW_FILE_UNREADABLE"),
        (errno.EIO, "RAW_FILE_IO_ERROR"),
    ],
)
def test_os_failure_mapping_at_each_stage(tmp_path, monkeypatch, stage, code, error):
    path = tmp_path / "regular"
    path.write_bytes(b"x")

    def fail(*args, **kwargs):
        raise OSError(code, "synthetic raw diagnostic", str(path))

    class Reader:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        read = fail

    if stage == "read":
        monkeypatch.setattr(type(path), "open", lambda *args, **kwargs: Reader())
    else:
        monkeypatch.setattr(type(path), stage, fail)
    with pytest.raises(BaquantPITError) as caught:
        sha256_file(path)
    assert caught.value.error_id == str(caught.value) == error
    assert str(path) not in repr(caught.value)
    assert caught.value.__suppress_context__


@pytest.mark.parametrize(
    "exception",
    [
        PermissionError("synthetic"),
        IsADirectoryError("synthetic"),
        FileNotFoundError("synthetic"),
        NotADirectoryError("synthetic"),
        OSError("synthetic"),
        UnicodeError("synthetic"),
        ValueError("synthetic"),
    ],
)
def test_exception_classes_without_errno(tmp_path, monkeypatch, exception):
    path = tmp_path / "regular"
    path.write_bytes(b"x")

    def fail(*args, **kwargs):
        raise exception

    monkeypatch.setattr(type(path), "open", fail)
    expected = {
        PermissionError: "RAW_FILE_UNREADABLE",
        IsADirectoryError: "RAW_FILE_NOT_REGULAR_FILE",
        FileNotFoundError: "RAW_FILE_NOT_FOUND",
        NotADirectoryError: "RAW_FILE_NOT_FOUND",
    }.get(type(exception), "RAW_FILE_IO_ERROR")
    with pytest.raises(BaquantPITError) as caught:
        sha256_file(path)
    assert caught.value.error_id == str(caught.value) == expected


def test_error_binding_and_public_exports():
    root = Path(__file__).resolve().parents[1]
    contract = json.loads(
        (root / "contracts/minimal-primitives-v1.json").read_text(encoding="utf-8")
    )
    for error_id in contract["error_ids"]:
        error = BaquantPITError(error_id)
        assert str(error) == error.error_id == error_id
        with pytest.raises(AttributeError):
            error.error_id = "different"
    for name in baquant_pit.__all__:
        assert getattr(baquant_pit, name) is not None
    assert baquant_pit.__version__ == "0.1.0"
