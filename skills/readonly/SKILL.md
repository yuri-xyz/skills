---
name: readonly
description: Use when the user asks for an audit or investigation that must not run tests or scripts, edit files, stage, or otherwise mutate anything.
---

# Read-Only Audit Mode

Use this skill when the user wants a code audit or investigation without repository changes. The goal is to gather evidence and report findings, not to fix them.

## Hard Rules

- Do not edit, create, delete, move, format, or stage files.
- Do not run `apply_patch`, formatters, generators, migrations, package installers, update commands, or commit commands.
- Do not run test suites, build scripts, dev servers, or project scripts unless the user explicitly permits them for this audit.
- Do not run commands that commonly write caches, lockfiles, build outputs, snapshots, coverage, databases, or generated artifacts.
- Do not mutate external state, service state, system state, git state, dependency state, or runtime config.

## Allowed Exploration

Prefer commands that only read files or inspect Git metadata:

```sh
git status --short
git diff --stat
git diff -- path/to/file
git show --stat
git log --oneline -- path/to/file
rg "pattern" path
rg --files path
sed -n '1,160p' path/to/file
nl -ba path/to/file
find path -maxdepth 2 -type f
```

Use `rg` before slower search tools. Parallelize independent reads when practical.

## Risky Commands

Avoid these unless the user gives explicit permission:

- `cargo test`, `npm test`, `bun test`, `pytest`, `nix flake check`, `nix build`, `make`, and similar validation commands.
- Any command with `--fix`, `--write`, `--update`, `--upgrade`, `--install`, `--generate`, `--watch`, `--serve`, or `--commit`.
- Commands with shell redirection that writes files, such as `>`, `>>`, `tee`, or heredocs.
- Cleanup commands such as `rm`, `git clean`, `git reset`, `git checkout`, or `git restore`.

If a command may be read-only but could write caches or derived files, either skip it or ask first.

## Audit Method

- Start by checking `git status --short` so existing user changes are visible.
- Read the relevant code, tests, docs, and call sites.
- Separate confirmed issues from suspicions.
- Prefer precise file and line references.
- Explain the impact and likely trigger for each finding.
- Suggest fixes conceptually, but do not implement them.

## Reporting

Lead with findings, ordered by severity. If there are no issues, say that clearly and mention the limits of the read-only audit.

For each issue, include:

- File and line reference.
- What is wrong.
- Why it matters.
- The shape of the fix, without editing code.

End with any checks you intentionally did not run because this was read-only.
