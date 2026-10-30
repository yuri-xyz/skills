---
name: keep-or-revert
description: Use when new evidence calls into question whether earlier changes made for an issue are still worth keeping.
---

# Judge Keep Or Revert

## Overview

Use this skill as an advisory checkpoint after new information changes the understanding of an issue. The question is not "revert everything"; it is "which previous changes still deserve to exist, and which should be manually cleaned up because they did not address the real problem?"

## Core Rule

Treat this as a question, not a mandate. Do not assume prior changes must be reverted. Inspect the changes and decide whether each one is still justified.

Keep changes that are true improvements independent of the failed or superseded hypothesis. Remove or revise changes that only made sense as an attempted fix for a hypothesis that is now unlikely, disproven, or replaced by a better root-cause understanding.

## When To Use

Use this skill after:

- The user reports that a previous fix or trial did not work.
- Investigation reveals a different root cause than the one earlier changes targeted.
- A temporary workaround, layered patch, or speculative change may no longer be appropriate.
- Several changes accumulated during debugging and some may now be unrelated to the real fix.
- The user asks whether previous edits should be kept, cleaned up, or manually reverted.

## Review Workflow

1. Identify the prior changes under review from the diff, recent edits, user context, or affected files.
2. Restate the new knowledge: failed user feedback, newly found root cause, better hypothesis, or changed scope.
3. For each relevant change, classify it as:
   - **Keep**: independently correct, useful, or clarifying even if it was not the root-cause fix.
   - **Remove**: only existed for the failed/superseded hypothesis or now adds misleading behavior.
   - **Revise**: contains useful intent but needs to be reshaped around the new root-cause understanding.
   - **Ask**: unclear whether the user wants to preserve behavior or undo it.
4. Explain the classification before editing when the cleanup is non-trivial.
5. Manually edit files to remove or revise changes that should not remain.
6. Preserve unrelated user work and unrelated agent work.
7. Run focused checks when the cleanup touches behavior, tests, config, or buildable code.

## Keep Criteria

Keep a previous change when it:

- Fixes a clear bug regardless of the current issue.
- Strengthens validation, tests, types, error messages, or invariants in a way that remains correct.
- Removes dead code or simplifies logic without changing intended behavior.
- Documents a real constraint that is still true.
- Aligns code with an established project pattern and does not add workaround layers.
- Is part of the newly confirmed root-cause fix.

## Remove Or Revise Criteria

Remove or revise a previous change when it:

- Was a temporary trial that the user says did not work.
- Compensates for behavior now known not to be the root cause.
- Shows a workaround signature from `/layering` that is no longer justified.
- Makes the code harder to understand without a confirmed benefit.
- Encodes misleading comments, assumptions, logs, or temporary markers from a failed hypothesis.
- Conflicts with the better root-cause fix.

## Manual Cleanup Rule

Do not use `git restore`, `git checkout`, `git reset`, or similar commands to undo prior changes. Do not use scripts or broad mechanical rewrites to revert them.

Clean up by manually editing the affected files with `apply_patch`, using the previous content, current surrounding code, and new evidence as guidance. The goal is to preserve useful work while removing failed or stale issue-specific edits.

## Output

When reporting the result, include:

- What new information triggered the review.
- Which changes were kept and why.
- Which changes were removed or revised and why.
- Any unclear changes that need user judgment.
- Checks run, or why checks were not run.
