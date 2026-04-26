param(
    [int]$Days = 10,
    [int]$CheckIntervalSeconds = 60,
    [string[]]$Labels = @("B3", "B3_LLM")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$EndAt = (Get-Date).AddDays($Days)
$SupervisorLogDir = Join-Path $RepoRoot "logs\supervisor"
$SupervisorLog = Join-Path $SupervisorLogDir "supervisor.log"
$RunLocal = Join-Path $PSScriptRoot "run_local.ps1"

New-Item -ItemType Directory -Force -Path $SupervisorLogDir | Out-Null

function Write-SupervisorLog {
    param([Parameter(Mandatory = $true)][string]$Message)

    $line = "[{0}] {1}" -f (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"), $Message
    Write-Host $line
    Add-Content -LiteralPath $SupervisorLog -Value $line -Encoding UTF8
}

function Get-CellPid {
    param([Parameter(Mandatory = $true)][string]$Label)

    $pidFile = Join-Path $RepoRoot "logs\$Label\pid.txt"
    if (-not (Test-Path -LiteralPath $pidFile)) {
        return 0
    }

    $pidRaw = Get-Content -LiteralPath $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1
    $pidValue = 0
    if ([int]::TryParse($pidRaw, [ref]$pidValue)) {
        return $pidValue
    }

    return 0
}

function Test-CellRunning {
    param([Parameter(Mandatory = $true)][string]$Label)

    $pidValue = Get-CellPid -Label $Label
    if ($pidValue -le 0) {
        return $false
    }

    return $null -ne (Get-Process -Id $pidValue -ErrorAction SilentlyContinue)
}

Write-SupervisorLog "Starting supervisor for labels: $($Labels -join ', '); end at $($EndAt.ToString('s')) local time."

while ((Get-Date) -lt $EndAt) {
    foreach ($label in $Labels) {
        if (Test-CellRunning -Label $label) {
            $pidValue = Get-CellPid -Label $label
            Write-SupervisorLog "$label running as PID $pidValue."
            continue
        }

        Write-SupervisorLog "$label is not running; restarting."
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $RunLocal $label -Restart
    }

    Start-Sleep -Seconds $CheckIntervalSeconds
}

Write-SupervisorLog "Supervisor reached $Days day limit. Leaving running cells untouched."
