---
name: nix-flake-init
description: Use when a project needs a new Nix flake, or its flake lacks pinned inputs, a real build, a dev shell, or checks.
---

# Nix Flake Init

Give the project at hand a working `flake.nix`: pinned inputs, a package that
actually builds it, a dev shell that can develop it, and checks that validate it.

Read `/nix` first and apply it throughout — it owns the language, module,
determinism, and validation rules this skill assumes. Check the NixOS Wiki when
a package, builder, or platform detail is unclear.

Do not add a flake to a project that did not ask for one.

## Preflight

1. Find the project root and inspect existing Nix entry points: `flake.nix`,
   `shell.nix`, `default.nix`, `nix/`, `.envrc`, CI workflows.
2. If a `flake.nix` already exists, do not clobber it. Report what it provides
   and extend the missing outputs instead, keeping its structure and style.
3. If `shell.nix` or `default.nix` exists, carry its dependency list into the
   flake and ask before removing the old entry point — other tooling may use it.
4. Identify the project type from manifests and lockfiles, not from file
   extensions alone: `Cargo.toml`, `package.json` plus its lockfile,
   `pyproject.toml`, `go.mod`, `build.zig`, `CMakeLists.txt`, `*.cabal`, mix,
   gradle, and so on.
5. Note the target systems the project realistically supports. Default to
   `x86_64-linux` and `aarch64-darwin` unless the project says otherwise; do not
   claim systems you cannot evaluate.

## Inputs

- Pin every input to an upstream **immutable versioned release tag**. Use a named
  release branch only when upstream publishes no suitable tag. Use an exact
  commit only when there is no compatible release at all, and say why in a
  comment.
- Never declare an implicit default branch, `master`, `main`, `latest`, or a
  moving rolling ref such as `nixos-unstable` as the fallback.
- Keep the input set minimal. Every input is a maintenance obligation.
- Deduplicate transitive nixpkgs with `inputs.<dep>.inputs.nixpkgs.follows =
  "nixpkgs"` so the closure does not carry several nixpkgs revisions.
- Commit `flake.lock`. Generate it with `nix flake lock`, and update a declared
  release together with its lock entry.

## Structure

Keep the flake small and explicit. A single `flake.nix` is right for most
projects; move logic into `nix/` when it grows past what fits comfortably in one
screen of outputs, and split before any file approaches 700 lines.

Use a plain per-system helper unless the project already uses `flake-parts` or
`flake-utils`:

```nix
systems = [ "x86_64-linux" "aarch64-darwin" ];
forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
```

Provide the outputs the project can honestly support:

- `packages.<system>.default` — the buildable artifact. Required whenever the
  project produces one.
- `devShells.<system>.default` — everything needed to build, test, and lint.
- `checks.<system>.*` — cheap validation wired to `nix flake check`.
- `formatter.<system>` — the project's formatter.
- `apps.<system>.default` — only when the entry point is not obvious from the
  package's `meta.mainProgram`.
- `overlays.default` / `nixosModules.*` — only when the project is genuinely
  consumed by other flakes.

Do not emit outputs the project cannot back up. An empty or broken output is
worse than a missing one.

## The Package

Use the ecosystem's real builder rather than hand-rolling phases:

- Rust: `rustPlatform.buildRustPackage`, or `crane` when incremental,
  workspace-aware, or cross-cutting builds matter.
- Go: `buildGoModule` with `vendorHash`.
- Node: the packaging path that matches the lockfile
  (`buildNpmPackage`, `pnpm.fetchDeps`, yarn helpers).
- Python: `buildPythonApplication` / `buildPythonPackage`, with `uv2nix` or
  `poetry2nix` only when the dependency set justifies it.
- C/C++: `stdenv.mkDerivation` with the project's real build system
  (`cmake`, `meson`, `ninja`) in `nativeBuildInputs`.

Rules:

- Split `nativeBuildInputs` (build-time) from `buildInputs` (runtime/link-time)
  correctly; getting this wrong breaks cross-compilation silently.
- Set `meta` with `description`, `license`, `mainProgram`, and `platforms`.
- Wrap runtime dependencies with `makeWrapper` instead of assuming the user's
  `PATH`.
- Do not fetch from the network at build time. Fixed-output dependency
  derivations (`cargoHash`, `vendorHash`, `npmDepsHash`) are the supported path.
- Never leave `lib.fakeHash` in a finished flake. Obtain the real hash by
  building once and taking the value from the mismatch error, then record it.
- Scope `src` so unrelated files do not trigger rebuilds — `lib.fileset` or
  `lib.cleanSource` rather than a bare `./.` in projects with large assets or
  scratch directories.
- Avoid import-from-derivation when a plain expression works; it slows every
  evaluation of the flake.

## The Dev Shell

- Include exactly the toolchain, build tools, linters, formatters, and test
  runners the project's own workflows call. Not a grab bag of favorites.
- Prefer `mkShell { packages = [ ... ]; }` and declared `env` attributes over a
  `shellHook` that mutates the environment.
- Reuse the package's own inputs with `inputsFrom = [ self.packages.${system}.default ];`
  instead of restating the dependency list twice.
- Add `.envrc` with `use flake` only when the project already uses direnv or the
  user asks; if you add one, ensure `.direnv/` is gitignored.

## Checks

Wire checks that are cheap and meaningful — a formatter check, a lint run, the
test suite when it is fast and hermetic. Do not wire a check that needs network
access, a live service, or host state; say so instead of faking it.

## Validation

Flakes only see **Git-tracked** files. `git add` new files before evaluating, or
evaluation fails with a confusing "path does not exist" error.

Work up the ladder, narrowest first:

```sh
nix-instantiate --parse flake.nix
statix check flake.nix
nix flake metadata .
nix flake check . --no-build
nix build .#default --no-link --print-out-paths
```

`nix build` is the only real proof the package works. Run it when the user
permits a real build; it can be slow and needs network access for the substituter
and fixed-output fetches. If you skip it, say plainly that the package is
unbuilt and unverified rather than implying it works.

Add `result`, `result-*`, and `.direnv/` to `.gitignore` if they are not already
covered.

## Boundaries

- Do not restructure the project's source layout, change its build system, or add
  CI to make packaging easier. Package what exists.
- Do not run installs, switches, activation, or anything touching system state.
- Do not add a flake to a repository whose owners chose a different Nix entry
  point without asking.
- If packaging is genuinely blocked — a vendored binary blob, a build that
  requires network access, an unfree dependency — stop and report the specific
  blocker rather than shipping a flake that only appears to work.
- If the project has a `.spec/` and adding the flake changes its distribution,
  supported platforms, or build contract, follow `/spec-sync`.

## Report

State the outputs created, the pinned input versions, the commands to build, run,
and enter the dev shell, every hash that still needs filling, and exactly which
validation steps ran versus were skipped.
