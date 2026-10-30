---
name: research-literature
description: Use when academic papers could inform the current task, plan, decision, or exploration, or when the user asks for a literature search.
---

# Research Literature

## Objective

Find the academic papers that matter for the task, plan, decision, or
exploration at hand — the most relevant ones, plus popular, recent, or
noteworthy work in the area — and extract the ideas and approaches worth
adopting from them. This skill combines `/criteria`, `/harvest`, and,
when the user is deciding something, `/interview`.

Papers are learning material, not ground truth. A result only counts when it
fits the work at hand; a clever idea that does not survive judgment against
this project is discarded, however well cited.

## Mode

Decide the mode from the request before starting:

- **Decision**: the user intends to make decisions from the findings — choose
  an approach, shape a plan, settle a design. End with step 6.
- **Research only**: the user wants to know what the literature says. Skip
  step 6 and end with the report.

If the request does not make the mode clear, default to research only and say
so in the report.

## Workflow

### 1. Frame the search

Restate the subject in a sentence or two: the problem, the constraints, and
what a useful paper would contribute — a technique, an algorithm, a design, an
evaluation, a negative result. Inspect the relevant local code, plans, or
discussion first when the subject is grounded in this repository. Derive the
search terms from it: the field's own vocabulary, synonyms, named techniques,
known authors or venues, and arXiv categories when they apply.

### 2. Search

Use the web search tool to locate papers on arXiv, Semantic Scholar, Google
Scholar, the ACM and IEEE digital libraries, USENIX, OpenReview, and author or
lab pages. Keep downloaded full texts outside tracked repository paths.

Search wide before deep: several query phrasings, both relevance and
newest-first ordering, and citation or related-paper expansion from the
strongest hits. Include well-known foundational work alongside
recent results. Stop when new queries only resurface papers already seen.

### 3. Filter by title and abstract

Cut noise quickly. Drop papers on a different problem, ones whose assumptions
this work cannot meet, superseded versions, surveys that add nothing beyond
their sources, and results that are only tangentially related. Read abstracts,
not full texts, at this stage. Keep a short reason for each paper you keep so
the next step has something to judge.

### 4. Narrow with /criteria

Judge each remaining candidate's core contribution, as it would apply here,
with `/criteria`: useful for this work, sound under its stated
assumptions and evaluation, consistent with the project's architecture and
direction, and proportionate in the cost of adopting it. Drop candidates with a
`Violated` rating and those whose `Weak` ratings have no justification.
Read the full text of borderline candidates when the abstract cannot settle a
rating. Repeat until the remaining set is the best one, not merely a short one.

### 5. Harvest with /harvest

Treat the final paper set as the `/harvest` reference and the task, plan, or
area under discussion as its target. Follow its investigation discipline: read
each paper closely, compare its approach honestly with how this project does or
would do the same thing, and turn the differences into concrete candidates
expressed in this project's terms, each with its benefit and its main tradeoff.

Harvest as much as is genuinely useful. There is no target count: take every
idea, technique, approach, or decision the papers support that fits the work,
and stop when what remains is marginal or off-target. Credit each candidate to
its paper or papers.

`/harvest`'s confirm-and-plan steps run only in decision mode, through step 6
here. In research-only mode, report the candidates instead.

### 6. Propose with /interview (decision mode only)

Follow `/interview` to present the strongest findings as decisions for the
user: each candidate's summary, the papers that support it, its benefit, and
its tradeoff. Put the highest-confidence findings first, and let the user
accept, reject, or defer each one individually. When accepted findings warrant
a plan, continue with `/harvest`'s planning step.

## Report

- The subject as framed, the mode, and the search tool used with its main
  queries.
- The funnel: how many papers were found, kept after title and abstract
  filtering, and kept after `/criteria`, with the reason for each
  final paper.
- The harvested findings, each with its supporting papers, benefit, tradeoff,
  and — in decision mode — the user's decision.
- Citations for every paper discussed: title, authors, year, and arXiv ID, DOI,
  or link.
- Caveats: preprints without peer review, results that depend on assumptions
  this work does not share, and conflicting findings.

## Boundaries

- Keep research read-only: no repository edits, installs, or state-changing
  commands while searching, judging, or harvesting.
- Do not run code, artifacts, or scripts that accompany a paper.
- Do not present a paper's claim as settled when its evaluation is narrow or
  other papers dispute it.
- Do not cite papers that were not actually found and read; never invent
  titles, authors, or results.
