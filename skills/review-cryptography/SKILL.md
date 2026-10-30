---
name: review-cryptography
description: Use when reviewing code changes that touch cryptography, such as encryption, nonces, keys, randomness, secret comparisons, password hashing, or protocol negotiation.
---

# Review Cryptography

## Objective

Review the current or proposed changes to code that encrypts, decrypts,
hashes, signs, verifies, derives keys, stores passwords, generates secrets,
or parses cryptographic formats. Look for misuse that breaks the security
goal while every round-trip test still passes. Find each bug by naming the
attacker, what they observe or control, and what they gain, and prove it with
a failing test, a known-answer or Wycheproof vector, or a specific input
before fixing it.

`/cryptography` owns the standards: threat modeling, primitive and format
selection, the library gate, and parameter guidance. Judge findings against
it instead of restating it. For security holes outside the cryptographic
boundary, use `/review-security`.

## Workflow

1. Inspect the recent diff, pending plan, or relevant files, and map the
   cryptographic boundary: which secrets and keys exist, where they come from,
   which primitives and libraries are used, what is encrypted, authenticated,
   or only hashed, and what crosses to storage or the network.
2. State the security goal the code appears to need: confidentiality,
   integrity, authenticity, password guessing resistance, replay or rollback
   protection, or metadata hiding. When the goal is unclear, report that
   first; most crypto bugs are a mismatch between goal and construction.
3. Walk the boundary through the classes in
   `references/crypto-classes.md`. For each candidate, name the attacker,
   their capability (passive observer, active network attacker, holder of a
   ciphertext, chosen-input or timing access, local reader of logs), and the
   impact: plaintext recovery, forgery, key recovery, offline guessing,
   downgrade, replay, or metadata leak. Drop candidates no attacker can
   exploit.
4. Check the tests: known-answer vectors, tampering and wrong-key cases,
   truncation, malformed and oversized input, unsupported versions, and
   randomness failure, as `/cryptography`'s testing checklist lists. Note the
   missing ones.
5. Fix a bug when it is confirmed, local, and the fix stays inside the
   existing format and library: write a failing test first, fix it, and watch
   it pass. Typical safe fixes are a constant-time comparison, checking an
   ignored verification result, switching to the OS CSPRNG, failing closed on
   authentication failure, or redacting a secret from a log.
6. Report, without fixing, anything that changes the wire or storage format,
   invalidates existing ciphertext, signatures, or password hashes, swaps a
   primitive or library, or needs a key rotation or migration; those are
   human decisions. Report a confirmed key or secret exposure as urgent, with
   rotation as the first step.
7. Run the focused tests and checks for the changed code.

## Avoid

- Inventing or composing primitives while fixing; use the library's
  higher-level API instead, as `/cryptography` requires.
- Upgrading algorithms or parameters without a migration path for existing
  data, or silently accepting the old format forever.
- Calling code secure because tests pass; round trips prove nothing about
  tampering, nonces, or timing.
- Adding a new cryptographic dependency without `/cryptography`'s library
  gate and `/dependency-add`.

## Output

If no bug was found, say so and name the boundary, the stated security goal,
and the classes reviewed.

Otherwise list findings, most severe first:

```markdown
- 🔴 <file:line> <class>: <attacker> with <capability> → <impact>. Fixed; regression test `<name>`.
- 🟡 <file:line> <class>: <attacker> with <capability> → <impact>. Not fixed: <why>.
- 🔵 <file:line> Hardening: <missing defense or test>. Added / not added: <why>.
```

🔴 plaintext or key recovery, forgery, authentication bypass, or exposed
secrets; 🟡 needs unusual access or yields partial information, such as a
timing or metadata leak, weak but not broken parameters, or replay in a narrow
window; 🔵 defense in depth or a missing test. Finish with the checks run, or
why none were, and state that this review is not a substitute for a
professional cryptographic audit when the code guards high-value secrets.
