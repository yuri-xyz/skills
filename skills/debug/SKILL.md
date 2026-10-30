---
name: debug
description: Use when a bug or unclear runtime behavior needs investigating with added logging.
---

# Debug

## Overview

Use this skill to add focused debug instrumentation that helps isolate an issue with concrete runtime evidence. The goal is to make the next run answer a specific question, not to blanket the codebase with noisy logs.

## Workflow

1. Identify the question the logs must answer, such as which branch runs, which values cross a boundary, whether a callback fires, or where state diverges.
2. Inspect the relevant, suspicious, and core code paths before editing. Prefer narrow instrumentation around ownership boundaries, conditionals, loops, async/task boundaries, cache reads/writes, serialization, external commands, and error paths.
3. Confirm where logs will be written. The destination must be a file.
4. Add minimal, structured debug logs with a unique marker that is easy to grep.
5. In hot paths, log summaries, counters, throttled samples, or state transitions instead of every event.
6. Run the narrowest reproduction or check that should produce the logs when feasible.
7. Report the log file path, marker string, what was instrumented, and the command or scenario that should generate evidence.
8. Keep useful debug logs and markers in place until the user runs `/debug-cleanup`.

## Log Destination

The agent should usually determine the log file from the project's existing logging setup, documented commands, service config, test harness, or local conventions.

If the file destination is not known, is ambiguous, or the project only logs to stdout/stderr, ask the user before adding instrumentation. Ask where the debug log file should go or whether file logging is already configured. Do not guess and add logs that only print to the terminal when the user needs file-based debugging.

When adding a new temporary log file is appropriate, choose a repo- or app-local path that is easy to find and ignore, such as an existing `logs/`, `tmp/`, or `.debug/` location. Do not write debug logs into source-controlled generated output, system directories, or user-global locations unless the project already does so.

## Instrumentation Guidance

- Use the project's existing logging framework, levels, and structured fields when available.
- Temporary debug logs usually do not need a new environment variable, feature flag, or gated config switch. Prefer unconditional instrumentation for the specific run unless the project already has a low-friction debug logging gate or the logs would be too expensive, risky, or noisy without one.
- Include a unique marker prefix in every added debug line, for example `DEBUG_INVESTIGATE_RENDER_202606`.
- For fast-growing log files, make the marker specific enough to grep efficiently and include nearby identifiers such as request IDs, task IDs, host names, paths, or state names.
- Log before and after key boundaries when that proves causality: input summary, branch chosen, important derived values, error context, and output summary.
- Avoid logging secrets, tokens, private keys, full credentials, cookies, personal data, or large payloads. Redact or summarize sensitive values.
- Keep temporary logging easy to remove. Group related markers and avoid scattering unrelated instrumentation across the codebase.
- Prefer summaries in rapid-fire hot paths: counts, first/last item, changed fields, periodic samples, rate-limited warnings, or aggregate timing.
- Do not weaken behavior, swallow errors, alter timing-sensitive logic unnecessarily, or introduce broad debug abstractions just to log.
- The agent MUST NOT remove, clean up, or revert debug logs before the user runs `/debug-cleanup`, unless specific logs have stopped helping narrow the current bug or problem being investigated.

## Hot Paths

In tight loops, render ticks, file watchers, network streams, async polling, or repeated validation paths, avoid one log line per iteration unless the issue requires it and the run is tightly bounded.

Prefer patterns such as:

- Log only when state changes.
- Log every Nth event with a counter.
- Accumulate counts and emit one summary at the end of the operation.
- Log anomalous values only, with enough context to identify the surrounding operation.
- Include elapsed time buckets instead of every timing sample.

## Final Response

When instrumentation has been added, report:

- The exact log file path.
- The marker string to grep.
- The code paths instrumented.
- The reproduction command or action that should populate the file, if known.
- A note that useful debug logs should stay in place until `/debug-cleanup`, unless they stop helping narrow the current issue.
