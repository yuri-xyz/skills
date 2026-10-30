---
name: hacky
description: Use when the current direction might be a hack or workaround rather than a proper root-cause solution, or the user asks whether it is.
---

# Judge Hacky

## Objective

Perform a short self-check on the current direction before continuing. Decide whether the work is a proper long-term fix or a hacky workaround.

This skill is a checkpoint, not a full architecture review. Keep it brief unless the answer exposes a real problem.

## Protocol

1. Pause current implementation work.
2. Briefly inspect the current plan, recent edits, and relevant code context if needed.
3. Ask: is this addressing the root cause and intended design, or is it a temporary workaround that only makes the symptom disappear?
4. If the approach is proper, say so briefly and continue the original work.
5. If the approach is hacky or uncertain, stop before adding more code.

## Treat As Hacky

Use the workaround signatures defined in `/layering`. In short: new logic whose job is to compensate for logic that is already wrong, duplicated behavior that is owned elsewhere, hidden errors, dependence on timing or ambient state, a single case passing while the failure mode survives, and temporary code with no removal path.

If the answer needs more than this checkpoint — comparing real alternatives or judging the architecture — escalate to `/approach`.

## If It Is Proper

If the current direction is the intended robust fix:

- State the reason in one or two sentences.
- Continue with the work the agent was already doing.
- Do not derail into a long explanation just because `/hacky` was invoked.

## If It Is Hacky

If the current direction is hacky, temporary, or likely wrong:

- Stop immediately.
- Explain why it is going in the wrong direction.
- State what the root-cause or long-term fix should be instead.
- Ask for explicit confirmation before continuing with the hacky path.

## Output Shape

Use one of these forms:

```markdown
Proper: <brief reason>. Continuing.
```

or:

```markdown
Hacky: <brief reason>.

Better path: <root-cause direction>.

I should not continue with the workaround unless you explicitly confirm.
```
