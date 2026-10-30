---
name: review-http-security
description: Use when reviewing HTTP servers, APIs, or their hosting configuration for hardening gaps, such as authentication, authorization, input parsing, uploads, CORS, headers, cookies, limits, SSRF, redirects, TLS, proxy trust, or exposed endpoints and metadata.
---

# Review HTTP Security

## Objective

Review the current or proposed changes to an HTTP server, API, or the
configuration that hosts it (reverse proxy, CDN or edge worker, container,
systemd unit, or platform config) for hardening gaps a remote client could
exploit. Find them by walking each route and each layer between the internet
and the handler, naming the request an attacker sends and what it gets them,
and prove each one with a failing test or a specific request before fixing
it.

Judge everything by least trust and least exposure: treat every request as
hostile until parsed and authorized, return only what the client needs, with
errors that are short, generic, and free of internals, and advertise nothing
about the server's software, versions, or topology.

This is the HTTP specialization of `/review-security`, which still covers
general injection, memory safety, and file handling inside handlers. Use
`/review-cryptography` for token and session cryptography, and `/openapi` for
API contract design.

## Workflow

1. Inspect the recent diff, pending plan, or relevant files, and map the
   surface: every route and method, who may call it, what it reads and
   changes, and the layers in front of it: TLS termination, reverse proxy,
   CDN or edge, load balancer, and the platform's own settings.
2. Note the deployment facts that change the answers: public or internal,
   browser clients or machine clients, cookies or bearer tokens, single or
   multi-tenant, and which layer owns TLS, limits, and headers. Read the
   actual proxy and platform config instead of assuming defaults.
3. Walk the surface through the classes in `references/http-classes.md`.
   For each candidate, name the attacker (anonymous internet client, signed-in
   user of another tenant, malicious site in the victim's browser, or a
   client on the internal network), the request, and the impact. Drop
   candidates no attacker can reach, such as a header the proxy already sets
   and the app cannot bypass.
4. Check the tests: unauthenticated and cross-tenant requests to every
   protected route, oversized, malformed, and type-confused bodies and uploads,
   hostile origins, and
   redirect and SSRF targets. Note the missing ones.
5. Fix a gap when it is confirmed, local, and the right behavior is clear:
   write a failing test first when the project has tests, fix it at the layer
   that owns the concern, and watch the test pass. Prefer the framework's or
   proxy's built-in mechanism over hand-written middleware.
6. Report, without fixing, gaps whose fix changes authentication, the public
   API, client compatibility (such as tightening CORS or CSP), or deployed
   infrastructure; those need the user. Never probe live production endpoints
   or change live hosting settings; report what to change instead.
7. Run the focused tests and checks for the changed code.

## Prefer Fixes Like

- Layered checks on auth and other critical paths: authorization at the
  route and again where data is read or changed, assertions for states that
  should be impossible, and fail-closed errors that are logged.
- Default-deny routing: authentication and authorization applied by the
  router or a middleware every route passes through, with explicit public
  exceptions.
- Limits set once, at the layer that sees the request first, and matched or
  tightened behind it: body size, header size, timeouts, rate limits, and
  concurrency.
- Parsing every request once, at the edge, with the project's schema or
  validation library into typed values, rejecting unknown, duplicate, and
  out-of-range input instead of coercing it.
- Allowlists for CORS origins, redirect targets, outbound hosts, and
  content types.
- Security headers and cookie flags set in one place for every response.
- Trusting forwarded headers only from known proxies, configured explicitly.
- Least exposure: generic, concise error responses with a stable code and a
  request ID, details kept in server logs, and explicit output schemas that
  return only the fields the caller needs.
- No fingerprints: banner and version headers removed, and default error and
  status pages replaced at every layer.

## Avoid

- Duplicating a configured limit or header at every layer with different
  values, so nobody knows which one applies. Layered authorization and
  invariant checks on critical paths are different: keep them, and share one
  policy between the layers.
- CSP, CORS, or cookie changes that break existing clients without the
  user's agreement.
- Security through obscurity, such as hidden routes or unusual ports, in
  place of authentication.
- Logging credentials, tokens, cookies, or full request bodies while fixing.

## Output

If no gap was found, say so and name the routes, layers, and classes
reviewed.

Otherwise list findings, most severe first:

```markdown
- 🔴 <file:line or config> <class>: <attacker> sends <request> → <impact>. Fixed; regression test `<name>`.
- 🟡 <file:line or config> <class>: <attacker> sends <request> → <impact>. Not fixed: <why>.
- 🔵 <file:line or config> Hardening: <missing defense or test>. Added / not added: <why>.
```

🔴 unauthenticated access to data or actions, cross-tenant access, account
takeover, SSRF to internal services, or an exposed admin or debug surface;
🟡 needs a victim's interaction or unusual conditions, such as CSRF, XSS
through a missing header, or denial of service from a missing limit; 🔵
defense in depth or a missing test. Finish with the checks run, or why none
were.
