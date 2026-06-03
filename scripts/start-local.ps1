$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path $root "backend"
$frontendDir = Join-Path $root "frontend"
$toolsDir = Join-Path $root ".tools"
$mavenHome = Join-Path $toolsDir "apache-maven-3.9.9"
$mavenZip = Join-Path $toolsDir "apache-maven-3.9.9-bin.zip"

function Find-JavaHome {
    if ($env:JAVA_HOME -and (Test-Path (Join-Path $env:JAVA_HOME "bin\java.exe"))) {
        return $env:JAVA_HOME
    }

    $adoptium = Get-ChildItem "C:\Program Files\Eclipse Adoptium" -Directory -Filter "jdk-21*" -ErrorAction SilentlyContinue |
        Sort-Object Name -Descending |
        Select-Object -First 1

    if ($adoptium) {
        return $adoptium.FullName
    }

    throw "JDK 21 was not found. Please install Eclipse Temurin JDK 21 and retry."
}

function Ensure-Maven {
    New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null

    if (!(Test-Path $mavenHome)) {
        if (!(Test-Path $mavenZip)) {
            Write-Host "Downloading Maven 3.9.9..."
            curl.exe -L --retry 5 --retry-delay 2 -o $mavenZip "https://archive.apache.org/dist/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.zip"
        }
        Expand-Archive -LiteralPath $mavenZip -DestinationPath $toolsDir -Force
    }

    return Join-Path $mavenHome "bin\mvn.cmd"
}

function Wait-HttpOk($url, $name) {
    for ($i = 0; $i -lt 45; $i++) {
        try {
            $status = & curl.exe -s -o NUL -w "%{http_code}" $url
            if ($status -ge 200 -and $status -lt 300) {
                Write-Host "$name is ready: $url"
                return
            }
        } catch {
            Start-Sleep -Seconds 1
        }
    }

    throw "$name did not start in time: $url"
}

$javaHome = Find-JavaHome
$mvn = Ensure-Maven
$env:JAVA_HOME = $javaHome
$env:Path = "$javaHome\bin;$mavenHome\bin;$env:Path"

Write-Host "Using Java: $javaHome"
Write-Host "Using Maven: $mavenHome"

Push-Location $backendDir
try {
    & $mvn -q package
} finally {
    Pop-Location
}

$backendPort = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue
if (!$backendPort) {
    $backendLog = Join-Path $backendDir "target\backend-run.log"
    $backendErr = Join-Path $backendDir "target\backend-run.err.log"
    Start-Process -FilePath (Join-Path $javaHome "bin\java.exe") `
        -ArgumentList "-jar", "target\endpoint-security-platform-0.1.0.jar" `
        -WorkingDirectory $backendDir `
        -RedirectStandardOutput $backendLog `
        -RedirectStandardError $backendErr `
        -WindowStyle Hidden
}

Wait-HttpOk "http://localhost:8080/actuator/health" "backend"

Push-Location $frontendDir
try {
    if (!(Test-Path "node_modules")) {
        npm.cmd install
    }
    npm.cmd run build
} finally {
    Pop-Location
}

$frontendPort = Get-NetTCPConnection -LocalPort 55300 -State Listen -ErrorAction SilentlyContinue
if (!$frontendPort) {
    $frontendLog = Join-Path $frontendDir "frontend-55300.log"
    $frontendErr = Join-Path $frontendDir "frontend-55300.err.log"
    Start-Process -FilePath "npm.cmd" `
        -ArgumentList "run", "dev", "--", "--host", "127.0.0.1", "--port", "55300", "--strictPort" `
        -WorkingDirectory $frontendDir `
        -RedirectStandardOutput $frontendLog `
        -RedirectStandardError $frontendErr `
        -WindowStyle Hidden
}

Wait-HttpOk "http://localhost:55300/dashboard" "frontend"

$api = Invoke-RestMethod -Uri "http://localhost:55300/api/endpoints" -TimeoutSec 5
if (!$api.success -or $api.data.Count -lt 1) {
    throw "Frontend proxy API check failed."
}

Write-Host "Run completed:"
Write-Host "  Frontend: http://localhost:55300"
Write-Host "  Backend: http://localhost:8080"
Write-Host "  Health: http://localhost:8080/actuator/health"
