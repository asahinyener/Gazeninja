<#  batch_run.ps1
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
    Usage:  .\batch_run.ps1  -Input  ".\data"  -Output ".\metrics"
#>

param(
    [string]$Input  = ".\data",
    [string]$Output = ".\metrics"
)

# Create output folder if missing
if (-not (Test-Path $Output)) { New-Item -Path $Output -ItemType Directory | Out-Null }

Get-ChildItem -Path $Input -Filter "*.csv" | ForEach-Object {
    $base = $_.BaseName
    python analyze_growbox.py `
        --csv $_.FullName `
        --episodes  (Join-Path $Output "${base}_episodes.csv") `
        --metrics   (Join-Path $Output "${base}_metrics.json")
}
# Notify completion
Write-Host "Analysis complete. Results saved to $Output"