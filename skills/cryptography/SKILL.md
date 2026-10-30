---
name: cryptography
description: Use when designing, implementing, reviewing, or choosing anything cryptographic, such as encryption, hashing, password storage, key derivation, signatures, key exchange, tokens, wallets, secure randomness, encrypted file metadata, crypto libraries, or post-quantum requirements.
---

# Cryptography

Apply this skill whenever code creates, stores, derives, transports, authenticates, hashes, signs, or verifies secrets or security-sensitive data. Use it for design and review; do not treat it as a substitute for a professional cryptographic audit. To review existing or changed code for cryptographic misuse, use `/review-cryptography`, which judges findings against this skill.

## Non-negotiable rules

- Never invent a cipher, hash, MAC, KDF, signature scheme, key exchange, nonce construction, password format, or cryptographic protocol. Do not “improve” a primitive by composing it informally. Use a maintained, high-level library or an established interoperable format whose security design is documented and reviewed.
- Never use a password, username, timestamp, process ID, device identifier, predictable seed, UUID v1, `Math.random`, an ordinary PRNG, or a hand-rolled generator as key material, a salt, a nonce, a token, or a wallet seed.
- Never treat encryption without authentication as sufficient. Prefer an AEAD or a maintained format that provides authenticated encryption, and fail closed on authentication failure.
- Never hard-code private keys, symmetric keys, salts, nonces, test secrets in production paths, or recovery material in source, logs, command lines, ordinary environment variables, or tracked configuration.
- Never claim that encryption hides all metadata. Inventory and deliberately handle names, paths, sizes, types, timestamps, recipient/key identifiers, access patterns, timing, logs, caches, temporary files, backups, and error behavior.
- Never select a cryptographic dependency solely because it is popular, fast, or has many GitHub stars. Stars are a minimum supply-chain signal, not evidence of correctness, audit quality, or suitability.
- Never make a cryptographic or post-quantum choice from memory when current standards, library releases, advisories, or protocol requirements can be checked.

## Workflow

1. Define the threat model and the security goal before choosing an algorithm. Identify the data and metadata assets, confidentiality/integrity/authenticity requirements, offline password-guessing risk, replay or rollback risk, key compromise and recovery assumptions, active and passive attackers, trust boundaries, availability/resource limits, interoperability or FIPS requirements, and whether a future quantum attacker is actually in scope.
2. Identify what must be secret, what may be public but authenticated, what must be unlinkable, and what may be visible for operational reasons. Write down the format version, key ownership, key lifecycle, rotation/revocation, recovery, downgrade policy, and migration plan before implementing a new format.
3. Search the current repository, lockfiles, callers, tests, protocol specifications, and existing helpers. Reuse an existing vetted abstraction at the owning boundary. Do not add a parallel crypto wrapper when the project already has a correct shared path.
4. Select a maintained primitive or complete format using the guidance below. Check current upstream documentation, release notes, advisories, compatibility, and target-platform support before coding.
5. Implement with typed byte-oriented APIs, explicit context binding, bounded inputs, fail-closed errors, and no secret-dependent observables. Keep the smallest possible cryptographic boundary and document non-obvious choices and remaining exposure.
6. Validate with known-answer vectors and adversarial negative tests, then run the repository’s focused checks. Review the final diff, dependency and lockfile changes, generated output, logs, and error paths for secret or metadata leakage.
7. Report the threat model, selected primitives and versions, library provenance and current-star check, randomness source, nonce/key lifecycle, metadata exposure, tests run, compatibility constraints, and residual risks. State uncertainty instead of calling an unverified design secure.

## Library and dependency gate

For every new cryptographic, hashing, password, randomness, serialization, or key-management dependency:

- Prefer a high-level library from an established ecosystem or the protocol’s reference/official implementation. Prefer an API that makes misuse difficult, generates or validates nonces correctly, authenticates associated data, uses constant-time verification, and exposes clear failure states.
- Verify the exact package name, upstream repository, license, source distribution, release history, maintenance activity, security advisories, audit history, unsafe/native boundaries, transitive dependencies, and supported platform/toolchain versions. Check the package contents when supply-chain risk matters; do not trust a similarly named package.
- Enforce the project policy: verify the upstream GitHub repository has at least 100 stars before adding it, prefer more than 500, and ask the user before using a dependency below 100 stars or one whose repository or star count cannot be verified. Treat stars only as a floor; strong maintenance, expert stewardship, sound APIs, published specifications, and security history matter more.
- Check the latest stable compatible release at the package registry and upstream release page at the time of the change. Do not pin a stale version from memory, a moving branch, an unreviewed git revision, or a nightly release merely because it is newer. Review breaking changes, minimum supported versions, advisories, reproducibility, and the lockfile before upgrading. “Latest” means the latest suitable stable release, not an incompatible major version forced into the project.
- For Rust, verify the crate’s current crates.io release and repository, inspect `Cargo.lock` and `cargo tree`, use `cargo metadata --locked`, and run the repository’s format, lint, test, and advisory checks when configured. Prefer the crate’s high-level API and its documented feature set over enabling broad or unusual features.
- For Nix, use the repository’s pinned source and normal flake lock workflow. Prefer an official immutable release tag or an exact justified commit over a moving branch, and keep the lock entry reviewable.
- Do not replace an existing dependency solely because its star count is lower. Apply the threshold to proposed additions, then assess whether a migration has a concrete security or maintenance benefit.

## Primitive and format selection

Choose by security goal and protocol constraints, not by a generic “strongest algorithm” ranking.

| Goal | Default direction | Do not do |
| --- | --- | --- |
| Password storage | Argon2id with a unique random salt and tuned memory/time/parallelism; use a standard encoded representation and rehash when policy increases | Store plaintext or reversibly encrypt passwords; use BLAKE3, SHA-2, MD5, or another fast hash alone |
| Password-derived encryption key | Argon2id (or scrypt when required), with a unique salt and parameters recorded with the ciphertext; add a separately protected pepper only when the threat model justifies its operational cost | Treat a password as a uniformly random key; use a fast hash once; confuse a password salt with a secret |
| General unkeyed hash | Prefer BLAKE3 for new general-purpose hashing when interoperability, regulatory validation, and protocol requirements permit it; use SHA-256/SHA-512/SHA-3 when a standard, FIPS validation, ecosystem, or wire format requires them | Use MD5 or SHA-1 for new security decisions; assume any hash gives authenticity against an attacker |
| Authenticity of data | Use a MAC such as HMAC or a specified keyed BLAKE3 mode, or use a digital signature when verification must not require a shared secret | Compare raw hashes for authenticity; concatenate a key and message into an ad hoc hash; use a non-constant-time secret comparison |
| General KDF | Use a specified HKDF or BLAKE3 derive-key mode with independent context/domain labels; use Argon2id for password inputs | Invent `hash(key || context)` constructions or reuse one derived key for unrelated purposes |
| Symmetric encryption | Use an AEAD such as AES-GCM where its nonce and deployment requirements are satisfied, or XChaCha20-Poly1305 where a long random nonce and a misuse-resistant API are useful; follow the selected library’s limits | Use ECB, unauthenticated CBC/CTR/stream encryption, homemade encrypt-then-MAC, or a raw block cipher API without a reviewed protocol |
| File encryption | Prefer a maintained, documented format such as age when its recipient, passphrase, streaming, interoperability, and metadata behavior fit; otherwise use a reviewed streaming AEAD format | Invent a file header, recipient wrapping scheme, chunk nonce scheme, or passphrase format casually |
| Key agreement / public-key encryption | Use a specified protocol/library such as HPKE or X25519-based wrapping, or RSA-OAEP only where compatibility requires it; bind the transcript and context | Use raw Diffie-Hellman, raw RSA, unauthenticated public keys, or an unreviewed hybrid composition |
| Signatures | Use a maintained implementation of the algorithm required by the protocol, commonly Ed25519 for suitable modern non-FIPS uses or RSA-PSS/ECDSA where required; authenticate the verification key and context | Sign ambiguous bytes, reuse signing keys for other roles, use RSA PKCS#1 v1.5 for new designs, or invent signature encoding |

BLAKE3 is the current BLAKE-family choice for general-purpose hashing, and its design also defines keyed, MAC, KDF, and XOF modes. “Latest BLAKE” refers to the implementation release rather than a promise that BLAKE3 fits every protocol. Do not force BLAKE3 into password hashing, FIPS-bound interfaces, standardized HKDF/HMAC fields, or interoperability boundaries merely because it is fast. A plain hash detects accidental changes; use a MAC or signature when an attacker can modify and recompute the hash.

Argon2id is a memory-hard password hashing and password-to-key derivation function, not a bulk encryption cipher. Start from current OWASP and RFC 9106 guidance, benchmark on the actual deployment, account for concurrent login/resource-exhaustion attacks, and store parameters for future upgrades. OWASP’s current baseline is 19 MiB, two iterations, and one lane; RFC 9106 gives stronger 2 GiB/one-pass and constrained 64 MiB/three-pass recommendations. These are starting points, not universal constants.

Age is a modern file-encryption tool, format, and library. It is not an encryption algorithm. Use the complete format rather than copying selected primitives from its specification. Inspect its visible header/recipient and size behavior for the privacy goal; current age releases also have optional hybrid post-quantum recipient support, so do not assume every age file has the same cryptographic or metadata profile.

## Randomness, keys, salts, and nonces

- Obtain security-sensitive bytes from the operating system’s cryptographically secure random facility through a maintained library: for example `getrandom`/`OsRng` on Rust targets, Web Crypto in browsers, `crypto.randomBytes` in Node.js, `secrets` in Python, or the platform secure API. Verify the chosen API’s backend for the actual target, especially early boot, embedded, WASM, and virtualized environments.
- A CSPRNG seeded from trusted OS entropy is the normal secure design. Do not require direct “true random” hardware when the platform CSPRNG is the supported, well-reviewed interface. Use hardware entropy only through a trusted OS/library integration unless the platform and threat model require a separately reviewed design.
- Check and propagate randomness-source errors. Never silently fall back to a timestamp, counter, process state, ordinary PRNG, user timing, keyboard mashing, or a weaker API. Refuse to generate keys, wallet seeds, salts, tokens, or nonces if secure randomness is unavailable.
- Generate independent random keys and salts. Salts are normally public and unique; keys and peppers are secret. Use the library’s standard encoded password format so salt and cost parameters travel with the verifier.
- Keep a clear key hierarchy: separate data-encryption keys, key-encryption/wrapping keys, signing keys, authentication keys, and derivation contexts. Bind derived keys to a purpose, protocol version, tenant/object identity, and direction where applicable. Plan rotation, revocation, compromise response, backup, and recovery before storing ciphertext.
- Use a fresh, library-generated nonce/IV for every encryption under a key, or use a carefully designed persistent counter when the format requires it. Never reuse a `(key, nonce)` pair; account for retries, concurrent workers, process forks, crashes, resumable uploads, and restored snapshots. A nonce can be public but may need uniqueness or unpredictability depending on the primitive.
- Treat extended nonces as easier nonce management, not as nonce-reuse resistance: XChaCha20-Poly1305 and AES-GCM still require the selected library’s nonce rules to be obeyed.
- Use deterministic randomness only in tests and published test vectors, with obvious test-only boundaries. Never seed a production CSPRNG with a fixture, and never make production key generation reproducible for convenience.
- Treat zeroization and memory locking as defense in depth, not proof that a secret has no copies. Avoid converting secret bytes to immutable strings, logging them, interpolating them into shell commands, or leaving them in long-lived caches.

## Passwords and brute-force resistance

- Hash passwords for verification; encrypt only data that must later be recovered. Use Argon2id with a unique salt, calibrated memory/time/parallelism, an explicit maximum resource budget, and a standard encoding that records parameters. Rehash on successful authentication when the stored parameters are below policy.
- Keep the password pepper, if used, outside the password database in a secret manager/HSM or equivalent protected boundary. Treat a pepper as a key with rotation and recovery consequences; do not add one as a substitute for salts, strong passwords, rate limits, MFA, or access control.
- Preserve password bytes according to the protocol’s documented encoding and normalization rules. Do not silently truncate, normalize, or pre-hash passwords unless the selected password scheme explicitly requires and specifies it.
- Make online verification resistant to abuse: rate-limit and monitor attempts, cap concurrent expensive derivations, bound encoded parameter values before allocation, and avoid letting attacker-controlled parameters create a denial of service.
- Do not call a fast hash “brute-force resistant.” Memory hardness belongs at the password boundary; randomly generated high-entropy keys already resist guessing differently and should not be run through Argon2id as a substitute for key management.

## AEAD, protocol framing, and side channels

- Authenticate every value that affects interpretation: version, algorithm/format identifier, object or tenant binding, recipient context, chunk ordering, and relevant metadata. Put only intentionally public values into associated data because AAD is authenticated but not encrypted.
- Treat authentication failure, malformed framing, truncated input, wrong key, wrong recipient, and unsupported version as safe failures with no partial plaintext publication. Avoid distinguishable padding, parsing, or key-selection errors that create an oracle.
- Define canonical encoding, field lengths, maximum sizes, chunk limits, and algorithm negotiation. Authenticate the negotiated result and reject downgrade or unknown-version paths unless an explicit migration policy allows them.
- Use constant-time library comparisons for tags, MACs, password verifiers, and secret identifiers. Avoid secret-dependent branches, indexing, allocation sizes, memory access, and early-return timing in cryptographic paths. Let a mature primitive library handle low-level arithmetic and validation.
- Do not log plaintext, keys, passwords, tokens, nonces when they are sensitive in context, recipient lists, decrypted filenames, raw authentication failures, or full cryptographic error details. Use redacted identifiers and generic external errors while retaining narrowly scoped internal diagnostics.
- For signatures and public-key systems, authenticate or pin the verification key through the application’s trust model. Encryption to an attacker-controlled public key can be perfectly implemented and still fail the application’s security goal.

## Metadata and privacy

Encryption normally protects plaintext, not the surrounding record. Before choosing a format, enumerate whether an observer can learn:

- names, paths, extensions, MIME types, tags, thumbnails, and directory structure;
- plaintext and ciphertext lengths, chunk counts, padding, timestamps, versions, key IDs, recipient identifiers, and object linkage;
- who accesses an object, when, how often, from where, and whether two records are related; and
- data in logs, filenames, temporary files, caches, crash dumps, swap, backups, URLs, metrics, and error messages.

When hiding a field is part of the goal, encrypt filenames and manifests inside the authenticated envelope, use opaque random storage IDs, keep sensitive values out of operational paths and logs, and consider padding, fixed-size chunks, batching, access-control changes, or traffic shaping where the threat model justifies the cost. Authenticate visible metadata as AAD when it must remain visible, but remember that AAD is not secret. Record residual leakage explicitly: encryption alone generally does not hide size, timing, access pattern, or the existence of a record.

Do not promise “zero metadata exposure” unless the complete storage, transport, index, backup, and operational design actually provides it. Avoid adding padding or traffic-shaping complexity without a concrete leakage target and tests that demonstrate the intended bound.

## Testing and review checklist

Require more than a successful encrypt/decrypt round trip. Add or inspect:

- known-answer vectors from the selected standard/library and, where applicable, C2SP Wycheproof vectors;
- tampered ciphertext, tag, nonce, AAD, header, version, recipient stanza, key ID, chunk order, and final-chunk cases;
- wrong key/password/recipient, truncated or oversized input, malformed encodings, duplicate nonce attempts, replay/rollback, algorithm downgrade, and unsupported-version cases;
- salt uniqueness, password-parameter parsing and upgrade behavior, resource/concurrency limits, crash/retry/resume behavior, and randomness-source failure behavior;
- property tests or fuzzing for parsers, framing, decryptors, and key/parameter boundaries; and
- checks that secrets, plaintext, filenames, recipient data, and sensitive metadata do not appear in logs, errors, paths, temporary artifacts, test snapshots, or generated configuration.

Inspect the diff and dependency tree for accidental crypto rewrites, stale or duplicate implementations, unreviewed feature flags, hard-coded material, legacy compatibility paths, and lockfile drift. Run the project’s narrowest meaningful formatter, linter, type/build, test, and advisory checks. Do not claim a library or algorithm is audited merely because the local tests pass.

## Stop and ask the user

Pause before implementation when the threat model, metadata goal, key custody, recovery semantics, compliance boundary, interoperability requirement, or acceptable resource budget is materially unclear. Also pause when the only candidate dependency is below 100 GitHub stars or its provenance cannot be verified, when a proposed design requires a custom primitive/protocol, when a migration would invalidate existing ciphertext, or when a post-quantum choice would change the wire format or deployment boundary.

## Post-quantum cryptography

Do not add post-quantum algorithms merely because they sound stronger. For ordinary applications, use a mature classical design that fits the current protocol and library ecosystem. If the threat model includes harvest-now-decrypt-later risk, long-lived confidentiality, or a stated PQ requirement, use current standardized algorithms and an established, interoperable implementation; NIST finalized ML-KEM (FIPS 203), ML-DSA (FIPS 204), and SLH-DSA (FIPS 205) in 2024. Consider a documented hybrid only when the protocol and library define its composition and downgrade behavior. Do not invent a hybrid, silently mix independent shared secrets, or label an unreviewed implementation quantum-safe.

## Authoritative references

Consult the relevant current source rather than relying on this list as a permanent version record. The following sources informed this skill on 2026-08-19:

- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) and [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html): threat modeling, custom-algorithm prohibition, AEAD, CSPRNGs, key management, Argon2id, salts, peppers, and work factors.
- [RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html): Argon2 specification and parameter recommendations.
- [RFC 5869](https://www.rfc-editor.org/rfc/rfc5869.html) and [RFC 9180](https://www.rfc-editor.org/rfc/rfc9180.html): HKDF and HPKE specifications.
- [BLAKE3 upstream design and implementation](https://github.com/BLAKE3-team/BLAKE3): current BLAKE3 capabilities and security claims.
- [age upstream project](https://github.com/FiloSottile/age), [age format specification](https://age-encryption.org/v1): complete file-encryption format, streaming behavior, and current optional PQ recipient support.
- [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), and [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final): finalized PQ standards.
- [Rust `getrandom` documentation](https://docs.rs/getrandom/latest/getrandom/): operating-system randomness sources and target-specific caveats.
- [C2SP Wycheproof](https://github.com/C2SP/wycheproof): implementation-agnostic vectors for known attacks and edge cases.
