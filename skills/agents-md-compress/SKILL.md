---
name: agents-md-compress
description: Use when the user asks to shorten, compress, or deduplicate a repository's `AGENTS.md` without losing rules.
---

# Compress AGENTS.md

Make `AGENTS.md` shorter and denser without losing a single rule. The output
must govern agent behavior exactly as the input did: same obligations, same
prohibitions, same commands, same safety boundaries — expressed in fewer words.

This is an editing pass, not a rewrite. Never use compression as cover for
dropping a rule you disagree with, softening a hard prohibition, or inventing
guidance the original did not state.

## Preflight

1. Locate the file. It is normally `AGENTS.md` at the repository root; some
   repos symlink `CLAUDE.md` to it, or the reverse. Resolve symlinks and edit
   the real file, never the link. If both exist as independent regular files,
   ask which one is canonical before touching either.
2. Read it completely, end to end, before editing anything.
3. Check whether the repository has a `.spec/` entry point (`OVERVIEW.md`).
4. Check for nested `AGENTS.md` files in subdirectories or packages. Compress
   only the one requested; a rule that lives in a nested file is not a
   duplicate of the root file's rule unless the user says so.

## Rule Inventory

Before rewriting, build a numbered inventory of every distinct normative
statement in the file: each rule, constraint, prohibition, command, path,
convention, and safety boundary. Keep this inventory for the whole session; it
is the checklist you verify against at the end. One inventory entry per
obligation, even when several share a bullet.

Mark each entry as one of:

- **keep** — a real rule that stays in `AGENTS.md`.
- **merge** — semantically covered by another entry; record which one absorbs it.
- **drop** — pure restatement, filler, or a near-exact copy adding nothing.
- **move** — belongs in the specification rather than in agent instructions.
- **ask** — you are not certain, so the user decides.

Anything that is not obviously in one bucket is **ask**. Guessing here is how
a working rule quietly disappears.

## What To Compress

- **Exact and near-exact duplicates.** Delete the copy. When two statements
  differ only in wording, keep the more precise one; when they differ in
  strength, keep the stricter one and say so in your report.
- **Overlapping rules.** Merge into one statement that covers both cases. If
  merging would blur a distinction the repository actually depends on, do not
  merge.
- **Verbose prose around a simple rule.** Reduce explanation to the rule plus
  the reason it exists, when the reason is load-bearing. Drop rationale that
  only restates the rule.
- **Enumerations of the obvious.** Long example lists collapse to the rule and
  one or two representative examples — keep the examples that are surprising or
  easy to get wrong.
- **Scattered rules on one topic.** Gather them under a single heading instead
  of repeating context in three places.
- **Process narration and hedging.** "You should probably consider trying to"
  becomes "Do". Imperative voice throughout.

## What Never Gets Compressed Away

- Exact commands, flags, paths, file names, option names, and host names.
- Safety boundaries, destructive-operation gates, secret-handling rules, and
  explicit prohibitions. Keep their force; compress only their packaging.
- Reasons that explain why a non-obvious rule exists. Deleting the reason makes
  the rule look arbitrary and invites a future agent to override it.
- Any rule whose wording looks deliberately narrow — an exception, a carve-out,
  or "except when" — those carry more meaning per word than the surrounding
  text.
- Escaping, quoting, determinism, and correctness-boundary guidance.

## Moving Content Into The Spec

`AGENTS.md` answers "how should an agent work in this repository". The
specification answers "what is this project and how must it behave". Content in
the wrong file is the largest single source of bloat.

Candidates for relocation: product intent and direction, feature behavior and
edge cases, architectural decisions and their rationale, contracts, invariants,
domain glossary terms, and API descriptions.

Stay in `AGENTS.md`: repository layout, workflow and validation commands,
source-of-truth files, tooling conventions, code style, testing practice, and
safety boundaries.

Procedure:

1. If the repository has a `.spec/`, load `/spec` and follow it. Add the moved
   content to the file that owns it — a feature contract, `INVARIANTS.md`,
   `GLOSSARY.md`, or an appended ADR for a recorded decision. Never edit a
   committed ADR in place.
2. If it has no `.spec/`, do not create one silently. Creating a spec is
   `/spec-init` and needs explicit user approval. Ask whether to initialize one
   and move the content, or leave the content in `AGENTS.md` for now. If the
   user declines, the content stays; compress it in place and say so.
3. Leave a pointer in `AGENTS.md` when an agent still needs to find the moved
   content — one line linking to the spec file, not a summary that will drift.
4. Move content verbatim in substance. Relocation and compression are separate
   operations; do not reword a rule while it is in transit.

## When To Ask

Use `/interview` whenever you are unsure whether something may be removed,
merged, or moved. Specifically:

- Two rules look redundant but might cover distinct cases.
- A rule seems obsolete, contradicted by the repository, or outside what the
  project does today.
- A statement could be either agent guidance or specification content.
- The reason for a rule is unclear and dropping the reason might strip meaning.
- Moving content would require creating a `.spec/`.
- A section reads like a historical decision, a migration note, or a boundary
  the user set deliberately.

Collect the pending questions, then run the interview per that skill's rules. Do not delete first and ask afterward.

## Verification

Before reporting, walk the inventory and confirm:

- Every **keep** entry appears in the new file with the same force.
- Every **merge** entry is genuinely covered by its absorbing statement; state
  which one, in your report.
- Every **drop** entry was a restatement, not a rule.
- Every **move** entry is present in its new spec location and, where needed,
  is reachable from `AGENTS.md`.
- Every **ask** entry has an answer from the user.
- All commands, paths, and option names still match the repository.
- No new rule appeared that the original did not state.
- Headings and links resolve; the structure is still navigable.

Do not report a line-count reduction as success on its own. A shorter file that
lost a rule is a regression.

## Report

State the before/after size, what was merged and into what, what was dropped
and why it was not a rule, what moved to which spec file, what the user decided
during the interview, and anything you deliberately left verbose because
compressing it would have cost meaning.
