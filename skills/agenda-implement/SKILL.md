---
name: agenda-implement
description: Use when the user asks to implement a specific agenda plan or task to completion, or to resume or continue the active or most recent unfinished one.
---

# Agenda Implement

Implement the plan or task the user specifies alongside this skill, or resume the one already under way. Treat it as the active objective and carry it through to completion unless the user redirects you or a genuine external blocker prevents progress.

## Target

The target is one `.agenda/plans/` or `.agenda/tasks/` entry, or a plan or task given directly in the conversation. When several tasks are named together, implement them one at a time in the given order.

When the user names no target, such as when asking to continue or resume, the target is the plan or task that was active or most recently being implemented in this conversation, or else the one entry marked `active` or `in_progress` in `.agenda/`. If none can be identified with confidence, say there is no recoverable plan or task instead of guessing or inventing one. If the target is already complete, respond exactly `Already completed`, with no other text.

- **Plan:** the deliverables are its items and verification checklist. Progress lives in item heading statuses, checkboxes, and `## Progress Notes`.
- **Task:** the deliverable is the described outcome or completion condition. Progress lives in appended `## Notes` entries. When a task is too large to finish as one coherent change, say so and suggest turning it into a plan with `/agenda-plan-create` instead of improvising a hidden plan.

Before starting, check for a `> **Not ready:**` disclaimer or an `## Open Decisions` section. If either is present, do not implement. List the open decisions and ask the user to resolve them; record the answers in the entry and remove the markers per `/agenda` before continuing.

## Core Behavior

1. Read the entry carefully and identify its concrete deliverables.
2. If the entry is already in progress, first inspect its recorded progress: plan checklists and progress notes, or task notes. Treat items marked completed or checked off as already implemented unless there is concrete evidence otherwise; do not re-audit them by default.
3. Convert the deliverables into a concise working checklist with `update_plan` or the harness's equivalent checklist tool. Keep at most one item `in_progress`, and focus on the next incomplete item.
4. Implement the current item thoroughly, including production code, tests, docs, config, and generated source-of-truth updates when those are part of the repo's normal workflow. Do not do broad exploratory or unrelated bulk work ahead of the current item.
5. After finishing each item, or a small explicitly bounded group of tightly coupled items, immediately record progress in the entry and update the working checklist. Do not defer several completed items into one bulk status update, but do not update it after every tiny edit.
6. Give concise user-facing progress updates when significant progress is made, when beginning a new major phase, or when resolving a blocker.
7. Keep going until the entry is genuinely complete and verified.

## Entry Files And Status

When the entry lives under `.agenda/`, follow `/agenda` for storage rules, filenames, and status conventions:

- Move the entry to its in-progress status when work starts (`active` for a plan, `in_progress` for a task) and to `done` only when it meets the completion bar below, renaming the file without changing its ID or slug.
- For plans, keep item heading statuses and checkboxes synchronized and add dated progress notes for durable discoveries.
- For tasks, append progress, discoveries, and completion evidence to `## Notes` instead of rewriting the original description.

## Blockers

If you hit a blocker:

- Investigate the root cause in the code, tests, configuration, or environment.
- Prefer durable fixes over shortcuts.
- Do not add hacks, broad suppressions, weakened tests, skipped checks, temporary shims, or workarounds just to move forward.
- If the blocker reveals a real prerequisite, implement or document that prerequisite in the correct source-of-truth location.
- After fixing the blocker, continue with the entry instead of stopping at the unblock.

Only stop and ask the user when the next step requires a decision that cannot be inferred safely from the entry or codebase.

## Better Approaches Found Mid-Work

An entry's locked decisions, chosen libraries or dependencies, assumptions, and approaches record the best knowledge available when it was written, not a contract to follow verbatim. When implementation uncovers something better, such as a cleaner approach, a better-suited or better-maintained dependency, a wrong or outdated assumption, or an option the entry did not weigh, prefer the better path regardless of what the entry says:

1. When the better path is clear, take it. When you are unsure, settle it with `/decide` as a delegated decision, scaled to the stakes, weighing the new evidence against the entry's original rationale.
2. Update the entry before continuing: revise the affected items, decisions, and checklists, and record what changed, why, and the evidence in the plan's `## Progress Notes` or the task's `## Notes`. Never leave the entry describing an approach the code no longer follows.
3. Continue implementing without waiting for the user.

Stop and ask only when the change needs explicit human input by `/decide`'s definition, such as product or UX direction, scope, removed features, data or money, outward-facing effects, or reversing a decision the entry records as the user's own choice. Adding a new dependency still goes through `/dependency-add`, which decides when the user's approval is needed.

## Testing And Verification

Add or update tests for meaningful behavior changes. Choose the test scope based on risk:

- focused tests while iterating;
- broader crate or workspace tests when shared behavior changes;
- lint, type, format, build, or generation checks when the work touches those surfaces.

Before finishing, run the checks that prove the implementation. If a check cannot run, report the exact command and blocker.

## Resuming Work

When picking up an existing or partially completed plan or task:

1. Read the recorded checklist, notes, comments, or prior summary.
2. Assume items already marked completed or checked off are done. Perform only the minimal targeted check needed when a pending item depends on them, the recorded state conflicts with the repository, or verification exposes a problem.
3. Orient yourself around the next incomplete item. Use `git status` and a targeted `git diff` to understand pending work when needed, then inspect only the directly relevant files, call paths, tests, or configuration needed to execute that item.
4. Correct stale recorded state only when a targeted check provides concrete evidence that it is stale.
5. Resume from the next pending item rather than repeating completed work or broadly re-exploring the repository.
6. Keep the original goal and scope. Do not start a new plan, switch to other work, or take on adjacent cleanup the entry does not need.

## Completion

A plan or task is complete only when:

- every required deliverable is implemented or explicitly made obsolete by the final design;
- blockers found along the way are fixed at the root cause;
- relevant tests and checks pass or any remaining verification gap is clearly explained;
- the entry's recorded status and notes reflect the final state;
- the final response summarizes what changed, what was verified, and any residual risk.

Record follow-up work the implementation leaves behind as new tasks with `/agenda-task-create` rather than silently widening scope.
