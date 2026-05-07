# Global Agent Skills

This repository mirrors the global user skills from:

```powershell
C:\Users\ebrar\.agents\skills
```

It intentionally excludes Codex system skills from:

```powershell
C:\Users\ebrar\.codex\skills\.system
```

## Restore

From a cloned copy of this repository:

```powershell
.\install.ps1
```

The script copies every folder under `skills\` into:

```powershell
$env:USERPROFILE\.agents\skills
```

Use `-Force` to overwrite existing installed skill folders:

```powershell
.\install.ps1 -Force
```
