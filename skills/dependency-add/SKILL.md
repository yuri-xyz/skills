---
name: dependency-add
description: Use whenever adding a new third-party dependency to any project, or when choosing between candidate libraries, packages, or tools to depend on.
---

# Dependency Add

## Objective

Every new third-party dependency is vetted before it is added or installed. A candidate that meets the trust bar is added without asking. Anything else waits for the user's explicit approval, and a candidate with known malware stops all work.

Dependencies we own, such as the user's own packages, libraries, and flake inputs, are out of scope. Add those normally.

Do not add a dependency merely for convenience.

## Process

1. **Find candidates.** List the best candidates from knowledge, or find them with `/research-web`.
2. **Filter with `/dependency-judge`.** Drop candidates that lose to keeping the code local, or that fail its maintenance, license, and transitive-risk checks.
3. **Check security.** Start with the advisory queries in Fast Checks With gh, then use `/research-web`. For each remaining candidate, at the exact version you plan to use, search for actively exploited vulnerabilities, major CVEs, supply-chain compromises, and malware or infostealers reported or trending in the last full month. Check the package itself and any compromise of its registry account or maintainers.
4. **Apply the trust bar.** A candidate meets it when its upstream repository has more than 1,000 GitHub stars, verified with `gh repo view`, and step 3 found no major CVE and no reported malware, infostealer, or supply-chain compromise for that version.
5. **Pick the best candidates** that meet the trust bar. Add them following the project's package manager workflow and pinning policy.

## Fast Checks With gh

The GitHub CLI answers the star and advisory questions faster than a web search. Use it first, then use `/research-web` for compromises too recent or too broad for the advisory database, such as a registry or maintainer takeover still being reported.

Stars, activity, and archive status:

```sh
gh repo view OWNER/REPO --json nameWithOwner,stargazerCount,pushedAt,isArchived
```

Advisories for the exact planned version, from the GitHub Advisory Database. `ECOSYSTEM` is one of `npm`, `pip`, `rust`, `go`, `maven`, `nuget`, `rubygems`, `composer`, `pub`, `swift`, `erlang`, or `actions`:

```sh
gh api -X GET /advisories -f ecosystem=ECOSYSTEM -f affects=PACKAGE@VERSION \
  --jq '.[] | [.ghsa_id, .cve_id, .severity, .published_at, .summary] | @tsv'
```

Malware is excluded from that query by default, so always run it a second time with `-f type=malware`, without a version to catch any malicious release of the package:

```sh
gh api -X GET /advisories -f ecosystem=ECOSYSTEM -f affects=PACKAGE -f type=malware \
  --jq '.[] | [.ghsa_id, .published_at, .summary] | @tsv'
```

Advisories the project published itself:

```sh
gh api repos/OWNER/REPO/security-advisories --jq '.[] | [.ghsa_id, .cve_id, .severity, .state, .summary] | @tsv'
```

An empty result is not proof of safety: the database covers these ecosystems only, and new reports land with a delay.

Prefer a stable version published at least three weeks ago over a fresh release to reduce supply-chain attack risk, unless the work needs a feature or fix from a newer version.

## Approval

- Add a candidate that meets the trust bar without asking.
- Ask for explicit approval for every candidate that does not, including any whose stars or security status cannot be verified. Say which part of the bar it misses.
- Group all candidates that need approval into one question, or a few, instead of asking one by one.
- Skip the approval request for dependencies that are already a settled decision, such as those named in an approved plan. Still run step 3 on them, since a compromise may have been reported since the decision.

## Stop On Malware

🛑 If a dependency that is about to be added, or already was added, fetched, or installed, has known malware, an infostealer, or a supply-chain compromise:

1. Stop immediately and do not continue the task under any circumstances.
2. Do not install, build, run, or import anything that could load it.
3. Check, read-only, whether it was already fetched, installed, or executed, and where: manifests, lockfiles, package caches, the Nix store, virtual environments, and shell history.
4. Tell the user under a 🛑 heading what was found, which parts are affected, and the report that identified it. Leave cleanup to the user.

## Output

For each dependency considered, report briefly:

- The candidate and version, and whether it was added, needs approval, or was rejected.
- Its GitHub stars and the security check result, with sources for anything found.
- For candidates that need approval, which part of the trust bar they miss.
