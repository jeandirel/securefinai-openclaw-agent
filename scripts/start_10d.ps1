param(
    [int]$Days = 10,
    [string[]]$Labels = @("B3", "B3_LLM")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Runner = Join-Path $PSScriptRoot "run_cell_10d.ps1"

foreach ($label in $Labels) {
    $logDir = Join-Path $RepoRoot "logs\$label"
    $pidFile = Join-Path $logDir "pid.txt"
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null

    if (Test-Path -LiteralPath $pidFile) {
        $oldPidRaw = Get-Content -LiteralPath $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1
        $oldPid = 0
        if ([int]::TryParse($oldPidRaw, [ref]$oldPid)) {
            Stop-Process -Id $oldPid -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 1
        }
    }

    $command = "& '$Runner' -Label '$label' -Days $Days"
    $encodedCommand = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($command))
    $process = Start-Process -FilePath "powershell.exe" `
        -WorkingDirectory $RepoRoot `
        -ArgumentList "-NoExit -NoProfile -ExecutionPolicy Bypass -EncodedCommand $encodedCommand" `
        -PassThru

    Set-Content -LiteralPath $pidFile -Value $process.Id -Encoding ASCII
    Write-Host "Started $label runner PID: $($process.Id)"
    Write-Host "  Logs: $logDir"
    Write-Host "  Stop: Stop-Process -Id $($process.Id)"
}
