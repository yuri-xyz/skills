---
name: refactor-dedupe
description: Use when code may re-implement something the project already has, such as a generic component, helper, or type.
---

# Refactor Dedupe

Use this skill to find places where hand-rolled, one-off code stands in for something the project already provides, and to replace the copy with the real thing.

This is the retroactive counterpart to `/refactor-reuse`. The duplicate already exists — usually because whoever wrote it (often an agent) did not know the generic was there, or copy-pasted a sibling file and tweaked it. The fix is to delete the custom instance and route its callers to the canonical implementation, not to invent a new abstraction.

Follow `/refactor-reuse` for how to search for the canonical owner and how to decide whether a candidate is genuinely the same thing. This skill owns what happens after that: the replacement.

## Scope

Work within the scope the user names: a diff, a file, a directory, a feature area, or the changes made in this session. When no scope is given, default to recently changed code, since that is where fresh duplicates live. Keep the search bounded; this is a targeted sweep, not a whole-repository audit.

## Workflow

1. Inventory the candidates in scope: locally defined components, helpers, hooks, wrappers, types, constants, fixtures, config blocks, and script snippets that are not obviously specific to their file.
2. For each candidate, locate the canonical owner and confirm the match, per `/refactor-reuse`.
3. Choose an action per candidate: replace directly, extend the generic first and then replace, or keep with a stated reason.
4. Replace by updating call sites to the canonical implementation and deleting the bespoke copy. Do not leave the old definition behind unused.
5. When the generic is nearly right, extend it backward-compatibly — one added parameter, variant, or option — then replace. If the extension needs several flags or awkward branching, keep the local version and say why.
6. Run the focused checks and tests that cover the changed call sites. For UI, confirm the rendered result still matches.

## Signals To Look For

- A locally defined button, modal, card, table, spinner, or layout wrapper when the project has a component library that exports one.
- Private `formatDate`, `sleep`, `clamp`, `chunk`, `deepMerge`, or `retry` helpers sitting next to an existing utility module or a standard library function that does the same job.
- Re-declared interfaces, structs, or types that mirror a shared model, generated schema type, or API client type.
- A hand-rolled HTTP, retry, logging, or serialization wrapper when a configured project client already exists.
- Literal values redefined locally when a shared constants, theme, or config module already names them.
- Copies of a shared config block, CI job, shell snippet, or Nix helper that drifted slightly from the original.
- A file that is a near-clone of a sibling with small tweaks.
- Test fixtures, builders, and setup helpers reimplemented per test file when a shared fixture exists.

## When Not To Replace

- The bespoke version is deliberate. A comment, a doc, or a test explaining the divergence means it stays until the user says otherwise.
- The generic lives in a layer this code should not depend on, or the import would create a circular or upward dependency.
- Replacing it would change observable behavior in a way the current task does not authorize.
- The generic is deprecated or mid-migration. Do not migrate code toward a dying API; report it instead.
- The code is generated, vendored, or otherwise not hand-maintained.
- The copy exists to work around the generic being broken. That is a root-cause problem, not a duplication problem; use `/layering`.

## Boundaries

- Replace, do not redesign. This skill creates no new abstractions; if no canonical owner exists and the duplication is real, use `/refactor-consolidate`.
- Preserve behavior. If the copy and the generic genuinely differ, that difference is either a bug or a requirement. Report it and ask; do not silently adopt the generic's behavior.
- Do not add a compatibility shim around the generic to make old call sites compile unchanged. Adapt at the call site; a shim is just a new bespoke layer.
- Keep the diff scoped to the replacement and its call sites.

## Report

- Each bespoke instance, the canonical replacement it was routed to, and the call sites updated.
- Candidates deliberately kept, with the reason.
- Code deleted, checks run, and any behavior differences found between copy and generic.
