---
name: agenda-plan-create
description: Use when work is large enough to need a detailed implementation plan in the `.agenda` workspace before implementing; use /agenda-plan-refine instead to validate or improve an existing plan.
---

# Agenda Plan Create

Use this skill to turn the user's goal into a concrete, task-based markdown plan under the current repository's `.agenda/` directory.

## Storage

Follow `/agenda` for storage rules, filenames, IDs, statuses, and the baseline plan section skeleton. Plans live in `.agenda/plans/`. This skill adds the stricter content requirements below on top of that shape.

## Plan Shape

The plan should be detailed enough that an implementation agent can execute it autonomously without rediscovering the same decisions or deciding what "explore" means.

Plans must be task-based, progress-oriented, and action-oriented. Prefer markdown task list items that name the concrete code, Rust assert tests, or docs to change, such as:

```markdown
- [ ] Implement the parser changes in the owning module
- [ ] Add regression coverage for invalid input handling
- [ ] Update the CLI error path in `crates/example/src/commands.rs`
```

Do not use plain unordered bullets or vague task labels for executable work items, such as:

```markdown
- Parser changes
- Tests
- Explore validation options
- Maybe add compatibility handling
```

Beyond the standard plan sections in `/agenda`, every plan produced by this skill must have:

- A todo/task list with ordered implementation steps using `- [ ]` items.
- An edge cases section with concrete edge cases to verify in code or cover with tests when applicable.
- A verification section with task-based Rust assert-test checks using `- [ ]` items.
- Locked decisions with their rationale, and explicit non-goals.

If the existing `.agenda/plans` convention uses numbered item headings, keep that outer structure but make each actionable item task-based inside it.

Avoid "future", "explore", "investigate", "consider", "maybe", and similar abstract placeholders in executable task lists. If more discovery is genuinely required, make it a concrete task with a target and output, such as "Inspect `crates/config/src/lib.rs` and record the selected helper in Decisions", then follow it with the implementation task that uses the result. If a deferred item is not part of the implementation, put it in non-goals or leave it out.

Do not add runtime-check tasks anywhere in the plan. A plan should not ask the user or the agent to manually run the app, launch a UI-facing binary, drive the UI, inspect screenshots, or confirm behavior by interacting with the running product. Express verification as Rust assertions instead.

## Autonomous Pending Tasks

A finalized plan must be a 100% autonomous implementation task list: every pending
item must be executable and verifiable by the agent using the repository and its
normal tools, without waiting for a human to perform a check or interact with the
live product.

Never encode a pending task whose completion depends on a human performing,
observing, approving, or attesting to the result, or interacting with the live
product. Phrases such as “human must verify,” “human must live-check,” “ask the
user to try it,” and “have a user approve the result” are illustrative examples;
the same rule covers equivalent manual acceptance, sign-off, visual inspection,
live testing, operator action, or other human-dependent validation. Resolve
user-owned decisions during planning with the Ask And Lock workflow, record the
decision, or make the scope an explicit non-goal before finalizing the plan. Do
not leave human verification or live checking as unfinished implementation
work.

## Edge Cases Section

Every plan must include an edge cases section unless the task is purely documentation-only and no behavior can change. The section should list specific cases that implementation must verify by reading relevant code and, where applicable, adding or updating tests.

Write edge cases as task-based checks, for example:

```markdown
## Edge Cases

- [ ] Verify empty input returns the existing validation diagnostic instead of panicking
- [ ] Add coverage for paths containing spaces, quotes, and dollar signs
- [ ] Confirm legacy config without the new field still emits the same Nix
```

Do not write generic edge-case placeholders such as "handle errors" or "check edge cases". Name the input, state, boundary, or failure mode and what should happen.

## Verification Section

Every plan must include a verification section. Keep it concise, but make it strong enough to confirm implementation correctness.

Write verification as task-based checks, for example:

```markdown
## Verification

- [ ] Add or update Rust unit tests that assert the changed behavior
- [ ] Add or update Rust regression tests for the main failure mode
- [ ] Run the focused `cargo test` filter that executes those assert-based tests
```

Prefer high-quality tests and checks that prove the intended behavior, failure paths, and integration boundary. Quality matters more than quantity.

For testing and validation:

- Avoid smoke tests.
- Do not add task items that require the user to manually run the app, click through behavior, inspect UI, or confirm runtime behavior.
- Do not add task items that require the agent to launch the app, launch a UI-facing binary, drive a GUI, take screenshots, or perform heavyweight runtime/UI automation.
- Do not add "manual check", "smoke test", "run the app", "try it locally", or similar runtime-check items to plans.
- Use only regular Rust assert-based unit or integration tests for planned test coverage.
- Use focused `cargo test` invocations only to execute those Rust assert tests; do not use app/runtime execution as a substitute for assertions.
- Avoid filler verification steps that only confirm files exist, commands run, or binaries start without exercising the plan's correctness through assertions.
- Tie verification steps back to the implementation tasks and edge cases. If an edge case is important enough to list, the plan should say how it will be verified.

## Workflow

### 1. Capture Intent

Start from the information the user provided when invoking the skill. Treat it as the seed, not the whole plan. Expand it into the likely full scope by applying project context, existing patterns, related files, and reasonable production concerns. Convert that context into concrete edits, tests, and checks.

### 2. Identify Open Decisions

Before finalizing the plan, identify anything vague, user-owned, or design-sensitive, such as:

- Product behavior or user-facing scope.
- Architecture boundaries.
- Data model or API contract choices.
- Migration, compatibility, or rollout strategy.
- Security, privacy, persistence, or operational tradeoffs.
- Validation depth and acceptance criteria.

Do not leave these as unresolved placeholders if they are required for implementation. Lock the decision, ask the user, or mark the item explicitly out of scope.

### 3. Ask And Lock

For remaining open decisions, use the available `ask` or user-input tool to ask the user focused questions.

When offering choices:

- Provide high-quality, mutually exclusive options.
- Put the recommended option first.
- Make the recommended option the best long-term fit that likely matches the user's intent.
- Explain each option's practical impact or tradeoff briefly.
- Avoid asking about decisions the agent can safely infer from repo context.

After the user answers, immediately edit the plan file to record the decision and rationale. Repeat until all implementation-blocking decisions are locked.

If no ask tool is available, ask the same focused questions in chat and update the plan after the user responds.

### 4. Finalize Implementation Readiness

Once all required decisions are locked in, update the plan so it is ready to implement:

- Convert ambiguous notes into concrete tasks.
- Replace speculative future/exploration language with concrete actions, locked decisions, or explicit non-goals.
- Ensure task order reflects dependencies.
- Ensure each task has a clear completion condition.
- Ensure every pending task is autonomously executable and contains no human-verification or live-check requirement.
- Add an edge cases section with concrete cases and expected behavior.
- Add concise Rust assert-test coverage and focused `cargo test` commands for those tests.
- Ensure the verification section contains concise, task-based Rust assert tests that confirm correctness.
- Mark the plan status as planned or active according to the local `.agenda` convention.
- State that the plan is ready for implementation in the final response.

Do not begin implementation unless the user explicitly asks for implementation after the plan is ready.
