---
name: gaps-settle
description: Use when leftover work should be settled without asking the user about each item, such as the items of a `/gaps` leftover-work report, or the options, follow-ups, and gaps a conversation has left that may be safe to finish now. Not for only recording leftovers as tasks, which is `/gaps-record`, or for working through the `.agenda` backlog, which is `/autopilot`.
---

# Gaps Settle

## Objective

Settle every leftover item by its `/gaps` category, without asking the user:
record what needs the user, decide what needs a technical choice, and finish
what is safe to finish now. Invoking this skill is the user's delegation of
those technical choices. No item should end up both recorded and fixed, or
neither.

## Input

Act on, in order of preference:

1. the items given with the invocation, in the `/gaps` output format;
2. otherwise, the items of the latest `📋 **Leftover work**` report in the
   conversation;
3. otherwise, the candidates the conversation raised: offered options,
   suggestions, follow-ups, found gaps, and partially finished work.

Do not collect work from outside the chosen source.

Tag each untagged item with its `/gaps` category first, following that skill's
definitions and its rule to choose the more cautious category when an item is
borderline. If part of an item qualifies for a different category on its own,
such as a clear bug fix inside a larger redesign, split it and tag each part.

## What Counts As Unattended

An item is unattended only when **all** of these hold, whatever its tag says:

- **No user input needed.** It does not wait on the user's preference, and it
  does not depend on open or loosely refined decisions.
- **Obvious and due now.** The right outcome is clear, and it needs or should
  be done now rather than being speculative or optional polish.
- **Can be done now.** Nothing blocks it: no unfinished prerequisite, missing
  access or credentials, pending upstream change, or other external dependency.
- **Not a new feature or UI.** It does not add whole new features, user-facing
  UI, or new product surface. Such items need the user's explicit approval.
  Once the user has approved one in this conversation, and the approved scope
  is concrete, it can count as unattended.
- **Quick and straightforward.** It is a contained fix, change, or
  implementation, not a larger task such as a multi-step plan, a new
  subsystem, or work spanning many areas with its own design choices. The
  exception is a behavior-preserving restructure: refactors, file or module
  splits, renames, deduplication, and similar cleanups count as unattended even
  when they touch many lines, as long as observable behavior stays the same.
- **Safe and contained.** It has no costly, destructive, irreversible, or
  outward-facing side effects. The usual safety boundaries still apply.

Typical unattended work:

- fixing bugs whose cause and fix are clear
- closing gaps found during the work when the solution is obvious or
  straightforward
- finishing work that was started but not completed, when the remaining part
  itself qualifies as unattended
- fixing failing checks, lints, or tests at their root cause
- small consistency fixes the conversation already identified, such as stale
  references, missing wiring, or mismatched names
- behavior-preserving refactors, such as splitting files that grew too long,
  extracting or consolidating duplicated logic, or reorganizing modules along
  existing boundaries

Not unattended (illustrative examples, not a complete list):

- implementing a large feature suggestion that has not been refined yet and
  still carries open design decisions
- carrying out a large plan, such as one that adds a new feature, even when
  its steps look clear
- a "refactor" that also changes observable behavior, public interfaces, or
  data formats
- choosing between options the user has not weighed in on when the trade-off is
  a real preference rather than a clear technical winner
- downloading very large artifacts, such as many gigabytes of images or models
- wiping or repartitioning drives, deleting user data, or other destructive
  operations
- restarting or shutting down the machine, switching or activating system
  generations, or other live system-state changes
- making live network calls to arbitrary or paid endpoints, or any action that
  may cost money, publish content, or change remote state
- anything blocked on the user, a third party, or an external event

When an item is borderline, treat it as not unattended.

## Workflow

1. **Deferred:** record these with `/gaps-record` before anything else, so
   they are captured even if the rest is interrupted. Never implement them.
   For candidates taken from the conversation rather than a report, record
   only those `/gaps` would have listed; leave trivia and speculative ideas
   out.
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
   step 2, against the criteria above. Record the ones that fail with
   `/gaps-record`. Implement the rest following the repository's conventions
   and instructions, using the relevant skills where they fit, such as
   `/fix-lints`, and validate each change with the
   narrowest useful checks, broadening them when shared behavior changed.
4. **Stop when an item stops qualifying.** If work on an item reveals an open
   decision, a blocker, or a larger scope than it seemed, stop that item,
   revert only your own partial changes to it if they would leave things
   inconsistent, and record it instead. If implementation invalidates a
   decision, revisit it with `/decide`.

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

Omit a section when it has no entries, and do not pad the report with items
the chosen source never raised.

When a completion report follows, its leftover-work list names only work that
came up while settling these items, not the items themselves.

## Boundaries

The boundaries of the skills used still apply: no destructive, irreversible,
costly, outward-facing, or live system-state operations without the user's
explicit approval, and no large plans. A decision that leads to a large
undertaking is recorded, not implemented.
