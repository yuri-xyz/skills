# Spec — Writing Entries

This reference is the normative part of the [spec standard](../SKILL.md)
that governs how entry content is written: requirement strength, encoded
reasoning, security, references, open questions, technical depth, algorithms,
and performance. Read it when writing or reviewing entry content.

## Requirement Levels

Every statement carries a strength. Make it explicit wherever the strength is
not obvious, using three words and nothing else:

- **must** — inviolable; deviating is a bug and a deliberate deviation needs an
  ADR and a spec annotation.
- **should** — the default expectation; deviation needs a stated reason at the
  deviation site.
- **may** — real latitude; the implementation chooses.

Never write "must" for something not actually decided. That is an open question
or an ADR proposal, not a requirement.

## Edge Cases And Encoded Reasoning

Write an edge case as a condition, expected behavior, and reason when the reason
is not self-evident, for example: empty HTTP 200 → retry as transport failure;
the CDN's failover response previously looked like an empty dataset.

Never invent a reason. If the rule exists but its rationale is unknown, ask or
record the uncertainty under `## Open Questions`; an invented reason outlives
the code that prompted it.

## Security And Privacy Considerations

When the project touches user data, network input, credentials, secrets, or a
trust boundary, `OVERVIEW.md` has a first-class `## Security and Privacy
Considerations` section. Address briefly and specifically:

- **Trust boundary.** What is trusted, what is not, and where the boundary sits.
- **Attacker-controlled input.** Which inputs are hostile and how they are
  bounded, validated, or refused.
- **Credentials and secrets.** How they enter, where they may persist, what is
  never logged, and how rotation or revocation works when in scope.
- **Logging and telemetry.** What is recorded, redacted, or prohibited from
  leaving the machine.
- **Persistence.** What is stored, for how long, and who can read it.
- **Deliberate non-defenses.** Threats the project explicitly does not address.

Feature-local security rules stay with the feature. Cryptographic algorithms and
their non-negotiable security expectations belong in the feature and/or
`INVARIANTS.md`, with the project-wide threat model in the manifest.

## References

When a feature or contract conforms to an external standard, list it under
`## References` rather than restating foreign semantics. Split references into
`### Normative` and `### Informative`, and link the specific section when one
exists. A normative reference constrains local prose; a conflict is a bug until
the local spec is deliberately updated.

## Open Questions

Record unresolved matters with the evidence that would settle them, such as
`§Q-02` asking whether old offline edits are discarded or archived and naming the
queue-age measurement that would answer it.

Remove a question when answered and move the answer into the owning feature,
invariant, or a new ADR. Do not leave a resolved question as stale task text,
and do not keep a `## Resolved Questions` section.

## Technical Depth, Pseudocode, And Grammars

Use detail for ambiguous ordering, state transitions, protocol shapes, retries,
timeouts, data lifetimes, failure semantics, and boundary contracts. Use short,
language-neutral pseudocode or a compact ABNF-like grammar only when prose is
insufficient; omit grammar for an existing standard with no local productions.
Do not paste implementations, signatures, types, or file contents; name stable
external identifiers such as flags, routes, wire fields, or on-disk paths. A
function name is allowed only as the narrow label of a feature-local performance
bullet.

## Algorithms And Cryptography

Name the specific algorithm and parameters that affect interoperability or
security: `AES-256-GCM`, `XChaCha20-Poly1305`, `Ed25519`, `X25519`,
`HKDF-SHA-256`, `Argon2id (m=64 MiB, t=3, p=1)`, `SHA-256`, and so on. For
cryptography, state construction role, key wrapping, domain separation, nonce
rules, tag lengths, limits, and wire algorithm identifiers when they matter.

Prefer standardized, reviewed constructions. Do not invent a novel cipher mode,
signature scheme, KDF, or hybrid by combining primitives ad hoc. Changing a
pinned algorithm or interoperability parameter is a spec change and requires an
ADR; it must not happen quietly.

## Performance Expectations

Keep performance focus in a dedicated `**Performance.**` mini-section on the
owning feature entry. Scope each bullet to the relevant function or operation,
not to a global performance chapter:

```markdown
**Performance.**
- **plan.** O(n log n) in n = files under the local root; memory stays O(1) in n.
- **compare manifests.** O(n) in n = remote entries; one list request per page.
```

Rules:

- Use one bullet per relevant function or operation, and name what `n` counts.
- State the cost that matters: CPU, memory, allocations, network round trips,
  filesystem syscalls, database queries, or re-render counts.
- Add a concrete budget only when it is user-visible or contractual, including
  the conditions under which it holds.
- State observable cost, not the data structure or other implementation that
  happens to achieve it.
- Record why the bound exists when it was earned by a regression, incident,
  benchmark, or explicit product constraint.
- Omit the block only when performance is not meaningful or not at risk. Do not
  turn every trivial function into a table of `O(1)` claims.

Only write a bound that every future implementation should preserve. A material
change to a stated bound is a spec change and, when it reflects a durable
decision, gets an ADR.
