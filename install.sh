#!/usr/bin/env bash
# install.sh — copy skills from this repo into ~/.claude/skills/
#
# Usage:
#   ./install.sh <skill-name>          install one skill
#   ./install.sh --all                 install every skill in skills/
#   ./install.sh --uninstall <name>    remove a skill
#   ./install.sh --list                list available skills in this repo

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DST="$HOME/.claude/skills"

color_red()   { printf '\033[31m%s\033[0m' "$1"; }
color_green() { printf '\033[32m%s\033[0m' "$1"; }
color_dim()   { printf '\033[2m%s\033[0m' "$1"; }

usage() {
  cat <<EOF
Install Claude Code skills from this repo.

Usage:
  $0 <skill-name>           install one skill
  $0 --all                  install every skill in $SKILLS_SRC
  $0 --uninstall <name>     remove a skill from $SKILLS_DST
  $0 --list                 show what's available in this repo

Skills are copied to: $SKILLS_DST/<name>/
EOF
}

ensure_dst() {
  mkdir -p "$SKILLS_DST"
}

list_skills() {
  if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "No skills/ directory found at $SKILLS_SRC"
    exit 1
  fi
  echo "Available skills:"
  for dir in "$SKILLS_SRC"/*/; do
    [[ -d "$dir" ]] || continue
    name=$(basename "$dir")
    desc=""
    if [[ -f "$dir/SKILL.md" ]]; then
      desc=$(awk '/^description:/ {sub(/^description: */,""); print; exit}' "$dir/SKILL.md")
    fi
    printf "  %s  %s\n" "$(color_green "$name")" "$(color_dim "${desc:-(no description)}")"
  done
}

install_one() {
  local name="$1"
  local src="$SKILLS_SRC/$name"
  local dst="$SKILLS_DST/$name"

  if [[ ! -d "$src" ]]; then
    echo "$(color_red "Error:") skill '$name' not found in $SKILLS_SRC"
    echo "Run '$0 --list' to see available skills."
    exit 1
  fi

  ensure_dst

  if [[ -d "$dst" ]]; then
    echo "$(color_dim "Updating") $name (overwriting $dst)"
    rm -rf "$dst"
  else
    echo "$(color_green "Installing") $name to $dst"
  fi

  cp -R "$src" "$dst"
  # Strip junk that may have slipped in
  find "$dst" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
  find "$dst" -name "*.pyc" -delete 2>/dev/null || true
  find "$dst" -name ".DS_Store" -delete 2>/dev/null || true

  echo "  $(color_green "✓") installed"
}

install_all() {
  if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "No skills/ directory found"
    exit 1
  fi
  for dir in "$SKILLS_SRC"/*/; do
    [[ -d "$dir" ]] || continue
    install_one "$(basename "$dir")"
  done
}

uninstall_one() {
  local name="$1"
  local dst="$SKILLS_DST/$name"
  if [[ ! -d "$dst" ]]; then
    echo "$(color_dim "Not installed:") $name"
    exit 0
  fi
  rm -rf "$dst"
  echo "$(color_green "✓") removed $dst"
}

main() {
  if [[ $# -eq 0 ]]; then
    usage
    exit 1
  fi

  case "$1" in
    -h|--help)
      usage
      ;;
    --list)
      list_skills
      ;;
    --all)
      install_all
      ;;
    --uninstall)
      if [[ $# -lt 2 ]]; then
        echo "$(color_red "Error:") --uninstall requires a skill name"
        exit 1
      fi
      uninstall_one "$2"
      ;;
    -*)
      echo "$(color_red "Error:") unknown flag '$1'"
      usage
      exit 1
      ;;
    *)
      install_one "$1"
      ;;
  esac

  echo
  echo "$(color_dim "Skills load on the next Claude Code session. Restart any running session to pick them up.")"
}

main "$@"
