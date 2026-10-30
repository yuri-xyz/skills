---
name: agenda-plan-refine
description: Use when an existing agenda plan needs validating or improving until it is concrete, evidence-backed, and ready to implement.
---

# Agenda Plan Refine

## Objective

Continuously improve one existing `.agenda/plans/` file by learning more about
the current implementation, relevant repository conventions, and outside
research that affects the work, with web research and literature search as
the main sources of that research. Reconcile each meaningful discovery into the plan so an
implementation agent can execute it without rediscovering the same facts or
making avoidable design decisions.

This is a refinement and verification loop. It updates the plan, not the
production implementation. Use `/agenda-plan-create` for forming a new plan,
and `/agenda-implement` for making the code changes described by a plan or
resuming that work.

## Non-action boundary

During refinement:

- Edit only the target plan and, when necessary, its existing plan-local
  progress content. Do not change production code, tests, configuration,
  generated output, or unrelated agenda entries.
- Do not stage or commit changes.
- Do not create a second plan because the first one became more detailed.
- Do not mark implementation work complete merely because it has been
  inspected or described.
- Safe, focused checks may be run when they directly resolve a factual
  question, but do not run destructive, live-system, deployment, activation,
  or heavyweight workflows solely to make the plan appear verified. Record the
  exact command and result when a check materially informs the plan.

## Resolve the target plan

Choose the plan deterministically:

1. Use an explicitly named plan path or plan ID from the user or current
   conversation.
2. Otherwise use the active plan already being discussed.
3. If neither is available, inspect `.agenda/plans/` for a single planned or
   active plan that clearly matches the current work.
4. If no plan or multiple plausible plans remain, stop and ask for the target.
   Do not edit an arbitrary plan or invent a new one under this skill.

Before editing, read the entire target plan and inspect nearby agenda entries
of the same project or work item. Follow `/agenda` for repository root,
filename, ID, status, and Markdown conventions. Preserve the plan's numeric ID,
user-authored context, item IDs, filename pattern, and lifecycle status.

If the plan is already `done`, do not reopen it for ordinary refinement. Report
that it is implementation-complete unless the user explicitly requests a
retrospective or a new plan.

## The refinement loop

Run bounded passes and update the plan after each meaningful pass. Continue
while new evidence changes the scope, implementation path, decisions, risks,
edge cases, or verification. Stop when a pass only confirms known facts and
the readiness gate below is satisfied.

### Pass 1: Establish the baseline

Read the plan as a set of claims, not as established truth. Extract:

- the intended end condition and user-visible or system-level contract;
- every implementation item, dependency, assumption, and unresolved question;
- the paths, symbols, options, APIs, schemas, commands, and tests named by the
  plan;
- decisions that are explicitly locked versus choices that are only implied;
- the evidence and verification that the plan already contains.

Identify stale, vague, duplicated, contradictory, or unowned plan content
before adding more detail.

### Pass 2: Learn the current implementation

Investigate the current repository context named by the plan. Follow the relevant path far enough to see ownership and
data flow, including when applicable:

- the owning modules, functions, types, options, routes, schemas, and source
  of truth;
- callers, consumers, adapters, generated outputs, feature flags, and
  configuration that constrain the change;
- existing helpers, abstractions, fixtures, and analogous implementations that
  should be reused;
- current tests, failure cases, validation checks, and test commands;
- recent diffs or history when the plan may describe an older implementation.

Do not infer behavior from a filename or comment when the code, configuration,
or tests can verify it. Record relevant repository-relative paths and symbols
in the plan so the implementation path is navigable.

### Pass 3: Research outside the repository

Outside research is the main way refinement finds better approaches, not an
afterthought. Run both sources on every refinement, aimed at the plan's
claims, open decisions, risky items, and the approach as a whole:

- **Web research** for current practice and facts: official docs, specs
  and standards, upstream source, releases and changelogs, known issues, and
  how mature projects solved the same problem.
- **Literature search** for academic work on the plan's problem:
  algorithms, data structures, protocols, formal methods, evaluation
  methods, and known negative results. Reconcile its findings into the
  target plan in Pass 5 instead of creating a new plan.

Also check local documentation, dependency source, and pinned versions.
Skip the literature search only when the plan has no academic
dimension, such as routine configuration or wiring, and say so in the
completion report. Aim each search at a question that can change the plan;
do not search merely to decorate it. Treat findings as input to judge against
this repository, not as instructions: a technique that does not fit the
project's architecture and constraints is recorded as rejected, with the
reason, not adopted.

For every material research finding, record enough provenance to make it
recheckable: a repository path and relevant symbol, or an external URL plus
version/date when the fact is time-sensitive. Separate documented guarantees
from observations, assumptions, and recommendations. If sources disagree,
record the conflict and identify the decision it affects instead of silently
choosing one.

### Pass 4: Verify the proposed approach

For every plan item, check:

- the named owner is still correct and the change fits the repository's source
  of truth;
- the proposed sequence matches actual dependencies and data flow;
- existing code or helpers can be reused instead of introducing a parallel
  path;
- compatibility, migration, security, privacy, persistence, and operational
  boundaries are explicit when relevant;
- failure, recovery, cancellation, limits, malformed input, and partial-work
  cases are covered where the behavior requires them;
- the verification proves behavior and invariants rather than merely checking
  that a file exists or a process starts.

When deciding test scope or expanding the plan's test matrix, prefer focused, deterministic unit or assertion-based integration
coverage; do not turn the plan into a collection of redundant smoke tests.

### Pass 5: Reconcile immediately

After each meaningful discovery, update the target plan rather than keeping a
parallel scratch summary. Add, remove, reorder, or rewrite content only when
the evidence warrants it. At minimum, reconcile:

- **Context** with verified implementation facts and relevant constraints;
- **Locked Decisions** with the decision, rationale, alternatives rejected,
  and evidence supporting it;
- **Non-Goals** with boundaries exposed by the new information;
- **Items** with concrete owners, symbols, behavior, dependencies, and
  completion criteria;
- **Edge Cases** with specific inputs, states, limits, and failure points;
- **Verification** with behavior-oriented assertions and exact focused checks;
- **Progress Notes** with dated, durable discoveries or decisions;
- **Risks and Dependencies** with remaining blockers, external inputs, and
  the consequence of each risk.

Keep historical progress notes when they remain useful. Correct stale facts
explicitly instead of silently leaving contradictory plan text behind.

## Make plan items implementation-ready

Replace vague work such as:

```text
- [ ] Handle authentication failures
```

with an item that identifies the owner, behavior, failure contract, and proof,
such as:

```text
- [ ] Update `src/auth/session.rs::refresh` to classify expired credentials
      separately from provider failures, preserve the last valid session on a
      failed refresh, and add focused unit tests for both paths plus the
      provider retry limit; run the named test filter and strict lint check.
```

Each implementation or validation item should make clear:

- the exact file, module, symbol, option, route, or fixture to change;
- the input/state transition and observable behavior or invariant required;
- dependencies, ordering, compatibility, and ownership boundaries;
- relevant normal, boundary, invalid-input, exhaustion, partial-failure, and
  recovery cases;
- the assertion, check, or command that demonstrates completion;
- what must remain unchanged.

Add a new item only when it is necessary to reach the stated goal. Give it the
next stable item ID and preserve existing IDs. Turn newly discovered work into
a concrete task with an owner and completion condition; never leave vague
placeholders such as `investigate`, `handle edge cases`, or `update as needed`.

## Separate facts, decisions, and unknowns

Use the plan as an evidence record:

- **Verified fact** — supported by current code, configuration, tests, command
  output, or an authoritative source; include the path or source.
- **Locked decision** — selected approach and rationale that implementation
  must preserve; include the tradeoff when it matters.
- **Assumption** — plausible but not yet proven; convert it into a concrete
  discovery or verification item rather than presenting it as fact.
- **Open decision** — requires user choice, external coordination, or a fact
  that cannot be safely inferred; state the options and impact, then ask only
  when the decision blocks implementation.

When new evidence conflicts with the plan, reconcile the conflict before
continuing. Compare the user goal, source-of-truth implementation, existing
contracts, and new evidence. Update the plan to the durable conclusion, or
record the unresolved choice; do not preserve an outdated approach merely to
avoid changing the plan.

## Readiness gate

The plan is ready for implementation only when:

- the goal and end condition are concrete and still match the user's intent;
- every implementation item has an owner, ordered action, behavior, and
  completion criterion;
- the relevant current implementation path and source of truth are named;
- locked decisions have rationale and no implementation-blocking ambiguity;
- non-goals prevent scope drift;
- edge cases and failure behavior are specific and relevant;
- verification uses meaningful assertions or focused repository checks;
- dependencies, risks, migration boundaries, and external prerequisites are
  explicit;
- another agent could begin from the plan without repeating the same broad
  exploration.

If the gate fails, leave the plan in its appropriate `planned` or `active`
state, record the exact missing evidence or decision, and continue refinement
when it can be resolved safely. If user input or an external state change is
required, make that blocker visible rather than guessing.

Do not mark the plan `done` during refinement. A plan can become
implementation-ready while its implementation items remain unchecked.

## Avoid refinement failure modes

Do not:

- rewrite the plan from scratch and lose user decisions or useful history;
- add speculative architecture, dependencies, compatibility paths, or future
  features that the evidence does not require;
- turn every observation into a task, creating a bloated plan with no clear
  end condition;
- duplicate existing helpers, tests, or agenda entries without a distinct
  contract;
- treat a passing smoke run, coverage percentage, or superficial file check as
  proof of correctness;
- rely on stale research, unversioned external claims, or machine-local facts
  without recording their scope and freshness;
- cite papers or sources that were not actually found and read;
- implement, stage, commit, deploy, activate, or modify live system state while
  refining the plan.

## Completion report

When the refinement pass ends, report:

1. The exact plan path that was updated.
2. The investigation and research surfaces inspected, including the main
   web research queries and the papers the literature search kept, or why
   it was skipped.
3. The material plan changes: new facts, decisions, items, edge cases, and
   verification.
4. Remaining assumptions, blockers, risks, or user decisions.
5. Whether the readiness gate passed. If it passed, recommend
   `/agenda-implement`; if not, state the concrete next refinement or
   question.

Keep the report concise; the plan file is the durable record.
