# Canonicalization v1

Format: `baquant-pit-canonical-v1`. Contract: `baquant-pit-minimal-primitives`,
version 1. Status: `PRIVATE_REVIEW_CANDIDATE`. This independently authored design
deliberately resolves the incompatible serializers identified in the prior
inventory. It selects new semantics, not an existing serializer as global winner.
`baquant_compatibility = NOT_CLAIMED`.

## Closed typed domain and decision table

Python accepts only the exact listed built-in types and exact Decimal, without
subclass dispatch, repr fallbacks or arbitrary Mapping/Sequence protocols.
In particular bool is distinct from int; Enum, IntEnum and StrEnum are rejected
even when they resemble accepted scalars. Other languages can bind equivalent
abstract values without requiring Python class identities or representations.

| Input | v1 decision | Normalized NODE |
| --- | --- | --- |
| null / None | accepted | ["null"] |
| bool | accepted, distinct from integer | ["bool",true] or ["bool",false] |
| integer | exact base-10 magnitude; no JSON numeric precision loss | ["int","17"] |
| string | Unicode scalar sequence; no normalization | ["str","text"] |
| float | reject all, finite/NaN/Infinity | CANONICAL_FLOAT_FORBIDDEN |
| Decimal | finite only; exact sign/coefficient/exponent strings | ["decimal","0","100","-2"] |
| date | distinct from datetime and string | ["date","2032-04-05"] |
| datetime | aware, normalized; temporal v1 fixed UTC text | ["datetime","2032-04-05T06:07:08.000000Z"] |
| list | accepted, element order retained | ["list",[NODE,...]] |
| tuple | rejected, no hidden list equivalence | CANONICAL_UNSUPPORTED_TYPE |
| mapping | exact dict with exact str scalar keys | ["map",[[KEY,NODE],...]] |
| Enum / IntEnum / StrEnum | rejected, no inheritance-order coercion | CANONICAL_UNSUPPORTED_TYPE |
| bytes / bytearray / memoryview | rejected here; exact bytes have separate raw hash capability | CANONICAL_UNSUPPORTED_TYPE |
| set / frozenset | rejected, no guessed stable order | CANONICAL_UNSUPPORTED_TYPE |
| other object or custom subclass | rejected, no str/repr fallback | CANONICAL_UNSUPPORTED_TYPE |
| cyclic containers | rejected, shared acyclic values allowed | CANONICAL_CYCLE_DETECTED |

## Grammar and type identity

The document is the positional array ["baquant-pit-canonical-v1", NODE]. NODE is
exactly one of the closed array forms in the table. Each tag's arity is fixed;
unknown tags are invalid. Integer text is `0` or `-?[1-9][0-9]*`, with ASCII
digits, no plus, leading zero, whitespace or integer negative zero. Sign, decimal
coefficient and decimal exponent also use strings, never JSON numbers. Boolean
payloads use JSON booleans. No normalized JSON object is used.

User lists contain tagged nodes; user mappings are lists of raw-string-key/node
pairs inside a map node. User data that happens to say "date", "map" or the
format ID cannot become grammar. For example the string "2032-04-05" emits a str
node, while that date emits a date node; "1.00" and Decimal("1.00") differ too.
Type tags belong to the closed representation language, not to user keys.
The root format ID is an explicit namespace included in canonical bytes, not
an extra salt added by the hash function. This grammar is language-portable.

## Decimal, keys and Unicode

A finite decimal is represented ["decimal",SIGN,COEFFICIENT,EXPONENT], with SIGN
"0" or "1", COEFFICIENT `0` or `[1-9][0-9]*`, and EXPONENT in canonical signed
integer text. Numeric value is (-1)^sign * coefficient * 10^exponent. Leading
coefficient zeros are not retained; trailing coefficient zeros and exponent
(quantum) are retained. Finite Python Decimal's exact tuple defines these fields;
no arithmetic context, rounding or numeric normalization is applied.

Decimal("1.0") -> ["decimal","0","10","-1"] and Decimal("1.00") ->
["decimal","0","100","-2"] are distinct. Decimal("-0.00") ->
["decimal","1","0","-2"] retains negative zero and scale, distinct from
positive zero. Decimal("1E+3") retains exponent "3"; there is no scientific
notation string in the canonical representation. Decimal("1.20E-3") has
coefficient "120", exponent "-5". Spellings yielding the same exact tuple are
identical. NaN, signaling NaN and either Infinity are rejected.

Mapping keys must be exact Unicode scalar strings; no str(key) coercion. Sort
lexicographically by numeric Unicode scalar values; shorter equal prefixes sort
first. Case is retained. Exact duplicate keys in an abstract mapping input are
rejected before lossy construction; a Python dict alone cannot recover a
duplicate already discarded by an upstream parser, so that loss is outside
the primitive's input. Non-string keys, including a conceptual {1:...,"1":...}
coercion collision, fail CANONICAL_INVALID_MAPPING_KEY. Equal normalized keys
are not newly created because no normalization is performed. Composed "é" and
decomposed "é" remain distinct both as strings and keys. Duplicate exact scalar
keys fail CANONICAL_DUPLICATE_MAPPING_KEY. Empty string keys are valid.

All text contains Unicode scalar values only; U+D800..U+DFFF are rejected even
if a Python string contains a surrogate pair. Use the actual supplementary
scalar instead. No NFC or NFKC, replacement encoding or locale collation is
applied. Composed/decomposed synthetic vectors make this choice explicit.

## Exact UTF-8 bytes

Render the root and node arrays as strict JSON encoded UTF-8 without BOM,
whitespace outside strings or terminal newline. Comma is the sole array element
separator. Boolean literals are lower-case true/false. There are no numeric
JSON literals or object members in this representation. Colon is the JSON
object separator for asset files, but never appears as a structural separator
in a normalized canonical document; a colon inside user text is literal.

JSON strings always use double quotes. Escape U+0022 as \" and U+005C as \\.
Use exactly \b, \f, \n, \r, \t for U+0008/000C/000A/000D/0009. Every other
U+0000..001F uses \u00xx with lowercase hex. Solidus / is NOT escaped. Every
other scalar, including non-ASCII, U+007F, U+2028/2029 and supplementary scalars,
is literal UTF-8 (ensure_ascii=false behavior). No optional escape variant is
allowed. NFC-equivalent source text may therefore have different canonical
bytes and hashes. The literal golden byte hex is authoritative for each vector.

Canonical text is exactly the decoding of those bytes. Canonical SHA-256 hashes
the complete envelope bytes, yielding exactly 64 lowercase hex ASCII characters;
no additional namespace, salt, key, path or metadata is appended. This does not
claim truth, authenticity, availability, native vintage, authority or completeness.

## Normative resource bounds and failures

The root NODE has depth 0, its list children and mapping values have depth +1;
the format envelope, tag arrays and mapping keys do not add semantic node depth.
Maximum node depth is 16 inclusive; maximum emitted node occurrences is 1024
including the root. Aliased acyclic substructures count once per occurrence.
Each scalar string or key may have at most 4096 strict UTF-8 bytes before JSON
escaping; integer magnitude and Decimal coefficient at most 1024 ASCII digits;
Decimal exponent is within [-1024,1024]. Complete encoded envelope is at most
65536 bytes inclusive, including escaping overhead. Boundaries are normative
v1, not platform tuning. Exceeding any bound yields CANONICAL_RESOURCE_LIMIT
and no digest. Internal chunk size/allocations may vary without changing bytes;
a conforming implementation may not silently lower these limits. Cancellation
or system exhaustion is operational failure, not a successfully conforming hash.

Visit values in list order or validated/sorted map-key order. At each node:
exact type gate first (float has its dedicated error, other rejected types use
CANONICAL_UNSUPPORTED_TYPE); active-ancestor cycle gate next; then depth/count
limits; then the scalar-specific validity/limits or mapping-key validation;
then children. Scalar datetime uses temporal v1 error order. Decimal finiteness
precedes its bounds; Unicode validity precedes UTF-8 length. Mapping invalid key
type precedes invalid Unicode, then duplicate exact-key check, then key size,
then recursion in sorted order. Complete-byte length is checked last. Among
multiple failures the first gate in this traversal wins. Error IDs are stable;
future Python exception classes and safe diagnostic detail names remain undecided.

Cycles use active ancestors, not a global visited-set: two references to the
same acyclic list are valid and serialized twice. Callers must not mutate inputs
during normalization; the primitive does not promise concurrent snapshots.

Newly authored declarative vectors are in `tests/fixtures/golden/canonical-v1.json`.
Asset tests validate recorded logical forms, text/hex/digest agreement and error
IDs, not normalization from semantic inputs. Passing those tests is not runtime
conformance. Normative vectors supplement, and do not replace, all rules above.
