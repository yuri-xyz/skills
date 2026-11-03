---
name: agenda-roadmap
description: Use when the user asks for ideas to expand a project's goals, direction, or roadmap, such as new features, capabilities, or improvements worth pursuing, and wants the chosen ones recorded in `.agenda/roadmap`. Not for planning one feature already chosen, which is `/agenda-plan-create`.
---

# Agenda Roadmap

## Objective

Help the user decide where the project goes next. Research the project and
its field, propose abstract, outcome-oriented ideas, such as features,
capabilities, directions, and improvements, settle with the user which are
worth pursuing, record those as roadmap entries, and offer to plan each one.

Ideas stay at the roadmap level: what the project could become and why it
matters, not how to build it. Detailed steps belong in a later plan.

## 1. Understand the project

Use `/research` to learn what the project is, who it serves, and where it
stands: its README, specs, docs, the main features in code, and the existing
`.agenda` roadmap, plans, tasks, and notes. Note the goals it already
states, what is in progress, and anything recorded as out of scope or
rejected, so ideas build on the direction instead of repeating or reversing
it.

## 2. Research the field

Use `/research-web` to look outward: comparable projects and products,
recent developments in the field, standards and platforms the project builds
on, and what users of similar tools ask for. Keep the sources for each idea
they inform. Take inspiration from the field without proposing to copy any
one product's distinctive features.

## 3. Propose ideas

Draft five to twelve ideas, spread across kinds, such as new capabilities,
audiences, integrations, quality and reliability goals, developer
experience, and long-term direction. For each, write:

- a short title and one or two sentences on the outcome;
- why it matters for this project, citing what the research found;
- a rough size (small, medium, or large) and any dependency on other ideas
  or open decisions.

Drop ideas that duplicate an existing entry, contradict a recorded decision
or the project's stated scope, or that you cannot tie to a reason found in
the research. Order the rest by expected value.

## 4. Confirm with the user

Run `/interview` over the ideas: for each, ask whether to pursue it, adjust
it, or drop it, presenting your recommendation first. Ask also about the
direction questions the ideas raise, such as priorities between them or an
audience to focus on. Record only what the user accepts, with their
adjustments.

## 5. Record the accepted ideas

Write each accepted idea as a roadmap entry with `/agenda`, following its
roadmap conventions: `.agenda/roadmap/<id>-[planned]-<slug>.md`, conceptual
and outcome-oriented, with the intended direction, why it matters, the
research sources, and the user's adjustments. Merge an idea into an existing
roadmap entry when it extends one rather than creating a near-duplicate.

## 6. Offer plans

For each recorded idea, propose whether to turn it into a plan now with
`/agenda-plan-create`, recommending yes for ideas that are settled and ready
to design and no for ones that still need direction. Ask in one batch, and
create plans only for the ideas the user confirms.

## Report

End with the roadmap entries written, the ideas dropped or deferred and why,
and the plans created or offered.
