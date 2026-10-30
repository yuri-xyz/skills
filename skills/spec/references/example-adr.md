# ADR File Example

ADR files live under `.spec/adr/`, are grouped by stable topic, and are
append-only after their entries are committed.

```markdown
# Mirrorctl — Security Decisions

> Status: active
> Parent: [OVERVIEW.md](../OVERVIEW.md)

## ADR-0003 — Treat bucket responses as untrusted input <a id="adr-0003"></a>

**Recorded.** 2026-08-19

**Context.** The bucket and network path are outside the trusted workstation;
malformed responses must not corrupt the local plan.

**Decision.** Parse, bound, and validate every remote response before using it
to plan or execute an action.

**Consequences.** Malformed responses fail closed and may require a retry.

**Alternatives considered.** Trusting the provider's schema was rejected
because proxies and compromised endpoints can return unexpected data.

**Related specs.** [§F-02](../features/plan.md#f-02),
[§INV-01](../INVARIANTS.md#inv-01).

**Skills consulted.** `/spec`, `/examples`.

## ADR-0004 — Do not add client-side encryption in v1 <a id="adr-0004"></a>

**Recorded.** 2026-08-19

**Context.** The first release relies on the bucket's at-rest guarantees and
does not define key management or recovery semantics.

**Decision.** Client-side encryption is out of scope until its threat model and
key lifecycle are specified.

**Consequences.** Confidentiality at rest remains a bucket responsibility.
```

If the second decision changes later, append a new `ADR-0005` entry with
`**Supersedes.** [§ADR-0004](#adr-0004)`. Then append the single permitted
back-link line, `**Superseded by.** [§ADR-0005](#adr-0005)`, to the end of
§ADR-0004. Change nothing else in it.
