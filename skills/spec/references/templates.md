# Spec Templates

Use these templates for consistent files under `.spec/features/`, `.spec/api/`,
and `.spec/adr/`, and for verification obligation sub-entries. Create
`.spec/api/` only for projects with an API service. Replace placeholders, keep
stable IDs, and remove optional blocks that carry no information. An API
Markdown file documents one route operation; if a field is not applicable,
write `None` rather than silently omitting a required contract.

## Feature File Template

```markdown
# <Project> — <Feature Area>

> Status: active
> Parent: [OVERVIEW.md](../OVERVIEW.md)

## Features

### F-12 <Feature name> <a id="f-12"></a>

**Intent.** <What this feature accomplishes and why it exists.>

**Behavior.**
- <Observable behavior stated in the present tense.>
- <Ordering, failure, persistence, or boundary rule.>

**Edge cases.**
- <Condition> → <expected behavior>. Why: <earned rationale, when non-obvious>.

**Constraints.** <Hard implementation boundary, if applicable.>

**Current boundary.** <Only when Status is `partial`: which parts of the
behavior are not yet satisfied.>

**Performance.**
- **<function or operation>.** <Big-O cost; define what `n` counts. Include
  memory, I/O, or a concrete budget when it is load-bearing.>

**Testing.**
- **<kind>** — <what tests of this kind must establish.>

**Depends on.** [§F-08](../features/<dependency>.md#f-08),
[§INV-03](../INVARIANTS.md#inv-03).

**Related specs.** [§ADR-0007](../adr/<topic>.md#adr-0007).

**Skills.** `/examples` — interpret the product example used by this contract.

**Status.** planned

## References

### Normative

- [<standard section>](<url>) — <local contract it constrains>.
```

Keep one feature per entry. `Intent`, `Behavior`, and `Status` are required;
`Status` is `planned`, `partial`, or `implemented`, and `Current boundary` is
required exactly when it is `partial`. `Testing` names test kinds and their
targets, not individual tests, and is expected whenever the feature has
testable behavior. The other blocks are conditional. When performance is load-bearing, use one
`**Performance.**` bullet per relevant function or operation and define every
Big-O input. Use `[§F-12](#f-12)` for a same-file link and
the relative path form above for a cross-file link.

## Verification Obligation Template

Place obligations one heading level below the owning feature, invariant, or API
route entry, after the owner's other blocks. Inside a feature file:

```markdown
#### VER-3 — <Property title> <a id="ver-3"></a>

**Property.** <Firm, quantified statement in domain terms: for every ..., ...>

**Role.** <design-model | code-check | concurrency-check | proof |
fault-simulation | property-test | delegated>

**Tool.** <Quint | Kani | shuttle | Lean 4 | ...>

**Scope.** <State machine, operation, or function label the check covers.>

**Bounds.** <Every state-space, unwinding, size, or thread limit, or
`Unbounded`.>

**Assumptions.** <What the check takes as given, or `None`.>

**Model.** [<area>.qnt](../models/<area>.qnt)

**Code link.** <How the result reaches shipped code: trace conformance,
differential tests against an executable reference, or `none needed (shipped
from the proof)`.>

**Rationale.** <Why this property is a candidate, when not obvious.>

**Obligation.** planned
```

`Property`, `Role`, `Tool`, `Scope`, `Bounds`, `Assumptions`, and `Obligation`
are required. `Model` is required for `design-model`. `Code link` is required
when the tool does not check shipped code, which applies to `design-model` and
usually to `proof`. `Obligation` is `planned`, `required`, or
`waived — [§ADR-0009](../adr/<topic>.md#adr-0009)`. Link an obligation like
any other ID, such as `[§VER-3](../features/<feature>.md#ver-3)`.

## Invariant Entry Template

```markdown
### INV-03 — <Rule title> <a id="inv-03"></a>

**Rule.** <Firm, project-wide obligation that must never be violated.>

**Rationale.** <Why it exists: the incident, threat, or property it protects.>

**Related specs.** [§F-12](features/<feature>.md#f-12),
[§ADR-0007](adr/<topic>.md#adr-0007).
```

`Rule` and `Rationale` are required. An invariant that must be machine-checked
adds `VER-<n>` obligation sub-entries after its blocks.

## Glossary Entry Template

```markdown
### <Term> <a id="<term-slug>"></a>

**Definition.** <What the term means in this project.>

**Not to be confused with.** <Nearby meanings or terms it excludes.>

**Related specs.** [§F-12](features/<feature>.md#f-12).
```

`Definition` is required. Glossary terms have no ID, so the heading carries an
explicit kebab-case anchor, initially the heading's slug, such as
`<a id="sub-spec"></a>` for `### Sub-spec`. Links target it, and it stays
when the term is renamed.

## API Route File Template

```markdown
# <Project> — API <Operation summary>

> Status: active
> Parent: [OVERVIEW.md](../OVERVIEW.md)

## API-001 — POST /v1/users <a id="api-001"></a>

**Method.** `POST`

**Path.** `/v1/users`

**Operation ID.** `createUser`

**Intent.** <What this route enables and why it exists.>

**Behavior.** <What the handler accepts, handles, changes, or returns. State
observable ordering, side effects, and failure behavior.>

**Authentication.** <Required or `Public`; credential type and unauthenticated
failure response.>

**Authorization.** <Required actor, scopes, roles, ownership, or `None`.>

**Incoming data validation.**
- <Required headers, path/query parameters, and body fields.>
- <Type, size, format, cross-field, duplicate, and unknown-field rules.>
- <Reject or normalize malformed, missing, oversized, or untrusted input.>

**Rate limiting.** <Policy, identity/key, window, response, and retry guidance;
write `None` only when the route has no limit.>

**Request.** <Parameters, content type, body shape, and idempotency key rules.>

**Responses.**
- `201` — <success body, headers, and persistence/side-effect result>.
- `400` — <validation failure shape>.
- `401` / `403` — <authentication/authorization failure shape, when applicable>.
- `429` — <rate-limit failure shape, when applicable>.

**Errors.** <Stable error codes, redaction, retryability, and status mapping.>

**Edge cases.**
- <Incoming-data condition> → <expected response and state change>. Why: <reason>.
- <Replay, duplicate, timeout, dependency, or partial-failure condition> → <behavior>.

**Testing.**
- **contract** — <the request, response, and error contract above holds
  against the running service.>
- **<kind>** — <other target, such as integration with real storage.>

**Depends on.** [§F-12](../features/<feature>.md#f-12),
[§INV-03](../INVARIANTS.md#inv-03).

**Related routes.** [§API-002](auth/sign-in.md#api-002).

**Related specs.** [§ADR-0007](../adr/<topic>.md#adr-0007).

**Skills.** `/examples` — preserve the relevant contract pattern.

**Status.** planned

## References

### Normative

- [OpenAPI <version>, <section>](<url>) — <local contract it constrains>.
- [Machine-readable API description](<path-or-url>) — <source, if one exists>.
```

`Method`, `Path`, `Operation ID`, `Intent`, `Behavior`, `Authentication`,
`Authorization`, `Incoming data validation`, `Rate limiting`, `Request`,
`Responses`, `Edge cases`, and `Status` are required. `Errors`, dependencies,
related routes/specs, skills, and references are conditional, but include them
when they carry contract or rationale. Use `[§API-001](#api-001)` for a same-file
link; from a feature or root special file, link the route with its path, such as
`[§API-001](../api/users.md#api-001)` or `[§API-001](api/users.md#api-001)`.
For a route nested below `.spec/api/`, adjust every relative link to its actual
location: the `Parent`, feature, invariant, and ADR links gain the needed
`../` segments, while related-route links use the shortest valid route path.

## ADR File Template

```markdown
# <Project> — <Decision Topic>

> Status: active
> Parent: [OVERVIEW.md](../OVERVIEW.md)

## ADR-0007 — <Decision title> <a id="adr-0007"></a>

**Recorded.** YYYY-MM-DD

**Context.** <Problem, constraints, evidence, and the rejected direction that
led to this decision.>

**Decision.** <What was decided, stated precisely enough to guide future work.>

**Consequences.** <Important benefits, costs, and new constraints.>

**Alternatives considered.** <Meaningful alternatives and why they lost.>

**Supersedes.** [§ADR-0003](../adr/<topic>.md#adr-0003)
<!-- or, for a partial change: **Amends.** [§ADR-0003](...) -->

**Retires.** §F-9, §INV-04
<!-- IDs of entries this decision deletes; bare mentions, since the entries no
     longer exist. Omit when nothing is removed. -->

**Related specs.** [§F-12](../features/<feature>.md#f-12),
[§INV-03](../INVARIANTS.md#inv-03).

**Skills consulted.** `/spec`, `/examples`.
```

`Recorded`, `Context`, and `Decision` are required. `Retires` lists the IDs of
deleted entries; the IDs are never reused, and older ADRs may keep linking them.
If entries were deleted before a spec used `Retires`, append one ADR whose
`Retires` field names them. Append newer records at the
end of the topic file. Use `Supersedes` from a new record when a decision
changes, or `Amends` when it changes only part of one. In the same change,
append one back-link line to the end of the older record, which is the only
permitted edit to a committed ADR:

```markdown
**Superseded by.** [§ADR-0007](../adr/<topic>.md#adr-0007)
```

Use `**Amended by.**` for a partial change. Never edit an earlier record in any
other way.
