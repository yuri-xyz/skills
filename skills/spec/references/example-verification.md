# Verification Example

This example shows verification obligations for a small ledger service
written in Rust. It shows one obligation for each common role, a design model,
the manifest's verification strategy, and the `§` markers on artifacts.
Only the verification-specific parts are shown. Headers and other blocks follow
[example-spec.md](example-spec.md).

## `OVERVIEW.md` — `## Verification Strategy`

```markdown
## Verification Strategy

- **Testing kinds.** `unit`, `integration`, and `contract` use the Rust test
  harness; `property` uses proptest. All run by `just test`.
- **design-model.** Quint, run by `just verify-models`. Trace conformance uses
  an in-repo replayer for Quint's trace format.
- **code-check.** Kani through bolero harnesses, run by `just verify`; the same
  harnesses run as property tests in `just test`.
- **proof.** Lean 4, run by `just verify-proofs`. Lean definitions are
  executable references, checked against Rust by differential property tests.
- **Project-wide assumptions.** The Rust compiler, the Lean kernel, and
  PostgreSQL's serializable isolation are trusted.
- **Approved verification dependencies.** bolero.
```

## `features/transfers.md`

````markdown
### F-04 Transfer <a id="f-04"></a>

**Intent.** Move money between two accounts of the same currency exactly once
per client request.

**Behavior.**
- A transfer debits the source and credits the destination atomically.
- A transfer that would make the source negative is rejected with no effect.
- A request whose idempotency key was already applied returns the original
  result and changes nothing.

**Testing.**
- **integration** — concurrent requests with the same idempotency key apply
  exactly one transfer against real storage.
- **contract** — a rejected transfer returns its documented error and changes
  no balance.

Formal checks for this feature are the obligations below, not testing kinds.

**Depends on.** [§INV-02](../INVARIANTS.md#inv-02).

**Status.** implemented

#### VER-1 — Transfers conserve total balance <a id="ver-1"></a>

**Property.** For every reachable ledger state and every applied, rejected, or
retried transfer, the sum of all account balances is unchanged.

**Role.** design-model

**Tool.** Quint

**Scope.** Ledger state machine: transfer and retry.

**Bounds.** 3 accounts, 2 concurrent clients, 8 steps.

**Assumptions.** Storage is serializable; a retried request reuses its
idempotency key.

**Model.** [ledger.qnt](../models/ledger.qnt)

**Code link.** Trace conformance: model traces replay against the ledger
transition function.

**Rationale.** A double-applied retry is the costliest ledger failure.

**Obligation.** required

#### VER-2 — Amount arithmetic is exact <a id="ver-2"></a>

**Property.** For every pair of amounts, checked addition and subtraction
return the exact result or report overflow, and never panic or wrap.

**Role.** code-check

**Tool.** Kani

**Scope.** Amount type: checked add, checked subtract.

**Bounds.** All 64-bit signed inputs; no loops.

**Assumptions.** None.

**Obligation.** required

#### VER-3 — Fee splits are exact <a id="ver-3"></a>

**Property.** For every amount and every positive split count, the split parts
sum exactly to the amount and differ from each other by at most one minor unit.

**Role.** proof

**Tool.** Lean 4

**Scope.** Fee split.

**Bounds.** Unbounded.

**Assumptions.** None.

**Code link.** The Lean split definition is the executable reference;
differential property tests compare it with the Rust split.

**Rationale.** Must hold for every split count, so a bounded check is not
enough.

**Obligation.** planned
````

## `INVARIANTS.md`

```markdown
### INV-02 — Authorization denies by default <a id="inv-02"></a>

**Rule.** A request is denied unless at least one policy explicitly permits it,
and any matching forbid policy denies it.

**Rationale.** An authorization gap exposes every account.

#### VER-4 — Policy evaluation is verified upstream <a id="ver-4"></a>

**Property.** For every request and policy set, evaluation denies unless a
permit matches and no forbid matches.

**Role.** delegated

**Tool.** Cedar

**Scope.** Authorization decisions for every API route.

**Bounds.** Unbounded (upstream proofs).

**Assumptions.** Cedar's Lean-verified semantics match its Rust evaluator, as
established upstream by differential testing.

**Code link.** Integration tests check that every route sends its decision to
the Cedar evaluator and maps a deny to `403`.

**Obligation.** required
```

## `models/ledger.qnt`

```quint
// Parent: OVERVIEW.md
module ledger {
  pure val ACCOUNTS = Set("alice", "bob", "carol")
  pure val TOTAL = 300

  var balances: str -> int

  action init = balances' = ACCOUNTS.mapBy(_ => 100)

  action transfer(src: str, dst: str, amount: int): bool = all {
    src != dst,
    amount > 0,
    balances.get(src) >= amount,
    balances' = balances
      .set(src, balances.get(src) - amount)
      .set(dst, balances.get(dst) + amount),
  }

  action step = {
    nondet src = ACCOUNTS.oneOf()
    nondet dst = ACCOUNTS.oneOf()
    nondet amount = 1.to(TOTAL).oneOf()
    transfer(src, dst, amount)
  }

  // §VER-1
  val totalConserved = ACCOUNTS.fold(0, (sum, a) => sum + balances.get(a)) == TOTAL
}
```

A real model also covers retries, idempotency keys, and concurrent clients
within the stated bounds.

## Artifacts In The Code Tree

```rust
// §VER-2
#[test]
#[cfg_attr(kani, kani::proof)]
fn amount_checked_add_is_exact() {
    bolero::check!()
        .with_type::<(i64, i64)>()
        .for_each(|&(a, b)| {
            let expected = (a as i128) + (b as i128);
            match Amount::new(a).checked_add(Amount::new(b)) {
                Some(sum) => assert_eq!(sum.minor_units() as i128, expected),
                None => {
                    // Reachability: the overflow branch is not vacuous.
                    #[cfg(kani)]
                    kani::cover!(true, "overflow is reachable");
                    assert!(expected > i64::MAX as i128 || expected < i64::MIN as i128);
                }
            }
        });
}
```

`§VER-1`'s trace-conformance driver carries `// §VER-1` in the same way.
`§VER-3` is `planned`, so it has no artifact yet. When it is promoted, its Lean
theorem and differential test both carry `§VER-3`, and neither may contain
an unproven step such as `sorry`.
