# HTTP security classes

Walk every route and every layer through each class that applies. For each,
ask who the attacker is, what request they send, and what it gets them.

## Authentication

- Routes reachable without authentication that should require it, including
  new routes, alternate methods (`HEAD`, `OPTIONS`, method override headers),
  trailing-slash or case variants, and versioned or legacy paths.
- Auth enforced in one router or middleware stack but not in another, such as
  WebSocket upgrades, file downloads, GraphQL, RPC, or health and metrics
  servers.
- Tokens accepted from query strings, missing expiry or revocation, weak
  session IDs, sessions not rotated on login or privilege change, and logout
  that does not invalidate the server-side session.
- Missing brute-force protection on login, password reset, MFA, and API key
  endpoints; account enumeration through different responses or timing.
- Password reset and email verification links that are guessable, reusable,
  long-lived, or built from the request's `Host` header.

## Authorization

Apply `/review-security`'s "Defense in depth on critical paths" to every
authentication and authorization path: no single gate, impossible states
asserted, fail closed.

- Auth checked only in route middleware, with handlers, services, and queries
  assuming a valid caller; re-check identity, tenant, and ownership where the
  data is read or changed, for example by scoping every query to the caller's
  tenant.
- Object access by ID without an ownership or tenant check (IDOR / BOLA),
  including nested resources and bulk endpoints.
- Function-level gaps: admin actions protected only by hiding them in the UI.
- Mass assignment: request bodies bound directly to models, letting clients
  set roles, owners, prices, or flags.
- Authorization decided from client-supplied fields such as user ID, role, or
  tenant in the body or headers.

## Browser-facing protections

- CORS: reflected or wildcard origins with credentials, `null` origin allowed,
  origin matching by substring or unanchored regex, and preflight caching too
  long.
- CSRF on cookie-authenticated state-changing requests: missing tokens,
  `SameSite` not set, state changes on `GET`.
- Cookies without `Secure`, `HttpOnly`, and an appropriate `SameSite`; overly
  broad `Domain` or `Path`; missing `__Host-` prefix where it fits.
- Missing or weak headers: `Content-Security-Policy`,
  `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`,
  `frame-ancestors` or `X-Frame-Options`, `Referrer-Policy`, and
  `Permissions-Policy`; CSP with `unsafe-inline` or wildcard sources.
- Content type sniffing and user uploads served from the main origin with a
  renderable type; missing `Content-Disposition: attachment` for downloads.
- Open redirects through `next`, `returnTo`, or `redirect` parameters.

## Input and request limits

- Missing or very large limits on body size, multipart parts and file sizes,
  header size and count, URL length, JSON depth, array lengths, and query
  complexity (GraphQL depth and cost).
- Missing timeouts: header read (slowloris), body read, handler, idle
  keep-alive, upstream calls, and WebSocket idle.
- No rate limiting or concurrency caps on expensive or abusable endpoints:
  login, signup, search, export, upload, email or SMS sending, and AI or
  paid upstream calls.
- Pagination without a maximum page size; unbounded fan-out per request.
- Content type not enforced, so a parser the handler did not expect runs.

## Parsing user-submitted data

- No schema validation at the edge: handlers reading raw request objects
  instead of parsing once into typed values, with unknown fields rejected or
  dropped deliberately.
- Lenient parsing and type coercion: `"1"` versus `1`, `"true"` versus
  `true`, numbers beyond 2^53 or outside the target integer type, `NaN`,
  negative or zero where only positive values make sense, and empty strings
  treated as missing.
- Ambiguous input: duplicate JSON keys, repeated query parameters
  (`?id=1&id=2`) and array syntax (`a[]=`, `a[0]=`) that frameworks parse
  differently (parameter pollution), and the same field in the query, body,
  and path.
- Prototype pollution or object injection from merging parsed input into
  objects (`__proto__`, `constructor`), and NoSQL operator injection from
  objects where strings were expected (`{"$ne": null}`).
- Text input: invalid UTF-8, NUL bytes, control and bidirectional characters,
  Unicode normalization and lookalikes in usernames, emails, and slugs
  (account confusion), and length limits measured in the wrong unit.
- Format-specific fields: emails, URLs, phone numbers, dates, and time zones
  validated with ad hoc regexes, or not canonicalized before comparison and
  uniqueness checks.
- File uploads: trusting the client's filename, extension, or
  `Content-Type`; missing magic-byte checks; filenames used in paths;
  image and document parsing without dimension or page limits
  (decompression bombs, pixel floods); SVG, HTML, or PDF uploads served
  inline; archives extracted without entry, size, and path checks; and
  uploads not scanned or isolated when other users download them.
- Parsers with dangerous defaults: XML with external entities or DTDs
  enabled (XXE), YAML that constructs objects, CSV exported to spreadsheets
  without escaping leading `=`, `+`, `-`, `@` (formula injection), and
  Markdown or rich text rendered without sanitizing.
- User data reused later: stored input rendered in another user's browser,
  admin panel, email, log viewer, or PDF without encoding for that context
  (stored XSS and second-order injection).

## Server-side requests

- SSRF from user-supplied URLs (webhooks, link previews, imports, image
  fetches): reaching loopback, private ranges, link-local and cloud metadata
  endpoints, or other schemes; redirects and DNS rebinding bypassing the
  check.
- Outbound calls without timeouts or response size limits.
- Webhook receivers that do not verify signatures, timestamps, or replay.

## Proxies, hosts, and headers

- Trusting `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Forwarded-Host`, or
  `Forwarded` from any client, which spoofs client IPs for rate limits and
  logs, or the scheme and host for redirects and links.
- `Host` header not validated, enabling cache poisoning and poisoned reset
  links.
- Proxy and app parsing requests differently: request smuggling through
  `Content-Length` and `Transfer-Encoding`, path normalization differences
  (`..`, `%2e`, `;`, double slashes) bypassing proxy-level access rules.
- Cache keys that ignore auth or vary headers, caching private responses
  publicly; missing `Cache-Control: no-store` on sensitive responses.
- CR/LF in values placed into response headers.

## TLS and transport

- Plain HTTP accepted for authenticated traffic; missing HTTP-to-HTTPS
  redirect or HSTS.
- Outdated protocol versions or weak cipher suites at the terminating layer.
- Internal hops sending credentials in plaintext across untrusted networks.
- Certificate verification disabled on outbound calls.

## Exposure and configuration

- Admin panels, debug endpoints, profilers, metrics, health checks with
  details, API docs, and GraphQL introspection reachable from the internet.
- Debug mode and stack traces in production; banners and other
  fingerprinting are under "Server metadata and fingerprinting".
- Directory listing, served `.git`, `.env`, backup files, source maps, and
  build artifacts.
- Services bound to `0.0.0.0` that should be loopback or a private interface;
  databases and caches reachable without authentication.
- Default credentials, sample apps, and permissive platform defaults left on.
- Secrets in the repository, container images, client bundles, or
  environment exposed through error pages or diagnostics.

## Minimal responses and errors

Expose as little as possible, and trust the client as little as possible:
every byte a response returns is something an attacker can read, probe, and
compare.

- Exception messages, stack traces, SQL or ORM errors, upstream responses,
  file paths, hostnames, internal IPs, library names, or versions echoed in
  response bodies or headers, in production or behind a debug flag that can
  reach it.
- Errors more specific than the client needs: "user not found" versus "wrong
  password", "email already registered", or validation messages that reveal
  internal rules, field names, or other users' data. Return a short, stable
  error code and a generic message; give detail only where the client can act
  on it, such as which of its own fields failed validation.
- Status codes and timing that leak the same facts: `403` versus `404` for
  resources the caller may not know exist, and faster responses for unknown
  accounts.
- Input reflected back verbatim in errors or responses, which aids XSS,
  header injection, and probing; echo only what the client needs.
- Over-broad responses: whole database rows or model objects serialized
  instead of an explicit output schema, leaking internal IDs, hashes,
  timestamps, flags, or other users' fields; list endpoints returning more
  fields or records than the caller needs.
- Debug or diagnostic data in responses: request IDs are fine, but not
  internal timing, query plans, feature-flag states, or environment details.

Correlate a generic client error with full detail in server logs through a
request ID instead of putting the detail in the response.

## Server metadata and fingerprinting

Advertise nothing an attacker could use to pick an exploit: the less a
response says about the stack, the more an attacker has to guess.

- Banner headers naming software or versions: `Server`, `X-Powered-By`,
  `X-AspNet-Version`, `X-Generator`, `Via`, and framework, proxy, or platform
  headers such as `X-Runtime` or upstream and cache identifiers. Remove them,
  or reduce `Server` to a bare value where the server cannot drop it.
- Default error, 404, and maintenance pages from the framework, proxy, or
  platform that reveal the software by their markup; replace them with
  minimal custom pages or bodies at every layer, including the proxy's own
  errors such as `502` and `413`.
- Software and versions revealed elsewhere: generator `<meta>` tags, asset
  paths and filenames naming frameworks and versions, source maps, cookie
  names that identify the stack (`PHPSESSID`, `JSESSIONID`,
  `connect.sid`), and `ETag` formats that leak inode or build details.
- Version and build endpoints, health and status pages with dependency
  details, `/.well-known` or `/robots.txt` entries pointing at hidden areas,
  and API docs or schemas reachable without authentication.
- Internal topology: internal hostnames, IPs, ports, service names, region or
  node identifiers, and backend names in headers, redirects, cookies,
  certificates' subject alternative names, or error bodies.
- Responses to unusual requests (`TRACE`, `OPTIONS`, malformed HTTP, unknown
  hosts) that answer with the full stack's defaults; the default virtual host
  should return a minimal response, not a real site or a server welcome page.
- Hiding versions is defense in depth, not a fix: keep software patched
  regardless, and never rely on obscurity in place of authentication.

## Errors and logging

- Logs capturing passwords, tokens, cookies, `Authorization` headers, or full
  bodies; log injection through unescaped client input.
- Missing audit logs for authentication events and privileged actions.

## Runtime and hosting

- The server process running as root or with broad capabilities and
  filesystem access; missing systemd hardening, container user, or read-only
  root filesystem where the platform supports them.
- Writable paths shared between the web root and uploaded files.
- Missing resource limits for memory, file descriptors, and processes.

## Missing tests

HTTP security needs tests for unauthenticated and cross-tenant requests to
every protected route, hostile `Origin` and `Host` values, malformed, ambiguous,
and type-confused bodies and uploads, CSRF without a
token, oversized and deeply nested bodies, slow or never-finishing requests
where the framework allows, redirect and SSRF targets, and error responses
that must not leak details.
