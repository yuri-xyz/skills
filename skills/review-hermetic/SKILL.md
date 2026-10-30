---
name: review-hermetic
description: Use when code, generators, Nix outputs, or tests might produce different results across runs or machines.
---

# Review Hermetic

## When To Use This

Use this after writing or when reviewing:

- Code whose job is to *produce* output that other things depend on being stable: a derivation, a generated/tracked file, a Home Manager link target, JSON/config emitted by a script, or anything feeding a Nix store path or `nix eval`. This repo's design principles are explicit that this output must not vary between builds, machines, or runs (`CLAUDE.md` principle #6).
- Ordinary code, scripts, or tests that could behave correctly on this machine/run but fail unpredictably on another machine, in CI, at a different time, or under a different locale/timezone/run order — even when there's no generated artifact involved.

This skill is the checklist for actually verifying non-flakiness, not just assuming it.

Not every script needs this. Skip it for one-off interactive commands, local dev tooling, or anything whose behavior is never compared across runs, machines, or environments.

## Traps To Scan For

For each, search the code under audit and flag any hit:

- **Timestamps**: `date` command output embedded in generated content, `builtins.currentTime`, build/commit timestamps baked into files, `SystemTime::now()` / `Instant::now()` written to output, cache-busting suffixes derived from wall-clock time.
- **Random IDs**: `$RANDOM`, `uuidgen`, `openssl rand`, unseeded RNG calls, or `mktemp`-style names that leak into the *output content* itself (as opposed to purely transient scratch file paths that never appear in the result).
- **Host-specific paths**: absolute paths under `$HOME`, `/home/<user>`, `pwd`-derived paths, hostnames, or other machine-specific strings embedded in generated content instead of repo-relative or store paths.
- **Unstable iteration**: language collections without guaranteed order feeding into generated output — Rust `HashMap`/`HashSet` (use `BTreeMap`/`BTreeSet` or explicit sort), unsorted directory listings (`readdir`/`ls` without a sort step) in shell/Rust/Python, unsorted glob results. Nix attrsets are already lexicographically ordered by key, so plain `builtins.attrNames`/`lib.mapAttrsToList` over a Nix attrset is not a risk by itself — the risk is elsewhere (external command output, non-Nix collections) feeding into Nix-generated content.
- **Formatting churn**: locale-dependent sorting or number formatting, non-pinned formatter/tool versions that can change output byte-for-byte between runs, trailing-whitespace or line-ending inconsistency introduced by a generator.
- **Impure/unpinned fetches**: `fetchurl` without a hash, `fetchGit`/`fetchFromGitHub` without a pinned `rev`, or any network call made at eval/build time whose result isn't pinned — these make the *build*, not just formatting, nondeterministic.
- **Environment leakage**: `builtins.getEnv`, reading `$USER`/`$HOSTNAME`/shell env vars into content that's supposed to be reproducible across machines or sessions.
- **Timezone/locale assumptions**: parsing or formatting dates/times/numbers without pinning a timezone or locale (`date` without `-u`/`TZ=UTC`, locale-dependent string sorting or number parsing, assuming a 24h clock or a specific decimal separator).
- **Timing- and order-dependent logic**: `sleep`-based waits standing in for real synchronization, races between concurrent writers/readers without locking, retry logic masking a race instead of fixing it, floating-point equality comparisons instead of tolerance-based checks.
- **Fixed external resources**: hardcoded ports, hardcoded temp/socket paths that can collide across parallel runs, or assumptions that a specific network host/service is reachable without mocking or skipping when unavailable.
- **Test-order and shared-state dependence**: tests that only pass in a specific execution order, rely on state left behind by another test, share mutable global/module state across test cases, or depend on filesystem case-sensitivity/path-separator behavior that differs across systems.

## Workflow

1. Identify what's under audit and what "stable" means for it: a derivation's build output, a generated tracked file, a rendered config/emitted JSON (consumed via a store path, `nix eval` check, committed file, or Home Manager link) — or a script/function/test whose *behavior* must hold across machines, timezones, locales, and run order rather than producing a specific artifact.
2. Read the code end-to-end and check it against each trap above. Use targeted greps as a starting point: `date `, `currentTime`, `getEnv`, `RANDOM`, `uuid`, `HashMap`, `HashSet`, hostname/`$HOME`/`os.environ`, unsorted `readdir`/`ls`/glob calls, `sleep`, hardcoded ports, `TZ`/locale calls.
3. For anything flagged, trace whether it actually matters in practice: a `mktemp` used only for a scratch working directory that's deleted before the real output is written is fine; one whose name ends up *in* generated output is not. A `sleep` used as a deliberate rate limit is fine; one used to paper over a missing wait-for-ready check is not.
4. Where practical, verify empirically rather than by inspection alone:
   - For a Nix derivation: build it twice (`nix-build` / `nix build`) and diff the resulting store paths or content; a content-identical, path-identical result across runs is a strong signal.
   - For a generated tracked file: run the generator twice into separate temp locations and diff the results.
   - For `nix eval` checks already defined in this repo (e.g. `.#checks.x86_64-linux.config-state`), re-run and confirm output is byte-identical across invocations.
   - For ordinary code or tests: run the relevant test(s) repeatedly and, where feasible, under a different `TZ`/`LC_ALL` (e.g. `TZ=UTC`, `TZ=Pacific/Kiritimati`, `LC_ALL=C`) and in a different order (test-runner shuffle/seed flag if available) to surface hidden assumptions.
5. Fix findings using the lightest correct approach: drop the timestamp/ID entirely if it isn't load-bearing, replace it with content-derived versioning (e.g. a hash of the actual inputs) if some form of identity is genuinely needed, sort collections explicitly before use, switch ordered-map types, pin fetches with an explicit hash/rev, remove environment/host-path leakage in favor of repo-relative or store-relative references, replace `sleep`-based waits with real readiness checks, and remove shared mutable state or ordering assumptions between tests.
6. Re-run the empirical check from step 4 after fixing to confirm the nondeterminism is actually gone, not just superficially patched.

## Output

Report, ordered by what's most likely to actually break reproducibility or cause a flake on another system:

- Trap found: file/line, which category (timestamp, random ID, host path, unstable iteration, formatting, unpinned fetch, env leakage, timezone/locale, timing/race, fixed resource, test-order/shared-state), and whether it actually reaches the output or affects behavior.
- Fix applied or recommended.
- Verification performed (double-build diff, re-run diff, check re-eval, or repeated/shuffled/TZ-varied test run) and its result.
- Anything flagged but intentionally left as-is, with a one-line reason (e.g. a timestamp that is genuinely required and already called out in an existing comment).
