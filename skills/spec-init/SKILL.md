---
name: spec-init
description: Explicit invocation only. Use when the user asks to create a project's initial `.spec/` specification.
---

# Spec Init

Create the initial specification for a repository under `.spec/`, written to the
`/spec` standard.

Only run this when explicitly asked. Never create `.spec/` on your own
initiative as a side effect of other work.

## Preflight

1. Find the repository root.
2. Determine whether this is a monorepo: a workspace manifest (`package.json`
   `"workspaces"`, `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`,
   `rush.json`, a Cargo `[workspace]`, `go.work`) or a conventional
   multi-package layout (`packages/*`, `apps/*`, `services/*`) whose members are
   independently versioned or built.
3. Determine the target `.spec/` location before writing anything, per the
   standard's file-layout rule (load `/spec` if the exact rule is needed):
   - Not a monorepo: `.spec/` at the repository root.
   - Monorepo, package named or clearly implied by the request (e.g.
     "spec-init the api service"): `.spec/` at that package's root.
   - Monorepo, user explicitly asked for one shared spec covering the whole
     monorepo: `.spec/` at the repository root, describing the monorepo as a
     whole.
   - Monorepo, scope not stated or inferable: **stop and ask** which package
     this spec is for, or whether they want a single monolithic spec for the
     whole monorepo. Per-package `.spec/` is the default for monorepos, but
     guessing the wrong package wastes a full distillation pass.
4. If the target `.spec/` already contains an `OVERVIEW.md` entry point,
   **stop**. Report the existing path and point at `/spec-sync` for updates.
   Do not create a second spec or a draft alongside it.
   If the directory has a separated layout (`features/`, `adr/`, `api/`,
   `GLOSSARY.md`, or `INVARIANTS.md`) but no `OVERVIEW.md`, report the
   incomplete or malformed spec instead of creating a competing entry point.
5. Otherwise, load `/spec` and follow it. That standard, not this file,
   defines the spec's structure and content rules.
6. Confirm the target `.spec/` is not covered by `.gitignore`; specs are
   tracked in Git.

## Substance Check

A spec distilled from nothing is worse than no spec. Before writing, decide
whether the target scope — the package, or the whole repository for a
single-package repo or an explicit monolithic monorepo spec — actually carries
enough signal.

There is enough to distill when the scope has real source beyond scaffolding
— a working entry point, a public surface such as a CLI, API, module, or UI, and
usually a README or meaningful commit history.

There is not enough when the scope is empty, is an untouched framework
template, or is a single trivial script. In that case **stop and ask the user**
what it is meant to be and where it is heading, then write the spec from their
answer. Do not invent a direction, and do not write a placeholder spec.

## Discovery

Read before writing. Aim for a broad pass over the surfaces that reveal intent,
scoped to the target package's directory for a per-package spec (skim
root-level docs too, only for context on how the package fits into the larger
repo):

- `README*`, `AGENTS.md`, `CLAUDE.md`, `docs/`, and `.agenda/notes/` — stated intent.
- Package manifests, `flake.nix`, build files — project type and dependencies.
- Entry points and top-level module layout — component boundaries.
- Public surface: CLI flags and subcommands, API routes and methods, exported
  interfaces, config schema, on-disk paths, wire formats.
- Tests — the densest source of edge cases and intended behavior.
- Defensive branches, retries, guards, and `// why`-style comments — earned rules.
- `git log` on the areas that changed most — direction, reversals, and bug fixes
  that explain why a rule exists.
- Existing issues, TODO comments, and `.agenda/` tasks or plans — open questions
  and planned work.
- Existing spec links, stable IDs, and `/skill-name` references — traceability
  conventions to preserve.

Use `/explore` when the repository is large enough that a shallow pass would
misrepresent it.

## Distilling

Map what you found onto the standard's structure:

- **Purpose and intent** come from README, docs, and commit history. If the
  stated intent and the code disagree, describe the code and record the tension
  as an open question.
- **Features** come from the public surface, not from the internal call graph.
  One feature per thing a user or caller can do.
- **API routes** come from the API service's path/method operations. Keep their
  request, response, authentication, validation, and rate-limit contracts under
  `api/`, not duplicated in feature files.
- **Edge cases** come from tests, defensive code, and bug-fix commits. When a
  fix commit explains its reason, carry that reason into the spec.
- **Non-goals** come from explicit refusals in docs, removed features in history,
  and boundaries the architecture makes obvious.
- **Invariants and decisions** come from constraints the code enforces
  everywhere, and from choices the history shows were deliberate.
- **Performance bounds** come only from evidence that a cost was intended:
  benchmarks, load tests, comments, incident-driven fixes, or an explicit budget
  in docs. Put them in a compact `**Performance.**` block on the owning feature,
  with one bullet per relevant function or operation. Do not derive a bound by
  reading an algorithm — writing down what the code currently happens to do turns
  an accident into a contract.
- **Status** per feature reflects what the code actually implements.

Record what is genuinely unclear under `## Open Questions` rather than guessing.
Never invent intent, reasons, or planned work. If several ambiguities are
material to the project's direction, ask the user in one batch instead of
guessing repeatedly.

## Writing

1. Write `.spec/OVERVIEW.md` as the manifest and entry point. Use the scope's root
   determined in Preflight (the package root for a per-package spec; the
   repository root for a single-package repo or an explicit monolithic
   monorepo spec), with the required header naming the standard.
2. Follow the standard's section order, feature shape, and style rules.
   Create `OVERVIEW.md`, `GLOSSARY.md`, `INVARIANTS.md`,
   `features/`, and `adr/` even when initially empty; use `.gitkeep` for empty
   directories. Write `## Verification Strategy` and record no
   verification obligations unless the user asks for them.
   Create `api/` only when the project defines an API service, then document one
   OpenAPI-shaped route operation per Markdown file. Use the feature, API, and
   ADR templates and make file, section/ID, and skill references first-class
   links.
3. If a file exceeds 700 lines, split it into area files per the standard's
   splitting rules and add a `## Spec Map`. Never trim content to fit.
4. Do not modify code, tests, or configuration. This skill only creates `.spec/`.
   In particular, do not backfill spec markers (`§` mentions) across the
   codebase; those get added to code as it is
   touched, not in a mass annotation pass.

## Verification

- Every file is at or under 700 lines.
- Non-empty Markdown files declare the standard and status; area files declare
  `Parent` (empty required placeholders are allowed).
- Internal links and `## Spec Map` entries resolve.
- `OVERVIEW.md` is the manifest; related files/IDs use Markdown
  links and skills use `/skill-name` notation.
- Required root files and `features/`/`adr/` directories exist; `api/` is
  present if and only if the project defines an API service, and each API file
  documents one route operation with the required template fields.
- Feature IDs are unique.
- No secrets, credentials, hostnames, personal paths, or machine state.
- Every claim traces back to something you actually read.

## Report

State the scope the spec covers (package name, or "whole repository"), the
files created with line counts, the features captured, and the open questions
that need the user's answer.
