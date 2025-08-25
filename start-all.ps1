# Healthcare Assistant - Unified Service Launcher
# PowerShell version for better cross-platform support

param(
    [switch]$OpenBrowser = $true,
    [switch]$Verbose = $false
)

# Set console title and colors
$Host.UI.RawUI.WindowTitle = "Healthcare Assistant - All Services"

function Write-ColoredOutput {
    param(
        [string]$Message,
        [string]$Color = "White",
        [string]$Prefix = "INFO"
    )
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] [$Prefix] $Message" -ForegroundColor $Color
}

function Test-ServiceDependencies {
    Write-ColoredOutput "Checking service dependencies..." "Cyan" "CHECK"
    
    # Check if directories exist
    $requiredDirs = @("ai_service", "server", "client")
    foreach ($dir in $requiredDirs) {
        if (-not (Test-Path $dir)) {
            Write-ColoredOutput "Directory '$dir' not found!" "Red" "ERROR"
            exit 1
        }
    }
    
    # Check if key files exist
    $requiredFiles = @(
        "ai_service\app.py",
        "server\index.js", 
        "client\package.json"
    )
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            Write-ColoredOutput "Required file '$file' not found!" "Red" "ERROR"
            exit 1
        }
    }
    
    Write-ColoredOutput "All dependencies verified!" "Green" "CHECK"
}

function Start-ServiceInNewWindow {
    param(
        [string]$ServiceName,
        [string]$WorkingDirectory,
        [string]$Command,
        [string]$Arguments,
        [int]$Port
    )
    
    Write-ColoredOutput "Starting $ServiceName on port $Port..." "Yellow" "START"
    
    $processArgs = @{
        FilePath = "powershell"
        ArgumentList = @(
            "-NoExit",
            "-Command",
            "Set-Location '$WorkingDirectory'; $Command $Arguments"
        )
        WindowStyle = "Normal"
        PassThru = $true
    }
    
    try {
        $process = Start-Process @processArgs
        Write-ColoredOutput "$ServiceName started successfully (PID: $($process.Id))" "Green" "START"
        return $process
    }
    catch {
        Write-ColoredOutput "Failed to start $ServiceName`: $_" "Red" "ERROR"
        return $null
    }
}

function Wait-ForService {
    param(
        [string]$ServiceName,
        [string]$Url,
        [int]$TimeoutSeconds = 30
    )
    
    Write-ColoredOutput "Waiting for $ServiceName to be ready..." "Cyan" "WAIT"
    
    $timeout = (Get-Date).AddSeconds($TimeoutSeconds)
    
    do {
        try {
            $response = Invoke-WebRequest -Uri $Url -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-ColoredOutput "$ServiceName is ready!" "Green" "READY"
                return $true
            }
        }
        catch {
            # Service not ready yet, continue waiting
        }
        
        Start-Sleep -Seconds 2
    } while ((Get-Date) -lt $timeout)
    
    Write-ColoredOutput "$ServiceName startup timeout - continuing anyway" "Yellow" "WARN"
    return $false
}

# Main execution
try {
    Clear-Host
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host "  Healthcare Assistant - Service Launcher" -ForegroundColor Magenta  
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host ""
    
    # Check dependencies
    Test-ServiceDependencies
    
    Write-Host ""
    Write-ColoredOutput "Starting all services..." "Cyan" "MAIN"
    Write-Host ""
    
    # Start AI Service
    $aiProcess = Start-ServiceInNewWindow -ServiceName "AI Service" -WorkingDirectory "ai_service" -Command "python" -Arguments "app.py" -Port 5001
    Start-Sleep -Seconds 3
    
    # Start Backend Server
    $backendProcess = Start-ServiceInNewWindow -ServiceName "Backend Server" -WorkingDirectory "server" -Command "node" -Arguments "index.js" -Port 5000
    Start-Sleep -Seconds 3
    
    # Start React Frontend
    $frontendProcess = Start-ServiceInNewWindow -ServiceName "React Frontend" -WorkingDirectory "client" -Command "npm" -Arguments "start" -Port 3000
    Start-Sleep -Seconds 5
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  All Services Started Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    Write-ColoredOutput "Frontend:   http://localhost:3000" "Yellow" "URL"
    Write-ColoredOutput "Backend:    http://localhost:5000" "Green" "URL"  
    Write-ColoredOutput "AI Service: http://localhost:5001" "Cyan" "URL"
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host ""
    
    if ($OpenBrowser) {
        Write-ColoredOutput "Opening application in browser..." "Cyan" "BROWSER"
        Start-Sleep -Seconds 3
        Start-Process "http://localhost:3000"
    }
    
    Write-ColoredOutput "All services are running!" "Green" "SUCCESS"
    Write-ColoredOutput "Close the individual service windows to stop services." "White" "INFO"
    Write-Host ""
    
    Read-Host "Press Enter to exit this launcher (services will continue running)"
    
}
catch {
    Write-ColoredOutput "An error occurred: $_" "Red" "ERROR"
    exit 1
}
