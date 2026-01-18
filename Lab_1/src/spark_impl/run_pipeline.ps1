<#
.SYNOPSIS
    Automated setup and execution script for the TMDB Data Engineering Pipeline.

.DESCRIPTION
    This script handles the end-to-end execution flow:
    1. Checks for Python installation.
    2. Creates a virtual environment (venv) if not present.
    3. Install/Upgrades dependencies from requirements.txt.
    4. Verifies environment configuration (.env).
    5. Executes the main Spark ETL pipeline.

.EXAMPLE
    .\run_pipeline.ps1
#>

$ErrorActionPreference = "Stop"

# --- Configuration ---
$ProjectRoot = $PSScriptRoot
$VenvPath = Join-Path $ProjectRoot "venv"
$PythonScript = Join-Path $ProjectRoot "main.py"
$RequirementsFile = Join-Path $ProjectRoot "requirements.txt"
$EnvFile = Join-Path $ProjectRoot "..\.env"  # Assumption based on project structure or standard location

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   TMDB Data Pipeline Executive Script    " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Python
Write-Host "[1/5] Checking Python Environment..." -ForegroundColor Yellow
try {
    $null = python --version
    Write-Host "      Python found." -ForegroundColor Green
} catch {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.8+."
}

# 2. Setup Virtual Environment
if (-not (Test-Path $VenvPath)) {
    Write-Host "[2/5] Creating Virtual Environment at $VenvPath..." -ForegroundColor Yellow
    python -m venv $VenvPath
    Write-Host "      Venv created successfully." -ForegroundColor Green
} else {
    Write-Host "[2/5] Virtual Environment found." -ForegroundColor Green
}

# 3. Activation & Dependencies
Write-Host "[3/5] Installing/Updating Components..." -ForegroundColor Yellow
$PipHelper = Join-Path $VenvPath "Scripts\python.exe"
# Upgrade pip first
& $PipHelper -m pip install --upgrade pip | Out-Null
# Install requirements
if (Test-Path $RequirementsFile) {
    & $PipHelper -m pip install -r $RequirementsFile | Out-Null
    Write-Host "      Dependencies installed." -ForegroundColor Green
} else {
    Write-Warning "requirements.txt not found! Skipping dependency installation."
}

# 4. Environment Check
Write-Host "[4/5] Checking Configuration..." -ForegroundColor Yellow
# Note: The referencing of .env is handled by python-dotenv in the script, 
# but good to check if it exists to warn user.
if (-not (Test-Path $EnvFile)) {
    if (-not (Test-Path (Join-Path $ProjectRoot ".env"))) {
        Write-Warning "      .env file not found in parent or current directory. Pipeline might fail if API keys are missing."
    }
} else {
    Write-Host "      Configuration found." -ForegroundColor Green
}

# 5. Execute Pipeline
Write-Host "[5/5] Starting Spark ETL Pipeline..." -ForegroundColor Yellow
Write-Host "      Log output follows:" -ForegroundColor Gray

try {
    # Add venv to PATH so sub-processes (Spark workers) can find 'python'
    $env:PATH = "$VenvPath\Scripts;$env:PATH"

    # Run the main script using the venv python
    & $PipHelper $PythonScript
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nPassed: Pipeline executed successfully." -ForegroundColor Green
    } else {
        Write-Error "Pipeline failed with exit code $LASTEXITCODE"
    }
} catch {
    Write-Error "Failed to execute pipeline script: $_"
}

Write-Host "`nProcess Complete." -ForegroundColor Cyan
