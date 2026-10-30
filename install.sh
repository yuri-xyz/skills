#!/usr/bin/env bash
# Copy skills into Claude Code and Codex. Run it from a clone, or piped from
# curl, in which case it downloads the repository first. `nix run` runs this
# same script with SKILLS_SRC pointing at the skills in the Nix store.
set -euo pipefail

archive=https://github.com/yuri-xyz/skills/archive/refs/heads/master.tar.gz
usage="usage: install.sh [skill...]

Copy skills into Claude Code (\${CLAUDE_CONFIG_DIR:-~/.claude}/skills)
and Codex (\${CODEX_HOME:-~/.codex}/skills), for each agent whose
directory exists. With no names, install every skill. Installed
skills with the same names are replaced, except ones that are
links, which are skipped."

# The script's own path, read here because inside a function a piped script
# reports `bash`, which would make a `skills/` in the current directory look
# like a clone. It is empty when piped from curl.
self=${BASH_SOURCE[0]:-}

# Find the skills: the Nix store, the clone this script sits in, or, when piped
# from curl, a fresh download.
find_skills() {
  if [[ -n ${SKILLS_SRC:-} ]]; then
    src=$SKILLS_SRC
  elif [[ -f $self && -d $(dirname "$self")/skills ]]; then
    src=$(cd "$(dirname "$self")" && pwd)/skills
  else
    work=$(mktemp -d)
    trap 'rm -rf "$work"' EXIT
    curl -fsSL "$archive" | tar -xz -C "$work"
    src=$work/skills-master/skills
  fi
}

# Everything runs from main, so a download cut short by `curl | bash` runs
# nothing at all.
main() {
  for arg in "$@"; do
    case $arg in
      -h | --help)
        echo "$usage"
        exit 0
        ;;
      -*)
        echo "install.sh: unknown option $arg" >&2
        exit 2
        ;;
    esac
  done

  find_skills
  skills=()
  for arg in "$@"; do
    if [[ ! -f $src/$arg/SKILL.md ]]; then
      echo "install.sh: no skill named $arg" >&2
      exit 2
    fi
    skills+=("$arg")
  done
  if [[ $# -eq 0 ]]; then
    for dir in "$src"/*/; do
      skills+=("$(basename "$dir")")
    done
  fi

  installed=0
  for home in "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" "${CODEX_HOME:-$HOME/.codex}"; do
    [[ -d $home ]] || continue
    mkdir -p "$home/skills"
    count=0
    for skill in "${skills[@]}"; do
      # A link means the skill is managed elsewhere; leave it be.
      if [[ -L $home/skills/$skill ]]; then
        echo "Skipped $skill: $home/skills/$skill is a link" >&2
        continue
      fi
      rm -rf "${home:?}/skills/$skill"
      cp -R "$src/$skill" "$home/skills/$skill"
      # Copies from the read-only Nix store must stay editable and replaceable.
      chmod -R u+w "$home/skills/$skill"
      count=$((count + 1))
    done
    echo "Installed $count skills into $home/skills"
    installed=1
  done
  if [[ $installed -eq 0 ]]; then
    echo "install.sh: found neither Claude Code nor Codex; create ~/.claude or ~/.codex first" >&2
    exit 1
  fi
}

main "$@"
