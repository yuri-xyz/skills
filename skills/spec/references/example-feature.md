# Feature File Example

This is the complete shape of a small feature file. It belongs under
`.spec/features/` and is not a decision log.

```markdown
# Mirrorctl — Execution

> Status: active
> Parent: [OVERVIEW.md](../OVERVIEW.md)

## Features

### F-03 Execute <a id="f-03"></a>

**Intent.** Apply a plan such that interrupting the process leaves the remote
in a valid state and the next run resumes without redoing completed work.

**Behavior.**
- Uploads run with at most `--concurrency` in-flight parts.
- Each completed action is appended to the journal before the next starts.
- Remote deletions run last, after every upload succeeds.

**Edge cases.**
- SIGINT or SIGTERM during an upload → abort in-flight multipart uploads, flush
  the journal, and exit 130. Why: orphaned uploads accrue storage charges.
- Any upload fails → skip the deletion phase and exit non-zero. Why: deleting
  remote objects after a partial mirror can destroy the only complete copy.

**Testing.**
- **fault-injection** — an interruption at any upload step leaves no orphaned
  multipart upload and a journal that resumes without repeating finished
  actions.
- **integration** — a failed upload against a local object store skips every
  deletion.
- **unit** — each edge case above, with exit codes.

**Depends on.** [§F-02](../features/plan.md#f-02).

**Related specs.** [§INV-01](../INVARIANTS.md#inv-01),
[§ADR-0002](../adr/storage.md#adr-0002).

**Skills.** `/examples` — preserve the failure-handling pattern illustrated by
this example.

**Status.** implemented
```
