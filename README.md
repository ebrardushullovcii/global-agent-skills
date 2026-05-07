# Global Agent Skills

This repository stores global user/agent skills that can be synced across machines.

It intentionally contains only user-managed skills under `skills/`. It does not include bundled Codex system skills or plugin cache skills.

## Global Install Location

Install these skills into the global agent skills directory:

- macOS/Linux: `~/.agents/skills`
- Windows: `%USERPROFILE%\.agents\skills`

Each direct child folder under `skills/` is one installed skill. For example:

```text
~/.agents/skills/frontend-design/SKILL.md
~/.agents/skills/agent-browser/SKILL.md
```

## Restore

Clone the repo, then run the installer for your platform.

### macOS/Linux

```bash
git clone <repo-url>
cd global-agent-skills
./install.sh
```

Use `--force` to overwrite existing installed skill folders:

```bash
./install.sh --force
```

### Windows PowerShell

```powershell
git clone <repo-url>
cd global-agent-skills
.\install.ps1
```

Use `-Force` to overwrite existing installed skill folders:

```powershell
.\install.ps1 -Force
```

## Agent Instructions

If you are an agent installing this repo for a user:

1. Clone the repository.
2. Install every direct child directory under `skills/` into the user's global agent skills directory.
3. Use `~/.agents/skills` on macOS/Linux and `%USERPROFILE%\.agents\skills` on Windows.
4. Preserve each skill folder exactly, including `SKILL.md`, `agents/`, `scripts/`, `references/`, and `assets/` when present.
5. Do not install these into Codex system skill directories such as `~/.codex/skills/.system`.
6. Do not overwrite existing skill folders unless the user explicitly asks for overwrite/force behavior.

The provided `install.sh` and `install.ps1` scripts implement this behavior.
