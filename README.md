# Agyle Werkwijze

Hoe wij bij Agyle werken, als installeerbaar pakket: de mappenstructuur, de bestanden die
we per klant bijhouden, de skills die het routinewerk overnemen, en twee hooks die de
administratie automatisch bijhouden.

Bedoeld voor nieuwe medewerkers en stagiairs. Na installatie werk je meteen op dezelfde
manier als de rest.

---

## Installeren

Drie stappen, ongeveer vijf minuten.

```powershell
# 1. Vul je eigen gegevens in
Copy-Item config\persoon.example.json config\persoon.json
notepad config\persoon.json

# 2. Installeren
.\INSTALL.ps1

# 3. Controleren
.\VALIDATE.ps1
```

Start daarna Claude Code opnieuw op, zodat de skills en hooks geladen worden.

**Vereist:** Python 3, Edge of Chrome (voor PDF's), Claude Code. Geen pip-packages.

Daarna nog één keer werk: [`docs/03-MCP-SETUP.md`](docs/03-MCP-SETUP.md) om je mailbox,
agenda en het CRM te koppelen. Reken op een half uur.

## Waar begin je met lezen

| Document | Waarom |
|---|---|
| [`docs/01-START-HIER.md`](docs/01-START-HIER.md) | Wat Agyle doet en wat je eerst doet |
| [`docs/02-WERKWIJZE.md`](docs/02-WERKWIJZE.md) | **De vijf regels. Het belangrijkste document.** |
| [`docs/03-MCP-SETUP.md`](docs/03-MCP-SETUP.md) | Je systemen koppelen |
| [`docs/04-DELIVERABLES.md`](docs/04-DELIVERABLES.md) | Welke skill wanneer |
| [`docs/05-VEILIGHEID.md`](docs/05-VEILIGHEID.md) | Wat je niet moet doen |

## Wat er geïnstalleerd wordt

**Skills** (in `~/.claude/skills/`) — roep je aan met een schuine streep:

`/nieuwe-klant` · `/notulen` · `/mail` · `/briefing` · `/prep-klant` · `/voorstel-site` ·
`/onderhoudscontract` · `/poc-verantwoording` · `/setup-progress`

Plus `_agyle_branding`: de gedeelde huisstijl-assets en de PDF-generator die alle skills
gebruiken.

**Hooks** (in `~/.claude/hooks/`) — draaien vanzelf aan het eind van een werksessie:

- `update_progress.py` schrijft een entry in `PROGRESS.md` met een urenschatting.
- `update_handover.py` laat `HANDOVER.md` bijwerken: open punten, waar je op wacht, hoe
  je het project weer draaiend krijgt.

Beide slaan projecten zonder `PROGRESS.md` respectievelijk `HANDOVER.md` stilzwijgend
over, en beide doen niets bij een sessie van een paar minuten.

## Wat er niet in zit

Een paar van Abduls skills zijn persoonsgebonden — geschreven in zijn stem, of gekoppeld
aan zijn eigen projecten — en horen niet in een gedeeld pakket. Heb je zoiets nodig,
overleg dan; een eigen variant maken kan.

## Je huisstijl aanpassen

Werkt Agyle ooit onder een andere naam of kleur, dan zitten de aanpassingen op drie
plekken:

1. `skills/_agyle_branding/logo_base64.txt` — het logo in alle PDF's
2. `skills/_agyle_branding/templates/*.html` — de kleuren in de sjablonen
3. `templates/agyle-signature-url.template.html` — de e-mailhandtekening

De handtekeningplaatjes staan gehost op Vercel (project `agyle-email-assets`); die URL's
staan in het handtekeningsjabloon.

## Voor beheerders

Canonieke bron is de GitHub-repository. De kopie in SharePoint is een **snapshot** voor
wie niet met git werkt — na een wijziging opnieuw publiceren, anders lopen ze uiteen.

Vóór elke push:

```powershell
.\VALIDATE.ps1 -Pakket
```

Die controleert op absolute paden naar één specifieke machine en op sleutels in de
bestanden. Rood betekent niet pushen.

Nieuwe medewerker toevoegen: laat diegene het pakket clonen en `INSTALL.ps1` draaien met
een eigen `config/persoon.json`. Regel daarnaast toegang tot de MCP-servers (eigen
Agyle-account, eigen GitHub-token) en beslis wat er met Plaud gebeurt — een eigen account
ziet andermans opnames niet.
