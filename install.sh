#!/usr/bin/env bash
set -euo pipefail

force=0
if [[ "${1:-}" == "--force" ]]; then
  force=1
elif [[ "${1:-}" != "" ]]; then
  echo "Usage: ./install.sh [--force]" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$repo_root/skills"
target_dir="$HOME/.agents/skills"

if [[ ! -d "$source_dir" ]]; then
  echo "Missing skills directory: $source_dir" >&2
  exit 1
fi

mkdir -p "$target_dir"

find "$source_dir" -mindepth 1 -maxdepth 1 -type d | while IFS= read -r skill_dir; do
  skill_name="$(basename "$skill_dir")"
  destination="$target_dir/$skill_name"

  if [[ -e "$destination" && "$force" -ne 1 ]]; then
    echo "Skipping existing skill: $skill_name"
    continue
  fi

  if [[ -e "$destination" ]]; then
    rm -rf "$destination"
  fi

  cp -R "$skill_dir" "$destination"
  echo "Installed skill: $skill_name"
done
