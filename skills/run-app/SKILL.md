---
name: run-app
description: Use when the user wants this project's app running locally to test.
disable-model-invocation: true
---

# Run App

Start whatever the project needs to be testable locally — a single process, or a server plus a
frontend — through the project's own development environment, running in the background so the
conversation can continue while the user tries it out.

## When To Use

Only when the user explicitly asks for it in this conversation: "run the app", "start it up so I
can test it", "spin up the server/frontend", or a direct invocation of this skill. Do not invoke
this skill on your own initiative to verify a change works — that is a different, agent-driven
verification step (if the environment has a dedicated skill for that, use it instead). This skill
exists to hand the user something running, not to self-check your own work.

## Core Constraint

**Use the environment the project declares.** node, npm, python, cargo, go, or any other runtime
this project needs may only exist inside its declared environment: a Nix flake, a dev container,
a version manager file such as `.tool-versions` or `.nvmrc`, or a virtualenv. When the project
declares one, every command that starts part of the app runs through it, such as `nix run .#<app>`,
`nix develop -c <command>`, or the dev container, never against an ambient shell that may have a
different toolchain.

## Workflow

1. Identify what "the app" actually is before starting anything:
   - Check for a dedicated run entry point, such as `apps.<system>.<name>` outputs in `flake.nix`;
     prefer one when it matches.
   - Otherwise combine the declared environment with the project's own start command: `package.json` scripts (`dev`, `start`, `serve`), a `justfile`/`Makefile` target,
     `Procfile`, `docker-compose.yml`, or explicit run instructions in the README.
   - If the app has separate pieces (backend API, frontend dev server, database, worker), identify
     all of them — the user needs the whole thing testable, not just one half.
2. Check whether something this skill previously started is already running (a tracked PID file or
   job from an earlier invocation this session). If so, report that it's already up with its
   URL/port instead of starting a duplicate.
3. Start each required component through the declared environment, in the background, one at a time:
   - Prefer the harness's native background/async command execution when available.
   - Otherwise fall back to shell backgrounding: redirect output to a log file, background the
     process, and record its PID (`<command> > /tmp/run-app-<name>.log 2>&1 & echo $! > /tmp/run-app-<name>.pid`,
     adjusted to this session's scratch directory when one exists).
   - Give each component its own log file and PID so failures are attributable and each can be
     stopped independently.
4. Confirm each component actually came up — check the log for its own "listening"/"ready" line, or
   probe the port — before reporting success. Do not report the app as running from the mere fact
   that a background job was launched.
5. Report to the user: what was started, the URL(s)/port(s) to open, where the logs live, and that
   it will keep running in the background until they ask to stop it.
6. Leave it running. Do not stop, restart, or touch these processes again unless the user asks —
   including across later turns in the same conversation.

## Stopping

When the user says to stop it (this app, "it", or equivalent):

- Stop only the process(es) this skill started and tracked (by PID/job), not unrelated processes on
  the same ports or names — another agent or the user's own shell may be running something else.
- Terminate cleanly (SIGTERM) and only escalate to SIGKILL if the process doesn't exit.
- Clean up the PID/log files once confirmed stopped, and confirm to the user that it's down.

## Failure Handling

If a component fails to start, report the failure with the relevant log output rather than silently
retrying or falling back to a different, unrequested way of running it. A missing run entry point, a
missing environment, or a port already in use are all things to surface, not work around unasked.

## Boundaries

- Do not modify `flake.nix`, dev container, or other environment files, or otherwise change tracked project files just
  to make something runnable — if the project genuinely has no way to run it, say so and ask.
- Do not run build, install, or migration steps beyond what the project's own start command already
  does as part of coming up.
- Do not use this skill's background processes for automated checks, screenshots, or other
  agent-driven verification — it is for the user's own manual testing.
