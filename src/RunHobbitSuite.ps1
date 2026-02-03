<#
.SYNOPSIS
    Installs requirements and runs hypothesis fuzz on all Python files in RunHobbitSuite
    with a 2-minute timeout per file
#>
$ScriptDir = $PSScriptRoot
Set-Location -Path $ScriptDir
$VenvDir = Join-Path $ScriptDir "venv"
$ParentDir = Split-Path -Path $ScriptDir -Parent
$ReqFile = Join-Path $ParentDir "requirements.txt"
$SuiteDir = Join-Path $ScriptDir "RunHobbitSuite"
$FailureLog = Join-Path $ScriptDir "hypofuzz_failures.log"

# Executables
$PipExe = Join-Path $VenvDir "Scripts\pip.exe"
$HypothesisExe = Join-Path $VenvDir "Scripts\hypothesis.exe"

# clear log before running
if (Test-Path $FailureLog) {
    Clear-Content $FailureLog
} else {
    New-Item -ItemType File -Path $FailureLog | Out-Null
}


# install Requirements
if (Test-Path -Path $ReqFile) {
    Write-Host "[*] Installing requirements from: $ReqFile" -ForegroundColor Cyan
    & $PipExe install -r $ReqFile
} else {
    Write-Error "CRITICAL: requirements.txt NOT found at $ReqFile"
    return
}

if (-not (Test-Path $HypothesisExe)) {
    Write-Error "Hypothesis was not found in the venv. Please ensure 'hypothesis' is in your requirements.txt"
    return
}

# define target dir
$targetDir = Join-Path -Path $PSScriptRoot -ChildPath "RunHobbitSuite"

if (-not (Test-Path -Path $targetDir)) {
    Write-Error "Directory '$targetDir' not found."
    exit 1
}

$pythonFiles = Get-ChildItem -Path $targetDir -Filter "*.py"

$terminatedCount = 0
$timeoutSeconds = 120

Write-Host "Found $($pythonFiles.Count) Python files. Starting fuzzing..." -ForegroundColor Cyan

foreach ($file in $pythonFiles) {
    Write-Host "Fuzzing file: $($file.Name)" -NoNewline

    $pInfo = New-Object System.Diagnostics.ProcessStartInfo
    $pInfo.FileName = $HypothesisExe

    $pInfo.Arguments = "fuzz `"$($file.FullName)`" --no-dashboard"
    $pInfo.WorkingDirectory = $PSScriptRoot
    $pInfo.UseShellExecute = $false
    $pInfo.RedirectStandardOutput = $true # set to false to see output
    $pInfo.RedirectStandardError = $true

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $pInfo
    $process.Start() | Out-Null

    $exitedNaturally = $process.WaitForExit($timeoutSeconds * 1000)

    if ($exitedNaturally) {
        Write-Host " -> Terminated (Success)" -ForegroundColor Green
        $terminatedCount++  # a relic from a previous ver. of this script, probably worth removing
    }
    else {
        Write-Host " -> Timed out (Killing process)" -ForegroundColor Yellow
        try {
            $process.Kill()
        }
        catch {

        }
    }
    
    $process.Dispose()
}

$failureCount = 0
if (Test-Path $FailureLog) {
    $failureCount = (Get-Content $FailureLog | Measure-Object -Line).Lines
}

Write-Host "--------------------------------------------------"
#Write-Host "Total files that terminated naturally: $terminatedCount" -ForegroundColor Green
Write-Host "Inequivalences found: $failureCount / $($pythonFiles.Count)" -ForegroundColor Red
Write-Host "Script complete."