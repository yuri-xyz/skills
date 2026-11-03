---
name: review-pii
description: Use when recent work, the material under discussion, a commit, a build, or something about to be published or deployed should be checked for personal or machine-identifying details, such as the user's name, emails other than their GitHub commit email, phone numbers, addresses, home paths, hostnames, IP or MAC addresses, hardware, disk, or device IDs, or passwords. For private workflow files such as agenda, spec, or agent material use /review-leaks, and for runtime telemetry and data collection use /review-privacy.
---

# Review PII

## Objective

Find details that identify the user or their machines wherever they should
not be: in recent changes, in the material the conversation is about, and in
built output that will ship. Report what was found, where, and how bad it is.

This skill only reviews and reports. Do not edit, rewrite history, or delete
anything unless the user asks.

## Allowed Identity

The user's GitHub username and the email they commit with on GitHub, such as
the GitHub no-reply address or their public GitHub email, are allowed. Read
them from `git config user.email`, the project's commit history, or
`gh api user` (read-only). Any other email, and the user's real name where it
is not the GitHub username, is a finding.

## Build The Needle List

Generic patterns miss most real leaks, so collect this machine's actual
values first and search for them literally. Read them only from local
sources, keep them in memory, and never write them to a file, a command
history entry meant to persist, or the report.

- **Person:** real name from the account's full-name field (`getent passwd
  "$USER"`) and Git configuration, other configured emails, and anything the
  user has stated in the conversation.
- **Machine:** hostname, username, and home directory path; `/etc/machine-id`;
  MAC addresses (`ip -br link`); local, LAN, VPN, and public IP addresses the
  machine uses (`ip -br addr`); and Wi-Fi network names.
- **Hardware:** serial numbers, UUIDs, and WWNs of disks and partitions
  (`lsblk -o NAME,SERIAL,WWN,UUID,PARTUUID`), NVMe and SSD serials,
  DMI product and board identifiers readable without root under
  `/sys/class/dmi/id/`, and USB or PCI device identifiers that are unique to
  the device rather than to its model.
- **Credentials:** passwords, password hashes, API tokens, and keys the
  material might contain; search by pattern and by any value the
  conversation surfaced, never by reading a secret store.

Add generic patterns for what the needle list cannot know: email addresses,
phone numbers, street addresses, IPv4 and IPv6 addresses, MAC addresses,
`/home/<name>` and `/Users/<name>` paths, and common token formats.

## Scope

Pick the scope from the request and the conversation:

- **Recent work:** uncommitted changes, staged changes, and commits not yet
  on the upstream branch, including commit author, committer, and message
  fields. Commit timestamps reveal the committer's timezone; report a non-UTC
  offset only when the work is about to be published.
- **Material under discussion:** the files, logs, outputs, screenshots, or
  text the conversation is about.
- **Built output,** when the work produces or ships it: the artifact that
  will be published or deployed, such as `dist/`, `result`, packages,
  archives, images, and binaries. Build tools embed absolute paths, usernames,
  hostnames, and build machine details, so search binaries with `rg -a` or
  `strings`. Skip built output when nothing in the request ships.
- **Before publishing:** the full tree and history being made public, as
  /review-leaks scopes it.

## Workflow

1. State the scope and what was excluded.
2. Build the needle list, then search the scope for each value and pattern.
3. Read every hit in context. Drop false positives, such as example
   addresses from reserved ranges, documentation IPs, test fixtures with
   fake data, or values that are a model rather than a device, with a stated
   reason.
4. Judge exposure: whether the location is or will become public, is
   tracked, or stays local.

## Report

List each finding with its severity, the path and line or artifact, the kind
of detail, a masked excerpt such as `j***@e***.com` or `…3F:A2`, and the fix.
Never print a full secret, password, or serial in the report. Order findings
by severity:

- 🔴 Passwords, tokens, keys, or other credentials anywhere, or identifying
  details already public.
- 🟠 Real name, personal email, phone number, or street address, or hardware
  serials, in tracked or shipped material.
- 🟡 Machine details in tracked or shipped material, such as hostnames, home
  paths, IP or MAC addresses, machine IDs, or a revealing commit timezone.
- 🟢 Identifying details only in local, untracked, or ignored material that
  will not ship.

When nothing is found, say so in one line and name the scope checked:

🟣 No leak found: <scope checked>
