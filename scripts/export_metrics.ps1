param(
    [string]$OutJson = "results/metrics.json",
    [string]$OutMd = "results/h1_table.md",
    [string]$B3StartFrom = "",
    [string]$B3LlmStartFrom = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$B3Equity = Join-Path $RepoRoot "logs\B3\equity.csv"
$B3LlmEquity = Join-Path $RepoRoot "logs\B3_LLM\equity.csv"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Missing venv Python at $Python"
}

if (-not (Test-Path -LiteralPath $B3Equity)) {
    throw "Missing B3 equity log at $B3Equity"
}

if (-not (Test-Path -LiteralPath $B3LlmEquity)) {
    throw "Missing B3_LLM equity log at $B3LlmEquity"
}

Set-Location -LiteralPath $RepoRoot

$h1Args = @(
    "scripts/h1_test.py",
    "--equity-csv", "B3=logs/B3/equity.csv",
    "--equity-csv", "B3_LLM=logs/B3_LLM/equity.csv",
    "--out-json", $OutJson,
    "--out-md", $OutMd
)
if ($B3StartFrom) {
    $h1Args += "--start-from"
    $h1Args += "B3=$B3StartFrom"
}
if ($B3LlmStartFrom) {
    $h1Args += "--start-from"
    $h1Args += "B3_LLM=$B3LlmStartFrom"
}

& $Python @h1Args

exit $LASTEXITCODE
