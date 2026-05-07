#!/usr/bin/env bash
set -euo pipefail

message="${1:-Sync global agent skills}"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$HOME/.agents/skills"
target_dir="$repo_root/skills"

if [[ ! -d "$source_dir" ]]; then
  echo "Missing global skills directory: $source_dir" >&2
  exit 1
fi

if [[ ! -d "$repo_root/.git" ]]; then
  echo "This script must live in a git repository." >&2
  exit 1
fi

cd "$repo_root"

rm -rf "$target_dir"
mkdir -p "$target_dir"

find "$source_dir" -mindepth 1 -maxdepth 1 -type d | while IFS= read -r skill_dir; do
  cp -R "$skill_dir" "$target_dir/$(basename "$skill_dir")"
done

git add skills

if [[ -z "$(git status --porcelain)" ]]; then
  echo "No skill changes to sync."
  exit 0
fi

git commit -m "$message"
git push
