---
name: onderhoudscontract
description: Stel een onderhouds-/beheerovereenkomst op in de Agyle-huisstijl — intake, interne calculatie, contracttekst (markdown) en branded PDF met genummerde artikelen en ondertekenblok. Gebruik wanneer een project van bouwfase naar beheerfase gaat en er een maandpakket/SLA-achtige overeenkomst nodig is ("onderhoudscontract", "beheerovereenkomst", "SLA", "maandpakket", "servicecontract").
---

# Onderhoudscontract

Levert twee documenten per traject:

1. **Klantversie** — `Onderhoudscontract <Leverancier> - <Klant> - <Dienst> (concept).md` + branded PDF.
2. **Interne versie** — `INTERN - Onderhoudscontract calculatie (NIET naar klant).md` met marge, onderhandelruimte en positionering. Gaat **nooit** mee naar de klant.

Schrijf altijd eerst de interne calculatie, dan pas de contracttekst. De prijsstelling is een besluit, geen bijproduct van het schrijven.

## Stap 1 — Intake

Stel deze vragen in één keer (max. ~8 regels, geen vragenlijst van drie pagina's). Wat de gebruiker al heeft verteld niet opnieuw vragen.

- **Partijen** — leverancier (naam, rechtsvorm, adres, ondertekenaar + functie) en klant (idem). Wie tekent, wie is inhoudelijk aanspreekpunt?
- **Dienst** — wat wordt onderhouden, in één zin, en wat is de huidige status (pilot / productie / aantal deployments)?
- **Voorgeschiedenis** — is er een eerdere getekende offerte/overeenkomst waar dit een vervolg op is? Datum en uurtarief daaruit.
- **Hosting** — wie neemt de omgeving af, wie beheert netwerk/server/repository? Draait het on-prem of publiek benaderbaar?
- **Pakketten** — hoeveel uur per maand, welk tarief, hoeveel varianten (standaard: twee — Basis en Uitgebreid, met volumekorting op de grootste)?
- **Eenmalige inrichting** — is er migratie-/opzetwerk bij livegang? Uurbasis + urenband.
- **Looptijd** — vaste termijn, daarna opzegtermijn.
- **Algemene voorwaarden** — welke set (bijv. NL Digital, KvK-nummer), en gelden er eigendoms-/continuïteitsafspraken uit de eerdere offerte?

Ontbreekt er iets? Doe een expliciet benoemd voorstel in plaats van te blokkeren. Bij ambiguïteit over een naam, datum of bedrag: één regel terugkoppelen hoe je het leest, dan door.

## Stap 2 — Interne calculatie eerst

Schrijf `reference/calculatie-template.md` vol met de echte cijfers. Vaste kern:

- Pakketopbouw met uren × tarief → maandbedrag → jaaromzet per pakket.
- Impliciete volumekorting op het grootste pakket, uitgedrukt in €/mnd én % — verdedigbaar als commitment-beloning.
- Buiten-pakket-tarief = het **volle** uurtarief (nooit het kortingstarief).
- Marge-overwegingen: welke kosten liggen bij wie, waar zit break-even, wat gebeurt er in een rustige maand.
- Onderhandelruimte per knop (tarief grootste pakket, looptijd, SLA-zwaarte) mét ondergrens.
- Wat **niet** in het contract komt en waarom (variabele kosten zoals API-/tokenverbruik, aparte scopes).

Laat de gebruiker de prijzen bevestigen vóór je de klantversie schrijft.

## Stap 3 — Contracttekst schrijven

Volg `reference/contract-structuur.md` — dat is de vaste artikelindeling (11 artikelen) met per artikel het doel, de modelzinnen en de valkuilen. Wijk daar alleen van af als de dienst het vraagt; nummering blijft dan doorlopend.

Schrijfregels:

- **Toon**: zakelijk-warm, volledige zinnen, geen juridisch jargon-stapelwerk. Het is een brief die toevallig een contract is: aanhef ("Geachte heer/mevrouw X,"), openingsalinea die de context schetst, dan de artikelen.
- **Inspanningsverplichting, geen resultaatsverplichting.** Geen boeteclausules, geen P1–P4-matrix, geen uptime-percentages die je niet kunt waarmaken.
- **Rolverdeling scherp**: per verantwoordelijkheid expliciet wie wat doet (leverancier = applicatie/container/updates/scans/rapportage; klant = hosting, netwerk, server, repository/pipeline, toegang). Dit is de belangrijkste aansprakelijkheidsknop in het hele document.
- **Elke belofte moet een deliverable zijn.** "Beveiliging" is pas iets waard als er een maandelijkse scan én een korte rapportage tegenover staat.
- **Prijzen uitsluitend in de klantversie zoals afgesproken** — marge, korting-in-%, onderhandelruimte en "waarom dit pakket" horen in de interne versie, niet in de contracttekst.
- **Advies-/verkooptekst hoort in de begeleidende mail**, niet in het contract. Het contract beschrijft de pakketten neutraal; de aanbeveling ("wij adviseren Uitgebreid") gaat mee in de mail.
- Uitzondering: één **:::teal**-box met "Ter overweging" mag in het contract, waarin je de keuze tussen de pakketten feitelijk toelicht (groei, volume, gunstiger tarief). Feiten, geen superlatieven.

## Stap 4 — PDF genereren

```bash
python scripts/build_contract_pdf.py "pad/naar/Onderhoudscontract ... (concept).md"
```

De PDF komt naast de markdown te staan. Opties: `-o` voor een ander pad, `--logo` voor een andere `logo_base64.txt`, `--footer` en `--brand` voor een andere afzender, `--keep-html` om de tussen-HTML te bewaren.

Vereist Python 3 en Edge of Chrome (headless print). Geen pip-packages.

Markdown-conventies die het script begrijpt staan bovenin `scripts/build_contract_pdf.py` en in `reference/contract-structuur.md`. Belangrijk:

- `**Betreft:** …`-regels bovenaan (tot de eerste `---`) worden de meta-tabel.
- `## 3. Titel` levert de zwarte genummerde badge; zonder nummer geen badge.
- `:::teal … :::` = opvallende box, `:::box … :::` of `> …` = rustige box.
- De tabel met kop `| Te leveren door | Te leveren aan |` wordt automatisch het twee-koloms ondertekenblok — regelvolgorde: `Datum:`, `Handtekening:`, `**Naam** — Functie`, `Bedrijf, adres`.

Controleer de PDF daarna op: geen artikelkop onderaan een pagina zonder tekst, tabellen niet over een paginarand, bedragen en datums consistent met de interne calculatie.

## Stap 5 — Opleveren

- Klantversie (md + PDF) in de offerte-/contractmap van het project; interne calculatie ernaast met `INTERN -` in de bestandsnaam.
- Concept-mail bij het contract: kort, de aanbeveling voor het zwaarste pakket, de onderbouwing van de uren (proactief onderhoud + rapportage + deployment-buffer, niet "aantal storingen"), en het comfort-argument (na de eerste termijn maandelijks opzegbaar, dus downgraden kan).
- Meld expliciet welke punten nog openstaan (ondertekenaar, ingangsdatum, definitieve tarieven).

## Valkuilen

- Contract schrijven vóór de calculatie rond is → tarieven die je later moet terugdraaien.
- Prijsargumentatie in de contracttekst → leest als verkoop, verzwakt het document.
- Variabele kosten (API-/tokenverbruik, licenties) in een vast maandbedrag stoppen → marge lekt weg; apart beleggen.
- Een korting geven op het kleinste pakket → ondermijnt het net afgesproken uurtarief.
- SLA-taal overnemen uit een template van een grote leverancier (boetes, uptime-garanties) terwijl de relatie en de bemensing dat niet dragen.
