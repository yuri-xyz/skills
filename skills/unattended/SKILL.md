---
name: unattended
description: Use when the conversation has left options, follow-ups, or gaps that may be safe to finish without the user, meaning obvious, small or behavior-preserving, and unblocked work.
---

# Unattended

## Objective

Review the options, suggestions, follow-ups, gaps, and unfinished work raised
in the current conversation. Select only the items that qualify as unattended,
carry them through end to end, and leave the rest for the user to decide.

## What Counts As Unattended

An item is unattended only when **all** of these hold:

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

When an item is borderline, treat it as not unattended. If part of a large
item qualifies on its own, such as a clear bug fix inside a larger redesign,
take only that part.

## Workflow

1. Collect the candidates from the conversation: offered options, suggestions,
   follow-ups, found gaps, `/gaps`-style notes, and partially finished
   work.
2. Classify each candidate against the criteria above. Mark it unattended only
   when every criterion holds.
3. Implement the unattended items, following the repository's conventions and
   instructions. Use the relevant skills where they fit, such as `/fix-lints`
   or `/refactor-reuse`.
4. Validate each change with the narrowest useful checks, and broaden them when
   shared behavior changed.
5. If an item turns out not to be unattended while you work on it, for example
   because it reveals an open decision, a blocker, or a larger scope than it
   seemed, stop that item, revert only your own partial changes to it if they
   would leave things inconsistent, and move it to the remaining list.

## Report

End with a short report:

- **Done:** each unattended item handled, in a line each, with how it was
  validated.
- **Left for you:** each skipped candidate, in a line each, with the criterion
  it failed, such as needs a decision, blocked by X, new feature, too large, or
  risky side effect.

Do not pad the report with items that were never raised in the conversation.
