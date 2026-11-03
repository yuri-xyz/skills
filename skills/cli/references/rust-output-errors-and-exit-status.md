# Rust Output, Errors, and Exit Status

## Separate channels

Use stdout for successful requested data and stderr for everything that explains execution. This lets callers redirect or pipe results without scraping diagnostics.

For human output:

- make the default concise;
- gate progress and decorations on terminal capability;
- allow quiet and verbosity controls when the operation warrants them;
- avoid success chatter when stdout is intended to feed another command.

For machine output:

- require an explicit format;
- serialize structured types rather than assembling JSON strings;
- keep every byte on stdout within the selected format;
- choose JSON for one document and JSON Lines for incremental records;
- document nullability, units, identifiers, ordering guarantees, and schema evolution;
- encode native non-UTF-8 arguments and paths with a documented reversible representation rather than lossy display text;
- put fatal diagnostics on stderr and use status to indicate failure.

JSON strings are Unicode and cannot losslessly represent every Unix `OsStr`. Choose an explicit representation such as tagged platform bytes or a reversible platform encoding when the format must round-trip native values. A human-readable lossy companion may aid diagnostics, but must not become the identity or reconstructed path.

## Terminal and color behavior

Check the actual output stream with `std::io::IsTerminal`. stdin, stdout, and stderr can have different terminal states. A prompt depends on the input and prompt-output terminal; color depends on the output stream.

Prefer a maintained stream abstraction such as `anstream` when the project needs robust ANSI support. Honor explicit `always`, `auto`, and `never` policy and common conventions including `NO_COLOR`. Never color machine output.

Do not prompt in automation. If a dangerous action requires acknowledgement, provide a clearly named affirmative flag and reject absent confirmation in non-interactive contexts. An EOF is not consent.

## Errors

Add context at the boundary where it becomes meaningful: name the failed command, path, host, option, or operation. Preserve the source error for debugging. Keep one component responsible for final rendering.

- Typed errors fit libraries and recoverable domain distinctions.
- `anyhow` can fit application-level propagation and context.
- `miette` fits source-oriented diagnostics with labels and spans; its rich handler belongs near the executable boundary and is not automatically justified for every CLI.

Avoid `unwrap`, `expect`, and panics for user input, environmental failures, and ordinary child-process failures. Do not reveal secrets in error context or debug chains.

## Exit status

Return `ExitCode` or implement `Termination` at `main`. Keep domain code return-based. `process::exit` terminates immediately and does not run destructors, so reserve it for exceptional process-boundary needs.

Use zero only for success under the documented contract. Let the parser own its conventional help and usage behavior. Add distinct nonzero statuses only when callers can act differently; document them and keep them stable. If wrapping a child, decide explicitly whether the wrapper maps or preserves its status.

Handle partial success deliberately. A batch command should state whether it is fail-fast, best-effort with a summary, or transactional.

For broken pipes, avoid a scary diagnostic when a downstream reader intentionally closes early, while still surfacing unrelated write failures.

## Research baseline

Reviewed 2026-08-02.

- [Rust CLI book: communicating with humans](https://rust-cli.github.io/book/tutorial/output.html)
- [Rust CLI book: communicating with machines](https://rust-cli.github.io/book/in-depth/machine-communication.html)
- [`std::process::exit`](https://doc.rust-lang.org/std/process/fn.exit.html)
- [`std::io::IsTerminal`](https://doc.rust-lang.org/std/io/trait.IsTerminal.html)
- [`anyhow`](https://docs.rs/anyhow/latest/anyhow/)
- [`miette`](https://docs.rs/miette/latest/miette/)
- [`anstream`](https://docs.rs/anstream/latest/anstream/)
