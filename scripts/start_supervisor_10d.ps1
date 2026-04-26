param(
    [int]$Days = 10,
    [int]$CheckIntervalSeconds = 60
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SupervisorLogDir = Join-Path $RepoRoot "logs\supervisor"
$Supervisor = Join-Path $PSScriptRoot "supervise_10d.ps1"
$PidFile = Join-Path $SupervisorLogDir "pid.txt"
$StdoutLog = Join-Path $SupervisorLogDir "supervisor.stdout.log"
$StderrLog = Join-Path $SupervisorLogDir "supervisor.stderr.log"

New-Item -ItemType Directory -Force -Path $SupervisorLogDir | Out-Null

if (Test-Path -LiteralPath $PidFile) {
    $oldPidRaw = Get-Content -LiteralPath $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
    $oldPid = 0
    if ([int]::TryParse($oldPidRaw, [ref]$oldPid)) {
        $oldProcess = Get-Process -Id $oldPid -ErrorAction SilentlyContinue
        if ($null -ne $oldProcess) {
            throw "Supervisor already appears to be running as PID $oldPid. Stop it with: Stop-Process -Id $oldPid"
        }
    }
}

$supervisorArg = '"' + $Supervisor + '"'
$process = Start-Process -FilePath "powershell.exe" `
    -WorkingDirectory $RepoRoot `
    -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File $supervisorArg -Days $Days -CheckIntervalSeconds $CheckIntervalSeconds" `
    -RedirectStandardOutput $StdoutLog `
    -RedirectStandardError $StderrLog `
    -PassThru

Set-Content -LiteralPath $PidFile -Value $process.Id -Encoding ASCII
Write-Host "Started supervisor PID: $($process.Id)"
Write-Host "  Log: $SupervisorLogDir"
Write-Host "  Stop: Stop-Process -Id $($process.Id)"
