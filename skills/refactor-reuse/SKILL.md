---
name: refactor-reuse
description: Use before writing a new function, helper, class, component, or similar code, to find existing code to reuse or extend.
---

# Refactor Reuse

Apply this skill to whatever the surrounding prompt asks Codex to create. Before writing new code, spend a bounded effort checking whether something close enough already exists, and prefer reusing or extending it over adding a near-duplicate.

This skill owns the two judgments the whole refactor family depends on: how to look for existing code, and how to decide whether two pieces of code are the same thing. `/refactor-dedupe` and `/refactor-consolidate` defer to the sections below instead of restating them.

## Workflow

1. Identify the concrete unit the prompt asks for: a component, function, hook, utility, type, module, config block, script, or similar. Note its purpose, inputs/outputs, and the area of the codebase it belongs to.
2. Look for candidates using the search technique below.
3. Judge each candidate against the match rules below.
4. If a genuine match or near-match exists, use or extend it and skip creating a new instance. State which existing piece is reused and what changed if it was extended.
5. If nothing similar enough exists, build the new component/function/utility as the prompt originally requested. Do not force a bad fit just to avoid adding new code.

## Search Technique

- Start where the new unit belongs — sibling files, the module's own helpers — then widen only as needed.
- Widen to shared, common, lib, utils, and ui locations; design-system or component packages; the project's own internal packages; dependencies already in the manifest; and the language's standard library.
- Search by behavior and shape, not just the literal name from the prompt. Use synonyms, the underlying operation, the parameter or prop shape, and the return type. A copy is usually renamed, so identifiers are the weakest signal.
- Follow the call sites of near-misses. The canonical helper is often one hop away from code that already does the same job.
- Keep the effort bounded. Search the parts of the codebase actually relevant to the unit, not everything, and stop once a reasonable sweep comes up empty.

## Match Rules

Reuse or extend when the existing code:

- Solves the same problem or renders the same kind of thing, even if named differently.
- Differs from the need only by a parameter, prop, option, or minor variation that can be added without breaking existing callers.
- Is a generic helper/utility that the new need is a specific case of.

Treat as no match when:

- The existing code is similar in name only, or serves a different domain concept.
- Reusing it would require invasive changes to existing callers or unrelated behavior changes.
- Extending it would need many new conditional branches or flags to serve unrelated cases, making a wrapper or parameter list worse than a small new unit. `/refactor-consolidate` owns the fuller guardrails against over-abstraction.

## Boundaries

- Do not skip building the requested thing while endlessly searching for a maybe-reusable match; if a bounded search finds nothing suitable, proceed to create it.
- Do not force-fit unrelated code together just to avoid a new file or function; a bad abstraction is worse than a small duplicate.
- When extending existing code, preserve its existing behavior and callers; do not change its contract in a way that breaks other usages.

## Output

- Before writing new code, briefly state whether an existing match was found.
- If reused or extended: name the file/symbol reused and, if extended, what was added and why it stays backward-compatible.
- If nothing suitable existed: say so briefly, then proceed to build what the prompt asked for.

## Related Skills

- `/refactor-dedupe`: this skill applies before new code is written; use dedupe to clean up bespoke copies that already exist.
- `/refactor-consolidate`: use it when several repeated instances exist and none of them is a canonical owner yet.
