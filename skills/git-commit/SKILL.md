---
name: git-commit
description: Use when the user asks to commit pending work.
---

# Git Commit

Turn the current pending worktree into one clean commit in the repository's own message style. Gather just enough context to describe the change honestly, exclude generated junk, and commit.

## When To Use

Use this skill when the user asks to:

- commit the current work
- prepare a commit
- write a commit message
- inspect the pending git changes before committing
- make sure the commit only contains the right files

## Core Constraints

Two rules govern everything below.

**Read enough, not everything.** The goal is an accurate commit message, not an understanding of the codebase. Stop reading the moment the message can be written truthfully in the chosen style.

**Commit the work; do not change it.** The worktree is the input, not the subject of improvement. Arrive at `git commit` with the same code that was there when the skill started, aside from the narrow exceptions listed below.

## Workflow

1. Get the shape of the work: `git status --short` and `git diff --stat` (including staged changes).
2. Scan the path list for generated artifacts, local outputs, dependencies, caches, and binaries that should not be committed.
3. If such files are present, update `.gitignore` and drop them from the commit scope. Keep lockfiles and other artifacts the repo intentionally tracks.
4. Read the diffs only to the depth needed to name the intent of each meaningful change. See Reading Budget.
5. Treat all remaining applicable pending files as the default commit scope.
6. Before writing the commit message or staging, apply the Spec Sync Gate below.
7. Choose the message style per Commit Message Style, then write the message, including any spec changes made by the gate.
8. Stage and commit everything in scope: `git add -A` (or scoped to specific paths when files were deliberately excluded), then `git commit`.
9. Report the commit, the scope, anything deliberately excluded, and anything noticed but left alone.

## Spec Sync Gate

Before every commit, use `/spec-sync` if and only if both conditions hold:

- the project has a governing `.spec/` folder; in a monorepo, the changed package must have its own `.spec/`, or the repository must use a top-level `.spec/` entry point
- the current pending work has not already been synced to that spec

Use the conversation and the current spec/diff to determine whether this work
has already been synced. If either condition is false, do not invoke
`/spec-sync`. Do not create a `.spec/` folder; that requires an explicit
`/spec-init` request. Let `/spec-sync` decide whether the unsynced change is
spec-affecting, and finish it before continuing to the commit message and
staging steps.

## Reading Budget

Read diffs the way a reviewer skims a changelog, not the way an auditor reads a codebase.

Do:

- Start from `--stat` to see where the weight of the change is.
- Read full hunks for the files that carry the intent of the change.
- Skim or skip mechanical churn: renames, formatting, lockfile regeneration, generated output, repeated boilerplate edits. One representative hunk is enough to name the pattern.
- Use the conversation as context when the change was just made in this session. Work already discussed does not need rediscovering from the diff.
- Stop as soon as the message can be written accurately.

Do not:

- Open files beyond the diff to understand surrounding code.
- Trace callers, dependencies, or tests that the diff does not touch.
- Reconstruct why code that was not changed works the way it does.
- Build a full architectural picture of the affected subsystem.
- Verify that the change is correct, complete, or well designed.
- Run builds, tests, linters, formatters, or type checks.

If the diff is large or unfamiliar, prefer a slightly more general bullet over another round of reading. A commit message that says "reworks the request retry path" without naming every call site is fine. An accurate summary at the right altitude beats an exhaustive one.

## No-Change Rule

While committing, do not:

- Fix bugs, typos, naming, or style problems noticed in the diff.
- Add or update tests, comments, or documentation.
- Run formatters, linters, or codemods, or apply their fixes.
- Refactor, simplify, or consolidate anything.
- Revert, amend, or discard parts of the pending work.
- Stage changes the user asked to leave out.

Three exceptions are part of committing itself:

- `.gitignore` updates needed to keep generated artifacts out of the commit scope.
- `.agenda` status updates, per the Agenda Tracking section below.
- The narrowly scoped spec updates produced by the required `/spec-sync` gate.

Anything else noticed while reading the diff belongs in the final response as an observation, not in the commit. Suggest it; let the user decide whether it becomes its own task.

## Version Control Tool

Use plain git throughout via `git status`, `git diff`, `git add`, and `git commit`. Do not use history-editing commands (`rebase`, `commit --amend`, `reset`, etc.) as part of this skill; committing pending work is the only operation in scope.

## Artifact Scan

Treat these as suspicious by default and verify them before committing:

- `node_modules/`
- `dist/`
- `build/`
- `.next/`
- `.turbo/`
- `.cache/`
- `coverage/`
- generated bundles
- compiled binaries and other `*.bin`, `*.exe`, `*.dll`, `*.so`, `*.dylib`, `*.o`, `*.a`, `*.class`
- editor junk, temp files, logs, and local machine artifacts

Do not remove files from the commit just because they are large or uncommon. Keep files that are intentionally tracked by the repo, such as:

- lockfiles like `bun.lock`
- checked-in snapshots if the repo uses them
- generated files that the repo intentionally versions

When in doubt, use the repo's existing patterns as the source of truth. If a file is already tracked and should remain tracked, do not try to hide it with `.gitignore`.

## Commit Scope

- By default, include all applicable pending files from `git status` after excluding junk and intentionally omitted paths.
- Prefer committing the full applicable pending worktree, not just the most recent subset.
- If `.gitignore` changed as part of cleaning the scope, include it in the commit.
- Exclude only files that clearly should not be committed, or files the user explicitly asked to leave out.
- If the worktree contains multiple clearly separate changesets, split them only when the user asks or when combining them would make the commit misleading.
- If the right scope is ambiguous, ask only when the ambiguity risks combining unrelated work into a misleading commit.
- Do not rewrite or squash prior commits unless the user explicitly asks.

## Agenda Tracking

When the repo has a local `.agenda` workspace and the landing work clearly changes the status of a tracked item, update the relevant `.agenda` task, plan, roadmap, or note before committing and include the resulting `.agenda` changes in the commit:

- mark a task, plan item, or roadmap item completed or advanced when this work did that
- register a blocker or follow-up discovered during the work

Keep this to a status or note update on items the commit actually affects. Do not audit the whole `.agenda` tree, restructure trackers, or open new work while committing.

## Commit Message Style

Pick the first source that applies and follow it for the subject and body:

1. **Documented or stated convention.** The user's instructions, or a commit guide the repository documents, such as a section in `CONTRIBUTING.md`, `AGENTS.md`, or `README.md`, a commitlint or commitizen config, or a `.gitmessage` template. Follow it as written, and fill anything it leaves open from the recent history or the default format.
2. **Recent history.** Otherwise read the last 5 non-merge commits with `git log -5 --no-merges --format='%B%n---'` and learn their structure: subject prefix or type scheme (Conventional Commits, Gitmoji, ticket IDs, plain imperative), scopes, capitalization, tense, subject length, and whether bodies are absent, prose, or bullets, and how long. Use that structure when most of these commits share it. Treat bot, release, and revert commits as noise.
3. **Default format.** When the repository has no commits, or the recent commits share no clear structure, use the Default Format below.

Match the structure, not the content: a history of terse subjects with no body still gets an accurate subject for this change. Whatever the style, describe what the diff does and do not claim verification that was not performed.

## Default Format

Write the subject as a plain Conventional Commit subject. Do not use emoji
or Gitmoji anywhere in the subject or body:

```text
feat: add OAuth login
fix(api): handle expired tokens
docs: document configuration
```

Use one of the standard Conventional Commit types:

- `feat: ...`
- `fix: ...`
- `refactor: ...`
- `perf: ...`
- `docs: ...`
- `test: ...`
- `build: ...`
- `ci: ...`
- `chore: ...`

Choose the type that best matches the actual diff, not the user's wording.

The commit body must contain 3 to 6 detailed bullet points. Each bullet should, when possible, capture:

- the intention or goal
- what was changed
- why the change was needed or what it improves

Aim for substantive bullets, not terse fragments.

Write body bullets as consecutive lines with no blank line between bullet items. Keep only the normal blank line between the subject and the first body bullet.

For example:

```text
feat: restore legacy stream output

- restore plain stream output to the legacy ANSI delimiter format so existing embedders keep working without command changes
- keep framed ANSI and cell protocols available behind explicit stream-format values for new length-prefixed integrations
- update parsing tests, rendered-frame coverage, and user docs to lock in both compatibility and opt-in framed behavior
```

Keep the bullets concrete, tied to the diff, and informative enough that someone scanning git history can understand both the change and its purpose.

## Shell Quoting

- When running `git commit` from a shell command, do not place backticks directly inside double-quoted `-m` arguments because the shell will treat them as command substitution. Use single-quoted `-m` arguments when possible, or escape backticks, dollar signs, and other shell-sensitive characters explicitly.
- Prefer `git commit -F <file>` for multi-line commit bodies or any message containing shell-sensitive characters.
