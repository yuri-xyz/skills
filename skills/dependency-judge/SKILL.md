---
name: dependency-judge
description: Use when deciding whether custom functionality should stay local or be replaced by a maintained dependency. For sweeping a whole dependency tree for small dependencies to replace with our own code, use /dependency-tree-compress.
---

# Dependency Judge

Use this skill to decide whether a recent manual implementation should remain local code or be replaced by a well-maintained dependency.

This is a long-term maintainability review. The goal is not to add packages by default; the goal is to choose the simpler, safer, more durable option for the project.

## Review Scope

Inspect the relevant recent work before judging:

- the manual functionality, algorithm, parser, validator, check, integration, or helper;
- call sites and ownership boundaries;
- tests and expected behavior;
- existing project dependencies and package manager conventions;
- the amount of code being maintained locally;
- correctness, security, edge-case, and standards-compliance risks.

Do not evaluate from memory alone when the repository can answer the question.

## Keep Manual When

Prefer the local implementation when it is:

- small, clear, and stable;
- specific to this codebase's model or domain;
- easier to test than a dependency wrapper;
- not implementing a broad standard, format, protocol, parser, crypto, auth, date/time, URL, shell escaping, serialization, or security-sensitive algorithm;
- unlikely to accumulate edge cases;
- free of meaningful maintenance burden;
- more readable than adapting a general-purpose package.

A dependency is not better just because one exists.

## Prefer A Dependency When

Recommend a package when the local implementation is likely to become long-term risk:

- it reimplements a known standard, protocol, format, parser, matcher, resolver, planner, validator, serializer, escaping layer, or security-sensitive behavior;
- correctness depends on many edge cases;
- the algorithm is subtle enough that maintenance would require specialized knowledge;
- a mature package would delete significant code or tests without hiding project-specific logic;
- the project already uses the package family or ecosystem pattern;
- ongoing compatibility with external systems is part of the problem.

Do not replace simple project-specific logic with a broad dependency unless the dependency clearly reduces risk and total complexity.

## Package Trust Gate

Before recommending or adding a third-party package, verify it with current data. Do not rely on memory.

The package should pass all of these checks:

- Its source repository is identifiable, preferably GitHub.
- It meets the GitHub star and security bar in `/dependency-add`, which owns those thresholds and the approval rules.
- The repository shows meaningful activity within the last 3 months.
- If the user specifically cares about comments or discussion freshness, verify the latest issue, pull request, discussion, or review comment is no older than 3 months.
- The package has a current release/version available from the project's package manager or registry.
- The license and maintenance model are acceptable for the project.
- The dependency graph and transitive risk are reasonable for the benefit.

Use the globally available GitHub CLI for GitHub checks. Useful commands include:

```sh
gh repo view OWNER/REPO --json nameWithOwner,description,stargazerCount,pushedAt,updatedAt,latestRelease,licenseInfo,url
gh search issues --repo OWNER/REPO --sort updated --order desc --limit 10 --json updatedAt,comments,title,url
gh search prs --repo OWNER/REPO --sort updated --order desc --limit 10 --json updatedAt,comments,title,url
gh api 'repos/OWNER/REPO/issues/comments?per_page=100' --paginate --jq '.[] | [.updated_at, .html_url] | @tsv'
```

Use the project's package manager or official registry to verify the latest available version. Examples:

```sh
cargo info PACKAGE
npm view PACKAGE version repository license
pnpm view PACKAGE version repository license
yarn info PACKAGE version repository license
python -m pip index versions PACKAGE
go list -m -versions MODULE
```

Pick the command that matches the project. If the package manager has an `add` command, prefer it over hand-editing manifests and lockfiles.

If a candidate package cannot pass the trust gate, do not recommend it as the default. Either keep the manual implementation or continue searching for a better-maintained package.

## Decision Process

1. Restate the local problem and what the manual implementation currently owns.
2. Identify the project package manager and existing dependency style.
3. Decide whether this is the kind of problem that benefits from a dependency.
4. If a dependency may be better, find candidate packages from official registries, current ecosystem norms, and repository context.
5. Verify each serious candidate with the package trust gate.
6. Compare the best package option against keeping the manual implementation.
7. Recommend one path and explain the long-term maintenance tradeoff.
8. If changing code, add the dependency through `/dependency-add`, using the project's normal package manager workflow.
9. Run focused validation after any dependency or implementation change.

## Output Shape

Start with one of these verdicts:

- `Keep manual`: the local implementation is simpler and maintainable.
- `Use dependency`: a verified package is better long term.
- `Unclear`: more code or package ecosystem evidence is needed.

Then include:

- Current implementation: what was reviewed.
- Package candidates: packages considered, including stars, recent activity, latest version, and why they passed or failed.
- Tradeoff: code simplicity, correctness, maintenance, dependency risk, and project fit.
- Recommendation: the concrete path to keep, replace, or defer.
- Verification: tests or checks needed after the decision.

## Guardrails

- Do not add a dependency just to avoid a small amount of straightforward code.
- Do not recommend packages below the `/dependency-add` trust bar unless the user explicitly approves an exception.
- Do not recommend packages with no meaningful activity in the last 3 months unless the package is intentionally complete, widely standardized, and the user explicitly approves the maintenance risk.
- Do not guess the latest version. Verify it through the package manager or registry.
- Do not manually edit lockfiles when the package manager can update them.
- Do not replace project-specific domain logic with generic package behavior that changes semantics.
- Do not hide complex dependency adapters behind wrappers that are harder to maintain than the original code.
