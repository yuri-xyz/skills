# Spec — Formal Verification

This reference is the normative part of the [spec standard](../SKILL.md)
that governs verification obligations. Read it before adding, promoting,
implementing, weakening, or reviewing an obligation.

A spec may attach **verification obligations** to a feature, invariant, or
API route. An obligation states a property precisely, names the kind of tool
that must check it, and records the bounds, assumptions, and link to shipped
code that limit what a passing check proves. It tells an implementing agent
that a written rule is not enough for this property: a machine-checked
artifact is expected, now or later.

Obligations are rare by design. Most behavior stays in prose and ordinary
tests. Verification artifacts must be updated whenever the code under them
changes, so each obligation is a standing maintenance cost; spend it only where
a defect would be expensive.

## Selecting Candidates

Attach an obligation only when **all** of these hold:

- **Checkable.** The property can be stated precisely over defined inputs or
  states, such as "for every amount and every split count", "in every reachable
  state", or "for every interleaving".
- **Core or critical.** Much of the project depends on it, or a violation loses
  money, data, access control, or user trust.
- **Failure-prone.** It is where defects usually hide: state machines,
  arithmetic with overflow or rounding, parsers of untrusted input, concurrency,
  retries and idempotency, authorization decisions, merge or ordering logic,
  encodings, and `unsafe` code.
- **Stable enough.** For `required`, the owning behavior has settled and has
  few open questions. A `planned` obligation may be recorded earlier.

Do not attach obligations to UI, glue, plain CRUD, configuration, or I/O
plumbing. When logic worth verifying is tangled with I/O, the owning feature
should require a pure core so the property stays checkable; verify the core,
not the handler.

## Obligation Entries

Each obligation is a sub-entry one heading level below its owning feature,
invariant, or API route entry, placed after the owner's other blocks:

```markdown
#### VER-3 — Transfers conserve total balance <a id="ver-3"></a>

**Property.** For every reachable ledger state and every transfer, reversal, or
rejected transfer, the sum of all account balances is unchanged.

**Role.** design-model

**Tool.** Quint

**Scope.** Ledger state machine: transfer, hold, release, reverse.

**Bounds.** ≤ 3 accounts, ≤ 2 concurrent clients, ≤ 8 steps.

**Assumptions.** Storage is linearizable; a retried request reuses its
idempotency key.

**Model.** [ledger.qnt](../models/ledger.qnt)

**Code link.** Trace conformance: model traces replay against the ledger
transition function in project tests.

**Rationale.** Double-spend under concurrent retries is the costliest ledger
failure.

**Obligation.** planned
```

`Property`, `Role`, `Tool`, `Scope`, `Bounds`, `Assumptions`, and `Obligation`
are required. `Model` is required for the `design-model` role. `Code link` is
required whenever the tool does not check the shipped code itself. `Rationale`
is optional; include it when the obligation was earned by an incident or is not
obviously a candidate. Use the
[verification obligation template](templates.md#verification-obligation-template).

- **Property** is a firm, quantified statement of what holds, written in the
  domain's terms. It is the contract. Tool syntax, theorem names, and harness
  names do not belong here.
- **Scope** names the state machine, operation, or function the check covers.
  As in a performance block, a function name may appear as a narrow label.
- **Bounds** states every limit on the check, such as state-space limits, loop
  unwinding, input sizes, or thread counts, or says `Unbounded`.
- **Assumptions** lists what the check takes as given and does not prove, such
  as storage semantics, clock behavior, a trusted dependency, or a compiler or
  runtime. Write `None` only when that is true.

## Verification Roles

`Role` names what kind of guarantee the obligation needs. `Tool` names the
concrete tool. Use one of these roles:

| Role | Checks | Default tool |
|---|---|---|
| `design-model` | A model of states and transitions, not the code | Quint |
| `code-check` | The shipped code, for every input within the bounds | Kani for Rust |
| `concurrency-check` | Real concurrent code across interleavings | shuttle; loom for tiny primitives |
| `proof` | A property for every input size, with no bound | Lean 4 |
| `fault-simulation` | Real code under injected network, disk, crash, and clock faults | turmoil or madsim |
| `property-test` | Sampled inputs only; a stand-in when no mature checker exists for the language | the project's property-test library |
| `delegated` | Discharged by an upstream component that is itself verified | the named dependency |

Prefer the cheapest role that gives the needed guarantee. A bounded
`code-check` is preferred over a `proof` whenever a bound is acceptable for the
property, because an automatic checker leaves only the property to maintain,
while a proof also has to be kept working as the code changes. Use `proof` only
for small, self-contained, critical logic that must hold for every input size,
and give it a cheap code link. Per-role tool guidance, alternatives for other
languages, and escalation options are in `/formal-verification`.

A `property-test` obligation must say in `Assumptions` that the guarantee is
sampled, not exhaustive. It stands in for a checker only when the checker
cannot be installed under the project's dependency policy, not merely because
the distribution has no package for it; `## Verification Strategy` records that
departure, and moving to the checker later is a strengthening. A `delegated`
obligation names the dependency and the
upstream verification it relies on, and its `Code link` names the integration
check showing the project uses that component as verified.

## Linking Checks To Shipped Code

A check that does not examine the shipped code proves something about a model
or a reference definition. Its `Code link` must say how that result reaches the
code:

- **design-model.** Trace conformance. Traces from the model, from simulation
  or from model checking, replay against the implementation's pure transition
  logic. Keep the replay adapter thin so that only the adapter changes when the
  code is refactored.
- **proof.** By default, the proof's definitions are an executable reference
  and differential property tests compare them against the implementation.
  Extracting proof definitions from source, for example Rust to Lean with
  Aeneas, gives a stronger link but breaks on most code changes; use it only
  for code that is effectively frozen. When the proven code itself is compiled
  into the product, as with Dafny, write `Code link: none needed (shipped from
  the proof)`.
- **code-check, concurrency-check, fault-simulation, property-test.** These run
  against the shipped code. Omit `Code link`.

## Obligation Lifecycle

`Obligation` is exactly one of:

- **planned** — the property is stated and a check is expected eventually. An
  agent must not implement the check unless the user asks. Code changes should
  keep the property checkable, for example by keeping the logic pure, but need
  no artifact. This is the default for a new obligation.
- **required** — the artifact must exist, carry its `§VER-<n>` marker, and pass in
  the project's checks. A change to code within the obligation's scope must keep
  the artifact passing without weakening it, in the same change.
- **waived** — the property is deliberately not checked. Write
  `waived — [§ADR-<n>](...)`; the ADR records why.

Promote `planned` to `required` only when the user asks, either for named
obligations or as a stabilization pass over the spec. During a pass, re-judge
each candidate against [Selecting Candidates](#selecting-candidates),
especially stability, and present the shortlist before implementing it.
Promotion is a status change like a feature's `Status` and needs no ADR.

The spec never records whether a check currently passes; the project's checks
decide that. `required` means "must exist and pass", not "has passed".

## Integrity Rules

A verification artifact is only as strong as its stated property, bounds, and
assumptions. Each of the following is a spec change that requires an ADR in the
same change:

- weakening or narrowing a `Property`;
- shrinking `Bounds` or adding to `Assumptions`;
- moving to a weaker role, such as `proof` to `code-check` or `code-check` to
  `property-test`;
- demoting `required` to `planned` or `waived`, or removing an obligation.

Within artifacts for a `required` obligation, an agent must not:

- leave an unproven step in a proof, such as Lean's `sorry`/`admit` or a new
  `axiom`, or Dafny's `assume`;
- add input assumptions narrower than the obligation's stated `Assumptions`,
  such as a new `kani::assume`;
- lower unwinding limits, state-space bounds, or iteration counts below the
  stated `Bounds`;
- skip, ignore, or quarantine the check, or catch its failure;
- restate the checked property in a weaker form than the `Property` text.

A `required` check should also include a reachability check, such as Kani
`cover!`, a Quint witness, or an equivalent, showing that the interesting states
are reachable under the stated assumptions. A check that passes because nothing
interesting is reachable is vacuous. A property test has no `cover!`; assert
instead that its generators produce every outcome the property distinguishes,
such as accepted and refused inputs, at a stated minimum rate, and record that
rate in `Bounds`. Independent random fields rarely line up into the accepting
case, so weight the generators until they do.

Before promoting an obligation to `required`, confirm that the artifact fails
when the code is wrong: break each clause of the property in turn, by hand or
with `cargo-mutants`, and check that the artifact fails each time. Then restore
the code and delete any failure seeds the deliberate defects left behind, such
as `proptest-regressions` files, since they record defects the code never had.

## Design Models

`.spec/models/` holds design models. These are spec content: they describe
intended behavior, not implementation. Name files by area in kebab-case with the
tool's extension, such as `ledger.qnt` or `install-lifecycle.qnt`. Each model
starts with a comment header naming its parent, and marks each
property it checks with the owning obligation ID:

```quint
// Parent: OVERVIEW.md
module ledger {
  // §VER-3
  val totalConserved = ...
}
```

Models follow the 700-line limit; split them by area. A model changes when the
behavior it describes changes, not when code is refactored. Proofs, harnesses,
and conformance drivers are code and live in the code tree, not in `.spec/`.
