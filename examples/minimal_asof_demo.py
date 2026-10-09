"""Synthetic, example-local knowledge-time visibility; no package reader API."""

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from baquant_pit import (
    BaquantPITError,
    canonical_sha256,
    format_utc_instant,
    normalize_utc_instant,
)

DEMO_ID = "minimal-asof-v1"
DATA = Path(__file__).resolve().parent / "data/minimal_asof_demo.json"


class DemoDataError(ValueError):
    """Fixed safe demo-local input error, outside primitive semantic IDs."""

    def __init__(self):
        super().__init__("DEMO_INVALID_DATA")


class DemoAmbiguousObservationError(ValueError):
    """Fail closed for different records at the latest relevant instant."""

    def __init__(self):
        super().__init__("DEMO_AMBIGUOUS_OBSERVATION")


@dataclass(frozen=True)
class DemoObservation:
    observation_id: str
    value: str
    available_at: datetime


def _parse_instant(text: str) -> datetime:
    if type(text) is not str:
        raise DemoDataError()
    try:
        value = datetime.fromisoformat(text)
    except ValueError:
        raise DemoDataError() from None
    # Preserve primitive error IDs, including naive/null-offset/invalid type.
    return normalize_utc_instant(value)


def _ordered(observations: list[DemoObservation]) -> list[DemoObservation]:
    if type(observations) is not list or not observations:
        raise DemoDataError()
    seen = set()
    normalized = []
    for observation in observations:
        if type(observation) is not DemoObservation:
            raise DemoDataError()
        key = observation.observation_id
        if type(key) is not str or not key or key in seen:
            raise DemoDataError()
        if type(observation.value) is not str:
            raise DemoDataError()
        seen.add(key)
        normalized.append(
            DemoObservation(
                key, observation.value, normalize_utc_instant(observation.available_at)
            )
        )
    # ID ordering makes displayed lists/digests stable; it never resolves a tie.
    return sorted(
        normalized,
        key=lambda observation: (observation.available_at, observation.observation_id),
    )


def parse_demo(document: dict) -> tuple[list[DemoObservation], datetime]:
    fields = {"demo_id", "observations", "demonstration_as_of"}
    if type(document) is not dict or set(document) != fields:
        raise DemoDataError()
    if type(document["demo_id"]) is not str or document["demo_id"] != DEMO_ID:
        raise DemoDataError()
    rows = document["observations"]
    if type(rows) is not list or not rows:
        raise DemoDataError()
    observations = []
    for row in rows:
        if type(row) is not dict or set(row) != {
            "observation_id",
            "value",
            "available_at",
        }:
            raise DemoDataError()
        observations.append(
            DemoObservation(
                row["observation_id"], row["value"], _parse_instant(row["available_at"])
            )
        )
    return _ordered(observations), _parse_instant(document["demonstration_as_of"])


def _unique_fields(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise DemoDataError()
        result[key] = value
    return result


def load_demo(path: Path = DATA) -> tuple[list[DemoObservation], datetime]:
    try:
        document = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=_unique_fields
        )
    except (OSError, UnicodeError, ValueError):
        raise DemoDataError() from None
    return parse_demo(document)


def _latest(observations: list[DemoObservation]) -> DemoObservation | None:
    if not observations:
        return None
    latest = max(observation.available_at for observation in observations)
    candidates = [
        observation
        for observation in observations
        if observation.available_at == latest
    ]
    if len(candidates) != 1:
        raise DemoAmbiguousObservationError()
    return candidates[0]


def demonstrate(observations: list[DemoObservation], as_of: datetime) -> dict:
    """Demo rule only: greatest visible available_at, with ambiguous maxima rejected."""
    cutoff = normalize_utc_instant(as_of)
    ordered = _ordered(observations)
    visible = [
        observation for observation in ordered if observation.available_at <= cutoff
    ]
    future = [
        observation for observation in ordered if observation.available_at > cutoff
    ]
    selected = _latest(visible)
    naive = _latest(ordered)
    result = {
        "demo_id": DEMO_ID,
        "as_of": format_utc_instant(cutoff),
        "naive_latest": naive.observation_id,
        "pit_as_of": None if selected is None else selected.observation_id,
        "visible": [observation.observation_id for observation in visible],
        "future_excluded": [observation.observation_id for observation in future],
        "result": "LOOK_AHEAD_PREVENTED"
        if naive.available_at > cutoff
        else "NO_FUTURE_OBSERVATIONS",
    }
    input_material = {
        "demo_id": DEMO_ID,
        "as_of": cutoff,
        "observations": [
            {
                "observation_id": observation.observation_id,
                "value": observation.value,
                "available_at": observation.available_at,
            }
            for observation in ordered
        ],
    }
    return result | {
        "input_digest": canonical_sha256(input_material),
        "result_digest": canonical_sha256(result),
    }


def json_bytes(result: dict) -> bytes:
    """Presentation JSON only; content identity uses existing canonical_sha256."""
    return (
        json.dumps(
            result, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        + b"\n"
    )


def human_text(result: dict) -> str:
    selected = result["pit_as_of"] or "none"
    future = ", ".join(result["future_excluded"]) or "none"
    return (
        "baquant-pit minimal as-of demo\n"
        f"as_of: {result['as_of']}\n"
        f"naive latest: {result['naive_latest']}\n"
        f"point-in-time visible: {selected}\n"
        f"future observations excluded: {future}\n"
        f"result: {result['result']}\n"
        f"input_digest: {result['input_digest']}\n"
        f"result_digest: {result['result_digest']}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="deterministic UTF-8 JSON")
    args = parser.parse_args()
    try:
        observations, cutoff = load_demo()
        result = demonstrate(observations, cutoff)
    except (DemoDataError, DemoAmbiguousObservationError, BaquantPITError) as error:
        sys.stderr.buffer.write((str(error) + "\n").encode("utf-8"))
        return 1
    # Explicit binary UTF-8/LF avoids locale encodings and Windows newline conversion.
    sys.stdout.buffer.write(
        json_bytes(result) if args.json else human_text(result).encode("utf-8")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
