---
name: layering
description: Use when a fix or change might be a patch or wrapper layered over broken behavior instead of fixing it where it originates.
---

# Judge Layering

Use this skill as a quality gate after making or reviewing changes.

## Goal

Keep fixes flat: change the code that owns the behavior instead of adding another layer that compensates for it.

A layered fix is code that makes a symptom disappear by stacking new behavior on top of existing behavior. It often looks like an override, wrapper, hook, activation script, compatibility shim, special case, duplicated branch, retry, fallback, cleanup pass, or post-processing step whose real purpose is to correct something earlier code produced incorrectly. Other signatures: it hides an error instead of fixing why it happens, depends on timing, ordering, global state, or manual operator discipline, makes one observed case pass while the general failure mode survives, or adds temporary code with no removal path.

This skill owns that definition. `/hacky` and `/approach` refer to it rather than restating the list.

## Review Checklist

Before finishing recent work, check whether the change:

- Adds logic whose main job is to fix output from other logic.
- Adds an override because the original source of truth is inconvenient to change.
- Duplicates behavior instead of moving the existing behavior to the right owner.
- Adds a script, hook, migration, cleanup, postprocessor, or fallback to mask a defect.
- Adds a special case that could be removed by simplifying the model or API.
- Preserves broken intermediate state and repairs it later.
- Makes future readers understand two paths when one corrected path would do.

If any item is true, pause and identify the owner of the incorrect behavior.

## Preferred Response

1. State whether the current approach is flat or layered.
2. If layered, name the layer and the underlying behavior it is compensating for.
3. Replace the layered approach with a root-cause change at the ownership boundary.
4. Prefer deleting workaround code, simplifying control flow, or correcting data/model generation over adding another condition.
5. Validate the behavior at the level where the root cause lives.

## Allowed Exceptions

Use an explicit layer only when it is the real domain boundary, such as:

- Adapters between external APIs and internal models.
- Compatibility support for an intentionally supported old interface.
- Security checks that must defend in depth.
- Feature flags or migrations with a planned removal path.

When keeping a layer, explain why it is a real boundary instead of a workaround.
