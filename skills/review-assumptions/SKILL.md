---
name: review-assumptions
description: Use when the user asks to review, list, check, or confirm the assumptions behind recent work, a plan, a decision, or the topic under discussion, or wants to be sure before relying on important work, code, or conclusions. For latent edge-case bugs in a diff use `/review-bugs`, and for weak checks such as string sniffing use `/fragile`.
---

# Review Assumptions

## Objective

Bring every assumption behind the recent work, or the subject under
discussion, into the open, then check each one against evidence instead of
memory. Work built on an unchecked assumption is only as sound as that
assumption; this skill turns "I believe" into "I checked" or "this is
wrong".

## Scope

Take the subject from the user's request. Without one, use the recent work in
the conversation: the changes made, the plan followed, the decisions taken,
and the claims made to the user. Include assumptions the user stated, as well
as your own.

## 1. List the assumptions

Go through the work and write down everything taken as true without having
seen or verified it in this session.

What counts:

- **Not an assumption:** a fact written in a spec, doc, code, config, test,
  or command output that was actually read or seen this session and that the
  work uses as written.
- **An assumption:** anything the work relies on without having seen it this
  session, such as recalled behavior, guessed file contents or defaults,
  facts taken from a summary or memory, inferences beyond what the source
  says, or a source read earlier that may have changed since.

Assumptions come from our own code and from everything outside it, including
third-party libraries, dependencies, services, APIs, platforms, and systems,
and from the environment the work runs in, such as the OS, network, and
hardware.
Look in particular for:

- **Code and APIs:** how a function, option, flag, or command behaves; its
  signature, defaults, return values, and error cases.
- **Third parties:** how a library, dependency, service, API, platform, or
  system behaves at the version or plan actually in use, including its
  limits, quotas, defaults, errors, and guarantees.
- **Environment:** the OS and its version, kernel, shell, filesystem,
  hardware, network and DNS, proxies, connectivity, time zone and locale,
  paths, tools and their versions, permissions, and what is installed,
  running, or reachable.
- **Data and inputs:** formats, sizes, encodings, ranges, ordering, and which
  cases cannot occur.
- **Behavior and state:** what the code did before the change, what callers
  rely on, what a test or check proves, and that it ran and passed.
- **Requirements and intent:** what the user wants, what is in scope, and
  which constraints, conventions, or decisions apply.
- **External facts:** upstream behavior, standards, limits, licensing, and
  anything recalled from training rather than read.
- **Reasoning:** causal claims, such as "this fixes it because", and
  generalizations from one case to many.

State each assumption as one specific, checkable claim, with where it was
relied on. Skip trivia that cannot affect the outcome.

## 2. Sort and rank them

Split the list in two:

- **Intent and preference:** assumptions about what the user wants, prefers,
  or meant, such as scope, priorities, product or UX direction, naming,
  style, trade-offs, and which option they would pick. Only the user can
  confirm these, unless they already said so in this conversation or the
  project records it.
- **Verifiable:** everything else, which evidence can settle without the
  user.

Order each group by impact if the assumption were false: correctness,
security, data, money, or user-facing behavior first, then cost of rework,
then cosmetic.

## 3. Align with the user first

When any intent or preference assumption is left, tally all of them before
checking anything, then run `/interview` once over the whole tally, highest
impact first, offering the assumed answer as the recommended option. Record
each answer as confirmed or corrected. Do not interleave questions with
verification, and do not ask about anything evidence can settle.

When none are left, skip this step and verify without asking.

## 4. Verify the rest

Then review every verifiable assumption automatically, highest impact first,
including any the user's answers created or changed. Check each with the
strongest evidence available, cheapest first:

- read the code, config, docs, or manifest that owns the fact, at the
  version actually in use;
- run a narrow command, evaluation, query, or focused test, following the
  repository's rules for heavy or state-changing commands;
- check the authoritative external source, such as upstream docs, the source
  of the pinned version, or a standard.

Record a verdict for each:

- **Confirmed:** with the evidence, such as a file and line, a command and
  its output, or a source.
- **Refuted:** with what is actually true and what the work got wrong as a
  result.
- **Unverifiable:** what blocks checking it, and the risk of leaving it.

Never mark an assumption confirmed from memory, from how plausible it seems,
or from the fact that nothing has failed yet.

## 5. Act on the results

- Fix work that rests on a refuted or user-corrected assumption when the fix
  is clear and in scope, then re-run the checks that cover it. Report the
  rest with what it affects.
- Settle technical questions a refuted assumption reopens with `/decide`.
- Record durable findings where the work's records live, such as the agenda
  entry's notes.

## Report

```markdown
🔎 **Assumptions**

- 🔴 Refuted: <claim> — actually <truth>; affected <what>; fixed in <where> / still open
- 🟡 Corrected by you: <claim> — you said <answer>; changed <what>
- ⚪ Unverifiable: <claim> — <why it cannot be checked>; risk <what>
- 🟢 Confirmed: <claim> — <evidence>
```

Mark lines with the markers shown above, lead with refuted and open items, and keep
each line to one claim.
