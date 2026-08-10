# De skills — wanneer gebruik je wat

Alle skills roep je aan met een schuine streep, bijvoorbeeld `/notulen`. Ze staan na
installatie in `~/.claude/skills/`.

---

## Per situatie

| Je moet... | Gebruik | Wat je krijgt |
|---|---|---|
| een nieuwe klant of traject opzetten | `/nieuwe-klant` | mappen, `CLAUDE.md`, `PROGRESS.md`, `HANDOVER.md`, `mail_<contact>.md` |
| een vergadering verwerken | `/notulen` | transcript, notulen in markdown, branded PDF, conceptmail |
| een mail klaarzetten | `/mail` | conceptmail in Outlook met jouw handtekening |
| weten waar een project staat vóór een meeting | `/briefing` | korte kern om te spreken + uitgewerkte achtergrond |
| een nieuwe prospect voorbereiden | `/prep-klant` | SPIN-voorbereiding met onderzoek naar het bedrijf |
| een voorstel maken dat indruk moet maken | `/voorstel-site` | voorstel als scrollytelling-microsite in plaats van PDF |
| een beheerovereenkomst opstellen | `/onderhoudscontract` | contracttekst, interne calculatie, branded PDF |
| een PoC verdedigen in een demo | `/poc-verantwoording` | draaiboek, waarheidsladder, generale repetitie |
| voortgangslogging aanzetten in een bestaand project | `/setup-progress` | `PROGRESS.md` + automatische logging |

---

## De vier die je het eerst nodig hebt

### `/nieuwe-klant`

Zet een klant of traject in één keer correct neer volgens regel 1 en 2 van de werkwijze.
Vraagt om klantnaam, contactpersonen, de opdracht in één zin en het acceptatiecriterium
van de klant. Gebruik dit altijd — met de hand mappen aanmaken gaat een keer mis en dan
staat het scheef voor de rest van het traject.

### `/notulen`

De hele keten van opname naar klant. Haalt de opname uit Plaud (**zoek op datum, niet op
naam** — Plaud verzint zelf namen die zelden kloppen), maakt een transcript, corrigeert
sprekersnamen tegen de agenda, schrijft notulen en rendert een Agyle-branded PDF. Zet
daarna een conceptmail klaar.

Twee dingen die je moet weten: de PDF wordt **niet** automatisch als bijlage toegevoegd —
die sleep je zelf in de concept. En in de klant-PDF horen geen prijzen, geen
salesobservaties en geen sfeerbeschrijvingen; die blijven in de markdown-werkversie.

Bestandsnamen, exact aanhouden:
```
<Klant> - Transcript <onderwerp> - <JJJJ-MM-DD>.txt
<Klant> - Notulen <onderwerp> - <JJJJ-MM-DD>.md
<Klant> - Notulen <onderwerp> - <JJJJ-MM-DD>.pdf
```
Intern overleg krijgt het voorvoegsel `INTERN - `.

> In bestaande klantmappen kom je nog twee oudere naamgevingen tegen. Hernoem die niet;
> gebruik voor nieuw werk alleen bovenstaande.

### `/mail`

Zet een conceptmail klaar met jouw handtekening. **Alleen concepten, nooit verzenden** —
dat doe je zelf in Outlook nadat je hem hebt nagelezen.

De handtekening bevat al een afsluiting, dus zet er zelf geen "Met vriendelijke groet"
boven; dan staat het er twee keer.

### `/briefing`

Draai deze vóór elke meeting waar je niet precies weet wat de stand is. Leest
`PROGRESS.md`, `HANDOVER.md`, je mail-scratchpads en de recente wijzigingen, en geeft je
een korte kern om te zeggen plus de achtergrond om vooraf door te lezen. Werkt in elke
projectmap.

---

## Documenten die de klant ziet

Alles wat naar buiten gaat is Agyle-branded: zwart `#000000` met lichtblauw `#97D4E8`.
De sjablonen en de PDF-generator staan in `~/.claude/skills/_agyle_branding/` — daar zit
één renderer die alle skills gebruiken. Zelf een eigen opmaak verzinnen doen we niet.

Werk je voor een klant met eigen huisstijl, dan komen hun kleuren als accent bovenop de
Agyle-basis.

---

## Skills die je niet krijgt

Een paar van Abduls skills zijn persoonsgebonden en zitten daarom niet in dit pakket:
`/linkedin-post` (geschreven in zijn stem), `/video-scan` (beoordeelt op zijn
interessegebied), `/nomura-pitch` (privéproject) en `/diagram-generator` (hangt aan een
andere repository). Heb je zoiets nodig, overleg dan — een eigen variant maken kan.
