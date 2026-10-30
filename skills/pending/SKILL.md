---
name: pending
description: Use when the user asks what pending agenda work is ready to do, or when another skill, such as `/autopilot`, needs the ready-work overview as a step.
---

# Pending

## Objective

Give the user a quick overview of the ready work waiting in the repository's
`.agenda` workspace, so they can pick what to do next. This skill only reports;
it does not create, edit, rename, or implement agenda entries.

Follow `/agenda` for the workspace layout, filename statuses, and the not-ready
disclaimer shape.

## Protocol

1. Find the repository root and read `.agenda/tasks` and `.agenda/plans`. If
   neither exists or both are empty, report that there is no agenda.
2. Collect pending entries: tasks with `todo` or `in_progress` status, and
   plans with `planned` or `active` status. Skip `done` entries. Read each
   pending entry's content, not just its filename.
3. Filter out every entry that is not ready (see Readiness).
4. Assign each remaining entry an importance and a feature or area, and mark
   whether it is independent.
5. Report them in the output format below.

## Readiness

Classify each pending entry with `/agenda-readiness` and keep only the ones it
rates **ready**. Leave out the rest, including entries an agent is already
working on, manual entries that act on live external state and need your
oversight, and exploratory or intentionally deferred entries that are being
considered rather than given the go-ahead. Count the entries left out for the
footer.

An entry left unfinished, with no agent working on it, is listed like any other
ready entry; note its stale worktree or session in its summary so it is
resumed rather than restarted.

## Importance

Judge how important each entry likely is from its content and the repository
context; do not just copy any stated priority without checking it still holds.

- 🔴 **High**: correctness, security, data-loss, or broken-workflow issues,
  work that unblocks other entries, and unfinished `active` or `in_progress`
  work left stale.
- 🟡 **Medium**: meaningful improvements, features, or cleanups with clear
  value but no urgency.
- 🟢 **Low**: polish, minor refactors, nice-to-haves, and speculative ideas.

## Independence

Mark an entry 📦 **independent** when it can be done in parallel with the rest
of the pending work without coordination beyond trivial steps:

- it does not depend on another pending entry, and no other pending entry
  depends on it;
- it is unlikely to edit the same files, modules, or shared configuration as
  another ready entry, so parallel work would not conflict;
- it needs no shared migration, lockfile or input update, live system-state
  change, or approval that other work also waits on.

Check this against the entries' content and the files they name, not only
their areas. When unsure, leave the mark off.

## Areas

Group entries by the feature, subsystem, or area they concern, such as
networking, desktop, or build tooling. Derive area names from the entries and
the repository's own structure, keep them short, and merge areas that would
hold a single closely related entry into a broader one when that reads better.

## Output Format

Order areas by their most important entry, then by entry count. Within each
area, order entries by importance, highest first. Use exactly this shape:

```markdown
📋 **Pending work**

**Area name**
- 🔴 Task 3: Title — one-line summary of what it does and why it matters
- 🟡📦 Plan 2: Title — one-line summary (active, item 2 of 5)

**Other area**
- 🟢📦 Task 7: Title — one-line summary

📦 independent: can run in parallel with other work
⏸️ 4 entries left out (in progress, manual, blocked, waiting, or not given the go-ahead)
```

- Label entries `Task <id>` or `Plan <id>` using their numeric ID.
- Put 📦 directly after the importance emoji, with no space, for independent
  entries. Show the 📦 legend line only when at least one entry carries the
  mark.
- For `in_progress` tasks and `active` plans, note progress in parentheses
  when it is visible from item statuses or checklists.
- Omit the footer when nothing was filtered out.

If nothing ready remains, output exactly this instead, keeping the footer when
blocked entries exist:

```markdown
🟣 **No pending work**
```
