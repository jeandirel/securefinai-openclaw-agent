param(
    [string]$Destination = "results/logs_snapshot"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Source = Join-Path $RepoRoot "logs"
$Dest = Join-Path $RepoRoot $Destination

if (-not (Test-Path -LiteralPath $Source)) {
    throw "Missing logs directory at $Source"
}

New-Item -ItemType Directory -Force -Path $Dest | Out-Null

Copy-Item -LiteralPath (Join-Path $Source "B3") -Destination $Dest -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -LiteralPath (Join-Path $Source "B3_LLM") -Destination $Dest -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -LiteralPath (Join-Path $Source "metrics") -Destination $Dest -Recurse -Force -ErrorAction SilentlyContinue

$manifest = [ordered]@{
    timestamp_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    source = $Source
    destination = $Dest
    files = @(Get-ChildItem -LiteralPath $Dest -Recurse -File | ForEach-Object {
        [ordered]@{
            path = $_.FullName.Substring($Dest.Length).TrimStart("\")
            bytes = $_.Length
            last_write_time = $_.LastWriteTimeUtc.ToString("yyyy-MM-ddTHH:mm:ssZ")
        }
    })
}

$manifestPath = Join-Path $Dest "manifest.json"
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

Write-Host "Backed up logs to $Dest"
Write-Host "Manifest: $manifestPath"
