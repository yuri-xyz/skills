---
name: spec
description: Use when writing, reviewing, or maintaining a `.spec/` specification, or when work must follow or cite one. Reference freely; creating a spec requires explicit user approval.
---

# Spec

This document is the normative definition of the **spec** standard. It
separates ownership of features, decisions, domain terms, inviolable rules, and
API routes, and adds **formal verification obligations**: a spec can state,
next to the behavior it constrains, which properties must eventually be
machine-checked rather than only written down, by which kind of tool, under
which bounds and assumptions, and how the check connects to the shipped code.

Verification is narrow and on demand. It targets the few properties that
are core, failure-prone, and precise enough to check, and it is implemented
when the user asks or the owning area has stabilized, not from day one. The
main cost of formal verification is keeping artifacts current while code
changes, so breadth is the thing to avoid, not difficulty.

## What A Spec Is

A spec is the source of truth for what a project is meant to be. An agent that
reads only the spec should know what the project does, what it deliberately does
not do, how its features are supposed to behave, which edge cases matter, and
why the non-obvious decisions were made.

A spec is a technical document with one twist: it also carries **intent**. Where
a rule was earned by a bug, incident, platform quirk, security consideration, or
rejected design, the spec records the reason next to the rule or in the ADR that
led to it.

A spec operates at the level of direction, features, contracts, and behavior. It
is not a code mirror: type definitions, file tours, and line numbers change
constantly, and the code already states them.

## When To Use This Skill

Read and cite this standard freely: to answer questions about spec structure, to
judge whether a spec is well-formed, to interpret a project's `.spec/` while
doing other work, or when `/spec-init` / `/spec-sync` load it.

**Creating spec files requires explicit user approval.** Reading this standard is
never authorization to create `.spec/`, an entry point, or an area file for a
project that does not already have one. If a project would clearly benefit from
a spec, say so in one sentence and wait for the user to ask.

**Maintaining an existing spec is expected.** If a project already has a
`.spec/` and work changes its direction, features, contracts, invariants, or
documented behavior, update the spec as part of that same change. Material
decisions are recorded in `adr/` without waiting for a separate prompt.

## File Layout

Specs are committed to Git under a `.spec/` directory. Never gitignore them;
never place secrets, credentials, tokens, hostnames, or personal paths in them.

The layout is:

```text
.spec/
├── OVERVIEW.md             # project manifest and context
├── GLOSSARY.md             # domain vocabulary and business meanings
├── INVARIANTS.md           # project-wide rules that must never be violated
├── features/               # feature contracts only
│   ├── sync.md
│   └── conflict-resolution.md
├── adr/                    # append-only decision records only
│   ├── architecture.md
│   └── security.md
├── api/                    # route contracts, required only for an API service
│   ├── users.md
│   └── auth/
│       ├── sign-up.md
│       └── sign-in.md
└── models/                 # design models, only when an obligation uses one
    └── ledger.qnt
```

`OVERVIEW.md` is the required manifest and entry point.
Project identity and direction belong there; feature behavior belongs under
`features/`; decision history belongs under `adr/`; route contracts belong under
`api/` when the project defines an API service; design models backing
verification obligations belong under `models/`.

`OVERVIEW.md`, `GLOSSARY.md`, `INVARIANTS.md`, `features/`, and `adr/` are
required in every spec, even when empty; a workspace spec with nested
sub-specs needs `features/` and `adr/` only for workspace-wide entries. Keep an
empty required file empty and an empty required directory in Git with
`.gitkeep`. A usable `OVERVIEW.md` needs its header and manifest sections.
Create `api/` if and only if the project defines an API service. Omit it
entirely for projects without one; when present, every Markdown file below it
describes exactly one route operation. Create `models/` only when at least
one verification obligation is backed by a design model; it holds model source
files, not Markdown notes.

The only normal top-level Markdown files are `OVERVIEW.md`, `GLOSSARY.md`, and
`INVARIANTS.md`; do not add arbitrary feature, decision, glossary, or invariant
files beside these directories; `api/` is conditional, not a place for API notes
or a copy of a generated OpenAPI document.

Directory names are lowercase and use kebab-case when they contain a name.
`GLOSSARY.md` and `INVARIANTS.md` use uppercase basenames and a lowercase
`.md` extension as stable, easy-to-find special files.

### Where `.spec/` Lives

A single-package repository has one `.spec/` at its root. In a monorepo, each
package that has a spec owns its own `.spec/`, unless the user explicitly asks
for one monolithic spec or a workspace spec with nested sub-specs such as
`.spec/billing/OVERVIEW.md`. [placement.md](references/placement.md) defines
these layouts and what counts as a monorepo.

Every spec has a **spec name** used to qualify mentions across specs: its
package or sub-spec directory name in kebab-case, declared by the
`Spec-Name` header of its `OVERVIEW.md`. Spec names are unique within a
repository, because a qualified mention resolves by name alone. Each spec
numbers its IDs independently, so the same ID can exist in several specs; see
[Mentioning Spec IDs](#mentioning-spec-ids) for how mentions stay unambiguous.

## Required Headers

Every spec Markdown file starts with an H1 title, one blank line, and a header
block:

```markdown
# Acme Sync — Overview

> Status: active
> Spec-Name: acme-sync
```

`Status` is `draft`, `active`, or
`superseded`. `Spec-Name` is required in `OVERVIEW.md` only and gives the spec
name used in qualified mentions. Do not add an `Updated` date; Git records when a file changed,
and a hand-kept date goes stale. `Parent` is required under
`features/`, `adr/`, and `api/` and links to the entry point. Root special files
do not need `Parent`; empty placeholders and `.gitkeep` files need no header.
An ADR header becomes immutable after its first committed entry.

## OVERVIEW.md Manifest

`OVERVIEW.md` is the first-read project context and the manifest. It explains
what the project is, why it exists, and what it will and will not do. Use these sections in order; omit optional sections only
when empty:

- `## Purpose` — what the project is and who consumes it.
- `## Goals` and `## Non-goals` — explicit direction and firm boundaries.
- `## Intent and Principles` — durable values and rejected directions.
- `## Scope` — behavior covered by the project.
- `## Architecture Summary` — boundaries and source of truth, when applicable.
- `## Cross-Cutting Behavior`, `## Security and Privacy Considerations`,
  `## Open Questions`, and `## References` when applicable.
- `## Verification Strategy` — required; see
  [Verification Strategy](#verification-strategy).
- `## Spec Map` — links to `GLOSSARY.md`, `INVARIANTS.md`, every feature area,
  every ADR topic or group, every API route or route group when `api/`
  exists, and every design model when `models/` exists.

The manifest must not contain feature entries, invariant entries, glossary
definitions, ADRs, or API route contracts. If it reaches 700 lines, keep it as
an index and split project-context areas under `.spec/overview/`.

## Feature Files

Feature contracts live exclusively under `.spec/features/`. A file may contain
one feature or a cohesive, bounded group of related features. Prefer one file
per feature when the area is large or likely to change independently.

Each feature file has a `## Features` section. Every entry has required
`**Intent.**`, `**Behavior.**`, and `**Status.**` blocks, plus optional edge
cases, constraints, performance, security, out-of-scope, current-boundary,
testing, dependency, related spec, and skill blocks. A feature's `**Performance.**` block is a compact
function/operation-scoped mini-contract: use one bullet for each relevant
function or operation, state Big-O, and define what `n` counts. A feature may
end with `VER-<n>` verification obligation sub-entries per
[Formal Verification](#formal-verification). Use the
[feature file template](references/templates.md#feature-file-template).

A feature's `**Status.**` is exactly one of these words:

- **planned** — specified, not yet implemented.
- **partial** — partly implemented. A `**Current boundary.**` block states which
  parts of the behavior are not yet satisfied.
- **implemented** — the behavior is satisfied as written.

The file header's `Status` (`draft`, `active`, `superseded`) describes the
document, not the feature. Never put code paths or progress narrative in
`Status`; code cites a feature by its `§` mention. A removed feature, invariant,
route, or obligation is deleted, never kept as a tombstone: the ADR that removes
it lists the ID in a `**Retires.**` field, links to it outside `adr/` point at
that ADR instead, and the ID is never reused. Older ADRs keep their links to the
retired entry unchanged, since committed ADRs are never edited.

Write behavior as firm declarative statements in present tense. One feature per
entry. If an entry grows past roughly 60 lines, split the feature or move a
cohesive area into another feature file without changing its ID.

Feature files may contain local grammar and algorithm details, local security
rules, and a `## References` section. They must not become decision logs,
glossaries, API route contracts, or replacements for `INVARIANTS.md`. Link to
the owning API route instead of duplicating its request/response contract.

## API Route Files

When a project defines an API service, API contracts live exclusively under
`.spec/api/`; otherwise the directory is omitted. Each Markdown file describes
one route operation identified by its path and HTTP method. If several methods
share a path, use one file per method. Nested directories group route files by
resource or path family; they do not combine routes or bypass the 700-line
limit.

Use an OpenAPI-oriented shape: path, method, unique `operationId`, intent,
security scheme/scopes, parameters, request body, responses, errors, and edge
cases. Record the OpenAPI version and link normative sections under References.
The template requires explicit `Authentication`, `Authorization`, `Incoming data
validation`, `Rate limiting`, `Request`, `Responses`, and `Edge cases` blocks;
write `None` when a policy does not apply. If present, link a machine-readable
OpenAPI document; do not paste it into the spec. A feature may link to its API
route, but the route file owns the externally observable contract.

Use the [API route template](references/templates.md#api-route-file-template).
Each route heading starts with a stable `API-<n>` ID. Keep route files at or below
700 lines; split growing route families into subdirectories and extract shared
schemas or protocol context when one route needs more detail.

## Append-Only ADR Files

Decision records live exclusively under `.spec/adr/`. ADR files are topic-based
logs, not one giant history file and not one file per implementation detail.
Choose a stable subject such as `architecture.md`, `security.md`,
`data-model.md`, or `operations.md`. Create a new topic file when a decision
does not belong to an existing topic.

Each record has a globally unique, never-reused ID and is appended at the end of
its topic file, newest last. `**Recorded.**`, `**Context.**`, and `**Decision.**`
are required; add consequences, alternatives, superseding links, retired IDs,
related spec links, and consulted skills when informative. Use the [ADR file template](references/templates.md#adr-file-template).

Context records the problem, constraints, evidence, or rejected direction; do
not record a bare conclusion.

Once an ADR file or entry is committed, never edit, reorder, renumber, delete,
or rewrite it. If a decision changes, append a new ADR with a new ID and a
`**Supersedes.**` link; if it changes only part of an earlier decision, use
`**Amends.**` instead. If a record is wrong, append a correction instead of
silently changing history. The file header is also immutable after its first
committed entry.

There is one permitted edit to a committed entry: when a newer ADR supersedes or
amends it, append a single `**Superseded by.**` or `**Amended by.**` line, with
a link to the newer ADR, at the end of the older entry, in the same change, so
a reader of the old decision learns that it no longer stands. Never change
anything else or use another status marker.

ADR IDs use `ADR-` followed by four or more digits, assigned from the next
unused number across the whole `.spec/`. Parallel branches must preserve both
existing IDs and resolve any collision by assigning a new unused ID before
merging. A retired ID is never reused.

If appending the next entry would exceed 700 lines, start a continuation such as
`architecture-2.md`. Do not split or move old entries to make room. The new file
has its own header and continues the topic with newer IDs.

## First-Class Links

Use links as traceability, not decoration. When a target exists, link it at its
first relevant mention instead of repeating its content:

- **Skills.** Write `/skill-name`, for example `/examples`, `/spec`, or
  `/spec-sync`. In a feature or ADR, use a `**Skills.**` / `**Skills consulted.**`
  block when a skill materially informed the contract or decision.
- **Spec files.** Use regular relative Markdown links such as
  `[conflict feature](../features/conflict-resolution.md)` or
  `[INVARIANTS.md](../INVARIANTS.md)`; do not leave a bare filename as the only
  reference.
- **API routes.** Link route files and IDs such as `[§API-12](../api/auth/sign-in.md#api-12)`;
  API files use actual relative paths.
- **Sections and IDs.** Link stable anchors such as
  `[§F-12](../features/sync.md#f-12)`, `[§INV-03](../INVARIANTS.md#inv-03)`,
  `[§ADR-0007](../adr/security.md#adr-0007)`, `[§API-12](../api/users.md#api-12)`, or
  `[Security](../OVERVIEW.md#security-and-privacy-considerations)`.
- **Definitions.** Headings for features, invariants, ADRs, API routes,
  verification obligations, and questions start with their bare stable ID, with
  no `§`, and end with an explicit anchor that is the lowercased ID:
  `### F-12 Sync <a id="f-12"></a>`. Links always target that anchor, such as
  `#f-12`, never the slug a renderer generates from the title. The anchor
  survives title changes, and generated slugs do not.

Verify every repository-relative link and every referenced ID. A skill token is
not a substitute for a file link, and an ID is not a substitute for its anchor
link when the target is outside the current entry.

## Mentioning Spec IDs

Every mention of a spec ID carries the `§` sigil (U+00A7, the section sign):
`§F-12`, `§INV-03`, `§VER-3`, `§ADR-0007`, `§API-12`, `§Q-02`. This applies
everywhere a spec ID is referenced: spec files, code comments, tests, design
models, commit messages, plans, tasks, reviews, and agent replies. The sigil
makes a mention unambiguous, because a bare `F-12` or `Q-02` can mean many
things, and it makes mentions findable:

```text
rg '§([a-z0-9-]+:)?[A-Z]+-[0-9]+'   # every spec mention
rg '§VER-3\b'                       # every unqualified mention of one ID
rg '^#+ VER-3\b' .spec              # its definition
```

The sigil marks a mention, never a definition. A definition heading keeps its
bare ID, such as `### F-12 Sync`, so a reference and its definition are always
distinguishable. Inside a spec, a mention is normally also a link, and the link
text carries the sigil: `[§F-12](../features/sync.md#f-12)`. Text that
describes an ID format, such as "feature IDs are `F-<n>`", is not a mention and
takes no sigil.

A mention resolves to the nearest spec that owns the place where it is
written: the spec of the enclosing package or sub-spec, else the root spec. To
mention an ID in a different spec, qualify it with that spec's name:
`§billing:F-3`, `§auth:ADR-0107`. Qualify every mention whose nearest spec
is not the owner, including code in one package that cites another package's
spec.

A mention inside a code span, a string literal, or a fenced block is an
example, not a citation. Write examples of the syntax, test fixtures, and
mentions of fictional specs that way. The `rg` searches above still match them,
so skip such hits when tracing citations.

Agents always write the sigil. When a user types a bare ID such as `F-12` and
the context clearly refers to the spec, treat it as `§F-12`; when it is not
clear, ask rather than guess.

## GLOSSARY.md

`GLOSSARY.md` defines business-specific terms, abbreviations, and concepts that
an agent or outsider could misunderstand. It is authoritative for meaning, not
for implementation.

Use one entry per term with a required `**Definition.**`, an optional `**Not to
be confused with.**` naming the nearby meanings it excludes, and optional
`**Related specs.**` links. Put the term's boundary in those two blocks; there
is no separate boundary block. Use the
[glossary entry template](references/templates.md#glossary-entry-template).

Terms have no IDs, so each term heading carries an explicit kebab-case anchor,
`### Sub-spec <a id="sub-spec"></a>`, and links target it. Start from the
heading's slug and keep the anchor when the term is renamed, so its links
survive the rename.

Do not put feature behavior, decisions, or invariants in the glossary. Link to
the owning feature or invariant when that helps. If the glossary reaches the
line limit, keep `GLOSSARY.md` as an index and split terms into a
`.spec/glossary/` directory with the same header and `Parent` link.

## INVARIANTS.md

`INVARIANTS.md` captures project-wide obligations that must never be violated,
including security, privacy, cryptographic, data-integrity, and trust-boundary
expectations. It is the highest-priority behavioral contract for an agent.

Use stable IDs and one invariant per entry, with a firm `**Rule.**`, a
`**Rationale.**`, and linked `**Related specs.**` such as
`[§F-12](features/<feature>.md#f-12)`. Use the
[invariant entry template](references/templates.md#invariant-entry-template). An invariant
that should be machine-checked carries `VER-<n>` obligation sub-entries, like a
feature does.

An invariant's `**Rule.**` is firm; do not write an unresolved proposal as an
invariant. Feature-local rules remain in the owning feature file. Adding,
removing, weakening, or materially changing an invariant requires an ADR in the
same change. Never renumber or reuse an invariant ID.

If `INVARIANTS.md` reaches 700 lines, retain it as an index and split the
entries into `.spec/invariants/` topic files with stable IDs and `Parent` links.

## Writing Entries

Entry content follows the rules in [writing.md](references/writing.md). In
short:

- **Requirement levels.** State strength with **must**, **should**, or **may**
  only. Never write "must" for something not decided.
- **Encoded reasoning.** Write an edge case as condition, expected behavior,
  and reason when the reason is not self-evident. Never invent a reason; ask or
  record an open question.
- **Security and privacy.** A project that touches user data, network input,
  credentials, or a trust boundary has a `## Security and Privacy
  Considerations` section in `OVERVIEW.md`.
- **References and open questions.** External standards go under
  `## References` as `### Normative` or `### Informative`. Open questions carry
  the evidence that would settle them and are removed once answered.
- **Technical depth.** Use detail, short pseudocode, or a compact grammar only
  where prose is ambiguous. Never paste implementations, signatures, or types.
- **Algorithms and cryptography.** Name algorithms and parameters that affect
  interoperability or security. Changing one needs an ADR.
- **Performance.** A feature's `**Performance.**` block has one bullet per
  function or operation with its Big-O cost and what `n` counts.

## Testing Expectations

A feature, API route, or invariant states which **kinds** of tests it needs and
what each kind must establish, in a `**Testing.**` block. The implementing agent
then knows what "done" means without guessing, and a reviewer can see when a
kind is missing. The block names kinds and targets, never individual test
names or files, so it stays stable while tests are added, renamed, and moved.

```markdown
**Testing.**
- **property** — printing then parsing any generated syntax tree returns the
  same tree.
- **fuzz** — arbitrary input bytes never panic or hang, and memory stays within
  the input-size bound.
- **golden** — one reviewed diagnostic snapshot per error code.
- **unit** — every edge case above.
```

Use these kinds:

| Kind | Establishes |
|---|---|
| `unit` | One function or module behaves as specified, including its edge cases |
| `integration` | Components work together with real dependencies such as a database or filesystem |
| `end-to-end` | The product behaves correctly through its public surface: CLI, HTTP, or UI |
| `contract` | An API route's request, response, and error contract holds against the running service |
| `property` | A stated property holds over generated inputs |
| `fuzz` | Untrusted input never crashes, hangs, or reaches undefined behavior |
| `golden` | Output matches a reviewed snapshot: rendered text, diagnostics, generated code, serialized formats |
| `differential` | Output matches a reference implementation, an oracle, or a previous version |
| `model-based` | The implementation follows a model's traces |
| `concurrency` | Behavior holds across thread or task interleavings |
| `fault-injection` | Behavior holds under injected network, disk, crash, or clock faults |
| `performance` | A stated `**Performance.**` bound does not regress |
| `visual` | Rendered UI matches reviewed screenshots |
| `accessibility` | UI meets the stated accessibility rules |
| `compile-fail` | Misuse that the API forbids does not compile |

The list is closed. Common names map onto it: snapshot and approval tests are
`golden`; smoke, acceptance, and system tests are `end-to-end`; load, stress,
and benchmark tests are `performance`. Mutation testing measures the tests
rather than the product, so name its tool in `## Verification Strategy`
instead of a `**Testing.**` block.

Rules:

- Each bullet is one kind and the target it must establish. Choose the kinds
  that fit the logic. For example, parsers usually need `property`, `fuzz`,
  `golden`, and often `differential`; state machines need `property` or
  `model-based`; UI needs `visual`, `accessibility`, and `end-to-end`; API
  routes need `contract`. Do not list every kind out of habit.
- Name tools once, in `## Verification Strategy`. Name a tool in a bullet only
  when the feature departs from the project's default for that kind.
- Formal checks are not testing kinds. They are `VER-<n>` obligations per
  [Formal Verification](#formal-verification). Do not list a check twice, once
  as a test and once as an obligation.
- A feature with testable behavior should have a `**Testing.**` block. When
  nothing is worth testing, write `**Testing.** None — <reason>`.
- A feature is `implemented` only when tests of every listed kind exist and
  establish their targets. Implementing a feature includes writing them.
- Removing a kind or weakening its target is a deliberate spec change, with the
  reason given in the change. Never drop one to make work pass.

## Formal Verification

A spec may attach **verification obligations**, `VER-<n>` sub-entries, to a
feature, invariant, or API route. An obligation states a property precisely,
names the kind of tool that must check it, and records the bounds, assumptions,
and link to shipped code that limit what a passing check proves.

Obligations are rare by design, because every artifact must be kept current as
the code under it changes. Attach one only when the property is checkable,
core or critical, failure-prone, and stable enough; never to UI, glue, plain
CRUD, configuration, or I/O plumbing. The essentials:

- **Fields.** `Property`, `Role`, `Tool`, `Scope`, `Bounds`, `Assumptions`, and
  `Obligation` are required; `Model` for a design model, and `Code link` when
  the tool does not check the shipped code.
- **Roles.** `design-model`, `code-check`, `concurrency-check`, `proof`,
  `fault-simulation`, `property-test`, or `delegated`. Prefer the cheapest role
  that gives the needed guarantee.
- **Lifecycle.** `planned` is the default and creates no artifact work until
  the user asks; `required` means an artifact marked `§VER-<n>` exists and
  passes; `waived` links the ADR that explains why.
- **Integrity.** Weakening a property, its bounds, assumptions, or role, or
  demoting an obligation, needs an ADR. Artifacts of a `required` obligation
  never contain unproven steps, narrower assumptions, lowered bounds, or
  skipped checks.

Read [verification.md](references/verification.md), the complete rules, before
adding, promoting, implementing, weakening, or reviewing an obligation;
[example-verification.md](references/example-verification.md) backs it up, and
`/formal-verification` chooses the tool for each role.

## Verification Strategy

`OVERVIEW.md` has a required `## Verification Strategy` section. It states:

- which tool fills each testing kind the project uses, such as `property` →
  proptest, `fuzz` → cargo-fuzz, and `golden` → insta;
- which tool fills each verification role used by this project, and the reason
  for any departure from the defaults in
  [Verification Roles](references/verification.md#verification-roles);
- the project command or check that runs each tool, so `/checks` can find it;
- assumptions that apply to the whole project, such as trusted compilers,
  runtimes, or verified dependencies;
- which verification dependencies are approved under the project's dependency
  policy.

When the project has no obligations yet, the section says so in one line. It
must not repeat individual testing blocks or obligations.

## What Must Not Go In A Spec

- Full implementations, copied source, exact signatures, file tours, line
  numbers, or directory dumps that duplicate the tree.
- Task tracking, plans, TODOs, changelogs, release notes, routine-refactor
  narratives, or test lists; describe the behavior they verify instead.
- Secrets, credentials, tokens, personal paths, hostnames, machine state,
  marketing tone, hedging, or redundant restatements.
- Proof scripts, harnesses, conformance drivers, check results, or lists of
  individual tests. Only design models under `models/` are verification source
  inside `.spec/`; tests and checks cite the spec through `§` markers.
- Unaccepted proposals or design notes. The spec states the current contract;
  a proposal lives in planning notes or project docs until it is accepted, and
  then it updates the spec.
- Code paths or file names, including in `Status`, except stable external
  identifiers such as on-disk paths the product itself reads or writes.

## Splitting And Line Limits

Every spec Markdown file, including the manifest, special files, feature, API
route, and ADR files, and every design model under `models/`, is at most
**700 lines** in total.

When a file approaches or exceeds the limit:

1. Split by ownership or topic, not arbitrary line count.
2. Keep each feature entry and each ADR entry intact.
3. Preserve all IDs and links.
4. Add the required `Parent` header to files under a subdirectory.
5. Update `Spec Map` or the relevant special-file index.
6. Never trim reasoning or compress content merely to fit.

Feature, ADR, and API detail belongs in their existing directories.
`GLOSSARY.md` and `INVARIANTS.md` become indexes when they need topic files. Keep
`OVERVIEW.md` a focused manifest; move detail to the owning area rather than
recreating a monolith. Group large API surfaces with nested route directories,
not multi-route Markdown files.

## IDs And Stability

Feature IDs are `F-<n>`, API route IDs are `API-<n>`, invariant IDs are
`INV-<n>`, verification obligations are `VER-<n>`, open questions are `Q-<n>`,
and ADR IDs are `ADR-<n>`. Assign the next unused number in the relevant
namespace; never reuse a retired ID or renumber an existing entry. Moving an
entry between files keeps its ID.

## Referencing Specs From Code

Implementation cites spec IDs so a reader can get from code to the reasoning:

```rust
// §API-04, §F-04, §INV-02
fn resolve_conflict(local: &Record, remote: &Record) -> Record {
```

A code marker is a comment of comma-separated `§` mentions, using the
language's comment syntax; the sigil already identifies a spec reference.

Every `implemented` or `partial` feature or API route, and every invariant
that code enforces, is cited at least once: at the owning entry point, the
route's handler, or the enforcement point, else from the test that verifies
it. An invariant that links only `planned` features needs no citation yet. An
uncited entry is therefore dead or unimplemented. Beyond this, annotate
edge-case branches and contract tests where the link helps a reader. Do not
annotate every file or line.

Every artifact that discharges a verification obligation carries the
obligation's marker: the proof theorem, the code-check harness, the
concurrency or fault-simulation test, the conformance driver, and the property
inside a design model. This makes obligations traceable mechanically: every
`required` obligation has at least one marked artifact, and every `§VER-<n>`
mention points at an obligation that exists.

```rust
// §VER-7
#[kani::proof]
fn money_checked_add_is_exact() {
```

The reference points one way: code cites the spec; the spec does not cite code
paths, symbols, or line numbers. Obligations therefore name no theorem or
harness identifiers; the artifacts point back to them. A deliberate deviation uses
`// §F-04 (deviation) — <reason>` and is fixed or recorded in the spec and an
ADR when material.

### Keep Citations Out Of What Users See

The spec is the project's own working material, and its users never see it,
so a spec mention of any kind, whether an ID, an ADR, a plan or task number,
or a pointer such as "see the spec", appears only where developers read the
code. Never put one in text the software shows or ships to its users:

- doc comments and module headers that documentation tools, generated API
  docs, editor hover, or `doc`-style commands display;
- CLI help, usage, and version text;
- diagnostics, error, warning, and log messages, and the long explanations
  behind error codes;
- panic, assertion, and `unreachable` messages a user can hit;
- generated files, emitted code, build output and its source maps, and
  headers written into either;
- UI text, API responses, and any skills, templates, or examples the
  software installs or scaffolds.

Put the marker on an internal comment next to the code, inside the body,
above an undocumented helper, or on the test that verifies the contract, and
keep the user-facing text itself free of it. When a contract's citation would
naturally sit on a public item's doc comment, place the marker on a separate
comment that the doc tooling does not attach, such as one inside the item, or
cite it from the test. Where the project can, add a test that fails when
user-facing text contains a spec mention.

## Maintaining A Spec

Update the spec in the same change that makes it stale. `/spec-sync` performs
the full procedure, but an agent working on a project with a spec must not wait for an
explicit sync request when a material decision has been made.

An ADR records a **decision with a real choice**: a direction someone could
reasonably have taken differently, and would need the reasoning to revisit.
Append an ADR in the same change for decisions made by the user or the agent
that:

- change direction, architecture, scope, or a non-goal;
- choose between meaningful alternatives, or reverse an earlier decision;
- add, remove, weaken, or materially change an invariant;
- break compatibility of an API route or other external contract: removing or
  renaming a route or field, changing authentication, or changing what an
  existing client receives;
- change a trust boundary, redaction rule, sensitive-data persistence rule,
  cryptographic suite, algorithm, or interoperability parameter;
- materially loosen a stated performance bound;
- weaken, demote, waive, or remove a verification obligation, per
  [Integrity Rules](references/verification.md#integrity-rules), or change a
  role's tool in `## Verification Strategy`.

Ordinary feature work is not an ADR. Adding a feature, changing behavior, adding
an edge case, adding a backward-compatible route or field, or resolving an open
question with an obvious answer updates the owning entry in place. Write the
reasoning next to the rule, such as an edge case's `Why:`. When in doubt, ask
whether a future reader would need the rejected alternatives; if not, the
feature text is enough.

Do not create ADRs for formatting, routine refactors, dependency updates, or
implementation choices that do not change a contract. If the reason for a
decision is unknown, ask or record the uncertainty; do not invent context.

When a spec is present, normal project work implicitly includes checking the
owning feature or API route, `INVARIANTS.md`, `GLOSSARY.md`, relevant ADR
topic, and the obligations on those entries. Code changes within the scope of a
`required` obligation keep its artifacts current and passing in the same change.
If the behavior itself changes, update the `Property`, and any affected model,
as a spec change. A `planned` obligation creates no artifact work. If the
project has no spec, creating one remains `/spec-init` and requires explicit
approval.

Never store hashes, line numbers, or other code fingerprints in the spec to
detect drift. Drift is computed: the `§` markers link entries to code, and Git
history shows when an entry changed after the code that implements it, or the
other way round. When an entry's normative text changes, re-check every site
that mentions it.

## Quality Checklist

Before finishing spec work, go through the
[quality checklist](references/checklist.md).

See [example-spec.md](references/example-spec.md) for the manifest and links to separated feature, API route, ADR, glossary, and invariant examples, and [example-verification.md](references/example-verification.md) for verification obligations, a design model, and a verification strategy.
