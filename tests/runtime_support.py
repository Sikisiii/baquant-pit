"""Synthetic descriptor materialization only; never derive expected outputs."""

from datetime import datetime, tzinfo
from decimal import Decimal
from enum import Enum, IntEnum, StrEnum


class Offset(tzinfo):
    def __init__(self, result=None, throws=False):
        self.result = result
        self.throws = throws
        self.calls = 0

    def utcoffset(self, value):
        self.calls += 1
        if self.throws:
            raise ValueError("synthetic offset failure")
        return self.result


def instant(descriptor):
    if "text" in descriptor:
        return datetime.fromisoformat(descriptor["text"])
    return datetime(
        2032,
        4,
        5,
        tzinfo=Offset(throws=descriptor.get("utcoffset_behavior") == "raises"),
    )


def nested(depth, leaf=None):
    for _ in range(depth):
        leaf = [leaf]
    return leaf


def envelope_input(byte_length):
    # Explicit grammar punctuation, 16 empty str nodes and 15 separators.
    overhead = len(b'["baquant-pit-canonical-v1",["list",[]]]') + 16 * 10 + 15
    lengths = [4096] * 15 + [byte_length - overhead - 15 * 4096]
    assert all(0 <= length <= 4096 for length in lengths)
    return ["x" * length for length in lengths]


def materialize(d):
    from datetime import date

    kind = d["type"]
    if kind == "null":
        return None
    if kind == "bool":
        return d["value"]
    if kind == "integer":
        return int(d["text"])
    if kind in ("float", "Decimal"):
        return (float if kind == "float" else Decimal)(d["text"])
    if kind == "string":
        if "scalar_values" in d:
            return "".join(chr(int(code[2:], 16)) for code in d["scalar_values"])
        return d["value"]
    if kind == "date":
        return date.fromisoformat(d["text"])
    if kind == "datetime":
        return instant(d)
    if kind == "list":
        if "shared_child" in d:
            shared = materialize(d["shared_child"])
            return [shared] * d["occurrences"]
        return [materialize(item) for item in d["items"]]
    if kind == "mapping":
        return {key: materialize(item) for key, item in d["entries"]}
    if kind in ("bytes", "bytearray", "memoryview"):
        data = bytes.fromhex(d["hex"])
        return {"bytes": bytes, "bytearray": bytearray, "memoryview": memoryview}[kind](
            data
        )
    if kind in ("set", "frozenset", "tuple"):
        return {"set": set, "frozenset": frozenset, "tuple": tuple}[kind](d["items"])
    if kind in ("Enum", "IntEnum", "StrEnum"):
        base = {"Enum": Enum, "IntEnum": IntEnum, "StrEnum": StrEnum}[kind]
        return base("SyntheticMember", {"X": d["member_value"]}).X
    if kind == "unsupported_object":
        return object()
    if kind == "custom_str_subclass":
        return type("SyntheticString", (str,), {})(d["value"])
    if kind == "list_cycle":
        value = []
        value.append(value)
        return value
    if kind == "mapping_cycle":
        value = {}
        value[d["key"]] = value
        return value
    if kind == "conceptual_bounded_input":
        if "max_node_depth" in d:
            return nested(d["max_node_depth"])
        if "node_occurrences" in d:
            return [None] * (d["node_occurrences"] - 1)
        return envelope_input(d["canonical_byte_length"])
    if kind == "conceptual_string":
        return "x" * d["UTF8_byte_length"]
    if kind == "conceptual_integer":
        return 10 ** (d["magnitude_digits"] - 1)
    if kind == "conceptual_Decimal":
        return Decimal((0, (1,) * d["coefficient_digits"], 0))
    raise AssertionError("Unmaterialized synthetic descriptor")
