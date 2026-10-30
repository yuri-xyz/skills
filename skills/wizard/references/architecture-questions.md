# Architecture and product questions

The checklist `/wizard` works through before proposing an approach. Each entry
names the decision and the typical answers to offer as options. Ask only what
applies to the request and is not already obvious from it, the repository, or
an earlier answer, and say which entries were skipped as obvious.

A new project or product touches most of the list. A feature inside an
existing project touches only the entries it could change. Settle these with
the user, since they rest on intent, money, audience, or risk appetite, not on
technical merit.

## Purpose and audience

- **Problem and outcome.** What it is for, and what success looks like in
  concrete terms.
- **Audience.** Only the owner, friends or a small group, a company's own
  staff, other businesses (B2B), the public (B2C), or developers (a library,
  API, or tool).
- **Scale.** Expected users, data volume, and traffic: one person, tens,
  thousands, more. Whether spikes matter.
- **Scope of the first version.** What the MVP must include, what can wait,
  and the explicit non-goals.
- **Timeline.** A prototype to try, a durable personal tool, or a product to
  launch, and whether there is a deadline.

## Platform and distribution

- **Platform.** Web app, CLI, desktop app (Linux, macOS, Windows), mobile app,
  server or API only, library, browser extension, or several.
- **Distribution.** Self-hosted, a hosted service, app stores, package
  registries (npm, crates.io), Nix flake only, or not distributed at all.
- **Deployment target.** For anything hosted: Cloudflare (Workers, Pages, R2,
  D1), a VPS, a managed platform (Fly.io, Vercel, Render), a big cloud (AWS,
  GCP, Azure), the owner's own machine or home server, or none.
- **Offline and sync.** Online only, offline-first with sync, or local only.

## Money and licensing

- **Business model.** Free, paid once, subscription, usage-based, freemium,
  donations, internal cost only, or undecided.
- **Payments.** When it is paid: which provider (Stripe, Paddle, Lemon
  Squeezy, app-store billing), and whether taxes and invoicing must be
  handled.
- **Running-cost budget.** Free tiers only, a small monthly budget, or
  whatever scale needs.
- **License and openness.** Open source (which license), source-available,
  proprietary and distributed, or private use only. Follow the project's
  existing license when it has one.

## Users, data, and trust

- **Accounts and auth.** No accounts, local single user, email and password,
  OAuth or social login, passkeys, a hosted auth provider (Clerk, Auth0),
  or SSO for businesses.
- **Tenancy.** Single user, multi-user with shared data, or multi-tenant with
  isolated organizations.
- **Data and persistence.** What is stored, where it lives (local files,
  SQLite, Postgres, object storage, a hosted database), and how long it is
  kept.
- **Privacy and compliance.** Personal data, GDPR or other jurisdictions,
  data residency, analytics and telemetry stance, and anything regulated
  (health, finance, minors).
- **Security posture.** What would be damaging if it leaked or broke, and who
  could be an attacker.

## Integrations and operations

- **Integrations.** External services, APIs, or existing systems it must talk
  to, and whether those are given or open to choice.
- **Availability.** Best effort, or a real uptime expectation, and who is
  paged when it breaks.
- **Backups and recovery.** Whether data loss is acceptable, and how far back
  restores must reach.
- **Maintenance.** Who maintains it long-term, and how much ongoing upkeep is
  acceptable.

## Experience

- **Interface and branding.** Whether it has a visual identity, a reference
  look, or follows an existing project's design.
- **Languages and regions.** One language, or internationalization from the
  start.
- **Accessibility.** The level expected, especially for public products.
