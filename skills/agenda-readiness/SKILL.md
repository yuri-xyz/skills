---
name: agenda-readiness
description: Use when deciding whether an `.agenda` task or plan has the go-ahead to act on or report, such as before picking up, summarizing, bundling, or unblocking agenda work, or when another agent may already be doing it.
---

# Agenda Readiness

## Objective

Decide whether a pending `.agenda` entry is work that can start now, and if
not, why. Other skills, such as `/pending` and `/autopilot`, use these classes
instead of each keeping its own criteria. This skill only classifies; it does
not edit entries.

Follow `/agenda` for the workspace layout, filename statuses, and the not-ready
disclaimer.

## Classes

Read each entry's content, not only its filename, and assign the first class
that applies, in this order:

1. **In progress.** An agent is working on the entry right now (see Activity
   below), in the main checkout or in a git worktree. The filename status alone
   does not make an entry in progress: an `in_progress` task or `active` plan
   that no agent is working on was left unfinished, and gets one of the
   classes below like any other entry.
2. **Exploratory or deferred.** The entry records something being considered
   rather than work that has the go-ahead, so it stays parked even once its
   questions are answered. Signs:
   - the open question is whether to do the work at all, such as "should we
     add this?" or "decide whether to keep X";
   - it is framed as an idea, proposal, evaluation, or investigation with no
     committed outcome;
   - it is marked as deferred, later, someday, or waiting for the user to
     decide whether it is wanted.
   An entry that improves, extends, or fixes something with a clear outcome,
   and only leaves *how* to do it open, is not exploratory.
3. **Waiting.** It cannot start until something outside a decision happens: an
   upstream release, an external party, or another unfinished task or plan.
4. **Decision-blocked.** It has a committed outcome, but carries the
   `> **Not ready:**` disclaimer or an `## Open Decisions` section, or leaves a
   design choice unresolved that implementation depends on.
5. **Underspecified.** No decision is open, but the goal is unclear, the
   approach is missing, or a plan still needs `/agenda-plan-refine` before it
   could be implemented.
6. **Manual.** Everything is settled, but finishing the entry means acting on
   live state outside the repository, which needs the user's oversight rather
   than an agent working alone (see Live State below).
7. **Ready.** None of the above: an agent could implement it now without
   further input, entirely through changes it can review and verify in the
   repository.

When unsure between two classes, choose the earlier, more cautious one. In
particular, when unsure whether an entry is exploratory, treat it as
exploratory.

## Live State

An entry is **manual** when its outcome requires, rather than merely enables,
any of these:

- changing a live cloud, SaaS, or provider account: AWS, Cloudflare, DNS
  registrars and records, GitHub repositories, settings, secrets, or apps,
  OAuth clients, API keys, or billing and paid plans;
- changing the running system outside declarative source: switching, booting,
  or activating a configuration, installing or enabling a service or app
  imperatively, editing runtime state, flashing firmware, or partitioning,
  formatting, or migrating disks;
- configuring other live devices or services, such as a router, NAS, homelab
  host, or deployed server;
- creating, rotating, or moving secret material or credentials;
- publishing or contacting anyone: releases, package uploads, pushes, pull
  requests, issues, emails, or messages to third parties;
- physical or interactive steps only the user can take, such as plugging in
  hardware or signing in through a browser.

A repository change that takes effect at the user's usual rebuild or switch is
not manual: the deliverable is the reviewed change, and applying it is the
user's normal step. When an entry mixes a repository part with a live part,
classify it as manual and say which part could be split off as ready work.

## Activity

Look for two signs of an agent working on an entry. Match an entry by its
path, its `<id>-[` filename prefix, its slug, or clearly matching wording.

- **Worktrees.** List them with `git worktree list --porcelain` and match each
  feature worktree to an entry by its branch or directory name, by commits on its branch that name the entry, or
  by its copy of the entry having a different status or progress.
- **Agent sessions.** Look for Claude Code
  transcripts under `~/.claude/projects/` and Codex rollouts under
  `~/.codex/sessions/` that mention the entry, such as an `/agenda-implement`
  run or edits to the files it names. Ignore the current session.

Count an agent as working only when it was active in the last 30 minutes: a
matching session transcript was written to, or files in the matching worktree
changed, within that window. A matching worktree or session with no activity
in that window is **stale**: the entry is not in progress, but record the
stale worktree path or session so whoever picks the entry up resumes that work
instead of starting over.

## Output

When used on its own, list each entry with its class and a short reason:

```markdown
- 🚧 Task 14: Title — in progress: agent active in `../repo-feature-x`
- ✅ Task 12: Title — ready (stale worktree `../repo-feature-y`)
- 🧭 Task 7: Title — exploratory: asks whether to add the feature at all
- ⏳ Task 8: Title — waiting: upstream release
- ✋ Task 16: Title — manual: creates the Cloudflare tunnel in the live account
- 🔒 Plan 3: Title — decision-blocked: storage format open
- 📝 Task 9: Title — underspecified: no approach
```
