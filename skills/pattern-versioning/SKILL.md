---
name: pattern-versioning
description: Use when code modules, formats, or functionality need explicit forward-compatible versions, or when code assumes a latest version or mutates historical ones.
---

# Pattern: Versioning

Use this skill when a code module or functionality has multiple versions, when
adding a new versioned code path, or when reviewing a change for version-
boundary mistakes. This includes schemas, protocols, storage layouts,
parsers, serializers, algorithms, and module behavior.

Do not use this skill for crate, package, application, or release versioning.
Use the project's release-versioning convention for those cases.

## Core Contract

Treat these as invariants of every versioned system:

1. **Versions are open-ended.** `v6` is the latest known version, not the final
   version. Do not write code that assumes no `v7` or later version will exist.
2. **Version identity is explicit.** Name implementations, modules, paths,
   fixtures, and tests with their version: `encode_v1`, `parser_v6`, or
   `formats/v6`. Use the repository's established prefix or suffix style, but
   keep the `vN` visible.
3. **Latest has one authority.** Keep the latest-version value and any
   latest-version selection/contract in one canonical owner. Generic defaults,
   dispatch, invariants, and user-facing behavior must derive from that owner;
   they must not repeat the latest number throughout the codebase.
4. **Historical versions are frozen.** All versions before the latest are
   historical/legacy in lifecycle terms, but no one version is a synonym for
   `legacy`, `old`, or `current`. Every earlier version remains identified by
   its own `vN` name. Do not add new features to it or silently make it behave
   like the latest version.
5. **Evolution follows compatibility.** Add compatible features to the latest
   version. Add `vN+1` when a change is breaking for the latest version. Fix an
   older version only for a defect in that version's intended contract; do not
   use a bug fix as a reason to backport new functionality.

The word `latest` is acceptable for the one central selector or façade whose
job is deliberately dynamic. It is not an acceptable name for each
version-specific implementation. Likewise, `legacy` may describe a separately
documented compatibility policy, but it must not be assigned to whichever
version happens to be previous today.

## Correct Names And References

Separate exact-version references from role references:

| Meaning | Good | Bad |
| --- | --- | --- |
| A concrete implementation | `decode_v6`, `FormatV6`, `formats/v6` | `decode_current`, `new_format` |
| A concrete version value | `Version::V6`, `SCHEMA_V6` | `CURRENT_SCHEMA = 6` in many files |
| The single latest authority | `LATEST_SCHEMA_VERSION = Version::V6` | `LATEST_SCHEMA_VERSION` duplicated beside every caller |
| A historical implementation | `migrate_v1_to_v6`, `read_v2` | `legacy_reader`, `old_reader` |
| A default path | `decode_for(LATEST_SCHEMA_VERSION)` | `decode_v6` used as the default everywhere |

An explicit `v6` reference is correct when the code really means `v6`: a v6
reader, a v6 fixture, a migration from v2 to v6, or a compatibility test for
v6. It is incorrect when it only means “whatever is latest.” Search for both
version literals and role words, then classify each occurrence before changing
it.

Do not use `Version::Latest` as a substitute for explicit version variants if
the language can represent `Version::V1`, `Version::V2`, and so on. Define the
latest role once, for example:

```text
enum FormatVersion { V1, V2, V6 }
const LATEST_FORMAT_VERSION = FormatVersion::V6

default_encoder(...) = encoder_for(LATEST_FORMAT_VERSION, ...)
```

The exact spelling and type should follow the project. The important boundary
is that changing the latest version happens in one place. A per-version
contract table or selector should likewise own latest-specific invariants;
callers should not each contain `if version == V6` because v6 is currently
latest.

## Module And File Isolation

Prefer a separate module, file, or directory for each non-trivial version of
the code: `formats/v1`, `formats/v2`, and `formats/v6`, for example. Keep the
latest selector/registry and version-neutral shared types separate from those
implementations. Visible file boundaries make it harder to accidentally add a
feature to a frozen version or let one version's assumptions leak into
another.

Do not put every version into one large file full of `if version == Vn`
branches, and do not create arbitrary tiny files just to satisfy the rule. If
an existing file mixes version responsibilities, split it by cohesive version
ownership. Share a helper only when it is genuinely
version-neutral; a helper that encodes latest behavior belongs with the
latest authority or the explicit version that owns it.

## Version Evolution

Before editing a versioned path, establish which version the change belongs to:

- **Compatible feature:** update only the latest implementation, its explicit
  vN contract/tests, and the central latest authority if needed. Do not edit
  v1, v2, or another historical implementation to gain the feature.
- **Breaking feature:** create a new explicit version with the next available
  number. Keep the previous latest version intact, add the new dispatch and
  contract, then move the central latest authority to the new version.
- **Bug in an older version:** determine whether the behavior violates that
  version's own documented intent. If so, patch that version narrowly and add
  a regression test named for it. If correcting it would change its promised
  wire/data/API contract, preserve the old version and make the correction a
  new version or explicit migration.
- **Compatibility or migration:** keep the source and destination versions
  explicit. A migration may understand multiple versions without turning any
  of them into an ambiguously named `legacy` path.

Never silently rewrite an old version's fixtures, encodings, validation rules,
or behavior merely because the latest version changed. Adding support in a
newer reader for data produced by an older version can be valid, but that is a
new reader capability, not permission to modify the older writer or relabel
the older implementation.

Unknown future versions must have an intentional behavior: normally reject
them with an actionable unsupported-version error, or route them through an
explicit extension mechanism. Never parse an unknown version as the latest
known version just because the latest number is the maximum currently present.

## Workflow

1. **Confirm scope.** Verify that the task concerns versioned code behavior,
   not a package or release number. Identify the versioned boundary, supported
   versions, compatibility promises, and the requested feature or defect.
2. **Read the current model.** Inspect version declarations, implementations,
   dispatch, serializers/parsers, migrations, tests, fixtures, and docs. Find
   the existing latest authority before adding another one.
3. **Classify references.** Mark each occurrence as an exact `vN` reference, a
   latest/current/default role, or an ambiguous historical name. Preserve
   exact-version references; centralize role references; rename ambiguous
   names only when their meaning is clear.
4. **Consolidate latest knowledge.** Reuse a suitable authority when one
   already exists. If repeated latest values or logic have no owner, create
   the smallest shared constant, enum, table, selector, or module. Do not build a broad versioning framework just
   to remove a few literals.
5. **Choose the version boundary.** Apply the compatible-feature, breaking-
   feature, older-version-bug, or migration rule above. State which explicit
   version(s) may change and why.
6. **Implement narrowly.** Keep each version's code and tests under explicit
   module/file ownership. Route generic/default behavior through the central
   latest authority. Do not add feature flags or conditionals that make a
   frozen version impersonate a newer one.
7. **Validate the boundaries.** Run focused checks for the changed version,
   the latest selector, migrations, and unknown/future-version handling. Check
   that historical-version tests still exercise their own contracts and that
   no new latest hard-coding was introduced.
8. **Review the diff.** Look for names such as `current`, `new`, `old`, and
   `legacy`; scattered copies of the latest number; changed historical
   fixtures; accidental terminal assumptions; and unrelated package-version
   work.

## Review Checklist

- Is this actually module/functionality versioning rather than release or
  package versioning?
- Does every version-specific implementation have an explicit `vN` identity?
- Is there exactly one canonical latest-version authority and selector?
- Do default paths derive from that authority instead of hard-coding `vN`?
- Are hard-coded version numbers that remain truly exact-version references?
- Does the design allow a later version without treating today's latest as
  final?
- Are previous versions unchanged except for a narrowly justified bug fix in
  their own contract?
- Was a breaking change made into a new version rather than backported?
- Are migrations, errors, fixtures, and tests explicit about source and target
  versions?
- Is unknown-version behavior deliberate and safe?

## Output

When editing, state the versioned boundary, the central latest authority, and
the evolution decision. Report which explicit versions changed and which were
intentionally left frozen. Include the focused checks run and any unresolved
compatibility or future-version risks.

When auditing, report findings by explicit version and distinguish:

- scattered latest assumptions that should be consolidated;
- ambiguous names that hide a concrete version;
- unauthorized changes to historical versions; and
- legitimate exact-version references that should remain.
