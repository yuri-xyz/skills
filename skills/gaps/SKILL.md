---
name: gaps
description: Use when finishing longer-running work and reporting the worthwhile work left undone and not yet recorded, such as in a completion report.
---

# Gaps

## Objective

When longer-running work is finished, tell the user what worthwhile work was
noticed but left undone and is not tracked anywhere yet, so nothing is
silently dropped. This skill only reports; it does not implement or record the
gaps.

## What to include

List work you noticed but left undone, for example because it was out of
scope, needed a user decision, should be deferred, or was blocked. Only
include actual code or configuration work: remaining changes, fixes,
improvements, bugs, missing tests, or similar.

Omit:

- gaps already recorded, for example by `/gaps-record` or `/agenda-task-create`
  earlier in the conversation, or already covered by an existing entry in
  `.agenda/tasks` or `.agenda/plans`; check those directories when they exist;
- routine follow-up steps such as committing or pushing;
- building, rebuilding, or switching system configurations;
- running or deploying the result;
- the user testing the change manually;
- trivia and speculative ideas nobody would act on.

## Categories

Tag every item with exactly one category. `/autofix` acts on each tag without
asking, so when an item is borderline, choose the more cautious category.
Write the list as plain Markdown, never inside a code block, so tools that
pick up the items do not mistake it for an example.

- `unattended`: a follow-up that can be finished now with no input, meeting
  every criterion of `/unattended`: obvious, due now, unblocked, quick or
  behavior-preserving, and safe.
- `decision`: worth doing now and safe to do, but it needs a technical
  decision first, as `/decide` defines it, that an agent can settle without
  the user.
- `deferred`: needs the user's explicit approval or belongs to later work.
  This includes changes that are substantial or would change the project
  overall, such as a noticeably different design or behavior; large
  refactors, plans, and explorations; choices that rest on the user's
  preference; and anything with dangerous or outward-facing effects, such as
  deleting files, folders, or projects, live or paid calls, remote writes, or
  exposing information.

## Output format

Order items by priority, highest first, using exactly this format:

```markdown
📋 **Leftover work**
- 🔴 (high) [unattended] Task name: short description
- 🟡 (medium) [decision] Task name: short description
- 🔵 (low) [deferred] Task name: short description
```

If nothing worthwhile and unrecorded was left over, output exactly this
instead:

```markdown
🟣 **No leftover work**
```
