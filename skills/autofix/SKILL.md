---
name: autofix
description: Use when the user wants the leftover work from a /gaps report settled without being asked about each item.
disable-model-invocation: true
---

# Autofix

## Objective

Take the leftover work handed over and settle every item by its `/gaps`
category, without asking the user: record what needs the user, fix what is
safe to finish now, and decide what needs a technical choice and then carry
it through. Invoking this skill is the user's delegation of those technical
choices. No item should end up both recorded and fixed, or neither.

For the cautious path that decides nothing, use `/unattended`, which leaves
everything that is not unattended for the user, or `/gaps-record` alone.

## Input

Act on the leftover-work items given with the invocation, in the `/gaps`
output format. When none are given, take the items of the latest `📋
**Leftover work**` report in the conversation. Do not collect other work.

Tag each untagged item with its `/gaps` category first, following that skill's
definitions and its rule to choose the more cautious category when an item is
borderline. If part of an item qualifies for a different category on its own,
split it and tag each part.

## Workflow

1. **Deferred:** record these with `/gaps-record`, before anything else, so
   they are captured even if the rest is interrupted. Never implement them.
2. **Decision:** settle each decision, or group of decisions one coherent
   solution would settle, with `/decide` as a delegated decision. A decision
   `/decide` finds to be human is recorded with `/gaps-record` as not ready,
   carrying its findings. Then classify the work each settled decision
   unblocks:
   - **Pursue**: worth doing now and small or medium enough to finish in this
     session. Treat it as unattended work in step 3.
   - **Record**: too large, blocked, or not worth it now. Record it with
     `/gaps-record`, or update its existing task, with the decision and its
     rationale so it is not re-litigated.
   - **Drop**: the decision shows it should not be done. Close any existing
     task for it with the rationale.
   Record before implementing so the outcome survives an interruption.
3. **Unattended:** check each unattended item, and each pursued item from
   step 2, against the `/unattended` criteria. An `unattended` tag still has
   to meet them. Fix the ones that do following the `/unattended` workflow,
   including its validation, and record the rest with `/gaps-record`. If an
   item stops qualifying while you work on it, stop, revert only your own
   partial changes when they would leave things inconsistent, and record it
   instead; if implementation invalidates a decision, revisit it with
   `/decide`.

## Report

```markdown
Decisions:
- <decision> — <choice>: <one-line rationale>

Fixed:
- <item> — <how it was validated>

Recorded:
- `.agenda/tasks/<id>-[todo]-<slug>.md` — <item>, <why it was not fixed>

Dropped:
- <item> — <why it should not be done>

Left for you:
- <human decision or approval-gated step>
```

Omit a section when it has no entries.

When a completion report follows, its leftover-work list names only work that
came up while settling these items, not the items themselves.

## Boundaries

The boundaries of the skills used still apply: no destructive, irreversible,
costly, outward-facing, or live system-state operations without the user's
explicit approval, and no large plans. A decision that leads to a large
undertaking is recorded, not implemented.
