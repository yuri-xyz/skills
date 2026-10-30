---
name: agenda-note-create
description: Use when durable, non-actionable project knowledge, such as a finding, rationale, or reference, should be saved as a `.agenda` note rather than a task or plan.
---

# Agenda Note Create

## Objective

Turn the current discussion into durable repo-local knowledge for future agents or maintainers.

Use this for non-actionable or reference-oriented context: explanations, architecture notes, decisions, research findings, operational knowledge, migration context, conventions, and lessons learned.

If the item is primarily actionable work to do later, use `/agenda-task-create` instead.

## Storage

Follow `/agenda` for storage rules, filenames, and local conventions. Notes live in `.agenda/notes/`, named with a descriptive kebab-case slug. Do not put project documentation in `.agenda/`; follow the repository's existing documentation directory instead.

## Note Shape

Keep notes clear, organized, comprehensive, and descriptive enough to be useful later without needing the original conversation. Include:

- A clear `#` title.
- The reason this knowledge matters.
- The relevant context, constraints, decisions, or findings from the discussion.
- File paths, commands, links, examples, or references when they make the note actionable to future readers.
- Current status or caveats if the information may change.

Prefer structured sections when the note contains multiple concepts. Do not make notes terse at the expense of missing important context, rationale, examples, constraints, or caveats.

## What To Capture

Capture durable knowledge that should survive the conversation:

- Architecture decisions and rationale.
- Project conventions or workflow rules.
- Research summaries and source references.
- Known pitfalls, migration constraints, or compatibility notes.
- Explanations of why an approach was chosen or rejected.

Do not create a note for ephemeral status, temporary debug logs, or obvious facts already documented nearby. Update an existing note instead of creating a duplicate when there is a clear home for the information.

## Workflow

1. Decide whether to update an existing note or create a new one.
2. Write a comprehensive, descriptive note with enough context to stand alone.
3. Report the note path and the key knowledge captured.
