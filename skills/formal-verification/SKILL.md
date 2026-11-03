---
name: formal-verification
description: Use when deciding whether a property deserves formal verification, or which tool, such as Quint, Kani, shuttle, Lean 4, fault simulation, or property tests, should check it.
---

# Formal Verification

Use this skill when deciding whether some logic should be formally verified,
choosing which kind of check and which tool to use, or writing and reviewing a
verification artifact such as a design model, a bounded-check harness, a
concurrency test, or a proof.

The guidance reflects the ecosystem as of October 2026. Re-check a tool's
maturity and maintenance before relying on it, and add any tool as a dependency
only through the project's dependency policy.

In a project with a `.spec/`, verification is
recorded as `VER-<n>` obligations. Follow `/spec` and its
`references/verification.md` for obligation fields, lifecycle, integrity rules,
and `§VER-<n>` markers; this skill only chooses what to verify and with what.
Record the project's actual tool choices in `OVERVIEW.md` under
`## Verification Strategy`.

## Decide Whether To Verify

Every artifact must be kept passing as the code under it changes, so each one
is a standing maintenance cost. Verify a property only when all of these hold:

- **Checkable.** It can be stated precisely over defined inputs or states, such
  as "for every amount and split count", "in every reachable state", or "for
  every interleaving".
- **Core or critical.** Much of the project depends on it, or a violation loses
  money, data, access control, or user trust.
- **Failure-prone.** It sits where defects usually hide: state machines,
  overflow or rounding arithmetic, parsers of untrusted input, concurrency,
  retries and idempotency, authorization, merge or ordering logic, encodings,
  and `unsafe` code.
- **Stable enough.** The owning behavior has settled.

Do not verify UI, glue, plain CRUD, configuration, or I/O plumbing. When
logic worth verifying is tangled with I/O, extract a pure core and verify that
instead of the handler.

The sweet spot is a **small, critical, self-contained area** with a crisp
property, where ordinary tests sample a huge or tricky input space and a missed
case is costly. Breadth is the wrong target: one verified 50-line core is worth
more than shallow checks across a whole codebase.

### Good Fits

- **Money splitting.** "Splitting an amount across `n` payees never loses or
  creates a cent, for every amount and every `n`." Rounding bugs hide in rare
  inputs; a `code-check` with Kani covers all of them within bounds, or a
  `proof` if it must hold for every `n`.
- **A checked arithmetic or unit-conversion helper** used everywhere, such as
  `Money::checked_add` or a byte-size parser: overflow and truncation are
  exactly what bounded checkers find.
- **A ledger or order state machine.** "Total balance is conserved across
  transfer, hold, release, and reverse, under concurrent retries." A Quint
  `design-model` explores interleavings no test suite would enumerate.
- **An install, update, or migration lifecycle** that must never leave the
  system half-applied after a crash: `design-model` plus `fault-simulation`.
- **A decoder of untrusted input**, such as a binary header parser: "never
  panics, never reads out of bounds, and decode inverts encode."
- **A path sanitizer** guarding a filesystem boundary: "the result never
  escapes the root for any input string."
- **An authorization decision function**: "a revoked grant never allows
  access." Delegate to Cedar when possible.
- **A CRDT merge or sync ordering function**: commutativity, associativity,
  and idempotence must hold for all histories, which suits a `proof`.
- **A lock-free queue or custom lock** in a hot path: `concurrency-check`.
- **Any `unsafe` block**: run Miri at minimum; add Kani when the safety
  argument depends on arithmetic or indexing.

### Poor Fits

- **UI and layout**, such as a settings screen or a button's enabled state.
  Visual and interaction behavior has no crisp property worth a prover; use
  component and snapshot tests.
- **CRUD endpoints and glue** that copy fields between a request and a database
  row. Bugs here are mapping mistakes, better caught by contract tests.
- **Configuration and wiring**, such as a NixOS module, a CI file, or
  dependency-injection setup. Evaluate or build it instead.
- **I/O plumbing**: HTTP clients, file walkers, retries around a network call.
  Extract the decision logic into a pure function and verify that if it is
  critical; leave the plumbing to integration tests.
- **Code that is still changing shape**, such as a prototype or a feature with
  open questions. Artifacts would churn with every edit; record the property
  for later and verify once the design settles.
- **Properties without a precise statement**, like "the ranking feels
  relevant" or "the output looks right". If you cannot write the property as a
  quantified sentence, there is nothing to check.
- **Low-stakes logic** whose failure is obvious and cheap, such as formatting a
  log line or sorting a display list. A unit test is enough.
- **Reimplementing a verified dependency's guarantees**, such as re-proving
  AES or a TLS handshake. Delegate to the verified library and check only how
  you use it.

When in doubt, start with a property test that states the property precisely.
If it keeps finding bugs or the stakes rise, escalate to a checker.

## Choose By Maintenance Cost

The deciding cost is how often an artifact must be reworked as code changes,
not how hard it is to write:

- **Automatic checkers**, such as model checkers and bounded checkers, keep
  only the property statement. When code changes, rerun the check.
- **Interactive proofs** keep the statement and a proof that depends on exact
  definitions. Refactors and prover or library upgrades can break them.
- **What the artifact is tied to** sets how often it breaks. A design model
  breaks only when the design changes, a code-level harness when one function's
  interface changes, and a proof extracted from source on nearly any edit.

So prefer `design-model` and `code-check`, and pick the cheapest role that
gives the needed guarantee. Use `proof` only for small, critical logic where a
bounded check is not enough.

## Roles And Default Tools

| Role | Checks | Default | Escalate or substitute when |
|---|---|---|---|
| `design-model` | A model of states and transitions, not the code | **Quint** | **TLA+** when the model mostly needs liveness or fairness ("eventually"), refinement mappings, or TLAPS proofs. **Alloy** for structural or relational models such as permission graphs and schema constraints. |
| `code-check` (Rust) | The shipped code, for every input within the bounds | **Kani**, optionally through **bolero** so one harness runs as a property test, a fuzz target, or a Kani proof | Add Kani function or loop contracts when a property must hold beyond the unwinding bound. **ESBMC** is an alternative bounded checker. |
| `code-check` (C/C++) | As above | **CBMC** | **ESBMC**. |
| `code-check` (other languages) | As above | No mature default. Use `property-test` and state that the guarantee is sampled | **Dafny** for a small critical piece that can be written, proven, and compiled into the target language. |
| `concurrency-check` | Real concurrent code across interleavings | **shuttle** (randomized, scales, replays failures exactly) | **loom** for tiny lock-free primitives that need every interleaving explored. |
| `proof` | A property for every input size, with no bound | **Lean 4**, with definitions as an executable reference and differential property tests against the shipped code | **Aeneas** (Rust to Lean) only for frozen, high-assurance code. **Verus** when unbounded proofs must live inside the Rust code and a high proof-to-code ratio is acceptable. **Dafny** when the proven code itself should ship. |
| `fault-simulation` | Real code under injected network, disk, crash, and clock faults | **turmoil** | **madsim** when full determinism of time and randomness matters. |
| `property-test` | Sampled inputs only; a stand-in when no mature checker exists or can be approved | **proptest** for Rust, **fast-check** for TypeScript, **rapid** for Go | — |
| `delegated` | Discharged by an upstream component that is itself verified | **Cedar** for authorization policy. **aws-lc-rs** for cryptographic primitives | **libcrux** for its hax-verified post-quantum algorithms once it leaves pre-release. |

Use `property-test` as a stand-in only when the checker cannot be installed
under the dependency policy, not merely because the distribution lacks a
package; moving to the checker later is a strengthening.

Supporting tools that are not roles:

- **Miri** detects undefined behavior in `unsafe` Rust at test time. Run it
  wherever `unsafe` exists; it needs no maintenance.
- **Kani `cover!`** and **Quint witnesses** show that the interesting states
  are reachable, so a passing check is not vacuous.
- **cargo-mutants** checks whether the properties catch injected defects. Run
  it periodically, not on every change.

Per-tool notes, including how to pin Kani in a Nix project, are in
[references/tools.md](references/tools.md).

## Candidate Patterns

Typical choices by kind of logic:

- **State machines and workflows** (orders, ledgers, install or update
  lifecycles, session states): `design-model` with trace conformance. See
  `/pattern-state-machine` for keeping the transition logic pure.
- **Retries, idempotency, and crash recovery:** `design-model`, plus
  `fault-simulation` for distributed or I/O-heavy cores.
- **Money, units, and overflow-prone arithmetic:** `code-check`.
- **Parsers and decoders of untrusted input:** `code-check` for panic freedom
  and round trips within bounds.
- **Path and input sanitization:** `code-check`.
- **Merge, sync, and ordering laws** (commutativity, associativity,
  idempotence, total order): `proof` when the laws must hold for all histories.
- **Rounding and allocation that must hold for every count:** `proof`.
- **Authorization decisions:** `delegated` to Cedar when possible; otherwise
  `code-check` on a pure decision function.
- **Cryptography:** `delegated` to verified libraries. Verify how primitives
  are used and composed, never reimplemented primitives. Protocol security
  needs dedicated tools such as Tamarin or ProVerif and is out of scope by
  default; see `/cryptography`.
- **Lock-free structures and custom synchronization:** `concurrency-check`.

## Linking Results To Shipped Code

A check that does not run against the shipped code proves something about a
model or a reference definition. Connect it to the code:

- **Design models:** replay traces from simulation or model checking (Quint's
  ITF format) against the implementation's pure transition logic. Keep the
  replay adapter thin so only it changes when the code is refactored.
- **Proofs:** treat the proof's definitions as an executable reference and run
  differential property tests against the implementation. Extraction from
  source, such as Aeneas, is stronger but breaks on most edits; use it only for
  effectively frozen code. Code compiled from the proof, as with Dafny, needs
  no extra link.
- `code-check`, `concurrency-check`, `fault-simulation`, and `property-test`
  already run against the shipped code.

## Keep Checks Honest

A check is only as strong as its stated property, bounds, and assumptions:

- State every bound (unwinding, state-space limits, input sizes, thread counts)
  and every assumption (storage semantics, clocks, trusted compilers or
  dependencies) next to the property.
- Never leave unproven steps (`sorry`, `admit`, new `axiom`, Dafny `assume`),
  add narrower input assumptions (such as a new `kani::assume`), lower bounds,
  skip or quarantine the check, or restate the property more weakly to make it
  pass. Fix the code or report the gap.
- Add a reachability check, such as Kani `cover!` or a Quint witness. For a
  property test, assert that generators produce every outcome the property
  distinguishes, such as accepted and refused inputs, at a stated minimum rate,
  and weight the generators until they do.
- Before relying on a check, break each clause of the property in turn, by hand
  or with `cargo-mutants`, and confirm the check fails. Then restore the code
  and delete failure seeds the deliberate defects left behind, such as
  `proptest-regressions` entries.
- For Lean, review the theorem statement, not the proof; the kernel checks the
  proof.
- Wire each tool into the project's checks (for example a `just verify` recipe)
  so `/checks` can run it.
