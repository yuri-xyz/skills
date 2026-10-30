---
name: review-critical-paths
description: Use when the user wants an application's most critical code paths, such as authentication, API routes, input parsing, payments, secrets, privilege changes, and data deletion, found and reviewed.
---

# Review Critical Paths

## Objective

Spend review effort where a bug hurts most. First find the code paths whose
failure would let an attacker in, leak or destroy data, lose money, or take
the system down, based on what the application actually is. Then review each
path with every review lens that applies to it, and report one ranked list.

This skill orchestrates; the lenses own their checklists, fix rules, and
severity scales. Unlike them, it reviews the existing code on the critical
paths, not only the recent diff.

## Workflow

### 1. Understand the application

Work out what kind of software this is and who can reach it: read
`AGENTS.md`, `.spec/`, the README, manifests, entry points, routing, and
deployment config. Note the trust boundaries (internet, other tenants, local
users, files, plugins), the assets worth protecting (accounts, credentials,
money, personal data, the host itself), and the deployment, such as public
web, internal service, CLI, desktop app, or library.

### 2. Locate the critical paths

Use `references/critical-paths.md` for the application's kind, and expand it
with whatever this application has that the list misses. Find each path in
the code with search, routing tables, call graphs, and tests, following it
from the entry point through to where data is read, changed, or sent.

Rank the paths by impact times exposure: what an attacker or a bug gains on
that path, and how reachable it is. Write the map before reviewing:

```markdown
| # | Path | Entry → sink | Why critical | Lenses |
|---|---|---|---|---|
| 1 | Login | `POST /login` → `auth/session.ts` | Account takeover | security, http, crypto, bugs |
```

When there are more than about ten paths, review the top ten and list the
rest as not reviewed, so the user can ask for them.

### 3. Review each path with the lenses that apply

For each path in rank order, apply every lens that fits, following that
skill's workflow on the path's code:

- `/review-security` on every critical path, including its "Defense in depth
  on critical paths" section.
- `/review-http-security` when the path is served over HTTP or sits behind a
  proxy, edge, or hosting config.
- `/review-cryptography` when the path hashes, encrypts, signs, verifies,
  derives keys, stores passwords, or generates secrets or tokens.
- `/review-bugs` on every critical path, focused on parsing, bounds,
  arithmetic, and the edge cases its inputs can reach.

Report a finding once, under the lens that owns it, even when several lenses
see it. Follow each lens's rules on what to fix directly and what to report;
fix nothing that changes authentication, the security model, data formats,
or public behavior without the user.

### 4. Check coverage

For each path, note whether tests exercise its hostile and edge cases, and
add the missing ones the lenses call for when they are cheap and local.

## Output

1. **Application:** kind, trust boundaries, and assets, in two or three lines.
2. **Critical path map:** the table from step 2, plus the paths not reviewed.
3. **Findings:** one list across all paths and lenses, most severe first, in
   the lenses' shared format, each tagged with its path number and lens:

```markdown
- 🔴 [#1 security] <file:line> <class>: <attacker> sends <input> → <impact>. Fixed; regression test `<name>`.
- 🟡 [#3 bugs] <file:line> <class>: <input> → <what happens>. Not fixed: <why>.
```

4. **Paths with no findings,** with the lenses applied, so a clean result is
   visible rather than implied.
5. **Checks run,** or why none were.

## Boundaries

- Read-only toward live systems: never probe production endpoints, real
  accounts, or payment providers.
- Large fixes, migrations, and security model changes are reported, not made.
- Do not commit unless the user asks; then use `/git-commit`.
