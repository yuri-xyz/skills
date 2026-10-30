---
name: unblock
description: Use when `.agenda` tasks or plans are blocked on decisions and the user wants them made ready to implement.
disable-model-invocation: true
---

# Unblock

## Objective

Turn `.agenda` tasks and plans that are blocked only on decisions into ready
work. Settle each open technical decision with `/decide` and lock in its
recommendation, ask the user only about decisions a person must own, and update
the entries so `/pending` lists them as ready. This skill decides and edits
agenda entries; it does not implement them.

Invoking this skill is the user's delegation of technical decisions to the
agent. It overrides `/decide`'s default of only proposing, and `/agenda`'s rule
that not-ready entries wait for the user, for the decisions this skill may
settle on its own.

Follow `/agenda` for the workspace layout, filename statuses, the not-ready
disclaimer, and plan sections.

## Scope

1. **Named entries.** When the user names tasks or plans, by ID, title, or
   path, take exactly those. Process a named entry even if it looks
   exploratory, since naming it is the go-ahead; still apply the human-decision
   rule below.
2. **Otherwise, all candidates.** Classify every task with `todo` or
   `in_progress` status and every plan with `planned` or `active` status with
   `/agenda-readiness`, and take the ones it rates **decision-blocked**.
3. **Skip, without asking,** every other class: entries another agent is
   working on, exploratory or deferred entries, entries waiting on something
   other than a decision, and underspecified, manual, or already ready ones.
4. **Limit to 20.** When more than 20 candidates remain, take the 20 most
   recently created or edited. Order by the last commit touching each file
   (`git log -1 --format=%ct -- <path>`), treating uncommitted or untracked
   entries as newest and falling back to file modification time outside Git.
   Mention how many were left out.

## Decision Types

Classify every open decision in an in-scope entry as technical or human, by
`/decide`'s "Human versus technical decisions":

- **Technical**: decide it with `/decide` and lock in its recommendation
  without asking.
- **Human-required**: still run `/decide` on it, then confirm with the user
  before locking it in (see Workflow).

## Workflow

1. **Collect** the candidates per Scope, apply the skips and the limit, and
   list each in-scope entry's open decisions. Group decisions that one coherent
   solution settles together, including across entries.
2. **Decide with `/decide`.** Run it for each decision or group. Scale its
   research to the decision: local research is enough for small choices; use
   web research when the choice turns on external facts, such as an upstream
   API, a release, or a known issue. Keep this phase read-only apart from the
   agenda edits below.
3. **Lock technical decisions.** Update each entry right away, so the results
   survive an interruption:
   - **Tasks:** remove the answered items from `## Open Decisions` and add each
     answer to a `## Decisions` section with the choice and a one-line
     rationale. Fold any facts the research established into the description.
   - **Plans:** record each answer under `## Locked Decisions` with its
     rationale and the rejected alternatives, and update the items it affects,
     following `/agenda-plan-refine`'s rules for a ready plan.
   - When no open decision remains, remove both the `> **Not ready:**`
     disclaimer and the empty `## Open Decisions` section.
4. **Confirm human-required decisions.** Present them together, each marked
   with `⚠️` and carrying `/decide`'s recommendation, rationale, and main risk,
   and ask the user with the available question tool, listing the
   recommendation first. Lock each answer as in step 3. Leave any decision the
   user does not answer in `## Open Decisions` with the `/decide` findings
   attached, so the next pass does not redo the research.
5. **Do not drop work on your own.** If `/decide` concludes an entry should not
   be done at all, treat that as a human-required decision instead of closing
   the entry.
6. **Review** each edited entry: `/agenda-readiness` must now rate it ready,
   manual when its remaining work acts on live external state, or
   decision-blocked when only human-required decisions remain. It must
   keep its ID and status and have no unrelated changes.

## Report

List every in-scope entry with a status marker, then the skipped entries:

```markdown
🔓 **Unblocked**

- 🟢 Task 12: Title — ready; decided: <choice>, <choice>
- ✋ Task 14: Title — decided: <choice>; manual: <live step needing you>
- 🟡 Plan 3: Title — waiting on your answer to ⚠️ <decision>
- 🔴 Task 9: Title — still blocked: <reason>

⏭️ Skipped: Task 7 (exploratory), Task 8 (waits on upstream release), 4 older entries over the limit
```

- 🟢 now ready to implement, ✋ decided but manual because its remaining work
  acts on live external state, 🟡 waiting only on a human-required decision
  you were asked about, 🔴 still blocked for another reason found while
  deciding.
- Then show the entries that became ready in `/pending`'s output format, so the
  user sees where they now rank among the ready work.
- If nothing was in scope, say so and list the skipped entries.

## Boundaries

- Do not implement tasks or plan items; use `/agenda-implement` for that once
  the user asks.
- Do not change entry IDs, rename statuses beyond what `/agenda` requires, or
  delete entries.
- Do not run destructive, costly, outward-facing, or live system-state
  operations while researching or deciding.
- Do not commit unless the user asks; then use `/git-commit`.
