---
name: autopilot
description: Use when the user runs `/autopilot`, directly or as a `/goal` condition, or explicitly asks you to work through the ready `.agenda` backlog on your own, picking settled, code-focused tasks and plans, implementing them, and committing each unit until none are left. Not for only listing ready work, which is `/pending`.
---

# Autopilot

## Objective

Work down the repository's ready agenda without the user. Pick the pending
tasks and plans that are settled and code-focused, implement them, commit each
unit of work, and repeat until no applicable entry is left. Small tasks come
first, bundled into larger units; plans follow once the small tasks run out.
The run feeds itself: gaps it records along the way join the selection when
they qualify, so it keeps going until no qualifying entry is left, including
its own.

Run it as `/autopilot` for one pass, or as `/goal /autopilot` to keep going
across turns until the selection is empty.

Invoking this skill is the user's go-ahead to implement and commit every
entry that passes the selection below. It does not approve anything else.

Follow `/agenda` for the workspace layout, filenames, and statuses, and
`/agenda-implement` for how each entry is carried out, its progress records,
and its completion bar.

## Selection

Build the `/pending` overview of ready work, then keep an entry only when all
of these hold:

- `/agenda-readiness` rates it **ready**: no agent is working on it, its
  decisions are settled, and it is not exploratory, intentionally deferred,
  waiting, underspecified, or manual.
- It is code-focused: fix a bug, implement a feature, handle an edge case,
  refactor, or update docs, config, or tests, verified by fast, narrow checks
  such as a parse, a lint, an evaluation, a type check, or one focused test.
- Its outcome does not depend on long-running or heavy work, such as golden or
  snapshot test runs, full test suites, fuzzing, benchmarks, formal
  verification, or long builds.
- Its outcome does not involve deploying or interacting with external
  services, accounts, devices, or live system state.

When unsure whether an entry qualifies, leave it out. Keep a list of the
entries left out and why, so later rounds do not weigh them again.

## Units Of Work

- **Task bundles.** Take three to five selected tasks at a time and implement
  them together as one unit. Prefer tasks that share an area, files, or
  context, and that do not depend on one another or on other pending work.
  Order the bundle by importance, highest first, following `/pending`. Take
  fewer when fewer qualify.
- **Plans.** Once no selected task is left, take one selected plan at a time,
  of any size. A plan is one unit; for a large plan, commit at each coherent
  milestone, such as a finished group of items, rather than only at the end.

Resume an entry with a stale worktree or session from its partial work, as
`/pending` notes, instead of starting over.

## Loop

1. **Select** the next unit from a fresh `/pending` overview, since the
   agenda changes as entries finish, other agents work, and the run records
   new entries.
2. **Claim** every entry of the unit following `/agenda`'s Claims procedure
   before any other work on them, including reading their code: check for
   another assignee, write the claim on the default branch, and re-read it.
   Drop an entry another agent claimed first, and release each claim when its
   entry is done or stops qualifying.
3. **Implement** each entry in the unit with `/agenda-implement`, recording
   progress and moving it to `done` once it meets its completion bar. Settle
   technical questions that come up with `/decide`, and note the choice in
   the entry. Run only the narrow checks the entry needs, under `nice`.
4. **Record gaps** the unit left, such as bugs it found, edge cases it did not
   cover, or follow-ups it surfaced, with `/gaps-record`. Record only real
   gaps; never split a unit's own work into new entries to keep the run
   going.
5. **Commit** the unit with `/git-commit`, scoped to the files the unit
   changed, including its agenda entries and the gaps it recorded. Other
   agents may share the checkout; never commit, revert, stash, or reformat
   their changes.
6. **Repeat** from step 1 until the selection is empty. Entries the run
   recorded go through the same selection as any other; those that qualify
   are implemented in later rounds, and the rest are left out.

### When an entry stops qualifying

When an entry turns out to need a human decision, an external or live
action, or heavy verification it did not show at selection, stop work on that
entry: record what is left and why in its notes, following `/agenda-implement`
for blockers, release its claim, and leave it pending. Finish and commit the rest of the unit,
then carry on. Never ask the user mid-run.

### When an entry needs an upstream change

Sometimes an entry depends on a change in a platform, library, language, or
tool the project builds on. When we own that
upstream, meaning the user or their organization created or maintains it as
confirmed from its remote or manifest, and its checkout is available locally,
fix it upstream instead of working around it here. Never ship
a local workaround, shim, vendored patch, override, or temporary fix in its
place.

1. Make the change in the upstream checkout at its root cause, following
   that repository's own instructions, conventions, and
   narrow checks. Keep the upstream change to what the entry needs.
2. Commit it there, scoped to your own changes; other
   agents may share that checkout too.
3. Continue the entry here. When the project can consume the upstream commit
   only after a push or release, which autopilot cannot do, finish
   everything that does not depend on it, record the upstream commit and the
   exact pin or lock change waiting on it in the entry's notes, and leave the
   entry pending.

When the upstream is not ours, or no local checkout exists, treat the entry
as one that stopped qualifying.

## Boundaries

- Do not create, bundle, or reword entries beyond recording progress,
  blockers, and the gaps units leave, and do not take on work outside the
  selected entries, other than the upstream changes they need.
- Do not push, open pull requests, or perform any other remote or
  outward-facing action.
- Do not run builds, switches, or other state-changing commands the
  repository's instructions hold back.

## Report

When the selection is empty, the final message is this report and any
completion report, with no text before or after them: no recap of the last
step, no commentary on the run.

```markdown
🛩️ **Autopilot**

Implemented 1 plan and 2 tasks: 1 feature, 1 bug fix, and 1 improvement.

- 🗺️ Plan 19: Show backlinks and unlinked mentions on pages

- 📌 Task 12: Keep the cursor in place when a page reloads
- 📌 Task 15: Reject empty tags in the CLI

- ⬆️ Upstream `libexample`, for Task 15: Allow empty string patterns (unpushed)

⏸️ 41 entries left out: 34 need decisions, 3 are too large for one unit, 2 are waiting on other work, 2 need you or an outside service.
```

- Open with one count sentence: how many plans and tasks were finished, and
  how many of them are features, bug fixes, and improvements (refactors,
  docs, config, and tests count as improvements). Leave out zero counts.
- List each finished entry on one line, grouped by kind: all plans first,
  then all tasks, then upstream changes, with a blank line between groups and
  entries ordered by number within each. Each line has its marker, its kind
  and number, and a one-line brief of what it does in plain words, not its
  commit subject. Mark an upstream change `(unpushed)` while it is.
- Count every entry left out or stopped in the ⏸️ line, grouped by reason,
  as `/pending`'s footer does. Name an entry only when the user must act on
  it, such as one stopped mid-run, and keep the detail in each entry's notes.
- When nothing qualified, replace the count sentence and list with
  `Nothing qualified for autopilot.` and keep the ⏸️ line.

Then add any completion report the repository's or user's instructions ask
for, formatted as `/checks` and `/gaps` produce it.
