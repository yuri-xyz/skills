# TypeScript Patterns

Small examples of the patterns in the skill. Adapt names and helpers to the
project; when it already has a matcher, `Result`, `Option`, brand, or schema
library, use that instead of these hand-written versions.

## Contents

- Discriminated unions instead of optional fields
- Exhaustive `switch`
- Exhaustive lookup tables
- Enumerations from one `as const` source
- Brands
- Results and tagged errors
- Parsing at the boundary
- Narrowing instead of assertions
- Inference helpers
- Type tests

## Discriminated Unions Instead Of Optional Fields

```ts
// Eight combinations, three of them real, and nothing stops `data` and
// `error` from both being set.
type Loose<T> = { loading?: boolean; data?: T; error?: Error };

// Exactly the real states; `data` exists only where it is meaningful.
type RemoteData<T, E> =
  | { readonly kind: "loading" }
  | { readonly kind: "loaded"; readonly data: T }
  | { readonly kind: "failed"; readonly error: E };
```

## Exhaustive `switch`

```ts
export const assertNever = (value: never, message = "Unreachable branch"): never => {
  throw new TypeError(message, { cause: value });
};

const describe = <T, E>(state: RemoteData<T, E>): string => {
  switch (state.kind) {
    case "loading":
      return "Loading";
    case "loaded":
      return "Ready";
    case "failed":
      return "Failed";
    default:
      // Adding a variant makes `state` no longer `never` here: a compile error.
      return assertNever(state);
  }
};
```

Without a helper, `state satisfies never;` in the `default` branch gives the
same compile-time check. A matcher library, when the project has one, gives
the same guarantee as an expression and is preferable to `switch`.

## Exhaustive Lookup Tables

```ts
type Status = "draft" | "published" | "archived";

// A missing or misspelled key is a compile error, and the values keep their
// literal types.
const STATUS_LABEL = {
  draft: "Draft",
  published: "Published",
  archived: "Archived",
} as const satisfies Record<Status, string>;
```

## Enumerations From One `as const` Source

```ts
export const ROLES = ["viewer", "editor", "admin"] as const;
export type Role = (typeof ROLES)[number];

const isRole = (value: string): value is Role =>
  ROLES.some((role) => role === value);
```

The runtime list and the type cannot drift, and the list is available for
validation and iteration, which a `type` alone is not.

## Brands

```ts
declare const brand: unique symbol;
type Brand<T, Name extends string> = T & { readonly [brand]: Name };

export type UserId = Brand<string, "UserId">;
export type OrderId = Brand<string, "OrderId">;

// The only place a UserId is minted.
export const parseUserId = (raw: string): Result<UserId, InvalidId> =>
  /^usr_[a-z0-9]{12}$/.test(raw) ? ok(raw as UserId) : err({ _tag: "InvalidId", raw });

declare const cancel: (order: OrderId) => void;
declare const user: UserId;
cancel(user); // Compile error: a UserId is not an OrderId.
```

The single `as` lives inside the validating constructor, next to the check
that justifies it; nothing else in the codebase casts to a brand.

## Results And Tagged Errors

```ts
type Ok<T> = { readonly ok: true; readonly value: T };
type Err<E> = { readonly ok: false; readonly error: E };
type Result<T, E> = Ok<T> | Err<E>;

const ok = <T>(value: T): Ok<T> => ({ ok: true, value });
const err = <E>(error: E): Err<E> => ({ ok: false, error });

type NotFound = { readonly _tag: "NotFound"; readonly id: UserId };
type Forbidden = { readonly _tag: "Forbidden"; readonly reason: string };

declare const loadUser: (id: UserId) => Promise<Result<User, NotFound | Forbidden>>;

const result = await loadUser(id);
if (!result.ok) {
  // `result.error` is `NotFound | Forbidden`; match on `_tag` exhaustively.
  return handleLoadError(result.error);
}
use(result.value);
```

## Parsing At The Boundary

```ts
// With a schema library: one declaration gives both validation and the type.
const Settings = schema.object({
  theme: schema.literal("light", "dark"),
  fontSize: schema.number().int().min(8).max(32),
});
type Settings = schema.Infer<typeof Settings>;

const loadSettings = (raw: string): Result<Settings, ParseError> =>
  Settings.parse(JSON.parse(raw) as unknown);
```

`schema` stands for the project's validator. `JSON.parse` itself throws on
malformed input, so wrap it the way the project turns throwing calls into
results. It also returns `any`; the
`as unknown` widens it to the safe top type rather than asserting anything, so
the value cannot be used until the schema has checked it. Never write
`JSON.parse(raw) as Settings`.

## Narrowing Instead Of Assertions

```ts
// Instead of `map.get(key)!`:
const entry = map.get(key);
if (entry === undefined) {
  return err({ _tag: "MissingEntry", key });
}

// Instead of `(event.target as HTMLInputElement).value`:
if (event.target instanceof HTMLInputElement) {
  setValue(event.target.value);
}

// Instead of `catch (e) { log(e.message) }`:
try {
  run();
} catch (error) {
  log(error instanceof Error ? error.message : String(error));
}

// Instead of `items[0]!` with noUncheckedIndexedAccess:
const [first] = items;
if (first === undefined) {
  return none;
}
```

## Inference Helpers

```ts
// `const` type parameter: literal types without `as const` at the call site.
const defineRoutes = <const R extends Record<string, `/${string}`>>(routes: R) => routes;
const routes = defineRoutes({ home: "/", settings: "/settings" });
// routes.home is "/" rather than string.

// NoInfer: `fallback` is checked against T but does not widen it.
const pick = <T extends string>(options: readonly T[], fallback: NoInfer<T>) => fallback;
pick(["a", "b"], "c"); // Compile error instead of T widening to "a" | "b" | "c".

// satisfies: checked against the wider type, precise type kept.
type Setting = number | string;
const config = {
  retries: 3,
  mode: "strict",
} satisfies Record<string, Setting>;
config.retries.toFixed(); // `retries` is number, not number | string.
```

## Type Tests

```ts
// In a type test file that runs through the type checker.
// @ts-expect-error a UserId is not an OrderId
cancel(userId);

// @ts-expect-error a new Status without a label must fail
const LABELS: Record<Status | "deleted", string> = STATUS_LABEL;
```

`@ts-expect-error` is right here because the error is the thing under test:
if the line ever compiles, the test fails. Use the test runner's type
assertion helpers, where it has them, for positive checks such as "this
function returns `Result<User, NotFound>`".
