# Critical paths by application kind

Starting points, not a complete list: every application has paths of its own
that matter more than any generic entry. Most applications combine several
kinds; take the union.

## Everywhere

- Authentication, sessions, tokens, API keys, and account recovery.
- Authorization and tenant or ownership checks, and every path that changes
  roles, permissions, or ownership.
- Parsing of anything from outside: requests, files, archives, messages,
  configuration, environment, command-line arguments, and IPC.
- Secrets: loading, storing, passing to subprocesses, logging, and rotation.
- Destructive operations: deletion, overwrite, truncation, migrations, and
  bulk actions.
- Money and quotas: payments, credits, billing, usage limits, and anything
  with a balance.
- Update, install, and plugin loading: anything that fetches or executes
  code.
- Error handling and logging on all of the above.

## Web apps and APIs

- Login, signup, logout, password reset, MFA, OAuth and SSO callbacks, email
  verification, and session refresh.
- Every API route and method that reads or changes another user's data, admin
  routes, and internal or service-to-service endpoints.
- Request parsing and validation, file uploads, imports, and exports.
- Outbound fetches from user input: webhooks, link previews, image proxies,
  and imports from URLs.
- Webhook receivers, especially payment providers.
- Rendering of user content: templates, Markdown, rich text, emails, and
  PDFs.
- Reverse proxy, CDN or edge, CORS, headers, cookies, and TLS config.
- Background jobs and queues acting on behalf of users.

## CLIs and developer tools

- Argument and config parsing, environment variables, and file paths from
  input.
- Shell and subprocess invocation.
- File writes, deletes, and recursive operations, including symlink handling.
- Network fetches, downloads, and anything that executes fetched content.
- Credential storage and handling for remote services.

## Desktop and Electron apps

- IPC between renderer and main process, preload bridges, and exposed APIs.
- Loading remote content, navigation, `webview`s, and deep links or custom
  URL schemes.
- File open and save, drag and drop, and clipboard.
- Auto-update and plugin or extension loading.
- Local credential storage and keychain use.

## Services, daemons, and agents

- Network listeners and their protocol parsers.
- Privilege handling: running as root, capabilities, privilege drops, and
  setuid helpers.
- Sockets and IPC endpoints, and who can connect to them.
- Config reload, and state files writable by other users.

## Libraries, parsers, and codecs

- Public entry points that take untrusted bytes or text.
- Length, offset, and size arithmetic; recursion; and allocation from input.
- `unsafe` code, FFI, and native extensions.
- Defaults that downstream users rely on for safety.

## Infrastructure and configuration (Nix, containers, CI)

- Secrets in configuration, build outputs, and logs.
- Network exposure: open ports, firewall rules, and services bound to all
  interfaces.
- Sandboxing and privilege of services and applications.
- CI workflows that handle secrets or run on untrusted pull requests; pinned
  versus moving dependencies.

## Data pipelines and AI features

- Ingestion and parsing of external data.
- Prompt construction from untrusted content (prompt injection) and tools or
  actions the model can trigger.
- Exports and sharing of user data.
