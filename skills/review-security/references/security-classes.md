# Security classes

Trace each untrusted source through every class that applies. For each, ask
who the attacker is, what input they control, and what it gets them.

## Injection and code execution

- Shell commands built from strings with untrusted parts; `sh -c`,
  `system`, `exec` with interpolation; word splitting and globbing; arguments
  starting with `-` read as options.
- `eval`, `Function`, `exec`, dynamic `import` or `require`, template engines
  rendering untrusted templates, and expression languages.
- SQL, NoSQL, LDAP, XPath, GraphQL, and regex built by concatenation.
- Unsafe deserialization: `pickle`, Java serialization, YAML with object
  tags, `Marshal`, and formats that instantiate types from input.
- Loading code or config from writable or untrusted locations: plugins,
  `PATH` or library search paths, the current directory, `LD_PRELOAD`,
  `.env` files, and auto-run hooks.
- Downloading and running code without pinning and verification.

## Memory safety

- Buffer overflows and over-reads from unchecked lengths, off-by-one bounds,
  and missing NUL terminators.
- Integer overflow or truncation in size, offset, and allocation math
  that leads to a short allocation or an out-of-bounds write.
- Use-after-free, double free, dangling references, and uninitialized memory.
- Format strings taken from input.
- `unsafe` blocks, FFI boundaries, and raw pointer arithmetic whose
  invariants are not documented and checked.

## Bounds and resource exhaustion

- Length, count, and range checks that are off by one, done in the wrong unit,
  done after the work, or skippable on some path.
- Attacker-controlled sizes, depths, counts, and loop bounds without limits:
  nested payloads, huge allocations, decompression and archive bombs, XML
  entity expansion, and pagination.
- Regular expressions with catastrophic backtracking on attacker input.
- Unlimited requests, connections, retries, or expensive operations per
  client; missing timeouts.
- Hash flooding when untrusted keys feed hash maps without a randomized hash.

## Paths and files

- Path traversal: `..`, absolute paths, and encoded separators escaping a root;
  checks done before canonicalization.
- Archive extraction writing outside the target (zip slip), including
  symlink and hardlink entries.
- Symlink following and TOCTOU races between check and use; predictable
  temp file names; files created world-readable or world-writable.
- Deleting or overwriting paths built from input without a scope check.

## Web and network

For servers and APIs, `/review-http-security` covers these in depth.


- Cross-site scripting from untrusted data rendered without contextual
  encoding; unsafe HTML sinks such as `innerHTML` and `dangerouslySetInnerHTML`.
- Server-side request forgery: fetching user-supplied URLs that reach internal
  hosts, loopback, link-local metadata endpoints, or other schemes; redirects
  and DNS rebinding bypassing the check.
- CSRF on state-changing requests; permissive CORS with credentials.
- Open redirects, header injection through CR/LF, and request smuggling from
  inconsistent parsing.
- Local services bound to all interfaces, or to loopback without
  authentication when other local users or browsers can reach them.

## Defense in depth on critical paths

Authentication, authorization, payments, secrets, deletion, privilege
changes, and other critical paths must not rest on a single check. Treat
"this can't happen" as something to assert, not assume.

- A single gate: the only authorization check lives in one middleware,
  router, or caller, so a new route, refactor, background job, or internal
  call path skips it. Re-check at the point of action, close to the data,
  such as an ownership check in the data-access layer as well as the route.
- Impossible states left unchecked: an unauthenticated user reaching a
  handler behind auth, a session with no user, a user with no tenant, an
  object whose owner does not match the caller, a role outside the known set,
  or a negative amount. Assert these explicitly and fail closed with a
  logged, alertable error instead of continuing.
- Fail-open defaults: `switch` or `match` without a denying default, role
  checks written as "deny if admin is false" instead of "allow only if",
  missing values treated as permitted, and exceptions caught and ignored
  around a check.
- Checks that trust earlier layers: handlers relying on the client, the
  proxy, the API gateway, or a previous step to have validated identity,
  scope, or input, with nothing re-verified where it matters.
- Inconsistent checks: the same rule implemented differently in two places,
  so they drift; prefer one shared policy function called from every layer.
- Missing invariants in critical state changes: balance, ownership, quota,
  and state-machine transitions not validated before and after the change,
  and not done atomically.
- No signal when a check fires: an impossible-state assertion or a denied
  privileged action that is silent instead of logged for audit and alerting.

## Authentication and authorization

- Missing authorization on some path to an action: alternate routes, bulk
  endpoints, background jobs, and direct object references by ID (IDOR).
- Checks done on the client only, or on attacker-controlled fields such as
  user IDs, roles, or tenant IDs in the request.
- Session and token handling: no expiry or revocation, tokens in URLs or logs,
  predictable identifiers, and missing rotation after a privilege change.
- Fail-open logic: an error, timeout, or missing value that grants access.
- Comparing secrets with non-constant-time equality.

## Secrets and data exposure

- Secrets in source, logs, error messages, command lines, environment
  dumps, crash reports, or files with loose permissions.
- Verbose errors and stack traces returned to clients.
- Sensitive data in caches, temp files, or backups without cleanup.

## Cryptography and randomness

- Non-cryptographic randomness for tokens, IDs, nonces, or keys.
- Homemade crypto, disabled certificate verification, weak or deprecated
  algorithms, and reused nonces. Hand cryptographic code to
  `/review-cryptography`.

## Privilege and isolation

- Running with more privilege than needed: root, broad capabilities,
  setuid, wide tokens, or full filesystem access.
- Dropping privileges in the wrong order or not at all after setup.
- Sandboxes, containers, or permission checks that a symlink, an inherited
  file descriptor or environment variable, or an exposed socket bypasses.

## Parsing and confusion

- Two components parsing the same input differently: URLs, paths, headers,
  JSON with duplicate keys, Unicode normalization, and case folding.
- Type confusion from loose comparisons or coercion, such as `"0" == false`
  or prototype pollution through merged objects.
- Unicode tricks: homoglyphs, bidirectional overrides, and invisible
  characters in identifiers, filenames, and displayed names.

## Missing tests

Security-relevant code needs tests that feed it hostile input: traversal
paths, injection payloads, oversized and deeply nested input, malformed
encodings, missing or forged credentials, and other users' object IDs.
Prefer fuzzing or property-based tests where the project already uses them.
