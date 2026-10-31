---
name: nix
description: Use when working with Nix code, flakes, derivations, overlays, NixOS, Home Manager, or nix-darwin modules.
---

# Nix Engineering Guide

Use this guide for any task that reads, edits, reviews, validates, or designs Nix code. If it is already in context and you have applied it in the current session, do not reload it just because another Nix file appears.

## First Pass

- Identify whether the file is a NixOS module, Home Manager module, package derivation, overlay, flake output, library helper, generated file, or test/check expression.
- Read nearby imports and call sites before editing. Nix files often rely on module option merging or special arguments that are not visible in the edited file.
- Preserve ownership boundaries. Host-specific behavior belongs in host modules; reusable helpers belong in library files only when they are genuinely shared.
- Prefer small, local changes over broad rewrites. Avoid formatting churn in unrelated attrsets.

## Validation

Use the narrowest useful checks while iterating, then broaden when shared behavior changed.

```sh
nix-instantiate --parse path/to/file.nix
statix check path/to/file.nix
nix eval .#checks.x86_64-linux.some-check --json
nix flake check . --no-build
```

- Run `statix check` for static analysis when changing Nix code, unless the repo has an established replacement.
- Use `nix-instantiate --parse` for fast syntax validation of standalone files.
- Use `nix eval` for module outputs, check derivations, generated JSON, and option assertions.
- Use `nix flake check --no-build` when flake outputs, shared modules, or check wiring changed. Build only when the task needs build-time validation.
- If evaluation needs impure host state, call that out and prefer pure alternatives where possible.

## Module Organization

- Keep modules focused by responsibility. Split monolithic files when a change would make them harder to scan.
- Put options near the module that owns the behavior. Do not add global helpers just to avoid a few lines of local code.
- Use typed options for reusable module interfaces. Prefer `lib.types.submodule`, `attrsOf`, `listOf`, `enum`, `nullOr`, and `oneOf` over untyped `attrs`.
- Use `lib.mkIf`, `lib.mkMerge`, `lib.optionals`, and `lib.optionalAttrs` for conditional configuration instead of manually constructing sparse attrsets.
- Keep host-specific facts in host modules or host fact files. Do not make one host depend on another host's defaults.
- Avoid activation scripts for declarative state. Use normal NixOS/Home Manager options, packages, services, files, tmpfiles, or systemd units when they model the behavior.

## Language Patterns

- Prefer `let` bindings for repeated expressions and names that clarify intent.
- Use `inherit` when it improves readability, but avoid dense inherited lists that hide where values come from.
- Prefer helpers from `pkgs.lib` or `lib` already in scope, and use `builtins.*` where applicable, over reimplementing list, attrset, string, path, or JSON handling.
- When checking available builtins, use the Nix builtins reference: https://nix.dev/manual/nix/2.28/language/builtins.html
- Use `builtins.toJSON`, Nix string escaping, structured lists, and systemd/Home Manager options instead of hand-concatenating shell or config syntax.
- Keep derivations deterministic. Avoid timestamps, random IDs, current working directory assumptions, unpinned network fetches, and host-specific absolute paths.
- Keep flake outputs pure. Reference repo files through flake-relative paths or explicit source helpers, not live home-directory paths.

## Pitfalls To Avoid

- Broad `types.attrs` on module options that should be typed or explicitly `attrsOf types.anything`.
- `with lib;` or `with pkgs;` in large scopes when it obscures provenance.
- Stringly typed shell commands with unquoted interpolations.
- Using `rec` attrsets when a local `let` binding is clearer and less fragile.
- Importing `pkgs` from inside reusable modules when it is already supplied by the module system.
- Adding overlays or package overrides for behavior that belongs in a host/service option.
- Patching generated files, store paths, Home Manager symlinks, or `/run/current-system` to make the active machine appear fixed.

## Documentation

- Add short comments for non-obvious NixOS, Home Manager, security, DNS, boot, kernel, service, and override choices.
- Explain why a surprising option is needed, not what the option mechanically says.
- Keep comments next to the option or helper they justify.
- Avoid documenting obvious assignments, local naming, or standard module patterns.

## Before Finishing

- Confirm the edited files parse.
- Run `statix check` on the edited Nix files.
- Evaluate the closest check or module output that exercises the change.
- Summarize any checks skipped and why.
