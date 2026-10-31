---
name: dependency-tree-compress
description: Use when the user asks to shrink, audit, or de-risk a project's dependency tree by finding small, low-trust third-party dependencies that could be replaced with our own code. For deciding about one specific piece of local code versus a package use /dependency-judge, and for adding a new dependency use /dependency-add.
---

# Dependency Tree Compress

## Objective

Find the third-party dependencies, crates first, that are small enough to own and not trustworthy enough to keep, and rank them as candidates for replacement with our own implementation. Each removal shrinks the supply-chain surface and the build.

This skill scans and recommends. Replace a dependency only after the user picks it from the report.

## Size Bar

A candidate is small when its own source is about 6,000 lines of code or fewer. Count only the library's non-test source: for Rust, `src/` and `build.rs`, excluding comments, blank lines, `tests/`, `benches/`, and `examples/`. Treat the bar as a guide, not a cutoff: a 6,500-line crate we use one function of is a better candidate than a 2,000-line crate we use all of.

Also weigh what we actually use. The replacement only needs the surface our code calls, so record the used items next to the line count.

## Trust Signals

A small dependency is a candidate when one or more of these hold. More signals rank it higher.

- **Low stars.** Under 300 GitHub stars is a strong signal, under 500 a moderate one, and under 1,000 a weak one.
- **Abandoned.** The repository is archived, has no commits in the last 12 months, has open security or soundness issues without maintainer responses, or carries a RustSec `unmaintained` advisory.
- **Outdated.** We pin a version well behind the latest release, or the crate depends on outdated major versions of its own dependencies.
- **Unknown author.** A single maintainer with no recognizable track record: no organization, few other maintained projects, little review history, or a recently created account.
- **Weak release hygiene.** No source repository, a repository that does not match the published crate, or yanked releases without explanation.

## Exclusions

Skip these even when they are small or show trust signals, since owning them would add more risk than it removes:

- Cryptography, hashing, randomness, constant-time comparison, TLS, certificates, authentication, and password handling.
- Security-critical code, such as sandboxing, privilege handling, input sanitizing, or escaping.
- Code with heavy `unsafe`, FFI, platform syscalls, or atomics and lock-free concurrency, where subtle bugs are memory-safety bugs.
- Implementations of broad standards, formats, or protocols where correctness depends on many edge cases, as `/dependency-judge` describes.
- Mature, trusted crates: those maintained by the Rust project or a well-known organization such as `rust-lang`, `tokio-rs`, `serde-rs`, `RustCrypto`, or `rustls`, or widely depended-upon crates with active maintenance.
- Dependencies we own, such as the user's own crates, packages, and flake inputs.

When an excluded dependency, such as an obscure crypto crate, shows strong trust signals, do not propose our own implementation. Report it separately as a candidate to swap for a trusted alternative through `/dependency-add`, or for `/cryptography`'s library gate when it is cryptographic.

## Process

1. **List the tree.** Get direct and transitive dependencies with their versions and source paths:

   ```sh
   cargo tree --edges normal,build --prefix none --no-dedupe | sort -u
   cargo metadata --format-version 1 | jq -r '.packages[] | [.name, .version, .repository // "", .manifest_path] | @tsv'
   ```

   For other ecosystems use the equivalent, such as `npm ls --all` or `go mod graph`.

2. **Measure size.** Count lines for each package from its source directory, the parent of its `manifest_path`, with `tokei` or `scc`. Run them through a temporary tool install if they are missing. Drop everything clearly over the size bar.
3. **Apply exclusions.** Drop the excluded categories above, noting excluded crates that show trust signals for the separate list.
4. **Check trust signals.** For each remaining package, gather current data rather than memory:

   ```sh
   gh repo view OWNER/REPO --json nameWithOwner,stargazerCount,pushedAt,isArchived,owner
   gh api users/OWNER --jq '[.login, .type, .created_at, .public_repos, .followers] | @tsv'
   cargo info PACKAGE
   ```

   Run `cargo audit` or `cargo deny check advisories` for unmaintained and unsound advisories, and compare the pinned version with the latest release.

5. **Check removability.** A transitive dependency only leaves the tree when every parent drops it. Find who pulls it in with `cargo tree -i PACKAGE`. For transitive candidates, note whether a parent feature flag, a parent upgrade, or replacing the parent would remove it; otherwise mark it not removable by us.
6. **Size the replacement.** Find our call sites and the items we use. Estimate the lines our own implementation would need, and whether existing project code already covers part of it.
7. **Rank.** Order candidates by removability, trust signals, and the smallest replacement, and stop at a useful shortlist rather than listing the whole tree.

## Replacing A Candidate

When the user picks a candidate:

- Write the replacement idiomatically in the owning crate or module, covering only the used surface, with tests ported or written for the behavior we rely on.
- Check the candidate's license before reading its source closely. When it is open source, attribute any adapted code under its license; otherwise implement from its documented behavior.
- Remove the dependency from the manifest and update the lockfile with the package manager, then confirm with `cargo tree -i PACKAGE` that it left the tree.
- Run the project's focused checks and tests.

## Output

Lead with the shortlist, ranked, as a table with these columns:

- Package and version, and whether it is direct or transitive.
- Lines of code, and the used surface.
- Stars, last commit, and maintainer.
- Trust signals that apply.
- Removability, and what removing it would take.
- Estimated replacement size.

Then list excluded dependencies that showed trust signals, with the trusted alternative to consider, and briefly state how many packages were scanned and dropped by size, exclusions, and trust.
