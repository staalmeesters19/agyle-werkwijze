# Losse prompt — onderhoudscontract

Voor gebruik zonder skill-installatie: plak onderstaande prompt in het gesprek en hang `reference/contract-structuur.md` erbij (of plak de inhoud eronder). De PDF-stap draai je daarna met `scripts/build_contract_pdf.py`.

---

Je schrijft een onderhouds-/beheerovereenkomst tussen een IT-leverancier en zijn klant, in de stijl van een zakelijke brief die toevallig een contract is. Werk in deze volgorde en wacht op mijn antwoord waar dat gevraagd wordt.

**Stap 1 — Intake.** Stel in één keer, in maximaal acht regels, de volgende vragen. Sla over wat ik al verteld heb; ontbreekt iets, doe dan een expliciet benoemd voorstel in plaats van te blokkeren.
1. Partijen: leverancier en klant (naam, rechtsvorm, adres, ondertekenaar + functie), plus het inhoudelijke aanspreekpunt.
2. De dienst in één zin, en de huidige status (pilot, productie, aantal omgevingen/deployments).
3. Is dit een vervolg op een eerdere getekende offerte? Datum en het uurtarief daaruit.
4. Hosting: wie neemt de omgeving af, wie beheert netwerk/server/repository, draait het on-prem of publiek benaderbaar?
5. Pakketten: hoeveel uur per maand en welk tarief, standaard twee varianten (Basis en Uitgebreid) met volumekorting op de grootste.
6. Eenmalig inrichtings-/migratiewerk bij livegang? Uurtarief plus urenband.
7. Looptijd en opzegtermijn.
8. Welke algemene voorwaarden gelden, en zijn er eigendoms-/continuïteitsafspraken uit de eerdere offerte?

**Stap 2 — Interne calculatie eerst, contract daarna.** Schrijf een intern document (`INTERN - Onderhoudscontract calculatie (NIET naar klant).md`) met: pakketopbouw (uren × tarief → maandbedrag → jaaromzet), de impliciete volumekorting in €/mnd én %, het buiten-pakket-tarief (altijd het volle uurtarief, nooit het kortingstarief), marge-overwegingen, onderhandelruimte per knop mét ondergrens, en wat bewust níét in het contract komt (variabele kosten zoals API-/tokenverbruik, aparte scopes). Vraag mij de prijzen te bevestigen voordat je verder gaat.

**Stap 3 — Contracttekst.** Schrijf de klantversie in markdown, volgens de bijgevoegde artikelstructuur: kop met meta-blok (Betreft, Datum, Gericht aan, Inhoudelijk contact), aanhef, openingsalinea, daarna elf genummerde artikelen — 1 Introductie en context, 2 Opzet: drie pilaren, 3 Onderhoudspakketten, 4 Wat valt binnen het pakket en wat erbuiten, 5 Beschikbaarheid en werkwijze, 6 Hosting en eenmalige inrichting, 7 Looptijd/verlenging/opzegging, 8 Indexatie, 9 Randvoorwaarden opdrachtgever, 10 Uitsluitingen en risicoverdeling, 11 Algemene voorwaarden, IE en continuïteit — en een ondertekenblok met twee kolommen.

Houd je aan deze regels:
- Inspanningsverplichting, geen resultaatsverplichting. Geen boeteclausules, geen P1–P4-matrix, geen uptime-percentages.
- Scherpe rolverdeling: leverancier = applicatie, updates, containerbeheer, scans en rapportage; klant = hosting, netwerk, server, repository/pipeline, toegang. Dit is de belangrijkste aansprakelijkheidsknop in het document; houd de bewoordingen consistent tussen artikel 6, 9 en 10.
- Elke belofte krijgt een deliverable. "Beveiliging" bestaat pas als er een maandelijkse kwetsbaarheidsscan én een korte maandelijkse rapportage tegenover staan; zet die in het pakket.
- Eenmalige inrichting altijd als urenband op uurbasis, met de onzekerheden expliciet benoemd — nooit een vast bedrag.
- Geen marge, korting-in-% of verkoopargumentatie in de contracttekst. Eén feitelijke "Ter overweging"-box bij de pakketten mag; de aanbeveling zelf hoort in de begeleidende mail.
- Continuïteitsclausule altijd opnemen: bij beëindiging van de leverancier gaan broncode, documentatie, configuratie, scripts, componenten en toegangen onvoorwaardelijk en zonder vergoeding over naar de klant.
- Nederlands, volledige zinnen, zakelijk-warm, geen jargon-stapelwerk. Bedragen als `€ 175` en `€ 1.600`.

**Stap 4 — Opmaakconventies** (zodat de PDF-generator het herkent):
- Meta-regels bovenaan als `**Betreft:** …` tot de eerste `---`; optioneel `**Ondertitel:** …`.
- Artikelkoppen als `## 3. Onderhoudspakketten`.
- `:::teal … :::` voor de "Ter overweging"-box, `:::box … :::` voor bedragen/voorwaarden.
- Ondertekenblok als tabel met de kop `| Te leveren door | Te leveren aan |` en de rijen `Datum:`, `Handtekening:`, `**Naam** — Functie`, `Bedrijf, adres`.

**Stap 5 — Oplevering.** Geef de klantversie en de interne versie als aparte bestanden, en schrijf een korte begeleidende mail: aanbeveling voor het zwaarste pakket, de uren-onderbouwing (proactief onderhoud + rapportage + deployment-buffer, niet "aantal storingen"), en het comfort-argument dat de overeenkomst na de eerste termijn maandelijks opzegbaar is. Sluit af met de punten die nog openstaan (ondertekenaar, ingangsdatum, definitieve tarieven).
