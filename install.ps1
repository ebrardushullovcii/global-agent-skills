param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$source = Join-Path $repoRoot "skills"
$target = Join-Path $env:USERPROFILE ".agents\skills"

if (-not (Test-Path -LiteralPath $source)) {
    throw "Missing skills directory: $source"
}

New-Item -ItemType Directory -Path $target -Force | Out-Null

Get-ChildItem -LiteralPath $source -Directory | ForEach-Object {
    $destination = Join-Path $target $_.Name

    if ((Test-Path -LiteralPath $destination) -and -not $Force) {
        Write-Host "Skipping existing skill: $($_.Name)"
        return
    }

    if (Test-Path -LiteralPath $destination) {
        Remove-Item -LiteralPath $destination -Recurse -Force
    }

    Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse -Force
    Write-Host "Installed skill: $($_.Name)"
}
