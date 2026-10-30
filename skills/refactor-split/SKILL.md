---
name: refactor-split
description: Use when a file or module is monolithic or exceeds a requested line limit, such as 700 lines, and needs splitting into idiomatic modules.
---

# Split

Use this skill to break monolithic code into organized, idiomatic modules without changing behavior unless the user explicitly asks for behavior changes.

## Goal

Turn large files or tightly-coupled projects into smaller source files with clear ownership. Every applicable source file in the requested scope should end at 700 lines or fewer. If any applicable source file remains above 700 lines, continue splitting it until it is at or below the limit.

Applicable source files are handwritten project files. Exclude generated output, dependency directories, vendored code, lockfiles, snapshots, build artifacts, minified bundles, binary assets, and files outside the user-specified scope.

## Workflow

1. Identify the requested scope and list oversized applicable source files with line counts.
2. Read surrounding project structure and naming conventions before choosing module boundaries.
3. Split by cohesive responsibility: domain concepts, parser/emitter layers, UI components, commands, adapters, tests, or helpers that already exist in the codebase.
4. Move code without broad rewrites first. Preserve public behavior, exports, feature flags, comments that explain non-obvious decisions, and test coverage.
5. Keep imports, module declarations, re-exports, and visibility narrow. Prefer existing module style over new architecture.
6. After each meaningful split, run focused formatting/checks and re-count applicable source files in scope.
7. Repeat until no applicable source file in scope exceeds 700 lines.

## Splitting Rules

- Do not create dumping-ground modules such as `utils`, `misc`, or `common` unless the codebase already uses that pattern and the contents are genuinely shared.
- Do not split mechanically by line number alone. Use the 700 line limit as a constraint, not as the design principle.
- Prefer a few cohesive modules over many tiny files that make reading harder.
- Keep tests near the behavior they verify when that is the local convention.
- Move shared types only when multiple modules need them. Otherwise keep types with their owning behavior.
- Avoid compatibility wrappers or duplicate paths just to make the split compile; update call sites to the new ownership boundary.
- Preserve deterministic output and escaping behavior when moving emitters, command builders, templates, shell snippets, or generated-code helpers.

## Completion Criteria

Before finishing, report:

- The files or project scope that was split.
- The final line-count check for applicable source files in scope.
- The validation commands run, or why validation could not be run.
