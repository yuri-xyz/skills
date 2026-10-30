---
name: review-leaks
description: Use when something is about to be published, deployed, exposed, open-sourced, or packaged, such as a deploy, a release, or a package upload, and its source tree, build output, or history must be checked for private workflow material, such as agenda, spec, debug, reference, licensing, agent, or secrets files, decision records, or agent transcripts. For personal and machine-identifying details use /review-pii, and for runtime telemetry and data collection use /review-privacy.
---

# Review Leaks

## Objective

Find private material in anything that is about to become public, before it
does. Private material is everything that exists for the user's own work
rather than for the product: plans, specs, decisions, debugging, research,
compliance records, agent configuration and transcripts, and secrets. None of
it belongs in a public repository, a published package, or a deployed site,
even when the project itself is open source.

This skill only reviews and reports. Do not delete, rewrite, or move anything
unless the user asks; when it runs inside a publish or deploy workflow, that
workflow owns the fixes.

## Scope

Check every surface that will become public, not only the source tree:

- **Source to be published:** the tracked files at the commit being published,
  read with `git ls-files` or `git archive`, never a raw working-tree listing
  that misses what is ignored or includes what is not tracked.
- **Built output:** the exact directory, archive, or image that ships, such as
  `dist/`, `build/`, `out/`, `public/`, `result`, a static-site or Worker
  assets directory, an npm tarball (`npm pack --dry-run`), a crate
  (`cargo package --list`), a wheel or sdist, a container image's layers, or
  a release archive. Build tools copy dotfiles and whole directories in more
  often than expected.
- **Source maps and embedded sources:** `*.map` files and inline
  `sourceMappingURL` data carry the original source, comments included, to
  anyone who loads the page.
- **History:** when an existing repository is being made public, every
  reachable commit, tag, and branch, not just the tip. A file deleted later
  is still in history.
- **The live deployment,** when it already exists and the user agrees: request
  a short list of known private paths, such as `/.env`, `/.git/config`,
  `/.agenda/`, and `/.spec/`, with an anonymous user agent, and report any
  that answer with content.

## Private Material

Flag any of these on a public surface:

- **Planning and decisions:** `.agenda/`, `.spec/`, architecture decision
  records (`adr/`, `docs/adr/`, `decisions/`, files named `ADR-*`), design
  rationale written for the user rather than for users of the project, and
  task lists or roadmaps.
- **Debugging:** `.debug/`, `*.log`, debug and trace dumps, `core.*` files,
  crash reports, profiler output, and temporary probe scripts.
- **Reference material:** `.refs/`, and anything recording which other
  products, projects, or designs were studied, compared against, or
  replicated, including comments that name them as the source of an idea.
- **Compliance records:** `.licensing/`, clean-room notes, patent searches,
  and provenance working files.
- **Agent configuration and history:** `.claude/`, `.agents/`, `.codex/`,
  `AGENTS.md`, `CLAUDE.md`, local skills, agent memory, and transcripts or
  session logs of conversations with AI agents, such as `*.jsonl` session
  files or pasted conversations.
- **Deployment and publish configuration that is private:** `.cloudflare/`
  and local deploy settings that name private accounts, zones, or internal hosts.
- **Secrets and environment:** `.env`, `.env.*`, `env` and `*.env` files,
  `.dev.vars`, `secrets/`, encrypted secret files such as `*.age` or SOPS
  files, private keys (`*.pem`, `*.key`, `id_*`), keystores, credential
  files, tokens, and connection strings. An encrypted secret still leaks its
  existence, names, and recipients.
- **Private locations:** URLs of private repositories, private flake inputs
  or Git dependencies, non-public deployments, preview or staging hosts,
  internal dashboards, and hosting account identifiers.
- **References to any of the above inside shipped files:** comments or
  strings that cite a spec section (`§`), an agenda item, an ADR number, a
  debug trace, a skill reference such as `/skill-name` or `$skill-name`, or
  agent instructions.

Ignore files only when they are genuinely part of the product, such as a
`.env.example` with placeholder values or a public `CONTRIBUTING.md`; say why
each such file was accepted.

## Workflow

1. Identify what is being made public, how (repository, package, deploy,
   image), and the exact artifact or commit. Ask only when it cannot be
   determined from the project and the conversation.
2. List the files of every surface in Scope. For archives and images, list
   their contents without extracting them into the project.
3. Match paths against Private Material, then search contents, including
   minified and binary files with `rg -a`, for the content-level markers and
   for private URLs.
4. Check the ignore rules that govern each surface, such as `.gitignore`,
   `.npmignore`, the manifest's `files` field, `.dockerignore`, and asset
   ignore files, and report rules that would let private material in.
5. Read each hit in context and drop false positives with a stated reason.

## Report

List each finding with its severity, the surface and path, what it reveals,
and the fix, such as excluding the path, adding an ignore rule, stripping
source maps, or rewriting history. Mask secret values; never repeat one in
full. Order findings by severity:

- 🔴 Secrets or credentials, or private material already public.
- 🟠 Private material on a surface about to be published, such as agenda,
  spec, decision, reference, transcript, or compliance content.
- 🟡 Indirect leaks, such as source maps, comments citing private material,
  private URLs, or ignore rules that would let private files in later.
- 🟢 Minor exposure with little to learn from it, such as an empty private
  directory or a generic config file.

When nothing is found, say so in one line and name the surfaces checked:

🟣 No leak found: <surfaces checked>
