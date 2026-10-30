---
name: examples
description: Use when the user gives examples, sketches, placeholders, or partial ideas and expects the full result inferred from them.
---

# Examples

Use this skill whenever the user provides examples, sample items, rough concepts, simple sketches, partial lists, placeholders, or intentionally casual wording.

## Core Rule

Treat user-provided examples as intent signals, not as an exhaustive specification or text to copy 1:1.

Examples are illustrative unless the user explicitly says they are exact, exhaustive, or must be copied verbatim. Use them to understand the pattern, goal, constraints, tone, and level of abstraction the user is pointing toward.

## Required Behavior

When examples are present:

1. Infer the underlying intent behind the examples.
2. Identify the reasonable next cases, variants, edge cases, or adjacent items implied by that intent.
3. Expand partial lists into the complete practical set needed for the task.
4. Refine vague, simple, inconsistent, or placeholder examples into a coherent production-ready form.
5. Match existing project patterns, architecture, naming, style, and quality bar.
6. Prefer the version the user likely meant over the literal minimal version they happened to type.

## Do Not

- Do not treat examples as exhaustive unless the user says they are.
- Do not copy vague examples literally when they need refinement.
- Do not preserve inconsistencies from an example when the surrounding system has a clearer pattern.
- Do not implement only the named examples if the task naturally requires the full reasonable set.
- Do not use "the user only listed X" as a reason to omit obvious adjacent work.

## If Exactness Matters

If the difference between illustrative and exact examples would materially change scope, cost, risk, or user-visible behavior, make the assumption explicit. Ask only when a reasonable production interpretation would be risky or irreversible.
