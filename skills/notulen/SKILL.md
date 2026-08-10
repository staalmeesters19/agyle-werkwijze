---
name: notulen
description: Haal een meeting-opname op uit Plaud (MCP) en verwerk die naar een volledig transcript + Agyle-branded notulen (md + PDF) in de juiste klant/project-vergaderingenmap, met een concept-mail mét echte handtekening klaar in Outlook. Vervangt /verwerk-meeting; losse audiobestanden kunnen als fallback nog via AssemblyAI.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, PowerShell, ToolSearch, mcp__plaud__list_files, mcp__plaud__get_transcript, mcp__plaud__get_note, mcp__ms365__list-calendar-events, mcp__ms365__get-calendar-view, mcp__ms365__list-mail-messages, mcp__ms365__list-users, mcp__ms365__create-draft-email
---

# Skill: `/notulen` — Plaud-opname → transcript + Agyle-notulen + concept-mail

Vervangt `/verwerk-meeting`. Standaardbron is **Plaud via MCP**; een los audiobestand is de fallback (Stap 1b).

**Aanroep:** `/notulen <klant/onderwerp/datum>` — bijv. `/notulen Kropman stuurgroep 23 juli`, `/notulen vandenpol revit`, `/notulen latest`.

## Harde regels

- **Nooit het volledige transcript in een chatbericht uitschrijven.** Alles gaat via Write direct naar disk (32k output-token-limiet heeft dit eerder gesloopt).
- **Schrijf het transcript weg vóór je aan de notulen begint.** Als de sessie klapt, is de dure stap dan al binnen.
- **Nooit verzenden.** De skill maakt uitsluitend drafts.
- **Nooit e-mailadressen verzinnen** — opzoeken via MS365, of vragen.
- **Nooit naar de klant-root schrijven** als de klant projectsubmappen heeft.
- **Geen prijzen/tarieven in de klant-PDF** tenzij Abdul dat expliciet vraagt.

---

## Stap 1 — Recording vinden in Plaud

Laad de tools: `ToolSearch` met `query: "select:mcp__plaud__list_files,mcp__plaud__get_transcript,mcp__plaud__get_note"`.

Plaud-namen zijn AI-gegenereerd en matchen zelden de meetingnaam (bv. `07-23 Strategische bespreking over AI-toepassingen, Revit-automatisering en teaminzet` voor "Revit-kickoff"). **Zoek dus op datum, niet op naam.**

1. Zit er een datum in `$ARGUMENTS` → `list_files` met `date_from`/`date_to` op die dag ±1.
2. Geen datum → `list_files` over de laatste 14 dagen.
3. `latest` → nieuwste opname.
4. Filter de kandidaten op plausibiliteit (duur > 5 min, naam/onderwerp).

Blijft er precies één plausibele kandidaat over → ga door en meld hem in één regel. Meerdere → toon een genummerd lijstje (naam, datum, duur) en vraag welke. **Gok nooit tussen twee kandidaten.**

### Stap 1b — Fallback: los audiobestand (geen Plaud-opname)

Alleen als er geen Plaud-opname bestaat en Abdul een bestand aanlevert:

```bash
python "<SKILL_DIR>/transcribe.py" "<audio_pad>" "<nl|en>" "<output_pad>"
```

(AssemblyAI-key zit in `<SKILL_DIR>/.env`.) Levert `.transcript.md` + `.transcript.json`; ga daarna verder bij Stap 3.

---

## Stap 2 — Transcript en notes ophalen

- `get_transcript(file_id)` → volledig, getimede transcript.
- `get_note(file_id)` → Plaud's AI-samenvatting, actiepunten en topics. Gebruik dit als **steun** bij het schrijven, nooit als vervanging van het transcript.

Noteer voor de header: recordingnaam, `file_id`, duur, opnamedatum.

---

## Stap 3 — Klant en project bepalen (routing)

Clients-root: het pad uit `clients_root` in `~/.claude/agyle-persoon.json`. Ontbreekt dat
bestand, zoek dan vanaf de werkmap omhoog naar een map `clients/` binnen `agyle-business`.

1. Lijst de klantmappen (`Bohn`, `Harwig`, `Kropman`, `kuijpers`, `vandenpol`, …) — hardcodeer ze niet, kijk wat er staat.
2. Heeft de klant een `CLAUDE.md`? Lees die — daar staat de projectsplitsing en wie welke contactpersoon is (Van den Pol heeft bv. `fds/`, `syntess-werkbonnen/`, `revit/`, elk met eigen `vergaderingen/`).
3. Bepaal het **project** uit de inhoud van het transcript, niet uit de klantnaam alleen.
4. Doelmap = `clients/<klant>/<project>/vergaderingen/` (of `clients/<klant>/vergaderingen/` als de klant geen projectsplitsing heeft).

Meld de gekozen map in één regel. Vraag alleen bij twijfel: onbekende klant, of twee projecten even plausibel. Nieuwe klant → stel de mapstructuur voor en wacht op akkoord voordat je aanmaakt.

### Bestandsnamen (bestaande conventie — volg exact)

```
<Klantnaam> - Transcript <onderwerp> - <YYYY-MM-DD>.txt
<Klantnaam> - Notulen <onderwerp> - <YYYY-MM-DD>.md
<Klantnaam> - Notulen <onderwerp> - <YYYY-MM-DD>.pdf
```

`<Klantnaam>` is de nette schrijfwijze ("Van den Pol", "Kropman", "Bohn"), `<onderwerp>` kort en herkenbaar ("Revit-automatisering", "FDS productie, hosting en onderhoud").

---

## Stap 4 — Transcript wegschrijven (checkpoint — nu meteen)

Schrijf het `.txt`-transcript direct weg met Write. Header-blok, dan de tekst in `[mm:ss]`-blokken:

```
Transcript — <onderwerp>
Datum: <YYYY-MM-DD>, ~<begin>-<eind>, <locatie>
Bron: Plaud-opname id <file_id> ("<recordingnaam>"), duur ~<N> min
Sprekers: <naam (organisatie), …> — <of: "Plaud leverde geen sprekerattributie">; tijden zijn [mm:ss].

[00:00] …
[00:30] …
```

Bevat Plaud wél sprekerlabels → zet ze vóór de tekst: `[04:19] Gerben: …`.

---

## Stap 5 — Sprekers en namen corrigeren

Spraakherkenning verhaspelt namen structureel (Cristian→Christian, Cornée→Corné/Cornee, Ronald→Roman). Corrigeer in transcript én notulen:

1. Lees `<SKILL_DIR>/aliases.json` en pas alle bekende correcties toe.
2. Vul aan uit: de klant-`CLAUDE.md` (contacttabel), eerdere notulen in dezelfde `vergaderingen/`-map, en de agenda-uitnodiging van die dag (`mcp__ms365__get-calendar-view` of `list-calendar-events`).
3. Vond je een nieuwe verhaspeling → voeg die toe aan `aliases.json` zodat de volgende keer beter gaat.
4. Weet je het niet zeker → laat de naam staan zoals Plaud hem gaf en meld het. **Verzin geen deelnemers.**

---

## Stap 6 — Notulen `.md` (volledige werkversie)

Dit is jouw versie, niet de klantversie: hier mag context in die de PDF niet haalt.

```markdown
# Notulen — <onderwerp>

**Datum**: <YYYY-MM-DD>, ~<tijd>, <locatie>
**Aanwezig**: <naam (organisatie, rol), …>
**Bron**: Plaud-opname "<naam>" (id `<file_id>`, ~<N> min)
**Status project**: <verkennend / lopend / …>

---

## Kern
<2-5 alinea's: waar ging het over, wat is het probleem, wat is de beoogde oplossing, wat is de verwachte winst — met de concrete getallen uit het gesprek>

## Sleutelpersonen <klant>
<alleen als er nieuwe mensen/rollen langskwamen>

## <thematische secties>
<per onderwerp wat besproken is, wie welk standpunt had>

## Afspraken & actiepunten

| Wie | Actie |
|---|---|

## Aanpak-notitie Agyle
<jouw eigen inschatting: startpunt, scope, wat eerst uitzoeken. Optioneel.>
```

Cijfers, bedragen, deadlines en namen komen **letterlijk uit het transcript** — niet afronden of gladstrijken.

---

## Stap 7 — Klant-PDF (Agyle branding)

De PDF is de klantversie: neutraal en feitelijk.

**Wel**: besproken onderwerpen, actiepunten (wie/wat/deadline), vervolgstappen.
**Niet**: pijnpunten als salesobservatie, sfeer/dynamiek, interne aanbevelingen, Agyle-strategie, tarieven of prijzen.

```bash
python -c "
import sys
sys.path.insert(0, '<SKILL_DIR>')
from generate_pdf import generate_notulen_pdf
generate_notulen_pdf(
    output_path=r'<doelmap>\<Klant> - Notulen <onderwerp> - <datum>.pdf',
    titel='<onderwerp>',
    datum='<23 juli 2026>',
    locatie='<locatie>',
    deelnemers='<namen met organisaties>',
    type_meeting='<kennismaking / stuurgroep / verdieping / …>',
    duur='<N minuten>',
    onderwerpen_html='<h3>1. …</h3><p>…</p>',
    actiepunten_html='<tr><td>Wie</td><td>Wat</td><td>Wanneer</td></tr>',
    vervolgstappen_html='<p>…</p>',
)
"
```

HTML moet valide fragmenten zijn (h3/p voor onderwerpen, tr/td voor de tabel). Templates en logo komen uit `~/.claude/skills/_agyle_branding/`; PDF-rendering gaat via headless Edge/Chrome.

**Optioneel, alleen op verzoek:** een verdiepingsnotitie (citaten → implicaties → één eerste stap) via `generate_verdieping_pdf` uit hetzelfde bestand.

---

## Stap 8 — Concept-mail in Outlook (mét echte handtekening)

Handtekening = **gehoste-URL-blok, GEEN inline-bijlagen** (bewezen 2026-07-27, zie skill `/mail` + CLAUDE.md). Inline-cid-plaatjes worden door OWA gedupliceerd/verminkt.

### 8.1 Ontvangers

- **To** = externe deelnemers (de klant) die in het transcript spraken.
- **Cc** = interne Agyle-collega's (`@agyle.nl`) die meededen.
- Adressen ophalen uit de agenda-uitnodiging (`get-calendar-view` op die dag) of recente mailwisseling (`list-mail-messages` met `search`, KQL tussen dubbele quotes). Niet te matchen → vraag het, gok niet.

### 8.2 Draft opbouwen (één call)

`mcp__ms365__create-draft-email` — `subject`, `toRecipients`, `ccRecipients`, en `body.contentType=html`, `body.content` = [mailtekst-divs] + [inhoud van `~/.claude/assets/agyle-signature-url.html`]. **Geen `add-mail-attachment`, geen `update-mail-message` nodig.**
Onderwerp: `Verslag — <onderwerp> (<datum>)` (NL) / `Notes — <topic> (<date>)` (EN, bij een Engelstalige meeting).

### 8.3 Body

HTML met `<div>`'s en expliciete `<div><br></div>` als witregel — **geen `<p>`** (OWA's `p{margin:0}` slaat alinea's plat) en geen platte tekst met `\n`.

**Aptos-wrapper verplicht.** Wikkel alle bodytekst vóór de handtekening in:

```html
<div style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">…</div>
```

Zonder die wrapper rendert de body in Times New Roman terwijl de handtekening in Aptos staat.

Kort, verwijzend naar de bijlage, in de taal van de meeting. **Geen eigen afsluiting** — de afsluiting en je naam zitten al in het handtekeningblok.

> Beste \<voornamen\>, zoals afgesproken stuur ik jullie hierbij het verslag van onze meeting (zie bijlage). Mochten er onjuistheden in staan of iets ontbreken, laat het me gerust weten.

### 8.4 Bijlage = handmatige stap

De branded PDF (~150–180 KB) is te groot om betrouwbaar als base64 door een tool-call te sturen. **Hecht hem niet automatisch aan.** De body verwijst al naar "de bijlage"; meld Abdul expliciet dat hij de PDF er nog in moet slepen.

---

## Stap 9 — Afronden

Meld compact:

> Verwerkt — `<klant>/<project>/vergaderingen/`:
> - Transcript: `<bestandsnaam>.txt`
> - Notulen (werkversie): `<bestandsnaam>.md`
> - Notulen (klant-PDF): `<bestandsnaam>.pdf`
>
> Concept-mail klaar — Aan: \<namen\> · Cc: \<namen\> · Onderwerp: \<onderwerp\>
> Eén handmatige stap: sleep de PDF in de draft voordat je verzendt.
>
> \<eventueel: namen die ik niet zeker wist, of ontbrekende adressen\>

Noem ook wat je **niet** kon bepalen — liever een open puntje dan een stille aanname.
