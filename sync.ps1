param(
    [string]$Message = "Sync global agent skills"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$source = Join-Path $env:USERPROFILE ".agents\skills"
$target = Join-Path $repoRoot "skills"

if (-not (Test-Path -LiteralPath $source)) {
    throw "Missing global skills directory: $source"
}

if (-not (Test-Path -LiteralPath (Join-Path $repoRoot ".git"))) {
    throw "This script must live in a git repository."
}

Push-Location $repoRoot
try {
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }

    New-Item -ItemType Directory -Path $target -Force | Out-Null
    Get-ChildItem -LiteralPath $source -Directory | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $target $_.Name) -Recurse -Force
    }

    git add skills

    $changes = git status --porcelain
    if (-not $changes) {
        Write-Host "No skill changes to sync."
        return
    }

    git commit -m $Message
    git push
}
finally {
    Pop-Location
}
