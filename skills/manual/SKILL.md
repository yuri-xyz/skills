---
name: manual
description: Use when the user asks for manual, targeted edits without scripts, codemods, or broad rewrites.
---

# Manual Edit Mode

Use this skill when the user wants the work done through deliberate, targeted edits instead of custom automation.

## Core Rule

Make the change with the normal agent editing flow:

- Read the relevant files and nearby context.
- Reason about the smallest correct edit.
- Use `apply_patch` for manual file changes.
- Keep changes tightly scoped to the requested behavior.

## Avoid

Do not create or run custom scripts, codemods, one-off Python/Ruby/Perl/sed rewrites, broad search-and-replace commands, generators, or migration-style transformations to perform the edit.

Also avoid:

- Large mechanical rewrites when a few targeted patches would do.
- Formatting unrelated files or entire trees just because it is convenient.
- Introducing helper automation that will not remain part of the requested solution.
- Rewriting structure just to make a manual edit easier.

## Allowed

This skill does not prohibit ordinary engineering tools used around the edit:

- Use `rg`, `sed -n`, `nl`, `git diff`, and similar read-only commands for inspection.
- Run focused tests, type checks, parse checks, or project validation after editing.
- Run a standard formatter only when it is already the repo's expected validation path and the scope is limited to touched files or clearly necessary files.

## If Manual Editing Becomes Impractical

If the requested change truly requires many repetitive edits, stop and say why a manual approach is likely to be error-prone. Ask for explicit confirmation before switching to automation.

Do not silently escalate from manual edits to scripts or broad replacements.
