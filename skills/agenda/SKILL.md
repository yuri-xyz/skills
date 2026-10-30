---
name: agenda
description: Use when managing, listing, editing, or organizing tasks, plans, roadmaps, or notes in a repository's `.agenda` workspace and no more specific agenda skill fits.
---

# Agenda Project Workspace

Treat `.agenda/` as a repository-local, human-readable project workspace. Read and
write its Markdown files directly, preserve existing conventions, and keep every
change reviewable in Git.

This skill owns the expected structure of the workspace: layout, filenames, IDs,
statuses, entry shapes, and where they may be written. `/agenda-task-create`,
`/agenda-note-create`, `/agenda-plan-create`, and `/agenda-implement` follow
the rules here instead of restating them.

## Storage Rules

- The Markdown files are the source of truth, and this structure is what they
  must end up matching. Edit them directly. If the repository provides a local
  CLI that produces these same shapes, using it is fine, but the resulting files
  still have to match this guide.
- Use repo-local `.agenda/` storage only. Never write to global state, `$HOME`, or
  any agent directory outside the repository.
- Inspect existing entries of the same type before writing, and preserve the
  local filename pattern, numbering, status marker, title style, and Markdown
  structure even when they differ from this guide.
- Keep unrelated entries untouched, and never place secrets, generated output,
  caches, or scratch artifacts in `.agenda/`.

## Workspace Layout

Use this structure at the repository root:

```text
.agenda/
├── plans/
├── notes/
├── tasks/
└── roadmap/
```

- `plans/`: ordered multi-step implementation plans.
- `notes/`: durable project knowledge, decisions, investigations, and references.
- `tasks/`: bounded actionable work.
- `roadmap/`: higher-level goals and direction.

Do not create `.agenda/docs/`. For project documentation,
follow the repository's existing documentation directory and conventions, such
as a top-level `docs/` directory. If the project has no established location,
ask before creating one.

Create only missing directories needed for the requested operation. Do not
rewrite or normalize unrelated entries.

## Core Workflow

1. Find the repository root and inspect the existing `.agenda/` tree.
2. Read nearby entries of the same type before creating or changing a file.
3. Reuse the established format when it differs from this guide.
4. Choose the next numeric ID by finding the highest numeric filename prefix in
   that collection and adding one. Never reuse an old ID.
5. Create or update the Markdown file directly.
6. Keep each entity's filename status synchronized with its lifecycle state, and
   keep plan item heading statuses synchronized with their checklists.
7. Review the resulting path, content, and diff for accidental unrelated edits.

Use lowercase kebab-case slugs. Keep IDs stable when renaming a title or changing
status. Preserve older nonconforming filenames unless the requested change
requires renaming them.

## Tasks

Name new task files:

```text
.agenda/tasks/<id>-[<status>]-<slug>.md
```

Use `todo`, `in_progress`, or `done` as the status. Start new tasks as `todo`
unless the user gives a different state. When status changes, rename the file
without changing its ID or slug.

Write tasks as:

```markdown
# Task title

Describe the problem, desired outcome, relevant context, constraints, and
important paths. Make the task independently understandable.

## Notes

- 1. Append later discoveries or progress here.
```

Omit `## Notes` until a note exists. Append notes in chronological order instead
of repeatedly rewriting the original description. Record completion evidence in
a final note when it will help future readers.

A task with a `> **Not ready:**` disclaimer and an `## Open Decisions` section
still needs user input. Do not implement or plan it as ready work until the user
resolves those decisions; then record the answers and remove both markers.
Write the disclaimer directly under the title, keep the `todo` status, and list
every open decision with its viable options and any recommendation:

```markdown
# Task title

> **Not ready:** this task has open decisions that the user must resolve
> before implementation. Do not start it until every item under
> `## Open Decisions` is answered and that section is removed.

Problem, context, desired outcome, and relevant paths as usual.

## Open Decisions

- The decision, the viable options, and the recommendation if any.
```

## Plans

Name plan files:

```text
.agenda/plans/<id>-[<status>]-<slug>.md
```

Use `planned`, `active`, or `done` for the plan status. A useful plan normally
contains:

```markdown
# Plan title

Briefly summarize the planned change.

## Goal

State the concrete end condition.

## Context

- Relevant fact or constraint.

## Locked Decisions

- Decision that implementation should preserve.

## Non-Goals

- Work explicitly outside this plan.

## Items

### 1-[todo]-First item

- [ ] Concrete implementation or validation step.

### 2-[todo]-Second item

- [ ] Concrete implementation or validation step.

## Verification

- [ ] Check that demonstrates the goal is met.

## Progress Notes

- YYYY-MM-DD: Durable progress or discovery.

## Risks and Dependencies

- Important risk, prerequisite, or external dependency.
```

Tailor sections to the work; omit empty boilerplate. Use `todo`, `in_progress`,
or `done` in item headings. Keep item IDs stable and update both the heading
status and its checkboxes as work progresses. Mark the plan `done` only after
all required items and verification are complete.

## Roadmaps

Name roadmap files:

```text
.agenda/roadmap/<id>-[<status>]-<slug>.md
```

Use `planned`, `active`, or `done`. Keep roadmap entries conceptual and
outcome-oriented; move detailed execution steps into a task or plan.

```markdown
# Roadmap goal

Describe the intended direction and why it matters.

## Notes

- 1. Append material decisions or progress here.
```

## Notes

Name note files `.agenda/notes/<slug>.md`. Use normal Markdown and choose
sections that fit the material. Notes should capture durable knowledge rather
than actionable work. Prefer tasks or plans when the primary content is work to
be completed.

When updating a note, integrate new facts into the appropriate section and keep
historical context only when it remains useful. Link repository files with
repo-relative paths and never copy secrets or machine-local credentials into
`.agenda/`.

## Finding and Updating Entries

Search filenames and Markdown contents across `.agenda/` before creating a new
entry. Update the existing entry when it represents the same work or knowledge;
do not create duplicates merely because wording differs.

For status changes, rename the entity file and preserve its contents. For title
changes, update the H1 and slug while preserving the numeric ID. For removal,
confirm the user actually wants the durable record deleted; completed work is
normally retained with a `done` status.

## Quality Rules

- Keep entries self-contained, specific, and concise.
- Preserve user-authored context and unrelated notes.
- Separate current facts from historical notes.
- Use checklists for verifiable execution steps, not general prose.
- Avoid timestamps except for progress notes or meaningful lifecycle events.
- Never place secrets, generated output, caches, or scratch artifacts in
  `.agenda/`.
