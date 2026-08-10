---
name: briefing
description: Brief Abdul voor een meeting — zoekt uit wat er recent gedaan is in het huidige project, welk klant-contact er is geweest (mail-historie, meeting-prep-docs), en wat er hierna zou moeten. Werkt in élke project-folder. Default = CWD laatste 7 dagen. Output = korte kern-samenvatting voor live-gebruik plus uitgewerkte detail-secties voor pre-reading. Gebruik vóór élke meeting waar je niet precies weet wat de stand is.
argument-hint: [periode (7d, 3d, since 2026-04-15) of context-hint ("corné", "ecofrost") — leeg = laatste 7 dagen CWD]
context: fork
model: opus
allowed-tools: Read, Glob, Grep, Bash
---

# Briefing — wat heb ik/we recent gedaan, waar staan we, wat hierna

Abdul vraagt een briefing voor een aankomende meeting. Je zoekt uit wat er gedaan is, wat er met de klant is besproken, en wat de next steps zijn. Je bent grondig — Abdul zei expliciet: "helemaal uitzoekt voor mij".

## Kernregels

1. **Onderbeloof-toon**. Zelfde regels als elke klant-facing output: verboden "af", "werkt", "gevalideerd" (zonder "intern"), "production-ready", "opgelost" zonder klant-bevestiging. Bij twijfel: voeg actor of caveat toe.
2. **Robuust in élke folder**. Project-specifieke bestanden (PROGRESS.md, mail_corne.md, etc.) kunnen ontbreken. Val terug op git-log en file-mtimes. Fail gracefully — als een bron niet bestaat, sla over zonder foutmelding aan gebruiker.
3. **Twee-laags output**: kern-samenvatting bovenaan (live-gebruik, ≤80 woorden, spreek-taal), uitgewerkte detail-secties daaronder (pre-reading, doornemen vóór meeting).
4. **Synthese, geen herhaling**. Als 5 bronnen hetzelfde feit bevatten, noem het één keer. Cluster per thema, niet per bron.
5. **Niet verzinnen**. Als een bron iets niet zegt, schrijf "onbekend" of sla over. Niet invullen uit redenering.

## Input

Argument: `$ARGUMENTS`

Parseer volgens deze volgorde:
- Leeg → periode = laatste 7 dagen, geen filter
- Matcht `\d+d` (bijv. `3d`, `14d`) → die periode
- Matcht `since YYYY-MM-DD` → vanaf die datum
- Matcht `klant:X` of `project:X` → focus-filter op klantnaam/projectnaam
- Anders (vrije tekst) → context-hint voor framing, gebruik om prioritering te bepalen (bijv. `"corné"` betekent filter contact-bronnen op die naam)

Meerdere argumenten mogen combineren: `/briefing 3d corné`.

## Stappen

### 1. Bepaal periode + context

```bash
!`date +%Y-%m-%d`
```

Bereken begin-datum: vandaag minus `<periode>`. Default = 7d.

### 2. Detecteer bronnen in CWD

Glob en categoriseer (parallelliseer de zoekopdrachten):

**Progressie-bronnen** (prioriteit bepaalt welke je gebruikt als er meerdere zijn):
1. `PROGRESS.md` in CWD, subfolder, of parent (tot 2 levels omhoog — sommige projecten consolideren PROGRESS/mail centraal in de projectroot, met per-deployment subfolders eronder). Activity log, uren-tabel. Bij centrale file met H2-deployment-tags (`## YYYY-MM-DD — <deployment> — …`): filter op huidige CWD-foldernaam als je vanuit een deployment-subfolder draait.
2. `HANDOVER.md` — ontwikkelhistorie (vaak outdated, gebruik alleen als PROGRESS ontbreekt)
3. `CHANGELOG.md` / `RELEASES.md`
4. Git log (als `.git/` bestaat): `git log --since=<begin-datum> --oneline --all`
5. File mtimes: `find . -type f -mtime -<N> -not -path "*/.*"` (laatste hulpbron)

**Klant-contact-bronnen**:
1. `mail_*.md` / `*_mail.md` in CWD, subfolder, of parent (tot 2 levels omhoog) — scratchpads met klant-mail-drafts. Bij centrale file met H2-deployment-tags: filter op de relevante deployment-sectie als de briefing deployment-gebonden is.
2. `prep_*.md` / `*_prep.md` / `meeting_*.md` / `voorbereiding_*.md` — prior meeting-preps
3. `contact_*.md`, `contacts.md`, adresboek-achtige files
4. CLAUDE.md — Klant-context sectie als die er is

**Next-step-bronnen**:
1. `NEXT_SESSION_HANDOVER.md`, `NEXT_STEPS.md`, `TODO.md`, `ROADMAP.md`
2. Openstaande checkboxes in PROGRESS.md of HANDOVER.md
3. Prep-docs: "openstaande vragen" / "open items" secties
4. Mail-drafts met onbeantwoorde vragen aan klant

**Memory**:
- `~/.claude/projects/<slug>/memory/MEMORY.md` indexfile + topic-files
- Bij twijfel over project-slug: vraag via Glob op `<slug>/memory/MEMORY.md` met slug afgeleid van CWD-pad

Als een hele categorie leeg is: geen probleem, sla over in de output.

### 3. Lees parallel (fan-out)

Spawn Sonnet-subagents in parallel om grote bronnen te lezen (PROGRESS.md kan >100KB zijn). Elk subagent krijgt één bron + jouw periode + focus-filter, rapporteert max 200 woorden per bron.

Als ≤3 bronnen totaal: lees zelf sequentieel, geen subagent nodig.

Bij bronnen >50KB: gebruik `offset` + `limit` op laatste entries (tail), niet het hele bestand.

### 4. Synthetiseer — cluster per thema

Extract uit alle bronnen:

**Progressie**: wat is er feitelijk gedaan? Concreet — fixes, features, nieuwe onderdelen. Niet claims over kwaliteit.

**Klant-contact**:
- Wat is er verstuurd (mails, meetings, docs)?
- Wat zijn de commitments die Abdul heeft gedaan?
- Welke vragen staan open bij de klant (onbeantwoord)?
- Welke vragen staan open bij Abdul (te stellen)?

**Next steps**:
- Wat is expliciet als next step benoemd?
- Wat blokkeert voortgang (blockers, wachten-op)?
- Welke deadlines zijn genoemd?

### 5. Schrijf briefing

Print direct naar stdout (niet naar file tenzij user daar om vraagt):

```markdown
# Briefing — <project-naam> — <vandaag>

**Periode**: <X dagen / sinds datum> · **Focus**: <filter of "algemeen">
**Bronnen**: <korte lijst van wat je hebt gelezen>

---

## Kern — 3-5 spreek-bullets (≤80 woorden totaal)

- <feit 1 in spreek-taal, 1 regel>
- <feit 2>
- <feit 3>
- <een zin: "ik ben bezig met X, volgende stap Y">

*Bruikbaar als opener in een meeting.*

---

## Progressie — wat is er gebeurd

<uitgewerkt per thema-cluster. Geen datum-per-datum tenzij de opdracht dat vereist.>
<elke cluster: 1-3 bullets met concrete werk-items>
<alleen claims die je hard kunt onderbouwen vanuit de bronnen>

---

## Klant-contact — wat is er besproken

### Wat is verstuurd / besproken
<mails, meetings, docs die de klant heeft gezien>
<per item: wat + wanneer>

### Commitments op papier
<beloftes/milestones die Abdul heeft gedaan — letterlijke citaten waar mogelijk>

### Wat we van de klant nodig hebben (te vragen in de meeting)

**Documenten / data**:
<lijst van concreet ontbrekende bestanden, specs, exports — alleen wat echt niet al aanwezig is in de CWD, dus eerst Globben>

**Beslissingen / prioritering**:
<keuzes waar we op wachten: scope, volgorde, budget-goedkeuring, go/no-go>

**Feedback / review**:
<specifieke outputs waar de klant naar moet kijken voordat we verder kunnen>

**Toegang / context**:
<systemen, contacten bij de klant, info die wij niet zelf kunnen vinden>

### Open vragen — klant moet nog antwoorden
<onbeantwoorde vragen uit eerdere mails/meetings — met datum wanneer gesteld>

### Open vragen — Abdul moet nog stellen
<strategische/tactische vragen die Abdul zelf nog niet heeft gesteld maar die voor voortgang nodig zijn>

---

## Wat hierna zou moeten

### Expliciet benoemde next steps
<uit NEXT_SESSION_HANDOVER / TODO / prep-docs>

### Blockers / wachten-op
<wat kan pas starten als X is beantwoord/gebeurd>

### Deadlines
<wat heeft een harde of zachte deadline>

---

## Signalen die je moet weten

<2-4 bullets met ding-je-moet-onthouden: risico's, beslissingen-in-de-lucht, recent gewijzigde afspraken>
<alleen als er echt iets is — anders weglaten>

---

## Vraagtekens bij deze briefing

<zelf-kritische lijst: wat heb je niet kunnen vinden, welke aannames zitten in de synthese, welke bronnen ontbraken>
<max 3 items>
```

### 6. Self-check vóór tonen

Scan je briefing:

- **Verboden-woorden**: "af", "afgerond", "compleet", "klaar", "werkt", "opgelost", "gevalideerd" (zonder "intern") → herschrijf met actor/caveat.
- **Claim-bewijs-check**: elke harde claim heeft een bron in §Bronnen? Zo niet, verwijder of markeer als "aanname".
- **Periode-compliance**: staan er feiten in van vóór de begin-datum? → weghalen of expliciet "(van X, vóór periode)" erbij.
- **Kern-bullets-lengte**: totaal ≤80 woorden, in spreek-taal? → inkorten/herschrijven.
- **Klant-contact-secties**: staat er iets in "commitments" zonder datum/bron? → tag of verwijder.
- **Vraagtekens-sectie**: is eerlijk over wat je niet wist? → max 3 items, geconcentreerd op wat Abdul echt moet weten.

### 7. Output

Print de briefing direct in chat. Geen bestand aanmaken — dit is consumeerbare output voor het moment.

Als Abdul zegt "sla op": sla op als `briefing_<project>_<YYYY-MM-DD>.md` in CWD.

## Voorbeelden van toon

GOED (kern-bullet):
> "Peeling-feedback 13/04 is verwerkt; Cutting + Sorting hebben we intern gecheckt maar Corné heeft ze niet gereviewd."

FOUT (te stellig):
> "Peeling is af en Cutting + Sorting zijn gevalideerd."

GOED (commitment):
> "Mail 15/04 aan Corné: beloofd 'diepe verificatie overige secties in afgesproken volgorde' na Peeling-afronding. Nog niet opgestart."

FOUT (claim zonder bron):
> "Corné verwacht dat alle secties eind april klaar zijn." (dat staat nergens)

GOED (vraagteken):
> "Niet gecontroleerd: of Corné op de Ecofrost-vragen-mail heeft geantwoord — mail_corne.md is scratchpad, geen inbox."

FOUT (doen-alsof):
> "Alle openstaande vragen zijn gecheckt." (zonder mailbox-toegang is dit gelogen)

## Wanneer NIET te gebruiken

- Voor klantvoorbereidingen van **nieuwe** prospects → gebruik `/prep-klant` (SPIN)
- Voor klant-specifieke meetings met veel context → gebruik project-specifieke prep-skill (bijv. `/prep-corne` in Van den Pol project)
- Voor dagelijkse standup-achtige updates → te zwaar, gebruik git log + PROGRESS.md-tail handmatig

Voor élke andere meeting waar je vooraf wilt weten "waar sta ik/staan we": gebruik deze skill.
