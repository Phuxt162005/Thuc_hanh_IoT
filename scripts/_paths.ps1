# Shared paths for the Windows setup scripts.
$RepoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$LocalDir = Join-Path $RepoRoot '.local'
$BrokerPathFile = Join-Path $LocalDir 'mosquitto-path.txt'

function Find-Mosquitto([string]$RequestedPath) {
    $candidates = @()
    if ($RequestedPath) {
        $candidates += $RequestedPath
    } else {
        if (Test-Path -LiteralPath $BrokerPathFile) {
            $candidates += (Get-Content -LiteralPath $BrokerPathFile -Raw).Trim()
        }
        $candidates += Join-Path $RepoRoot '.tools\mosquitto\mosquitto.exe'
        $candidates += Join-Path ([Environment]::GetFolderPath('Desktop')) 'Tools\Mosquitto\mosquitto.exe'
        $candidates += Join-Path $env:ProgramFiles 'Mosquitto\mosquitto.exe'
        $command = Get-Command mosquitto.exe -ErrorAction SilentlyContinue
        if ($command) { $candidates += $command.Source }
    }
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate -PathType Container) {
            $candidate = Join-Path $candidate 'mosquitto.exe'
        }
        if ((Test-Path -LiteralPath $candidate -PathType Leaf) -and
            ([IO.Path]::GetFileName($candidate) -ieq 'mosquitto.exe')) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }
    throw 'Mosquitto not found. Install from https://mosquitto.org/download/ then run setup.ps1 -MosquittoPath "<installation folder>".'
}
