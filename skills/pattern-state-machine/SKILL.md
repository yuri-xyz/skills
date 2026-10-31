---
name: pattern-state-machine
description: Use when designing or reviewing a workflow with non-trivial states and transitions, such as a lifecycle, protocol, retry policy, or multi-step process.
---

# Pattern: State Machine

Use this skill when designing, implementing, or reviewing a non-trivial module or
system that has a finite set of meaningful states, normally occupies one active
state at a time, and can move to a limited set of valid next states.

Prefer an explicit finite-state-machine shape when it makes the lifecycle easier
to name, inspect, test, and extend. The goal is not to introduce a state-machine
framework. The goal is to make state, events, transitions, effects, and failure
recovery visible in the code.

## Recognize the fit

This pattern is a strong fit when most of these are true:

- The behavior is more than a short conditional or a single straight-line
  operation.
- The system has several distinct lifecycle or algorithmic states, such as
  `idle`, `configuring`, `waiting`, `ready`, `completed`, or `failed`.
- At a given point, one state (or one independently running machine per actor,
  request, job, or session) owns the active behavior.
- Each state has a small, understandable set of events or outcomes that may
  lead elsewhere.
- Invalid, duplicate, late, cancelled, timed-out, or failed steps matter.
- The transition rules are important enough that a future maintainer should be
  able to read them without reconstructing them from scattered branches.

Good examples include:

- setup, configuration, onboarding, and migration flows;
- a bot or agent receiving a message, choosing work, and producing a response;
- sending a request and waiting for an acknowledgement, response, timeout, or
  rejection;
- a queue item, job, download, upload, or transfer with bounded lifecycle
  stages;
- a parser, protocol exchange, or non-trivial algorithm with clear procedural
  steps;
- retry, cancellation, approval, or recovery workflows.

Do not force this pattern onto a trivial `if`/`else`, a plain data enum with no
meaningful transitions, or a value with many independent attributes rather than
one lifecycle. For genuinely concurrent work, model each independent workflow
as its own machine and coordinate the machines explicitly. Do not hide a
cross-product of unrelated boolean flags inside one enormous enum.

This skill owns the domain transition model, not every concern around it,
such as async runtime, cancellation, and task ownership details.

## Core model

Make the transition boundary explicit. A useful functional shape is:

```text
transition(current_state, event) ->
    accepted(next_state, effects)
  | rejected(transition_error)
```

The names and types should follow the language and project. The important
properties are:

- States are named domain cases, preferably with a tagged union, enum, or
  equivalent type that can carry only the data valid in that state.
- Events describe inputs or outcomes that may cause a transition. They are not
  hidden calls to arbitrary state methods.
- The transition function is the authority for which state/event pairs are
  valid. An event cannot silently mutate state from a random call site.
- Effects such as sending a request, persisting data, emitting a notification,
  or starting a task are returned as explicit commands/results or handled at a
  clearly owned boundary. Keep the decision core pure when practical.
- The caller or effect runner executes effects and feeds their outcomes back as
  events. It must not bypass the transition function to manufacture a new
  state.

For small machines, one focused `transition` function and a match/table may be
clearest. For larger machines, split state-specific behavior into cohesive
modules while keeping the state/event contract and transition ownership easy to
find. Split one state-machine file once it becomes monolithic.

## Design workflow

1. **Check existing ownership first.** Search nearby modules, types, helpers,
   reducers, workflow code, and error models before adding another state enum or
   transition path. Extend a genuine existing
   machine or shared type rather than creating a parallel implementation.

2. **Confirm the boundary and the owner.** Identify what one machine represents:
   a session, request, job, message, resource, process, or algorithm. State who
   owns it, whether it is in memory or persisted, and which component is
   allowed to submit events.

3. **Inventory states before branches.** Name the initial state, active and
   waiting states, successful and terminal states, cancellation states, and
   retryable or non-retryable failure states that are relevant. For every state,
   record its invariant, payload, allowed operations, and observable meaning.
   Distinguish a state from data that merely describes it.

4. **Inventory events and outcomes.** List user commands, internal commands,
   dependency results, timeouts, cancellation, process restart, and malformed or
   unexpected input that can reach the boundary. Keep external outcomes as
   events so the state machine remains explicit about what it accepts.

5. **Write the transition contract.** Define the smallest useful state/event
   function, such as `State × Event -> Result<Transition, Error>`. Make valid
   transitions return the next state and effects. Make invalid transitions
   return an actionable, structured error rather than ignoring the event,
   returning `None`, or setting a collection of flags.

6. **Review a transition table.** Before or alongside implementation, write a
   table like this and make every row intentional:

   | Current state | Event/outcome | Next state | Effects | Recovery |
   | --- | --- | --- | --- | --- |
   | `Idle` | `Begin` | `Loading` | start load | fail to `Failed` |
   | `Loading` | `Loaded(config)` | `Ready` | none | — |
   | `Loading` | `LoadFailed(error)` | `Failed` | record failure | `Retry` -> `Loading` |
   | `Ready` | `Submit(request)` | `Waiting` | send request | timeout -> `Failed` |
   | `Waiting` | `ResponseOk(value)` | `Succeeded` | publish result | terminal |

   A table is a design aid, not a requirement to build a generic table-driven
   engine. Use a typed `match` or state-owned functions when that is clearer.

7. **Separate decisions from effects.** Keep validation, transition choice,
   invariant preservation, and retry policy in the state-machine core. Keep
   network, filesystem, process, UI, and other side effects in adapters or an
   effect runner. When atomicity or persistence matters, define the ordering of
   the state write and effect explicitly; do not rely on destructor cleanup or
   an implicit callback sequence.

8. **Make lifecycle edges explicit.** Decide what happens on duplicate and
   out-of-order events, timeout, cancellation, restart, retry exhaustion,
   shutdown, and terminal-state input. If an event is safe to repeat, make that
   idempotence deliberate. If it is invalid, reject it with context. Do not
   leave these cases to whichever branch happens to run.

9. **Consolidate genuinely shared failures.** When several states can fail in
   the same semantic way and share diagnostics, retryability, recovery, or
   observability, give them one reusable failure type/state or transition helper.
   A shared failure should preserve the source state, error kind, relevant
   context, cause, and retry/terminal policy. Shared error counters or labels
   should likewise be recorded at the common transition boundary when they have
   one meaning.

   Create one shared owner when repeated error data,
   transitions, or recovery logic has no canonical implementation. Do not
   collapse distinct domain failures merely to share an enum: map them to common
   diagnostics while retaining their different recovery behavior when needed.

10. **Test the graph, not just the happy path.** Apply `/writing-tests` and
    prefer fast tests of the pure transition function. Cover the initial state,
    every meaningful valid edge, invalid state/event pairs, terminal states,
    duplicate and late events, cancellation, retry limits, shared failures,
    effect descriptions, and recovery. Add a small integration test for the
    effect runner only where its boundary has a separate contract.

11. **Review the graph and the diff.** Look for states that cannot be reached,
    transitions that are only implicit in side effects, payloads that permit
    impossible combinations, duplicated error branches, unbounded retries,
    hidden global mutation, and unrelated feature work. Keep the machine at the
    domain boundary that owns the lifecycle.

## State and transition design rules

- Prefer one authoritative state representation over several booleans such as
  `is_loading`, `has_result`, and `request_sent` that can contradict each other.
- Put state-specific data inside the corresponding state variant when the
  language supports it. This makes invalid combinations harder to construct and
  makes ownership obvious.
- Keep event names about what happened or was requested (`ResponseReceived`,
  `RetryRequested`, `Cancelled`), not about a hidden implementation branch.
- Keep transitions bounded and visible. A transition may return an effect that
  later produces another event, but it should not recursively perform an
  unbounded workflow behind the caller's back.
- Distinguish transient failure, permanent failure, cancellation, and successful
  completion when their user action, persistence, metrics, or retry policy
  differs.
- Make terminal states terminal. Allow reset, restart, or replay only as an
  explicitly named event with a defined data-retention and side-effect policy.
- Keep shared transition helpers narrow. A helper should encode one invariant or
  genuinely common edge, not turn every state into a parameterized framework.
- Preserve context across failure and recovery. A retry should not lose the
  request, configuration, cursor, or user input needed to resume safely.
- Bound retries, queues, timers, and retained state. Represent exhaustion as an
  explicit transition rather than silently retrying forever.
- If state is persisted or serialized, version the representation according to
  the project’s normal rules, validate rehydrated states, and define behavior for
  unknown or corrupt states before performing effects.

## Common failure modes to reject

- A state enum exists, but transitions are scattered through callbacks,
  handlers, and setters with no single authority.
- A "state machine" is only a wrapper around a long procedure and does not make
  any state or event more legible.
- Invalid combinations remain possible because flags, nullable fields, or
  loosely related objects represent the state independently.
- Every failure becomes `Error` with no source, kind, retry policy, or recovery
  path, so useful distinctions disappear.
- A shared error type forces unrelated domains into one abstraction or erases
  state-specific data.
- The transition function performs network, filesystem, UI, or process effects
  directly, making it nondeterministic and difficult to test.
- A generic FSM dependency, registry, or reflection layer is added when enums,
  functions, modules, or a small table already express the graph clearly.
- The implementation has a happy-path state diagram but no behavior for
  cancellation, timeout, duplicate events, restart, exhaustion, or shutdown.
- Tests assert only final success and never prove invalid edges or recovery.

## Review checklist

- Is this genuinely a finite, non-trivial lifecycle or procedural graph?
- Is the machine boundary and single active-state invariant clear?
- Are states, events, valid transitions, rejected transitions, and terminal
  behavior explicit?
- Does one pure or deterministic transition boundary own the graph?
- Are effects separate, observable, and safe to retry or cancel as required?
- Are shared failures consolidated only where semantics truly match, with source
  context and recovery policy preserved?
- Are retries, timeouts, cancellation, duplicate events, and restart behavior
  bounded and intentional?
- Do focused tests cover the graph and failure paths rather than only success?
- Is the abstraction smaller and clearer than the scattered branches it replaces?
- Were existing state/error types and helpers reused before adding new ones?

## Output

When editing or reviewing a stateful system, report:

- why the state-machine pattern fits or why a simpler design is better;
- the machine boundary, state variants, events, and transition authority;
- the effect and persistence boundary;
- shared failure/error owners and any transitions that intentionally converge;
- invalid, terminal, cancellation, retry, timeout, and restart behavior;
- focused tests or checks run and any remaining graph or recovery risks.

Related skills: `/writing-tests` and `/pattern-kernel` (when
the machine guards auth, money, keys, or durable data) where applicable.
