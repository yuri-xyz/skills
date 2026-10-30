# Bug classes

Walk risky code through each class that applies. For each, ask which concrete
input breaks it.

## Boundaries and off-by-one

- Loop bounds: `<` versus `<=`, starting at 0 or 1, the last iteration.
- Slices, ranges, and substrings: inclusive or exclusive ends, empty ranges,
  `end > len`, negative or reversed ranges.
- Min and max: limits that are off by one, inclusive where the spec says
  exclusive, min greater than max, or a limit checked after the work it
  should prevent.
- Fencepost counts: items versus gaps, pages versus page boundaries,
  pagination that skips or repeats the item at the edge.
- First, last, empty, and single-element cases of collections and strings.

## Unbounded work and resources

- Recursion and traversal without a depth limit, including nested JSON, YAML,
  or archives, and directory walks.
- Filesystem actions that can run away: walks following symlink cycles,
  deletes or writes without a scope check, unbounded file counts or sizes,
  temp files never cleaned up.
- Loops and retries without a maximum, backoff, or timeout; polling that never
  gives up; network calls without a timeout.
- Queues, caches, buffers, logs, and maps that grow without bound.
- Reading a whole file, response, or stream into memory with no size cap;
  decompression without a ratio or size cap.
- Pagination or following links without a page or item cap.
- Spawned processes, threads, or tasks without a concurrency limit.

## Untrusted input size and shape

- User or external input that can be huge, empty, deeply nested, or malformed:
  bodies, files, arguments, environment, headers, and query strings.
- Length checks done in the wrong unit, such as characters where storage is
  bytes.
- Regular expressions with catastrophic backtracking on long input.
- Assumptions that input is valid UTF-8, has no NUL bytes, no newlines, or
  no leading or trailing whitespace.

## Integers

- Overflow and underflow in sums, products, size and offset math, and counters,
  including `len - 1` on an empty collection with unsigned types.
- Truncating casts, such as 64-bit to 32-bit or size to int, and sign changes
  between signed and unsigned.
- Sizes beyond 2 GiB or 4 GiB, timestamps beyond 2038, and IDs beyond 2^53
  in JavaScript or JSON.
- Modulo and integer division with negative operands, which round
  differently across languages.

## Division and floating point

- Division or modulo by zero, including averages over empty sets and rates
  over zero elapsed time.
- NaN and infinity propagating silently; comparisons with NaN.
- Equality on floats, rounding at boundaries, money in binary floats, and
  accumulated error in long sums.

## Implicit conversions

- Strings to numbers: partial parses (`parseInt("12px")`), leading zeros,
  whitespace, signs, exponents, hex, locale decimal separators, and empty
  strings becoming 0.
- Integers to floats losing precision, and integer division where a
  fractional result was meant, or the reverse.
- Truthiness: 0, empty string, empty collection, and `None` or `null` treated
  alike when they mean different things.
- Booleans, dates, and enums serialized and parsed back differently.

## Text and Unicode

- Byte length versus code points versus grapheme clusters; emoji, combining
  marks, ZWJ sequences, and flags counted or cut wrongly.
- Truncation or slicing that splits a multibyte character or a grapheme.
- Normalization (NFC versus NFD) in comparisons, keys, and filenames.
- Case folding and locale, such as the Turkish dotless i, and `lower()` used
  for case-insensitive comparison.
- Display width for CJK and emoji in terminals and fixed-width layouts.
- Encodings at boundaries: bytes versus strings, BOMs, CRLF versus LF, invalid
  sequences, and lossy replacement characters.
- Bidirectional and invisible characters in identifiers and displayed names.

## Null, empty, and missing

- `null`, `None`, `undefined`, missing keys, and optional fields at every
  dereference, including after a failed lookup or parse.
- Empty string versus missing value, and defaults that hide a missing value.

## Errors and partial failure

- Ignored return values, swallowed exceptions, and errors logged but not
  propagated.
- Partial writes and multi-step updates that leave inconsistent state on
  failure; missing atomic rename, rollback, or cleanup.
- Resource leaks on error paths: files, sockets, locks, temp directories, and
  child processes.
- Retries that repeat a non-idempotent side effect.

## State, ordering, and concurrency

- Races and check-then-act (TOCTOU) on files, maps, and shared state; missing
  `await`; callbacks running after teardown.
- Aliasing and shared mutable defaults, such as mutable default arguments or
  a copied reference mutated by two owners.
- Stale caches without invalidation, and order-dependent logic relying on map
  iteration order or an unstable sort.

## Time

- Time zones, DST transitions, leap days, and month-end arithmetic.
- Wall clock used for durations or timeouts where a monotonic clock is needed.
- Parsing and formatting dates without an explicit format or zone.

## Paths and commands

- Paths with spaces, quotes, newlines, a leading dash, or non-UTF-8 bytes.
- Relative versus absolute paths, `..` segments, symlinks, and case-insensitive
  filesystems.
- Shell commands built by string concatenation; word splitting and globbing.

## Logic slips

- Inverted conditions, De Morgan mistakes, operator precedence, and
  short-circuit side effects.
- Non-exhaustive `switch` or `match`, missing defaults, and fallthrough.
- Copy-paste errors: the wrong variable, index, or field in a near-duplicate
  line.
- Comparators that are not consistent, such as `a < b` and `b < a` both true.

## Missing tests

Code that is likely to have bugs needs tests for the cases above that apply:
empty, one, boundary, maximum, over maximum, malformed, non-ASCII and emoji,
negative, zero, and failure paths. Prefer property-based or table-driven
tests where the project already uses them.
