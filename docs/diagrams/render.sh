#!/usr/bin/env bash
# Render the README flow diagrams from build.py with text converted to paths,
# because GitHub loads no external fonts in README images.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

mapfile -t fonts < <(nix build --no-link --print-out-paths nixpkgs#jetbrains-mono)
{
  echo '<?xml version="1.0"?><fontconfig>'
  printf '<dir>%s/share/fonts</dir>\n' "${fonts[@]}"
  echo '</fontconfig>'
} >"$work/fonts.conf"

nix run nixpkgs#python3 -- -I build.py "$work"

for src in "$work"/*.src.svg; do
  name=$(basename "$src" .src.svg)
  FONTCONFIG_FILE=$work/fonts.conf nix run nixpkgs#inkscape -- \
    --export-text-to-path --export-plain-svg --export-filename="$name.svg" "$src"
done
nix run nixpkgs#svgo -- --multipass ./*.svg
