---
name: options
description: Use when several plans, architectures, or solution approaches need comparing and ranking, or the user asks for options.
---

# Judge Options

## Objective

Turn proposed approaches into a clear comparison that makes tradeoffs and consequences easy to scan.

Use this for plans, architecture options, solution candidates, or proposed fixes. Do not use it for a generic short recap.

## Selection

- Include at most three approaches.
- Put the strongest recommended approach first.
- Omit weak options unless they are important for contrast.
- If fewer than three viable approaches exist, show only the viable ones.
- Keep each section high signal and avoid repeating the same point across every option.

## Required Format

For each approach, use this structure:

````markdown
**Approach Title**

```diff
+ Pro of this approach
+ Another meaningful pro
- Con or tradeoff of this approach
- Another meaningful con
```

What it entails:
- Concrete behavior, architecture, or implementation change
- Another high-value consequence or affected area
````

The pros must come first in the diff block. The cons must come after the pros. Use `+` for every pro and `-` for every con.

## Entails Bullets

The "What it entails" bullets should describe what would actually change if that approach is implemented:

- Behavior changes.
- Architecture or ownership changes.
- Data model, API, validation, or config changes.
- Tests or migration work.
- Operational or maintenance consequences.

Keep these bullets concise and concrete. Do not turn them into implementation task lists unless the user explicitly asks for a plan.

## Final Note

After the options, include a one-sentence recommendation only if it adds clarity beyond the ordering.
