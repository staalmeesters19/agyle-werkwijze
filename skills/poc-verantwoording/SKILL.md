---
name: poc-verantwoording
description: Bereid Abdul volledig voor op een demo/go-no-go waarin een (vibecoded) PoC verantwoord moet worden richting klant. E2E-verificatie zoals de klant het ziet, waarheidsladder (nooit "identiek" claimen boven het bewezen niveau), cel-voor-cel-vergelijk met redenen, functionele uitleg voor de presentator, master-draaiboek met letterlijke spreekteksten, en generale repetitie. Gebruik bij "demo voorbereiden", "PoC verantwoorden", "go/no-go meeting", "ik weet niet wat er gebouwd is".
---

# PoC-verantwoording — van vibecoded bouwsel naar verdedigbare demo

**Situatie waarvoor deze skill bestaat:** er is een PoC gebouwd (grotendeels via prompts — Abdul kent de binnenkant niet), er staat een demo/go-no-go met de klant, en het resultaat moet eerlijk en overtuigend verantwoord worden. De presentator moet alles kunnen uitleggen zonder de code te kennen.

**Uitgangspunten (hard):**
- Abdul presenteert; hij moet élk getal, élke claim en élk mechanisme in eigen woorden kunnen uitleggen. Alles wat hij niet kan uitleggen, hoort niet in de demo.
- Nooit iets claimen dat niet zelf nagedraaid is (zie klantregel `verify-agent-claims-before-client-comms`).
- Underpromise/overdeliver: verrassingen bewaren voor de meeting, beloften alleen op bewezen niveau.

## Fase 1 — Feiten & verwachtingen (wat is er beloofd?)

1. Lees contract/agreement + alle meetingverslagen en mailthreads uit de klantmap. Noteer het acceptatiecriterium **in de letterlijke woorden van de klant** (bv. "we have to come to the same results") — dat wordt het anker van de hele demo.
2. Bouw een **verwachtingen-matrix**: per klantuitspraak → wat beloofd is → wat geleverd is → status (gehaald / overgeleverd / bewust fase 2). Multi-agent fan-out over de bronnen als het er veel zijn.
3. Alles wat bewust NIET gebouwd is expliciet als roadmap framen, nooit verstoppen.

## Fase 2 — E2E-verificatie (werkt het écht, zoals de klant het ziet?)

1. **Start de juiste app op een eigen poort en verifieer dat 't de juiste is — vóór je een URL aan Abdul geeft.** Meerdere PoC's op deze machine draaien op de default-poort (Streamlit 8501); zonder pinning toon je per ongeluk de verkeerde app. Dus: (a) start met een expliciete, unieke poort (bv. `--server.port 8511`), (b) start uit de juiste projectmap, (c) bevestig de identiteit van wat er draait — check `page_title`/route in de broncode én dat de server op die poort antwoordt (HTTP 200) — en (d) noem in de URL welke poort de juiste is en welke je dicht moet laten. Nooit "draait op 8501" aannemen.
2. Draai de volledige flow **als klant**: verse input, schone omgeving, dezelfde knoppen die de klant ziet. Niet de dev-route, niet een cached resultaat.
2. Instellingen vastleggen die het klantbeeld bepalen (taal, defaults zoals reserve-%) — en in het draaiboek zetten welke stand de demo gebruikt.
3. Trage/dure/onvoorspelbare paden (agent-runs, vision): **nooit live als wachtmoment** — vooraf draaien en als voorbereide resultaten klaarzetten. Meet doorlooptijd en kosten; dat worden de demo-getallen.
4. Fallbacks voorbereiden: wat toon je als de live run faalt (een verse job van dezelfde ochtend), en degradeert de flow netjes (zichtbare melding i.p.v. stil verkeerd resultaat)?
5. Na de laatste groene run: **stack bevriezen**. Elke wijziging daarna = opnieuw testen of niet doen.
6. Datagaranties die de klant gaat vragen zelf empirisch bewijzen (bv. upload-only: referentiedata fysiek verwijderen en aantonen dat de uitkomst gelijk blijft).

## Fase 3 — Waarheidsladder (de kern: wat betekent "hetzelfde resultaat"?)

Claim nooit een hogere trede dan je bewezen hebt. De ladder:

1. **Tellingen** — totalen per type gelijk. (Zwakste claim; zeg nooit "identiek" op basis hiervan.)
2. **Structuur** — module-/onderdelenlijst gelijk (types, aantallen, volgorde).
3. **Semantische koppeling** — elk punt van ons 1-op-1 gematcht aan een punt van de klant, op betekenis (niet op positie of woordgelijkenis!). Onmatchbare punten expliciet als "extra bij ons" / "ontbreekt bij ons", elk met bronverklaring.
4. **Cel-voor-cel** — per gekoppelde rij élke kolom vergeleken; elk verschil krijgt een uit de bron bewijsbare reden.
5. **Vorm** — zelfde sjabloon/kolommen/naamgeving als het klantdocument.

Werkwijze trede 3-4:
- Parseer het klantreferentie-document **kolomzuiver** (coördinaten/tabellen, niet tekstvolgorde-giswerk).
- Koppel semantisch; verifieer twijfelparen tegen het bronmateriaal (welke groep/pagina hoort het punt bij), niet tegen woordovereenkomst — synoniemen en engineersnamen misleiden fuzzy matching.
- Maak een **vergelijk-werkboek** (Excel): per rij wij/zij naast elkaar, per kolom GELIJK of reden; kleurcodes; apart blad voor sjabloon-/instellingsverschillen. Dit is intern spiekmateriaal, niet voor de klant.
- Categoriseer elk celverschil: (a) instelling van de run, (b) sjabloon/kolommen, (c) naamconventie, (d) info die in de bron staat maar nog niet overgenomen, (e) expert-kennis die nérgens staat (nooit gokken — open laten + "zu bestätigen"), (f) fout/oddity in het klantdocument (als vráág formuleren, nooit als verwijt).
- De klant-framing volgt uit de ladder: *"same data points, same modules — every difference is explained; the form follows your template as soon as you send it."* Benoem het vormverschil zélf, vóórdat de klant het doet.

## Fase 4 — Functioneel begrip voor de presentator ("ik weet niets"-proof)

Schrijf een sectie in het draaiboek die per output-element beantwoordt: **waar komt dit vandaan → via welk mechanisme → met welke garantie**. In gewone taal, geen code. Minimaal:
- de route-keuzes die het systeem zelf maakt (en waaraan de presentator ze herkent op het scherm);
- waar elk soort gegeven vandaan komt (tabel, tekening, afleiding uit standaard) en wat het systeem doet bij ontbrekende informatie (expliciet melden, nooit gokken);
- de regels-hiërarchie (officiële standaard → klantbrede conventie → projectconfig) en waarom die schaalbaarheid geeft;
- de 3-5 getallen die uit het hoofd moeten (kosten/doorlooptijd/resultaten per referentieproject).
Toets: Abdul moet elke [ZEG]-zin kunnen laten volgen door een juist antwoord op "how does it do that?".

## Fase 5 — Master-draaiboek (één scroll-document voor tijdens de meeting)

Eén bestand, chronologisch, met per moment:
- **[KLIK]** wat je doet (exacte tab/bestand/knop), **[ZEG]** de letterlijke zinnen in de meeting-taal, **→** de boodschap die moet landen.
- Wachtmomenten gevuld met voorbereide resultaten van ándere projecten/onderdelen (bewijst generalisatie) — per item: wat het is, waar je klikt, wat je zegt, valkuilen.
- De **volledige vragenlijst voluit in de meeting-taal**, in vraagvolgorde (klapstuk-vraag apart aan het eind), zodat geen tweede document nodig is.
- Spiekbrief: verwachte vragen + letterlijke antwoordzinnen (inclusief de prijsvraag-afhouder; **nooit prijzen in de meeting**).
- Niet-doen-lijst en fallbacks.
- Klaarzet-checklist (vensters, bestanden, instellingen, login) met tijdstippen.
Hulpdocumenten (matrix, checklist, vergelijk-werkboek) blijven bestaan als achtergrond, maar de meeting draait op dit ene document.

## Fase 6 — Generale repetitie

1. Droge run door Abdul zelf, met de echte klikvolgorde en hardop de [ZEG]-zinnen.
2. Rollenspel: Claude speelt de klant-kant (per deelnemer een rol) en stelt de spiekbrief-vragen door elkaar, plus minstens 3 niet-voorbereide.
3. Demo-omgeving eindcheck: server/preflight groen, joblijst opgeschoond (alleen de jobs die het draaiboek noemt), voorbereide resultaten aanwezig en geopend getest, juiste taal-/instellingen-standen.
4. Daarna: niets meer wijzigen.

## Guardrails

- Klantdata is read-only; klantzichtbare output in de klant-taal; interne docs NL.
- Geen prijzen/tarieven in klant-facing materiaal of in de meeting; volumevragen eerst, voorstel later op papier.
- Negatieve bevindingen over klant-aanleveringen altijd als vraag formuleren en eerst zelf hard verifiëren.
- API-keys nooit persisteren; kosten-/interne bedragen niet noemen behalve het afgeronde marginale-kosten-anker.
- Log de sessie in PROGRESS.md (met urenschatting) en werk HANDOVER.md bij.
