---
name: debug-trace
description: Use when a long or multi-session debugging effort needs its evidence, ruled-out theories, and next steps recorded under `.debug/traces`.
---

# Debug Trace

Use this skill to keep a durable investigation note for the current bug. The trace should make the next agent run start from what is already known instead of rediscovering the same facts.

## When To Use

Use this skill automatically during bug investigations when new information materially changes the debugging state, including:

- A log, test, reproduction, or command output provides key evidence.
- Code inspection reveals a likely boundary, branch, invariant, or state transition involved in the issue.
- A hypothesis is confirmed, weakened, ruled out, or superseded.
- The next best debugging direction changes.

Do not wait for an explicit `/debug-trace` request when those events happen.

## Workflow

1. Identify the current problem being investigated from the conversation, repo context, logs, failing command, or active debug instrumentation.
2. Create `.debug/traces/` if needed.
3. Reuse an existing trace file when it clearly matches the same problem. Otherwise create a new Markdown file with a short kebab-case name, such as `.debug/traces/niri-resume-hang.md`.
4. Read the existing trace before editing it, and preserve useful prior evidence.
5. Add or update only concrete investigation state:
   - Symptom and scope.
   - Evidence observed from logs, commands, tests, screenshots, reproduction steps, or code inspection.
   - Things narrowed down, including paths, branches, state transitions, inputs, outputs, and timing.
   - Theories ruled out or deprioritized, with the evidence that made them less likely.
   - Best next directions to keep narrowing the problem.
6. Keep speculative notes clearly labeled as hypotheses. Do not present guesses as evidence.
7. Avoid secrets, tokens, private keys, credentials, cookies, personal data, and large payload dumps. Redact or summarize sensitive values.
8. Report the trace file path and the main update made.

## Trace Format

Prefer this structure unless the existing file already has a useful shape:

```markdown
# Short Problem Name

## Problem
- Current symptom:
- Reproduction or trigger:
- Scope:

## Evidence
- ...

## Narrowed Down
- ...

## Ruled Out
- [ ] Theory:
  Evidence:

## Next Directions
- ...
```

Use checkboxes in `Ruled Out` only when they help scan open vs closed theories. It is fine to write normal bullets when that reads better.

## Boundaries

- Trace files are investigation notes, not source-of-truth docs or permanent project plans.
- Keep trace files under `.debug/traces/*.md`.
- Do not edit generated output or runtime state just to update a trace.
- Do not delete debug logs, markers, or trace files as part of this skill. Cleanup belongs to `/debug-cleanup`.
