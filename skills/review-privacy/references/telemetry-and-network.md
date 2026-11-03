# Telemetry and Network Controls

## Classify outbound behavior

Keep separate findings for:

- product analytics and usage metrics;
- performance metrics and distributed traces;
- automated crash/diagnostic upload;
- experiments, feature flags, and remote configuration;
- advertising, attribution, recommendation, or tracking calls;
- update and revocation checks;
- user-initiated sync, API, download, or collaboration;
- authentication and licensing;
- local-network discovery and IPC.

The privacy question is not only whether a connection exists. Determine the payload, identifiers, destination ownership, trigger, necessity, retention, and ability to opt out.

## Inspect implementation and configuration

Look for initialization that runs before user settings load. Check whether disabling telemetry:

- prevents SDK initialization;
- suppresses collection as well as export;
- deletes or retains an existing local spool;
- disables crash uploads separately;
- survives upgrades and new profiles;
- applies to child processes, plugins, and language servers;
- stops retries queued before opt-out;
- changes only sampling while some events still transmit.

Check configuration precedence. A documented setting can be overridden by managed policy, command-line flags, environment, embedded defaults, or remote configuration.

## Prefer controls in order

1. Remove unnecessary collection/export code or build features when maintaining the source.
2. Use an application-supported policy or configuration that disables the channel before collection.
3. Use a documented version-appropriate environment variable when deployment needs it.
4. Remove endpoint credentials/exporters when that reliably produces a no-op rather than noisy retries or local spooling.
5. Enforce network policy when the program does not need the network or when defense in depth is justified.

Multiple layers can be appropriate, but every layer needs an owner and a verification method.

Environment variables are ordinary inherited configuration. They are not universal, cannot override code that ignores them, can be replaced by child launchers, and may appear in process inspection or crash metadata. Never place secrets in them merely because they are useful for opt-out flags.

Examples to verify rather than cargo-cult:

- `OTEL_SDK_DISABLED=true` asks a conforming OpenTelemetry SDK to use no-op signal providers; the specification notes that it does not disable configured propagators and it says nothing about other telemetry libraries.
- `DO_NOT_TRACK=1` is honored by some developer tools but is not a Linux-wide enforcement mechanism.
- Vendor-specific analytics, crash, and update variables vary by product and version; consult the exact upstream documentation/source and test the packaged build.

## Network enforcement

Blocking a hostname is weaker than controlling egress: destinations can change, use shared CDNs, resolve through another name, or use raw addresses. Proxy/firewall rules may miss local IPC that delegates network access. A separate network namespace provides a stronger default-deny boundary for a compatible process, but exposed helpers and sockets still matter.

Do not disable networking for software whose purpose requires it without defining allowed capabilities. Separate update traffic when blocking it would prevent security fixes; prefer a user-controlled update path rather than silently removing updates.

When suggesting allowlists, account for DNS, certificate validation, authentication, captive portals, and endpoint churn. State their maintenance burden and failure mode.

## Verification

Verify the control at the same boundaries the threat uses:

- source/config: channel is not initialized or data is discarded before collection;
- filesystem: no spool or retry queue appears;
- network: no DNS or connection attempt reaches an external interface;
- indirect IPC: no exposed service performs the request on the app's behalf;
- lifecycle: first run, idle, error, crash, shutdown, and upgrade remain quiet.

Do not require executing these tests under a review-only invocation. Present the verification plan for later authorization.

## Research baseline

Reviewed 2026-08-02.

- [OpenTelemetry SDK environment variables](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/)
- [bubblewrap network namespace behavior and limitations](https://github.com/containers/bubblewrap)
- [`strace` syscall classes for authorized observation](https://man7.org/linux/man-pages/man1/strace.1.html)
