---
name: typescript
description: Use when writing, refactoring, or reviewing TypeScript, especially when modeling data and states in the type system, branching over unions, or removing escape hatches such as `any`, type assertions, non-null assertions, or `@ts-ignore`.
---

# TypeScript

## Objective

Write TypeScript whose types carry the design, so that refactoring is
fearless: change a type, and the compiler lists every place that must change
with it. That only works when the types are true. Every `any`, cast, `!`, or
silent default is a place where the compiler stops telling you anything, and
a refactor that compiles is no longer evidence that it works.

The rule of thumb: make illegal states unrepresentable, branch exhaustively,
validate at the edges, and never lie to the type checker.

## Workflow

1. Read the project's `tsconfig.json`, lint configuration, and existing type
   utilities first. Reuse its result, option, matcher, schema, brand, and
   error helpers before writing new ones, and follow `/refactor-reuse`.
2. Model the data before writing logic: which states exist, which fields
   belong to which state, and which values are distinct even when they share
   a runtime type.
3. Write the logic so that every branch over a union is checked for
   exhaustiveness by the compiler.
4. Type the boundaries: everything entering from outside starts as `unknown`
   and is parsed into a domain type once.
5. Run the type checker and the linter. Fix type errors by correcting the
   types or the code, never by widening, casting, or suppressing.
6. For a refactor, change the type first and let the errors lead you to each
   call site.

## Compiler And Lint Settings

Treat these as the floor for new code, and propose them for existing projects
rather than silently loosening anything:

- `strict: true`, which includes `strictNullChecks`, `noImplicitAny`,
  `useUnknownInCatchVariables`, and `strictBuiltinIteratorReturn`. TypeScript
  6.0 and later turn it on by default; still write it explicitly so the intent
  survives a version change.
- `noUncheckedIndexedAccess`, so `array[i]` and `record[key]` include
  `undefined` until checked.
- `exactOptionalPropertyTypes`, so an optional property that is absent differs
  from one explicitly set to `undefined`.
- `noFallthroughCasesInSwitch`, `noImplicitOverride`, `noImplicitReturns`,
  `noUnusedLocals`, and `noUnusedParameters`.
- `verbatimModuleSyntax`, with `import type` for type-only imports.
- `erasableSyntaxOnly` for new code, which rejects `enum`, `namespace`, and
  constructor parameter properties: TypeScript syntax with runtime behavior.
  Code that passes it also runs under runtimes that strip types without
  compiling.
- `noUncheckedSideEffectImports`, so a mistyped `import "./setup"` is an
  error instead of a silent no-op.
- `isolatedDeclarations` for published libraries, which requires explicit
  types on exports so declaration files can be generated without a full
  type check and public types cannot drift by inference.
- An explicit `types` array. TypeScript 6.0 and later default it to empty
  rather than loading every installed `@types` package, so list the ambient
  types the code really uses.

TypeScript 7 is the native compiler. Its `tsc` checks like 6.0 and is much
faster, which makes strict settings and whole-project type checks cheap
enough to run constantly. Options that 6.0 deprecated, such as
`moduleResolution: node`, `baseUrl`, `outFile`, and `target: es5`, are errors
in 7. Tools that embed the compiler through its programmatic API may still
need the 6.x package until that API is stable again.

When the project lints with typescript-eslint, prefer its
`strict-type-checked` configuration plus
`@typescript-eslint/switch-exhaustiveness-check`,
`@typescript-eslint/strict-boolean-expressions`, and
`@typescript-eslint/consistent-type-assertions` with assertions disallowed
except `as const`. Never relax a setting or disable a rule to get a change
through; if a rule is genuinely wrong for a file, disable it for that line
with a comment explaining why.

## Model States, Not Bags Of Fields

- Represent a value that can be in several states as a discriminated union
  with a literal tag, such as `kind` or `_tag`, and put each field only on the
  states where it exists. A loading flag, an error field, and a data field
  that are all optional describe eight combinations when three are real.
- Prefer a union of literals over `boolean` when a value has, or may grow,
  more than two meanings, and over `string` when the set is closed.
- Derive enumerations from a single `as const` source instead of TypeScript
  `enum`: a `const` array or object, with the union type taken from it via
  `typeof` and indexed access.
- Brand values that share a runtime type but must not mix, such as user and
  order IDs, validated emails, or milliseconds and seconds. A brand costs
  nothing at runtime and turns a swapped argument into a compile error. Mint
  branded values only in one validating constructor.
- Make data `readonly` by default: `readonly` properties, `ReadonlyArray`,
  `ReadonlyMap`. Mutation is an implementation detail inside a function, not
  part of a public type.
- Use template literal types for structured strings with a known shape, such
  as route patterns or prefixed IDs, when the project already works at that
  level of precision.
- Derive types from one source of truth: `typeof`, `keyof`, indexed access,
  mapped types, `ReturnType`, and a schema's inferred type, instead of
  restating the same shape by hand in two places.

For larger lifecycles with transitions, also follow /pattern-state-machine.

## Exhaustive Matching

- Every branch over a union must fail to compile when a new member is added.
  That is the property that makes adding a variant safe.
- When the project has an exhaustive matcher library, use it for branching on
  unions and tags instead of `switch`, `if` chains, or ternaries.
- Otherwise use `switch` on the discriminant and end it with an exhaustiveness
  check on the narrowed value: a `default` that passes it to an
  `assertNever(value: never): never` helper, or `value satisfies never`.
- Do not write a `default` branch, an `else`, or a ternary fallback that
  quietly handles "everything else" on a union. It compiles today and
  swallows the next variant forever.
- For a mapping from each member to a value, use an object typed as
  `Record<Union, Value>` or checked with `satisfies Record<Union, Value>`; a
  missing key is then a compile error.
- Use a plain ternary only for a real `boolean`. A two-member union of literals
  is still a union and deserves a match, because it will not stay at two.

Read [patterns.md](references/patterns.md) for code examples of these and the
other patterns in this skill.

## Errors And Absence

- Model expected failure in the return type, with a project `Result` type or
  a discriminated union of outcomes, and model expected absence with the
  project's `Option` type or an explicit `undefined` in the type. Callers then
  have to handle both, and the compiler checks that they do.
- Give errors a tag and the data needed to act on them, and make the error
  part of the type as a union of the specific errors a function can return,
  not `Error` or `unknown`.
- Reserve `throw` for programmer errors and broken invariants, through a small
  `invariant` or `assertNever` helper, and for framework boundaries that
  require it.
- Catch variables are `unknown`. Narrow them, or convert them with one shared
  helper, before reading anything from them.
- Do not paper over absence with `?? ""`, `|| 0`, `?? []`, or similar defaults
  unless the default is a real domain value. A silent empty string is a
  missing-data bug that the type checker can no longer see; see /fallbacks.

## Boundaries

- Data from outside the program, such as `JSON.parse`, `fetch` responses,
  message events, storage, environment variables, files, and command-line
  arguments, starts as `unknown`.
- Parse it once at the boundary with the project's schema validator, and infer
  the static type from the schema rather than declaring both. Inside the
  boundary, code works with the parsed domain types and does not re-check.
- Read environment variables in one typed module that parses them at startup,
  not with scattered `process.env.X` reads and ad hoc `Number()` coercions.
- Type third-party values that arrive as `any` at the point they enter, by
  annotating them as `unknown` and parsing, so the `any` does not spread.

## Escape Hatches

Each of these switches off the checker for the code it touches. Replace it:

| Escape hatch | Replace with |
| --- | --- |
| `any` | `unknown` and narrowing, a generic, or the real type |
| `value as T` | narrowing, a checked type guard, `satisfies`, or parsing |
| `value as unknown as T` | fixing the types that disagree |
| `value!` | narrowing, an `invariant` with a message, or a type without `undefined` |
| `@ts-ignore`, `@ts-nocheck` | fixing the error; `@ts-expect-error` with a reason only for a confirmed compiler or library typing bug |
| `JSON.parse(raw) as T` | parsing with a schema |
| `Function`, `Object`, `{}` as types | a specific function or object type, or `unknown` |
| a `x is T` guard that does not check `T` | a guard that checks every property it claims, or a schema |
| `enum` | an `as const` object or array and a derived union |
| an index signature for known keys | a `Record` over a literal union, or a precise object type |

`as const` and `satisfies` are not escape hatches: they make types more
precise, not less. A user-defined type guard is a cast the compiler cannot
check, so keep each one small, test it, and prefer a schema for anything
non-trivial. When a library's types are wrong, fix them in one typed wrapper
or a declaration patch, not with casts at every call site.

## Generics And Inference

- Let inference work. Annotate function parameters and exported return types;
  do not annotate locals the compiler already infers correctly.
- Rely on inferred type predicates: since TypeScript 5.5, a function such as
  `(x) => x !== undefined` is inferred as a type guard, so
  `items.filter((x) => x !== undefined)` narrows without a hand-written,
  unchecked `x is T`.
- Constrain type parameters (`<T extends Base>`) so misuse fails at the call
  site, and use `const` type parameters to keep literal types without forcing
  callers to write `as const`.
- Use `NoInfer` to stop a parameter from widening an inferred type when it
  should only be checked against it.
- Prefer `satisfies` over an annotation when you want the value checked
  against a type but its precise inferred type kept.
- Keep type-level code proportionate. Conditional and recursive types earn
  their place in shared utilities with tests; in application code, a slightly
  more verbose plain type usually beats a clever one. Watch type-check time
  when a utility recurses.

## Pitfalls

- **Types are erased:** nothing checks a type at runtime. A function typed to
  receive `User` will receive whatever a caller, a response, or a cast hands
  it; that is why boundaries parse.
- **Structural typing:** any value with the right shape fits, so two
  `string` aliases are interchangeable; brand them. Excess property checks
  apply only to fresh object literals, so an extra field in a variable passes
  silently.
- **Unsound corners:** arrays are covariant, so a `Dog[]` passed as
  `Animal[]` can have a `Cat` pushed into it. Methods declared with method
  syntax (`m(x: T): void`) are checked bivariantly; declare callback members
  as properties (`m: (x: T) => void`) to get strict checking.
- **`readonly` is shallow** and only a compile-time view: a `readonly` array
  of objects still has mutable objects, and the same array may be mutable
  through another reference.
- **`Object.keys` and `for...in`** return `string[]`, not `(keyof T)[]`,
  because an object may have more keys than its type lists. Iterate over a
  known key list instead of casting.
- **Narrowing does not survive callbacks:** a narrowed `let` or property is
  widened again inside a closure that runs later. Copy it to a `const` first.
- **Floating promises:** an un-awaited promise loses its errors. Enable
  `@typescript-eslint/no-floating-promises` and
  `@typescript-eslint/no-misused-promises`; never pass an async callback to
  `forEach`, which does not wait for it.
- **Truthiness checks:** `if (count)` and `value || fallback` treat `0`,
  `""`, and `NaN` as missing. Compare with `undefined` explicitly or use `??`.
- **`typeof null === "object"`** and `Array.isArray` is the only reliable
  array check; `{}` as a type accepts every value except `null` and
  `undefined`.
- **In-place array methods:** `sort`, `reverse`, and `splice` mutate, and
  `sort()` without a comparator sorts numbers as strings. Use `toSorted`,
  `toReversed`, and `toSpliced` with an explicit comparator.
- **Numbers:** integers above `Number.MAX_SAFE_INTEGER` lose precision; use
  `bigint` or strings for 64-bit IDs and decimal libraries or integer minor
  units for money.
- **Resource cleanup:** use `using` and `await using` with `Symbol.dispose` or
  `Symbol.asyncDispose` where the runtime supports them, instead of
  `try`/`finally` blocks that are easy to forget.

## Refactoring With The Compiler

- Make the change in the type first, such as adding a variant, renaming a
  field, narrowing a parameter, or replacing a primitive with a brand, then
  follow the errors until the project compiles.
- If a refactor compiles too easily, look for the escape hatch that hid the
  change: a cast, an `any`, a default branch, or an optional field.
- Pin important type-level contracts with type tests, for example
  `@ts-expect-error` lines that must keep failing, or the type assertion
  helpers of the project's test runner; follow /writing-tests.
- Fix lint and type errors at their cause per /fix-lints, not by widening the
  type the error is about.

## Avoid

- `any`, casts other than `as const`, non-null assertions, and suppression
  comments in new code.
- Optional fields and boolean flags standing in for states that a
  discriminated union would make explicit.
- `default`, `else`, or ternary fallbacks that absorb future union members.
- `string` and `number` for IDs, units, and validated values that should be
  branded.
- `T | null | undefined` and empty-value defaults spreading absence through
  the codebase instead of handling it where it arises.
- Thrown exceptions for expected failures, and `catch (e)` blocks that read
  properties of `e` unchecked.
- Unvalidated `JSON.parse`, response bodies, or environment variables typed by
  assertion.
- Un-awaited promises and async callbacks passed to APIs that ignore them.
- Duplicated type declarations that must be kept in sync by hand.
- Loosening `tsconfig.json` or lint rules to make an error go away.
- Type-level cleverness that nobody can read, with no tests and a cost in
  type-check time.
