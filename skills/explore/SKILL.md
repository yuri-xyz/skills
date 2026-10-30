---
name: explore
description: Use before planning, judging, or editing an unfamiliar or broad area of local code that needs understanding first.
---

# Explore

## Overview

Use this skill to raise the minimum standard for local code exploration. The goal is to inspect enough relevant files, call paths, tests, configuration, and nearby patterns that conclusions are grounded in how the codebase actually fits together.

## Exploration Standard

Do not stop after the first plausible file or the first matching search result. Follow the relevant path until the important ownership boundaries, data flow, and existing patterns are visible.

Explore more than usual, but keep it bounded. This is not a mandate to read the entire repo or chase every transitive dependency. Prefer a wider pass over directly relevant code and one or two nearby ownership layers.

## What To Inspect

Choose from these based on the task:

- The owning file or module for the behavior under discussion.
- Callers, callees, importers, exports, trait implementations, module wiring, or command dispatch that connect to the behavior.
- Tests, fixtures, snapshots, validation checks, and failure cases around the behavior.
- Adjacent modules that solve similar problems or define local style.
- Configuration, generated code, schemas, feature flags, constants, environment variables, or assets consumed by the code path.
- Existing helpers, abstractions, or docs that may already encode the intended pattern.
- Recent diffs or git history when the issue may be regression-related.

## Workflow

1. State the exploration question or target area in one sentence.
2. Start with fast repository discovery: use `rg`, `rg --files`, language-aware navigation, package manifests, or module indexes.
3. Read the most relevant file first, then follow names, types, commands, options, paths, and tests outward.
4. Search for the same identifiers, error strings, option names, commands, routes, file paths, or data shapes across the repo.
5. Compare at least one nearby analogous implementation when the codebase has one.
6. Keep a short working map of what each file contributes so the final answer is not just a list of filenames.
7. Stop when new lookups are no longer changing the likely conclusion or the next files are clearly outside the requested scope.

## Depth Guidelines

For small questions, inspect the owner, at least one caller or callee, and the relevant tests or configuration if they exist.

For medium questions, inspect the owner, main call path, tests, nearby analogous code, and any configuration or generated output that affects behavior.

For broad audits, identify subareas first, then sample each relevant ownership area enough to avoid conclusions based on one isolated file.

## Avoid

Do not:

- Declare conclusions after only one or two superficial reads when more directly relevant context is available.
- Rely on filenames, comments, or naming alone when code can verify the behavior.
- Chase unrelated files just to increase count.
- Turn exploration into implementation unless the user asked for a fix or change.
- Ignore tests or configs when they are central to the behavior.
- Let one matching search result hide other implementations with different names.

## Output

When reporting findings:

- Summarize the path explored, not every command run.
- Reference the key files and why they mattered.
- Separate observed facts from inferences.
- Call out gaps that remain unexplored and why they were out of scope.
- End with the next concrete action the explored context supports.

When editing after exploration, briefly state the context that informed the change before touching files.
