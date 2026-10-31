param([int]$Left = 0, [int]$Top = 0)
$ErrorActionPreference = 'Stop'
$edge = Join-Path ${env:ProgramFiles(x86)} 'Microsoft\Edge\Application\msedge.exe'
if (-not (Test-Path -LiteralPath $edge)) { throw 'Microsoft Edge was not found.' }
$profile = Join-Path $env:TEMP 'ChurchView-Projector-profile'
if ($Left -eq 0 -and $Top -eq 0) {
    Add-Type -AssemblyName System.Windows.Forms
    $second = [Windows.Forms.Screen]::AllScreens | Where-Object { -not $_.Primary } | Select-Object -First 1
    if ($second) { $Left = $second.Bounds.Left; $Top = $second.Bounds.Top }
}
$arguments = '--kiosk http://localhost:8765/projector.html?native=1 --edge-kiosk-type=fullscreen --no-first-run --window-position=' + $Left + ',' + $Top + ' --user-data-dir="' + $profile + '"'
Start-Process -FilePath $edge -ArgumentList $arguments -WindowStyle Normal
