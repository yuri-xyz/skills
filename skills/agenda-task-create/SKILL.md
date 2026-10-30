---
name: agenda-task-create
description: Use when a discussed issue, bug, idea, or follow-up should be recorded as a `.agenda` task for later.
---

# Agenda Task Create

## Objective

Turn the current discussion into a durable `.agenda/tasks` markdown task that can be resumed later without losing the important context.

Use this for actionable work: bugs to fix, investigations to perform, follow-up implementation tasks, cleanup tasks, or decisions that require future action.

## Storage

Follow `/agenda` for storage rules, filenames, IDs, and status conventions. Tasks live in `.agenda/tasks/` and start as `[todo]` unless the local convention or the user's request clearly calls for another status.

## Task Shape

Keep task files concise but complete enough for a future agent to continue without rereading the whole conversation.

Include:

- A clear `#` title.
- The concrete problem or task to handle.
- Relevant context from the discussion, including important symptoms, constraints, decisions, and file paths.
- The desired outcome or completion condition.
- Any known non-goals or boundaries that prevent accidental scope expansion.
- Notes about current status, blockers, or what has already been tried when useful.

Prefer direct, actionable wording. Avoid vague placeholders like "look into this later" unless paired with the exact thing to inspect and why.

## What To Capture

Capture information that would be expensive or error-prone to rediscover:

- Commands, logs, errors, diagnostics, or observed symptoms.
- Relevant files, modules, functions, tasks, plans, PRs, or external references.
- Decisions the user made during the conversation.
- Root-cause hypotheses and why they are plausible or rejected.
- Follow-up actions that remain after the current work.

Do not dump the full conversation. Summarize the important facts and preserve exact snippets only when they are needed to identify the issue.

## Workflow

1. Determine whether the current discussion is actionable enough to be a task. If it is durable knowledge rather than work to do, use `/agenda-note-create`.
2. Create or update one task file that captures the relevant context.
3. Report the task path and the key context captured.
