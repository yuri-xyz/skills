---
name: local-create-skill
description: Use when the user asks to create a skill that belongs to the current project rather than the global skill set.
disable-model-invocation: true
---

# Local Create Skill

## Objective

Turn the user's description into a skill that only applies to the project
being worked on. Store it inside that project's repository so Claude Code
and Codex discover it there, and make sure git tracks it. Do not add it to the
global skill set, such as the user-level Claude Code or Codex skill directories.

## Location

Follow the project's existing convention when it already has local skills,
for example a populated `.claude/skills` or `.agents/skills` directory, or a
canonical source that those directories link to. Otherwise:

- Write the canonical skill to `.agents/skills/<name>/SKILL.md`. Codex
  discovers project skills there.
- Add a relative symlink `.claude/skills/<name>` pointing to
  `../../.agents/skills/<name>` so Claude Code discovers the same skill without
  a second copy.

Work from the repository root (`git rev-parse --show-toplevel`), not from a
subdirectory, unless the project is a monorepo and the user asked for the skill
to belong to one package.

## Workflow

1. Read the request and the project context the skill depends on: its
   `AGENTS.md` or `CLAUDE.md`, build and check commands, layout, and the code
   or workflow the skill targets. A project skill should name the project's
   real paths, commands, and conventions rather than generic advice.
2. Check for overlap with existing project and global skills. Extend or
   reference an existing skill instead of duplicating it, and ask the user when
   it is unclear whether the request is a new skill or a change to an existing
   one.
3. Ask concise clarifying questions only when the skill's purpose, trigger, or
   expected output cannot be inferred. Do not invent an objective.
4. Pick a short kebab-case `<name>` that describes the skill's job and does not
   collide with an existing project or global skill.
5. Write `SKILL.md` (see Skill Shape) and, matching the project's other skills
   or the global skill set, an `agents/openai.yaml` with `short_description`
   and `default_prompt`.
6. Add the discovery symlinks from Location, using relative link text so the
   links work in every clone.
7. Make sure git tracks it:
   - Run `git check-ignore -v` on every new path. If a path is ignored, add the
     narrowest unignore rule to the project's `.gitignore`, such as
     `!.claude/skills/`, and confirm it took effect. Never change global or
     user-level ignore files for this.
   - Stage the new files and symlinks with `git add`, then confirm with
     `git ls-files` that each one is tracked and symlinks are stored as links.
   - Do not commit unless the user asked for a commit; then use `/git-commit`.
8. Report the skill name, its paths, the discovery links, and any `.gitignore`
   change.

## Skill Shape

- Frontmatter has only `name`, matching the directory, and `description`,
  except that a skill meant only for the user to start also sets
  `disable-model-invocation: true`, with `policy.allow_implicit_invocation:
  false` in its `agents/openai.yaml`, so neither Claude Code nor Codex loads
  it unasked. Leave both unset on a skill another skill loads as a step,
  because the model cannot load a hidden skill at all.
- Write the `description` as when an agent should use the skill, not as a
  summary of what the skill does. Agents decide from the description alone
  whether to load the skill, so start with "Use when" and name the requests,
  situations, or signals that should trigger it. When a neighboring skill
  covers similar ground, add when not to use it and which skill to use
  instead. Leave the skill's steps, rules, and outputs to the body.
- Do not add display-name metadata such as `interface.display_name`.
- The body starts with a `# Title` and an `## Objective`, followed by the
  sections the job needs, such as scope, workflow steps, rules, and output
  format. Keep it short and imperative, and state the why behind non-obvious
  rules.
- Reference other skills as `/skill-name` instead of restating their content.
- Move long reference material into `references/*.md` files next to
  `SKILL.md`, and helper scripts into `scripts/` with executable bits, only when
  the skill genuinely needs them.
- Keep secrets, machine-specific absolute paths, and personal data out of the
  skill, because it is committed to the project.
