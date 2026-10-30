---
name: fragile
description: Use when core logic relies on fragile checks, such as weak pattern matching, string sniffing, or guessed sets of expected values, where a stronger check, parser, or type is available.
---

# Fragile

Use this skill when writing, reviewing, or refactoring core logic that decides
something: detecting a format, validating input, dispatching on a case,
classifying an error, interpreting a tool's result, or gating behavior. The
question it answers is whether the check is as strong as the context allows, or
whether it is a weak proxy standing in for a complete one that was available
all along.

This targets mainstream product and system logic — the code that has to be
right at runtime. Tests and assertions are not the target; see
[Tests Are Not The Target](#tests-are-not-the-target).

## Core Rule

Use the strongest check the context actually affords. When structure exists —
a parser, a typed API, an enum, a schema, a machine-readable output mode, a
real query interface — check against that structure instead of pattern matching
its rendered surface.

This is not "regexes are banned". A regex over genuinely unstructured text is
the correct tool. The failure is reaching for a substring, a regex, or a
name-based guess when a complete check was available and reasonable, so the
code appears to work while silently failing on every input the pattern did not
anticipate.

## Never Guess The Set Of Possible Values

Do not invent the set of values something can produce and then match against
the invented set. This means hard-coding the error messages an operation
"probably" returns, the status strings an API "likely" uses, the exit codes a
tool "should" emit, or the field names a payload "might" carry, and covering
the uncertainty with a list of alternatives. It is forbidden unless the set is
verified, or the user has deliberately accepted a guessed set for this case.

The tell is provenance: for every value in the list, you must be able to say
where it came from. "It seemed likely", "that's the usual wording", or "this is
what the error looked like once" are not sources. A second tell is growth — if
branches get added each time a run fails, that is brute forcing a set by trial,
and each new branch makes the code look more thorough while staying just as
unfounded. Stop and establish the real set instead of widening the guess.

Establish it by one of these, in whatever order the situation makes cheapest:

1. **Read the source.** If the dependency, crate, library, or tool is open
   source or vendored, inspect it. The error enum, the constant, the format
   string, the status table — they are in the code. Read the exact version the
   lockfile pins, not the latest one. Cloning or fetching source to read is
   fine; running it is a separate decision governed by the repository's
   remote-code rules.
2. **Read the documentation.** Use `/research-web` to find the specific
   documented values, error codes, status enumerations, or output schema in the
   upstream's own reference, changelog, or API docs. Invoking this skill is
   sufficient authorization for that lookup. Cite what you found.
3. **Observe it directly.** Run the operation and capture what it actually
   produces. Only when the user has authorized running it, and only for
   non-destructive operations. One real observation beats four imagined ones,
   but note that observing one value does not prove it is the only value.

If none of those are available, do not fabricate a set. Either check something
you can rely on structurally — a type, a code, an exit status the contract
guarantees — or handle the general case and fail loudly on the unrecognized
value, surfacing the value itself so the real set becomes knowable. Then say
plainly which set you could not determine and why, and ask the user if the
decision depends on it.

## Fragile Signatures

Treat these as fragile until proven otherwise:

| Fragile check | Stronger check when available |
| --- | --- |
| Regex or substring over JSON, YAML, TOML, XML, or HTML | Parse it and inspect the field or node |
| Scraping a command's human-readable output | The tool's `--json`/machine output, its exit codes, or its library API |
| Deciding a file's type from its name or extension | Content type, magic bytes, or the producer's declared type |
| Comparing an error's message text | Typed error variants, error codes, `kind()`, or downcasting |
| A hard-coded list of messages or states the code "might" encounter | The real set, read from the dependency's source, its docs, or observed output |
| `if`/`else if` chains over strings | An enum with an exhaustive `match`, so a new case is a compile error |
| `startsWith`/`contains` on paths | Path APIs, canonicalization, and real ancestor checks |
| Comparing version strings lexically | A semver or version-ordering parser |
| Only checking an exit code, or only that output is non-empty | The specific condition the code actually depends on |
| Inferring capability from an OS, hostname, or env var name | Probing for the capability itself |
| `grep` over source to determine code structure | AST, LSP, or the language's own tooling |
| Booleans and flag combinations encoding real states | An explicit state machine, per `/pattern-state-machine` |

The shared tell: the check tests a *rendering* of the truth rather than the
truth, so it breaks when the rendering changes even though nothing real did.

## Tests Are Not The Target

Do not apply this skill to test code, assertions, fixtures, or test helpers. A
loose assertion is a test-design question owned by `/writing-tests`, not a
fragile-check violation, and tests have their own reasons to match text
directly. Strengthening assertions can also over-fit a test to the current
implementation, which makes the suite worse rather than better.

Two narrow exceptions:

- The user explicitly asks to apply this skill to tests.
- A test helper is really production logic that happens to live under a test
  directory — a parser, a client, a fake that other code depends on being
  correct. Judge that by what the code does, not where it sits.

Otherwise, when a weak check in core logic and its test both need attention,
fix the core logic here and leave the test to `/writing-tests`.

## When A Weak Check Is Correct

Keep the weak check, deliberately, when:

- the input is genuinely unstructured — logs, free text, human prose;
- the text really is the contract, because the upstream tool documents that
  output and offers nothing machine-readable;
- no parser exists in the language or repo, and adding a dependency for it
  would violate the repository's dependency rules;
- the scope is a bounded one-off — a local script or a scratch check whose
  blast radius is a rerun.

In those cases make the weakness explicit rather than ambient:

- anchor and constrain the pattern instead of matching loosely anywhere;
- validate what was extracted before using it;
- fail loudly when the pattern does not match, rather than falling through to a
  default that pretends the check succeeded — see `/fallbacks`;
- note in a brief comment why the stronger check was not used.

A check that silently passes when its assumption breaks is worse than one that
errors. Prefer the loud failure.

## Protocol

1. Identify every decision point in the core logic you are touching: each
   detection, validation, dispatch, classification, and result interpretation.
2. For each, ask what the check is really testing, and what would make it pass
   or fail incorrectly. Name a concrete input that defeats it.
3. Wherever the check compares against a set of expected values, state where
   each value came from. If any of them is a guess, stop and establish the real
   set from source, docs, or observation before writing the check.
4. Ask what structure is already available at that point — a parsed value, a
   typed error, an enum, a schema, a machine-readable mode, an existing helper
   in this repo (see `/refactor-reuse`).
5. If a stronger check is available and reasonable here, use it.
6. If it is not, keep the weak check, constrain it, make its failure loud, and
   say why in a comment.
7. Report any fragile check you left in place and the reason, rather than
   leaving it silently.

## Scope And Restraint

- Apply this to the work at hand. Do not launch a repo-wide hunt for weak
  checks, and do not rewrite unrelated working code because it matches a
  signature above.
- Do not add a dependency purely to make a check more elegant. The
  repository's dependency rules still apply; a constrained regex beats an
  unjustified new dependency.
- Do not over-engineer. A parser, a typed error, and an exhaustive match are
  strong because they are complete, not because they are elaborate. If the
  strong option is genuinely more complex than the decision warrants and the
  weak one cannot fail meaningfully in this context, the weak one is fine.
- When the answer turns into an architecture question rather than a local
  choice of check, escalate to `/approach`. When the weak check exists to
  paper over behavior that is already wrong elsewhere, escalate to
  `/layering`.
