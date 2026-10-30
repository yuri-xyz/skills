---
name: pending-bundle
description: Use when the user wants related, ready `.agenda` tasks consolidated into larger plans.
disable-model-invocation: true
---

# Pending Bundle

## Objective

Turn many small ready tasks into fewer, larger units of work. Group related
tasks from the `/pending` overview into sizeable bundles, write one plan per
bundle with `/agenda-plan-create`, and remove the tasks once their plan holds
everything they said. This skill reorganizes the agenda; it does not implement
anything.

Invoking this skill is the user's approval to delete the tasks a new plan
replaces, after the checks in the workflow pass.

Follow `/agenda` for the workspace layout, filenames, IDs, and statuses.

## Candidates

1. Build the `/pending` overview of ready work, with its areas and importance.
2. Keep only **tasks** that `/agenda-readiness` rates **ready**. Leave out
   plans, which are already large units, and every other class: tasks in
   progress, exploratory or deferred, waiting, decision-blocked,
   underspecified, or manual.
3. Also leave out ready tasks with a stale worktree or session, because their
   partial work lives outside the agenda and should be resumed as it is.

## Bundles

- A bundle is three or more related tasks that one plan can carry coherently:
  they share a feature, subsystem, files, or goal, so doing them together saves
  context switches or rework. Use `/pending`'s areas as a starting point, but
  group by real relatedness, not by area name alone.
- Keep a bundle to what one plan can implement and verify; split a large area
  into several bundles rather than one sprawling plan.
- Order the plan's items by dependency first, then by the tasks' importance.
- A task that fits no bundle stays a task. Do not force unrelated tasks
  together to reach the minimum size.

## Workflow

1. **Collect and group** the candidates into bundles, and list the tasks left
   as they are.
2. **Create one plan per bundle** with `/agenda-plan-create`, status `planned`.
   Carry over everything each task records: its goal, context, file paths,
   decisions with their rationale, edge cases, verification, and notes. Turn
   each task into one or more plan items, and name the replaced tasks in the
   plan's context, such as "Replaces tasks 12, 15, and 18", so their history
   stays findable.
3. **Keep the plan ready.** If writing the plan exposes an open decision or a
   gap the tasks did not have, do not settle it here: drop that plan, leave its
   tasks unchanged, and report the reason so the user can run `/unblock` or
   refine them first.
4. **Verify before removing.** For each new plan, re-read every task it
   replaces and confirm the plan preserves each of its facts, paths, and
   decisions, and that `/agenda-readiness` rates the plan ready. Fix the plan
   until both hold; never remove a task whose content is not fully carried
   over.
5. **Update references.** Search the repository for mentions of each replaced
   task, by ID, filename, or path, in other agenda entries, specs, and docs,
   and point them to the new plan.
6. **Remove the replaced tasks.** Delete each task file with `git rm` when it
   is tracked, or a plain removal when it is not. Never reuse a removed task's
   ID.

## Report

```markdown
📦 **Bundled**

- Plan 7: Title — replaces tasks 12, 15, 18 (3 items)
- Plan 8: Title — replaces tasks 20, 21, 23, 24 (5 items)

Left as tasks: Task 9 (no related tasks), Task 30 (stale worktree)
Not bundled: tasks 31, 33 — plan exposed an open decision: <decision>
Updated references: `.spec/features/x.md`, `.agenda/plans/4-[planned]-y.md`
```

If no bundle of three or more related ready tasks exists, say so and list the
ready tasks that were considered.

## Boundaries

- Do not implement plans or tasks; use `/agenda-implement` once the user asks.
- Do not bundle or modify existing plans, or tasks outside the candidates.
- Do not commit unless the user asks; then use `/git-commit`.
