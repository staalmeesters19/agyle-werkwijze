# De werkwijze — vijf regels

Dit is hoe elk klantproject bij Agyle is ingericht. De regels zijn niet bedacht maar
gegroeid: ze staan zo in de mappen van Van den Pol, Bohn, Kropman, Harwig en Eltra. Houd
je eraan en iemand anders kan morgen jouw werk overnemen.

---

## Regel 1 — Mapstructuur

```
clients/<klant>/<traject>/
    vergaderingen/     opnames, transcripten, notulen (md + pdf), briefings
    documenten/        analyses, voorstellen, technische stukken
    offertes/          uitgebrachte offertes
    facturatie/        urenverantwoordingen en toelichtingen (alleen waar van toepassing)
```

**De trajectlaag gebruik je alleen bij een klant met meerdere trajecten.** Van den Pol
heeft er drie (`fds/`, `syntess-werkbonnen/`, `revit/`), dus daar zit hij. Bohn heeft één
traject, dus daar staan `vergaderingen/` en `documenten/` direct in de klantmap. Beide
zijn goed.

**Nooit losse bestanden in de klantroot.** Een notulen die daar belandt vindt niemand
terug. Uitzondering met reden: een getekend contract mag als ankerdocument in de
trajectroot staan — zoals de getekende offerte bij Van den Pol.

Code met een eigen git-repo krijgt een eigen submap (`poc/`, `<naam>-agent/`). De
voortgangsbestanden van zo'n repo leven ín de repo, niet in de klantmap.

`/nieuwe-klant` zet dit allemaal voor je neer. Gebruik die skill; dan kun je het niet
verkeerd doen.

---

## Regel 2 — Drie levende bestanden per project

Dit is het belangrijkste onderdeel van de hele werkwijze. Vier bestanden, elk met een
eigen taak, en je haalt ze niet door elkaar.

| Bestand | Wat erin hoort | Voor wie |
|---|---|---|
| `CLAUDE.md` | Wie is de klant, wat is de opdracht, welke afspraken gelden, waar staat wat | Claude + jij, elke sessie |
| `PROGRESS.md` | Wat er is gedaan, per sessie, met urenschatting | Jij + bron voor klantmails en facturen |
| `HANDOVER.md` | Wat de volgende sessie moet weten: open punten, waar je op wacht, herstartrecept | Intern — nooit naar de klant |
| `mail_<contact>.md` | Wat er met wie is gecommuniceerd, chronologisch | Jij |

**PROGRESS.md gaat automatisch.** Er draait een hook die na elke werksessie een entry
wegschrijft onder de kop *"Automatisch gelogd (nog te consolideren)"*, inclusief een
urenschatting. Jouw taak is die entries periodiek naar boven consolideren onder een
weekkop — dan is het bestand ook leesbaar voor een mens.

**HANDOVER.md gaat ook automatisch.** Na een echte werksessie (niet na een typfix) word
je gevraagd hem bij te werken. Open punten schrijf je als `- [ ]` zodat je ze kunt
afvinken in plaats van herschrijven.

**`mail_<contact>.md` is een tijdlijn, geen postvak.** Per blok: datum, status
(`VERSTUURD` / `ONTVANGEN` / `CONCEPT`), onderwerp, en wat er bewust níet in zat. Nuttig
gebleken: noteer ook hoe de klant overkwam. Bij Bohn staat bijvoorbeeld *"Vibe: kort,
beslist, pragmatisch — geen defensiviteit over de gevonden bronfouten"*. Dat is precies
wat je vergeet en later nodig hebt.

Correcties schrijf je eronder, je herschrijft de geschiedenis niet:
`**Update 2026-07-29:** deze mail is verstuurd op 28-07; de status 'concept' hierboven is achterhaald.`

---

## Regel 3 — Uren staan op drie plekken en dat mag verschillen

Dit verwart iedereen in het begin, dus expliciet:

| Waar | Wat | Hoe |
|---|---|---|
| `PROGRESS.md` | Wat je feitelijk gedaan hebt | Automatisch, een schatting (`±2,5 u [schatting]`) |
| Agyle CRM | Wat je boekt op de opdracht | Handmatig, per project, via de `agyle`-MCP |
| `facturatie/*.pdf` | Wat de klant op de factuur ziet | Via de urenverantwoording-skill |

Ze lopen uiteen en dat is een bewuste keuze, geen slordigheid. PROGRESS is jouw eigen
registratie; het CRM is de boekhouding. **Boek je uren op het juiste project** — bij
Kropman zijn de storingsrapportage en de L&D-opdracht twee aparte opdrachten en dat gaat
regelmatig mis.

Twee regels voor de factuur-PDF, in deze volgorde:

1. **Niet over-claimen.** Geen "afgerond" of "gevalideerd" zonder dat de klant het
   bevestigd heeft.
2. **Niet onder-billen.** Standaard acht uur op een gewerkte werkdag. Dagen wegknippen om
   bescheiden te lijken doen we niet.

---

## Regel 4 — Klanttaal

Alles wat een klant leest — mail, notulen, offerte, rapportage — gaat langs deze regels.

**Underpromise, overdeliver.** Liever een resultaat dat meevalt dan een belofte die
tegenvalt.

**Verboden woorden zonder bevestiging van de klant:** *af, afgerond, compleet, klaar,
werkt, werkend, gevalideerd, opgelost, production-ready, nu correct.* Ze suggereren een
eindoordeel dat alleen de klant kan vellen. Schrijf in plaats daarvan wat je wél weet:
"wij zien nu X, visuele review door de klant staat open".

Het helpt om per claim vier kolommen in gedachten te houden — *draait bij ons* ·
*intern gecheckt* · *feedback verwerkt* · *door klant goedgekeurd*. Alleen de vierde is
"af".

**Zet de actor erbij.** Niet "X is opgelost", wel "wij hebben Y aangepast; review staat
open".

**Geen prijzen in klant-facing documenten** tenzij Abdul dat expliciet vraagt. Houd een
interne versie mét bedragen en een klantversie zonder. Dit is twee keer misgegaan en
moest achteraf gestript worden.

**Geen intern jargon.** In klantoutput komen de woorden *skill, agent, AI, Claude,
prompt, pipeline-laag* niet voor, en ook geen bestandspaden of sessienummers.

---

## Regel 5 — Klantdata is read-only

Wat de klant aanlevert — exports, referentieprojecten, tekeningen — bewerk je niet. Dat
is de meetlat waartegen we ons werk verifiëren; verandert die, dan kun je niets meer
bewijzen. Werk met kopieën of afgeleide bestanden.

Hetzelfde geldt voor conclusies: **verifieer voordat je naar de klant communiceert.**
Loop je tegen wat een fout in de klantdata lijkt, controleer het eerst zelf handmatig, en
formuleer het dan als vraag en niet als klacht. Dat is hier een keer misgegaan en het
staat sindsdien als vaste regel in het Bohn-dossier.

---

## Samengevat

1. Trajectlaag als er meerdere trajecten zijn, dan `vergaderingen|documenten|offertes`. Nooit los in de klantroot.
2. `CLAUDE.md` = afspraken · `PROGRESS.md` = wat gedaan is · `HANDOVER.md` = wat de volgende moet weten · `mail_<contact>.md` = wat er gecommuniceerd is.
3. Uren: schatting in PROGRESS, boeking in het CRM, factuur via de skill. Mogen verschillen.
4. Klanttaal: underpromise, geen "af/werkt/gevalideerd", geen prijzen, geen jargon.
5. Klantdata niet aanraken; verifieer vóór je iets naar de klant stuurt.
