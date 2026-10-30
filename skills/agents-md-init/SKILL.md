---
name: agents-md-init
description: Use when a repository has no `AGENTS.md` yet, or the user asks to create or substantially rewrite one.
---

# Initialize AGENTS.md

Create an `AGENTS.md` that helps future agents work safely and idiomatically in
the repository. Keep it factual, project-specific, and reproducible.

## Workflow

1. Inspect the repository before writing.
   - Read top-level files such as `README*`, package manifests, build files,
     `flake.nix`, test configuration, existing docs, and source layout.
   - Identify the project type, primary languages, package managers, validation
     commands, generated files, deployment boundaries, and unsafe operations.
   - If an `AGENTS.md` already exists, preserve useful instructions and update
     stale or missing sections instead of replacing it wholesale.

2. Write instructions that are durable.
   - Prefer repo-relative paths and generic examples.
   - Describe source-of-truth files, common workflows, validation commands, code
     organization, and project-specific hazards.
   - Do not include private usernames, display names, hostnames, absolute home
     paths, live machine state, or local-only assumptions.
   - Do not claim commands exist until the repository evidence supports them.

3. Keep the file concise but actionable.
   - Use short sections with direct rules.
   - Include exact commands only when they are discoverable from the repo.
   - Call out skipped or optional workflows, especially expensive, destructive,
     networked, or deployment-like commands.

## Testing Guidance

- Require tests to be generic and reproducible across machines.
- Do not write tests that depend on the current user's home directory, username,
  display name, hostname, local absolute paths, private files, machine-specific
  devices, or checked-out path.
- Avoid mentioning real local paths, real personal names, usernames, display
  names, hostnames, or machine identifiers in tests or fixtures.
- Use temporary directories, fixtures, repo-relative paths, generated sample
  data, or dependency-injected paths.
- If a test genuinely needs a filesystem path, keep it local to the test's temp
  directory, fixture directory, or repository fixture and explain the constraint.
- Avoid smoke tests unless they exercise a meaningful project boundary. Prefer
  focused behavior tests, option evaluation, parser checks, command argument
  assertions, and generated-output checks.

## Nix Guidance

- If the repository uses Nix, flakes, NixOS, Home Manager, derivations, overlays,
  or `.nix` files, apply the project's Nix conventions before finalizing Nix-specific guidance.
- Prefer Nix-provided development and validation workflows when the project
  supports them, such as `nix develop`, `nix flake check --no-build`, focused
  `nix eval` checks, `nix-instantiate --parse`, and `statix check`.
- Encourage pure, deterministic flake inputs and repo-relative source paths.
- Document which Nix outputs, dev shells, checks, or packages are the practical
  entry points for agents.
- Do not suggest live system switching, activation, deployment, disk operations,
  or destructive install flows unless the project clearly owns those workflows
  and the AGENTS.md marks them as explicit opt-in operations.
- For Rust projects packaged with Nix, mention build-time-friendly patterns when
  applicable, such as using `crane`, incremental-friendly derivation structure,
  and avoiding needless rebuild triggers.

## Code Organization

- Warn against growing monolithic files. Prefer splitting new work into focused
  modules, components, packages, or helper files that match existing ownership
  boundaries.
- Keep generated files, vendored dependencies, build outputs, caches, lockfiles,
  and snapshots subject to the repository's existing policy.
- Tell agents to follow existing local patterns before introducing new
  abstractions, frameworks, or dependencies.

## Code Quality Guidance

- Prefer standard library helpers, typed APIs, structured parsers, and existing
  project utilities over ad hoc string manipulation or duplicated logic.
- Lean on the type system for invariants when the language supports it. Use
  runtime assertions for boundary checks, impossible states, and diagnostics,
  not as a substitute for sound data modeling.
- Use defensive programming at external boundaries: parsing, file I/O, network
  input, process execution, config loading, and user-provided values.
- Keep errors actionable and include relevant context such as option names,
  command names, source paths, or input labels.
- Optimize build and check times by preferring focused validation, module
  boundaries that avoid needless rebuilds, and dependency structures that keep
  expensive work cached.

## Documentation Guidance

- Ask agents to document non-obvious code, constraints, and safety decisions
  with concise comments.
- Use `/document` after architecture changes, bug fixes, or non-obvious
  implementation changes when inline comments would help future maintainers.
- Comments should explain why a surprising choice exists, not restate what the
  code already says.

## Recommended AGENTS.md Shape

Use only sections that match the repository:

- Project overview and source of truth
- Repository layout
- Core workflows and validation commands
- Testing rules
- Nix workflow, when applicable
- Code organization and quality expectations
- Documentation and comments
- Safety boundaries, secrets, generated files, and deployment constraints

Keep final instructions independent of the current machine so another agent can
follow them in a fresh clone.
