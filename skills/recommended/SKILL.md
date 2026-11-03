---
name: recommended
description: Use when the user tells the agent to proceed with recommended options or sensible defaults instead of asking.
---

# Recommended

Proceed with the best clearly fitting recommendations for the current task. Use
senior engineering judgment, local project context, and the user's stated goals
as the decision boundary.

## Default Behavior

- Continue with recommendations that are obviously appropriate for the task.
- Choose conservative, idiomatic options that fit the existing codebase.
- Prefer proven local patterns, existing dependencies, and focused changes over
  introducing new architecture.
- Implement the recommended path end to end when it is within the task scope.
- Validate the result with the narrowest useful checks, then broaden when shared
  behavior or public contracts changed.
- Briefly report what recommendation was applied and why it fit.

## Proceed Without Asking

Go ahead when the recommendation is a clear fit and has bounded blast radius,
such as:

- selecting between small implementation variants already discussed
- adding focused tests, assertions, or validation for changed behavior
- applying formatter, lint, or type-check fixes that preserve behavior
- splitting a modestly growing file along existing module boundaries
- using a standard library helper or existing project helper instead of local
  ad hoc logic
- adding concise comments for non-obvious decisions
- choosing the repo's existing package manager, test command, formatter, or
  build workflow
- making small dependency-free refactors that improve clarity without changing
  user-visible behavior

## Stop For Explicit Approval

Ask before proceeding when the recommendation would be drastic, ambiguous, or
hard to unwind, including:

- rewriting large parts of the repository from scratch
- deleting essential, critical, or large chunks of code
- replacing the main framework, runtime, language, architecture, storage model,
  or deployment model
- adding heavy new dependencies, services, package managers, build systems, or
  external infrastructure
- changing public APIs, data formats, migrations, secrets, authentication,
  authorization, encryption, billing, or destructive persistence behavior
- running live system changes, deployment, activation, switching, install,
  database writes, disk operations, or other state-changing production actions
- removing tests, weakening checks, suppressing diagnostics, or bypassing safety
  mechanisms instead of addressing the root cause
- making broad mechanical rewrites where review cost or merge risk is high
- combining unrelated changes that would make the history misleading

## Judgment Rules

- Treat "recommended" as permission to choose among good options, not permission
  to exceed the user's task.
- If a recommendation has clear local precedent and limited risk, implement it.
- If the best option is large but can be sliced, do the safe first slice and
  describe the larger follow-up.
- If two options are close and both are low risk, pick the one that best matches
  the repository's existing style.
- If the user already gave an explicit instruction that conflicts with the
  recommendation, follow the explicit instruction or explain the conflict.
- Do not ask for confirmation merely because the work is non-trivial. Ask only
  when scope, risk, destructiveness, or irreversibility justifies it.

## Communication

- Keep updates direct: state the recommendation being applied and the reason.
- Do not present every minor choice back to the user.
- When approval is required, identify the risky action, why it crosses the
  boundary, and the smaller safe alternative that can proceed now.
