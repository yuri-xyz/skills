---
name: interview
description: Use when the user's intent, decisions, priorities, or constraints are too unclear to start work without clarifying questions, or when the user asks to be interviewed.
---

# Interview

## Objective

Run a deliberate clarification interview before making a decision-sensitive
change. Ask about the user's intent, priorities, constraints, or desired
outcome in plain language, in focused rounds of one or more questions, then
use the answers to lock decisions and remove material ambiguity. Wait for a
round's answers before asking the next round.

An interview is not a generic questionnaire and it is not permission to make
the user design every implementation detail. Research facts that can be
verified locally or from authoritative sources, infer safe details from the
repository, and ask the user only about intent, tradeoffs, preferences,
constraints, or decisions that materially affect the result.

## Non-action boundary

The interview itself should not change production code, tests, configuration,
live state, or unrelated project files. Do not silently turn an answer into an
implementation, plan edit, task, or specification update unless the surrounding
user request explicitly authorizes that follow-up.

If an active plan or specification is part of the authorized workflow, use the
answers to summarize locked decisions and unresolved questions in the
appropriate place after the user responds. Preserve the user's words and
distinguish confirmed decisions from agent recommendations.

## Before asking

Do a lightweight context pass first:

1. Read the current request and recent conversation closely.
2. Inspect the relevant local plan, code, configuration, or documentation when
   it can answer an objective question without asking the user.
3. Identify the decisions that would change scope, architecture, behavior,
   compatibility, cost, risk, or validation.
4. Group related uncertainties and rank them by how much they affect the work.
5. Ask only the remaining user-owned questions. Do not ask for facts that are
   already visible in the repository or can be established by safe research.

Do not begin implementation while answers to material questions are pending.
If no meaningful ambiguity remains, do not invent an interview just to reach a
question count.

## Question count and quality

Usually ask 10–15 high-value questions when the task has that much meaningful
ambiguity. Ask fewer when all material decisions are resolved, and ask more
only when additional distinct decisions are necessary. Never pad the interview
with repetitive or low-impact questions.

Ask questions in rounds. A round may hold several questions when they are
independent of each other, such as scope, validation, and compatibility
decisions that do not change one another's options. Keep a round small enough
to answer comfortably, usually up to four questions. Put a question in a later
round when its options or relevance depend on an answer that is still
pending, and use a round of one when a single decision gates everything else.
Make each question detailed enough for an informed answer: provide a few
sentences of relevant context, explain the practical tradeoff, and include a
concrete example when it clarifies the choice. After the user answers, the
next turn may briefly reflect what you understood before asking the next
round. Do not dump the whole interview in one turn or list future rounds.

Each question must:

- ask about one primary decision or closely related choice;
- use ordinary language and briefly explain any technical term;
- include enough context, usually two to four sentences, for a person who does
  not know the implementation details to answer confidently;
- explain what the answer controls in a concise `Meaning` line of approximately
  eight to fifteen plain-language words;
- state meaningful tradeoffs in enough detail to explain their practical
  effect, without steering the user toward an unsupported answer;
- make each option a complete, descriptive sentence rather than a one-word
  label; use one or two sentences when the consequences need more explanation;
- use a small concrete example when the decision would otherwise be abstract;
- offer a clear way to say “I’m not sure; recommend a default” when that is
  reasonable;
- allow free-text clarification when fixed choices cannot capture the intent.

Prefer questions that lock decisions in roughly this order, adapting to the
actual task:

1. What outcome should exist when the work is complete?
2. How will success be recognized or measured?
3. Which users, workflows, or surfaces are in scope?
4. What is explicitly out of scope or should remain unchanged?
5. Which priority wins when correctness, simplicity, speed, compatibility,
   privacy, or completeness conflict?
6. Should the change extend an existing path, replace it, or preserve both?
7. Which platform, data, security, privacy, migration, or operational
   constraints must the result respect?
8. What should happen for invalid input, limits, partial failure, cancellation,
   or unexpected conditions?
9. Is compatibility with existing behavior, formats, users, or deployments
   required, and for how long?
10. What evidence or validation is sufficient to consider the work complete?

Do not ask all ten categories mechanically. Replace irrelevant questions with
the next decision that would materially change the implementation or outcome.

## Structured ask tools: always prefer them

Before writing questions inline, inspect the currently available tools. If any
structured ask, question, or user-input tool is available, always use it. Do
not fall back to a normal Markdown message merely because the tool supports
only a few questions per call. Give the tool the current round's questions in
one call, within its per-call limit, and wait for the user's response before
making the next call. Do not configure automatic resolution when explicit user answers
are required.

When the tool supports choices, provide two or three genuinely distinct
options. Order them from most recommended to least recommended, top to bottom.
The first option must be the best-supported recommendation, and its visible
label must end exactly with `(Recommended)`. Base that recommendation on
repository evidence or a clearly stated sensible default; if no responsible
recommendation can be made, ask an open-ended question instead of fabricating a
ranking. Give each option enough context to explain its practical consequence,
normally one detailed sentence or two short sentences rather than just a
label. Let the tool's built-in free-text or “Other” path handle answers outside
the choices.

Use the tool's own headers, IDs, and option schema. Do not duplicate the same
questions in a Markdown message after a successful tool call. Do not put a
blocking question in commentary when the structured tool can present it to the
user directly. A later tool call may ask the next round only after the current
answers have been received and handled.

## Markdown fallback when no ask tool exists

Only when no structured ask tool is available, ask the current round in a
normal Markdown message. Keep the format stable and make every possible answer
addressable:

```markdown
1. What outcome should this work deliver when it is complete?

   The answer sets the main boundary for the work. For example, a focused
   correction may leave surrounding architecture unchanged, while a broader
   redesign may change interfaces or migration work.

   Meaning: Establishes the primary result and scope boundary.

   1a) A focused fix (Recommended)
       Preserve nearby behavior and interfaces wherever possible. This is
       usually the smallest and lowest-risk option.
   1b) A broader redesign
       Address related problems or structural limitations as part of this
       change. This may produce a cleaner result but increases scope and
       validation effort.
   1c) I am not sure; recommend a default
       Ask for a recommendation after inspecting the repository and explaining
       the consequences of the available approaches.
```

Rules for the fallback format:

- Number questions sequentially from `1` onward across the whole interview.
- Present the current round's numbered questions together, separated clearly.
  After the answers, continue with the next unused number in a later turn.
- Label choices with the current question number and a letter, such as `1a)`
  and `1b)`, so the answer remains unambiguous.
- Order choices from most recommended to least recommended. The first choice's
  visible label must end with `(Recommended)`; do not put that suffix on any
  lower-ranked choice.
- Put the regular question first, follow it with the fuller context, and then
  provide the concise `Meaning:` explanation before the choices.
- Keep `Meaning:` to approximately eight to fifteen plain-language words, and
  use the surrounding context for the fuller explanation.
- Make choices mutually understandable and describe what selecting each one
  would entail in complete sentences. Include an “I’m not sure; recommend a
  default” choice when appropriate.
- Invite free text after the choices, for example: “Reply with `1a, 2b`; add
  details if useful.”
- If a question is inherently open-ended, still give it answer IDs such as
  `1a)`, `1b)`, and `1c)` for likely directions, then explicitly allow a
  written answer.

The user should be able to answer the current round compactly while adding
detail where useful, for example:

```text
1a, 2b; I want the smallest safe change, and existing imports and public behavior
must remain compatible. I am open to a broader refactor later if the repository
evidence shows the current structure is the root cause.
```

Do not make the user reconstruct questions from earlier turns.

## Make the questions accessible

The user may know the desired result without knowing the technical vocabulary
or all implementation consequences. Help them answer without taking control
of the decision:

- briefly define unfamiliar terms in the question or `Meaning` line;
- describe choices by their effect on the user, behavior, maintenance, or
  rollout rather than by framework jargon;
- use small concrete examples when they clarify a genuine distinction;
- offer a sensible default or recommendation with its tradeoff when the user
  says they are unsure;
- do not pretend that a choice is simple when it has a meaningful cost or
  irreversible consequence;
- separate decisions the user must make from details the agent can safely
  choose later.

Avoid compound questions that hide several independent decisions. If two
answers can vary independently, ask two separately numbered questions, in the
same round when neither depends on the other.

## Answer handling

After receiving answers:

1. Map each response to its question ID and record the decision in
   plain language, including any recommendation the user accepted or rejected.
2. Briefly reflect what you understood, including the practical consequence for
   scope or design. Do not merely say “got it,” and do not turn the reflection
   into a second question.
3. Separate locked decisions, remaining assumptions, and unresolved questions.
4. Detect contradictions or partial answers. If one needs clarification,
   include that focused clarification in the next round, ahead of new topics.
5. If material questions remain, ask the next round of highest-value
   unresolved questions in a new turn. Do not include a list of future rounds.
6. Do not treat silence, an unanswered question, or a vague “fine” as approval
   of a material choice.
7. Continue the requested work only after all implementation-blocking choices
   are resolved or explicitly deferred with a stated default.

If a user answers more than the current round, record useful information and
drop the questions it already settles from the next round.
Do not repeat questions whose answers are already clear. If new implementation
or research facts change the decision space, explain the change briefly and ask
the smallest focused follow-up in the next round.

## Interview quality checklist

Before sending questions, confirm:

- [ ] The questions resolve decisions, not facts already discoverable locally.
- [ ] The interview usually has 10–15 questions, without filler or duplicates,
      and may stop earlier or continue longer when the decisions require it.
- [ ] Each round holds only questions independent of pending answers, and
      stays small enough to answer comfortably.
- [ ] Each question has one clear decision, useful context, and an
      eight-to-fifteen-word `Meaning`.
- [ ] Each round's answers receive a substantive reflection before the next
      round.
- [ ] The wording is understandable without deep implementation knowledge.
- [ ] Relevant tradeoffs, scope boundaries, constraints, and success criteria
      are represented.
- [ ] Invalid input, limits, partial failure, cancellation, or compatibility
      questions are included when they could change the result.
- [ ] A recommendation or “not sure” path is available where appropriate.
- [ ] Choice lists are ordered from most to least recommended, with the first
      visible label ending in `(Recommended)`.
- [ ] The structured ask tool was used if any such tool is available.
- [ ] Inline fallback choices have stable IDs such as `1a)` and `1b)`.
- [ ] The agent has not implemented or silently locked an unanswered choice.

## Completion report

After the interview, report briefly:

- which decision IDs were answered;
- the resulting locked decisions and accepted defaults;
- remaining assumptions or follow-ups;
- whether work can proceed or needs another focused question.

Keep the durable record in the authorized plan, task, or specification when
that workflow calls for it; otherwise keep the summary in the conversation.
