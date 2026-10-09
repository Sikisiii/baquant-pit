"""Print CI result metadata from pytest XML; never include absolute host paths."""

import json
import platform
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


def summarize(path: Path) -> dict:
    if not path.is_file():
        raise RuntimeError("Conformance XML missing")
    cases = ET.parse(path).findall(".//testcase")
    counts = Counter()
    skips = []
    host_cases = []
    allowed_skips = {
        "test_golden_runtime_conformance[T109]",
        "test_golden_runtime_conformance[C117]",
        "test_golden_runtime_conformance[F104]",
        *(
            f"test_symlink_policy_when_host_supports_it[{kind}]"
            for kind in ("file", "broken", "directory", "parent")
        ),
    }
    for case in cases:
        name = case.attrib["name"]
        outcome = next(
            (
                kind
                for kind in ("failure", "error", "skipped")
                if case.find(kind) is not None
            ),
            "passed",
        )
        counts[outcome] += 1
        if outcome == "skipped":
            if name not in allowed_skips:
                raise RuntimeError("Core conformance skip forbidden")
            reason = case.find("skipped").attrib.get("message", "")
            if not reason:
                raise RuntimeError("Skip reason required")
            skips.append({"test": name, "reason": reason})
        if (
            name.startswith("test_symlink_policy_when_host_supports_it[")
            or name == "test_golden_runtime_conformance[F104]"
        ):
            host_cases.append({"test": name, "outcome": outcome})
    return {
        "os": platform.system(),
        "python": platform.python_version(),
        "total_tests": len(cases),
        "outcomes": dict(counts),
        "skips": skips,
        "conditional_filesystem": host_cases,
    }


if __name__ == "__main__":
    result = summarize(Path(sys.argv[1]))
    print(
        "PITX_RESULT_JSON="
        + json.dumps(result, ensure_ascii=True, separators=(",", ":"))
    )
    if result["outcomes"].get("failure", 0) or result["outcomes"].get("error", 0):
        raise SystemExit(1)
