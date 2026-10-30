---
name: research
description: Use before planning, debugging, designing, or fixing something that needs local and external context first.
---

# Research

## Objective

Build enough context to make the next decision or implementation grounded in evidence. Research means reading the relevant local code and project history, understanding how the system actually works, and looking up external information when that could explain the issue or reveal established solutions.

Do not stop at the first plausible explanation. Keep following relevant code paths and references until the important constraints, failure modes, and options are clear enough to proceed.

## Workflow

1. Clarify the question the research must answer: bug cause, plan feasibility, architecture choice, API behavior, dependency behavior, or prior art.
2. Inspect local context first: relevant files, call sites, tests, configs, docs, generated outputs, logs, and recent git history when useful.
3. Trace the code path far enough to understand ownership, inputs, outputs, invariants, error handling, and where state changes.
4. Search the repo for related names, patterns, TODOs, tests, feature flags, issue-specific strings, and nearby implementations.
5. Use web research when the answer depends on external behavior, current docs, third-party libraries, frameworks, operating systems, protocols, error messages, or similar reported issues.
6. Prefer primary sources: official docs, source code, changelogs, standards, issue trackers, release notes, and authoritative discussions. Use secondary sources only as pointers or corroboration.
7. Keep searching while each result reveals new relevant terms, APIs, errors, versions, or code paths. Stop when additional searching is no longer changing the likely conclusion.
8. Summarize the findings with concrete evidence and state what they imply for the next step.

## Local Research

Use local code as the source of truth for how this project behaves, and
explore it to the standard `/explore` sets, which owns what to inspect and how
far to follow it. On top of that:

- Verify assumptions against code rather than relying on naming or comments alone.
- Track open questions explicitly instead of filling gaps with guesses.

## Web Research

Use web research when local context is not enough or when current external behavior matters.

- Search exact error messages, API names, library versions, protocol terms, and behavior descriptions.
- Look for similar bugs, upstream issues, migration notes, breaking changes, and documented edge cases.
- Cross-check important claims across primary sources when possible.
- Record source links or names in the final summary when they informed the conclusion.
- Be clear when a conclusion is an inference from sources rather than directly stated.

Do not browse aimlessly. Each search should target a specific uncertainty from the local investigation.

## Output Shape

Report:

- Question: what the research was trying to answer.
- Local findings: relevant files, code paths, tests, configs, or history.
- External findings: useful docs, issues, examples, or similar cases, with source links when web research was used.
- Conclusion: what is now likely true.
- Implications: what this means for the bug, plan, or proposed fix.
- Next step: the concrete action the evidence supports.

Keep the answer concise, but include enough detail that another agent can continue without repeating the same research.
