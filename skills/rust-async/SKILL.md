---
name: rust-async
description: Use when writing or reviewing async Rust, such as runtimes, tasks, channels, cancellation, or sync and async boundaries.
---

# Rust Async

## Overview

Use this skill to keep Rust async work responsive, bounded, cancellation-aware, and runtime-correct. Prefer the project's existing runtime and concurrency patterns before adding new dependencies or changing public API shape.

## Workflow

1. Read `references/rust-async-practices.md` before giving substantive advice or editing code.
2. Identify the execution context: UI callback, request path, background worker, library API, CLI edge, test, or sync adapter.
3. Classify the workload: async I/O wait, short synchronous work, blocking syscall/library call, CPU-bound computation, long-lived blocking loop, shared resource, stream/fanout, or cancellation/shutdown path.
4. Choose the narrowest mechanism that matches the workload and existing runtime.
5. Check the result for blocking, unbounded concurrency, lock lifetimes, cancellation safety, task ownership, runtime nesting, and Send/'static constraints.

## Non-Negotiables

- Do not put blocking work on UI, event-loop, request-handler, or async executor paths.
- Do not assume `async` means parallel. Futures make progress only when polled by a runtime, and many combinators multiplex on one task.
- Do not call `block_on`, `recv`, `join`, `std::thread::sleep`, blocking file/network/database APIs, or long CPU loops from async code unless they are moved to the correct blocking or dedicated thread mechanism.
- Do not hold a synchronous lock guard across `.await`. Keep every lock scope small and obvious.
- Do not introduce unbounded task spawning, unbounded queues, or background tasks with ignored failure/cancellation semantics.
- Do not create a nested or per-call runtime in library or hot-path code. Put sync adapters at explicit process or API boundaries.

## Review Output

When reviewing or implementing async code, state:

- The async/sync boundary being changed or protected.
- The mechanism selected and why it fits better than nearby alternatives.
- The failure modes checked: blocking, backpressure, cancellation, lock lifetime, detached tasks, runtime mismatch, and API bounds.
- Any remaining assumptions that need local tests or runtime verification.

## Reference

- `references/rust-async-practices.md`: mechanism selection, Rust examples, pitfalls, review checklist, and source anchors.
