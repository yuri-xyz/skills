---
name: document
description: Use when recent changes need documenting, such as comments explaining why non-obvious code exists, or updates to the README, docs, specification, agent instructions, or other documentation the changes made stale.
---

# Document

Use this skill after implementation work to bring the documentation in line
with what changed: inline comments where the code needs its reasons, and the
project's documentation files where they no longer match.

## Goal

Leave the project documented as it now is. Future maintainers, users, and
agents should find the context they need in the place they would look for it:
the reason behind a surprising line next to that line, and changed behavior,
commands, options, or contracts in the docs that describe them.

Document what the changes affect, and only that. Do not rewrite documentation
that is still accurate, and do not comment every changed line.

## Workflow

1. Inspect the pending git diff, or the recent commits when the work is
   already committed, and list what changed in behavior, interfaces, commands,
   configuration, layout, and constraints.
2. Find the documentation those changes touch. Look at:
   - inline comments and doc comments in and near the changed code;
   - the README and any `docs/` directory, guides, or examples;
   - agent instruction files, such as `AGENTS.md` or `CLAUDE.md`;
   - a `.spec/` specification, if the project has one;
   - changelogs, help text, man pages, and API descriptions the project keeps
     by hand.

   Search them for the names, commands, paths, and options the diff changed,
   so stale mentions are not missed.
3. Read enough surrounding code and tests to understand the actual reason for
   each change before writing about it.
4. Update each affected place, following the standards below and the file's
   own conventions. Hand specification updates to `/spec-sync`, README changes
   to `/readme`'s rules, and `AGENTS.md` changes to `/agents-md-init`'s rules.
5. Re-read the diff of your edits and remove anything redundant, speculative,
   stale-sounding, or tied to the debugging process.
6. Run formatting and focused checks when the edits touch source files or
   documentation that has a linter or build step.

## Comment Standards

- Add comments only where the context is not obvious from names, types, or
  local structure. Prefer a few durable comments at ownership boundaries,
  tricky conditionals, validators, migrations, escaping logic, concurrency
  behavior, generated-output logic, public API tradeoffs, or code that looks
  surprising without the recent investigation.
- Explain `why` rather than restating `what`, and keep each comment close to
  the invariant or decision it protects.
- Mention the underlying problem, previous behavior, or constraint only when
  it helps prevent a future regression.
- Avoid blame, chronology, and vague phrases like "bug fix", "temporary", "for
  now", or "new behavior".
- Do not narrate assignments, branches, imports, or function calls.
- Do not add documentation comments to public APIs unless the public contract
  itself changed or was previously unclear.
- Keep comments short. If a comment needs a paragraph, consider whether the
  code should be clearer instead.

## Documentation Standards

- Describe the current state, not the history of how it got there. Changelogs
  are the exception and follow their own format.
- Change the smallest part that makes the document true again: a command, an
  option, a paragraph. Keep the document's structure, tone, and formatting.
- Update every mention of a renamed or removed command, option, path, or
  concept, including examples and code blocks.
- Run or check any command or example you add or change.
- Add new documentation only where readers will look for it, such as a new
  option in the section that lists options; do not start new documents unless
  the project has no place for the information.

## Shared Rules

- Do not preserve private investigation notes, command output, issue
  speculation, or conversation details.
- Leave generated files, vendored code, lockfiles, snapshots, and unrelated
  files alone.

## Completion Criteria

Before finishing, report:

- which files received comments, and which documentation files were updated;
- documentation reviewed where nothing needed changing;
- the validation commands run, or why validation was not run.
