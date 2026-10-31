---
name: hint
description: Use when an instruction is marked `/hint`, meaning it is a suggestion to evaluate, adapt, or reject rather than a directive.
---

# Hint

## Overview

Normally, an instruction in the prompt is a direction to follow. When the user tags part of the prompt with `/hint`, that part is instead an idea worth considering — the user is flagging their own uncertainty about it. Treat it as input to your judgment, not as a command that overrides your own assessment of the best approach for the underlying goal.

This only changes how the tagged instruction is weighed. It does not loosen any other explicit instruction, constraint, or prior direction in the same prompt or conversation — only the specific suggestion is optional.

## Workflow

1. Identify the underlying goal the suggestion is meant to serve (fix the bug, implement the feature, improve the design) separately from the suggestion itself. The goal still needs to be accomplished regardless of what happens to the suggestion.
2. Evaluate the suggestion against what you already know: the current code, recent conversation context, established project conventions, and this repo's agent instruction files, such as `AGENTS.md` or `CLAUDE.md`, guidance.
3. If the fit is unclear from local context alone and the suggestion references an external approach, library, pattern, or claim, do quick research before deciding — reading relevant local code first, and using web research only if the question genuinely depends on external behavior or current best practice. Keep this bounded to what's needed to judge the suggestion, not a full investigation.
4. Decide one of:
   - **Adopt as-is**: the suggestion is a good or best fit — proceed with it.
   - **Adapt**: the core idea is right but needs adjustment to fit this codebase's conventions, constraints, or edge cases — use the adjusted version.
   - **Set aside**: the suggestion doesn't fit, is already superseded by existing code, conflicts with project conventions, or a clearly better approach exists — proceed without it, using your own judgment for how to reach the underlying goal.
5. Proceed to accomplish the underlying goal using the decided approach. Do not stop and only ask for confirmation unless the decision is genuinely close and consequential enough to warrant checking in.

## Judging The Suggestion

Lean toward adopting when the suggestion:

- Matches how similar problems are already solved elsewhere in this codebase.
- Is confirmed as correct/current by a quick check of docs, code, or an authoritative source.
- Is at least as good as the alternative you'd otherwise choose, even if not clearly superior.

Lean toward setting it aside when:

- It conflicts with an existing convention, constraint, or explicit rule in the agent instruction files or the surrounding code.
- Research or local inspection shows it's outdated, deprecated, or based on a mistaken premise.
- A more idiomatic or simpler approach is already visible in the codebase.
- It would introduce risk, complexity, or scope disproportionate to the goal.

## Output

Briefly state the disposition before or alongside the resulting work:

- If adopted: note that the suggested approach was used (a short clause is enough; no need to over-explain).
- If adapted: note what changed from the original suggestion and why.
- If set aside: give a short, concrete reason (one or two sentences), then proceed with the approach actually used.

Keep this brief — the point is transparency about the decision, not a lengthy justification.
