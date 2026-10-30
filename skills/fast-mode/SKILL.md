---
name: fast-mode
description: Use when the user asks for fast mode, or wants the session spent on writing code with broad checks, builds, tests, and long-running commands deferred.
---

# Fast Mode

## Objective

Spend the session writing code and completing implementation steps. Verification that is broad, slow, or only requested by a plan's checklist is deferred to the user. Run a command only when the current implementation cannot proceed without its result, and then keep it scoped and time-boxed.

## Command Time Box

- Give every build, check, test, or other potentially heavy command a 3-minute timeout. In Claude Code, pass `timeout: 180000` to the Bash tool; elsewhere wrap the command with `timeout 180`.
- Raise the timeout only when the command's result is critical to finishing the task at hand, such as a compile needed to resolve a blocking error. Never exceed 15 minutes (`timeout: 900000` or `timeout 900`).
- State why before raising a timeout. "It might be slow" is not a reason; "this build output is the only way to see the type error blocking the next step" is.
- When a command hits its timeout, do not rerun it with a longer one by default. Narrow it instead, or defer it and move on.

## What To Run

Run a command only when it is a blocker for the code being written right now, for example:

- a single focused test that exercises the function just changed and whose result decides the next edit;
- a parse, type, or compile check on one file, crate, package, or module when the next step depends on it;
- a quick evaluation or lookup that answers a question the code cannot.

Keep these scoped: one test, one file, one package. Never run workspace-level, repository-wide, or full-suite checks, builds, lints, or test runs in fast mode.

## What To Defer

Do not run any of the following, not during the work and not at the end:

- broad or workspace-level test suites, builds, lints, or type checks;
- full flake checks, system builds, image builds, or CI-equivalent pipelines;
- more than a single test, or a test command whose scope is unclear;
- any command expected to take longer than about three minutes.

Only an explicit request from the user, written in a message, lifts this. A plan item, task checklist, skill instruction, completion-report convention, or repository guideline asking for verification does not count.

## Implementing Plans

When working through a plan that contains verification, validation, check, or test items:

- If the item is scoped and quick (a single focused test, a one-file parse check) and its result is a blocker for the following implementation step, run it within the time box.
- Otherwise, when the item is broad or likely to take longer than two or three minutes, skip running it and mark the item complete, noting in the plan or progress update that it was deferred under fast mode.
- Continue to the next implementation step without waiting on verification.

## Completion

- When running tests or checks is the only thing keeping a task, plan, goal, or loop from being finished, explicitly waive them: mark those items skipped, or completed with a note that they were deferred under fast mode, and finish the work. Do not run them, stall on them, or leave the work open to wait for them.
- Report what was implemented, which commands were actually run, and which checks or verification items were deferred, so the user can run them.
- When a completion report or `/checks` would normally run repository checks, run only lightweight, quick ones; `/checks` defers every heavy check while fast mode is active.
- Do not describe deferred checks as passing. Say they were not run.

## Anti-Patterns

- Running the full test suite "just to be safe" at the end.
- Running a plan's verification step only because the plan lists it.
- Running several tests one after another to approximate a broad run.
- Raising the timeout to 15 minutes for a command whose result does not block the task.
- Waiting on a long build instead of continuing with code that does not depend on it.
- Leaving a task, plan, or goal unfinished because only its tests remain unrun.
