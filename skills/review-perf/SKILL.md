---
name: review-perf
description: Use when reviewing changes for performance, such as complexity regressions, repeated work, avoidable allocations, or hot-path inefficiencies.
---

# Review Perf

## Objective

Review the current or proposed code changes for practical performance problems. Focus on algorithmic complexity, redundant operations, repeated calls, avoidable allocation, and hot paths.

Prefer simple, obvious improvements. Do not make the code harder to understand for speculative or tiny wins.

## Workflow

1. Inspect the recent diff, pending plan, or relevant files.
2. Identify likely hot paths, loops, repeated operations, and data-size-dependent behavior.
3. Reason about big-O behavior where it matters: nested loops, repeated scans, sorting, hashing, filesystem traversal, parsing, rendering, network/database calls, and repeated serialization.
4. Look for redundant work, such as recomputing values inside loops, repeated lookups, unnecessary clones, repeated allocations, duplicate parsing, or calling expensive helpers more often than needed.
5. If an improvement is obvious, local, and keeps the code clear, implement it.
6. If an optimization would add complexity, indirection, caching, invalidation, or subtle ownership behavior, do not apply it unless the performance issue is clearly significant.
7. Run focused tests or checks for changed code when applicable.
8. Report what was reviewed, what was changed, and any performance concerns intentionally left alone.

## Prefer Improvements Like

- Hoisting invariant work out of loops.
- Reusing already-computed values.
- Avoiding repeated linear scans when a small local map or set clearly improves hot-path behavior.
- Avoiding unnecessary clones or string allocations where borrowing is straightforward.
- Short-circuiting once the result is known.
- Combining passes when it stays readable.
- Moving expensive formatting, parsing, serialization, filesystem reads, or command construction out of repeated paths.

## Avoid

- Premature caching with unclear invalidation.
- Large refactors just to reduce a minor allocation.
- Clever iterator chains or data structures that obscure simple logic.
- Changing public behavior, ordering, determinism, or error reporting for speed.
- Optimizing cold setup paths unless they are obviously wasteful or repeatedly called.
- Adding benchmarks unless the user asks or the tradeoff cannot be evaluated without measurement.

## Output

If no changes are needed, say that no obvious performance issue was found and name the areas reviewed.

If changes are made, summarize:

- Hot path or complexity issue addressed.
- Concrete optimization applied.
- Why the code remains simple enough.
- Checks run, or why checks were not run.
