# Spec — Where `.spec/` Lives

This reference is the part of the [spec standard](../SKILL.md) that
decides where specs are placed in a repository. Read it when creating a spec
or working in a monorepo.

- **Single-package repository.** One `.spec/` at the repository root.
- **Monorepo, default.** Each independently versioned or buildable package
  that has a spec owns its own `.spec/OVERVIEW.md`. A package with no spec has no
  `.spec/` directory.
- **Monorepo, monolithic override.** A single top-level `.spec/` describing the
  whole monorepo is used only when explicitly requested. Do not also create
  per-package specs alongside it.
- **Workspace spec with nested sub-specs.** When the user asks for one place
  that holds both workspace-wide context and separate project specs, the root
  `.spec/` is the workspace spec and each sub-spec is a directory below it with
  its own complete layout, such as `.spec/billing/OVERVIEW.md`. A sub-spec's
  `OVERVIEW.md` has a `Parent` link to the workspace `OVERVIEW.md`, and the
  workspace `Spec Map` links every sub-spec. The sub-specs own the features
  and decisions, so the workspace spec needs `features/` and `adr/` only once
  it has workspace-wide features or decisions of its own.

A monorepo has a workspace manifest or a conventional multi-package layout with
independently versioned or buildable members; unrelated `tools/` or `scripts/`
do not make a single-package repo a monorepo.
