---
name: gaps-record
description: Use when the gaps left after recent work should be saved as agenda tasks.
---

# Gaps Record

## Objective

After finishing a piece of work, turn whatever it left unresolved into
`.agenda` tasks so nothing is lost. Tasks the agent could complete on its own
are written as normal, ready tasks. Tasks that still depend on user direction
are written with a "not ready" disclaimer that lists the open decisions, so no
later agent mistakes them for work that can start.

This skill captures gaps; it does not close them. Do not implement fixes
while recording.

## Protocol

1. Review the recent work: the request, plan or task, the diff, validation
   results, and anything deferred, skipped, stubbed, or mentioned as a
   follow-up during the conversation.
2. List the concrete gaps, such as unfinished items, known limitations,
   unhandled edge cases, missing tests or validation, `TODO` markers the work
   introduced, failing or unrun checks, and deferred cleanups.
3. Drop anything that is not a real gap: work already done, speculative
   improvements nobody asked for, and items already tracked. Search
   `.agenda/tasks` and `.agenda/plans` first and update an existing entry
   instead of creating a duplicate.
4. Group gaps that one change would close into a single task; split gaps that
   could be done or decided independently.
5. Classify each task as **ready** or **not ready** (see below).
6. Create each task with `/agenda-task-create`, following `/agenda` for the
   filename, ID, and `todo` status. Add the disclaimer to not-ready tasks.
7. Report the created or updated task paths.

## Ready Versus Not Ready

A task is **ready** when an agent could implement it without further input:
the desired outcome is clear, the approach follows from the code or existing
conventions, and no behavior, architecture, scope, or risk choice is open.

A task is **not ready** when it needs the user to choose or clarify anything
material, such as desired behavior, architecture or data model, scope,
compatibility, a dependency, a tradeoff between competing goals, or a
real-system action that needs approval. When unsure, mark it not ready.

## Not-Ready Disclaimer

Keep the normal task shape and `todo` status; do not invent a new status.
Put this disclaimer directly under the title, and list every open decision:

```markdown
# Task title

> **Not ready:** this task has open decisions that the user must resolve
> before implementation. Do not start it until every item under
> `## Open Decisions` is answered and that section is removed.

<Problem, context, desired outcome, and relevant paths as usual.>

## Open Decisions

- <The decision, the viable options, and the agent's recommendation if any.>
```

Describe each decision precisely enough that it can be answered later with
`/interview` without rereading this conversation. Include what is already
known and what each option would change.

## Output Shape

```markdown
Ready:
- `.agenda/tasks/<id>-[todo]-<slug>.md` — <one-line gap>

Not ready (needs your input):
- `.agenda/tasks/<id>-[todo]-<slug>.md` — <open decision>

No gaps captured: <reason>, when nothing remained.
```
