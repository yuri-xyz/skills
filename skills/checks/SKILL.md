---
name: checks
description: Use when changes need validating or the user asks which repository checks pass or fail, including for a completion report.
---

# Checks

Run the repo's normal verification commands, avoid opt-in suites by default, and return a compact pass/fail summary with emoji status markers.

## When To Use

Use this skill when the user asks to:

- run checks
- validate the repo
- make sure a change passes
- run lint, tests, build, typecheck, or similar verification
- summarize current repo health

## Workflow

1. Identify the repo root and inspect the available scripts and config before running anything.
2. Check whether the current conversation already established results for the same unchanged repo state.
3. If the same checks already ran and nothing has changed since then, do not rerun them unless the user explicitly asked to rerun them. Tell the user the checks already ran for the current repo state and show the prior summary again.
4. Otherwise, discover and run the applicable checks.
5. Report the results with one line per check using `🟢` for pass, `🔴` for fail, and `⚪` for skipped or not applicable.

## Check Selection

Prefer the project's canonical commands in this order:

1. CI-oriented local validation scripts such as `check`, `validate`, `verify`, `lint`, `typecheck`, `test`, `build`.
2. Package-manager scripts from `package.json`, `Cargo.toml`, `Makefile`, `justfile`, and similar repo-native task runners.
3. Tool-native commands only when the repo clearly uses them and there is no better project wrapper.

Run only checks that are applicable to the current repo. Do not invent extra work.

## Default Exclusions

Do not run these unless the user explicitly asks:

- E2E or browser suites
- live, networked, or external-service tests
- performance or load tests
- destructive migration or deployment validations
- commands clearly marked optional, manual, integration-only, smoke, or slow

If a test command mixes unit tests with excluded suites, prefer a narrower command when one exists.

## Fast Mode

When `/fast-mode` is active, it overrides this skill's check selection: skip every heavy check, such as broad or workspace-level test suites, builds, lints, type checks, flake checks, and anything likely to take longer than about three minutes. Run only lightweight, quick checks, such as single-file parses or formatting checks, within fast mode's 3-minute time box. Report each skipped heavy check as `⚪ <Check>: deferred (fast mode)`. Only an explicit user message asking for the heavy checks lifts this.

## Practical Rules

- Prefer targeted verification for the current change when the user asked for that specifically.
- Prefer the lightest command that faithfully covers a category.
- Avoid rerunning expensive commands after a failure unless needed for confirmation.
- If a command fails because dependencies are missing or the environment is blocked, report that clearly instead of masking it as a test failure.
- If the repo instructions define a preferred order, follow that order.

## Output Format

Return a short summary with one line per check, for example:

- `🟢 Lint: passed`
- `🔴 Test: failed in packages/compiler`
- `⚪ E2E: skipped by default`

After the list, include a short note if results were reused from cache instead of rerun.

## Notes

- Treat "nothing changed" as a repo-state judgment based on the visible git state in the current session.
- If the user explicitly says "run again", "rerun", or equivalent, rerun the checks even if the prior result still appears current.
