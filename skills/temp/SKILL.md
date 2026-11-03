---
name: temp
description: Use when the user says code changes are temporary or not meant to be permanent, or when an uncertain fix should be tried as a temporary trial pending user feedback.
---

# Temp

## Rule

When making a temporary code or configuration change, add a clear TEMP comment at the exact site of the temporary behavior.

Use this form in languages and files that support `//` comments:

```text
// TEMP: <concise explanation of why this temporary behavior exists and when it should be removed>
```

For files that do not support `//` comments, use the file's native comment syntax while preserving the exact `TEMP:` prefix, such as `# TEMP:`, `<!-- TEMP: ... -->`, or `/* TEMP: ... */`.

## Expectations

- Add the TEMP comment immediately above the temporary block, or on the same line for a tiny one-line change when that is clearer.
- Explain the reason, not just the action. Prefer "TEMP: Bypass auth while local OAuth callback is being repaired" over "TEMP: disable auth".
- Include the removal condition when it is known.
- Do not hide temporary behavior in vague comments like `TODO`, `hack`, or `for testing`.
- Do not mark permanent fixes, normal feature flags, or durable configuration choices as TEMP.
- Mention the temporary annotation in the final response when code was changed.

## Trials

Use a trial when a fix is plausible but not yet proven. Treat the change as a
trial: mark it temporary, explain what would confirm it, and be ready to either
promote it to permanent code or manually unwind it based on user feedback.

### Trial Lifecycle

1. State the hypothesis the trial is testing.
2. Apply the smallest reasonable change that tests that hypothesis.
3. Mark the trial change with a `TEMP:` comment as described in the Rule above.
4. Explain in the final response that the change is temporary and what confirmation would make it permanent.
5. If the user later says it worked, remove the `TEMP:` annotation and clean up the implementation so it reads as normal durable code.
6. If the user later says it did not work, treat that as evidence that the hypothesis was wrong or incomplete. Investigate further and usually remove or revise the failed trial.

### Trial Annotation

For a trial, the reason is the hypothesis and the removal condition is its
confirmation:

```text
// TEMP: Trial fix for <hypothesis>; remove once <confirmation condition>.
```

### When To Use A Trial

Use a temporary trial when:

- The proposed fix is plausible but the true root cause is not confirmed.
- The only reliable validation is user feedback, a live environment, hardware behavior, timing, production data, or another condition the agent cannot fully reproduce.
- The change exists mainly to address the proposed issue rather than being an obvious general improvement.
- The user explicitly asks to try the approach, try it for now, or mark it temporary until confirmation.

### When Not To Use A Trial

Do not mark a change temporary when it is already confirmed as the root-cause fix, a normal durable configuration choice, or a clear improvement that should remain regardless of whether the suspected issue is fixed.

If investigation reveals a plainly wrong bug, a missing invariant, a broken test, or an obvious cleanup that is valuable independently, keep that improvement as durable code. Only the uncertain issue-specific workaround should be temporary.

### If The Trial Works

When the user confirms the trial worked:

- Remove the `TEMP:` annotation.
- Clean up any trial-specific wording, overly narrow comments, debug scaffolding, or extra defensive code that is no longer needed.
- Keep the implementation if it is now the confirmed durable solution.
- Add or update tests or validation when feasible so the confirmed behavior is covered.

### If The Trial Fails

When the user says the trial did not work:

- Treat the failed result as evidence against the hypothesis.
- Reopen the investigation instead of stacking another workaround on top.
- Usually remove the failed temporary change before trying a different approach.
- Preserve only changes that are clearly useful independently of the failed trial, such as general bug fixes, stronger validation, clearer tests, or cleanup that should remain regardless.
- Explain what was learned from the failed trial and what hypothesis is being tested next.

### Manual Reversal Rule

Do not use `git restore`, `git checkout`, `git reset`, or similar commands to undo a failed trial. Those commands can discard unrelated user or agent work.

Undo failed trials by manually editing the affected files back to the appropriate state, using the previous content, surrounding code, and the user's feedback as guidance. Preserve unrelated changes.

### Trial Output

When applying a trial, report:

- The hypothesis being tested.
- The temporary annotation added.
- How the user can confirm success or failure.
- Any checks run locally.

When responding to success or failure feedback, report what temporary code was promoted, removed, or revised.
