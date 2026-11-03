---
name: fix-lints
description: Use when lint, formatting, type-check, build, test, or CI failures need fixing.
---

# Fix Lints

## Objective

Fix every relevant lint, warning, build, test, formatting, type-check, and validation failure until the applicable check suite is clean.

Prioritize durable root-cause fixes over cosmetic or suppressive changes.

## Workflow

1. Discover the repository's intended checks the way `/checks` does, following its check selection and default exclusions.
2. Run the narrowest relevant failing check first when a failure is already known. Otherwise, run the standard local validation suite for the changed area or repository.
3. Read failures carefully and identify the underlying cause before editing.
4. Fix the production code, tests, types, config, or documentation at the correct ownership boundary.
5. Re-run the failing check after each meaningful fix.
6. Continue until all applicable checks are clean or a genuine external blocker prevents completion.
7. Report what was fixed and which checks passed. If blocked, report the exact blocker and the last command/output summary.

## Fix Quality Bar

- Do not add blanket `allow`, `ignore`, `skip`, `noqa`, `eslint-disable`, `#[allow(...)]`, `#[expect(...)]`, `@ts-ignore`, `any`, relaxed compiler settings, weakened test assertions, or similar suppressions just to make checks pass.
- Use suppressions only when the warning is intentionally unavoidable, locally scoped, and justified by code structure or project policy.
- Do not remove tests, downgrade dependencies, hide failing paths, or change public behavior merely to satisfy a tool.
- Do not introduce temporary compatibility shims or broad refactors unless the failure truly requires them.
- Prefer small, typed, idiomatic fixes that preserve the existing design and improve maintainability.
- Treat new warnings as failures when the user asks for clean checks, even if the tool exits successfully.

## Validation

Run enough checks to prove the fix:

- The originally failing command must pass.
- Closely related checks must pass when the fix touches shared code, public APIs, build configuration, or tests.
- Repository-wide checks should run when the failure source is broad or uncertain.

If a check cannot be run because of sandboxing, missing dependencies, network access, or external services, request the needed approval when appropriate or clearly state the limitation.
