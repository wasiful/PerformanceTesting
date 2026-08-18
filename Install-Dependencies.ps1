# D:\autodev\performancetester\Install-Dependencies.ps1

$ErrorActionPreference = "Stop"
$BaseDir = "D:\autodev\performancetester"
$FrontendDir = Join-Path $BaseDir "frontend"

# 1. Ensure working directory exists
if (Test-Path $BaseDir) {
    Set-Location $BaseDir
    Write-Host "Working directory set to: $BaseDir" -ForegroundColor Green
} else {
    Write-Host "Error: Directory $BaseDir does not exist." -ForegroundColor Red
    exit 1
}

# 2. Check for required CLI tools
if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: 'uv' is not installed or not in PATH." -ForegroundColor Red
    exit 1
}
if (-not (Get-Command "npm" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: 'npm' is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

# 3. Install Python Dependencies using uv
Write-Host "`n=== Installing Python Dependencies ===" -ForegroundColor Cyan

# Resolve Python Virtual Environment path
$VenvPath = "D:\autodev\.venv"
if (-not (Test-Path $VenvPath)) {
    $VenvPath = Join-Path $BaseDir "venv"
}

if (Test-Path $VenvPath) {
    Write-Host "Using virtual environment at: $VenvPath" -ForegroundColor Green
} else {
    Write-Host "Warning: Virtual environment not found at 'D:\autodev\.venv' or '$BaseDir\venv'." -ForegroundColor Yellow
}

$ReqFile = Join-Path $BaseDir "requirements.txt"
if (Test-Path $ReqFile) {
    Write-Host "Found requirements.txt. Installing via uv..."
    uv pip install --python $VenvPath -r $ReqFile
} else {
    Write-Host "requirements.txt not found! Installing default packages directly into venv..." -ForegroundColor Yellow
    uv pip install --python $VenvPath fastapi uvicorn sqlalchemy pyodbc pandas matplotlib reportlab requests python-multipart pydantic
}
Write-Host "Python dependencies installed successfully." -ForegroundColor Green

# 4. Install Node.js/React Dependencies using npm in frontend directory
Write-Host "`n=== Installing Node.js Dependencies ===" -ForegroundColor Cyan

if (Test-Path $FrontendDir) {
    Write-Host "Changing directory to: $FrontendDir" -ForegroundColor Cyan
    Set-Location $FrontendDir
    
    Write-Host "Running 'npm install' in frontend directory..." -ForegroundColor Cyan
    npm install
    
    Write-Host "Ensuring required React UI and Charting libraries are installed..." -ForegroundColor Cyan
    npm install axios react-router-dom bootstrap chart.js react-chartjs-2
    
    # Return to base directory
    Set-Location $BaseDir
    Write-Host "Node.js dependencies installed successfully." -ForegroundColor Green
} else {
    Write-Host "Error: Frontend directory not found at $FrontendDir." -ForegroundColor Red
    exit 1
}

Write-Host "`n=== Setup Complete! All dependencies are ready. ===" -ForegroundColor Green