---
name: careful
description: Use when the user asks the agent to be careful, or when the work at hand touches uncommitted git state, deployments, live services, databases, or other actions whose mistakes could lose work or be hard to undo.
---

# Careful

## Objective

Do the requested work so that if anything goes wrong, it can be put back the way it was. Before each command or tool call that changes state, know what it will change and how to undo it. When it cannot be undone, say so and get the user's permission first.

Reversal is not always possible. The goal is to keep it possible wherever it reasonably can be, and to make the user aware of the cases where it cannot.

## Before Acting

For each step that mutates anything, such as files, git state, a service, a database, infrastructure, or an external account:

1. Inspect the target first: what exists now, what the step will change, and whether other work, other agents, or other people depend on it.
2. Know the undo path, such as a commit to return to, a backup, a down migration, a previous release, or the original value to restore.
3. Prefer the narrowest form of the step: one file, one row, one host, one environment, and a dry run or preview when the tool offers one.
4. If there is no undo path, stop and ask. See [Irreversible Actions](#irreversible-actions).

## Git

Never lose work, including uncommitted changes, untracked files, and work that other agents may have in progress in the same checkout.

- Do not run commands that discard or hide work: `git stash`, `git stash pop`, `git restore`, `git checkout` on files or branches, `git switch`, `git reset`, `git clean`, `git rm` on files you did not create, or `git worktree remove`.
- Do not rewrite history: no rebase, amend, squash, reword, or force-push.
- Check `git status` before changing git state, and stage only the paths your work touched.
- When work must be set aside or isolated, commit it or use `/git-worktree` instead of stashing or switching branches.
- If a destructive git command really is the only way forward, name the command and exactly what it would discard, and ask first.

## Deploying And Live Systems

Deployments, production or shared databases, live services, cloud resources, DNS, and other systems outside the repository affect real users and data.

- Work one step at a time, and verify each step before the next. Do not batch changes to live systems into one command or script.
- Prefer reversible forms: additive migrations before destructive ones, new resources before removing old ones, feature flags or staged rollouts over all-at-once switches, and releases that keep the previous version available for rollback.
- Before changing data, take or confirm a backup or export that can restore it, and check that the restore path actually works when that is cheap to do.
- Scope every query or command tightly. Run the read version first, such as a `SELECT` with the same `WHERE` clause before an `UPDATE` or `DELETE`, and use a transaction when the system supports one.
- Know the rollback for each step before running it, and say what it is.

## Irreversible Actions

Warn the user and get explicit permission before any action that cannot be undone or reversed cheaply, such as:

- Deleting or overwriting data, files, branches, or resources without a copy.
- Destructive migrations, dropped tables or columns, and bulk updates without a backup.
- Publishing, releasing, sending messages, charging money, or anything else outward-facing.
- Revoking or rotating credentials, or changing access, that other systems rely on.

State what the action is, what it will permanently change, and what, if anything, would remain recoverable. Approval covers that action only, not later ones of the same kind.

## Tools And Commands

- Read a command before running it, especially flags such as `--force`, `-f`, `--hard`, `--prune`, `--delete`, `-y`, or recursive options, and globs or variables that could expand wider than intended.
- Prefer targeted edits over sweeping rewrites, scripts, or codemods, whose mistakes are harder to spot and undo.
- Do not delete or overwrite anything you have not looked at.
- If a step fails or does something unexpected, stop. Assess what changed and restore the previous state before trying another approach, rather than piling further changes on top.

## Output

When the work is done, briefly report anything that changed outside the repository, the undo path for it, and any irreversible step that was taken with the user's permission.
