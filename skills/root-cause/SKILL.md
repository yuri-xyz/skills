---
name: root-cause
description: Use when a bug or problem needs its root cause found and fixed where it originates, including in upstream code we own, rather than worked around.
---

# Root Cause

## Objective

The current issue gets fixed at its origin. Investigate until the root cause is confirmed, then change the code that owns the defect. Where the defect lives in a library, package, or dependency we control, fix it there and update this project's pin to that fix.

## What A Root Cause Is

The root cause is the origin of the bug, meaning the first place where correct inputs become incorrect behavior or state. A root-cause fix does one of two things:

- Corrects the defect directly at that location.
- Removes the whole class of bug at its source, such as a wrong model, an unsafe API, a missing invariant, or a generator that emits bad output, so sibling instances cannot recur.

Prefer fixing the class when the same mistake can plainly happen again through the same path. Fix the single instance when it really is a one-off.

A fix that stacks behavior on top of the defect is not a root-cause fix. `/layering` defines those signatures, and none of them are allowed here.

## Investigate

1. Restate the symptom concretely: what happens, what should happen, and where it shows up.
2. Trace backward from the symptom to the first point where state or behavior goes wrong. Read the owning code; do not stop at the layer where the symptom surfaced.
3. Form a specific hypothesis that names the file, function, option, or input responsible.
4. Confirm it with evidence before changing anything: a reproduction, a focused test, an evaluated value, a log line, or code reading that leaves no gap. Use `/debug` for targeted instrumentation.
5. Check whether the same cause produces other instances, and whether the cause is itself a symptom of something earlier. Keep going until you reach the actual origin.

Do not write a fix while the cause is still a guess. If the evidence cannot settle it, say what is known, what is ruled out, and what probe or input would decide it.

## Decide Who Owns It

Locate the owner of the defective behavior, not the place where it hurts.

- **Local**: the defect is in this repository's code, configuration, or data, including this project misusing or misconfiguring a dependency.
- **Upstream, ours**: the defect is in a library, package, flake input, submodule, or other dependency whose source we control, for example a repository owned by the user or the user's organization, or a local checkout of one. Confirm ownership from the remote, the manifest, or the user; do not assume it.
- **Upstream, third-party**: the defect is in code we do not control.

## Fix It Locally

1. Apply the fix at the owning location identified above.
2. Remove any workaround code that existed only to compensate for this defect.
3. Validate at the level where the root cause lives, and confirm that the original symptom is gone.

## Fix It Upstream When We Own It

Treating other repositories as read-only does not apply to upstream code we own: this skill authorizes fixing it properly there.

1. Work in the upstream project's own checkout, following its conventions, checks, and agent instructions.
2. Fix the root cause there, add or update a test that covers it, and validate the fix in that project.
3. Commit it there. Pushing, tagging, releasing, or opening a pull request remains a remote write and needs explicit approval for that specific action.
4. Once the fix is reachable from a ref this project can consume, update the pin or ref and its lock entry together, following this project's pinning policy, for example a release tag over a bare commit.
5. Remove any local workaround the upstream fix makes unnecessary, and validate the result here.

If the fix cannot be published yet, stop before changing the pin. Report the upstream commit and the exact pin change that is waiting on it. Do not point the pin at unpublished local work, and do not add a local stand-in fix.

## Upstream Bugs We Do Not Own

Do not patch around the defect locally. Report the confirmed root cause, the upstream location, and the change it needs, then ask how to proceed, for example with an upstream report, a fork we own, or a version that already contains the fix.

## Not Allowed

- Workarounds, wrappers, overrides, retries, fallbacks, special cases, or post-processing that hide the defect.
- Temporary fixes, including `/temp` changes and trials standing in for the real fix.
- Hacky patches, such as vendored patch files, monkey-patching, or editing generated output or store paths, instead of fixing the source.
- Fixing only the reported instance when the same cause visibly produces others.

If the only option left is one of these, stop and explain why the root-cause fix is blocked instead of shipping the workaround.

## Output

Report briefly:

- The root cause, with its location and the evidence that confirmed it.
- Who owns it: local, upstream ours, or upstream third-party.
- The fix, and whether it covers the single instance or the whole class.
- For upstream fixes: the upstream commit, its push or release status, and the pin and lock update made or still pending.
- Validation run and its result.
