---
name: agenda-clean
description: Use when the user asks to clean up, prune, refresh, or declutter a repository's `.agenda` backlog by removing tasks, plans, or roadmap entries that are severely stale or no longer apply and bringing outdated but still valid ones up to date. Not for listing ready work, which is `/pending`, or for judging whether an entry can start, which is `/agenda-readiness`.
---

# Agenda Clean

## Objective

Find pending `.agenda` entries that no longer earn their place and remove
them, and bring entries that still apply but have drifted up to date, so the
backlog only holds accurate work that still matters. Asking for this skill is
the user's confirmation to delete and refresh the entries it finds; act on
clear cases without asking again.

Follow `/agenda` for the workspace layout, filenames, and statuses.

## Scope

Review pending entries only: `todo` and `in_progress` tasks, `planned` and
`active` plans, and `planned` and `active` roadmap entries. Leave `done`
entries and notes alone; they are the durable record.

Skip any entry `/agenda-readiness` would class as **in progress**: another
agent is working on it.

## What To Remove

Remove an entry only when the evidence clearly shows it no longer applies:

- **Already done.** The repository, its history, or another entry shows the
  outcome is in place, even though the entry was never marked done. Mark it
  `done` with a short completion note instead of deleting it when the work is
  substantial enough to be worth keeping on record.
- **Obsolete.** The code, module, app, host, feature, or dependency it targets
  has been removed or replaced, or the repository's instructions now forbid
  the direction it takes (for example, work this repository's `AGENTS.md` or
  `CLAUDE.md` says not to reintroduce).
- **Superseded or duplicate.** A newer task, plan, or roadmap entry covers the
  same work. Merge any context the survivor lacks into it before removing the
  older one.
- **Moot.** The problem it describes no longer reproduces, or the upstream
  issue, release, or decision it waited on resolved it.
- **Severely stale.** It has gone untouched for a long time and its premises
  no longer match the repository: the paths, symptoms, or design it describes
  are gone, so a future agent could not act on it without rewriting it from
  scratch.

Age alone is not a reason. Keep an entry that is old but still accurate, and
keep exploratory or deferred ideas the user parked on purpose unless they are
also obsolete.

When unsure, keep the entry and list it as a candidate instead of deleting it.

## What To Refresh

When an entry still applies but parts of it have drifted, update it in place
rather than removing it:

- fix renamed or moved paths, symbols, commands, and skill or entry references;
- drop steps, symptoms, or context that no longer hold, and note work that has
  since landed;
- point it at the entries or decisions that now relate to it.

Keep its ID, slug, and intent, preserve user-authored decisions, and follow
`/agenda` for appending notes. Do not widen its scope or settle its open
decisions while refreshing it. If the goal itself would have to change, list it
as a candidate instead.

## Workflow

1. List the pending entries and read each one in full.
2. For each, check its claims against the current repository: whether the
   paths and symbols it names exist, `git log` for the files and the entry
   itself (`git log --follow -- <entry>`), related entries, and the
   repository's instructions.
3. Sort each entry into remove, mark done, merge, refresh, keep, or
   candidate, with the evidence that decided it.
4. Apply the clear cases: delete removed entries, rename finished ones to
   `done` with a completion note, fold merged context into the surviving
   entry, and update refreshed entries. Keep unrelated entries untouched.
5. Search `.agenda/` for references to removed entries and update or drop
   them so nothing points at a missing file.
6. Review the diff for accidental edits. Do not commit unless asked.

## Output

Report what changed and what was left for the user, one line per entry with
the reason:

```markdown
Removed:
- Task 12: Title — obsolete: the `foo` module it targets was removed
- Plan 3: Title — superseded by plan 9

Marked done:
- Task 20: Title — already done in `abc1234`

Refreshed:
- Task 15: Title — updated paths after the `nix/hosts` move

Candidates (kept, need your call):
- Task 7: Title — untouched since spring and its approach looks outdated
```

Omit empty sections. If nothing needed cleaning, say so in one line.
