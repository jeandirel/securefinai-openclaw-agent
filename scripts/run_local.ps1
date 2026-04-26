param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateNotNullOrEmpty()]
    [string]$Label,

    [switch]$Restart,

    [switch]$Foreground
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$EnvFile = Join-Path $RepoRoot ".env.$Label"
$LogDir = Join-Path $RepoRoot "logs\$Label"
$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$StdoutLog = Join-Path $LogDir "stdout.log"
$PidFile = Join-Path $LogDir "pid.txt"

function Import-DotEnv {
    param([Parameter(Mandatory = $true)][string]$Path)

    foreach ($line in Get-Content -LiteralPath $Path) {
        $trimmed = Remove-InlineComment -Value $line
        $trimmed = $trimmed.Trim()
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

if (-not (Test-Path -LiteralPath $EnvFile)) {
    throw "Missing .env.$Label. Copy .env.example to .env.$Label and fill credentials for this ablation cell."
}

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Missing venv Python at $Python. Run: py -3.12 -m venv .venv --upgrade"
}

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

if (-not $Foreground) {
    if (Test-Path -LiteralPath $PidFile) {
        $oldPidRaw = Get-Content -LiteralPath $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
        $oldPid = 0
        if ([int]::TryParse($oldPidRaw, [ref]$oldPid)) {
            $oldProcess = Get-Process -Id $oldPid -ErrorAction SilentlyContinue
            if ($null -ne $oldProcess) {
                if (-not $Restart) {
                    throw "Cell $Label already appears to be running as PID $oldPid. Stop it with: Stop-Process -Id $oldPid, or relaunch with -Restart."
                }
                Stop-Process -Id $oldPid
                Start-Sleep -Seconds 1
            }
        }
    }

    $scriptArg = '"' + $PSCommandPath + '"'
    $labelArg = '"' + $Label + '"'
    $process = Start-Process -FilePath "powershell.exe" `
        -WorkingDirectory $RepoRoot `
        -ArgumentList "-NoExit -NoProfile -ExecutionPolicy Bypass -File $scriptArg $labelArg -Foreground" `
        -PassThru

    Set-Content -LiteralPath $PidFile -Value $process.Id -Encoding ASCII
    Write-Host "Started PowerShell process: $($process.Id)"
    Write-Host "  Logs: $LogDir"
    Write-Host "  Stop: Stop-Process -Id $($process.Id)"
    exit 0
}

Set-Location -LiteralPath $RepoRoot
Import-DotEnv -Path $EnvFile
$env:ABLATION_LABEL = $Label
$env:LOG_DIR = $LogDir

Write-Host "Starting OpenClaw-Agent cell $Label in $LogDir"
& $Python -m agent.main 2>&1 | Tee-Object -FilePath $StdoutLog -Append
exit $LASTEXITCODE
