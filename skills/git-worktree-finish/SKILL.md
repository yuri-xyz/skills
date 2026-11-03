---
name: git-worktree-finish
description: Use when the user asks to finish, land, or merge back a feature worktree created with /git-worktree.
---

# Git Worktree Finish

Land the agent's own feature worktree (see `/git-worktree` for the layout) on
the default branch and then remove it. Removal is the last step and happens
only when verification proves every commit and file of value is already on the
default branch. When in doubt, keep the worktree and report why.

## Core Constraints

**Never lose work.** Never run `git worktree remove --force`,
`git branch -D`, `git reset --hard`, `git clean`, `git stash`, `git checkout`,
or `git restore`. Never delete `.git` lock files
or another agent's files.

**Never rewrite history.** Integrate with regular `git merge` only. Do not
rebase, amend, squash, reword, absorb, cherry-pick to replace commits, or
force-push. A merge commit in the feature branch is the expected way to pick up
the default branch.

**Never disturb other work.** Outside the agent's own worktree, the only
allowed mutations are the commit in step 3, the fast-forward merge in step 7,
and the artifact cleanup in step 10. Do not touch other feature worktrees.

**Stay local.** Do not push. Pushing needs the user's explicit approval.

## Workflow

1. **Identify.** Confirm the current directory is a feature worktree, not the
   main checkout, and note its path and `feature/<name>` branch. Find the main
   checkout and default branch with `git worktree list` (the first entry and
   its branch). If the current directory is the main checkout, stop: there is
   no worktree to finish.
2. **Commit the worktree's pending work** with `/git-commit`, including its
   Spec Sync Gate. Skip this when the worktree is clean.
3. **Settle the main checkout.** If the main checkout has pending changes,
   commit them there with `/git-commit`, but skip its Spec Sync Gate and
   run no checks. Do not message the
   agents working there about it. If a commit is already in progress, wait
   for it.
4. **Merge the default branch into the feature branch**, inside the feature
   worktree:

   ```bash
   git merge --no-edit <default-branch>
   ```

   This keeps conflict resolution inside the agent's own worktree, away from
   the main checkout.
5. **Resolve conflicts properly.** For each conflicted file, read both sides
   and the merge base (`git diff`, `git log --merge -p <path>`) and produce a
   result that keeps the intent of both. Do not resolve by blindly taking
   "ours" or "theirs", and do not drop the other side's changes to make the
   merge pass. Settle technical decisions that do not need the user's input
   with `/decide`. Stop and ask the user when a resolution changes product
   behavior, discards either side's work, or is otherwise genuinely theirs to
   decide; leave the merge in progress in the feature worktree and report. Once
   resolved, stage the files and finish with `git commit --no-edit`.
6. **Validate the merged result** in the feature worktree with `/checks`.
   Fix failures caused by the merge at their root cause, commit the fixes, and
   repeat until checks pass. If a failure is not caused by this work, report it
   instead of landing on top of it unknowingly.
7. **Land with a fast-forward** in the main checkout:

   ```bash
   git -C <main-checkout> merge --ff-only feature/<name>
   ```

   The feature branch already contains the default branch, so this only moves
   the default branch forward. If it refuses because the default branch moved,
   repeat from step 3. If it refuses because pending files in the main checkout
   would be overwritten, repeat from step 3 rather than forcing it.
8. **Verify nothing can be lost.** All of these must hold before removal:
   - `git merge-base --is-ancestor feature/<name> <default-branch>` succeeds;
   - `git -C <worktree> status --porcelain` is empty, so no tracked changes or
     untracked files remain;
   - `git -C <worktree> status --porcelain --ignored` lists only regenerable
     output such as build directories, caches, `.direnv/`, and dependency
     directories; any ignored file that is not obviously regenerable (notes,
     `.env` files, `.debug/` traces, local data) blocks removal until the user
     decides;
   - no merge, rebase, cherry-pick, or bisect is in progress in the worktree;
   - `git -C <worktree> stash list` shows no stash created on this branch.

   If any check fails, keep the worktree and branch and report what is left.
9. **Remove the worktree** from the main checkout, never from inside the
   worktree being removed:

   ```bash
   git -C <main-checkout> worktree remove <worktree-path>
   git -C <main-checkout> branch -d feature/<name>
   ```

   Both commands refuse to discard unmerged or modified work; if either refuses,
   stop and report instead of forcing it. Move this agent's working directory
   to the main checkout afterwards.
10. **Free the worktree's build output.** Removing the worktree already deletes
    the ignored output inside it, such as `target/`, `node_modules/`, and
    `.direnv/`; note its size with `du -sh` before step 9 for the report.
    Then look for regenerable output kept outside the worktree that belonged
    only to it, for example a `CARGO_TARGET_DIR` or other build directory
    redirected to a per-worktree path, devenv or direnv state keyed by the
    worktree path, or `result` links in the main checkout that point into the
    removed worktree. Delete an item only when all of these hold:
    - its path or a recorded key names the removed worktree path or
      `feature/<name>`, so no other checkout or worktree can be using it;
    - it is regenerable build or cache output, not notes, traces, `.env`
      files, or local data;
    - it is not a symlink to elsewhere that the delete would follow (delete
      the link itself, never its target).

    Delete with `rm -rf -- <exact-path>` on each resolved, absolute path; never
    use globs or variables that could expand to a parent or shared directory.
    Leave shared caches alone (sccache, `~/.cargo`, `~/.cache/go-build`,
    package manager stores, other projects' caches), and do not run
    `nix-collect-garbage` or `nix store gc`, which reach beyond
    this worktree; Nix drops GC roots whose links were removed with the
    worktree on its next collection. When unsure whether an item belongs only
    to this worktree, keep it and list it in the report. Skip this step when
    the worktree was kept.
11. **Report** the merge and landing commits, any conflicts and how they were
    resolved, the check results, whether the worktree was removed, the build
    output freed and its approximate size, anything left for the user to
    delete, and that the default branch was not pushed.
