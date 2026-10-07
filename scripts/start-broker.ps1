#requires -Version 5.1
param([string]$MosquittoPath)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '_paths.ps1')

try {
    $broker = Find-Mosquitto $MosquittoPath
    $probe = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, 1884)
    $probe.Server.ExclusiveAddressUse = $true
    try { $probe.Start() } catch {
        throw 'Port 1884 is already in use. Check the existing lab broker terminal before starting another.'
    } finally { $probe.Stop() }
    Write-Host 'Starting lab broker at 127.0.0.1:1884. Keep this terminal open; Ctrl+C stops it.'
    & $broker -c (Join-Path $RepoRoot 'config\mosquitto.conf') -v
    exit $LASTEXITCODE
} catch {
    Write-Error $_ -ErrorAction Continue
    exit 1
}
