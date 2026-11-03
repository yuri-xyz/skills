{
  description = "Agent skills";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/26.05";

  outputs =
    { self, nixpkgs }:
    let
      inherit (nixpkgs) lib;
      systems = [
        "x86_64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = f: lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      formatter = forAllSystems (pkgs: pkgs.nixfmt);

      # Skills are copied rather than linked, because links into the Nix store
      # break once the store path is garbage-collected.
      apps = forAllSystems (pkgs: {
        default = {
          type = "app";
          program = lib.getExe (
            pkgs.writeShellApplication {
              name = "install-skills";
              runtimeEnv.SKILLS_SRC = lib.fileset.toSource {
                root = ./skills;
                fileset = ./skills;
              };
              text = builtins.readFile ./install.sh;
            }
          );
        };
      });

      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = [
            pkgs.nixfmt
            pkgs.statix
          ];
        };
      });

      checks = forAllSystems (pkgs: {
        nix-format = pkgs.runCommand "nix-format" { nativeBuildInputs = [ pkgs.nixfmt ]; } ''
          nixfmt --check ${./flake.nix}
          touch $out
        '';

        nix-lint = pkgs.runCommand "nix-lint" { nativeBuildInputs = [ pkgs.statix ]; } ''
          statix check ${./flake.nix}
          touch $out
        '';

        # Agents discover skills by frontmatter, so a missing description or a
        # name that differs from its directory silently hides or misroutes a skill.
        skills =
          pkgs.runCommand "skills"
            {
              src = lib.fileset.toSource {
                root = ./.;
                fileset = ./skills;
              };
            }
            ''
              status=0
              for dir in "$src"/skills/*/; do
                skill=$(basename "$dir")
                file="$dir/SKILL.md"
                if [[ ! -f $file ]]; then
                  echo "$skill: missing SKILL.md"
                  status=1
                  continue
                fi
                frontmatter=$(awk 'NR == 1 && $0 != "---" { exit } NR > 1 && $0 == "---" { exit } NR > 1 { print }' "$file")
                name=$(sed -n 's/^name: *//p' <<<"$frontmatter")
                description=$(sed -n 's/^description: *//p' <<<"$frontmatter")
                if [[ $name != "$skill" ]]; then
                  echo "$skill: frontmatter name '$name' does not match directory"
                  status=1
                fi
                if [[ -z $description ]]; then
                  echo "$skill: frontmatter description is missing"
                  status=1
                fi
                # Skills ship on their own, so every `/name` they mention must be a
                # skill in this repository. A `/name` counts as a reference when it
                # starts a word or an inline code span; the allowed names are an
                # agent command, a placeholder, and filesystem or API paths.
                for ref in $(grep -ohP '(?<=^|[\s(]|^`|[\s(]`)/[a-z][a-z0-9-]*(?![A-Za-z0-9/-]|\.[A-Za-z0-9])' "$dir"/SKILL.md $(find "$dir" -name '*.md' -path '*/references/*') | sort -u); do
                  case $ref in
                    /goal | /skill-name | /proc | /sys | /dev | /usr | /bin | /lib | /login | /advisories) continue ;;
                  esac
                  if [[ ! -d $src/skills/''${ref#/} ]]; then
                    echo "$skill: references $ref, which is not a skill in this repository"
                    status=1
                  fi
                done
              done
              [[ $status -eq 0 ]] && touch $out
              exit $status
            '';
      });
    };
}
