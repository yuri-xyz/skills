# AGENTS.md

This repository is a collection of general-purpose agent skills. It has no
application code; the skills are Markdown instructions.
`README.md` lists the skills and how to install them.

## Layout

- `skills/<name>/SKILL.md`: one skill per directory. This is the source of truth.
- `skills/<name>/references/*.md`: optional detail the skill loads on demand.
- `skills/<name>/NOTICE`: required attribution when a skill adapts third-party
  material.
- `skills/<name>/agents/openai.yaml`: optional Codex display metadata
  (`interface.short_description`, `interface.default_prompt`). Codex mentions
  skills as `$name`, so the default prompts use `$name` where `SKILL.md` files
  use `/name`.
- `global/AGENTS.md`: generic global agent instructions users copy into their
  own setup. Keep it free of personal details and of tools or skills that do
  not ship here.
- `docs/brand/`: README hero. Edit `hero.src.svg`, then run `render.sh` to
  regenerate `hero.svg` with text converted to paths. Its backdrop comes from
  `docs/diagrams/build.py`, shared with the diagrams.
- `docs/diagrams/`: README flow diagrams. Edit the layouts in `build.py`, then
  run `render.sh` to regenerate the SVGs.
- `flake.nix`: skill installer app, dev shell, formatter, and checks. There is
  no package output.

Some skills describe `.agenda/`, `.spec/`, and `.debug/` workspaces for other
repositories. Do not create them, or other private planning material, in this
repository.

## Writing Skills

- Name the directory in lowercase kebab-case, and set the frontmatter `name` to
  the directory name exactly.
- Start the frontmatter `description` with "Use when ..." and describe when to
  load the skill, not what it does step by step. Agents choose skills from this
  line alone, so make it specific enough to tell sibling skills apart.
- `skills/agenda/SKILL.md` owns the `.agenda` layout, filenames, IDs, statuses,
  and entry shapes. Other `agenda-*` skills reference it with `/agenda` instead
  of restating those rules. Change a shared rule there, once.
- Keep skills self-contained. Refer to other skills as `/skill-name`, and only
  to skills in this repository; describe any other step in plain words instead
  of naming a skill, tool, or file that ships elsewhere.
- Keep instructions machine-independent: no absolute home paths, usernames,
  hostnames, or agent-specific global state. Skills write only inside the
  target repository.
- Keep each `SKILL.md` focused. If one grows unwieldy, split responsibility into
  a separate skill rather than adding sections for unrelated workflows.
- When adding, renaming, or removing a skill, update the skill list in
  `README.md` and any `/name` references in other skills.

## Validation

Run tools inside the dev shell:

```sh
nix develop                   # dev shell with nixfmt and statix
nix fmt                       # format flake.nix with nixfmt
statix check flake.nix
nix flake check --no-build    # evaluate all checks
nix flake check               # also run them: skill frontmatter, Nix format, Nix lint
```

The `skills` check in `flake.nix` fails when a skill directory lacks
`SKILL.md`, when the frontmatter `name` differs from the directory, when the
`description` is missing, or when a skill references a `/name` that is not a
skill in this repository. It scans `SKILL.md` and `references/`, and allows a
short list of non-skill names, such as `/goal` and filesystem paths, in
`flake.nix`. Flakes only see Git-tracked files, so `git add` new
skills before evaluating.

## Nix

- Keep `nixpkgs` pinned to a release tag and update `flake.lock` together with
  it.
- Keep check sources scoped with `lib.fileset` so unrelated edits do not
  invalidate them.
- Add dev shell tools only when a documented workflow here uses them.
