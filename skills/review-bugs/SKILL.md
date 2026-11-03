---
name: review-bugs
description: Use when reviewing changes for latent bugs, such as off-by-one errors, unbounded inputs, integer overflow, unchecked division, lossy conversions, Unicode and byte handling, or untested edge cases.
---

# Review Bugs

## Objective

Review the current or proposed code changes for bugs that pass the happy path
and fail on edge cases: boundaries, sizes, numbers, text, and inputs from
users or the outside world. Find them by reasoning about concrete inputs, not
by pattern matching, and prove each one with a failing test or a specific
input before fixing it.

Prefer small, local fixes that make the edge case explicit. Do not rewrite
working code to guard against inputs that cannot reach it.

## Workflow

1. Inspect the recent diff, pending plan, or relevant files, and the callers
   and inputs that reach the changed code.
2. Mark the code most likely to hide bugs: parsing, indexing and slicing,
   arithmetic, size and offset math, loops and recursion, text handling,
   filesystem and network operations, retries, and anything fed by users,
   files, environment, or external services.
3. Walk that code through the classes in `references/bug-classes.md`. For
   each candidate, name the concrete input that breaks it and the observable
   result: a crash, wrong output, hang, data loss, or resource exhaustion.
   Drop candidates whose breaking input cannot reach the code.
4. Check the tests: for each risky path, is there a test for the empty,
   single, boundary, maximum, malformed, and non-ASCII cases that apply? Note
   the missing ones.
5. Fix a bug when it is confirmed, local, and the right behavior is clear:
   write a failing regression test first when the project has tests, fix it,
   and watch the test pass. Add missing edge-case tests for risky code even
   when no bug is found.
6. Report, without fixing, bugs whose correct behavior is a decision (settle
   technical ones with `/decide` when asked to fix them), and bugs whose fix
   is large or crosses module boundaries.
7. Run the focused tests and checks for the changed code.

## Prefer Fixes Like

- Using the language's checked, saturating, or wider arithmetic where
  overflow is reachable, and rejecting out-of-range values at the boundary.
- Explicit limits for depth, size, count, time, and retries, with a clear
  error when one is hit, rather than an arbitrary silent cutoff.
- Parsing and validating external input once, at the edge, into a typed
  value.
- Explicit conversions with checked failure in place of implicit coercion.
- Measuring, slicing, and truncating text in the unit the context needs:
  bytes for storage, code points for protocols, grapheme clusters for display.
- Inclusive or exclusive bounds stated in names or types, such as `end` versus
  `last`, and half-open ranges where the codebase uses them.

## Avoid

- Defensive checks for states the types or callers already rule out, except
  on authentication, authorization, and other security-critical paths, where
  `/review-security` asks for layered checks and impossible-state assertions.
- Silently clamping, truncating, or defaulting bad input when the caller
  should see an error.
- Changing public behavior, error types, or formats beyond fixing the bug.
- Speculative limits with no reasoning behind the number; state why each
  limit is what it is.
- Overlapping other lenses: use `/review-perf` for speed, `/review-hermetic`
  for nondeterminism, and `/review-privacy` for data exposure. Report
  security-relevant findings, such as path traversal or injection, and
  leave the security pass to `/review-security`.

## Output

If no bug was found, say so and name the areas and bug classes reviewed.

Otherwise list findings, most severe first:

```markdown
- 🔴 <file:line> <bug class>: <breaking input> → <what happens>. Fixed; regression test `<name>`.
- 🟡 <file:line> <bug class>: <breaking input> → <what happens>. Not fixed: <why>.
- 🔵 <file:line> Missing test: <edge case>. Added / not added: <why>.
```

🔴 crashes, corrupts data, hangs, or exhausts resources on reachable input;
🟡 wrong result on a plausible edge case; 🔵 a missing test or a guard for
an unlikely input. Finish with the checks run, or why none were.
