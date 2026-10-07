#requires -Version 5.1
param(
    [string]$MosquittoPath,
    [string]$PythonVersion = '3.13'
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '_paths.ps1')

try {
    $broker = Find-Mosquitto $MosquittoPath
    $python = Join-Path $RepoRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $python)) {
        if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
            throw 'Python Launcher not found. Install Python 3.13 from https://www.python.org/downloads/windows/.'
        }
        & py "-$PythonVersion" -m venv (Join-Path $RepoRoot '.venv')
        if ($LASTEXITCODE -ne 0) { throw 'Could not create .venv. Check the requested Python version and the error above.' }
    }
    & $python -m pip --version
    if ($LASTEXITCODE -ne 0) {
        & $python -m ensurepip --upgrade --default-pip
        if ($LASTEXITCODE -ne 0) { throw 'Could not prepare pip. See the error above.' }
    }
    & $python -m pip --disable-pip-version-check install --no-cache-dir --retries 1 --timeout 20 -r (Join-Path $RepoRoot 'requirements.txt')
    if ($LASTEXITCODE -ne 0) { throw 'Could not install dependencies. Check the Internet connection and the error above.' }
    & $python -c "import paho.mqtt.client as mqtt; from importlib.metadata import version; print('paho-mqtt:', version('paho-mqtt')); print('callback API:', mqtt.CallbackAPIVersion.VERSION2.name)"
    if ($LASTEXITCODE -ne 0) { throw 'Paho import check failed.' }
    & $broker -c (Join-Path $RepoRoot 'config\mosquitto.conf') --test-config
    if ($LASTEXITCODE -ne 0) { throw 'Mosquitto could not load the lab configuration.' }
    New-Item -ItemType Directory -Path $LocalDir -Force | Out-Null
    Set-Content -LiteralPath $BrokerPathFile -Value $broker -Encoding UTF8
    Write-Host "Setup OK. Broker: $broker"
    Write-Host 'Next: .\scripts\start-broker.ps1'
} catch {
    Write-Error $_ -ErrorAction Continue
    exit 1
}
