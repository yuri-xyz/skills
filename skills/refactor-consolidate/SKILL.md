---
name: refactor-consolidate
description: Use when the same values or logic are duplicated in several places and should become shared code.
---

# Refactor Consolidate

## Overview

Use this skill to union several repeated instances into one shared owner: a constant, helper, table, type, or module that did not exist before. It applies when duplication is real but nothing in the codebase is yet the canonical implementation.

Pick the right family member first:

- Nothing written yet → `/refactor-reuse`.
- A canonical implementation already exists and the code duplicates it → `/refactor-dedupe`.
- Several repeated instances, no canonical owner → this skill.

Follow `/refactor-reuse` for judging whether two pieces of code are genuinely the same thing. This skill owns the decision of what shared owner to create, and the guardrails against creating one that should not exist.

## Workflow

1. Identify the requested scope: code snippet, files, module, package, recent diff, or whole repo area.
2. Read enough surrounding code and tests to understand naming, ownership, existing helpers, and behavior.
3. Find repeated literals, repeated data shapes, similar branches, parallel functions, copy-pasted tests, and repeated command or option construction.
4. For each repetition, decide whether it is semantic duplication or accidental similarity, then whether a shared owner makes future maintenance simpler.
5. Consolidate only the surviving candidates, choosing the lightest option below.
6. Preserve behavior and public interfaces unless the user explicitly asks for an API change.
7. Run focused checks that cover the changed area, then broader checks when shared behavior or public contracts changed.
8. Review the diff for accidental feature changes, over-abstraction, and unclear indirection before finishing.

## Good Candidates

Consolidate when the code shows:

- Literal values repeated in multiple places with the same semantic meaning, such as option names, paths, command names, status strings, timeouts, limits, labels, or protocol values.
- Functions that differ only by a small parameter, type, command, option set, field name, or error context.
- Repeated validation, normalization, parsing, rendering, filtering, sorting, traversal, command-building, or test setup logic.
- Repeated ad hoc object construction that would be clearer as a named builder, constructor, fixture, table, or typed data model.
- Branches or match arms that can be represented as data plus one shared operation.
- Tests that repeat setup or assertions in a way that obscures the behavior being tested.

## Consolidation Options

Prefer the lightest abstraction that clearly owns the shared behavior:

- A named constant for repeated literal values with one stable meaning.
- A small helper function for repeated operations with the same behavior.
- A parameterized function when two or more functions have the same algorithm and differ by inputs.
- A data table or enum when repeated branches are better expressed as cases.
- A builder or constructor when repeated setup must preserve invariants.
- A trait, interface, or generic abstraction only when multiple concrete types genuinely share a contract and the local language or codebase style supports it.
- A module boundary when consolidation clarifies ownership and avoids making unrelated code depend on each other.

If the result would be a large new shared module, keep its file within the project's size conventions with `/refactor-split`.

## Avoid

These guardrails are the family's shared limit on abstraction; the other refactor skills defer to them.

Do not consolidate when:

- The repeated code is short, local, and easier to read inline.
- The similar code represents different domain concepts that may evolve independently.
- The abstraction needs awkward names, many boolean parameters, callback plumbing, or type gymnastics to work.
- The change would make callers understand a more complex framework to save a few lines.
- The existing duplication is temporary scaffolding around an active migration and the requested task does not include that migration.
- The right fix is deleting dead code or correcting ownership rather than creating an abstraction. When an existing helper already owns the behavior and the duplicate bypasses it, that is `/refactor-dedupe`, not a new abstraction.

## Review Standard

For each meaningful candidate, ask:

- Does the repeated code have one shared semantic meaning?
- Does the abstraction reduce the number of places future changes must touch?
- Does the new name make the domain clearer?
- Can tests still describe behavior directly?
- Would a future maintainer choose this structure after seeing the full surrounding code?

If the answer is no, leave the repetition or use a smaller consolidation.

## Output

When editing code:

- State the consolidation target before non-trivial edits.
- Keep the diff scoped to the requested area and nearby ownership boundary.
- Prefer deleting duplicated code over wrapping it.
- Add or update focused tests when consolidation touches behavior-sensitive code.
- Report checks run and any remaining risks.

When only auditing or reviewing:

- Lead with the best concrete opportunities, ordered by maintenance payoff.
- Include file and line references.
- Explain the proposed shared owner or abstraction.
- Call out candidates rejected as not worth abstracting when that helps prevent churn.
