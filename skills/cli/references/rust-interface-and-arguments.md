# Rust Interface and Arguments

## Start with the contract

Describe the CLI before choosing implementation details:

- Who calls it: a person, shell script, systemd unit, another program, or several of these?
- Which names and output fields become compatibility promises?
- Which actions merely inspect state and which can mutate it?
- Can the same operation be repeated safely?
- What happens with no arguments, `--help`, invalid input, and a literal `--`?

Prefer noun-like subcommands for resources and conventional option names. Keep a positional argument only when its meaning is obvious and stable. Use required flags when two same-shaped positional values would be easy to reverse.

## Typed parsing

With `clap`, normally derive `Parser`, `Subcommand`, `Args`, and `ValueEnum`. Express syntax in the parser:

- conflicts and requirements;
- repeatable values and value counts;
- mutually exclusive modes;
- enumerated textual values;
- defaults that are truly interface defaults.

Keep environmental and external validation out of the parser when it requires I/O or mutable state. Parsing should answer “is this command syntactically valid?”; application validation should explain why a valid command cannot run here.

Do not assume the latest online example matches the project. Check `Cargo.toml`, `Cargo.lock`, the Rust edition, and MSRV first. Preserve existing parser idioms unless a change has a concrete benefit.

## Native strings

Unix paths and arguments are byte sequences, not necessarily UTF-8 text. Use:

- `Path` and `PathBuf` for paths;
- `OsStr` and `OsString` for opaque native arguments;
- `std::env::args_os()` when reading argv without a parser;
- `Command::arg` with native values when forwarding.

Convert only values whose interface explicitly requires Unicode, such as an enum keyword or JSON string. For diagnostics, render lossy text only at the display boundary and avoid using that rendering as an identity or round-trip value.

If the CLI wraps another program, collect trailing native arguments without interpreting them and respect `--`. Document which options belong to the wrapper and which are forwarded.

## Compatibility

Treat these as public API when automation can observe them:

- command and option names;
- default behavior and precedence;
- stdout shape and ordering;
- machine schema;
- exit statuses;
- whether an operation prompts;
- side effects and idempotence.

Deprecate before removing widely used names. Aliases can ease migration but should not make help ambiguous. Avoid depending on help text wording as a machine interface.

## Research baseline

Reviewed 2026-08-02. Recheck current project versions before implementing.

- [Rust CLI Working Group book](https://rust-cli.github.io/book/)
- [`clap` derive reference](https://docs.rs/clap/latest/clap/_derive/)
- [`OsString` and Unix native string representation](https://doc.rust-lang.org/std/ffi/os_str/struct.OsString.html)
