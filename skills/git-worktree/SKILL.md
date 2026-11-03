---
name: git-worktree
description: Use when the user asks to work in a worktree or to isolate the agent's work from other agents in the same checkout.
---

# Git Worktree

Give this agent its own worktree so it can continue its existing work, or start
the upcoming work, without stepping on anyone else. The main checkout and every
other worktree belong to other agents and the user; leave their files,
branches, and pending changes exactly as they are.

Invoking this skill is the explicit request to create a worktree that general
"avoid creating worktrees" guidance asks for.

## Architecture

- The **main checkout** (the first entry of `git worktree list`) stays on the
  **default branch**, the branch checked out there. One agent may work in it
  directly.
- Every other agent works in its own **feature worktree** branched from the
  default branch. Each worktree has its own branch, index, and files, so agents
  cannot overwrite each other.
- A feature worktree does not follow the default branch on its own. To pick up
  newer default-branch commits, run `git merge <default-branch>` inside the
  feature worktree.
- Work lands back on the default branch with `/git-worktree-finish`, which
  also removes the worktree once nothing can be lost.

## Core Constraints

**Never disturb other work.** In the main checkout and in every other worktree,
do not run `git stash`, `git checkout`, `git switch`, `git reset`,
`git restore`, `git clean`, or `git worktree remove`. The only mutation allowed
outside the new worktree is the commit in step 4.

**Never rewrite history.** Integrate with regular `git merge` only. Do not
rebase, amend, squash, reword, force-push, or otherwise replace existing
commits.

**Keep worktrees findable.** Always place the worktree at
`<repo-parent>/<repo-name>.worktrees/<name>`, for example
`../myapp.worktrees/feat-add-export` next to a checkout named `myapp`. Never
create worktrees in a temporary directory, under the repository itself, in
hidden or cache directories, or anywhere else `git worktree list` users would
not look.

**Stay local.** Do not push, publish, or touch remotes.

## Workflow

1. **Inspect.** Find the main checkout and default branch with
   `git worktree list`, then run `git status --short` and
   `git branch --list 'feature/*'` to see pending changes, existing
   worktrees, and existing feature branches.
2. **Reuse when possible.** If this agent is already working inside a
   dedicated feature worktree, keep using it and stop here.
3. **Name the work.** Name the worktree after the work it starts with, led by
   the kind of work, for example:
   - `feat-add-export` for a feature
   - `fix-package-hash` for a bug fix
   - `plan-36-align-keychain` for an agenda plan, with its number
   - `task-31-nix-daemon` for an agenda task, with its number
   - `refactor-...`, `docs-...`, or `chore-...` for other Conventional Commit
     types

   Use kebab-case (lowercase letters, digits, single dashes, at most 64
   characters, no `feature/` prefix). The name only needs to fit the work at
   creation time; later work in the same worktree does not require renaming
   or a new worktree. If the name already exists as a branch or worktree,
   choose a more specific one rather than reusing someone else's.
4. **Settle pending changes.** If the main checkout has any pending changes,
   commit all of them there with `/git-commit`, but skip its Spec Sync Gate
   and run no checks, tests, or builds. This leaves the main checkout clean
   and lets the new worktree start from the latest changes. If a commit is
   already in progress (for example `.git/index.lock` exists), wait for it to
   finish instead of deleting the lock. Skip this step when the checkout is
   clean.
5. **Create the worktree** from the default branch:

   ```bash
   main=<main-checkout>
   git -C "$main" worktree add -b "feature/<name>" \
     "$(dirname "$main")/$(basename "$main").worktrees/<name>" HEAD
   ```

6. **Move in.** Run every later command and edit from the new worktree path,
   using absolute paths under it. Untracked and ignored files such as
   `.direnv/`, `target/`, `node_modules/`, and local `.env` files are not
   copied: re-enter the dev shell in the new path and rebuild caches there. Do
   not copy secrets or local-only files across without asking.
7. **Report** the worktree path, the branch, and the commit made in the main
   checkout if any.

## Afterwards

Keep working in the worktree until the user asks to finish it. A `/goal`
whose condition runs `/git-worktree` counts as that request: once the goal is
met, finish with `/git-worktree-finish` without stopping to ask for a commit
or a landing. Landing and removal always go through `/git-worktree-finish`.
