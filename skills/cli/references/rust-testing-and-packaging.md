# Rust Testing and Packaging

## Test the interface in layers

Keep parser tests fast, but do not stop there. Run the compiled program for observable behavior.

Suggested coverage:

- no arguments, help, version, and syntax errors;
- every subcommand and option relationship;
- stdout, stderr, and exit status as separate assertions;
- native non-UTF-8 paths and forwarded arguments on Unix, including reversible machine output when promised;
- configuration precedence and invalid configuration;
- terminal and non-terminal execution;
- color `auto`, `always`, and `never`;
- human and machine formats, including empty and incremental output;
- broken downstream pipes;
- cancellation and signals, including descendants when the CLI claims ownership of the whole job;
- child failure, large child output, and missing executables;
- dry-run truthfulness and unattended destructive-action rejection.

Use temporary directories and explicit environment isolation. Do not let tests read the developer's real config, cache, state, home directory, or network unless the test is explicitly an integration test with those prerequisites.

`assert_cmd`-style process assertions or `trycmd` transcript cases can be useful. Snapshot help and diagnostics only where reviewed textual stability is valuable; otherwise assert the behavioral fields that matter. Normalize only genuinely nondeterministic values, not bugs.

## Completions and manuals

Generate shell completions from the same command model as the executable, commonly with `clap_complete`. Generate man pages from that model or another single source of truth. Package generated artifacts for the exact binary version; do not ask users to write into immutable store paths at runtime.

Treat completions as code that can execute in a user's shell. Avoid embedding untrusted dynamic text and exercise representative completion behavior.

## Packaging

Package the CLI through the channels the project already uses, such as crates.io, release archives, a distribution package, Homebrew, or Nix. Whatever the channel:

- build from the tracked `Cargo.lock` (`cargo build --locked`) so the release matches what was tested;
- ship completions, man pages, and other generated artifacts built for that exact binary version;
- declare runtime executables and libraries explicitly instead of assuming they are on the user's `PATH`;
- do not make `cargo install`, runtime downloads, or self-update part of normal operation when a package manager owns the install;
- keep mutable config and state in the platform's config and state locations, never inside the install prefix.

### Nix

Follow the project's existing derivation style. For an ordinary locked Cargo workspace this often means `rustPlatform.buildRustPackage` with:

- the project source or a narrowly filtered source;
- the tracked `Cargo.lock`;
- the correct workspace package selection;
- native and runtime dependencies declared explicitly;
- check behavior aligned with the package's real test requirements;
- completions, man pages, desktop assets, or service units installed by the derivation.

Do not write into the Nix store at runtime. Patch build-time paths through Nix inputs or environment rather than assuming `/usr`, `/bin`, or `/lib`.

When Nix or Home Manager owns a config file, do not overwrite it from the application; report the conflict clearly.

Before editing packaging, inspect the project's flake, package helpers, overlays, and existing Rust derivations. Use focused Nix parsing/evaluation for packaging changes and Cargo checks when Rust code changed.

## Release checklist

- Confirm command help and examples match behavior.
- Confirm machine schema and exit statuses are documented.
- Confirm no secrets or diagnostics leak to stdout.
- Confirm the package, such as a Nix closure or a distribution package, contains every runtime executable and library dependency.
- Confirm completions/man pages match the released command tree.
- Confirm unsafe or destructive operations remain opt-in and test-covered.
- Confirm the MSRV and lockfile remain intentional.

## Research baseline

Reviewed 2026-08-02.

- [`clap_complete`](https://docs.rs/clap_complete/latest/clap_complete/)
- [`trycmd`](https://docs.rs/trycmd/latest/trycmd/)
- [Rust CLI Working Group book](https://rust-cli.github.io/book/)
