---
name: openapi
description: Use when creating, implementing, or reviewing an HTTP API or an OpenAPI 3.x description.
---

# OpenAPI

Use this skill when creating or changing an HTTP API, its OpenAPI description,
or the code that must honor that description. Treat the description as a
consumer-facing contract: a client should be able to understand the URL,
method, authentication, inputs, outputs, errors, and serialization without
reading server source code.

The goal is the essential, interoperable part of OpenAPI, not a contest for
exhaustive or validator-specific compliance. Do not add callbacks, webhooks,
XML modeling, links, custom parameter serialization, discriminators, or other
advanced features unless the API actually needs them.

## First establish the contract

Before editing code or a specification:

1. Read repository instructions, existing API descriptions, route definitions,
   schemas, tests, and the project's API/versioning conventions. Identify the
   source of truth: contract-first, code-first, or a deliberately synchronized
   pair.
2. Confirm the OpenAPI version supported by the repository's tooling. The
   `openapi` field is the specification version, not the API version and not
   `info.version`. Use the newest version the toolchain actually supports; use
   3.2.0 only when the consumers and validators support it. Do not use features
   from a newer version while declaring an older one.
3. List each use case as an operation: who calls it, which resource or action
   it affects, inputs, authentication, success result, known failures, and
   side effects. Resolve ambiguous product behavior before inventing a schema.
4. Decide the wire contract before implementation: paths, HTTP methods, media
   types, parameter serialization, status codes, request/response shapes, and
   stable operation identifiers.

Keep the contract and implementation synchronized in the repository's normal
way. Never document a behavior the server does not provide, and do not let an
implementation silently broaden or narrow a documented contract.

## The essential document shape

An ordinary API description should have this shape:

```yaml
openapi: 3.1.0                 # or the repository's supported version
info:
  title: Example API
  version: 1.0.0               # version of this API description/release
servers:
  - url: https://api.example.com/v1
paths:
  /users/{userId}:
    get:
      operationId: getUser
      summary: Get a user
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '200':
          description: User returned
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
components:
  parameters: {}
  responses: {}
  schemas: {}
```

For a normal HTTP API, `openapi`, `info.title`, `info.version`, and `paths`
are the important root fields. The OpenAPI root must contain at least one of
`paths`, `webhooks`, or `components`; an ordinary routed API should have
`paths`. `servers` is optional, but provide it when the base URL is not obvious
or when multiple environments matter. `components` is only a library of
reusable definitions: an unused component has no effect until referenced.

Do not copy the empty component maps from the example just for appearance.
Remove empty sections unless the local style or a generator requires them.

## Model every operation explicitly

For each path and method:

- Use a leading-slash path. Use `{parameterName}` for path variables, and
  define each one as `in: path` with the same name and `required: true`.
- Prefer stable, resource-oriented paths and HTTP semantics: `GET` reads,
  `POST` creates or performs a non-idempotent action, `PUT` replaces,
  `PATCH` partially updates, and `DELETE` removes. Use an action subpath only
  when the domain action is not naturally a resource mutation.
- Give every operation a unique, stable, case-sensitive `operationId`. Treat
  changing it as a client-facing compatibility change because generators and
  clients commonly use it as an identifier.
- Add a short `summary`; use `description` for important behavior, side
  effects, preconditions, pagination rules, or idempotency expectations. Use
  tags only for useful documentation grouping.
- Put scalar filters, pagination, sorting, and selectors in query parameters.
  Give them explicit types, defaults, bounds, and serialization behavior when
  those details affect callers. Avoid undocumented ad hoc query conventions.
- Use request bodies for payloads where the HTTP method has clear body
  semantics. Avoid request bodies on `GET` and `DELETE` unless the API has a
  deliberate, documented convention and its tooling supports it.
- Do not model `Authorization` or `Content-Type` as ordinary header
  parameters. Declare authentication with `securitySchemes` and payload media
  types with `content`.
- Avoid ambiguous or overlapping templated paths. A path placeholder must not
  be used to smuggle an unescaped `/`, `?`, or `#` into a path segment.

An operation's `responses` is not optional. Document at least the normal
success response and the known, meaningful errors. Use the actual HTTP status
semantics (`201` for creation when appropriate, `204` for no body, `400` or
`422` for invalid input according to the API convention, `401`/`403` for
authn/authz, `404`, `409`, rate limits, and server failures as applicable).
Every response entry should have a clear `description`; add `content` only
when that response has a body. Do not claim every possible status if the
implementation cannot produce it. A `default` response is useful for an
otherwise consistent error envelope, but does not replace documenting important
known errors.

Quote response-code keys in YAML (`'200'`, not `200`) for JSON/YAML/tooling
compatibility.

## Parameters, bodies, and media types

Parameter definitions describe serialized values, not just in-memory types.
For ordinary parameters, specify `name`, `in` (`path`, `query`, `header`, or
`cookie`), and exactly one of `schema` or `content`. OpenAPI 3.2 also has
`in: querystring` for describing the entire query string as one media-typed
value; use it only when needed, and do not mix it with ordinary query
parameters. Use `content` only when a parameter is genuinely represented as a
media type; keep ordinary parameters simple. A parameter is uniquely
identified by its name and location, so do not define duplicates at path and
operation level.

For a request body:

```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/CreateUser'
      examples:
        valid:
          value:
            email: sam@example.com
            displayName: Sam
```

Use the actual media type keys the server accepts or returns. For each
representation, define its schema and provide examples when the shape,
encoding, or edge cases are not obvious. Keep `application/json` as the
default only when the API really speaks JSON; do not use `*/*` to hide an
unknown contract. A request body's `required` flag means the body itself must
be present; property presence belongs in the schema's `required` list.

If arrays or objects appear in query, header, or cookie values, specify how
they are serialized (`style` and `explode`) or choose a simpler representation.
Do not rely on a framework's undocumented serialization defaults. Treat URL
percent-encoding and form-urlencoded `+`/space behavior as part of the wire
contract, especially when examples contain reserved characters.

## Schemas are JSON Schema models

In OpenAPI 3.1 and 3.2, Schema Objects are based on JSON Schema Draft 2020-12
with the OpenAPI dialect. In 3.0, the schema dialect is different; follow the
declared version and the project's supported subset.

For each model:

- Use an explicit `type` whenever the value's type matters. For objects,
  define `properties`; for arrays, define `items`; use `enum`, bounds, string
  constraints, and formats when they are real contract constraints.
- Remember that `required` is an object-level list of property names. A
  property is optional unless its name appears there. `required` is not a
  boolean on a property.
- Distinguish absent from `null`. In 3.1+, express nullability with the JSON
  Schema type union (for example `type: [string, 'null']`) or an equivalent
  schema. Use `nullable: true` only in a deliberately 3.0 contract.
- Treat `format` as useful semantic metadata, not a substitute for validation;
  many tools treat formats as annotations. Enforce business rules in the
  server and test the boundaries.
- Decide deliberately whether unknown object properties are accepted. JSON
  Schema permits them by default; use `additionalProperties: false` only when
  the API truly wants a closed shape and understands the compatibility cost.
- Model input and output differences explicitly. Separate create/update and
  response schemas when that is clearer; otherwise use `readOnly` and
  `writeOnly` intentionally and verify the chosen generator handles them.
- Use `oneOf`/`anyOf` only when the alternatives are distinguishable and the
  server can validate the same rule. `allOf` composes constraints; it does not
  by itself create an inheritance hierarchy. Add a discriminator only when
  clients need a stable type-selection hint.
- Prefer JSON Schema's `examples` or media-type/parameter `examples` in newer
  contracts. Use fields supported by the declared OpenAPI version and do not
  leave examples that contradict the schema.

For binary data, describe the real media type at the `content` level. In
3.1+, use JSON Schema `contentMediaType`/`contentEncoding` when binary is
embedded in text; do not blindly carry OAS 3.0's `format: binary` convention
into a 3.1+ schema. For a raw file body, a media type with an intentionally
empty schema may be the clearest contract.

## Reuse without obscuring the contract

Put genuinely shared schemas, parameters, responses, request bodies, headers,
and security schemes under `components`, then reference them with stable local
`$ref` values such as `#/components/schemas/User`. Reuse should reduce drift,
not hide operation-specific rules or force unrelated payloads into one model.

Keep references resolvable and avoid external references unless the repository
has a tested resolver and a stable deployment path. A Reference Object is not
a free-form object: do not put arbitrary sibling fields next to `$ref` and
expect every tool to merge them. Put descriptions in the target component, or
use only sibling fields supported by the declared OpenAPI version.

Use one consistent error model when the API has multiple operations. A useful
error response normally identifies a stable machine-readable code, a human
message, and any safe field-level details or request/correlation identifier.
Never place secrets or sensitive data in examples, descriptions, schemas, or
tracked generated output.

## Declare security where it applies

Represent authentication and authorization in the document, not only in
prose:

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
security:
  - bearerAuth: []
```

Use the scheme that matches the implementation (`apiKey`, `http`,
`mutualTLS`, `oauth2`, or `openIdConnect`). Apply global `security` for the
normal default and override it per operation for public or differently scoped
operations. Multiple entries in the `security` array are alternatives (OR);
multiple schemes in one object are all required (AND); an empty object `{}`
means anonymous access is allowed. For OAuth2/OpenID Connect, document the
real scopes and endpoints; do not invent scopes merely to fill the section.

## Examples and descriptions are part of usability

Examples should be valid instances of their schemas and valid serialized wire
values for their media type or parameter style. Include at least one normal
success example and representative invalid, empty, boundary, or error examples
when they clarify behavior. Keep descriptions precise about units, time zones,
ordering, inclusivity of bounds, side effects, and whether fields are omitted,
nullable, or server-generated.

OpenAPI field names are case-sensitive unless the relevant HTTP rule says
otherwise. Keep YAML JSON-compatible, use CommonMark conservatively in
descriptions, and use `x-...` for custom OpenAPI extensions. Do not add
vendor-specific fields to pretend they are portable standard fields.

## Implementation and review workflow

1. Inspect the existing routes, handlers, serializers, validators, auth
   middleware, tests, and local API conventions.
2. Write or update the contract at the repository's source-of-truth boundary.
   Keep operation IDs, schemas, examples, and error responses near the code or
   document that owns them according to local convention.
3. Implement the smallest change that makes the server behavior match the
   contract. Preserve compatibility deliberately: renaming fields, changing
   requiredness, changing status codes, or changing operation IDs can break
   clients.
4. Validate with existing repository tooling first. At minimum, parse the
   OpenAPI document, resolve local references, check every path placeholder,
   ensure operation IDs are unique, verify examples against schemas, and
   compare documented routes/methods/media types/statuses/auth with the actual
   implementation. Run focused request/response tests when available.
5. Review the diff for invented behavior, stale examples, undocumented error
   paths, accidental secrets, version mismatches, and changes outside the API
   ownership boundary.

Prioritize failures that affect interoperability or runtime truth: malformed
structure, broken references, missing path parameters, invalid examples,
misdocumented authentication, mismatched required fields, wrong media types,
and response/status behavior. Do not spend the task on optional metadata or
low-value stylistic warnings when the essential contract is sound.

The guidance is based on the [OpenAPI Specification v3.2.0](https://spec.openapis.org/oas/latest.html).
When the repository targets another OpenAPI version, its declared version and
toolchain take precedence, with the same essential contract principles.
