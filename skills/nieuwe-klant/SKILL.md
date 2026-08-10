---
name: nieuwe-klant
description: Zet een nieuwe klant of een nieuw traject bij een bestaande klant in één keer correct op — mappenstructuur met trajectlaag, klant-CLAUDE.md volgens het vaste skelet, PROGRESS.md, HANDOVER.md en een mailscratchpad per contactpersoon. Gebruik bij "nieuwe klant aanmaken", "traject opzetten", "map voor klant X", of wanneer je merkt dat een klant nog geen projectstructuur heeft.
---

# `/nieuwe-klant` — klant of traject opzetten

Zet de mappenstructuur en de vier levende bestanden neer volgens regel 1 en 2 van de
werkwijze (`docs/02-WERKWIJZE.md`). Handmatig aanmaken gaat een keer mis en dan staat het
scheef voor de rest van het traject — daarom deze skill.

## Stap 1 — Bepaal waar je bent

Zoek de clients-root:

1. `clients_root` uit `~/.claude/agyle-persoon.json`.
2. Ontbreekt dat, zoek dan vanaf de werkmap omhoog naar een map `clients/`.
3. Beide mislukt → vraag het pad en ga niet gokken.

Lijst wat er staat. **Bestaat de klantmap al?** Dan gaat het om een nieuw traject bij een
bestaande klant, niet om een nieuwe klant — dat verandert stap 3.

## Stap 2 — Vraag de gegevens

Stel deze vragen in één keer, niet één voor één. Ontbreekt iets, vraag dan door; verzin
niets.

| Veld | Toelichting |
|---|---|
| Klantnaam | Zoals de klant zichzelf schrijft. Wordt de mapnaam. |
| Traject | Alleen als er meer dan één traject komt of al is. Anders leeg laten. |
| Contactpersonen | Naam, rol (inhoudelijk / commercieel / facturen) en mailadres |
| Opdracht | Eén zin: wat gaan we voor ze bouwen of oplossen |
| Acceptatiecriterium | Waaraan meet de klant af of het goed is? |
| Contractuele basis | Tarief, budget, facturatieritme — of "nog niet vastgelegd" |
| Kernprincipe | Het niet-onderhandelbare uitgangspunt. Mag leeg als je het nog niet weet. |
| Taal | Taal van klantcommunicatie. Standaard Nederlands. |

Het acceptatiecriterium is het belangrijkste veld en wordt het vaakst overgeslagen.
Zonder dat weet je later niet waartegen je verifieert. Weet de klant het zelf nog niet,
noteer dan letterlijk "nog niet vastgesteld — eerst uitvragen" en zet het als open punt
in HANDOVER.md.

## Stap 3 — Beslis over de trajectlaag

- **Eén traject** → `clients/<klant>/` met daarin direct `vergaderingen/`,
  `documenten/`, `offertes/`.
- **Meerdere trajecten** → `clients/<klant>/<traject>/` met daaronder die submappen. De
  klantmap zelf krijgt dan een korte routerende `CLAUDE.md` die naar de trajecten wijst.

Voegt de gebruiker een tweede traject toe aan een klant die nu nog plat is? Stel dan voor
om eerst te herstructureren, **en wacht op akkoord** — bestaande bestanden verplaatsen
raakt paden in andere documenten.

`facturatie/` maak je alleen aan als er daadwerkelijk gefactureerd gaat worden.

## Stap 4 — Maak aan

Toon eerst de volledige lijst met te maken mappen en bestanden en **wacht op akkoord**.
Daarna:

1. De mappen uit stap 3.
2. `CLAUDE.md` uit `templates/klant-CLAUDE.md`, alle zeven secties gevuld. Laat een
   sectie liever weg dan met een lege kop achter.
3. `PROGRESS.md` uit `templates/PROGRESS.md`. Bestaat er al een centrale PROGRESS.md
   hoger in de boom, maak dan geen tweede aan — vraag of er aan de centrale log wordt
   bijgedragen. Dit volgt dezelfde regel als `/setup-progress`.
4. `HANDOVER.md` uit `templates/HANDOVER.md`, met het eerste open punt gevuld (meestal:
   ontbrekende contractuele basis of acceptatiecriterium).
5. `mail_<voornaam>.md` per contactpersoon, uit `templates/mail_contact.md`.

Vervang alle `{{PLACEHOLDERS}}`. Blijft er één staan, dan is de skill niet klaar.

## Stap 5 — Rond af

Meld in vijf regels: welke mappen, welke bestanden, welke velden nog open staan, en wat
de logische volgende stap is (meestal: de klant om het acceptatiecriterium vragen, of een
kickoff inplannen).

Wijs erop dat het CRM een aparte handeling is: een klant aanmaken in de mappenstructuur
maakt nog geen project in het Agyle CRM. Vraag of dat ook moet — dan kan dat via de
`agyle`-MCP.

## Wat deze skill niet doet

- Geen offerte schrijven — dat is `/voorstel-site` of `/onderhoudscontract`.
- Geen bestaande klantmappen herstructureren zonder expliciet akkoord.
- Geen contactpersonen of mailadressen verzinnen. Onbekend = vragen.
