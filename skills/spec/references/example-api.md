# API Route File Example

API files live under `.spec/api/` only when the project defines an API service.
Each file describes one path-and-method operation and follows the OpenAPI-shaped
route contract rather than becoming a feature summary or a copied OpenAPI
document.

```markdown
# Mirrorctl — API Create User

> Status: active
> Parent: [OVERVIEW.md](../OVERVIEW.md)

## API-001 — POST /v1/users <a id="api-001"></a>

**Method.** `POST`

**Path.** `/v1/users`

**Operation ID.** `createUser`

**Intent.** Create a user-owned mirror configuration after validating the
request and establishing its initial ownership boundary.

**Behavior.** The route validates the request, persists the configuration, and
returns its stable identifier. It does not start a mirror run in the same
request.

**Authentication.** Required — bearer token; missing or invalid credentials
return `401` without revealing whether the requested account exists.

**Authorization.** The authenticated principal must have the `mirror:write`
scope; cross-account ownership is rejected with `403`.

**Incoming data validation.**
- `name` is required, non-empty, and limited to 100 Unicode characters.
- `source` must be an absolute local path accepted by the service policy.
- Unknown JSON fields are rejected so clients cannot silently believe an
  unsupported setting was accepted.

**Rate limiting.** 10 creates per principal per minute; excess requests return
`429` with `Retry-After`.

**Request.** `application/json` with `name` and `source`; no idempotency key is
defined, so clients must not retry an ambiguous timeout as if it were safe.

**Responses.**
- `201` — returns the configuration identifier and normalized name.
- `400` — returns field-level validation errors without echoing secrets.
- `401` / `403` — returns the standard authentication or authorization error.
- `409` — returns a conflict when the normalized name is already owned.
- `429` — returns the rate-limit error and retry guidance.

**Errors.** Error codes are stable, response bodies contain no credentials or
local machine paths, and `400`/`409` are not retried without changing input.

**Edge cases.**
- Duplicate normalized name → return `409` and leave existing configuration
  unchanged. Why: creation must be repeatable without overwriting ownership.
- Request timeout after persistence → a later read may find the created
  configuration; clients must reconcile before retrying. Why: the response can
  be lost after the state change.

**Testing.**
- **contract** — each documented status code, body shape, and stable error
  code is returned by the running service.
- **integration** — a duplicate normalized name leaves the existing
  configuration unchanged.

**Depends on.** [§F-02](../features/plan.md#f-02),
[§INV-01](../INVARIANTS.md#inv-01).

**Related routes.** [§API-002](auth/sign-in.md#api-002).

**Related specs.** [§ADR-0003](../adr/security.md#adr-0003).

**Skills.** `/examples`, `/spec`.

**Status.** implemented

## References

### Normative

- [OpenAPI 3.1 Operation Object](https://spec.openapis.org/oas/v3.1.0.html#operation-object) —
  `operationId`, responses, parameters, and security are represented explicitly.
```

The example uses `None` only where a route truly has no applicable policy. A
real route should state its authentication, authorization, validation, rate
limit, request, response, and edge-case behavior even when those values are
public, empty, or intentionally unsupported.
