---
name: cli
description: Use when building, changing, or reviewing a command-line application in any language, including its arguments, help, output, errors, interactivity, configuration, testing, and distribution.
---

# CLI

Design a command-line interface as a durable text interface for people and
programs. Treat commands, options, environment variables, configuration files,
output formats, exit statuses, prompts, and side effects as observable public
behavior. Follow familiar Unix conventions while making the interface
discoverable and humane.

## Workflow

1. Inspect the repository's `AGENTS.md`, language/toolchain, package manifest,
   existing command model, error handling, tests, documentation, and packaging.
2. Identify the audiences: interactive users, shell scripts, CI, other programs,
   or a deliberate mix. Decide which operations inspect state and which mutate it.
3. Write the observable contract before implementation: commands, arguments,
   defaults, precedence, stdin/stdout/stderr, machine formats, exit statuses,
   prompts, signals, side effects, idempotence, and compatibility promises.
4. Design the smallest coherent command tree and choose a mature parser for the
   language. Keep parsing, validation, domain operations, rendering, and the
   process boundary independently testable.
5. Implement with existing project dependencies and conventions. Make network,
   filesystem, subprocess, and other boundary-crossing effects explicit.
6. Exercise the compiled executable as a process, not only parser or library
   functions. Test both terminal and automation paths.
7. Update help, examples, terminal/web documentation, completions, manuals,
   package metadata, and installation/uninstallation guidance when the public
   interface changes.
8. If the CLI is implemented in Rust, apply the conditional section below and
   read only the Rust references relevant to the change.

## General rules

### Human-first and composable design

- Design for the primary human workflow without breaking composition through
  standard streams, signals, exit statuses, and stable machine formats.
- Follow established conventions for option names, help, version reporting,
  color, paging, prompts, and cancellation. Break convention only for a clear
  usability or safety reason, and document the choice.
- Keep the default behavior useful for the common case. Avoid making users
  remember a flag that should have been the default.
- Make state changes visible: report what changed, show important resulting
  state, and suggest the next useful command when a workflow has one.
- Keep external boundaries explicit. Do not silently read unrelated files,
  contact remote services, or modify external state without a documented reason
  and an appropriate opt-in or confirmation.
- Prefer idempotent and recoverable operations. Make retries, partial success,
  concurrent invocations, and interrupted work have deliberate semantics.

### Discovery, help, and documentation

- Use a mature argument parser where available so syntax, help, defaults, and
  suggestions share one command model.
- Provide `-h` and `--help` at the root and for every subcommand; do not overload
  `-h` for another meaning. Make help tolerant of normal flag placement.
- If a command needs arguments, show concise help when invoked without them,
  unless it is intentionally interactive. Include what the program does, one or
  two useful examples, the common options, and how to request full help.
- Lead help with realistic examples and show representative output when it
  clarifies a non-obvious operation. Put common commands and flags first.
- Include a support or issue-reporting path. Provide terminal documentation for
  offline use and, for public tools, searchable web documentation; consider
  manuals or a `help` subcommand for detailed reference material.
- Suggest likely corrections or next commands after errors when doing so is
  safe. Do not silently reinterpret input or perform a guessed mutation.
- If a command expects piped input but stdin is a terminal, show usage or fail
  clearly instead of appearing to hang.

### Command surface

- Express syntax in the parser: subcommands, required values, conflicts,
  repetitions, enumerations, and defaults that are truly interface defaults.
- Prefer named flags for multiple independent concepts. Keep positionals for an
  obvious primary value, a source/destination pair, or multiple homogeneous
  inputs such as file paths.
- Give flags descriptive long forms. Reserve one-letter flags for common,
  high-frequency options and use conventional names such as `--help`,
  `--version`, `--quiet`, `--verbose`/`--debug`, `--dry-run`, `--force`,
  `--output`, and `--json` when their meanings fit.
- Preserve a literal `--` boundary when forwarding arguments. When an input or
  output is a file, support `-` for stdin or stdout when it is unambiguous.
- For an option with an optional value, use an explicit sentinel such as
  `none` when “disabled” must be distinguished from an omitted value.
- Make options and subcommands order-independent where practical. Avoid
  ambiguous positionals, implicit subcommand abbreviations, catch-all commands,
  and aliases that make future additions unsafe. Keep any aliases explicit and
  stable.
- Use consistent noun/verb ordering and terminology across nested subcommands.
  Do not create similarly named commands whose distinction users cannot guess.
- Give the executable a short, memorable, lowercase name that is easy to type
  without colliding with a common command or another tool's name.
- Make defaults safe and unsurprising. Require an explicit, scriptable
  acknowledgement for unattended destructive operations.

### Output, errors, and status

- Send requested result data to stdout. Send diagnostics, warnings, progress,
  prompts, and explanatory messages to stderr so pipelines receive data only.
- Keep human output concise and readable. Report successful state-changing work
  briefly; provide `--quiet` when non-essential success output would obstruct
  scripts.
- Offer an explicit machine format such as `--json` for structured data and a
  line-oriented or `--plain` form when rich human formatting would break simple
  tools such as `grep` and `awk`. Define fields, nullability, units, ordering,
  encoding, and evolution rules. Never mix prose, color, spinners, or logs into
  machine output.
- Treat native non-text values as a format-design issue. Use a documented
  reversible representation or reject values at an explicit text-only boundary;
  do not use lossy display text as an identity.
- Detect the relevant stream's terminal capability rather than inferring
  interactivity from an environment variable. Disable color and animation when
  output is not a terminal; honor `NO_COLOR`, `TERM=dumb`, and explicit
  `--no-color`/color policy where applicable. Never color machine output.
- Use a pager only for substantial human output and only when the relevant
  streams are interactive. Show useful progress before and during long work,
  but keep progress bars and parallel output off automation paths and expose
  useful failure details when progress rendering ends.
- Rewrite expected failures for humans with context, a likely remedy, and a
  useful next step. Keep stack traces, internal debug data, and log-level noise
  out of the default path; group repetitive failures when that improves signal,
  and provide an intentional verbose or diagnostic path.
- Return zero only for success. Map stable non-zero statuses to failure modes
  only when callers can act differently, and define partial-success behavior.
  Handle broken pipes as an ordinary pipeline outcome where possible.

### Input, interactivity, and safety

- Validate input early and close to the effect. Do not require a prompt: every
  required value must have a flag, argument, file, or stdin path.
- Prompt only when the relevant input/output streams are interactive. Provide
  `--no-input` or an equivalent mode that never prompts and fails with a clear
  non-interactive remedy.
- Hide terminal echo for password prompts. Never accept secrets through argv or
  ordinary environment variables when a protected file, stdin, descriptor,
  credential facility, or IPC mechanism is available.
- Match confirmation to risk. Use a normal prompt or explicit force flag for
  moderate mutations, a truthful dry run for complex work, and typed resource
  confirmation for severe or difficult-to-undo actions. Dry run must not perform
  the writes, network calls, or child effects it claims to omit.
- Keep Ctrl-C and equivalent cancellation responsive. Bound cleanup, explain
  escalation when a second interrupt forces termination, and make it clear how
  to escape an interactive child or wrapper.

### Configuration and environment

- Define one precedence order and test it. A useful default is flags, process
  environment, project configuration, user configuration, system configuration,
  then built-in defaults.
- Use flags for invocation-specific choices, environment variables for
  context-dependent choices, and version-controlled project configuration for
  stable team-wide behavior. Keep user and system configuration scoped and
  discoverable rather than scanning arbitrary locations.
- Follow XDG Base Directory roles on platforms that support them. Keep durable
  data, state, cache, and runtime coordination in their semantic locations.
- Use portable uppercase environment names, avoid commandeering standard names,
  and honor relevant conventions such as `NO_COLOR`, proxy variables, `PAGER`,
  `EDITOR`, and `TMPDIR` where the behavior genuinely applies.
- Treat `.env` as a limited convenience, not a substitute for structured
  configuration or secret storage. Never log secret values or expose them in
  diagnostics.

### Robustness and compatibility

- Acknowledge promptly before long work. Add bounded, configurable timeouts to
  network and other potentially blocking operations; do not hang indefinitely.
- Make transient failures resumable or safely retryable where possible. Use
  atomic state transitions and avoid requiring cleanup that cannot survive
  interruption, power loss, or forced termination.
- Keep concurrent work bounded and its output deterministic or clearly grouped.
  Do not trade a faster implementation for an unreadable or misleading UI.
- Treat command names, flags, environment variables, config files, output
  formats, and statuses as compatibility surfaces. Prefer additive changes;
  warn and document before removing or changing an established interface.
- Allow human output to improve over time, but direct automation to explicit
  `--plain` or machine formats. Do not create compatibility traps with implicit
  abbreviations or a positional catch-all.
- Distribute through a predictable artifact or the platform's native package
  manager, and make installation and removal straightforward. Do not make
  runtime downloads, self-installation, or self-update the normal path.
- Do not phone home usage or crash data without informed consent. Prefer docs,
  downloads, and direct user feedback over surprising background telemetry.

### Testing checklist

- Test the executable as a process and assert stdout, stderr, and exit status
  separately.
- Cover no arguments, help/version, invalid syntax, every important option
  relationship, examples, machine and human formats, empty output, broken
  pipes, and likely error remedies.
- Cover TTY and non-TTY behavior, color policy, prompts and `--no-input`,
  password handling, cancellation, timeouts, child failures, and large output
  when applicable.
- Isolate tests from the developer's home, real configuration, network, and
  ambient environment unless an integration test explicitly requires them.
- Test precedence, repeated/concurrent invocation, idempotence, dry-run
  truthfulness, destructive safeguards, generated completions/manuals, and
  packaged runtime dependencies when those surfaces exist.

## Rust implementation (conditional)

Apply this section only when the CLI executable is implemented in Rust. Do not
carry its crate names, Rust APIs, or Cargo commands into non-Rust projects.

- Inspect `Cargo.toml`, the tracked `Cargo.lock`, Rust edition, MSRV, workspace
  structure, existing error types, argument model, tests, and package/flake
  expressions before proposing a crate or API.
- Prefer the project's existing dependencies. For a new dependency, verify its
  maintenance, license, MSRV, lockfile impact, and repository policy first.
- Prefer typed `clap` derive types (`Parser`, `Subcommand`, `Args`, and
  `ValueEnum`) for the command grammar. Keep I/O and domain validation after
  parsing, and inspect the pinned `clap` version before using new APIs.
- Preserve native Unix values with `Path`/`PathBuf`, `OsStr`/`OsString`,
  `args_os`, and native `Command` arguments. Convert to Unicode only at an
  explicitly textual boundary.
- Use `std::io::IsTerminal` for stream decisions, return `ExitCode` or
  `Termination` at the process boundary, and keep `process::exit` out of domain
  code. Use the project's established terminal, error, and serialization
  libraries rather than assembling protocols by hand.
- Spawn children with `std::process::Command` and separate arguments. Choose
  stdio deliberately, drain piped output without deadlock, reap children, and
  define cancellation and descendant ownership before spawning.
- Keep parser, validation, domain, rendering, and entry/exit code separable.
  Combine focused Rust tests with process-level assertions for the public CLI.
- When the project uses Nix packaging, follow its existing declarative Rust
  derivation and immutable-store conventions. Package locked dependencies,
  completions, manuals, and runtime executables explicitly; do not rely on
  `cargo install`, runtime downloads, or self-update.
- When changing Nix packaging or non-trivial wrapper scripts, follow the
  project's Nix and shell conventions in addition to this skill.

For Rust CLIs, read these conditional Rust notes as needed; the guidance
above applies to any language:

- [Rust interface and arguments](references/rust-interface-and-arguments.md)
  when defining or changing the command surface.
- [Rust output, errors, and exit status](references/rust-output-errors-and-exit-status.md)
  when changing rendering, machine output, prompts, error libraries, or status
  codes.
- [Rust processes, configuration, and safety](references/rust-processes-config-and-safety.md)
  when invoking children, handling signals, writing files, or adding XDG/config
  behavior. Follow the platform's conventions for low-level Linux integration, and use `/rust-async`
  for runtime-specific async cancellation or subprocess work when available.
- [Rust testing and packaging](references/rust-testing-and-packaging.md)
  before finishing a public Rust CLI or changing its package.

## Avoid

- Hand-written argument scanning when a maintained parser fits.
- Making human prose, color, progress, or logs double as a machine protocol.
- Enabling prompts, color, animation, or pagers merely because stdin is open.
- Hiding side effects behind defaults, guessed corrections, or undocumented
  config discovery.
- Passing secrets in argv, logs, or ordinary environment variables.
- Spawning a shell for ordinary argument passing.
- Capturing unbounded output, waiting without draining pipes, or ignoring
  cancellation and timeouts.
- Adding a dependency or changing a public interface without checking the
  project's policy and compatibility boundary.
