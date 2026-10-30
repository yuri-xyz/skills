# Storage, Logs, and Deletion

## Inventory every persistent sink

Look beyond a file named `app.log`:

- stdout/stderr captured by journald, syslog, containers, CI, or a supervisor;
- rotating application logs and debug traces;
- crash dumps, backtraces, minidumps, and support bundles;
- analytics/event queues awaiting upload;
- cache, state, history, recents, thumbnails, and search indexes;
- SQLite journals/WAL files and deleted database rows;
- temporary files, editor swap/backup files, lock files, and print spools;
- shell history, command arguments, environment snapshots, and process metadata;
- backups, snapshots, sync services, and remote log collectors.

For each sink, record contents, path, mode/ownership, storage medium, retention/rotation, deletion trigger, backups, and downstream copies.

## Minimize before writing

Prefer this order:

1. Do not collect or render unnecessary sensitive values.
2. Log a coarse event or bounded count instead of payload, path, identifier, or content.
3. Redact or transform at the source before any formatter, queue, or exporter sees the value.
4. Keep diagnostics off by default and enable them for an explicit bounded troubleshooting session.
5. Retain only as long as the stated purpose requires, with strict access.

Hashing is not automatic anonymization. Stable hashes can correlate activity, and low-entropy values can be recovered by guessing. Avoid persistent identifiers when correlation is unnecessary.

Never record authentication secrets, access tokens, session IDs, private keys, raw request/response bodies, user documents, or sensitive personal data merely for debugging. Paths, hostnames, usernames, IP addresses, and command lines can also be sensitive.

## Balance privacy and security

Some security/audit events are necessary to detect abuse or explain privileged actions. Do not recommend eliminating them without identifying the security, operational, contractual, or legal consequence. Instead propose:

- the smallest useful event;
- redacted/pseudonymous fields;
- local rather than remote storage where appropriate;
- short, explicit retention;
- narrow access and no secondary analytics use;
- opt-in verbose diagnostics separate from the audit trail.

Be clear when the user's “no logs” posture accepts reduced diagnosability or incident response.

## Volatile is not unrecoverable

Memory-backed and runtime storage avoids ordinary durable files but can still be exposed through swap, hibernation, core dumps, process inspection, privileged access, or consumers that copy the data. `memfd`, anonymous files, `O_TMPFILE`, tmpfs, and `XDG_RUNTIME_DIR` solve different lifecycle problems; none alone proves forensic impossibility.

Under systemd, standard output may enter the journal. Journald storage can be persistent or volatile and may forward elsewhere. Core dumps can contain process memory, environment, mappings, paths, and open-descriptor metadata and may be stored externally or in the journal. Review both application and system policy.

## Deletion and recovery

Prevent creation when recovery risk matters. Ordinary unlink removes a name, not necessarily every copy or physical block. Files may survive in:

- copy-on-write extents;
- filesystem or volume snapshots;
- journals and database WAL files;
- SSD flash translation layers and wear leveling;
- backups, synchronization, replicas, or remote collectors;
- open file descriptors and application caches.

Do not promise that `shred` securely erases an ordinary file. GNU documents that it assumes in-place overwrites, an assumption many modern storage stacks do not satisfy. Encryption established before writing, lifecycle-aware key destruction, device sanitization, snapshot/backup retention, and media disposal are separate controls requiring their own threat model.

Do not delete files during a privacy review. Report existing artifacts and propose a separately authorized retention or remediation plan.

## Research baseline

Reviewed 2026-08-02.

- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [systemd-coredump behavior and stored metadata](https://www.freedesktop.org/software/systemd/man/latest/systemd-coredump.html)
- [journald storage configuration](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html)
- [GNU Coreutils `shred` limitations](https://www.gnu.org/s/coreutils/manual/html_node/shred-invocation.html)
