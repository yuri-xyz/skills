---
name: decide
description: Use when facing an important, complex, or hard-to-reverse technical decision, or whenever a technical decision would otherwise be put to the user.
---

# Decide

## Objective

Reach the best overall solution to an important or complex problem through
deliberate research and judgment, instead of jumping to the first plausible
fix. This skill combines `/research`, `/research-web`, `/options`,
`/criteria`, `/hacky`, `/layering`, and `/approach`.
The deliverable is a well-grounded proposal, not an immediate implementation.

## Workflow

1. **Think hard.** Restate the problem or problems at hand, the goal, the
   constraints, and what a good outcome looks like. Name the open questions and
   assumptions before looking for answers. Do not settle on a solution yet.
2. **Research locally with `/research`.** Inspect the relevant code, configs,
   specs, history, and existing mechanisms until you understand how the system
   actually works and where the problem lives.
3. **Research externally with `/research-web`.** Look up current docs, upstream
   projects, prior art, known issues, and how others solved the same problem.
   Prefer primary sources. Invoking this skill directly counts as an explicit
   request for web research; a delegated decision scales it as described under
   "Delegated decisions".
4. **Generate candidates.** Draw several distinct approaches from the research,
   including the obvious one, a more conservative one, and a more thorough one
   when they differ meaningfully. Drop candidates the evidence already rules
   out.
5. **Compare with `/options`.** Rank the strongest candidates, at most
   three, with their pros, cons, and what each entails.
6. **Rate with `/criteria`.** Rate each remaining candidate on
   usefulness, soundness, consistency, and proportionality, and let any `Weak`
   or `Violated` rating reshape or eliminate it.
7. **Screen for hacks with `/hacky` and `/layering`.** Check each
   remaining candidate for workarounds, symptom patches, and fixes layered on
   top of broken behavior instead of changing the code that owns it. Replace
   such candidates with the root-cause version, or drop them.
8. **Confirm with `/approach`.** Judge the leading candidate as the
   long-term architecture: root cause addressed, idiomatic for the codebase,
   scoped proportionately. If it falls short, revise it or promote the next
   candidate.
9. **Propose.** Recommend the best overall solution for each problem. When the
   problems are related, prefer one coherent solution over separate patches.

Iterate when a later step reveals something new: if judging exposes a gap in
the research or a better candidate, go back and close it before proposing.

## Human versus technical decisions

This is the definition other skills use when they decide who settles a
question.

- **Technical decisions** have a defensible answer an engineer can reach from
  the requirements, the codebase, and research: which mechanism, library,
  data model, module boundary, protocol, file layout, or algorithm to use, and
  how to meet a requirement the user already set.
- **Human decisions** rest on the user's intent, audience, money, risk
  appetite, taste, or priorities, with no technical winner, or have broad
  implications: reshaping architecture across many modules or hosts, changing
  the security or privacy model, touching the repository's migration
  boundaries, removing or replacing features, deleting data, costing money,
  or affecting anything outward-facing.

When a question sits between the two, treat it as human. A stated user
preference turns a technical choice into a given; do not reopen it. When a
technical choice turns on a human answer not yet given, that answer comes
first.

## Delegated decisions

By default this skill proposes. When the user or a calling skill delegates a
decision, such as `/autofix`, `/unblock`, `/wizard`, an unattended `/goal`, or
an agent settling a technical question mid-task under the user's standing
instructions, settle each **technical** decision by adopting the recommendation,
record the decision and its one-line rationale where the caller keeps its
work (the plan, task, or report), and let the caller carry on. Still surface
**human** decisions instead of settling them; the caller decides how to ask
or record them. Scale the research to the decision: local research is enough
unless it is high priority or turns on external facts such as an upstream
API, a release, or a known issue, and a delegated decision is not by itself a
request for web research.

## Report

- The problem or problems as understood, in a sentence or two each.
- Key findings from local and web research, with file references and source
  links.
- The `/options` comparison and the `/criteria` ratings.
- The `/hacky` and `/layering` findings, briefly, and the
  `/approach` verdict for the recommendation.
- The recommended solution or solutions, why they win, and the main risks or
  open decisions that remain for the user.

## Boundaries

- Propose; do not implement unless the user asked for implementation as well.
  A delegated decision is settled, not implemented; the caller implements.
- Keep research read-only: no edits, installs, or state-changing commands while
  investigating.
- Surface genuine open decisions, and every human decision, to the user
  rather than resolving them by guesswork.
