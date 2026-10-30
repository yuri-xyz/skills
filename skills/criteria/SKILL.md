---
name: criteria
description: Use when deciding whether a proposed feature, design, abstraction, or change is worth doing, or when comparing such proposals on usefulness, soundness, consistency, and proportionality.
---

# Criteria

## Objective

Base the decision on four guiding principles instead of convenience, novelty, or how easy the idea is to explain. State how the proposal scores on each principle, rate it, and let those ratings drive the verdict.

Use this for new features, abstractions, APIs, language or library design, configuration models, and other decisions whose cost outlives the current task. For the narrower question of whether a fix is a durable root-cause solution, use `/approach`. To rank several candidates side by side, use `/options`, and apply these principles to each candidate.

## Principles

- **Useful.** It will be used often and across many kinds of callers, apps, hosts, or workflows, not in a handful of places. Prefer abstractions that express safe, powerful things in little code over ones that are merely easier to explain.
- **Sound.** It behaves correctly and predictably on every input and state, not just the common ones. Nothing is fragile, heuristic, or dependent on a lucky case. A design that needs an unsound shortcut is not done.
- **Consistent.** It fits the existing architecture, conventions, and ownership boundaries, and ideally complements them: one coherent mechanism beats several special cases.
- **Proportionate.** The cost to implement and maintain it is in proportion to how widely and how much it helps. Reject a large implementation that only a few places use. Also reject bloat and speculative or research-grade ideas that do not pay for themselves.

When the repository documents its own guiding principles or design priorities, such as in `AGENTS.md` or `.spec/OVERVIEW.md`, apply them alongside these four. Where the two overlap, the repository's wording wins.

## Ratings

Rate how well the proposal holds up on each principle:

- `Strong`: clearly satisfies the principle, with evidence.
- `Adequate`: satisfies it with caveats, or has gaps that a named change would close.
- `Weak`: falls short on this principle; proceed only with an explicit justification.
- `Violated`: breaks the principle; this blocks the proposal until it is resolved.

Base each rating on evidence: call sites, expected users, failure cases, existing mechanisms, and estimated size. Do not guess when the codebase can answer the question. If the evidence is missing, say so and rate conservatively.

## Workflow

1. Restate the proposal and the problem it solves in concrete terms.
2. Inspect the relevant code, specs, existing mechanisms, and likely callers before rating.
3. Rate each principle and give a one- or two-sentence justification.
4. Derive the verdict from the ratings:
   - Any `Violated` rating means `No`, or `Mostly` only when a specific change removes the violation.
   - Mostly `Strong` ratings with no `Weak` rating support `Yes`.
   - A `Weak` rating needs an explicit justification for proceeding, or a change that raises the rating.
5. When a change would raise a `Weak` or `Adequate` rating, name it concretely.

## Output Shape

Start with the verdict: `Yes`, `Mostly`, `No`, or `Unclear`. Use `Unclear` when the evidence is insufficient, and name what must be inspected or decided.

Then give the ratings table:

```markdown
| Principle     | Rating   | Why |
| ------------- | -------- | --- |
| Useful        | Strong   | ... |
| Sound         | Adequate | ... |
| Consistent    | Strong   | ... |
| Proportionate | Weak     | ... |
```

Then provide:

- Blockers: every `Violated` rating and what resolves it. Omit this when there are none.
- Improvements: concrete changes that would raise `Weak` or `Adequate` ratings.
- Recommendation: proceed, revise, or reject, and why.

Keep the answer direct. Do not bury the verdict behind theory.

## Guardrails

- Do not let one strong principle excuse a `Violated` rating on another; a very useful but unsound design is still blocked.
- Do not rate `Useful` from imagined future callers; cite real or clearly planned uses.
- Do not mark a proposal `Consistent` just because it compiles or evaluates; check it against the existing mechanisms it overlaps with.
- Do not inflate ratings to approve the current direction, or deflate them to justify a rewrite.
