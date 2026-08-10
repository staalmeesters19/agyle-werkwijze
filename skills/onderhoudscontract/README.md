# Onderhoudscontract — skill + template

Reproduceert een onderhouds-/beheerovereenkomst in exact hetzelfde formaat en dezelfde opmaak als het FDS-onderhoudscontract (Agyle → Van den Pol, juli 2026): interne calculatie eerst, dan de contracttekst in 11 artikelen, dan een branded PDF met accentbalk, logo, genummerde artikel-badges en ondertekenblok.

## Inhoud

```
onderhoudscontract/
  SKILL.md                          — de skill: werkwijze in 5 stappen (intake → PDF)
  PROMPT.md                         — dezelfde werkwijze als losse copy-paste prompt
  reference/
    contract-structuur.md           — de 11 artikelen: doel, modelzinnen, valkuilen + opmaak-cheatsheet
    calculatie-template.md          — interne calculatie/onderhandelruimte (nooit naar de klant)
  templates/
    contract-template.md            — invulbaar skelet, direct renderbaar
  scripts/
    build_contract_pdf.py           — markdown → branded PDF (geen pip-dependencies)
  assets/
    logo_base64.txt                 — Agyle-logo, base64 (vervangbaar)
```

## Installeren als skill

Kopieer de map naar de skills-directory:

```powershell
Copy-Item -Recurse "onderhoudscontract" "$HOME\.claude\skills\onderhoudscontract"
```

Daarna in Claude Code: `/onderhoudscontract`, of gewoon "maak een onderhoudscontract voor <klant>" — de skill triggert op onderhoudscontract / beheerovereenkomst / SLA / maandpakket / servicecontract.

Werk je zonder skills (Claude.ai, ChatGPT, whatever): plak `PROMPT.md` in het gesprek en hang `reference/contract-structuur.md` erbij. Zelfde resultaat, alleen de PDF-stap draai je dan handmatig met het script.

## PDF genereren

```bash
python scripts/build_contract_pdf.py "Onderhoudscontract Agyle - Klant - Dienst (concept).md"
```

De PDF verschijnt naast de markdown. Opties:

| Optie | Doel |
|---|---|
| `-o pad.pdf` | ander outputpad |
| `--logo pad/logo_base64.txt` | ander logo (base64-tekst, zonder `data:`-prefix) |
| `--brand "A G Y L E"` | merknaam linksonder |
| `--footer "…"` | footerregel rechtsonder |
| `--keep-html` | schrijft ook de tussen-HTML weg (handig bij opmaak-debug) |

**Vereist:** Python 3 en Edge of Chrome (headless print). Geen pip-packages. Staat de browser ergens anders: `CONTRACT_PDF_BROWSER=/pad/naar/msedge.exe`.

Een `.html`-bestand als input wordt als body doorgegeven met dezelfde CSS eromheen — escape hatch voor opmaak die de markdown-conventies niet aankunnen. `{{LOGO}}` in die HTML wordt vervangen door het base64-logo.

## Andere huisstijl

Twee dingen aanpassen: `assets/logo_base64.txt` (of `--logo`) en het `CSS`-blok bovenin `scripts/build_contract_pdf.py`. De kleuren zitten op drie plekken: de accentbalk (`linear-gradient`), de artikel-badges/tabelkoppen (`#000` + `#7ec8e3`) en de box-randen. Verder is alles kleurloos, dus een andere huisstijl is een kwestie van die twee hex-waarden vervangen.

## Werkvolgorde (kort)

1. **Intake** — partijen, dienst, hosting, pakketten, looptijd, voorwaarden.
2. **Interne calculatie eerst** — uren × tarief, volumekorting, marge, onderhandelruimte, ondergrens. Prijzen laten bevestigen.
3. **Contracttekst** — 11 artikelen volgens `reference/contract-structuur.md`.
4. **PDF** — script draaien, doorbladeren op paginabreuken en bedragen.
5. **Opleveren** — klantversie + interne versie apart, plus een begeleidende mail waarin de aanbeveling staat (die hoort níét in de contracttekst).

De harde regels die het document zijn vorm geven: inspanningsverplichting zonder boeteclausules, scherpe rolverdeling leverancier vs. klant, elke belofte gekoppeld aan een deliverable (scan + rapportage), variabele kosten buiten het vaste maandbedrag, en een continuïteitsclausule die overdracht bij beëindiging onvoorwaardelijk regelt.
