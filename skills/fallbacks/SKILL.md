---
name: fallbacks
description: Use when writing or reviewing fallback, default, or recovery paths, or when a default value or catch-all might be masking missing data, errors, or broken invariants.
---

# Fallbacks

Use this skill when implementing, reviewing, debugging, or refactoring code
that substitutes a value, state, or control flow after something is missing,
invalid, or failed. This includes language-level defaults, optional values,
error recovery, UI placeholders, compatibility paths, and failures in
independent asynchronous work.

## Core rule

A fallback is application behavior, not a way to silence the type system.
Never add ??, a ternary, unwrap_or_default(), unwrap(), an empty catch, or an
equivalent construct merely because the compiler or type checker complains.
First determine why the value can be absent or why the operation can fail, then
repair that contract or propagate the failure to the owner that can make the
right decision.

Do not turn this rule into “all fallbacks are forbidden.” A fallback is good
when missing data or a failed dependency is an expected, understood condition,
the substitute is semantically correct, and the degraded behavior is bounded
to the part of the product that can safely degrade. The context and the
criticality of the affected operation decide.

## What to distinguish

Before changing a fallback, classify the situation:

| Situation | Proper default direction |
| --- | --- |
| Required domain data is missing | Fix the producer, schema, validation, or type contract; otherwise return or propagate an actionable error. |
| Optional, non-critical presentation data is unavailable | Preserve the primary operation and use an explicit unavailable state or carefully chosen placeholder at the presentation boundary. |
| An internal invariant is violated | Make the invariant explicit. Use a narrow assertion or panic when continuing would be incorrect; do not crash unrelated work for an optional defect. |
| An external, corrupt, or user-controlled value violates an assumption | Validate it and return a recoverable error or safe rejection. Do not treat it as unreachable just because the happy path says so. |
| An independent task or dependency fails | Classify whether that task is required for the result. Propagate required failure; isolate, record, and degrade optional failure. |
| A compatibility or legacy path is added | Confirm that the repository explicitly wants compatibility. Do not hide an unsupported format or old behavior behind a silent default. |

The key question is not “what value satisfies this type?” It is “what should
the product or operation mean when this value is unavailable?”

## Decision workflow

For each fallback candidate:

1. **Locate the boundary.** Identify the value or failure, its producer, all
   consumers, and the operation whose result it affects. Read the type,
   validation, persistence, async ownership, and error contracts around it.
2. **Trace the cause.** Find out whether the value is absent because of a
   broken invariant, incomplete input, an expected optional field, a
   recoverable dependency failure, cancellation, corruption, or an unhandled
   error. Do not infer this from the fallback expression alone.
3. **Mark criticality.** Ask whether the value affects authorization,
   identity, money, integrity, persistence, data selection, an external side
   effect, or only presentation and convenience. Map which work actually
   depends on it.
4. **Choose the owner.** Fix the source contract when the value is required,
   propagate a structured error when the caller must decide, represent an
   explicit state when absence is valid, or degrade only the independent
   non-critical consumer.
5. **Keep the substitute scoped.** A UI label such as “Name unavailable” must
   not become an account name, identifier, sort key, authorization claim,
   filename, financial input, or persisted replacement value.
6. **Make the reason observable.** Where a fallback is intentional, preserve
   enough state, logging, metrics, diagnostics, or user-visible status to
   distinguish “loaded” from “unavailable.” Do not log secrets or sensitive
   payloads.
7. **Test the failure path.** Force absence, invalid input, dependency failure,
   cancellation, and relevant falsy values. Prove that required work fails
   explicitly, optional work degrades safely, and fabricated defaults do not
   leak into critical logic.

If the cause and intended behavior cannot be determined from local contracts,
do not guess a default. Ask for direction or report the ambiguity.

## TypeScript and JavaScript

??, ?., ||, and ternaries are syntax, not policy:

~~~ts
const name = nameInput ?? '';
~~~

This is usually wrong when name is required. It turns missing data into a
valid-looking value and may move the failure into billing, persistence,
authorization, or a misleading UI. Repair the input type or validation, or
return a typed/structured error from the operation that requires the name.

The same concern applies to truthiness and optional chaining:

~~~ts
const amount = amountInput ? amountInput : 0;       // 0 may be valid
const label = user?.profile?.name ?? 'Unknown';     // may hide a broken load
const rows = loadRows().catch(() => []);             // may hide a failed query
~~~

Review these patterns carefully:

- ?? substitutes only for null or undefined, but it still masks a required
  value if absence is not valid.
- || also substitutes for false, 0, the empty string, and NaN. Do not treat a
  valid falsy domain value as missing.
- ?. is useful for genuinely optional traversal, but a long optional chain
  followed by a default needs an explicit decision about why the path may be
  absent.
- A ternary is not inherently bad. It is a good branch when its condition is
  a domain rule and both outcomes are intentional. It is a bad fallback when
  the condition only exists to satisfy a type or to hide an unexpected state.
- as, non-null assertions (value!), any, and broad casts are not fallbacks,
  but they can hide the same root cause. Validate or narrow the value at the
  boundary instead.
- Catching an error and returning [], {}, false, 0, or null is acceptable only
  when that result is a documented valid outcome and the failure is still
  observable or deliberately handled. Never use it to make a required
  operation appear successful.

An explicit presentation fallback can be correct:

~~~ts
const displayName =
  nameInput == null ? 'Name unavailable' : nameInput;
~~~

Use this only at a presentation boundary when the operation does not depend on
the name. Keep the unavailable state separate from the real name if downstream
code could otherwise reuse the string.

For concurrent work, do not let a failure in an unrelated optional task fail
the primary operation by accident, and do not use Promise.allSettled or a
catch-all as a license to ignore required failures. Classify each promise,
propagate failures that invalidate the result, and isolate only failures whose
owners can safely degrade.

## Equivalent patterns in other languages

The same review applies even when the syntax looks different:

- Python: inspect dict.get(key, default), value or default, broad
  except blocks, and functions that return None or an empty collection after
  catching an exception. Handle required errors explicitly and distinguish
  None from valid false, zero, or empty values.
- Go: inspect ignored errors, named zero-value returns, and errors converted
  into empty slices, nil pointers, or false. Return the error when the caller
  needs to decide; use a zero value only when the API contract gives it
  meaning.
- Kotlin, Swift, Java, and C#: inspect ?:, orElse, ??, TryParse defaults,
  null-object values, and catch-and-return-default paths. A language-provided
  optional helper does not establish that the default is semantically valid.
- SQL and data transforms: inspect COALESCE, NULLIF, default columns, and
  dropped rows. Do not turn missing required records or fields into successful
  business data without an explicit data contract.
- Nix and configuration code: inspect attr fallbacks, default option values,
  and missing-attribute handling. A default is safe only when the option's
  declared semantics make absence valid; otherwise fail evaluation or report
  the configuration error at the owning boundary.

## Rust

Rust's fallback methods are explicit but not automatically safe:

~~~rust
let name = input.name.clone().unwrap_or_default();
let parsed = parse_request(raw).unwrap();
~~~

These are suspicious when name or parsing is required. Prefer fixing the
input contract or propagating the reason:

~~~rust
let name = input
    .name
    .as_deref()
    .ok_or(Error::MissingName)?;
let parsed = parse_request(raw).map_err(Error::InvalidRequest)?;
~~~

Review these patterns as possible hidden fallbacks:

- unwrap(), expect(...), unreachable!(), and panic!() can be correct for a
  locally proven invariant, tests, or deliberately fatal corruption. They are
  wrong for routine external input, expected dependency failures, optional
  metadata, or a task that is not necessary for the critical result.
- unwrap_or_default(), unwrap_or(value), unwrap_or_else(...), and
  Default::default() are correct only when the chosen value has domain
  meaning. An empty collection, zero, false, or empty string is not a neutral
  replacement merely because it is easy to construct.
- ok(), filter_map, ignored Results, and discarded join errors can silently
  convert failure into absence. Use them only when dropping the failure is an
  explicit and safe policy.
- The ? operator is normally error propagation, not a fallback. Use it when
  the current operation should fail for that reason, and add context when the
  caller needs to understand the boundary.
- An optional UI label may use unwrap_or("Name unavailable"), but the resulting
  placeholder must stay out of identifiers, authorization, persistence,
  calculations, and protocol messages.

For a suspected internal invariant, debug-time failure can expose a logic bug
quickly while release code still handles a reachable failure safely:

~~~rust
debug_assert!(index < items.len(), "index was not bounded by the caller");
let Some(item) = items.get(index) else {
    return Err(Error::InvalidInternalIndex { index });
};
~~~

Do not use debug_assert! as the only protection when release builds could
continue with corrupt state. Conversely, do not replace a recoverable,
non-critical condition with a process-wide panic merely because an assertion
is convenient. A production panic can be justified for a truly impossible
invariant when continuing would be more dangerous, but keep the boundary
narrow, document the invariant, and assess its blast radius.

For async Rust, inspect both the task result and the task's semantic owner:

- If a task produces data required for the operation, propagate its error or
  cancel/rollback the operation according to the contract.
- If it only loads optional metadata, preserve the primary result, record the
  failure, and expose an unavailable state to that metadata's consumer.
- Do not unwrap a JoinHandle for convenience when an expected task failure or
  cancellation should be recoverable.
- Do not make a large operation crash because an independent task failed
  unless that task actually invalidates the operation's safety or correctness.

## Hard-coded and UI fallbacks

Hard-coded text or values are not automatically wrong. They are appropriate
when the domain explicitly specifies a degraded representation, such as
“Name unavailable” for non-critical metadata in a view. They are dangerous
when they impersonate valid data:

- empty or invented IDs, account names, paths, permissions, prices, balances,
  timestamps, or configuration values;
- a successful status after an operation failed;
- a default tenant, user, workspace, or security policy;
- silently dropping records because a display field failed to load;
- using a placeholder in a sort, filter, cache key, persistence field, or
  external request.

Prefer an explicit tagged state, status field, or error type when consumers
must distinguish loaded data from unavailable data. Put display-only
substitution at the edge, after critical work has completed.

## Failure containment

Before propagating or panicking, draw the dependency boundary:

~~~text
critical operation
  ├── required dependency failure -> fail the operation explicitly
  └── optional metadata failure  -> retain result, expose degraded metadata
~~~

A failure should affect every operation that depends on it, but no more. In
particular:

- A finance-critical operation must not panic because unrelated UI metadata
  could not be loaded.
- A large operation must not crash because an independent async task hit an
  expected or recoverable failure.
- A non-critical display failure must not be “fixed” by fabricating data that
  later enters a critical operation.
- If continuing is unsafe, stop the affected operation with an actionable
  error; do not broaden the failure into an application-wide shutdown without
  a clear safety reason.

## Review checklist

- [ ] Is the fallback solving a domain decision rather than a type-checker
      complaint?
- [ ] Was the producer, schema, validator, or invariant inspected first?
- [ ] Is missing data expected, invalid, recoverable, or truly unreachable?
- [ ] Does the operation actually depend on this value?
- [ ] Are identity, authorization, money, persistence, integrity, and external
      side effects protected from fabricated defaults?
- [ ] Are valid falsy values distinguished from missing values?
- [ ] Is the fallback scoped to the owning optional consumer?
- [ ] Is the failure still observable when degradation is intentional?
- [ ] Are assertions and panics limited to proven invariants with an
      appropriate blast radius?
- [ ] Do debug assertions improve diagnosis without being the only release
      safety mechanism?
- [ ] Are async task failures classified as required or optional?
- [ ] Do focused tests exercise the fallback, failure, cancellation, and
      recovery paths?
- [ ] If debug and release behavior differs, were both paths checked or tested?

## Output

When reviewing a fallback, lead with the concrete finding:

- **Fallback:** file, line, and construct.
- **Root cause:** why the value or operation can be missing or fail.
- **Risk:** what incorrect behavior, crash, or business impact can result.
- **Criticality:** which work depends on it and which work does not.
- **Recommendation:** repair the source contract, propagate an error, assert a
  proven invariant, or add a scoped explicit fallback.
- **Verification:** the test or check that proves the chosen behavior and
  failure containment.

If the fallback is correct, say why its input is legitimately optional, why
the substitute is semantically valid, and where the degraded behavior is
contained.

Related skills: /root-cause and /writing-tests where applicable.
