# Rust Processes, Configuration, and Safety

## Child processes

Use `std::process::Command` and pass every token with `.arg()` or `.args()`. This preserves argument boundaries and avoids shell interpretation. Use a shell only when the requested operation truly is shell language; then state that trust boundary and quote data with a purpose-built approach.

Resolve executables predictably. On NixOS, prefer a dependency supplied by the package closure or an explicit configured path over an FHS location. If searching `PATH` is part of the interface, diagnose which executable was chosen where practical.

Select stdio intentionally:

- inherit for an interactive child whose interface should remain visible;
- pipe when output is data the parent must consume;
- null only when discarding data is deliberate.

When both stdout and stderr are piped, drain them without allowing either pipe buffer to block the child. Bound captured data or stream it when output can be large. Close unused pipe ends. Always reap children.

Define interruption behavior before spawning. Coordinate cancellation, graceful termination, a bounded escalation to forced termination, and `wait`. Consider whether the child creates descendants; killing only the immediate child may not stop the operation. Establish a new process group/session or another supervised job boundary when the CLI owns the whole job, and signal that boundary deliberately. State the limitation when descendants may escape it. Async implementations must use runtime-aware process and signal APIs rather than blocking the executor.

## Signals and cleanup

Use a mature signal facility such as `signal-hook`, or the active async runtime's signal module. Keep handlers minimal and async-signal-safe; communicate intent to normal control flow. Make shutdown idempotent because multiple causes can race.

Prefer recoverable protocols and atomic state transitions over relying solely on destructor cleanup. SIGKILL, power loss, and process abort do not run destructors.

## Configuration and XDG directories

Define and test one precedence order. If multiple configuration scopes exist,
use flags, process environment, project configuration, user configuration,
system configuration, then built-in defaults, omitting scopes the application
does not support.

Explain the winning source in verbose or diagnostic modes without exposing secret values. Do not merge lists and maps inconsistently across layers.

Use XDG locations by semantic role:

- config: user-edited or declarative configuration;
- data: durable user data;
- state: durable state such as history that is not portable user data;
- cache: safely regenerable material;
- runtime: login-session-scoped sockets, locks, and transient coordination.

The XDG specification requires its path variables to be absolute; ignore a relative value rather than treating it as a working-directory-relative path. `XDG_RUNTIME_DIR` is private to the user, has mode 0700, and must not hold durable data.

Use an established project-directory helper when it matches the application identity, but still inspect its platform behavior and version. Allow explicit paths for tests.

## Writes and sensitive operations

For durable replacement, create a same-filesystem temporary file, set required mode and ownership, flush when durability matters, rename atomically, and sync the parent directory when the threat model requires crash durability. Do not call a sequence “atomic” unless its full failure behavior supports that claim.

Open sensitive files with least privilege. Avoid time-of-check/time-of-use validation, unsafe temporary names, and following untrusted symlinks in privileged code. Keep advisory locks bounded and recoverable.

For mutation:

- expose inspection or dry-run output that reflects the real execution plan;
- make the target unambiguous;
- validate close to the effect;
- require explicit acknowledgement for destructive unattended work;
- state whether retry is safe;
- preserve the underlying native command when acting as a system helper.

Do not put passwords, tokens, or other secrets in argv or logs. Prefer inherited descriptors, stdin where its contract is unambiguous, systemd credentials, or a protected file.

## Research baseline

Reviewed 2026-08-02.

- [`std::process`](https://doc.rust-lang.org/std/process/index.html)
- [`std::process::Command`](https://doc.rust-lang.org/std/process/struct.Command.html)
- [Rust CLI book: signals](https://rust-cli.github.io/book/in-depth/signals.html)
- [`signal-hook`](https://docs.rs/signal-hook/latest/signal_hook/)
- [Tokio signal support](https://docs.rs/tokio/latest/tokio/signal/)
- [XDG Base Directory Specification 0.8](https://specifications.freedesktop.org/basedir/0.8/)
- [`directories`](https://docs.rs/directories/latest/directories/)
