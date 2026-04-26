param(
    [int]$Days = 5,
    [int]$IntervalSeconds = 300
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ExportMetrics = Join-Path $PSScriptRoot "export_metrics.ps1"
$BackupLogs = Join-Path $PSScriptRoot "backup_logs.ps1"
$LogDir = Join-Path $RepoRoot "logs\metrics"
$LogFile = Join-Path $LogDir "autosave.log"
$PidFile = Join-Path $LogDir "pid.txt"
$EndAt = (Get-Date).AddDays($Days)

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
Set-Content -LiteralPath $PidFile -Value $PID -Encoding ASCII

function Write-AutosaveLog {
    param([Parameter(Mandatory = $true)][string]$Message)

    $line = "[{0}] {1}" -f (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"), $Message
    Write-Host $line
    Add-Content -LiteralPath $LogFile -Value $line -Encoding UTF8
}

Write-AutosaveLog "Metrics autosave started; end at $($EndAt.ToString('s')) local time; PID $PID."

while ((Get-Date) -lt $EndAt) {
    try {
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ExportMetrics | ForEach-Object {
            Write-AutosaveLog $_
        }
        Write-AutosaveLog "Saved results/metrics.json and results/h1_table.md."
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $BackupLogs | ForEach-Object {
            Write-AutosaveLog $_
        }
        Write-AutosaveLog "Saved logs snapshot."
    }
    catch {
        Write-AutosaveLog "Metrics autosave failed: $($_.Exception.Message)"
    }

    Start-Sleep -Seconds $IntervalSeconds
}

Write-AutosaveLog "Metrics autosave reached $Days day limit."
