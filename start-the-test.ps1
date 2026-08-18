# D:\autodev\performancetester\start-the-test.ps1

$BaseDir = "D:\autodev\performancetester"
$BackendDir = Join-Path $BaseDir "backend"
$FrontendDir = Join-Path $BaseDir "frontend"
$VenvPython = "D:\autodev\.venv\Scripts\python.exe"

Write-Host "Starting Performance Testing Platform..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 1. Validate Python Virtual Environment
if (-not (Test-Path $VenvPython)) {
    Write-Host "Error: Could not find Python at $VenvPython." -ForegroundColor Red
    exit 1
}

# 2. Validate Frontend package.json
$PackageJsonPath = Join-Path $FrontendDir "package.json"
if (-not (Test-Path $PackageJsonPath)) {
    Write-Host "Error: missing package.json in $FrontendDir." -ForegroundColor Red
    Write-Host "Please ensure package.json is created before launching." -ForegroundColor Yellow
    exit 1
}

# 3. Auto-install Frontend Node Modules if missing
$NodeModulesPath = Join-Path $FrontendDir "node_modules"
if (-not (Test-Path $NodeModulesPath)) {
    Write-Host "node_modules missing. Running 'npm install' in frontend directory..." -ForegroundColor Yellow
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c npm install" -WorkingDirectory $FrontendDir -Wait
}

# 4. Start Python FastAPI Backend
Write-Host "Starting Python FastAPI Backend on port 8000..." -ForegroundColor Cyan
Start-Process -FilePath $VenvPython -ArgumentList "-m uvicorn main:app --reload --port 8000" -WorkingDirectory $BackendDir -WindowStyle Normal

Start-Sleep -Seconds 3

# 5. Start React Frontend (Using /k so terminal window remains open on errors)
Write-Host "Starting React Frontend on port 3000..." -ForegroundColor Cyan
Start-Process -FilePath "cmd.exe" -ArgumentList "/k npm start" -WorkingDirectory $FrontendDir -WindowStyle Normal

Write-Host "`nBoth services launched successfully!" -ForegroundColor Green