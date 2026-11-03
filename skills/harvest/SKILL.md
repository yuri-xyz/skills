---
name: harvest
description: Use when the user points at a reference repository and wants the improvements it has over this one brought in.
---

# Harvest

## Objective

Learn from a reference repository that already solves problems similar to the
ones in this repository, identify a concrete list of improvements we could
adopt, and turn the user-confirmed subset into a durable implementation plan.

Harvest is a proposal-and-confirm workflow, not an implementation workflow. It
ends with an `.agenda` plan, never with code changes.

## Scope

Harvesting is usually about a specific concept, module, or section of code, not
about "improving the whole repository". Require two anchors before starting:

1. The reference repository: a local path, URL, or described repository that
   contains possible improvements.
2. The target areas: the specific concept, module, feature, or file region of
   this repository the harvest should focus on.

If either anchor is missing or too vague to act on, ask for it before doing any
investigation. Do not run an unfocused harvest across the entire codebase.

## Closed-source references

If the reference is closed-source or proprietary, or using it would mean
reverse engineering or extracting from a binary, installer, package, firmware,
or website, or reproducing distinctive copyrighted creative work, stop and
ask: name the situation and wait for the user's decision before reading
further. Open-source references under a license compatible with the project
need only attribution, recorded the way the project records it.

## Workflow

### 1. Access the reference

- If the reference repository is not available locally, clone it into a
  gitignored scratch path such as `.refs/` before reading it. Verify the path
  is ignored first; never let reference material appear in `git status` or a
  commit.
- Inspect the reference read-only. Do not run its code, tests, or installers,
  and do not modify it.

### 2. Learn the difference

For each target area, understand how the reference repo does it differently:

- Read the corresponding reference code, configuration, tests, and docs until
  the important patterns, invariants, and tradeoffs are visible.
- Read this repository's implementation of the same area just as carefully.
- Compare honestly: the reference is learning material, not ground truth. It
  may be outdated, worse for our goals, or dependent on decisions we do not
  share. Prefer this repository's conventions and architecture when they
  conflict.

### 3. Build the improvement list

Turn the observed differences into a concrete candidate list. Each candidate
must:

- be an obvious, concrete improvement — a named change to a specific file,
  module, option, workflow, or behavior, not a vague aspiration;
- plausibly adapt to this repository's existing style, helpers, and structure;
- not significantly change this project's direction, architecture, or product
  goals — if an idea requires that, reject it as out of harvest scope.

Filter aggressively. Quality over quantity: a short list of clearly valuable,
low-drift improvements beats an exhaustive diff dump. For each surviving
candidate, prepare a one-to-three sentence summary, the practical benefit, and
the main tradeoff or cost, expressed in this repository's terms.

Discard ideas that are refactoring for its own sake, style churn, copy-paste
transplants of large code chunks, or changes that weaken local standards.

### 4. Confirm each improvement via /interview

Run an interview so the user decides every improvement individually:

- Follow the `/interview` skill: use the structured ask tool when available,
  ask the candidates in rounds, and wait for each round's answers.
- Present each candidate as its own confirm/reject question with the summary,
  benefit, and tradeoff from the previous step. Include the option to defer a
  candidate for later instead of accepting or rejecting it.
- Never present the list as a single batch yes/no question, and never treat
  silence, a vague "fine", or partial answers as acceptance.
- Order questions so the highest-confidence improvements come first.
- Do not begin any implementation, and do not create the plan, until every
  candidate has an explicit user decision.

### 5. Plan the accepted improvements with /agenda-plan-create

Collect only the explicitly confirmed improvements and hand them to the
`/agenda-plan-create` skill to produce a comprehensive implementation plan in
`.agenda/plans/`:

- State each confirmed improvement as a concrete, task-based `- [ ]` work item
  grounded in the files and modules identified during investigation.
- Record the confirmed decisions and their rationale, including where the
  user's answers constrained the approach.
- Adapt each idea to this repository's own idioms; do not plan verbatim
  transplants of reference code.
- List rejected and deferred candidates as explicit non-goals so future
  harvests do not re-propose them without new information.
- Follow all `/agenda-plan-create` requirements: edge cases, task-based
  verification, locked decisions, and non-goals.

### 6. Report

Close with a concise summary:

- the reference areas investigated and what differed;
- each candidate with its outcome: accepted, rejected, or deferred;
- the plan file path and its readiness status;
- anything intentionally left out and why.

## Hard Boundaries

- Do not implement, stage, or commit anything as part of a harvest.
- Do not copy whole files, asset sets, large code chunks, branding, secrets, or
  license headers from the reference.
- Do not keep the cloned reference material in a tracked path or let it show in
  `git status`.
- Do not plan or perform changes that materially redirect this project without
  the user explicitly approving that larger scope.
- Do not proceed to planning with unconfirmed improvements in the accepted set.

## Good Use Of Harvest

- Adopting a better helper, validation, test pattern, or workflow that the
  reference has proven in practice.
- Discovering behaviors and edge cases the reference handles that this
  repository does not.
- Learning a cleaner module boundary that can be expressed in this
  repository's own architecture.
