---
name: root-cause
description: Use when a bug or problem needs its root cause found and fixed where it originates, including in upstream code we own, or when the current direction or a fix might be a hack, workaround, or patch layered over broken behavior instead.
---

# Root Cause

## Objective

The current issue gets fixed at its origin. Investigate until the root cause is confirmed, then change the code that owns the defect. Where the defect lives in a library, package, or dependency we control, fix it there and update this project's pin to that fix.

When the question is only whether the current direction or a recent change is a proper fix, run the checkpoint in [Check The Current Direction](#check-the-current-direction) and continue from its verdict.

## What A Root Cause Is

The root cause is the origin of the bug, meaning the first place where correct inputs become incorrect behavior or state. A root-cause fix does one of two things:

- Corrects the defect directly at that location.
- Removes the whole class of bug at its source, such as a wrong model, an unsafe API, a missing invariant, or a generator that emits bad output, so sibling instances cannot recur.

Prefer fixing the class when the same mistake can plainly happen again through the same path. Fix the single instance when it really is a one-off.

## Workaround Signatures

A fix that stacks behavior on top of the defect is not a root-cause fix. This skill owns that definition; other skills refer to it rather than restating the list.

A layered fix makes a symptom disappear by stacking new behavior on top of existing behavior. It often looks like an override, wrapper, hook, activation script, compatibility shim, special case, duplicated branch, retry, fallback, cleanup pass, or post-processing step whose real purpose is to correct something earlier code produced incorrectly. A change shows a workaround signature when it:

- Adds logic whose main job is to fix output from other logic.
- Adds an override because the original source of truth is inconvenient to change.
- Duplicates behavior instead of moving the existing behavior to the right owner.
- Adds a script, hook, migration, cleanup, postprocessor, or fallback to mask a defect.
- Adds a special case that could be removed by simplifying the model or API.
- Preserves broken intermediate state and repairs it later.
- Hides an error instead of fixing why it happens.
- Depends on timing, ordering, global state, or manual operator discipline.
- Makes one observed case pass while the general failure mode survives.
- Adds temporary code with no removal path.
- Makes future readers understand two paths when one corrected path would do.

### Allowed Exceptions

An explicit layer is fine when it is the real domain boundary, such as:

- Adapters between external APIs and internal models.
- Compatibility support for an intentionally supported old interface.
- Security checks that must defend in depth.
- Feature flags or migrations with a planned removal path.

When keeping a layer, explain why it is a real boundary instead of a workaround.

## Check The Current Direction

Use this as a short checkpoint mid-implementation or as a quality gate after making or reviewing changes. It is not a full architecture review; keep it brief unless it exposes a real problem, and escalate to `/approach` when the answer needs real alternatives compared or the architecture judged.

1. Pause the current work and inspect the plan, recent edits, and relevant code as needed.
2. Check them against the workaround signatures above.
3. If the direction is a proper fix, say so in one or two sentences and continue the original work without derailing.
4. If it is layered, hacky, or uncertain, stop before adding more code. Name the layer and the underlying behavior it compensates for, and identify the owner of that behavior.
5. Replace the layered approach with a root-cause change at the ownership boundary, following the rest of this skill. Prefer deleting workaround code, simplifying control flow, or correcting data or model generation over adding another condition. If the user asked only for the check, ask for explicit confirmation before continuing with either path.

Report the verdict in one of these forms:

```markdown
Proper: <brief reason>. Continuing.
```

or:

```markdown
Layered: <the layer and what it compensates for>.

Better path: <root-cause direction at the owning code>.
```

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

- Any of the workaround signatures above outside the allowed exceptions.
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
