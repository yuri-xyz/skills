# Threat Model and Review Method

## Define the privacy objective

Before searching, identify whose data is at risk and from whom:

- remote vendor, analytics provider, or unexpected third party;
- another local user or unprivileged process;
- administrator, device management, or centralized logging;
- later forensic recovery from the device;
- backups, snapshots, sync, search indexing, or cloud storage;
- accidental disclosure through diagnostics or support bundles.

State what functionality must remain. “No telemetry” can coexist with explicitly requested network features, but only if their traffic and data boundaries are understood.

## Build a data-flow inventory

Trace data through its complete lifecycle:

1. Input or generated identifier.
2. In-memory transformation or enrichment.
3. Local queue, cache, database, or log.
4. Serialization and destination selection.
5. Network, IPC, or filesystem sink.
6. Retry, retention, rotation, export, and deletion.

For each path, record purpose, default state, trigger, sensitivity, recipient, retention, and control. Include indirect processors such as crash handlers, SDKs, subprocesses, browser openers, D-Bus services, plugins, and operating-system collectors.

Use the principles of purpose limitation, data minimization, storage limitation, and confidentiality as review questions, not as legal conclusions.

## Static review

Inspect the actual version and build configuration:

- manifests, lockfiles, optional features, build scripts, and vendored code;
- application initialization and shutdown paths;
- HTTP, DNS, sockets, WebSockets, RPC, D-Bus, and child processes;
- analytics, metrics, tracing exporters, crash reporters, feedback, experiments, and remote configuration;
- hard-coded URLs, domains, DSNs, API keys, project identifiers, and user-agent strings;
- device/user/session IDs, fingerprint inputs, install timestamps, and correlation tokens;
- disk writers, log appenders, SQLite/LMDB stores, spool directories, and temporary files;
- configuration defaults, consent state, opt-out parsing, and failure/retry behavior.

Search terms reveal candidates, not conclusions. An SDK dependency can be unused; an endpoint can serve required functionality; dynamically constructed traffic can evade literal searches. Trace calls and feature gates to reachable behavior.

Review transitive dependencies and plugins when they execute in-process or receive user data. Do not assume an open-source top-level application controls every bundled component.

## Dynamic review boundary

Do not launch suspect software under a review-only request. If the user separately authorizes observation:

- use synthetic, non-sensitive inputs and an isolated account/profile;
- capture DNS and connection attempts as well as successful HTTP traffic;
- observe filesystem operations, subprocesses, D-Bus, and persistent artifacts;
- inspect first run, idle time, normal use, failure, crash, shutdown, and opt-out states;
- compare a clean baseline with the proposed control enabled;
- avoid uploading real content merely to prove an endpoint exists.

Runtime observation is sampled evidence, not proof that another code path never transmits. TLS metadata may show destinations while hiding payloads. Interception can change certificate pinning or program behavior; document the limitation.

## Confidence language

Use:

- **Confirmed:** reachable source/config evidence or controlled observation establishes behavior.
- **Likely:** strong indicators exist, but a key condition or payload remains unverified.
- **Possible:** a dependency or code path has capability without evidence it is active.
- **Not observed:** the bounded test did not see it; never translate this to “does not happen.”

## Research baseline

Reviewed 2026-08-02.

- [NIST Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework)
- [NIST: privacy across the data lifecycle](https://www.nist.gov/privacy-framework/getting-started-0)
- [GDPR Article 5 principles](https://eur-lex.europa.eu/eli/reg/2016/679/art_5/oj)
