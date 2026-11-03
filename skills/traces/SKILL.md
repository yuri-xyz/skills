---
name: traces
description: Use when the user refers to an earlier conversation, session, thread, trace, transcript, prompt, or agent run, or asks what was said or done before.
---

# Traces

## Objective

The user is talking about AI coding agent sessions: earlier conversations,
another agent's run, a prompt they typed last week, a decision or error that
came up before. The answer lives in local trace files. Find the right session
quickly with targeted searches, read only the relevant parts, and report what
the traces actually show.

Search the agent the user names. Otherwise search every agent whose trace
directory exists, starting with the one that has the most recent activity.

## Where the traces are

### Claude Code (`~/.claude`)

- `history.jsonl`: every prompt the user typed, across all projects, one JSON
  object per line: `display` (the prompt text), `project` (cwd),
  `sessionId`, `timestamp` (epoch **milliseconds**). It's the fastest index
  for "when did I ask about X" and for mapping a prompt to a session.
- `projects/<slug>/<sessionId>.jsonl`: full session transcripts. `<slug>`
  is the session's working directory with every non-alphanumeric character
  replaced by `-`, e.g. `/srv/app` →
  `-srv-app`, `/tmp/.tmpX` → `-tmp--tmpX`.
- `projects/<slug>/<sessionId>/tool-results/`: large tool outputs spilled
  out of the transcript.
- `projects/<slug>/memory/`: per-project auto-memory files.
- `plans/*.md`: saved plan-mode plans.
- `file-history/<sessionId>/`: snapshots of files edited in a session.

Transcript lines carry a `type`. The ones that matter:

- `user`: `.message.content` is a **string** for typed prompts, or an array
  of `tool_result` blocks for tool output.
- `assistant`: `.message.content[]` blocks of type `text`, `thinking`, or
  `tool_use` (`.name`, `.input`).
- `ai-title`: `.aiTitle`, a short generated session title, possibly
  repeated as it updates; the last one wins.
- `attachment`, `system`: injected context, hook output, reminders.

Every `user`/`assistant` line also has `cwd`, `gitBranch`, `timestamp` (ISO),
`sessionId`, and `uuid`/`parentUuid`. Other types (`api-request*`,
`file-history-*`, `mode`, …) are internal bookkeeping; skip them.

### Codex (`~/.codex`)

- `history.jsonl`: typed prompts: `session_id`, `ts` (epoch **seconds**),
  `text`.
- `session_index.jsonl`: `id`, `thread_name`, `updated_at` per thread.
- `sessions/YYYY/MM/DD/rollout-<timestamp>-<id>.jsonl`: transcripts. Lines
  have `type` `session_meta` (`.payload.cwd`, `.payload.id`), `turn_context`,
  `event_msg`, and `response_item`, where `.payload.type == "message"`
  carries `.payload.role` and `.payload.content[].text`. User-role messages
  also contain injected `AGENTS.md` and `<environment_context>` blocks.
- `*.sqlite` files hold newer thread history and state. Read them only if the
  JSONL files lack what you need. `sqlite3` may be missing; run it
  through a temporary tool install if so, and always open read-only (`-readonly`).

## Search strategy

Narrow before you read. Transcripts are large and full of injected context,
so never `cat` one whole.

1. **Pin down what the user means.** Pull out distinctive terms: file names,
   commands, error strings, skill names, project names, rough dates ("last
   week", "yesterday" are relative to today). If the user means "this
   repo", restrict to its slug directory.
2. **Search the prompt index first.** It's small and maps straight to
   session IDs:

   ```bash
   rg -i 'term' ~/.claude/history.jsonl \
     | jq -r '[(.timestamp/1000|floor|todate), .project, .sessionId,
               (.display|gsub("\n";" ")|.[:120])] | @tsv'
   ```

3. **Search transcripts** when the term came from the agent side (an
   error, a file it edited, a decision it made):

   ```bash
   rg -l -i --glob '*.jsonl' 'term' ~/.claude/projects/<slug> \
     | xargs -r ls -t | head
   ```

   Drop `<slug>` to search every project. Use `rg -c` to rank sessions by
   hit count, and combine terms (`rg -l a | xargs rg -l b`) to intersect.
   JSON escapes quotes, newlines and backslashes, so search for short
   fragments that contain none of them, or use a regex such as
   `'cargo.{0,40}error'`.
4. **List candidate sessions by title** to confirm you have the right one:

   ```bash
   for f in $(ls -t ~/.claude/projects/<slug>/*.jsonl | head -10); do
     printf '%s  %s\n' "$(basename "$f" .jsonl)" \
       "$(jq -r 'select(.type=="ai-title") | .aiTitle' "$f" | tail -1)"
   done
   ```

5. **Read only the conversation**, not the bookkeeping:

   ```bash
   jq -r 'if .type=="user" and (.message.content|type)=="string"
            then "USER: " + .message.content
          elif .type=="assistant"
            then (.message.content[]? | select(.type=="text") | "ASSISTANT: " + .text)
          else empty end' <session>.jsonl
   ```

   Add tool calls with `select(.type=="tool_use") | "TOOL \(.name): \(.input|tostring|.[:200])"`
   when you need to know what the agent actually ran or edited. Pipe into
   `rg -n -C3 'term'` or `sed -n` to jump to the relevant part.

6. **Codex equivalents:**

   ```bash
   rg -i 'term' ~/.codex/history.jsonl \
     | jq -r '[(.ts|todate), .session_id, (.text|gsub("\n";" ")|.[:120])] | @tsv'
   rg -i 'term' ~/.codex/session_index.jsonl
   fd '<id>' ~/.codex/sessions        # rollout file for a session id
   jq -r 'select(.type=="response_item" and .payload.type=="message"
                 and (.payload.role=="user" or .payload.role=="assistant"))
          | .payload.role as $r | .payload.content[]? | .text // empty
          | select(startswith("<") or startswith("# AGENTS.md") | not)
          | "\($r|ascii_upcase): \(.)"' <rollout>.jsonl
   ```

## Pitfalls

- **The current session is a trace too.** The newest transcript in the
  project's slug directory is usually the conversation you are in, and it
  matches whatever you just searched for. Exclude it unless the user means
  this session.
- **Injected context is noisy.** System reminders, `CLAUDE.md`/`AGENTS.md`
  contents, and skill listings repeat in almost every session and match
  common terms. Prefer distinctive terms, and confirm a hit sits in a real
  user prompt or assistant reply.
- **Resumed and compacted sessions** can continue in a new `sessionId`;
  follow up across neighboring sessions in the same project by time.
- **Timestamps differ:** Claude `history.jsonl` uses milliseconds, Codex
  uses seconds, transcripts use ISO strings in UTC.

## Privacy and safety

- Traces are read-only evidence. Never edit, delete, rewrite, or "clean up"
  trace files, histories, or databases.
- Never read credential files such as `~/.claude/.credentials.json` or
  `~/.codex/auth.json`. Traces themselves may contain secrets pasted into
  prompts or printed by tools; don't repeat those back, quote them in files,
  or send them anywhere.
- Quote only the excerpts needed to answer, and cite the session (ID, project,
  date) so the user can verify it.

## Reporting

Answer the user's actual question with what the traces show: what was asked,
decided, run, or changed, and when. Name the session(s) you used. If nothing
matched, say which locations and terms you searched rather than guessing at
what happened.
