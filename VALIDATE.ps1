<#
    VALIDATE.ps1 — controleer het pakket en de installatie

    Twee rollen in één script:

      .\VALIDATE.ps1              controleer JOUW installatie (na INSTALL.ps1)
      .\VALIDATE.ps1 -Pakket      controleer alleen het PAKKET zelf
                                  (geen absolute paden, geen secrets) —
                                  draai dit vóór elke push naar GitHub

    Exitcode 0 = alles goed, 1 = er zijn fouten.
#>

[CmdletBinding()]
param(
    [switch]$Pakket  # alleen de pakketcontroles, sla de installatiecontroles over
)

$pakketDir = $PSScriptRoot
$claudeDir = Join-Path $HOME ".claude"
$fouten = 0
$waarschuwingen = 0

function Kop($m) { Write-Host ""; Write-Host $m -ForegroundColor Cyan }
function Goed($m) { Write-Host "  [ok]      $m" -ForegroundColor Green }
function Waarschuw($m) { Write-Host "  [let op]  $m" -ForegroundColor Yellow; $script:waarschuwingen++ }
function Stuk($m) { Write-Host "  [FOUT]    $m" -ForegroundColor Red; $script:fouten++ }

Write-Host ""
Write-Host "Agyle Werkwijze — validatie" -ForegroundColor Cyan
Write-Host ("=" * 55)

# ================================================================ PAKKET
Kop "A. Het pakket zelf"

# A1 — geen absolute paden naar een specifieke medewerker
$padPatroon = 'C:\\Users\\[A-Za-z]+\\|OneDrive - Agyle'
$treffers = @()
foreach ($map in @("skills", "hooks", "templates", "docs")) {
    $volledig = Join-Path $pakketDir $map
    if (-not (Test-Path $volledig)) { continue }
    $treffers += Get-ChildItem $volledig -Recurse -File -Include *.md, *.py, *.ps1, *.json, *.html |
        Select-String -Pattern $padPatroon -ErrorAction SilentlyContinue |
        Where-Object { $_.Path -notlike "*persoon.example.json" -and $_.Path -notlike "*03-MCP-SETUP.md" }
}
if ($treffers.Count -eq 0) {
    Goed "Geen absolute gebruikerspaden gevonden"
} else {
    Stuk "Absolute paden gevonden — het pakket is niet overdraagbaar:"
    $treffers | Select-Object -First 12 | ForEach-Object {
        Write-Host "             $($_.Path.Replace($pakketDir,'.')):$($_.LineNumber)" -ForegroundColor Red
    }
}

# A2 — geen secrets
$secretPatroon = '(API_KEY|SECRET|PASSWORD|TOKEN)\s*[=:]\s*["'']?[A-Za-z0-9_\-]{16,}'
$secrets = Get-ChildItem $pakketDir -Recurse -File -Include *.md, *.py, *.ps1, *.json, *.html, *.env, *.txt -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike "*\.git\*" } |
    Select-String -Pattern $secretPatroon -ErrorAction SilentlyContinue
if ($secrets.Count -eq 0) { Goed "Geen sleutels of wachtwoorden aangetroffen" }
else {
    Stuk "Mogelijke secrets gevonden — NIET pushen:"
    $secrets | Select-Object -First 8 | ForEach-Object {
        Write-Host "             $($_.Path.Replace($pakketDir,'.')):$($_.LineNumber)" -ForegroundColor Red
    }
}

# A3 — geen .env bestanden (alleen .env.example mag)
$envs = Get-ChildItem $pakketDir -Recurse -File -Force -Filter ".env" -ErrorAction SilentlyContinue
if ($envs.Count -eq 0) { Goed "Geen .env-bestanden in het pakket" }
else { $envs | ForEach-Object { Stuk ".env aangetroffen: $($_.FullName.Replace($pakketDir,'.'))" } }

# A4 — elke skill heeft een SKILL.md met frontmatter
Get-ChildItem (Join-Path $pakketDir "skills") -Directory | ForEach-Object {
    $sk = Join-Path $_.FullName "SKILL.md"
    if ($_.Name -like "_*") { return }  # assets-mappen, geen skill
    if (-not (Test-Path $sk)) { Stuk "$($_.Name): SKILL.md ontbreekt"; return }
    $eerste = (Get-Content $sk -TotalCount 1)
    if ($eerste -ne "---") { Waarschuw "$($_.Name): SKILL.md heeft geen frontmatter" }
}
Goed "Skillmappen gecontroleerd"

# A5 — hooks compileren
Get-ChildItem (Join-Path $pakketDir "hooks") -Filter *.py | ForEach-Object {
    & python -m py_compile $_.FullName 2>$null
    if ($LASTEXITCODE -eq 0) { Goed "$($_.Name) compileert" } else { Stuk "$($_.Name) heeft een syntaxfout" }
}
Remove-Item (Join-Path $pakketDir "hooks\__pycache__") -Recurse -Force -ErrorAction SilentlyContinue

# A6 — geen onvervangen placeholders in templates die al gevuld horen te zijn
$sjabloonPlaceholders = Get-ChildItem (Join-Path $pakketDir "templates") -File |
    Select-String -Pattern '\{\{[A-Z_]+\}\}' -ErrorAction SilentlyContinue
if ($sjabloonPlaceholders) { Goed "Templates bevatten placeholders (zo hoort het)" }
else { Waarschuw "Geen placeholders in templates gevonden — klopt dat?" }

if ($Pakket) {
    Write-Host ""
    Write-Host ("=" * 55)
    if ($fouten -eq 0) { Write-Host "Pakket is schoon. Klaar om te pushen." -ForegroundColor Green; exit 0 }
    else { Write-Host "$fouten fout(en) gevonden. Niet pushen." -ForegroundColor Red; exit 1 }
}

# ================================================================ INSTALLATIE
Kop "B. Jouw installatie"

# B1 — persoonsconfig
$runtimePad = Join-Path $claudeDir "agyle-persoon.json"
if (Test-Path $runtimePad) {
    $rt = Get-Content $runtimePad -Raw | ConvertFrom-Json
    Goed "agyle-persoon.json aanwezig (voor $($rt.naam))"
    if (Test-Path $rt.clients_root) { Goed "clients_root bestaat: $($rt.clients_root)" }
    else { Stuk "clients_root bestaat niet: $($rt.clients_root)" }
} else { Stuk "agyle-persoon.json ontbreekt — draai INSTALL.ps1" }

# B2 — skills geinstalleerd
$verwacht = Get-ChildItem (Join-Path $pakketDir "skills") -Directory | Select-Object -ExpandProperty Name
$mist = @()
foreach ($s in $verwacht) { if (-not (Test-Path (Join-Path $claudeDir "skills\$s"))) { $mist += $s } }
if ($mist.Count -eq 0) { Goed "Alle $($verwacht.Count) skills geinstalleerd" }
else { Stuk "Niet geinstalleerd: $($mist -join ', ')" }

# B3 — handtekening
$sigPad = Join-Path $claudeDir "assets\agyle-signature-url.html"
if (Test-Path $sigPad) {
    $sig = Get-Content $sigPad -Raw
    if ($sig -match '\{\{[A-Z_]+\}\}') { Stuk "Handtekening bevat onvervangen placeholders" }
    else { Goed "Handtekening gegenereerd" }
    if ($sig -match 'abdul\.malik@agyle\.nl' -and $rt -and $rt.email -notlike "*abdul*") {
        Stuk "Handtekening bevat nog Abduls mailadres — draai INSTALL.ps1 opnieuw"
    }
} else { Stuk "Handtekening ontbreekt: $sigPad" }

# B4 — hooks geregistreerd
$settingsPad = Join-Path $claudeDir "settings.json"
if (Test-Path $settingsPad) {
    $inhoud = Get-Content $settingsPad -Raw
    foreach ($h in @("update_progress.py", "update_handover.py")) {
        if ($inhoud -like "*$h*") { Goed "$h geregistreerd als Stop-hook" }
        else { Stuk "$h niet geregistreerd in settings.json" }
    }
    try { $null = $inhoud | ConvertFrom-Json; Goed "settings.json is geldige JSON" }
    catch { Stuk "settings.json is geen geldige JSON — herstel via settings.json.bak" }
} else { Stuk "settings.json ontbreekt" }

# B5 — hookbestanden aanwezig en uitvoerbaar
foreach ($h in @("update_progress.py", "update_handover.py")) {
    $p = Join-Path $claudeDir "hooks\$h"
    if (Test-Path $p) { Goed "$h staat klaar" } else { Stuk "$h ontbreekt in ~/.claude/hooks" }
}

# B6 — MCP-servers (configuratie, niet of je ingelogd bent)
$mcpUit = & claude mcp list 2>&1 | Out-String
if ($LASTEXITCODE -eq 0) {
    foreach ($srv in @("ms365", "agyle", "github", "plaud")) {
        if ($mcpUit -match $srv) { Goed "MCP '$srv' geconfigureerd" }
        else { Waarschuw "MCP '$srv' nog niet geconfigureerd — zie docs\03-MCP-SETUP.md" }
    }
    Write-Host "            (of je ook ingelogd bent zie je met /mcp in Claude Code)" -ForegroundColor DarkGray
} else { Waarschuw "Kon 'claude mcp list' niet draaien" }

# ================================================================ SLOT
Write-Host ""
Write-Host ("=" * 55)
if ($fouten -eq 0 -and $waarschuwingen -eq 0) {
    Write-Host "Alles in orde. Je kunt aan de slag." -ForegroundColor Green
    exit 0
} elseif ($fouten -eq 0) {
    Write-Host "Geen fouten, $waarschuwingen aandachtspunt(en) hierboven." -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "$fouten fout(en) en $waarschuwingen aandachtspunt(en)." -ForegroundColor Red
    Write-Host "Los de fouten op en draai dit script opnieuw." -ForegroundColor Red
    exit 1
}
