---
name: review-privacy
description: Explicit invocation only. Use when the user wants privacy risks reviewed and controls recommended without making changes or running suspect software.
disable-model-invocation: true
---

# Review Privacy

Apply a deliberate, evidence-based privacy lens. Default to no telemetry and no unnecessary persistent records while preserving required functionality, security controls, and the user's stated task.

## Non-Action Boundary

- Treat invocation of this skill as read-only review authorization.
- Do not edit configuration, disable services, delete data, add wrappers, block networking, or run the reviewed program merely because this skill is active.
- Do not broaden another task. If the user separately requests a change, apply this lens only within that authorized change.
- Make recommendations with tradeoffs and wait for explicit implementation direction when review is the requested outcome.

## Review Workflow

1. State the reviewed component, deployment context, trust boundary, and privacy goal.
2. Inventory data actions: collection, generation, logging, storage, transmission, sharing, retention, and disposal.
3. Separate necessary application traffic and state from telemetry, diagnostics, convenience features, and undocumented behavior.
4. Trace each relevant path from source to sink: what data, who triggers it, where it goes, how long it remains, and who can access it.
5. Check defaults and controls against the exact version, source, package, and launch environment.
6. Prefer the least invasive control that is verifiable. Consider stronger containment only when configuration or source-level controls are insufficient.
7. Report evidence, uncertainty, breakage risk, and residual exposure. Do not claim absence from a narrow search.

Read [threat-model-and-review.md](references/threat-model-and-review.md) before a source audit or broad privacy assessment.

## Telemetry and Network Review

- Treat analytics, usage metrics, crash uploads, diagnostics, experiments, remote configuration, attribution, recommendation requests, and background endpoint checks as separate channels.
- Identify network clients, telemetry SDKs, crash reporters, exporters, DNS names, endpoint construction, queues/spools, retries, startup hooks, and consent/default logic.
- Distinguish user-requested remote functionality, security updates, and ordinary protocol traffic from telemetry. Do not label every connection exfiltration.
- Prefer removing or disabling telemetry at its source, then documented configuration or environment controls, then enforceable network policy.
- Verify controls. A variable such as `DO_NOT_TRACK=1` is only a convention unless the exact program consumes it. `OTEL_SDK_DISABLED=true` applies only to conforming OpenTelemetry SDK behavior and does not disable unrelated reporters.
- Treat “disabled in the UI” and “endpoint is empty” as hypotheses until code, documentation, or observation confirms that no data is queued or sent.
- Do not perform dynamic network testing unless the user has authorized running the software and the test environment prevents unintended disclosure.

Read [telemetry-and-network.md](references/telemetry-and-network.md) for search targets, control ordering, and verification limits.

## Files, Logs, and Recoverability

- Inventory application logs, journald/syslog output, crash dumps, telemetry spools, caches, histories, recent-file lists, thumbnails, databases and journals, editor backups, temporary files, and exported diagnostics.
- Default to not recording sensitive content. Prefer aggregate or event-minimal diagnostics, explicit opt-in debug sessions, redaction before the sink, short retention, and narrow permissions.
- Remember that stdout and stderr may become persistent journal or supervisor logs. “No log file” does not mean “no persistence.”
- Treat memory as a different risk, not a guarantee of non-persistence: swap, hibernation, core dumps, and downstream consumers can preserve it.
- Prefer preventing creation over trying to erase later. Do not promise that `shred` makes a file unrecoverable on copy-on-write filesystems, SSDs, snapshots, backups, journals, or remote storage.
- Do not remove security/audit records blindly. Identify the requirement and recommend the minimum safe event set and retention instead.

Read [storage-logs-and-deletion.md](references/storage-logs-and-deletion.md) when the concern includes local artifacts or forensic recovery.

## Isolation and Bubblewrap

- Consider containment only after understanding the program's real filesystem, IPC, device, and network requirements.
- Prefer an existing application/service sandbox model over an ad hoc wrapper: native permissions, systemd unit sandboxing, Flatpak portals, NixPak, or another maintained packaging boundary may fit better.
- Use bubblewrap only when a separately launched Linux process has a clear policy, the runtime supports user namespaces, compatibility is tested, and the wrapper has an owner.
- Remember that bubblewrap is a low-level policy construction tool, not a complete sandbox. Its protection is determined by the arguments and exposed sockets.
- Network namespaces do not neutralize a broadly exposed D-Bus socket, proxy, browser opener, or helper that can make requests on the process's behalf.
- Do not wrap an application, desktop program, browser, service, or development tool automatically. Sandboxing can break portals, authentication agents, GPU/audio, language tooling, subprocesses, and an application's own sandbox.
- Require failures to remain closed and visible. Do not silently retry unsandboxed.

Read [sandboxing-and-verification.md](references/sandboxing-and-verification.md) before recommending bubblewrap or another enforcement boundary. Follow the project's Nix conventions as well when a separately authorized implementation changes NixOS, Home Manager, NixPak, or package definitions.

## Finding Format

For each material finding, report:

- confidence and evidence;
- data and sensitivity;
- trigger and default behavior;
- local sink or remote destination;
- stated/likely purpose and necessity;
- available control and how to verify it;
- compatibility or security tradeoff;
- residual exposure after the control.

Separate confirmed behavior, likely behavior, and unanswered questions. Lead with confirmed high-impact collection, transmission, or persistence.

## Avoid

- Auto-invoking this skill because a task happens to mention logs, networking, security, or telemetry.
- Equating all network access, state, or logging with malicious exfiltration.
- Treating a privacy policy, UI toggle, environment variable, or blocked hostname as proof by itself.
- Blocking all networking before identifying required behavior and indirect egress paths.
- Adding bubblewrap as a reflex or presenting one example command as a complete policy.
- Deleting evidence or user data during a review.
- Disabling security updates, authentication, backups, or auditability without surfacing the consequences.
- Claiming secure deletion or zero telemetry without evidence proportional to that claim.
