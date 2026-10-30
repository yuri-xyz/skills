# Global agent working agreements

These rules apply across all repositories.

## Communication

- Strictly adhere to the Gricean maxims for efficient communication.
- Focus on concise, human-facing details that matter to me. Omit technical details, small unnecessary details, and technical notes unless I explicitly ask for them or the response needs them.

## Code quality

- Write idiomatic, maintainable code that follows the repository's existing conventions.
- Before adding new logic, functions, helpers, classes, or similar code, check
  whether something already defined does the same thing. Prefer reusing,
  extending, or consolidating it, using `/refactor-reuse`,
  `/refactor-consolidate`, or `/refactor-dedupe` where they fit, over adding a
  parallel implementation.
- Do not keep, add, or preserve legacy code, compatibility paths, or deprecated behavior unless the repository explicitly documents that legacy support is intentional.

## Decisions

- Settle technical decisions yourself with `/decide` instead of asking me. Treat this as a standing delegated decision, so adopt its recommendation, scale its research to the decision, and briefly report what you chose and why so I can override it.
- Ask me only about human decisions: direction, scope, product or architecture choices with broad implications, my preferences, and anything that needs my input, approval, accounts, or money. `/decide` defines which decisions are technical and which are human; when unsure, treat the decision as human.

## Dependencies

- **Important:** you MUST use `/dependency-add` when adding any new
  third-party dependency to a project. It vets candidates and decides when my
  explicit approval is needed. Dependencies we own, such as my own packages and
  libraries, are exempt.

## Resource usage

- When running large builds, checks, tests, or other CPU-intensive commands, use `nice -n 10` or another suitable positive niceness value on the top-level command.
- In projects that provide a development environment, such as a dev shell, container, or pinned toolchain, run project tooling such as compilers, package managers, linters, and test runners inside it rather than relying on globally installed versions.
- When you need a tool that is missing from the current environment and does not belong in the project's dependencies, such as a one-off utility for file conversion or other ad hoc operations, run it ephemerally instead of installing it.

## Network request metadata

- When making browser or `curl` fetches, using fetch libraries or tooling, or writing network code, avoid project-, user-, or machine-specific or otherwise identifying `User-Agent` values. Prefer randomized, anonymous user agents that reveal minimal or no metadata over custom or branded values. Use an identifying user agent only when the project specifically requires it, and document that requirement where it is configured.

## Remote code execution

- Never execute code fetched from a remote location unless I have explicitly approved that specific execution. This covers hosted Bash or shell scripts and code in other interpreters such as Python or JavaScript, remote installers, bootstrap commands, and one-liners, for example:
  - piping downloads into an interpreter: `curl ... | sh`, `curl ... | bash`, `wget -O- ... | sh`, `bash <(curl ...)`, `python -c "$(curl ...)"`;
  - loading remote code in place: `source <(curl ...)`, `eval "$(curl ...)"`, or equivalents;
  - scripts hosted on GitHub, GitLab, gists, paste sites, vendor domains, or documentation pages.
- Fetched code may be malicious. A URL, an official-looking source, popularity, or a tool's recommendation is not approval.
- Fetching remote content to read or inspect it is allowed. If you intend to execute a fetched script, save it locally, review it, and ask me first. Use reviewed, local, repository-owned code for normal work rather than remote execution shortcuts.

## Public repositories

- Never commit private notes to a public repository. Public files, docs, comments, and commit messages never mention me or this machine.

## GitHub and remote changes

- Never perform GitHub remote write actions without my explicit approval for that specific action. This includes pushing commits, creating or publishing repositories or projects, changing repository visibility, archiving or unarchiving repositories, modifying repository settings, secrets, or branch protections, opening or modifying pull requests or issues, merging, releasing, publishing packages, leaving comments or reviews, and any other non-read-only `gh` or GitHub operation.
- Read-only inspection of GitHub repositories and metadata is allowed; ask before any operation that changes remote state, even when it appears reversible.

## Git workflow

- Avoid creating Git worktrees; work in the existing checkout unless I explicitly request a worktree.
- Avoid using `git stash` or `git stash pop` unless absolutely necessary. They can lead to corruption, and other agents may be working on the same data; do not stash or pop their work.
- Avoid using `git checkout` unless absolutely necessary. It discards uncommitted work and leads to data loss, including work other agents may have in progress.

## Subagents

- Never use subagents.

## Other agents

- Do not message other agents, not even when creating, finishing, or committing in a worktree. Message another agent only when you need to ask it a question or request something from it; never send announcements, status notices, or heads-ups such as "I am moving into a worktree" or "I am about to commit". A message wakes the other agent, which then re-reads its whole conversation at full price for no benefit.

## Completion report

- When you fully finish longer-running work, such as an agenda plan or task, a goal, a loop, or another multi-step implementation effort, end your final response with a completion report just before you stop. Do not add it when simply answering questions or handling quick, small requests, nor to intermediate progress updates, clarifying questions, or pauses where you are waiting on the user.
- Build the report by invoking `/checks` and `/gaps` and using what they produce. Do not write either part from memory or by imitating a previous report; the skills decide what to include, such as which checks apply and which gaps are already recorded.
- The report has two parts in this order, separated by one blank line:
  1. A `🧪 **Checks**` heading followed by the `/checks` summary. Omit this part when no repository checks apply to the work.
  2. The `/gaps` output, exactly as the skill formats it.
