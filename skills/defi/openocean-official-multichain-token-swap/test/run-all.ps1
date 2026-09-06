$ErrorActionPreference = "Stop"

Write-Host "[OpenOcean Skills] Running full coverage tests..."

$repoRoot = Split-Path -Parent $PSScriptRoot
$testScript = Join-Path $PSScriptRoot "full_skill_coverage_test.py"

if (-not (Test-Path $testScript)) {
    Write-Error "Missing test script: $testScript"
    exit 1
}

try {
    Push-Location $repoRoot
    python $testScript
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Tests failed with exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }
    Write-Host "[OpenOcean Skills] All tests passed."
    exit 0
}
finally {
    Pop-Location
}

