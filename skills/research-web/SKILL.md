---
name: research-web
description: Use when the user explicitly asks for current information researched online with sources.
---

# Research Web

## Objective

Gather current, accurate, well-sourced information from the web about the subject under discussion. The deliverable is the external information itself: what exists, what it says, how it compares, and where it comes from — not a local code change or a repo-specific diagnosis.

## Workflow

1. Clarify what the research needs to answer: what a library/tool/API does, how others have solved a similar problem, what current best practice is, what a project's documentation says, how implementations compare, or what recent changes/releases exist.
2. Break the subject into concrete search queries: exact names, package/repo names, version numbers, error strings, protocol or API terms, and any synonyms worth trying.
3. Search broadly first, then follow the most relevant, authoritative results deeper.
4. Prefer primary and canonical sources:
   - Official documentation and specs.
   - The upstream GitHub/GitLab repository itself: README, source, issues, discussions, releases, changelog, and pinned/highly-relevant PRs.
   - Standards bodies, RFCs, and vendor docs.
   - Maintainer blog posts or release announcements for context primary docs don't cover.
5. Use secondary sources (community articles, blog posts, forum threads, Stack Overflow, Reddit) to corroborate, find real-world caveats, or surface issues not yet documented upstream — not as the primary basis for a claim if a primary source is available.
6. When comparing options (libraries, tools, approaches, repositories), gather comparable information for each candidate: maturity, maintenance activity, license, notable tradeoffs, and community consensus where visible.
7. Cross-check important or surprising claims against at least one other source before reporting them as fact.
8. Keep searching while new queries turn up materially new information. Stop once further searches are only re-confirming what's already found.

## What To Look For On GitHub

When a subject has a relevant repository:

- README and docs directory for intended usage and setup.
- Release notes / changelog / tags for current version and recent breaking changes.
- Issues and discussions for known problems, workarounds, and maintainer stance on a design question.
- Recent commit activity and open PR volume as a rough signal of maintenance health.
- License file when reuse or dependency suitability matters.

Do not clone or fetch full repository contents unless the user's request specifically requires reading source code in depth; prefer browsing rendered pages, README, docs, and issue/PR content first.

## Boundaries

- This skill produces findings, not repository edits. Do not modify project files as part of this skill; if the findings should lead to a code change, say so and let that happen as a separate, explicit step.
- Do not substitute local repository investigation for web research when the question is actually about how this codebase behaves — that is `/research`'s job, not this skill's.
- Do not present a single blog post or forum answer as settled fact when official docs or the source disagree with it.
- Note when information may be version-specific or time-sensitive (e.g. "as of vX" or "as of <date>") rather than stating it as a permanent fact.

## Output Shape

Report:

- Subject: what was researched.
- Findings: the concrete facts, comparisons, or explanations found, grouped by topic or candidate when comparing multiple things.
- Sources: links or clearly named sources for each material claim.
- Caveats: version/time sensitivity, conflicting sources, or open questions still unresolved.
- Relevance: how this maps back to what the user is trying to decide or build, if that context is known.

Keep the report concise but source-backed enough that the user or another agent can verify claims without repeating the same searches.
