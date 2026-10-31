---
name: nix-run
description: Use when a needed open-source CLI is missing from the environment and does not belong in the project's dependencies.
---

# Nix Run

## When To Use This

Use this skill for ephemeral, agent-initiated tool use: you need a capability right now to finish a step (convert an image, reformat data, inspect a binary/archive, run a one-off script), the tool isn't on `PATH`, and the tool has nothing to do with what the project itself depends on.

Do not use this skill when the tool is actually something the project should depend on going forward (a build tool, a runtime dependency, something a script or CI step will call again). That is a declarative Nix change — add it through the normal source of truth (the project's flake or dev shell, or the system configuration's package list), not an ad hoc `nix run` invocation. If unsure which case applies, ask: "would the next person working on this repo also need this tool?" If yes, it's a dependency, not a one-off.

## Workflow

1. Confirm the tool truly isn't available: check `command -v <tool>` or `which <tool>` first. Don't reach for `nix run` if the tool is already on `PATH`.
2. Confirm this is genuinely ephemeral, task-local tool use, not a project dependency (see above). If it turns out to be a real dependency, stop and make the declarative change instead.
3. Identify the right nixpkgs package/attribute for the capability (e.g. `imagemagick` for image conversion, `ffmpeg` for media, `poppler-utils` for PDF text extraction, `jq`/`yq` for structured data, `exiftool` for metadata).
4. **Verify the package is open source before running it**, regardless of whether this system's Nix config sets `allowUnfree = true`. That flag is a system-wide default for real project dependencies — it is not license clearance for a tool you're about to invoke ad hoc. Check one of:
   - `nix eval --json nixpkgs#<pkg>.meta.license.free` — should evaluate to `true`.
   - `nix eval nixpkgs#<pkg>.meta.license.spdxId --raw` (or `.fullName`) to see the actual license and confirm it's a recognized open-source license (MIT, Apache-2.0, GPL-*, BSD-*, MPL-2.0, ISC, etc.), not `unfree`, `unfree-redistributable`, or a proprietary EULA.
   - If eval access isn't available, check the package's listing on search.nixos.org or its upstream repository for a clear open-source license before proceeding.
   - If the package is unfree or its license is unclear, do not run it. Look for an open-source alternative that covers the same need, or ask the user.
5. Run it without installing anything persistent:
   - Single invocation: `nix run nixpkgs#<pkg> -- <args>`
   - Multiple invocations or an interactive session: `nix shell nixpkgs#<pkg> -c <command> <args>`, or `nix shell nixpkgs#<pkg>` followed by normal commands in that shell.
6. Use the unpinned `nixpkgs` flake registry reference for this kind of ephemeral, throwaway invocation — it does not need to match this repo's pinned `flake.lock` input, since nothing about the result is committed or depends on reproducing this exact tool run later.
7. Do not modify `flake.nix`, `flake.lock`, package lists, devShells, or any other tracked file just to make this one-off tool available. Nothing about this workflow should leave tracked-state changes behind.
8. Report which package and command were used, and the open-source license check performed, alongside the result.

## Examples

- Need to convert a PNG to WebP while inspecting an asset: check the license of `imagemagick` (Apache-2.0), then `nix run nixpkgs#imagemagick -- convert input.png output.webp`.
- Need to pretty-print or query some JSON output while debugging: `nix run nixpkgs#jq -- '.' file.json` (skip the license check step in explanation once it's established `jq` is MIT-licensed and well-known, but still don't install it into the project).
- Need to extract text from a PDF to answer a question: verify `poppler-utils` is open source (GPL-2.0), then `nix run nixpkgs#poppler-utils -- pdftotext file.pdf -`.

## Boundaries

- This skill is for tools the agent needs to get a task done, not for changing what the project builds, ships, or requires. If the same capability needs to be available to a script, CI job, systemd unit, or devShell in this repo, that must go through the normal declarative Nix module path, not a raw `nix run` embedded in tracked code.
- Never skip the open-source check to save time — proprietary or unclear-license tools are off-limits for this ad hoc workflow even if the host's `nixpkgs.config.allowUnfree` is `true` for its own declared packages.
- Do not use this skill to work around a package genuinely missing from the project's own dependency set when the task is actually about building or running the project — fix the declarative dependency instead.
- Do not leave any generated flake registry pins, lockfile changes, or profile installs behind; `nix run`/`nix shell` should not mutate repo or system state.
