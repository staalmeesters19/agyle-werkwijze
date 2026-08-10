---
name: voorstel-site
description: Bouw een klant-voorstel of presentatie als premium scrollytelling-microsite in plaats van een PDF of PowerPoint — full-bleed kleurbanden, fluid clamp-typografie, scroll-reveals, pincode-gate, handgebouwde SVG-dataviz en optioneel ondertekenen in de pagina. Gebaseerd op een volledige teardown van Clark's Harwig-voorstel. Gebruik wanneer Abdul vraagt om "een voorstel-site", "voorstel als website", "presentatie waarmee je indruk maakt", "microsite voor klant X", "zoiets als Clark deed", of een offerte/pitch die visueel moet knallen.
argument-hint: <klant> — <waar het voorstel over gaat>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, PowerShell, Agent, TodoWrite, ToolSearch
---

# Skill: `/voorstel-site` — voorstel als premium microsite

**Aanroep:** `/voorstel-site <klant> — <onderwerp>`
Voorbeelden: `/voorstel-site Kropman — onderhoudsrapportage-agent`, `/voorstel-site Bohn — Belegungsliste PoC`.

Een PDF is een afbeelding van een document. Deze vorm is een **ruimte**: je gaat ergens naar binnen
(gate), je beweegt erdoorheen (scroll-reveal), dingen blijven staan terwijl jij loopt (sticky), en
aan het eind is er een deur (akkoord). Geen van die vier is uit te drukken in pagina's. Dát is
waarom het indruk maakt — en het kost samen ~4 uur bouwtijd.

## Bronmateriaal — lees dit vóór je bouwt

| Bestand | Wat |
|---|---|
| `reference/PLAYBOOK.md` | **Het operationele recept.** 10 hoofdstukken, alle exacte waarden. Dit is de autoriteit |
| `reference/SPIN-EN-CIJFERS.md` | **De rekenlaag.** Implicatie kwantificeren, saldering, terugverdientijd, need-payoff |
| `assets/chassis.css` | Plakbare tokenlaag + sectie-chassis + motion + componenten, in Agyle-kleuren |
| `assets/chassis.js` | Observer, stagger, header, gate, count-up — kant-en-klaar |
| `reference/BRONNEN.md` | Waar de teardown-bron en de 8 deelanalyses staan |

Lees minimaal §3 (designsysteem), §4 (sectie-grammatica) en §9 (bouwvolgorde) van het playbook
voordat je één regel schrijft. De rest raadpleeg je per onderdeel.

## Werkwijze

### Stap 0 — beslis de prijsroute (blokkerend, één vraag aan Abdul)

`agyle-business/CLAUDE.md`: *geen prijzen in klant-facing documenten tenzij Abdul dat expliciet
vraagt.* Een ondertekenbare voorstelsite zónder prijs is intern inconsistent — je kunt niet laten
accorderen wat je niet toont. Vraag één keer, expliciet:

- **Route A** — mét prijs: dan ook mét totaal over de looptijd, mét btw, mét meerjarenlast.
- **Route B** — zonder prijs: kostensectie wordt scope + doorlooptijd + tijdsinvestering, CTA wordt
  "Akkoord op scope".

Niet doen: half. Twee van de drie prijzen is slechter dan beide varianten. Zie playbook §8.4.

### Stap 1 — discovery-oogst (±1 u)

Haal uit transcripts, mailthreads en de klant-CLAUDE.md **minstens 25 verifieerbare klantfeiten**:
openstaande rollen/problemen en hoe lang al · huidige tool + kosten + resultaat · concurrenten bij
naam · mensen op de afdeling met hun rol · het groeidoel · en **minstens één letterlijk idioom uit
het gespreksverslag**.

Volg hier de business-regel: klantcontext ophalen vóór strategie-output. Nooit een generiek
skelet invullen.

Quotum voor de rest van de bouw: **elke kaart of blok bevat minimaal één getal, jaartal, eigennaam
of bedrag dat de klant zelf heeft genoemd.**

Haal in hetzelfde gesprek de zes kostenposten op uit `reference/SPIN-EN-CIJFERS.md` §1 —
frequentie, tijd per keer, uurtarief, directe uitgaven nu, gemiste opbrengst, hoe lang al. Zonder
die zes bestaat er geen rekensom en blijft het voorstel bij "dit kost veel tijd".

### Stap 1b — de rekenlaag (±1 u, blokkerend vóór de copy)

De I van SPIN is een vermenigvuldiging, geen bijvoeglijk naamwoord. Werk `SPIN-EN-CIJFERS.md` §2–§3
uit vóórdat je één kaart schrijft — de uitkomst bepaalt de koppen.

1. **A — kosten van niets doen per jaar:** verborgen uren + directe uitgaven nu + gemiste opbrengst.
   Alleen posten die de klant zelf noemde, met bron en datum per regel.
2. **B — nieuwe last per jaar, álles:** onze fee + doorlopende licenties + verbruiks-/advertentie-
   budget + **de interne uren die wij van de klant vragen**. Die laatste post laat iedereen weg en
   elke klant rekent hem zelf uit.
3. **C — saldering in één tabel op één scherm**, met netto per jaar, terugverdientijd en het
   **totaal over de looptijd**. Dat laatste getal is het duurste vastgoed op een offerte.

Bandbreedtes, geen puntgetallen. Reken A op de ondergrens en B op de bovengrens, zodat de netto-
uitkomst je vloer is en niet je plafond — underpromise zit in de rekenrichting, niet in de toon.

Bij route B (geen tarieven in het klantstuk) vervalt de rekensom **niet**: kolom "Nu" is hun geld,
niet jouw tarief. Zie §6.

### Stap 2 — copy op het skelet (4–6 u)

Schrijf **eyebrows eerst** — dat is je argumentatie, zichtbaar gemaakt. De volgorde uit playbook
§4.2 is een SPIN-skelet: Jullie situatie → Prioriteiten → Onze aanpak → In de praktijk → Fasering →
Kosten → De lange termijn → Rolverdeling → Tijdsinvestering → CTA.

Vier regels die je niet overtreedt:

1. **De pijnmuur eindigt op een compliment.** Vijf kaarten die tekortdoen, de zesde erkent wat er al
   staat. De koper hoeft geen falen toe te geven om te kopen.
2. **De vijand is nooit de klant.** Aanvallen gaan naar hun leveranciers en tools, nooit naar hun
   eigen proces. "De mailbox blijft heilig, maar krijgt er een datalaag bovenop."
3. **Spiegel ≥10× hun vakjargon**, inclusief dat ene letterlijke idioom.
4. **Consequent "jullie"** — nooit "u", nooit "je". Grep erop vóór levering.
5. **Elke pijnkaart draagt zijn eigen bedrag of duur.** "Kost veel tijd" is geen implicatie;
   "€3.400 per maand" en "staat al vier jaar open" zijn het wel. De duur is de vermenigvuldiger.
6. **De kostensectie eindigt op een vraag, niet op een conclusie.** Niet "dus jullie besparen X",
   maar *"als dit over negen maanden staat — wat doet dat met jullie planning voor 2027?"* Zij
   noemen dan een groter getal dan het jouwe, en het is van hen. Dat is de N van SPIN.

Tijdsinvestering-sectie komt **ná** de prijs: de laatste zorg die je wegneemt is capaciteit, niet geld.

### Stap 3 — bouwen

Kopieer `assets/chassis.css` en `assets/chassis.js` naar het projectbestand en bouw de secties.
Chassis is eenmalig; per klant verandert alleen de content-laag.

Kleurpartituur (playbook §4.2): **donker = wij vragen iets** (kosten, tijdsinvestering) ·
**licht = jullie krijgen iets** (situatie, tijdlijn, rolverdeling) · **sky alleen hero/aanpak/CTA**.
Nooit twee identieke achtergronden achter elkaar.

Grafiek alleen als **alle vier** de voorwaarden uit §6.1 haalbaar zijn (zelfde font, eenheid op de
as, één grootheid per as, marker klopt met bijschrift). Anders: **drie getallen op een rij** —
eerlijker en leest sneller.

### Stap 4 — de verplichte gates vóór levering

| Gate | Check |
|---|---|
| **Render-QA** | 375 / 800 / 1024 / 1440 / 1920 px **plus printvoorbeeld**. Kijk ernaar. Dit is de goedkoopste QA die bestaat en het is de stap die iedereen overslaat |
| **JS uit + reduced-motion aan** | Pagina blijft leesbaar, niets op `opacity: 0` |
| **AV-kruistabel** | Webpagina · exportbestand · algemene voorwaarden in één tabel met drie kolommen. Geen belofte op de pagina die de AV tegenspreekt. Dit is de duurste fout die er is |
| **Rekengate** | Saldering in één tabel op één scherm? Kolom B compleet, inclusief interne uren van de klant? Netto, terugverdientijd én totaal over de looptijd zichtbaar? Elke regel in kolom A herleidbaar naar een klantopgave met datum? Zie `SPIN-EN-CIJFERS.md` §7 |
| **Drie vragen** | Totaal over de looptijd? Wat gebeurt er met het gebouwde bij stoppen? Waar ligt de norm waaronder we zakken? Alle drie beantwoord op de pagina |
| **Naam-check** | Bedrijfsnaam correct, óók in alt-teksten. Clark schreef "Harwig Beveiligingstechniek" op een document dat zijn geloofwaardigheid ontleent aan aandacht |
| **Bedragen** | Eén constantenobject als bron; pagina, samenvatting en export renderen daaruit |

## Wat dit onderscheidt van Clark

Vorm overtreffen is haalbaar; **eerlijkheid overtreffen is goedkoop.** Clark scoort nul op de drie
vragen hierboven, heeft nul bewijsvoering (geen case, geen referentie, geen klantlogo — alleen
leverancierslogo's), en laat twee kernbeloften door de eigen algemene voorwaarden tegenspreken.

En ze **salderen nooit**: €11.000–13.000 besparing en €3.600–6.000 nieuwe licentie staan allebei op
de pagina, ~5000px uit elkaar, nooit in één tabel. Hun kostencurve loopt naar nul terwijl die
licentie doorloopt.

Eén echte case met echte cijfers, plus één eerlijke salderingstabel, slaat dat hele blok uit elkaar.
Dat is het gat om in te gaan staan.

## Verhouding tot andere skills

- `/prep-klant` levert de SPIN-context die stap 1 voedt — draai die eerst als de deal-state onhelder is.
- `/notulen` levert de transcripts waar de klantfeiten en het idioom uit komen.
- `_agyle_branding` houdt de merkkleuren (`#000000` + `#97D4E8`); `chassis.css` leidt daar het
  paginazwart en de tint-ladder uit af.

## Effect-dragers op rendement — waar je je uren stopt

Als de tijd krap is, bouw in deze volgorde. De top-6 kost samen ~4,25 uur en levert het overgrote
deel van het duur-gevoel.

| # | Drager | Uren |
|---|---|---:|
| 1 | Eigen webfont, self-hosted woff2 | 0,5 |
| 2 | Sticky zijkolom in een split-sectie | 0,5 |
| 3 | Full-bleed sectiekleuren met veel lucht | 1,0 |
| 4 | `.reveal` + IntersectionObserver | 1,0 |
| 5 | Header die wegduikt bij scroll | 0,5 |
| 6 | Hero-collage | 0,75 |

Wat je overslaat als het moet: de cirkel-funnel, de custom grafiek en de handtekening+PDF-flow —
samen ~14 uur voor marginaal effect. **Klantfeiten hebben de laagste ratio en het hoogste plafond:**
vorm koopt aandacht, feiten kopen geloofwaardigheid. Alleen op ratio optimaliseren levert een mooie
lege huls.
