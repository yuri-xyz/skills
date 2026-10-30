# Cryptography bug classes

Walk the cryptographic boundary through each class that applies. For each,
ask who the attacker is, what they can observe or control, and what they
gain. `/cryptography` holds the recommended primitives and parameters.

## Wrong tool for the goal

- Encryption used where authenticity is needed, or a plain hash used as a
  MAC or signature an attacker can recompute.
- A fast hash (SHA-2, BLAKE3, MD5) for passwords; a password used directly as
  a key; Argon2id run over already-random keys.
- Encoding (base64, hex) or obfuscation (XOR with a constant) treated as
  encryption.
- Signing or encrypting when the goal was something else, such as uniqueness
  or unlinkability.

## Weak, broken, or homemade primitives

- MD5, SHA-1, DES, 3DES, RC4, ECB mode, RSA PKCS#1 v1.5 encryption, or
  small RSA and DH parameters in new code.
- Custom ciphers, MAC constructions such as `hash(key || msg)`, homemade KDFs,
  nonce schemes, padding, or protocol framing.
- Raw primitives (block cipher, raw RSA, raw Diffie-Hellman) where a complete
  format or high-level API exists.

## Authenticated encryption

- Unauthenticated CBC, CTR, or stream ciphers; encrypt-then-MAC done by hand
  with MAC-then-encrypt order, a shared key, or unauthenticated fields.
- Plaintext released before the tag is verified, including streaming
  decryption that emits chunks before the final authentication.
- Fields that change interpretation (version, algorithm, recipient, chunk
  index, final-chunk flag, object ID) left out of the associated data, enabling
  reordering, truncation, or swapping between objects.
- Secret values put into associated data, which is authenticated but not
  encrypted.

## Nonces and IVs

- Reusing a `(key, nonce)` pair: fixed or zero nonces, counters reset on
  restart, fork, retry, crash, restored snapshot, or concurrent workers.
- Random nonces too short for the number of messages under one key, such as
  96-bit random nonces with AES-GCM past its usage limits.
- Predictable IVs where the mode needs unpredictability, as CBC does.
- Exceeding a key's data or message limits without rotation.

## Randomness

- Non-cryptographic generators (`Math.random`, `rand`, `random`, seeded
  PRNGs, UUID v1, time or PID seeds) for keys, salts, nonces, tokens, or IDs
  that must be unguessable.
- Ignored errors from the OS random source, or a silent fallback to a weaker
  source.
- Too little entropy: short tokens, modulo bias when mapping random bytes to a
  range, or truncation that drops most of the randomness.
- Test seeds or fixtures reachable in production.

## Keys and secrets

- Hard-coded keys, salts, peppers, or test secrets in production paths.
- One key reused across purposes (encryption and signing, two tenants, both
  directions) without separate derivation and context labels.
- Keys in logs, error messages, command lines, environment dumps, URLs, crash
  reports, swap-prone long-lived buffers, or immutable strings that cannot be
  wiped.
- Missing rotation, revocation, or compromise handling where the design needs
  them; wrapping keys stored next to the data they protect.

## Verification and comparison

- Ignored verification results: signature or MAC checks whose return value or
  error is dropped, or that return true on an exception.
- Non-constant-time comparison of tags, MACs, password hashes, tokens, or
  secret IDs.
- Secret-dependent branches, table lookups, early returns, or allocation sizes
  in hand-written cryptographic code.
- Signatures over ambiguous encodings: concatenated fields without lengths,
  non-canonical JSON, or partial message coverage.

## Oracles and error handling

- Distinguishable errors or timing for bad padding, bad tag, wrong key,
  unknown recipient, or malformed input, giving an attacker a decryption or
  validity oracle.
- Partial plaintext, decrypted filenames, or internal details in errors and
  logs.
- Failing open: treating an unsupported version, missing signature, or
  verification error as success.

## Protocols, versions, and downgrade

- Algorithm or version chosen from unauthenticated input, including JWT
  `alg: none` and algorithm confusion between HMAC and public-key schemes.
- Missing replay protection: no nonce, timestamp window, or sequence number
  where messages or tokens can be resent.
- Missing rollback protection for encrypted state or update metadata.
- Public keys accepted without authentication or pinning; unvalidated curve
  points or parameters; trust-on-first-use without a stated reason.
- TLS with certificate or hostname verification disabled, outdated protocol
  versions, or custom trust stores that skip checks.

## Passwords

- Missing or reused salts, low or unbounded Argon2id, scrypt, or bcrypt
  parameters, parameters not stored with the hash, and no rehash on upgrade.
- Attacker-controlled cost parameters parsed without bounds, enabling denial
  of service.
- Silent truncation (bcrypt's 72 bytes), normalization, or pre-hashing that
  the scheme does not specify.
- Missing rate limits or concurrency caps on expensive verification.

## Parsing and bounds

- Length fields, chunk counts, and key sizes read from input without bounds;
  integer overflow in size math before allocation or slicing.
- Truncated, oversized, or duplicated fields in headers, recipient stanzas,
  PEM, DER, or JWT parsing; accepting multiple encodings of the same value.
- Off-by-one errors in chunk boundaries, final-chunk detection, or padding
  removal.

## Metadata

- Filenames, sizes, timestamps, key IDs, recipient lists, or access patterns
  left visible where the stated goal is to hide them.
- Plaintext copies in temp files, caches, thumbnails, backups, or indexes
  next to the ciphertext.

## Missing tests

Cryptographic code needs known-answer and Wycheproof vectors where they exist,
and negative tests for tampered ciphertext, tag, nonce, associated data,
header and version, wrong key or recipient, chunk reordering and truncation,
replay, downgrade, oversized and malformed input, and randomness failure.
