---
name: adapt
description: Use when bringing an external feature, change, design, or component into this project and it must fit the existing architecture rather than replace what exists, sit as a standalone island, or reshape the codebase.
---

# Adapt

The user wants something external brought into this project: a feature from
another codebase, an upstream change, a pasted snippet or module, a design, a
library's way of doing things, or an idea from a conversation. The goal is
settled — this should land. What this skill governs is how it lands.

Adapting means the incoming work is absorbed into the project as if it had been
designed here from the start. The existing architecture is the host; the
incoming work is the guest. It achieves its intended outcome, but expressed
through this project's structure, abstractions, conventions, and vocabulary.

## What Adapting Is Not

Avoid these three failure modes:

- **Replacing.** Swapping out an existing system, module, or pattern for the
  incoming one because the incoming version is what's in front of you. If the
  project already has a mechanism for something the incoming work also does,
  the project's mechanism wins.
- **Islanding.** Dropping the incoming work in as a self-contained,
  parallel implementation with its own helpers, config style, naming, types,
  error handling, or directory layout that sits beside the existing system
  without connecting to it.
- **Being overridden.** Letting the incoming work's assumptions, structure, or
  style leak outward until the surrounding code bends to match it — renaming,
  restructuring, or re-patterning existing code so the newcomer fits as-is.

## Closed-source sources

If the incoming work comes from a closed-source or proprietary source, or
using it would mean reverse engineering or extracting from a binary,
installer, package, firmware, or website, or reproducing distinctive
copyrighted creative work, stop and ask: name the situation and wait for the
user's decision before reading or bringing in more of it. Open-source sources
under a license compatible with the project need only attribution, recorded
the way the project records it.

## Workflow

1. **Extract the intent.** State what the incoming work is actually for: the
   behavior, capability, or outcome the user wants. Separate that goal from the
   incoming implementation's specific shape, which is only one way to reach it.

2. **Map the existing system.** Before designing anything, inspect the parts of
   this project the goal touches: the modules that own related behavior, the
   helpers and abstractions already available, the configuration and option
   models, naming conventions, error handling, tests, and documentation
   patterns. Use `/explore` or `/refactor-reuse` search technique as needed.

3. **Decompose the incoming work.** Break it into its parts and classify each:
   - **Already covered:** the project already does this. Use the existing
     mechanism and drop the incoming version of it.
   - **Extends something existing:** the project has a near-match. Extend that
     owner — add an option, case, parameter, or entry — rather than adding a
     sibling.
   - **Genuinely new:** nothing here does this. Add it, but placed where this
     project would put it, structured the way this project structures similar
     things, and wired into the existing systems that should know about it.
   - **Not needed:** scaffolding, compatibility shims, or concerns specific to
     the incoming work's original environment. Leave it out.

4. **Translate, don't transplant.** Re-express every kept part in local terms:
   this project's names, file layout, module boundaries, types, config style,
   and idioms. New pieces should be indistinguishable in style from their
   neighbors and should reuse shared facts, helpers, and registries rather than
   restating them.

5. **Integrate at the seams.** Connect new pieces to the systems that already
   coordinate similar things: registries, option trees, routing, dependency
   wiring, check suites, docs, and specs. A new piece that the rest of the
   system does not know about is an island, even if its internal style matches.

6. **Validate the fit.** Run the project's relevant checks. Then review the
   result as a whole: existing behavior is preserved, nothing parallel was
   introduced, and a reader could not easily tell which parts came from
   outside.

## When the Incoming Work Is Better

Sometimes the incoming approach is genuinely better than what exists. Do not
silently replace the existing system, and do not silently ignore the
improvement either. Adapt the incoming work to the current architecture as
asked, then surface the difference to the user as a separate, explicit
proposal: what is better, what replacing or upgrading the existing system would
involve, and what it would affect. Leave that decision to the user.

Likewise, if the incoming work cannot reach its goal without changing an
existing contract or architecture boundary, stop and explain the conflict
instead of forcing it through.

## Boundaries

- Do not remove or rewrite existing systems as a side effect of adapting.
- Do not add a parallel helper, abstraction, config format, or dependency when
  an existing one covers the need.
- Do not carry over the incoming work's names, comments, directory structure,
  or conventions when they differ from this project's.
- Do not over-engineer the adaptation layer. If integration needs a large
  wrapper or translation shim, the integration point is probably wrong; find
  the existing owner instead.
- Do not drop parts of the intended outcome just because they are awkward to
  fit. Find the right home for them, or raise the conflict.
- When the external source is a third-party reference whose code or identity
  must not be copied, also apply `/reference`.

## Output

Summarize the adaptation briefly:

- The intended outcome that was brought in.
- What was satisfied by reusing existing code, naming the reused pieces.
- What existing code was extended, and how.
- What was added new, and where it plugs into the existing system.
- What was intentionally left out, and why.
- Any proposed follow-ups where the incoming approach suggested a real
  improvement to the existing architecture.

## Related Skills

- `/refactor-reuse`: owns the search technique and match rules for deciding
  whether existing code already covers a need.
- `/reference`: use alongside this skill when the source is a reference that
  must be learned from without copying code, branding, or provenance.
- `/harvest`: use instead when the task is to discover and propose
  improvements from another repository rather than bring in a known one.
- `/suggestion`: use when the incoming idea itself is optional and may be
  rejected; adapt assumes it should land.
