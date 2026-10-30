---
name: debug-cleanup
description: Use when debugging is done and temporary logging, probes, or failed workarounds need removing without losing durable fixes.
---

# Debug Cleanup

## Objective

Clean up temporary investigation artifacts without erasing useful work. Remove debug logging and obvious failed attempts that were added during the current debugging effort, but keep real improvements and leave unrelated changes alone.

This skill is especially for the end of a debugging session where temporary logs, markers, experiments, or workaround logic may still be in the worktree.

## Workflow

1. Check `git status --short` to understand the pending worktree.
2. Inspect relevant diffs before editing. Identify which changes were part of the recent debugging/investigation and which are unrelated.
3. Search for temporary debug logging and markers added during the investigation, such as `DEBUG_`, `INVESTIGATE`, `TRACE`, `dbg!`, `println!`, `console.log`, `eprintln!`, temporary log file paths, and marker strings mentioned in the conversation.
4. Remove temporary debug logs, debug-only file writes, scratch log files, grep markers, and instrumentation scaffolding that is no longer needed.
5. Review attempted fixes or workaround logic added during the investigation, and classify each with `/keep-or-revert`'s criteria, which own the keep-or-remove judgment.
6. Keep the changes it rates Keep, such as the final root-cause fix, regression tests, and improvements valuable on their own.
7. Remove or revise the ones it rates Remove or Revise, and raise its Ask cases with the user.
8. Leave unrelated changes alone. If a file contains unrelated user work, edit only the cleanup-relevant lines and do not revert the file wholesale.
9. Run focused checks when code changed, especially tests that covered the final fix or affected behavior.
10. Report what was removed, what was intentionally kept, what was left untouched as unrelated, and which checks ran.

## Decision Rules

Remove:

- Temporary debug statements and log markers.
- Temporary log files, scratch files, or generated investigation output.
- Instrumentation helpers or config added only to produce debug evidence.

Attempted fixes and workarounds: decide with `/keep-or-revert`, as in steps 5–7.

Leave untouched:

- Changes unrelated to the recent debugging effort.
- User work in dirty files that you did not make.
- Other feature work, formatting, config edits, or generated changes unless they are clearly part of the temporary investigation artifacts.

## Scope

The attempted-fix cleanup rules apply only when the recent work involved debugging or trying multiple approaches. If the only temporary work was debug logging, just remove the debug logging and related files.

Do not run broad destructive commands or reset files. Prefer surgical edits based on the diff and conversation context.

## Final Response

Summarize:

- Removed: temporary logs, markers, files, or failed attempts.
- Kept: improvements or final fixes and why they are worth keeping.
- Untouched: unrelated changes deliberately left alone.
- Verification: checks run, or why checks were not run.
