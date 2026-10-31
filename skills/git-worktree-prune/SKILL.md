---
name: git-worktree-prune
description: Use when the user wants leftover, unfinished feature worktrees from earlier sessions landed and removed.
disable-model-invocation: true
---

# Git Worktree Prune

Clean up feature worktrees (see `/git-worktree` for the layout) that were left
behind by sessions that never ran `/git-worktree-finish`. Finish every
leftover worktree one at a time, so the default branch ends up with all of
their work and no finished worktree remains. Leave active worktrees alone.

`/git-worktree-finish` keeps all of its constraints here: no lost work, no
history rewriting, no forced removal, and no pushes.

## Workflow

1. **List worktrees** from the main checkout with
   `git worktree list --porcelain`, and check each one with
   `git -C <path> status --short`.
   The main checkout is never a candidate, and neither is this agent's own
   worktree unless the user named it.
2. **Classify each feature worktree** as active or leftover. Treat it as
   **active** and skip it when any of these hold:
   - a live agent is working in it: the session's list of running agents
     shows an agent in that path, or an agent claims it when asked;
   - it has pending changes: modified, staged, or untracked files mean the
     work is unfinished;
   - it is locked (`git worktree lock`), or a merge, rebase, cherry-pick, or
     bisect is in progress;
   - it was active in the last 24 hours: a commit on its branch, or a file
     in it, changed within that window;
   - its name points at agenda work that is still open, such as
     `plan-36-...` or `task-31-...` whose `.agenda` entry is not done and has
     no matching finished work on the branch.

   When unsure, treat the worktree as active. A worktree is **leftover** only
   when it is clean, unlocked, unowned, idle for more than 24 hours, and not
   tied to open agenda work.
3. **Handle missing directories.** For entries whose directory no longer
   exists (`prunable` in the porcelain output), run `git worktree prune` to
   drop only the stale metadata. Delete their branch with `git branch -d` only
   when it is already merged into the default branch; otherwise keep the
   branch and report it.
4. **Finish leftovers sequentially**, oldest last activity first. For each,
   work from inside that worktree and apply `/git-worktree-finish` in full,
   then move to the next. Each one merges the default branch as updated by
   the previous one. When a worktree needs a user decision or its checks
   fail, leave it in place with its merge state intact, record why, and
   continue with the rest.
5. **Report** a table of every feature worktree with its branch, status
   (`finished`, `skipped: active`, `blocked`, or `stale metadata pruned`),
   and the reason, plus the landing commits and the fact that nothing was
   pushed.
