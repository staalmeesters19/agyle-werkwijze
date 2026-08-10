# Start hier

Welkom bij Agyle. Dit pakket bevat hoe wij werken: de mappenstructuur, de bestanden die
we per klant bijhouden, en de tools die het meeste routinewerk overnemen.

Lees dit document helemaal (10 minuten). Daarna weet je genoeg om te beginnen.

---

## Wat Agyle doet

Agyle is een Nederlandse AI-consultancy. We bouwen werkende oplossingen voor bedrijven
van ongeveer 50 tot 1000 medewerkers — geen adviesrapporten, maar dingen die draaien.
Typisch traject: een probleem dat nu handwerk is, wordt een PoC, en die PoC wordt bij
succes een product.

Een paar lopende voorbeelden, zodat je een beeld hebt van het soort werk:

- **Van den Pol** — een pipeline die Siemens TIA Portal-exports omzet naar een compleet
  functioneel ontwerpdocument. Wat een engineer dagen kostte, duurt nu minuten.
- **Etec Bohn** — uit installatietekeningen automatisch een Belegungsliste genereren.
  Het acceptatiecriterium van de klant was letterlijk: *"we have to come to the same
  results"* als hun eigen engineer.
- **Kropman** — monteursrapportages in wisselende formaten samenvatten tot één
  gereedmeldrapportage.

## Wat je als eerste doet

1. **Installeer dit pakket** — zie [`../README.md`](../README.md). Duurt vijf minuten.
2. **Zet je MCP-servers op** — [`03-MCP-SETUP.md`](03-MCP-SETUP.md). Zonder dit werkt de
   helft van de tools niet. Reken op een half uur, vooral vanwege de inlogstappen.
3. **Lees de werkwijze** — [`02-WERKWIJZE.md`](02-WERKWIJZE.md). Vijf regels. Dit is het
   belangrijkste document van het pakket; de rest is gereedschap.
4. **Lees de veiligheidsregels** — [`05-VEILIGHEID.md`](05-VEILIGHEID.md). Kort, maar
   niet optioneel. Er staan dingen in die een klant geld of vertrouwen kosten als ze
   misgaan.
5. **Draai `VALIDATE.ps1`** — die vertelt je of je installatie compleet is.

## Hoe wij met Claude Code werken

Vrijwel al het werk loopt via Claude Code. Twee begrippen die je meteen tegenkomt:

- **Skills** zijn kant-en-klare werkwijzen. Je roept ze aan met een schuine streep:
  `/notulen`, `/mail`, `/nieuwe-klant`. Ze staan in `~/.claude/skills/` en dit pakket
  installeert ze voor je. Welke er zijn en wanneer je ze gebruikt:
  [`04-DELIVERABLES.md`](04-DELIVERABLES.md).
- **MCP-servers** zijn koppelingen naar externe systemen — je mailbox, de agenda, het
  CRM, GitHub. Daardoor kan Claude een conceptmail klaarzetten of een vergaderopname
  ophalen zonder dat jij knipt en plakt.

Verder: elke map met een `CLAUDE.md` erin geeft Claude automatisch de context van dat
project zodra je daar werkt. Je hoeft dus niet elke sessie opnieuw uit te leggen wie de
klant is.

## Taal

Intern Nederlands, code en technische documentatie Engels. Klantcommunicatie in de taal
van de klant — bij Bohn is dat Duits, bij de rest meestal Nederlands.

## Als je vastloopt

Vraag het Abdul. Serieus: een half uur vastzitten is duurder dan een vraag stellen. Wat
wél de bedoeling is, is dat je je vraag scherp maakt — wat heb je geprobeerd, wat
verwachtte je, wat gebeurde er. Dat scheelt een ronde heen en weer.
