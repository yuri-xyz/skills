---
name: instructions
description: Use when the user must do external steps themselves, such as configuring a website dashboard, settings page, sign-in, or access approval, and needs precise step-by-step instructions; not for teaching the user their own apps unless they asked.
---

# Instructions

## Objective

When the work needs the user to act, hand it over as instructions they can
follow without guessing: exact places, exact actions, what success looks
like, and what to report back. Use this whenever a step needs a person outside
what you can reach, mostly configuring or acting on external apps and
services: a web dashboard, a third-party account or settings page, a sign-in
or 2FA prompt, a DNS or billing change, a hardware action, a purchase, or
approving access.

## Scope

This is a handover of external steps, not a tutorial. Do not walk the user
through using, testing, or operating their own projects, apps, or
configuration, and do not explain how to do work you could do yourself. The
exception is when the conversation is explicitly about that, such as the user
asking how to test a change or how to use something you built; then lay those
steps out in this format.

## Before writing

1. **Keep only what needs the user.** Do every part you can do yourself, such
   as through a CLI, an API, or a file edit, and hand over only the rest. When
   a step could be automated but needs approval, say so and offer that
   instead.
2. **Verify the path.** Third-party interfaces change. When the steps depend
   on a website, app, or tool you have not seen in this session, check its
   current documentation with `/research-web` and use the labels it uses
   today. When you could not verify a label, say so at that step.
3. **Fill in the specifics.** Use the user's actual project, account,
   repository, host, and values in every step instead of placeholders, and
   prepare anything they will paste.

## Format

````markdown
🧑‍🔧 **Your turn: <goal in a few words>**

Why: <one sentence on what this unblocks>.

1. Go to <exact URL, app, or place>.
2. Open **<Section>** → **<Subsection>**.
3. Click **<Button>** and set **<Field>** to `<value>`.
   You should see <what confirms the step worked>.
4. Run:
   ```sh
   <exact command>
   ```

When you're done, send me: <the value, output, or simply "done">.
````

- One action per step, in the order the user meets them. Name every page,
  menu, tab, button, and field exactly as the interface labels it, in bold,
  and put values, paths, and commands in code.
- Add a short "You should see …" check after steps where it is easy to go
  wrong, and say what to do if it looks different.
- Mark choices the user must make at a step, with the option you recommend.
- Warn before any step that costs money, deletes data, changes access, or is
  hard to undo, on that step itself.
- Keep explanation out of the steps; one line of "Why" at the top is enough.
- For several independent tasks, give each its own numbered block.

## Secrets

Never ask the user to paste a password, token, private key, or recovery code
into the conversation. Tell them where to store it instead, such as an
environment variable, a secret store, or a file outside the repository, and
ask only for confirmation that it is in place.

## After the user reports back

Track every step until all of them are done. Each time the user reports
progress, even partial, such as "did 1 and 2" or "done with the DNS part":

1. **Check what you can.** Verify the reported steps yourself when possible,
   such as by running a command, calling an API, or reading a file, and treat
   a step as done only when the check passes or cannot be run.
2. **List what remains.** Reply with the steps still open, in the same format
   under `🧑‍🔧 **Still to do: <goal>**`, keeping their original numbers so the
   user can match them. Precede it with one line naming what is done, such as
   `✅ Done: 1, 2`. Do not repeat finished steps in full.
3. **Fix what went wrong.** When a reported step failed or the check shows it
   is not done, keep it open with corrected wording, starting from where it
   went wrong, and say what you saw.
4. **Carry on.** Continue with your own work as soon as a step it depended on
   is done, without waiting for the rest, and still list what remains.

When nothing remains, say so in one line, such as `✅ All steps done`, and
carry on with the work they unblocked.
