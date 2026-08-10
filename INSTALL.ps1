<#
    INSTALL.ps1 — Agyle Werkwijze installeren

    Zet de skills, de hooks en je persoonlijke configuratie op je eigen machine.
    Draai dit vanuit de map van dit pakket:

        .\INSTALL.ps1

    Bestaande bestanden worden geback-upt, niet overschreven zonder spoor.
    Draai daarna VALIDATE.ps1 om te controleren of alles klopt.
#>

[CmdletBinding()]
param(
    [switch]$Force  # skills overschrijven zonder te vragen
)

$ErrorActionPreference = "Stop"
$pakket = $PSScriptRoot
$claudeDir = Join-Path $HOME ".claude"

function Info($m) { Write-Host "  $m" }
function Goed($m) { Write-Host "  [ok] $m" -ForegroundColor Green }
function Waarschuw($m) { Write-Host "  [let op] $m" -ForegroundColor Yellow }
function Stuk($m) { Write-Host "  [fout] $m" -ForegroundColor Red }

function Schrijf-Utf8NoBom($pad, $inhoud) {
    # PowerShell 5.1 zet standaard een BOM voor UTF8; dat willen we niet in
    # bestanden die door Node/Python gelezen worden.
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($pad, $inhoud, $enc)
}

Write-Host ""
Write-Host "Agyle Werkwijze — installatie" -ForegroundColor Cyan
Write-Host ("-" * 50)

# ---------------------------------------------------------------- 1. vereisten
Write-Host ""
Write-Host "1. Vereisten"

$py = Get-Command python -ErrorAction SilentlyContinue
if ($py) { Goed "Python gevonden: $($py.Source)" }
else { Stuk "Python niet gevonden. Installeer Python 3 en draai dit script opnieuw."; exit 1 }

$cc = Get-Command claude -ErrorAction SilentlyContinue
if ($cc) { Goed "Claude Code gevonden" } else { Waarschuw "Claude Code niet op PATH — skills werken pas als dat klopt" }

$browser = $false
foreach ($p in @(
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe")) {
    if (Test-Path $p) { $browser = $true; break }
}
if ($browser) { Goed "Edge of Chrome gevonden (nodig voor PDF-generatie)" }
else { Waarschuw "Geen Edge/Chrome gevonden — PDF's genereren zal falen" }

# ---------------------------------------------------------------- 2. config
Write-Host ""
Write-Host "2. Persoonlijke configuratie"

$configPad = Join-Path $pakket "config\persoon.json"
$voorbeeldPad = Join-Path $pakket "config\persoon.example.json"

if (-not (Test-Path $configPad)) {
    Stuk "config\persoon.json ontbreekt."
    Info ""
    Info "Maak hem aan met:"
    Info "    Copy-Item `"$voorbeeldPad`" `"$configPad`""
    Info ""
    Info "Vul daarna je naam, mailadres, telefoonnummer en paden in, en draai dit script opnieuw."
    exit 1
}

$cfg = Get-Content $configPad -Raw | ConvertFrom-Json

$verplicht = @("naam", "functie", "email", "telefoon", "clients_root")
$ontbreekt = @()
foreach ($v in $verplicht) {
    if (-not $cfg.$v -or "$($cfg.$v)".Trim() -eq "" -or "$($cfg.$v)" -like "*JOUWNAAM*" -or "$($cfg.$v)" -like "Voornaam Achternaam") {
        $ontbreekt += $v
    }
}
if ($ontbreekt.Count -gt 0) {
    Stuk "Nog niet ingevuld in persoon.json: $($ontbreekt -join ', ')"
    exit 1
}
Goed "Configuratie gelezen voor $($cfg.naam)"

# ---------------------------------------------------------------- 3. skills
Write-Host ""
Write-Host "3. Skills"

$skillsDoel = Join-Path $claudeDir "skills"
New-Item -ItemType Directory -Force -Path $skillsDoel | Out-Null

$backupDir = Join-Path $claudeDir ("backup-werkwijze-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
$backupGemaakt = $false

Get-ChildItem (Join-Path $pakket "skills") -Directory | ForEach-Object {
    $naam = $_.Name
    $doel = Join-Path $skillsDoel $naam
    if (Test-Path $doel) {
        if (-not $Force) {
            if (-not $backupGemaakt) { New-Item -ItemType Directory -Force -Path $backupDir | Out-Null; $backupGemaakt = $true }
            Copy-Item $doel (Join-Path $backupDir $naam) -Recurse -Force
            Waarschuw "$naam bestond al — oude versie geback-upt"
        }
        Remove-Item $doel -Recurse -Force
    }
    Copy-Item $_.FullName $doel -Recurse -Force
    Info "$naam"
}
Goed "Skills geinstalleerd in $skillsDoel"
if ($backupGemaakt) { Info "Back-up van vervangen skills: $backupDir" }

# ---------------------------------------------------------------- 4. hooks
Write-Host ""
Write-Host "4. Hooks"

$hooksDoel = Join-Path $claudeDir "hooks"
New-Item -ItemType Directory -Force -Path $hooksDoel | Out-Null
Get-ChildItem (Join-Path $pakket "hooks") -Filter *.py | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $hooksDoel $_.Name) -Force
    Info $_.Name
}
Goed "Hooks gekopieerd naar $hooksDoel"

# ---------------------------------------------------------------- 5. settings
Write-Host ""
Write-Host "5. Hooks registreren in settings.json"

$settingsPad = Join-Path $claudeDir "settings.json"
if (Test-Path $settingsPad) {
    Copy-Item $settingsPad "$settingsPad.bak" -Force
    $settings = Get-Content $settingsPad -Raw | ConvertFrom-Json
    Info "Bestaande settings.json geback-upt naar settings.json.bak"
} else {
    $settings = [PSCustomObject]@{}
}

if (-not $settings.PSObject.Properties.Name.Contains("hooks")) {
    $settings | Add-Member -NotePropertyName "hooks" -NotePropertyValue ([PSCustomObject]@{}) -Force
}
if (-not $settings.hooks.PSObject.Properties.Name.Contains("Stop")) {
    $settings.hooks | Add-Member -NotePropertyName "Stop" -NotePropertyValue @() -Force
}

$bestaandeCommandos = @()
foreach ($groep in @($settings.hooks.Stop)) {
    foreach ($h in @($groep.hooks)) { $bestaandeCommandos += "$($h.command)" }
}

$teRegistreren = @(
    @{ script = "update_progress.py"; timeout = 30 },
    @{ script = "update_handover.py"; timeout = 60 }
)

$nieuweGroepen = @($settings.hooks.Stop)
foreach ($item in $teRegistreren) {
    $cmd = 'python "' + (Join-Path $hooksDoel $item.script).Replace('\', '/') + '"'
    $alAanwezig = $bestaandeCommandos | Where-Object { $_ -like "*$($item.script)*" }
    if ($alAanwezig) {
        Info "$($item.script) stond al geregistreerd"
        continue
    }
    $nieuweGroepen += [PSCustomObject]@{
        matcher = ""
        hooks   = @([PSCustomObject]@{ type = "command"; command = $cmd; timeout = $item.timeout })
    }
    Goed "$($item.script) toegevoegd als Stop-hook"
}
$settings.hooks.Stop = $nieuweGroepen

Schrijf-Utf8NoBom $settingsPad ($settings | ConvertTo-Json -Depth 12)
Goed "settings.json bijgewerkt"

# ---------------------------------------------------------------- 6. handtekening
Write-Host ""
Write-Host "6. E-mailhandtekening"

$assetsDir = Join-Path $claudeDir "assets"
New-Item -ItemType Directory -Force -Path $assetsDir | Out-Null

$sigTemplate = Get-Content (Join-Path $pakket "templates\agyle-signature-url.template.html") -Raw
$sig = $sigTemplate `
    -replace '\{\{NAAM\}\}', [regex]::Escape($cfg.naam).Replace('\', '') `
    -replace '\{\{FUNCTIE\}\}', $cfg.functie `
    -replace '\{\{EMAIL\}\}', $cfg.email `
    -replace '\{\{TELEFOON\}\}', $cfg.telefoon

if ([string]::IsNullOrWhiteSpace($cfg.bookings_url)) {
    # Geen boekingslink: het hele blok eruit in plaats van een kapotte knop.
    $sig = [regex]::Replace($sig, '<!-- BOOKINGS-START -->.*?<!-- BOOKINGS-END -->', '', 'Singleline')
    Waarschuw "Geen bookings_url ingevuld — boekingsblok weggelaten uit de handtekening"
} else {
    $sig = $sig -replace '\{\{BOOKINGS_URL\}\}', $cfg.bookings_url
    Goed "Boekingslink verwerkt"
}

$sigPad = Join-Path $assetsDir "agyle-signature-url.html"
if (Test-Path $sigPad) { Copy-Item $sigPad "$sigPad.bak" -Force; Info "Bestaande handtekening geback-upt" }
Schrijf-Utf8NoBom $sigPad $sig
Goed "Handtekening geschreven naar $sigPad"

# ---------------------------------------------------------------- 7. runtime-config
Write-Host ""
Write-Host "7. Padconfiguratie voor skills"

$runtime = [PSCustomObject]@{
    naam            = $cfg.naam
    email           = $cfg.email
    clients_root    = $cfg.clients_root
    prep_output_dir = $cfg.prep_output_dir
}
$runtimePad = Join-Path $claudeDir "agyle-persoon.json"
Schrijf-Utf8NoBom $runtimePad ($runtime | ConvertTo-Json -Depth 5)
Goed "agyle-persoon.json geschreven (skills lezen hier hun paden)"

# ---------------------------------------------------------------- klaar
Write-Host ""
Write-Host ("-" * 50)
Write-Host "Installatie afgerond." -ForegroundColor Green
Write-Host ""
Write-Host "Hierna:"
Write-Host "  1. .\VALIDATE.ps1                    controleer de installatie"
Write-Host "  2. docs\03-MCP-SETUP.md              zet je MCP-servers op"
Write-Host "  3. docs\02-WERKWIJZE.md              lees hoe wij werken"
Write-Host ""
Write-Host "Start Claude Code opnieuw op zodat de skills en hooks geladen worden."
Write-Host ""
