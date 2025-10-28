# Russian.Town Backend Setup Script
# PowerShell script for easy setup

Write-Host "========================================"
Write-Host "Russian.Town Backend Setup"
Write-Host "========================================"
Write-Host ""

# Change to backend directory
Set-Location -Path "backend"

# Step 1: Install packages
Write-Host "[1/3] Installing Python packages..."
Write-Host "This may take 1-2 minutes..."
Write-Host ""

pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Package installation failed!" -ForegroundColor Red
    Write-Host "Please check your Python installation."
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Set environment variables
Write-Host ""
Write-Host "[2/3] Setting environment variables..."
$env:DATABASE_URL = "postgresql://kru_user:password@localhost:5432/kru_community"
$env:REDIS_URL = "redis://localhost:6379/0"
$env:SECRET_KEY = "dev-secret-key"
$env:ENVIRONMENT = "development"

# Step 3: Start backend
Write-Host ""
Write-Host "[3/3] Starting backend server..."
Write-Host ""
Write-Host "========================================"
Write-Host "Backend server starting!"
Write-Host "Keep this window open!"
Write-Host "========================================"
Write-Host ""
Write-Host "API URL: http://localhost:8000" -ForegroundColor Green
Write-Host "Test URL: http://localhost:8000/api/posts/?category_id=1" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Read-Host "Press Enter to exit"
