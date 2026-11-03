---
name: reference
description: Use when the user provides a reference, such as another project, app, or design, to draw ideas from.
---

# Reference

Use the provided reference as learning material for the current task. The target project remains the source of truth.

## Workflow

1. Identify the reference artifact and the target deliverable.
   - Accept local paths, repositories, source snippets, URLs, screenshots, documents, or described examples.
   - If the reference cannot be accessed and the task depends on it, ask for the missing artifact or credentials.

2. Keep downloaded references local and untracked.
   - If a reference repository, archive, website export, document bundle, or other resource must be cloned or downloaded, place it inside the target project under a gitignored scratch path such as `.refs/`.
   - Ensure the scratch path is ignored before downloading or cloning into it.
   - Do not stage, commit, or reference the downloaded path, repository name, URL, provenance, or other linking details in project code, comments, docs, tests, commit messages, or generated artifacts.
   - Use the local copy only as temporary working material for inspection.

3. Inspect only what is relevant.
   - Read enough of the reference to understand patterns, constraints, interaction design, architecture, algorithms, naming conventions, data flow, tests, or edge cases that matter to the task.
   - Prefer targeted search and representative files over broad copying or exhaustive ingestion.
   - Treat reference runtime commands as read-only unless the user explicitly asks to run or modify that project.

4. Evaluate before adopting.
   - Check whether each observed idea fits the target project's architecture, style, dependencies, licensing constraints, security posture, and user request.
   - Do not assume the reference is correct, current, maintainable, idiomatic, complete, or better than the target codebase.
   - When the reference conflicts with local conventions or requirements, prefer the target project.

5. Adapt concepts, not artifacts.
   - Recreate behavior in the target project's style using its existing helpers, abstractions, and tests.
   - Translate ideas into fresh implementation details suited to the target codebase.
   - Use established APIs, protocols, formulas, or short idiomatic snippets only when they are generic and necessary.

6. Preserve provenance silence in public artifacts.
   - Do not add comments, docstrings, documentation, commit messages, generated UI text, filenames, symbols, or variable names that identify or link to the reference.
   - Do not say "based on", "inspired by", "copied from", or equivalent provenance notes in project artifacts.
   - In user-facing summaries, describe the implemented result and validation, not the reference's identity, unless the user explicitly asks for comparison or attribution.
   - Silence covers public project artifacts only. If the project keeps private provenance records, record the reference there. Attribution that the reference's license requires goes in the project's public licensing record, which is not a provenance leak.

## Closed-source references

If the reference is closed-source or proprietary, or using it would mean
reverse engineering or extracting from a binary, installer, package, firmware,
or website, or reproducing distinctive copyrighted creative work, stop and
ask: name the situation and wait for the user's decision before reading
further. Open-source references under a license compatible with the project
need only attribution, recorded the way the project records it.

## Hard Boundaries

- Do not copy whole files, asset sets, large exact code chunks, distinctive text, branding, private data, secrets, or license headers from the reference.
- Do not vendor the reference or add it as a dependency unless the user explicitly requests that and the target project policy allows it.
- Do not preserve reference-specific names, URLs, comments, IDs, examples, mock data, or visual branding unless they are part of a public standard the target project already uses.
- Do not let local reference scratch directories appear in `git status`, staged diffs, committed paths, or committed text.
- Do not weaken local quality standards just because the reference takes a shortcut.

## Good Use Of References

- Learn the shape of a feature, workflow, state machine, API integration, UI interaction, test case, or edge-case handling.
- Compare tradeoffs, then choose the approach that best fits the target project.
- Use the reference to discover questions and risks, not to outsource judgment.
- Keep final changes independently understandable without requiring readers to know the reference exists.
