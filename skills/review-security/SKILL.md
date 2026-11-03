---
name: review-security
description: Use when reviewing code changes for security oversights, such as injection, remote code execution, memory corruption, path traversal, broken authorization, unsafe deserialization, or secret exposure, or when auditing this machine or a project for recent CVEs, supply-chain compromises, or indicators of compromise.
---

# Review Security

## Objective

Find security holes an attacker could reach, in two modes. In code review,
review the current or proposed code changes: where untrusted data crosses a
trust boundary and what it can make the code do. Find holes by tracing
concrete attacker-controlled input to a dangerous sink, not by pattern
matching, and prove each one with a failing test or a specific input before
fixing it. In an exposure audit, check this machine or a project against
recent security incidents.

For deliberate malware in a dependency, use `/review-malware`; for
cryptography code, `/review-cryptography`; for HTTP servers, APIs, and their
hosting configuration, `/review-http-security`.

## Modes

- **Code review** (default): code, a diff, or a plan is in focus. Follow the
  workflow below.
- **Exposure audit**: the user asks whether recent CVEs, supply-chain
  compromises, or trust-store incidents affect this machine or a project, or
  asks for a security audit of the system. Follow
  `references/exposure-audit.md` instead, and use its report format.

When the user asks for both, run the exposure audit first, then the code
review, and report them separately.

## Code review workflow

1. Inspect the recent diff, pending plan, or relevant files, and map the trust
   boundaries they touch: network requests, IPC, files, archives, environment,
   command-line arguments, clipboard, plugins, other users, and data read back
   from storage another party can write.
2. List the sinks the untrusted data can reach: shells and process spawning,
   `eval` and template engines, SQL and other query languages, deserializers,
   file paths and filesystem operations, URLs and outbound requests, HTML and
   logs, memory and size arithmetic, and privilege or permission changes.
3. Trace each source to its sinks through the classes in
   `references/security-classes.md`. For each candidate, name the attacker,
   the input they control, and the impact: code execution, data read or
   written, privilege gained, denial of service, or secret leaked. Drop
   candidates no attacker can reach.
4. Check the defenses: validation at the boundary, authorization on every
   path to the action, and tests that feed hostile input to each risky path.
   Note the missing tests.
5. Fix a hole when it is confirmed, local, and the right behavior is clear:
   write a failing regression test first when the project has tests, fix it
   at the boundary or sink, and watch the test pass.
6. Report, without fixing, holes whose fix changes the security model,
   authentication, data formats, or public behavior; those are human
   decisions. Report anything already exploitable in released or deployed
   code as urgent, and do not test it against live systems.
7. Run the focused tests and checks for the changed code.

## Prefer Fixes Like

- Layered checks on critical paths: authorization at the entry point and
  again at the point of action, explicit assertions for states that should
  be impossible, and fail-closed handling that logs when one fires.
- Structured APIs instead of string building: argument arrays instead of
  shell strings, parameterized queries, contextual output encoding, typed URL
  and path builders.
- Allowlists over denylists, and canonicalizing before checking, such as
  resolving a path before confirming it stays under its root.
- Explicit size, depth, count, rate, and time limits on attacker-controlled
  work, failing closed with a clear error.
- Authorization checked where the action happens, on every path to it, with
  default deny.
- Least privilege: narrower file modes, scopes, capabilities, and tokens.
- Safe library primitives already in the project over hand-rolled ones.

## Avoid

- Fixing a hole by escaping or filtering at the wrong layer, or by a denylist
  an attacker can route around.
- Security theater: checks that cannot fail, or that the attacker controls.
- Logging or echoing secrets or attacker input while fixing.
- Broad rewrites or new dependencies without approval; follow
  `/dependency-add` for any new library.
- Overlapping other lenses: plain correctness bugs belong to `/review-bugs`
  unless an attacker can trigger them for impact; data collection and
  telemetry belong to `/review-privacy`.

## Code review output

If no hole was found, say so and name the trust boundaries and classes
reviewed.

Otherwise list findings, most severe first:

```markdown
- 🔴 <file:line> <class>: <attacker> sends <input> → <impact>. Fixed; regression test `<name>`.
- 🟡 <file:line> <class>: <attacker> sends <input> → <impact>. Not fixed: <why>.
- 🔵 <file:line> Hardening: <missing defense or test>. Added / not added: <why>.
```

🔴 code execution, authentication or authorization bypass, secret or data
exposure, or memory corruption reachable by an attacker; 🟡 limited impact or
needing unusual conditions, such as denial of service or a local-only attack;
🔵 defense in depth or a missing test with no known exploit. Finish with the
checks run, or why none were.
