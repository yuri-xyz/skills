---
name: edge-case
description: Use when the user lists edge cases and wants recent work checked against them.
disable-model-invocation: true
---

# Edge Case

## Objective

The user is pointing at one or more possible edge cases. Check whether the
agent's most recent work actually handles each one, then close the gaps:
fix the ones with an obvious answer, settle the ones that need a technical
decision with `/decide`, and confirm only the ones that need a human decision
with the user before changing them.

Treat the user's cases as hypotheses to verify, not as confirmed bugs. A case
may already be handled, may be impossible given the surrounding invariants,
or may expose a real gap.

## Protocol

1. Restate each edge case as a concrete scenario: the input, state, or
   sequence, and what correct behavior should be. Split compound cases.
2. Identify the recent work in scope: the changed files, the plan or task
   being implemented, and the code paths those changes own.
3. For each case, trace it through the real code. Read the implementation,
   callers, and invariants; run an existing test or a narrow check when that
   is cheaper and more decisive than reading.
4. Classify each case as exactly one of:
   - **Covered**: the code already handles it. Cite the file and line or the
     test that proves it.
   - **Not reachable**: an upstream invariant, type, or validation prevents it.
     Cite what prevents it.
   - **Trivial gap**: unhandled, and the correct behavior is obvious from the
     code, the surrounding conventions, or the user's stated intent.
   - **Decision gap**: unhandled, and closing it requires a choice about
     behavior, architecture, data format, compatibility, scope, or risk.
5. Fix every trivial gap directly at the owner of the behavior, with a
   focused test or assertion when the project has a test surface for it.
   Keep fixes flat per `/root-cause`; do not patch symptoms downstream.
6. Classify each decision gap as technical or human by `/decide`'s "Human
   versus technical decisions". Settle each technical gap with `/decide` as a
   delegated decision, then fix it like a trivial gap and report the choice
   and its reason so the user can override it.
7. For human gaps, use `/interview`: one question per gap, with `/decide`'s
   recommendation first and marked `(Recommended)`. Do not implement a human
   gap before the user answers; after answers arrive, implement the confirmed
   approaches and validate.

## Trivial Versus Decision

Fix without asking when the answer has one clearly correct shape, such as:

- a missing bounds, empty, null, or zero check with an obvious result;
- an unhandled error that should propagate like its neighbors already do;
- escaping, quoting, or encoding that the project already models elsewhere;
- a missing test for behavior that is already correct.

It is a decision gap when a reasonable engineer could pick differently, such
as:

- choosing between rejecting, clamping, defaulting, or silently accepting input;
- changing a public interface, data format, persisted state, or migration;
- adding a new component, dependency, state, retry, or fallback path;
- trading correctness against compatibility, performance, or simplicity;
- widening the work's scope beyond what the user asked for.

When unsure which side a case falls on, treat it as a decision gap. Most
decision gaps are technical and go to `/decide`; ones that change a public
interface, persisted data, or the work's scope, or that rest on product
intent, are usually human.

## Boundaries

- Stay on the cases the user raised plus directly adjacent cases the trace
  reveals. Mention other discoveries instead of fixing them.
- Do not invent an interview when no human decision gap remains.
- Do not weaken checks, suppress errors, or add fallbacks to make a case
  "pass"; follow `/fallbacks` when a case tempts a default value.

## Output Shape

Report once per invocation, before any interview question:

```markdown
| Edge case | Status | Evidence or action |
| --- | --- | --- |
| <scenario> | Covered | `path/to/file:42` rejects it before use |
| <scenario> | Fixed | <what changed>, tested by `<test>` |
| <scenario> | Decided | <choice> (`/decide`: <one-line reason>), tested by `<test>` |
| <scenario> | Needs decision | <the human choice to make> |

Validation: <checks run and results>
```

Then start `/interview` for the human decision gaps, if any remain.
