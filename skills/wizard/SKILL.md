---
name: wizard
description: Use when the user has a rough feature, behavior change, improvement, project, or exploration idea and wants to be guided to a clear, agreed approach before planning or implementing.
---

# Wizard

## Objective

Turn a rough idea into a crystal-clear, agreed approach through a guided,
back-and-forth conversation, then carry it forward. The user brings context
about something they want: a new project, a new feature, a behavior to
change, something to improve, or an area to explore. The agent researches it,
questions the user thoroughly until nothing about intent is left to guess,
surfaces what could block the work, settles the technical decisions itself,
and leaves the human decisions to the user. This skill combines `/research`,
`/interview`, `/decide`, and `/agenda-plan-create`.

The wizard ends in one of two ways: an `.agenda` plan for a large undertaking,
or an implementation of a small change after the user confirms it.

## Human versus technical decisions

Classify every open question as human or technical by `/decide`'s "Human
versus technical decisions", and let the kind decide who answers it:

- **Human decisions**, such as who it is for, where it runs, whether it is
  paid, and what is in scope: ask the user.
- **Technical decisions**: settle them with `/decide` as delegated decisions,
  without asking, and report each decision and its reason so the user can
  override it.

## Workflow

### 1. Understand the request

Restate the idea in a sentence or two: what the user wants, why, and what kind
of request it is: new project, new feature, behavior change, improvement, or
exploration. If the request is too vague to research at all, ask about it
through `/interview` before researching.

### 2. Research with /research

Follow `/research` to build grounded context before asking or proposing
anything, so questions are informed and nothing the repository already
answers is asked:

- Inspect the relevant code, configuration, specs, `AGENTS.md`, `.agenda`
  entries, and history to learn how the area works today and where the change
  would live.
- Look up external docs, upstream behavior, and prior art when the idea depends
  on them.
- Note the constraints, existing mechanisms that could be reused or extended,
  and the risks the research uncovers.

Keep research read-only. Do not edit, install, or run state-changing commands.

### 3. Interview the user thoroughly

Follow `/interview`, and ask much more than the minimum: the goal is that
nothing about the user's intent is left to assumption. A few extra questions
cost far less than building the wrong thing.

1. **Architecture and product questions first.** Work through
   `references/architecture-questions.md`: purpose, audience, scale, platform,
   distribution, deployment target, business model, payments, accounts, data,
   privacy, integrations, operations, and experience. Ask every entry that
   applies to the request and is not already obvious from it, the repository,
   or an earlier answer. A new project touches most of the list; a feature
   touches the entries it could change. Briefly list the entries skipped as
   obvious, with the evidence, so the user can correct a wrong inference.
2. **Then the request's own questions.** Behavior, edge cases, scope,
   non-goals, success criteria, and how the result will be validated.
3. **Ask in rounds** with the structured ask tool when available, up to four
   related questions per round, and wait for each round's answers. Offer
   concrete options with a recommended one first whenever the answer space is
   known, and keep the free-form answer available.
4. **Follow every answer.** Reflect it, adjust the picture, and ask the
   follow-ups it opens. When a new question is a fact local or web research
   can settle, research it instead of asking.

Keep going until the user's intent, constraints, scope, and success criteria
are crystal clear. Do not stop at the first workable picture; stop only when
no remaining question would change what gets built.

### 4. Check for blockers

Before proposing anything, look for what would stop or derail the work:
missing access or credentials, accounts or paid services that must exist
first, unavailable or abandoned dependencies, platform or licensing limits,
conflicts with existing code, specs, or `.agenda` work in progress, missing
upstream features, legal or compliance constraints, and prerequisites that
are themselves sizeable work.

For each blocker, state what it blocks and the evidence, then classify it:

- **Technical blocker**: resolve the approach with `/decide` and report the
  decision.
- **Human blocker**: present it with the viable ways to handle it, such as
  doing a prerequisite first, changing scope, accepting a cost or risk,
  choosing a provider, or deferring, recommend one, and let the user decide.

Report "no obvious blockers" explicitly when the check finds none.

### 5. Settle the approach with /decide

Hand the settled requirements, the human decisions, and the blocker
resolutions to `/decide` to reach the best overall technical approach: it
researches, compares candidates with `/options`, rates them with
`/criteria`, and checks for hacks and layering. Settle every remaining
technical decision the same way, scaling `/decide`'s depth to the decision.

Present the chosen approach with its runner-up and why it lost, every
technical decision made along the way with a one-line reason, and any
suggestions the research surfaced that go beyond the request, labeled as
suggestions rather than folded into the scope. If `/decide` shows that a
technical choice actually depends on an unanswered human question, return to
step 3 for it.

For an exploration request, the approach may be directions to investigate
instead of an implementation; settle them the same way.

### 6. Confirm the agreed approach and size

Summarize the agreed approach: what will change, where, what stays the same,
the human decisions as locked, the technical decisions as made, and how it
will be validated. Then classify the work:

- **Large undertaking**: spans several modules or areas, needs staged work or
  migrations, carries significant risk or open follow-ups, or would not
  reasonably fit in one focused session.
- **Small change**: a focused, well-understood edit to one area that can be
  implemented and validated in one pass.

State the classification and ask the user, as one final `/interview` question,
to confirm the summary and the next step: create a plan, or implement now.
The user may override the classification or any technical decision.

### 7a. Large undertaking: plan with /agenda-plan-create

Hand the agreed approach to `/agenda-plan-create` to write a plan in
`.agenda/plans/`. Record the human decisions from the interview and the
technical decisions from `/decide` with their rationale, the blockers and how
each is handled, rejected approaches and deferred suggestions as non-goals,
and follow all of that skill's requirements. Do not implement the plan.

### 7b. Small change: implement after confirmation

Only after the user explicitly confirms, implement the agreed change following
the repository's conventions, then run the narrow checks that apply. If
implementation reveals something that invalidates an agreed decision, stop:
settle a technical one with `/decide` and report it, and raise a human one with
the user instead of silently changing course.

## Report

- The request as understood and the key research findings, with file
  references and source links.
- The human decisions, including the architecture questions answered and
  those skipped as obvious.
- The blockers found and how each is handled.
- The chosen approach and the technical decisions `/decide` made, briefly.
- The outcome: the plan file path and its readiness, or the changes made and
  the checks run with their results.
- Suggestions the user deferred and any open follow-ups.

## Boundaries

- Do not edit anything before the user confirms the agreed approach and next
  step.
- Do not treat silence, a vague "fine", or a partial answer as confirmation.
- Do not ask the user a technical question `/decide` can settle, and do not
  settle a human question yourself.
- Do not widen the scope with unrequested suggestions unless the user accepts
  them.
- Do not implement a large undertaking directly; plan it.
