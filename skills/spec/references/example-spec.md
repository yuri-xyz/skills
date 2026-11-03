# Example Spec — Layout

A compact example of a `.spec/` governed by the spec standard. The
manifest stays small; each concern has one owner.

```text
.spec/
├── OVERVIEW.md
├── GLOSSARY.md
├── INVARIANTS.md
├── features/
│   ├── scan.md
│   └── plan.md
└── adr/
    └── storage.md
```

## `OVERVIEW.md`

```markdown
# Mirrorctl — Overview

> Status: active
> Spec-Name: mirrorctl

## Purpose

`mirrorctl` mirrors a local directory to an S3-compatible bucket on demand or
on a schedule. It is safe to interrupt and never requires an operator prompt.

## Goals

- Mirror local files safely and deterministically.
- Make interruption and recovery safe without operator prompts.

## Non-goals

- Remote-to-local or bidirectional synchronization.
- A GUI, daemon, or client-side encryption scheme.

## Intent and Principles

- Correctness over throughput; silent data loss is unacceptable.
- The local directory is the source of truth.
- Rejected: bidirectional sync, because it introduces conflict resolution and
  an always-on process outside this tool's purpose.

## Scope

In scope: one-way mirroring, resumable uploads, scheduling, integrity checks,
and dry runs.

## Architecture Summary

The scanner emits a sorted local view, the planner produces an ordered action
list, and the executor applies it with bounded concurrency. A resumable journal
is the only persistent state.

## Verification Strategy

- **Testing kinds.** `unit` and `integration` use the Rust test harness,
  `property` uses proptest, and `fault-injection` uses a local object-store
  double. All run by `just test`.
- **code-check.** Kani, run by `just verify`.
- **Project-wide assumptions.** The Rust compiler and the object-store client
  are trusted.
- No design models or proofs are used yet.

## Spec Map

- [GLOSSARY.md](GLOSSARY.md) — domain terms.
- [INVARIANTS.md](INVARIANTS.md) — project-wide obligations.
- [features/scan.md](features/scan.md) — deterministic local scanning.
- [features/plan.md](features/plan.md) — dry-run planning and action order.
- [adr/storage.md](adr/storage.md) — journal and persistence decisions.
```

## `features/plan.md`

```markdown
# Mirrorctl — Planning

> Status: active
> Parent: [OVERVIEW.md](../OVERVIEW.md)

## Features

### F-02 Plan <a id="f-02"></a>

**Intent.** Let an operator see exactly what a run will do before it changes
the remote bucket.

**Behavior.**
- Compares local entries to the remote manifest by size and `SHA-256` content
  hash.
- Emits uploads, replacements, and deletions in a stable order.
- `--dry-run` prints the plan and exits 0 without contacting the executor.

**Constraints.** Planning performs reads only and never mutates the journal.

**Performance.**
- **plan.** O(n log n) in n = files under the local root; planning streams both
  sides and uses O(1) additional memory in n. Why: one request per file made
  large trees exceed the original execution budget.

**Status.** implemented
```

## Optional `api/`

This CLI example has no API service, so it omits `api/` entirely. A project with
an API service adds one route-operation Markdown file per path and method under
`.spec/api/`; see [example-api.md](example-api.md) for the complete OpenAPI-shaped
template, including authentication, incoming-data validation, rate limiting,
responses, errors, and edge cases.

## `adr/storage.md`

```markdown
# Mirrorctl — Storage Decisions

> Status: active
> Parent: [OVERVIEW.md](../OVERVIEW.md)

## ADR-0001 — Keep the journal append-only <a id="adr-0001"></a>

**Recorded.** 2026-08-19

**Context.** A partial write can leave recovery state ambiguous, while a full
rescan is deterministic and inexpensive.

**Decision.** The journal is append-only. Recovery discards a truncated suffix
and rebuilds state from the local source of truth.

**Consequences.** Recovery is predictable, but a corrupt journal causes a
rescan.

## ADR-0002 — Keep remote deletion after uploads <a id="adr-0002"></a>

**Recorded.** 2026-08-19

**Context.** A failed upload must not remove the only complete remote copy.

**Decision.** Remote deletions run only after every upload in the same plan
succeeds.

**Supersedes.** None.
```

## `GLOSSARY.md` and `INVARIANTS.md`

The glossary holds definitions and boundaries only, and each term heading
carries an explicit anchor:

```markdown
### Remote manifest <a id="remote-manifest"></a>

**Definition.** The bucket-side record of every mirrored file's size and
content hash, written after each completed run.

**Not to be confused with.** The local journal, which records progress within
a run.
```

The invariant file contains obligations such as:

```markdown
### INV-01 — Never mutate the local source <a id="inv-01"></a>

**Rule.** The tool must not modify or delete a file under the configured local
root.

**Rationale.** The local tree is the source of truth.
```

The feature, ADR, glossary, and invariant files are independently maintainable;
the manifest is the navigation surface rather than a second copy of their
content. The other root files and `features/`/`adr/` directories remain required
even when their content is initially empty.
