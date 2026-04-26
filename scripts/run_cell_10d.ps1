param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateNotNullOrEmpty()]
    [string]$Label,

    [int]$Days = 10
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$EnvFile = Join-Path $RepoRoot ".env.$Label"
$LogDir = Join-Path $RepoRoot "logs\$Label"
$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$StdoutLog = Join-Path $LogDir "stdout.log"
$RunnerLog = Join-Path $LogDir "runner.log"
$PidFile = Join-Path $LogDir "pid.txt"
$EndAt = (Get-Date).AddDays($Days)

function Write-RunnerLog {
    param([Parameter(Mandatory = $true)][string]$Message)

    $line = "[{0}] {1}" -f (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"), $Message
    Write-Host $line
    Add-Content -LiteralPath $RunnerLog -Value $line -Encoding UTF8
}

function Remove-InlineComment {
    param([AllowEmptyString()][string]$Value)

    $inSingle = $false
    $inDouble = $false
    for ($i = 0; $i -lt $Value.Length; $i++) {
        $char = $Value[$i]
        if ($char -eq "'" -and -not $inDouble) {
            $inSingle = -not $inSingle
            continue
        }
        if ($char -eq '"' -and -not $inSingle) {
            $inDouble = -not $inDouble
            continue
        }
        if ($char -eq "#" -and -not $inSingle -and -not $inDouble) {
            return $Value.Substring(0, $i)
        }
    }

    return $Value
}

function Import-DotEnv {
    param([Parameter(Mandatory = $true)][string]$Path)

    foreach ($line in Get-Content -LiteralPath $Path) {
        $trimmed = (Remove-InlineComment -Value $line).Trim()
        if ($trimmed.Length -eq 0 -or $trimmed.StartsWith("#")) {
            continue
        }

        $separator = $trimmed.IndexOf("=")
        if ($separator -lt 1) {
            continue
        }

        $name = $trimmed.Substring(0, $separator).Trim()
        $value = $trimmed.Substring($separator + 1).Trim()
        if (($value.StartsWith('"') -and $value.EndsWith('"')) -or
            ($value.StartsWith("'") -and $value.EndsWith("'"))) {
            $value = $value.Substring(1, $value.Length - 2)
        }

        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

if (-not (Test-Path -LiteralPath $EnvFile)) {
    throw "Missing .env.$Label"
}

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Missing venv Python at $Python"
}

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
Set-Content -LiteralPath $PidFile -Value $PID -Encoding ASCII
Set-Location -LiteralPath $RepoRoot
Import-DotEnv -Path $EnvFile
$env:ABLATION_LABEL = $Label
$env:LOG_DIR = $LogDir

Write-RunnerLog "Runner started for $Label; end at $($EndAt.ToString('s')) local time; PID $PID."

while ((Get-Date) -lt $EndAt) {
    Write-RunnerLog "Starting agent process for $Label."
    & $Python -m agent.main 2>&1 | Tee-Object -FilePath $StdoutLog -Append
    $exitCode = $LASTEXITCODE

    if ((Get-Date) -ge $EndAt) {
        break
    }

    Write-RunnerLog "Agent for $Label exited with code $exitCode; restarting in 30 seconds."
    Start-Sleep -Seconds 30
}

Write-RunnerLog "Runner reached $Days day limit for $Label."
