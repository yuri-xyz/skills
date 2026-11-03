# Spec — Quality Checklist

Before finishing work on a spec governed by the
[spec standard](../SKILL.md), confirm each item.

- [ ] `OVERVIEW.md` has the required header, sections, and complete
      `Spec Map`.
- [ ] Every file is at or under 700 lines; features are only in `features/`, and
      API routes are only in `api/` when an API service exists.
- [ ] Each feature has intent/behavior and reasoned edge cases; each ADR has
      context/decision, a unique ID, and append-only history.
- [ ] Each API route has one method/path operation, OpenAPI-shaped fields, a unique
      ID, and links to related specs.
- [ ] Required root files and `features/`/`adr/` dirs exist; non-empty glossary
      and invariant files contain terms and stable obligations.
- [ ] Non-goals, security, algorithm, grammar, and performance rules are clear;
      undecided behavior remains an open question.
- [ ] Performance-sensitive features use a dedicated function/operation-scoped
      `**Performance.**` block with Big-O inputs defined.
- [ ] No invented intent, code dumps, task tracking, secrets, or machine state.
- [ ] Feature and ADR files follow their templates; skills use `/skill-name`,
      spec files and sections/IDs use Markdown links, and all targets resolve.
- [ ] Every spec ID mention carries `§`, cross-spec mentions are qualified,
      every `§` mention resolves to an existing ID, and all indexes resolve.
- [ ] Every definition heading has a bare ID and an explicit lowercased-ID
      anchor, every ID link targets that anchor, and every glossary term
      heading has an explicit kebab-case anchor.
- [ ] `Spec-Name` is unique within the repository.
- [ ] Every implemented or partial feature and API route, and every invariant
      that code enforces, is cited from code at least once.
- [ ] No spec mention appears in text users see: doc comments that tools
      display, help, diagnostics, error or panic messages, generated or emitted
      output, or anything the software ships.
- [ ] Feature `Status` is `planned`, `partial`, or `implemented`; each `partial`
      feature has `**Current boundary.**`; no file has an `Updated` header.
- [ ] Committed ADRs are unchanged except for single `Superseded by` or
      `Amended by` back-link lines.
- [ ] Every deleted entry's ID is listed in an ADR's `**Retires.**` field, is
      not defined again, and is linked only from ADRs.
- [ ] `OVERVIEW.md` has `## Verification Strategy`; each obligation meets the
      candidate criteria and has `Property`, `Role`, `Tool`, `Scope`, `Bounds`,
      `Assumptions`, and `Obligation`, plus `Model` and `Code link` where its
      role requires them.
- [ ] Every `required` obligation has at least one artifact marked with
      `§VER-<n>`; every waiver links its ADR; no obligation was weakened
      without an ADR.
- [ ] Features with testable behavior have a `**Testing.**` block of kinds and
      targets, and every kind in use has a tool in `## Verification Strategy`.
- [ ] Every design model is linked from an obligation and from `Spec Map`, and
      carries its header and `§VER-<n>` markers.
