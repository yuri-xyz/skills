---
name: rust
description: Use when writing, refactoring, or reviewing Rust, especially when modeling data and states in the type system, matching over enums, handling errors, or removing escape hatches such as `unwrap`, `as` casts, wildcard match arms, needless `clone`, or unjustified `unsafe`.
---

# Rust

## Objective

Write Rust whose types carry the design, so that refactoring is fearless:
change an enum, a field, or a signature, and the compiler lists every place
that must change with it. Rust gives this for free only when the code does
not opt out of it. A wildcard arm, an `unwrap`, an `as` cast, a `String`
where a type belongs, or a `clone` to quiet the borrow checker each turns a
compile error you wanted into a runtime surprise.

The rule of thumb: make illegal states unrepresentable, match exhaustively,
parse at the edges, return errors as values, and keep `unsafe` small and
justified.

## Workflow

1. Read `Cargo.toml`, the edition, `rust-version`, the `[lints]` tables, and
   `clippy.toml` first. Reuse the project's error types, newtypes, and
   helpers before writing new ones, and follow /refactor-reuse.
2. Model the data before writing logic: which states exist, which data
   belongs to which state, and which values are distinct even when they
   share a primitive representation.
3. Write logic so that every `match` over the project's own enums is
   exhaustive without a catch-all arm.
4. Parse untrusted input once at the boundary into domain types.
5. Run `cargo check`, `cargo clippy --all-targets`, and the tests. Fix
   warnings at their cause; never silence them without a stated reason.
6. For a refactor, change the type first and follow the errors.

## Edition, Toolchain, And Lints

- Use the 2024 edition for new crates. It enables let chains, makes
  `unsafe_op_in_unsafe_fn` warn, requires `unsafe extern` blocks, tightens
  `if let` and tail-expression temporary scopes, and changes `impl Trait`
  return types to capture all in-scope lifetimes.
- Set `rust-version` so the MSRV-aware resolver picks compatible
  dependencies, and check a feature's stabilization version against it before
  using it.
- Configure lints in `[lints.rust]` and `[lints.clippy]` (or the workspace
  `[workspace.lints]`) rather than scattered `#![deny]` attributes. Good
  defaults for application and library code, adjusted to the project:
  - `clippy::pedantic` as warn, with the noisy lints the project rejects
    allowed explicitly.
  - `clippy::unwrap_used`, `clippy::expect_used` (for libraries),
    `clippy::panic`, `clippy::indexing_slicing`, and
    `clippy::as_conversions` or the narrower `cast_*` lints.
  - `clippy::wildcard_enum_match_arm` and
    `clippy::match_wildcard_for_single_variants`.
  - `clippy::allow_attributes` and `clippy::allow_attributes_without_reason`,
    so every exception is an `#[expect(lint, reason = "...")]`.
  - `clippy::undocumented_unsafe_blocks` and `unsafe_code` where the crate
    should have none.
- Prefer `#[expect(...)]` over `#[allow(...)]`: it warns when the exception
  is no longer needed, so stale suppressions do not pile up.
- Make warnings fail CI through the project's configuration, such as
  `RUSTFLAGS=-Dwarnings` or Cargo's build warnings setting, not with
  `#![deny(warnings)]` in source, which breaks builds on new compiler lints.

## Model States, Not Bags Of Fields

- Represent a value with several states as an `enum` whose variants carry
  only the data that exists in that state. A struct with an `Option` per
  state and a `status` field describes combinations that cannot happen.
- Wrap primitives that mean something in newtypes: IDs, units, validated
  strings, indices into a specific collection. Construct them only through
  `TryFrom`, `FromStr`, or a `new` that validates, keep the field private,
  and the rest of the program can trust them.
- Use the standard library's refined types: `NonZero<T>` for values that
  cannot be zero, `Duration` instead of raw seconds, `PathBuf` instead of
  `String` for paths, and `std::num::Saturating` or `Wrapping` when that
  arithmetic is the intent.
- Encode protocol and lifecycle order with typestate when misuse is costly:
  a type per state, transitions that consume `self` and return the next
  state, and `PhantomData` markers when the states share data.
- Replace `bool` parameters with two-variant enums, so call sites read
  `Mode::Overwrite` instead of `true`.
- Mark results that must not be ignored `#[must_use]`, including builders and
  guards.
- Mark public enums and structs `#[non_exhaustive]` only when downstream
  crates must not match exhaustively; inside a crate, exhaustive matching is
  the feature.

For larger lifecycles with transitions, also follow /pattern-state-machine.

## Exhaustive Matching

- Every `match` over an enum the crate owns lists every variant. Adding a
  variant must be a compile error at each place that has to decide what to do
  with it. A `_ =>` arm silently picks a behavior for variants that do not
  exist yet.
- Group variants with `|` patterns when they share a branch instead of
  reaching for `_`.
- Use `_` only for values that are open by nature, such as integers, strings,
  or `#[non_exhaustive]` enums from other crates, and make that arm return an
  error or an explicit outcome rather than a guess.
- Destructure structs in patterns (`let Config { a, b, .. } = config;` or,
  better, without `..`) where a newly added field must be considered.
- Use `let ... else` for early returns on a refutable pattern, let chains
  (`if let Some(x) = a && let Ok(y) = b(x)`) instead of nested `if let`, and
  `if let` guards in `match` arms instead of matching twice.
- Use `matches!` for boolean checks and `assert_matches!` in tests, which
  prints the value on failure; it must be imported from `std`.

Read [patterns.md](references/patterns.md) for code examples of these and the
other patterns in this skill.

## Errors

- Return `Result` for anything that can fail for reasons outside the
  programmer's control, and propagate with `?`. Panics are for bugs: broken
  invariants and impossible states.
- In libraries, define error enums with one variant per failure the caller
  might handle, carrying the context needed to act, implementing
  `std::error::Error` with `source()` chains. Do not return `String`,
  `Box<dyn Error>`, or one catch-all variant. In applications, a
  context-carrying error type at the top level is fine, but keep typed errors
  in the modules below it.
- Add context where information is lost: which file, which key, which
  request. "No such file or directory" without a path is not actionable.
- `unwrap` and `expect` belong in tests, in examples, and after a check the
  compiler cannot see; there, `expect` states the invariant that makes it
  safe, not what went wrong.
- Do not hide failure behind `unwrap_or_default`, `ok()`, or `let _ =`
  unless discarding the error is the intended behavior; see /fallbacks.

## Boundaries

- Parse, don't validate: turn untrusted input from files, the network,
  environment variables, command-line arguments, and FFI into domain types
  once, at the edge, and pass the typed values inward.
- Derive deserialization with types that cannot represent invalid input,
  such as enums for closed sets, newtypes with validating `TryFrom`, and
  `#[serde(deny_unknown_fields)]` where unknown fields signal a mistake.
- Read configuration and environment once into a typed struct at startup.

## Escape Hatches

| Escape hatch | Replace with |
| --- | --- |
| `.unwrap()`, `.expect()` in non-test code | `?`, a handled `match`, or `expect` stating a real invariant |
| `_ =>` on an owned enum | every variant listed, grouped with `\|` |
| `x as u32` and other numeric `as` | `From`, `TryFrom`, `u32::try_from(x)?`, or explicit `checked_*`, `saturating_*`, `wrapping_*` |
| `slice[i]`, `map[&k]` that can miss | `get`, `get_mut`, or iterators |
| `.clone()` to satisfy the borrow checker | restructured borrows, `Arc` for real shared ownership, or `mem::take` |
| `Rc<RefCell<T>>` or `Arc<Mutex<T>>` everywhere | clear ownership, message passing, or a single owner with `&mut` |
| `#[allow(lint)]` | fixing the cause, or `#[expect(lint, reason = "...")]` |
| `unsafe` | a safe API; if none exists, a minimal block with a `// SAFETY:` comment |
| `transmute` | `from_le_bytes`, `bytemuck`-style checked casts, or `From` impls |
| `String`, `u64`, `bool` for domain values | newtypes and enums |
| `Box<dyn Error>` in a library API | a typed error enum |
| `panic!` or `todo!` left in shipped paths | a returned error or a finished implementation |

## Generics, Traits, And Ownership

- Accept the most general borrowed form: `&str`, `&[T]`, `&Path`,
  `impl AsRef<Path>`, or `impl IntoIterator<Item = T>`; return owned types.
- Prefer generics and `impl Trait` for static dispatch; reach for `dyn Trait`
  when you need heterogeneous collections or smaller code size. Trait
  upcasting (`&dyn Sub` to `&dyn Super`) works on stable.
- Use `use<..>` bounds on `impl Trait` return types to state exactly which
  lifetimes and type parameters the hidden type captures when the 2024
  default captures too much.
- Seal traits that outsiders must not implement, and use
  `#[diagnostic::on_unimplemented]` to give a clear error when a bound is not
  met.
- Use `LazyLock` and `LazyCell` from the standard library for lazy statics
  instead of extra crates, and `OnceLock` for set-once values.
- Use `slice::get_disjoint_mut` and `HashMap::get_disjoint_mut` for several
  mutable borrows into one collection, not indices with `unsafe` or clones.
- Keep type-level machinery proportionate. Typestate, const generics, and
  trait tricks earn their place where misuse is costly; elsewhere a plain
  enum and a runtime check read better and compile faster.

For async code, follow /rust-async.

## Pitfalls

- **Integer overflow:** it panics in debug builds and wraps silently in
  release. Use `checked_*` for untrusted arithmetic, and watch `len() - 1` on
  empty collections.
- **Lossy `as`:** `as` truncates, wraps, and saturates floats silently; it is
  never a validation. Use `TryFrom`.
- **Eager defaults:** `unwrap_or(expensive())` and `ok_or(format!(...))`
  evaluate their argument every time; use the `_else` forms.
- **`let _ = guard;`** drops the value immediately, releasing a lock or
  cancelling a guard on the same line. Bind guards to a named variable such as
  `_guard`.
- **Temporaries in conditions:** a lock or borrow taken in a `match` scrutinee
  lives for the whole `match`. Bind the value first when that would deadlock or
  conflict; the 2024 edition shortened this for `if let`, not for `match`.
- **Locks across `.await`:** holding a `std::sync::MutexGuard` or a
  `RefCell` borrow across an await point blocks or panics; release it first.
- **Iteration order:** `HashMap` and `HashSet` order is random. Use `BTreeMap`
  or sort before output that must be stable.
- **Floats:** no `Eq` or `Ord`, `NaN != NaN`; use `total_cmp` for sorting and
  never compare money with floats.
- **Strings:** `len()` is bytes, slicing at a non-character boundary panics,
  and `chars()` is code points, not user-visible characters. `Path::to_str`
  fails on non-UTF-8 paths; keep paths as `Path`.
- **`process::exit`** skips destructors, so buffers are not flushed; return
  from `main` with an `ExitCode` instead.
- **`Deref` for inheritance:** implementing `Deref` on a newtype to forward
  methods leaks the inner type's whole API and defeats the newtype.
- **Default derives:** `#[derive(Default)]` on a type without a meaningful
  default invents values; write the constructor instead.
- **Atomics:** `Ordering::Relaxed` gives no ordering with other memory; use it
  only for counters, and `Acquire`/`Release` or `SeqCst` when it guards data.
- **Panics in `Drop`** during unwinding abort the process; keep `Drop` simple
  and infallible.

## Refactoring With The Compiler

- Make the change in the type first, such as adding a variant, renaming a
  field, narrowing a parameter, or replacing a primitive with a newtype, then
  follow the errors until the crate compiles.
- If a refactor compiles too easily, look for the opt-out that hid it: a
  wildcard arm, a `Default` filling a new field, an `as` cast, or a `..` in a
  pattern.
- Pin important compile-time contracts with `compile_fail` doctests, or with
  the project's UI-test setup when it has one, and follow /writing-tests.
- Fix lint and build failures at their cause per /fix-lints.

## Avoid

- `unwrap`, `expect` without a real invariant, `panic!`, and `todo!` in
  shipped code paths.
- Wildcard arms over enums the crate owns.
- Numeric `as` casts, unchecked indexing, and unchecked arithmetic on
  untrusted values.
- Primitive types and `bool` parameters for domain concepts.
- Structs of `Option` fields that stand in for states an enum would make
  explicit.
- `clone`, `Rc<RefCell<_>>`, or `Arc<Mutex<_>>` used to make the borrow
  checker stop complaining.
- `#[allow]` without a reason, and `#![deny(warnings)]` in source.
- `unsafe` without a `// SAFETY:` comment proving each requirement.
- Stringly or boxed errors in library APIs, and errors that lose context.
- Type-level cleverness whose cost in readability and compile time exceeds the
  misuse it prevents.
