# Verification Tool Notes

Per-tool detail backing the role table in [SKILL.md](../SKILL.md). It reflects
the ecosystem as of October 2026; re-check maturity before relying on a tool.

## Notes By Tool

- **Quint.** TLA-based, with a type checker, a simulator (`quint run`), tests,
  a REPL, and symbolic model checking. It can export to TLA+ for TLC, which
  keeps lock-in low. It is maintained by an independent open-core company; the
  language and core tools are open source. Its trace format (ITF) supports
  model-based testing. `quint-connect` replays traces against Rust but was
  below a 100-star threshold at the time of writing, so a thin in-repo
  replayer is the default.
- **Kani.** Bit-precise bounded model checker for Rust, used to verify parts of
  the Rust standard library and AWS projects. It proves properties for all
  inputs within the bounds, including panics, overflow, and undefined behavior
  in `unsafe`. It does not verify concurrent code; use a `concurrency-check`.
  Its own setup downloads an unpinned toolchain. In a Nix project, pin it
  instead: build the `kani-verifier` crate, fetch the release bundle by hash
  and patch it to run on NixOS, and supply the nightly named in that release's
  `rust-toolchain.toml`, for example through fenix. Set `KANI_HOME` to the
  assembled tree. Code under `#[cfg(kani)]` also needs `cfg(kani)` declared
  in the crate's `unexpected_cfgs` lint so stable builds stay warning-free.
- **Lean 4.** The kernel checks every proof, so an AI-written proof is as
  trustworthy as a hand-written one; review the theorem statement, not the
  proof. `Std.Do` and `mvcgen`
  (since Lean 4.22) support Hoare-style verification of imperative-style Lean
  code. Cedar's verification-guided development is the reference pattern for
  linking Lean to Rust: readable Lean models with proofs, plus differential
  random testing against production code. Avoid heavy library dependencies in
  small proofs, because toolchain and library upgrades break them independent
  of code changes.
- **Aeneas.** Translates safe, sequential Rust to Lean. It is used in production
  for Microsoft SymCrypt, at roughly an order of magnitude more proof than code,
  and the soundness argument for the translation itself is still in progress.
- **Verus, Creusot, Flux.** Deductive and refinement-type verifiers for Rust.
  Verus is the most mature but costs several lines of proof per line of code.
  Creusot is active but requires nightly Rust. Flux is lightweight but still at
  research stage. Revisit when a project needs unbounded proofs inside Rust
  code.
- **loom vs shuttle.** loom is exhaustive and hits state explosion beyond a few
  threads. shuttle is randomized, so a pass is evidence rather than proof, but
  it scales to real code.
- **turmoil vs madsim.** turmoil uses the Tokio ecosystem's types, but
  nondeterminism from time and randomness in dependencies can leak through.
  madsim intercepts libc time and randomness behind a `--cfg madsim` build.
