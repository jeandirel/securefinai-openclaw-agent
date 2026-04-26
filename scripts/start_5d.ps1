param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $RepoRoot

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\start_10d.ps1 -Days 5

$metricsLogDir = Join-Path $RepoRoot "logs\metrics"
$metricsPidFile = Join-Path $metricsLogDir "pid.txt"
New-Item -ItemType Directory -Force -Path $metricsLogDir | Out-Null

if (Test-Path -LiteralPath $metricsPidFile) {
    $oldPidRaw = Get-Content -LiteralPath $metricsPidFile -ErrorAction SilentlyContinue | Select-Object -First 1
    $oldPid = 0
    if ([int]::TryParse($oldPidRaw, [ref]$oldPid)) {
        Stop-Process -Id $oldPid -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
    }
}

$autosave = Join-Path $PSScriptRoot "autosave_metrics.ps1"
$autosaveCommand = "& '$autosave' -Days 5 -IntervalSeconds 300"
$encodedAutosaveCommand = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($autosaveCommand))
$process = Start-Process -FilePath "powershell.exe" `
    -WorkingDirectory $RepoRoot `
    -ArgumentList "-NoExit -NoProfile -ExecutionPolicy Bypass -EncodedCommand $encodedAutosaveCommand" `
    -PassThru

Set-Content -LiteralPath $metricsPidFile -Value $process.Id -Encoding ASCII
Write-Host "Started metrics autosave PID: $($process.Id)"
Write-Host "  Logs: $metricsLogDir"
Write-Host "  Stop: Stop-Process -Id $($process.Id)"
