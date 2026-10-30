---
name: spec-sync
description: Use after substantial, directional, or contract-changing work has left parts of a project's `.spec/` specification stale.
---

# Spec Sync

Bring `.spec/` back in line with reality after work that changed what the
project is, what it does, or how it is supposed to behave.

## When This Runs

On explicit request, and automatically whenever both hold:

- the changed scope has a `.spec/` entry point — for a monorepo, that means the
  specific package(s) touched by the change, per the standard's file-layout
  rule (a package's own `.spec/`, or the repository's top-level `.spec/` when
  this repo uses the monolithic monorepo layout), and
- the current session landed a significant change: a new or removed feature,
  changed feature behavior or edge cases, a direction or scope change, a changed
  contract, invariant, or failure mode, or a resolved open question.

Do not run for pure refactors, formatting, dependency bumps, or bug fixes that
restore behavior the spec already describes. A bug fix that reveals an unstated
rule does qualify: add the rule and the reason it exists.

If the changed scope has no `.spec/`, do nothing there. Creating one is
`/spec-init`, on explicit request only. In a monorepo, treat each package
independently: a package without a `.spec/` gets no sync, even when a sibling
package has one or a monolithic top-level `.spec/` exists for the repo overall.

## Procedure

1. **Locate the governing spec(s).** For each changed path, find the nearest
   `.spec/` entry point: that package's own `.spec/` if it has one, otherwise
   the repository's top-level `.spec/` if this repo uses the monolithic
   monorepo layout. If the change spans several packages that each own a
   `.spec/`, treat this as several independent syncs, one per package — never
   merge their content into one file.

2. **Load the standard.** Load `/spec` and follow it for every spec touched.

3. **Gather the change surface**, scoped to that spec's package (the whole repo
   for a monolithic monorepo spec).
   - Changes made in this session within that scope.
   - `git status` and `git diff` for working-tree and staged work within it.
   - `git log` for commits landed since the spec last reflected reality, when the
     request covers already-committed work.
   - Spec markers in the changed code within it: `§` mentions. They name the
     exact entries to check, and are the cheapest way to find what a diff
     obligates.

4. **Classify.** For each change, decide whether it is spec-affecting under the
   standard's maintenance rules. Keep the non-affecting list; you will report it.

5. **Locate the owning sections.** Read the whole spec, including feature, API,
   special, and ADR area files, so the update lands in the right place and does
   not contradict another section.

6. **Edit narrowly.**
   - Update existing entries in place; keep their IDs.
   - Add new features or invariants with the next unused IDs. For decisions,
     append a new ADR as described below.
   - Delete removed features and append an ADR explaining the removal. No
     tombstones.
   - Add new edge cases with their reasons, especially when the change came from
     a bug. The reason is the point.
   - Update feature `Status` when implementation state changed.
   - Resolve or remove answered `## Open Questions`, moving the answer into the
     feature or an ADR according to the governing standard.
   - Leave unrelated sections untouched. Do not restructure or rewrite the spec
     while syncing it.
   - Keep the project manifest/context in `OVERVIEW.md`,
     feature contracts under `features/`, API route contracts under `api/` when
     an API service exists, glossary terms in `GLOSSARY.md`, and project-wide
     obligations in `INVARIANTS.md`.
   - Use the feature, API, and ADR templates for new files and
     preserve first-class Markdown links to related files, sections, and IDs;
     write skill references as `/skill-name`. Keep one API route operation per
     Markdown file and make authentication, input validation, rate limiting,
     responses, and edge cases explicit.
   - Check the verification obligations on every entry the
     change touches. A change within a `required` obligation's scope keeps its
     `§VER-<n>` artifacts current; a behavior change updates the
     obligation's `Property` and any design model under `models/`; weakening,
     demoting, waiving, or removing an obligation appends an ADR. Never create
     artifacts for a `planned` obligation unless the user asks.
   - Update the owning entry's `**Testing.**` block when the
     kinds of tests it needs, or their targets, change.
   - Update the owning feature's `**Performance.**` block when a
     stated function/operation bound changes.
   - Append every material decision made by the user or agent to
     the relevant file under `adr/` in the same change. Never edit, reorder,
     renumber, or delete a committed ADR entry; if a decision changes, append a
     new ADR with a `Supersedes` link.

7. **Re-check limits.** If a file now exceeds 700 lines, split it per the
   standard. Never trim or compress content to stay under the limit.

8. **Verify.** Links and `## Spec Map` entries resolve, IDs stay unique and
   stable, no secrets or machine-specific paths, and no section now contradicts
   another. Verify that `OVERVIEW.md` has no feature or decision content
   duplicated from its owned files, every Markdown file is at or under 700 lines,
   ADR files changed only by appending, API exists if and only if an API service
   exists, function/operation-scoped performance blocks are updated when their
   bounds change, and file/section/ID links plus `/skill-name` references are
   valid. If you deleted an entry, grep for its ID and clear the markers that now
   point at nothing.

## Judgment Rules

- The spec describes direction, features, contracts, and behavior. Do not push
  implementation detail into it because the diff touched implementation.
- Never invent intent. If you changed something on someone else's instruction and
  do not know the underlying reason, ask, or record it under
  `## Open Questions` — a wrong recorded reason outlives the code that caused it.
- When the code and the spec disagree and it is unclear which is correct, say so
  explicitly rather than quietly rewriting the spec to match the code.
- Keep the update in the same change as the work that made it necessary.
- A material decision made during implementation implicitly triggers an
  ADR append; do not wait for a separate `/spec-sync` request.

## Report

State which spec(s) you updated (naming the package, for a monorepo with
per-package specs), which files and sections/IDs within each, any ADR appended
for a decision, and the changes you deliberately judged non-spec-affecting.
