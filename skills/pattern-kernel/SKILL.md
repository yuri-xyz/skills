---
name: pattern-kernel
description: Use when designing, extracting, or reviewing code whose bugs could lose or corrupt data, leak secrets, grant unauthorized access, or misstate money, such as auth, sessions, balances, ledgers, cryptography, key custody, encryption formats, sync, replication, or backups, and that logic should live in a small, pure, auditable, verifiable trusted kernel. For the lifecycle model inside the kernel use /pattern-state-machine, and for choosing verification tools use /formal-verification.
---

# Pattern: Trusted Kernel

## Objective

Isolate the decisions whose bugs would be catastrophic into a small trusted
kernel: a pure, synchronous, dependency-light module that owns those decisions
and nothing else. Everything around it is an untrusted shell that gathers
inputs, carries out the kernel's verdicts, and reports outcomes back. The
kernel stays small and stable enough to audit in one sitting and to check
with model checking, bounded proofs, and property tests, so confidence comes
from evidence rather than from reading the whole application.

This is a functional-core, imperative-shell split with a security boundary
drawn around the core. Lifecycles inside the kernel are explicit state
machines (`/pattern-state-machine`); the kernel is where those machines live
when their transitions guard something critical.

## Recognize the fit

Use a kernel when most of these hold:

- A logic bug, not just an outage, could lose or corrupt durable data, leak
  plaintext or keys, authorize the wrong principal, double-spend or misstate a
  balance, or make a backup unrestorable.
- The critical rules are a small fraction of the code and are currently mixed
  with I/O, async, retries, UI, or protocol plumbing.
- The rules have stable invariants worth naming, such as "a committed ref is
  never blindly overwritten", "every retained generation is restorable",
  "a balance never goes negative", or "a session never outlives its TTL".
- Concurrency, crashes between steps, untrusted storage, or adversarial input
  make the invariants hard to see by reading call sites.

Typical kernel contents: authentication and authorization verdicts, session
and token lifecycles, key bundles, envelopes and wrapping formats, ledger and
balance transitions, versioned on-disk or on-wire formats, compare-and-swap
and merge decisions, garbage collection and retention plans, replication and
rollback guards, restore planning, and chunk or offset mapping.

Do not build a kernel for ordinary CRUD, presentation, or glue code, or when
the critical rule is one comparison already owned by a reviewed library. A
kernel with no named invariants is just an extra layer.

## Kernel contract

- **Admission rule.** Code enters the kernel only if a bug in it could cause
  the catastrophic class of failure above. Write this rule down in the
  project's agent docs or spec, and apply it to every addition. Everything
  else stays out, even if it is "nearby".
- **Pure and synchronous.** No filesystem, network, process, database,
  environment, terminal prompt, async runtime, global mutable state, clock, or
  randomness source. The caller passes clocks, listings, lookups, generated
  nonces or keys, and configuration in as plain values. This is what makes
  the kernel deterministic, replayable, and model-checkable.
- **Decisions out, effects outside.** Kernel functions return typed verdicts,
  plans, or `accepted(next_state, effects)` results. Callers carry them out and
  never re-derive, second-guess, or partially reimplement them. If a caller
  needs a slightly different decision, change the kernel.
- **Ask, do not fetch.** When a decision depends on a fact only the shell can
  establish, such as ancestry in a repository or whether an object exists,
  model it as an explicit question the kernel returns and an answer type the
  caller supplies, then decide again from the answers. Give "unknown" or
  "missing" its own answer instead of guessing.
- **Small, reviewed dependencies.** Keep direct dependencies to a short,
  justified list of mature libraries (serialization, hashing, the reviewed
  crypto library, zeroizing secret types). Never design primitives
  (`/cryptography`). Keep third-party types out of the kernel's public API
  where practical, so swapping an adapter never touches audited code.
- **Hard boundary.** Make the kernel a separate crate, package, or module
  whose dependency direction the build enforces: the kernel depends on nothing
  from the shell. In Rust, use `#![forbid(unsafe_code)]`, no async runtime,
  and a minimal `Cargo.toml`. In other languages, use a separate package plus
  an import or lint rule that forbids I/O modules.
- **Fail closed.** Unknown versions, bad authentication tags, malformed or
  oversized input, overflow, and impossible states are rejections with
  structured, actionable errors, never defaults (`/fallbacks`). Bound every
  decode and every collection the kernel accepts. Use checked arithmetic for
  money, sizes, generations, and expiries.
- **Typed domain values.** Parse untrusted strings into validated newtypes
  (names, IDs, amounts, ref names) at the kernel edge, so invalid values
  cannot reach decisions (`/fragile`).
- **Secrets stay contained.** Hold keys and plaintext in zeroizing, redacting
  types; never log, print, or serialize them by accident; keep their
  lifetimes inside the smallest scope that needs them.
- **Versioned formats.** Every persisted or wire format the kernel owns
  carries a version. Writers emit only the current version; readers keep a
  frozen, bounded, fail-closed decoder per supported version that upgrades
  losslessly in memory (`/pattern-versioning`). Bind documents to their
  context, such as the object key or account they belong to, so untrusted
  storage cannot swap them.
- **Auditable size.** Keep the kernel small enough for one careful review
  sitting. When it grows, first ask whether the new code passes the admission
  rule; split by responsibility only for code that does.

## Shell responsibilities

The shell is everything outside the kernel: CLIs, servers, agents, storage
adapters, UI, async tasks. It:

- gathers inputs and turns them into the kernel's plain values;
- answers the kernel's questions honestly, including "missing";
- executes the returned plan in the order the kernel's contract requires,
  for example upload, read back and verify, then reference, then
  compare-and-swap the pointer, then fan out to mirrors;
- feeds outcomes, conflicts, and failures back to the kernel as events or
  new inputs instead of deciding recovery itself;
- never writes critical state through a path that bypasses the kernel, and
  read-only surfaces never gain a write path of their own. When a secondary
  surface must act, it calls the same operation and kernel decisions as the
  primary one.

Document the effect ordering and crash points next to the plan type, because
the ordering is part of the safety argument even though the kernel does not
run it.

## State machines in the kernel

Most kernel decisions are transitions: a session from locked to unlocked to
expired, a push from evaluated to conflicted to merged, a balance through
pending, settled, and reversed, a backup through uploaded, verified, and
retained. Model each with `/pattern-state-machine`: named states carrying only
valid data, an explicit transition function, caller-supplied time, terminal
states that stay terminal, and bounded retries. Keep the transition function
inside the kernel and the effect runner in the shell. The state machine gives
the verification layer a finite graph to check; the kernel boundary makes
sure nothing else can move that graph.

## Invariants and verification

Confidence comes from layered evidence over the same kernel functions. Use
`/formal-verification` to decide which properties deserve which tool, and
`/spec` when the project keeps a `.spec/`.

1. **Name the invariants.** Write each as a rule with its rationale and the
   features it protects, for example `INV-n` entries with `VER-n` obligations.
   Every kernel decision should trace to at least one invariant.
2. **Design model.** For multi-actor protocols (concurrent writers, crashes
   between steps, compaction or GC during writes, replication lag), model the
   protocol in a checker such as Quint or TLA+, with witnesses for the
   dangerous interleavings. Replay its traces against the shipped kernel
   functions so the model and the code cannot drift apart.
3. **Bounded proofs.** Check per-decision properties over all small inputs
   with a bounded model checker such as Kani. Write the harnesses so the same
   code also runs as property tests under the normal test runner (for
   example bolero), so they never rot between proof runs.
4. **Property tests.** Use property tests where proofs cannot reach, such as
   decisions over large collections or behavior of opaque reviewed libraries
   (round-trips, tampering, wrong keys, truncation).
5. **Golden fixtures.** Keep frozen encoded samples of every supported format
   version, plus their decrypted or decoded expectations, so old data stays
   readable.
6. **Differential and end-to-end checks.** Compare the system's observable
   result with an independent reference where one exists, such as a fresh
   clone against its source or a replayed ledger against stored balances.

Keep every verification artifact in the same change as the logic it covers,
and keep them passing there. Never weaken a property, bound, or assumption to
make a check pass. Heavy runs (model checkers, Kani, long fuzzing) can exhaust
memory: follow the project's approval rules for running them, and keep the
fast property and unit tests in routine checks.

## Workflow

1. **Explore and reuse.** Map the critical paths (`/review-critical-paths`)
   and check for an existing kernel, core crate, or decision module before
   creating one. Extend a genuine kernel rather than
   starting a parallel one.
2. **State the catastrophic failures and invariants.** List what must never
   happen and why, in the project's spec or agent docs.
3. **Draw the boundary.** Inventory every decision that guards an invariant
   and every input it needs. Classify each input as plain value, question to
   the caller, or effect outcome. Record the admission rule.
4. **Extract decisions, not plumbing.** Move the decisions behind pure
   functions and state machines with typed inputs and verdicts. Leave I/O,
   retries, scheduling, and formatting in the shell. Delete the old in-place
   logic so there is one authority, and make
   callers carry out the verdict without re-deriving it.
5. **Harden the edges.** Validate and bound inputs, fail closed, version
   formats, contain secrets, and use checked arithmetic.
6. **Attach evidence.** Add unit tests for every verdict, including
   rejections (`/writing-tests`), then the verification layers the invariants
   justify. Link each obligation to the functions it covers.
7. **Document the contract.** In the kernel's module docs and the project's
   agent docs, state what the kernel owns, its admission rule, its purity
   constraints, its dependency allowlist, and how the shell must order effects.
8. **Review.** Use `/review-security`, `/review-cryptography`, and
   `/review-bugs` on the kernel diff, and look specifically for shell code
   that re-derives or bypasses a kernel decision.

## Common failure modes to reject

- The "kernel" reads a clock, environment variable, file, or random source,
  so its decisions cannot be replayed or checked.
- Callers re-implement part of a decision ("just this one guard here"), so
  the audited logic is no longer the logic that runs.
- Non-critical conveniences accumulate in the kernel until it is too large to
  audit and every change churns the verification artifacts.
- A secondary surface (admin endpoint, browse UI, background worker, script)
  writes critical state through its own path.
- Missing or unknown answers default to "allowed", "zero", or "latest".
- Formats are unversioned, decoders are unbounded, or old versions are read by
  the current decoder with ad hoc patches.
- Verification checks a hand-written model of the code rather than the shipped
  functions, with nothing tying the two together.
- A property or bound is relaxed to make a failing proof or test pass.
- A heavyweight dependency, framework, or async runtime is pulled into the
  kernel for convenience.

## Review checklist

- Does every piece of kernel code pass the written admission rule?
- Is the kernel pure, synchronous, and free of unsafe code, I/O, clocks, and
  randomness, with the build enforcing the boundary?
- Do all writes of critical state go through kernel verdicts, with no shell
  path that re-derives or bypasses them?
- Are inputs validated, bounded, typed, and failed closed, including unknown
  versions and missing answers?
- Are lifecycles explicit state machines with terminal and timeout behavior?
- Are secrets contained in zeroizing, redacting types and never logged?
- Does each invariant have proportionate evidence tied to the shipped
  functions, updated in this change?
- Is the effect ordering the safety argument depends on documented and
  followed by the shell?
- Is the kernel still small enough to audit in one sitting?

## Output

When designing, extracting, or reviewing a kernel, report:

- the catastrophic failures it prevents and the named invariants;
- the kernel boundary, admission rule, dependency allowlist, and what stays in
  the shell;
- the decisions, state machines, questions, and verdict types it exposes;
- the effect ordering the shell must follow and any crash points;
- the verification evidence per invariant, what ran, and what still needs an
  approved heavy run;
- remaining bypasses, oversized areas, or unverified invariants.

Related skills: `/pattern-state-machine`, `/pattern-versioning`,
`/formal-verification`, `/cryptography`, `/review-critical-paths`,
`/fallbacks`, `/fragile`, `/writing-tests`, `/spec`.
