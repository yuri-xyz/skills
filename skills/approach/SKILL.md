---
name: approach
description: Use when a proposed architecture, plan, or fix needs judging on whether it is the cleanest durable approach before committing to it.
---

# Judge Approach

## Objective

Assess whether the current proposal is the right long-term architecture for the problem at hand. Prefer solutions that fix the underlying cause, make recurrence unlikely, fit the codebase's existing design, and leave the system cleaner and easier to maintain.

This is an architecture judgment skill, not an implementation shortcut. Think hard, read relevant code when applicable, and give a concrete recommendation.

This is the deepest member of the judge family and owns its verdict discipline: lead with the verdict, then the reasoning, and never bury the recommendation. Reach for a narrower sibling when the question is narrower — `/root-cause` for a quick checkpoint on whether a fix is a workaround stacked on top of broken behavior, `/options` for ranking several candidate approaches, `/dependency-judge` for local code versus a package, `/keep-or-revert` for whether earlier changes should survive new evidence, `/criteria` for rating a new feature or design on usefulness, soundness, consistency, and proportionality.

## Workflow

1. Restate the problem and the proposed solution in concrete terms.
2. Inspect the relevant code, tests, contracts, call sites, data flow, and ownership boundaries before judging whenever the repository context can answer the question.
3. Identify the root cause, not just the visible symptom. If the issue is part of a larger known problem, evaluate the proper fix for that larger problem.
4. Check whether the proposal is idiomatic for this codebase: existing patterns, module ownership, types, abstractions, validation boundaries, error handling, and test strategy.
5. Reject approaches that are mostly hacks, temporary shims, compatibility layers, duplicated logic, broad workarounds, or "just make it pass" fixes.
6. Avoid over-scoping. Do not turn every issue into a rewrite. Expand scope only when the broader problem is clearly the root cause and solving it is the durable path.
7. Compare the best viable long-term options and recommend one.

## Evaluation Criteria

Prefer a proposal when it:

- Fixes the underlying issue rather than patching symptoms.
- Prevents the same class of bug from recurring through types, validation, centralization, clearer ownership, or better tests.
- Fits the existing architecture and local idioms.
- Removes or reduces duplication, special cases, and hidden coupling.
- Has a clear migration path and bounded blast radius.
- Improves maintainability without unnecessary abstraction.
- Can be verified with focused tests or checks that prove the behavior and failure modes.

Be skeptical of a proposal when it:

- Shows any of the workaround signatures defined in `/root-cause`.
- Makes the system harder to reason about, test, or evolve.
- Requires broad churn without clear root-cause payoff.
- Adds abstraction that no second caller needs yet.

## Output Shape

Start with the verdict:

- `Yes`: the proposal is the best long-term approach.
- `Mostly`: the direction is right, but specific changes are needed.
- `No`: it is not the right long-term approach.
- `Unclear`: the codebase evidence is insufficient; name exactly what must be inspected or decided.

Then provide:

- Root cause: the underlying issue the solution must address.
- Assessment: why the current proposal does or does not solve it robustly.
- Top contenders: the best proper solutions worth considering, with tradeoffs.
- Recommendation: the option you would choose and why.
- Verification: tests, checks, or code review points that would prove the fix prevents recurrence.

Keep the answer direct. Do not bury the recommendation behind excessive theory.

## Guardrails

- Do not recommend temporary fixes unless they are explicitly labeled as stopgaps and paired with the durable fix.
- Do not over-engineer. A small root-cause fix is better than a broad redesign when it fully addresses the class of issue.
- Do not approve an approach solely because it works for the immediate case.
- Do not claim certainty without reading the relevant code when the codebase can settle the question.
- If there are multiple strong solutions, present the top contenders instead of pretending there is only one reasonable answer.
