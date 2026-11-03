# Exposure audit

## Objective

Answer "are we affected?" for recent security incidents, with evidence. Find
what was disclosed in the window, check each item against what is actually
installed or depended on, look for indicators of compromise, and hand the user
a readable report with the fixes that need their approval. Default to
read-only: the audit observes and proposes; remediation waits for approval.

## Scope

- **Window:** the last 30 days unless the user names a period or a specific
  incident. State the dates you used.
- **Target:**
  - *System* (default): the running OS and kernel, its package managers and
    any configuration repository that declares the system, browsers and mail
    clients, language tooling and its vendored trust stores, user-level
    installs (Homebrew, Flatpak, Snap, `nix profile`, `pipx`, global npm
    packages, containers), running processes, and the user's own
    repositories.
  - *Project* (when the user says "audit this project" or names a path): its
    lockfiles and pinned inputs (`Cargo.lock`, `package-lock.json`,
    `bun.lock`, `pnpm-lock.yaml`, `uv.lock`, `poetry.lock`, `go.sum`,
    `flake.lock`), CI workflows, and editor and agent hook files. Skip system
    checks unless the project ships or runs them.

## Workflow

1. **Research** the window with `/research-web`. Search each category
   separately, because a broad query misses most of them:
   - supply chain: npm, PyPI, crates.io, Go modules, GitHub Actions, VS Code
     and Open VSX extensions, Docker images, AI and agent tooling;
   - the OS: the kernel and the distribution's or vendor's security
     advisories (see OS notes below);
   - browser engines: Chrome zero-days apply to every Chromium build (Edge,
     Brave, Electron apps); Mozilla advisories apply to Firefox, Thunderbird,
     and their forks, such as Tor Browser;
   - core libraries and daemons: OpenSSL, OpenSSH, curl, glibc, sudo,
     systemd, bubblewrap, BIND;
   - CA and trust-store incidents (compromised or distrusted roots).

   For each item, record the affected and fixed versions, the preconditions
   (a VM host, a local attacker, a specific feature), and the indicators of
   compromise. Prefer upstream advisories and cross-check surprising claims.
2. **Inventory** what is really in use, not what the config claims:
   - The OS and kernel version, and every package manager's list of what is
     installed, using the commands in the OS notes below. When a
     configuration repository declares the system, check the revision the
     machine actually runs, not only what the repository says.
   - User-level installs that the system package manager does not update,
     such as Homebrew, Flatpak, Snap, `nix profile`, `pipx`, and global npm
     packages, with their versions.
   - Browsers: each binary's version, the profile's `Last Version`, and for
     Chromium browsers the `CertificateRevocation/<n>/crl-set` sequence.
     A stale CRLSet means revocations and blocks have not arrived.
   - Trust stores: the OS store (`/etc/ssl/certs` and the p11-kit source on
     Linux, the System keychain on macOS, the certificate store on Windows)
     and every vendored bundle, such as certifi copies in Python
     environments and pip's own vendored certifi.
   - Lockfiles, node_modules, Python environments, package caches, container
     images, and running processes.
3. **Correlate** each finding with the inventory. Whether a fix exists
   downstream decides the remedy, so check it in the distribution's own
   package tracker or advisory, which may backport a fix without changing the
   upstream version number.
4. **Sweep for indicators of compromise**: the files, services, processes,
   network endpoints, and workflow names each advisory lists; recently
   changed `.claude/settings.json` and `.vscode/tasks.json` files; malicious
   versions in lockfiles and caches; and, read-only, the user's GitHub repos
   (`gh search code --owner <user>`, workflow file listings).
5. **Verify precisely.** Match certificates by SHA-256 fingerprint, not
   label, and hash only the certificate DER inside OpenSSL
   `TRUSTED CERTIFICATE` blocks. Check whether a bundle entry is trusted for
   TLS at all: NSS bundles carry email-only roots. Run a control alongside
   every negative test so that a failed check doesn't pass for a clean result.
   When an advisory ships a scanner script, reimplement its logic locally
   rather than running fetched code.
6. **Report** (see Output). Note what you could not check and why, such as
   a blocked command or a capped listing.

## OS notes

Use the native commands and advisory source for the machine at hand:

- **Debian and Ubuntu:** `dpkg -l` or `apt list --installed`; Debian Security
  Advisories (DSA) and the Debian security tracker, or Ubuntu Security
  Notices (USN).
- **Fedora and RHEL family:** `rpm -qa`, `dnf updateinfo list --security`;
  Fedora and Red Hat security advisories.
- **Arch Linux:** `pacman -Q`, `arch-audit` when installed; the Arch Linux
  security tracker.
- **NixOS and Nix:** `nixos-version`, `nix --version`, `nix profile list`,
  and the `flake.lock` input that actually drives the host; check a fix by
  reading the package's version on each nixpkgs branch. NixOS announces
  security issues on its Discourse.
- **macOS:** `sw_vers`, `softwareupdate --list`, `brew list --versions`;
  Apple security releases and Homebrew's formula versions.
- **Windows:** `winver` or `Get-ComputerInfo`, `winget list`; the Microsoft
  Security Update Guide.

For other systems, find the equivalent: the installed-package list, the
vendor's advisory feed, and how it reports backported fixes.

## Rules

- Remediation is a separate, approved step: system upgrades or rebuilds,
  package manager changes, `sudo`, mounts, cache deletion, credential rotation, and any
  GitHub write each need the user's explicit go-ahead.
- Before upgrading an app with a user profile (browsers, mail), back up its
  data directory with the app closed: profile databases migrate one way, so
  a downgrade cannot reopen them.
- A config fix that cannot take effect yet (a blocked rebuild, an unreleased
  channel) can be bridged with a runtime measure that ends at reboot. Name it
  as temporary and record the follow-up with `/gaps-record`.
- Probes clean up after themselves: `mktemp -d`, print the path, and delete
  only the literal files you created.

## Output

Lead with a one-line verdict: compromised, exposed, or clean. Then:

```markdown
## ✅ No indicators of compromise

| Incident | What I checked | Result |
|---|---|---|
| <name and date, linked> | <places and indicators> | ✅ None |

## ⚠️ Outdated / exposed

| Component | You have | Fixed in | Risk |
|---|---|---|---|
| <name (how installed, running?)> | <version> | <version, linked> | 🔴/🟠/🟡 <impact and preconditions> |

## What I'd do (each needs your go-ahead)

1. <action, its scope, and what it changes>

## Sources
- <links>
```

Use 🔴 for exploited in the wild or remote code execution in use now, 🟠 for
high severity or local root, and 🟡 for conditional exposure. Mark checked
and clean items ✅, items you could not check ⚪, and confirmed compromise ❌,
with the response steps (isolate, rotate credentials, rebuild) before
anything else.
