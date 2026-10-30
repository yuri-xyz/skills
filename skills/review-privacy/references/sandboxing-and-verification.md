# Sandboxing and Verification

## Decide whether containment fits

Recommend containment only after answering:

- Is the target a separately launched process under the user's control?
- Does it need outbound or local networking?
- Which files must it read and write?
- Which D-Bus, Wayland/X11, PipeWire, agent, keyring, GPU, audio, input, and device interfaces are required?
- Which subprocesses and toolchains does it launch?
- Does it already implement a browser/runtime sandbox that namespaces or seccomp could disrupt?
- Who will maintain and regression-test the policy after upgrades?

If the application can avoid collecting or exporting data in source, prefer that root fix. Use a sandbox for enforcement or defense in depth, not as a substitute for understanding behavior.

## Choose the owning sandbox

- systemd service: prefer unit-native controls such as `PrivateNetwork=`, filesystem protection, explicit writable directories, address-family restrictions, and IP policy when compatible.
- desktop application: prefer a maintained packaging sandbox and portals when the ecosystem supports it.
- NixOS: consider declarative NixOS/Home Manager service controls or a reviewed NixPak policy rather than an unowned shell wrapper.
- one-off compatible Linux process: bubblewrap can construct a useful boundary when its complete policy is understood.
- library or in-process plugin: bubblewrap cannot isolate it without moving it across a process boundary.

Do not present these options as equivalent. Their lifecycle, IPC mediation, usability, and enforcement differ.

## Bubblewrap due diligence

Bubblewrap always creates a mount namespace and can create user, PID, IPC, UTS, cgroup, and network namespaces. `--unshare-net` creates a network namespace with loopback but no host network access. These are building blocks, not a finished privacy profile.

A credible policy normally considers:

- an empty constructed root with only required read-only package/runtime paths;
- narrow writable state or ephemeral tmpfs, not a broad home bind;
- `--clearenv` followed by an allowlist of necessary environment;
- a PID namespace and correct child reaping where appropriate;
- `--die-with-parent` and `--new-session` where their semantics fit;
- no network namespace sharing when the app truly needs no network;
- filtered D-Bus rather than binding a full bus socket;
- only required Wayland, PipeWire, agent, or portal sockets;
- a minimal `/dev`, proc view, capabilities, and optional reviewed seccomp policy;
- closure of unrelated inherited file descriptors, with stdin/stdout/stderr treated as explicit boundary surfaces;
- resource limits or a constrained cgroup when hostile input could exhaust processes, memory, runtime, or writable storage;
- explicit failure rather than an unsandboxed fallback.

Do not copy a generic command. NixOS package paths, dynamic loaders, locale/fonts, GPU drivers, desktop portals, and authentication helpers make policy application-specific.

Exposed IPC can defeat the intended boundary. Bubblewrap's own documentation warns that a D-Bus socket can provide powerful host actions; use an appropriate filtering proxy and review every allowed name. A browser opener, package daemon, systemd API, or portal can also cause indirect network or filesystem effects.

Every writable mount remains a persistence and disclosure channel. A sandbox cannot distinguish intended output from embedded identifiers, debug logs, crash files, or malicious content written beside it. Stage outputs when practical, validate the expected artifact set, and remember that later software may upload or render those artifacts.

Test whether outer restrictions prevent the application from installing its own sandbox. Do not weaken a browser's or runtime's internal seccomp/namespace protections accidentally.

Bubblewrap shares the host kernel. For an actively hostile workload or a threat model that does not accept that boundary, recommend an appropriately isolated VM or stronger execution environment rather than overstating namespaces.

## Verification plan

Propose, but do not execute without authorization:

1. Functional tests for required operations and denial behavior.
2. Source/config checks proving telemetry channels remain disabled.
3. Filesystem observation with a clean temporary profile.
4. DNS, socket, and indirect IPC observation with synthetic data.
5. Tests for first run, idle, crash, restart, update, plugins, and child processes.
6. Negative tests showing prohibited network/filesystem/IPC operations fail.
7. A check that wrapper or sandbox failure cannot launch the program unrestricted.

State what the tests cannot prove. A clean observation window does not establish that every future input, feature, or version is private.

## Report proportional recommendations

Classify proposals:

- **Source/config fix:** least behavioral friction; depends on correct implementation.
- **Packaging policy:** reproducible deployment control; version and package specific.
- **Sandbox enforcement:** stronger boundary; higher compatibility and maintenance cost.
- **Network perimeter control:** useful defense in depth; may miss indirect egress and shared destinations.
- **Operational policy:** retention, backups, crash handling, and diagnostic procedures outside the app.

Explain why the selected layer fits and why stronger layers are or are not justified.

## Research baseline

Reviewed 2026-08-02.

- [bubblewrap security model, namespace behavior, and limitations](https://github.com/containers/bubblewrap)
- [systemd execution environment and sandboxing](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html)
- [Flatpak sandbox permissions](https://docs.flatpak.org/en/latest/sandbox-permissions.html)
