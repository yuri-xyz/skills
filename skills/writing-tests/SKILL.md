---
name: writing-tests
description: Use when writing or changing tests.
---

# Writing Tests

## Objective

Write tests that provide durable evidence about a behavior or contract. A test
should make a likely regression easier to detect and diagnose, without tying the
suite to one developer's machine, incidental implementation details, or a
large amount of brittle setup.

Use this skill when adding tests, deciding which test layer to use, reviewing
test quality, or expanding coverage around a bug or feature.

## The test-worthiness check

Before adding a test, answer these questions:

1. What observable behavior or invariant is the test specifying?
2. What plausible regression or failure would it catch?
3. Would the test fail if that regression were introduced?
4. Is this behavior already covered by an existing test?
5. Can the behavior be proved with a smaller, faster, more isolated test?

If there is no clear answer, do not add the test yet. Do not add tests merely
to increase a coverage percentage, repeat an assertion that adds no new
confidence, or restate an implementation line by line.

## Choose the smallest useful test scope

Prefer the narrowest test layer that can prove the contract:

1. **Unit test** — Use for pure functions, parsers, validators, state
   transitions, formatters, policy decisions, and other logic that can be
   exercised with injected or in-memory collaborators. Unit tests should be
   the foundation: fast, isolated, repeatable, and numerous enough to cover
   meaningful behavior.
2. **Integration test** — Use when the contract is specifically at a module,
   process, filesystem, database, protocol, or public API boundary and a unit
   double would not prove it. Keep the boundary explicit and the fixture
   controlled.
3. **Smoke test** — Use sparingly for one high-value wiring, startup, health,
   or availability claim that lower-level tests cannot establish. A smoke test
   should assert meaningful behavior, not merely that a process starts. Do not
   use a growing collection of smoke tests as a substitute for unit coverage.
4. **End-to-end test** — Use only when the user-visible or cross-system
   behavior cannot be meaningfully proved at a lower layer. Keep these few,
   intentional, and clearly justified because they are slower and more
   failure-prone.

Do not duplicate the same scenario at every layer without a distinct contract
at each boundary. A test pyramid is a useful default: many small unit tests,
some boundary tests, and few high-level tests. It is a heuristic, not a reason
to force a unit test where the real boundary is the behavior under test.

## Keep tests generic and hermetic

Tests must not depend on the current machine, user account, checkout path, or
hardware. Do not put real machine facts into fixtures, snapshots, expected
values, or test names, including:

- the user's username, real name, email, `$HOME`, the current working
  directory, or personal filesystem paths;
- hostnames, machine IDs, boot IDs, mount points, local network addresses,
  environment variables, or machine-specific timestamps;
- CPU, GPU, kernel, display, disk, memory, device, serial-number, or other
  hardware-identifying facts;
- live `/proc`, `/sys`, device nodes, mounted disks, real services, or external
  network responses in ordinary unit tests.

Use generic, obviously inert data when those shapes matter: conventional
placeholder identities such as `alice`, `bob`, and `alice@example.com`;
reserved names such as `example.invalid` and documentation addresses such as
`192.0.2.1`; and synthetic values such as `test-device` and `fixture-serial`.
If the feature parses a system, protocol, or vendor format, use a minimal
synthetic fixture that resembles the format rather than copying an
individual's actual output.

When a real filesystem or process boundary is the contract, create paths under
a fresh temporary directory from the language's standard library or the test
harness (for example Python's `tempfile.TemporaryDirectory`, Go's `t.TempDir`,
or the repository's existing temp-dir helper) and derive every expected path
from it rather than hardcoding one. Use a controlled fake process for
subprocess boundaries. Never read from or write to the user's home, the
checkout, live mounts, or the active system just to make a test pass. For
resource behavior, inject a small, deterministic quota or fake resource
provider instead of relying on the machine's available memory, disk, CPU,
devices, or network.

Control other sources of nondeterminism:

- inject clocks and use fixed timestamps;
- inject random generators and fixed seeds, or test the random boundary with a
  deterministic fake;
- replace network, subprocess, database, filesystem, and hardware discovery
  with fakes, stubs, or local fixtures at unit-test scope;
- avoid sleep-based synchronization and uncontrolled concurrency;
- make each test independent, repeatable, and safe to run alone or in any
  order;
- clean up resources and temporary state even when assertions fail.

Tests that intentionally require a real external service, machine, or device
must be separately labeled, opt-in where the project supports that convention,
and documented as integration or hardware tests. They must not silently become
the default unit suite.

## Keep tests automated and free of host side effects

Running the test suite must be fully unattended and must not visibly change or
depend on the host session. A developer running tests should never see
anything appear on their desktop or be asked to do anything.

- Do not open windows, GUIs, dialogs, popups, tray icons, desktop
  notifications, browser tabs, or file pickers on the host. Test UI logic
  through its view model, state, or rendering output; when a real window is
  the contract, run it against a headless or virtual display backend that the
  test owns, and keep such tests opt-in.
- Never require user interaction: no stdin prompts, confirmations, password,
  polkit, or keyring dialogs, OAuth or browser logins, hardware-key touches, or
  waiting for a click. Inject the answer or a fake authenticator instead. A
  test that could block on input must fail fast rather than hang.
- Do not alter host state: the clipboard, audio, displays, input devices,
  system or desktop settings, default applications, keyrings, user or system
  services, D-Bus or systemd units, firewall rules, package state, or shell and
  application configuration. Point such integrations at a fake or at an
  isolated instance the test starts and tears down.
- Do not launch real user applications or talk to the user's running session
  buses, agents, or daemons. Clear or override inherited session variables
  such as `DISPLAY`, `WAYLAND_DISPLAY`, and `DBUS_SESSION_BUS_ADDRESS` for
  subprocesses when the code under test could otherwise reach the live
  session.
- Do not depend on host state to pass: installed applications, logged-in
  accounts, existing config files, the current locale or timezone, a desktop
  session, or network availability. Set what the test needs explicitly.

## Design each test around behavior

Use a clear Arrange–Act–Assert or Given–When–Then structure:

- **Arrange** only the data and collaborators needed for the scenario.
- **Act** once on the behavior under test whenever practical.
- **Assert** the observable result, error, state transition, or externally
  meaningful side effect.

Test names should state the operation, scenario, and expected outcome, for
example `parse_empty_input_returns_no_entries` or
`enqueue_at_capacity_rejects_without_growing_the_queue`. A useful failure
should tell the next person which contract broke.

Prefer behavior and stable contract assertions over implementation details:

- assert returned values, public errors, persisted state, emitted events, or
  bounded side effects;
- do not assert private helper calls, incidental call order, internal data
  structures, or exact algorithms unless those are explicitly part of the
  contract;
- test private behavior through the public behavior that exposes it;
- assert stable error categories, codes, or structured fields rather than
  brittle prose when the exact message is not a contract;
- do not compute the expected value with the same algorithm as the production
  code, because the test can repeat the same bug.

Keep fixtures minimal. Every input field should either be required to arrange
the scenario or make the assertion clearer. Use named constants for values
whose meaning matters, and choose simple values that make the expected result
obvious. Avoid magic values, huge copied payloads, and snapshots that conceal
which behavior is being checked.

Avoid logic in tests. Do not reproduce production branching, parsing,
iteration, retries, or calculations inside the oracle. A declarative table of
small cases is fine when the framework reports the case that failed; split
cases into separate tests when setup or expected behavior differs enough to
make a failure ambiguous.

## Build an edge-case matrix

For each meaningful input or state dimension, consider the cases that expose
incorrect assumptions. Select the cases relevant to the contract rather than
blindly generating a large matrix.

### Boundaries and unexpected input

- empty, missing, null/nil, whitespace-only, and zero-item inputs;
- the smallest valid value, the largest valid value, just below and just above
  each limit, and negative or overflowing values where the type permits them;
- malformed syntax, invalid enum/tag values, duplicate entries, unexpected
  ordering, truncated data, unknown fields, and unsupported versions;
- unusually long strings, large collections, Unicode or escaping cases, and
  values containing spaces or shell metacharacters when those are relevant;
- invalid combinations of otherwise valid fields, not only individually
  invalid fields.

### Limits and resource exhaustion

If the code has a capacity, retry, timeout, pagination, output-size,
recursion, concurrency, queue, memory, or disk bound, test it explicitly:

- succeed at the limit and reject or stop at the first value beyond it;
- verify work, output, retries, and retained state remain bounded;
- simulate exhaustion with a tiny deterministic fake quota or failing
  allocator/provider, never with actual system exhaustion;
- assert that resources are released and later operations remain usable;
- verify the failure is explicit and safe rather than silently truncating,
  looping, or allocating without bound.

### Partial failure, cancellation, and recovery

Ask what happens if an operation stops at each meaningful checkpoint:

- the dependency fails before any work, midway through work, or immediately
  after a side effect;
- a timeout, cancellation, process exit, broken connection, malformed response,
  or retry limit occurs;
- cleanup, rollback, atomicity, idempotency, and previously committed state
  are preserved according to the contract;
- retrying does not duplicate side effects or lose acknowledged work;
- a failed operation leaves the object, queue, file, or session in a valid
  state and reports an actionable error.

For concurrent code, use deterministic coordination or a controllable fake to
exercise the important interleaving, cancellation, ownership, and race
invariants. Do not rely on sleeps or hope that a timing-sensitive race appears
in CI.

## Avoid low-value tests

Do not add or preserve tests that:

- only launch a binary, construct a default object, or assert that a trivial
  constant equals itself without checking meaningful behavior;
- duplicate an existing test with different irrelevant data;
- assert a getter, setter, pass-through wrapper, or framework behavior with no
  project-specific contract;
- mirror private implementation steps so closely that a harmless refactor
  breaks the test;
- use a broad snapshot or end-to-end flow where a few focused assertions would
  identify the behavior more clearly;
- read live machine state or external services when a generic fixture would
  prove the same parser or decision logic;
- add a test that can pass while the intended behavior is broken.

Reuse the repository's existing test framework, fixtures, and helpers. Do not
add a dependency merely to make one test more convenient. If a helper hides the
scenario, simplify or specialize it rather than adding layers of setup.

## Workflow

1. Inspect the public contract, nearby tests, existing fixtures, and the
   repository's test commands before writing anything.
2. Identify the smallest test scope and write down the behavior and likely bug
   it protects against.
3. Choose minimal synthetic inputs and inject environmental, time, random,
   process, network, hardware, and resource dependencies.
4. Add the normal case only when it establishes a meaningful contract, then
   prioritize relevant boundaries, invalid inputs, limits, and failure states.
5. Keep each test focused, deterministic, independently runnable, and clear
   about its expected outcome.
6. Run the focused unit test first, then the narrowest relevant integration or
   broader suite. Do not replace assertion-based verification with a smoke
   run.
7. Review every new test with the test-worthiness check. Remove redundant
   setup and cases that do not add distinct confidence.

## Review checklist

Before considering test work complete, confirm:

- [ ] Each test names a behavior or invariant and a plausible regression.
- [ ] Unit scope is used wherever it can prove the behavior.
- [ ] Integration, smoke, and end-to-end tests each cover a distinct boundary.
- [ ] Fixtures contain no real username, path, host, machine ID, timestamp, or
      hardware identity; filesystem tests use fresh temporary directories.
- [ ] Tests are isolated, deterministic, repeatable, and safe in parallel.
- [ ] Tests run unattended: no windows, popups, notifications, prompts, or
      other user interaction, and no changes to host or session state.
- [ ] Normal, boundary, invalid, exhaustion, partial-failure, and recovery
      cases are covered where relevant.
- [ ] Limits are tested with deterministic small quotas, not actual exhaustion.
- [ ] Assertions check behavior and stable contracts rather than implementation
      details or tautological calculations.
- [ ] Test logic is simpler than the production logic it verifies.
- [ ] Failure output identifies the broken scenario without requiring a human
      to inspect logs or rerun the application manually.

## Research basis

This guidance is informed by:

- [Microsoft Learn: Best practices for writing unit tests](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices)
  (fast, isolated, repeatable, minimal, behavior-focused tests; infrastructure
  belongs at integration scope; coverage percentage alone is not quality).
- [The Rust Programming Language: How to Write Tests](https://doc.rust-lang.org/book/ch11-01-writing-tests.html)
  and [Test Organization](https://doc.rust-lang.org/book/ch11-03-test-organization.html)
  (Arrange–Act–Assert structure and the distinction between focused unit and
  public-interface integration tests).
- [GoogleTest Primer: Why GoogleTest?](https://google.github.io/googletest/primer.html)
  (independent, repeatable, portable, informative, and fast tests).
- [Martin Fowler: The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
  (many small tests, some coarse-grained tests, and few high-level tests as a
  practical heuristic).
