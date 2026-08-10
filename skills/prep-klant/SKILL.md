---
name: prep-klant
description: SPIN-klantvoorbereiding voor een nieuwe prospect. Onderzoekt het bedrijf via web-search, toetst het tegen het Agyle propositie-referentiekader, en levert Situation-, Problem-, Implication- en Need-Payoff-vragen plus een branded PDF. Gebruik vóór een eerste gesprek met een bedrijf dat nog geen klant is — voor bestaande klanten gebruik je /briefing.
---

# Skill: `/prep-klant` — SPIN Klantvoorbereiding

## Trigger

Wanneer de gebruiker `/prep-klant [Bedrijfsnaam]` of `/prep-klant` typt, voer je onderstaande workflow uit.

---

## Stap 1 — Bedrijfsnaam bepalen

Als de bedrijfsnaam meegegeven is in de trigger, gebruik die. Anders vraag je:

> "Voor welk bedrijf wil je je voorbereiden?"

Sla de bedrijfsnaam op als `[Bedrijfsnaam]`.

---

## Stap 2 — Context ophalen (één bericht, 4 vragen)

Stel de volgende 4 vragen in één bericht:

> **Snelle context voor [Bedrijfsnaam]**
>
> 1. Met wie spreek je? (naam + functie van de contactpersoon, als bekend)
> 2. Wat voor type gesprek is het? (bijv. eerste kennismaking, demo, voorstelgesprek, follow-up)
> 3. Wat weet je al over dit bedrijf of deze persoon?
> 4. Welke Agyle-diensten zijn mogelijk relevant? (bijv. automatisering, AI-implementatie, data-integratie — of "weet ik nog niet")
>
> *Typ "doorgaan" om dit over te slaan en direct te beginnen met research.*

Wacht op antwoord. Verwerk de antwoorden (of sla over bij "doorgaan"). Sla de datum van het gesprek op als `[Gespreksdatum]` als de gebruiker die noemt, anders gebruik je vandaag als `[Datum opgesteld]`.

---

## Stap 3 — Webresearch

Voer de volgende 5 zoekopdrachten uit met WebSearch, én fetch de bedrijfswebsite met WebFetch:

1. `[Bedrijfsnaam] bedrijf over ons missie diensten`
2. `[Bedrijfsnaam] automatisering digitalisering AI`
3. `[Bedrijfsnaam] nieuws 2024 2025 uitdagingen groei`
4. `[Bedrijfsnaam] LinkedIn bedrijfspagina medewerkers`
5. `[Bedrijfsnaam] jaarverslag resultaten OR "digitale transformatie"`

Probeer ook de website te fetchen: zoek het domein via de eerste zoekopdracht en fetch de homepage + eventueel de "Over ons" pagina.

Noteer per bron:
- URL
- Sector / branche
- Geschatte omvang (medewerkers, omzet indien gevonden)
- Kernactiviteiten / producten / diensten
- Gebruikte tools of systemen (indien vermeld)
- Recent nieuws, uitdagingen, groei, of strategische prioriteiten
- Wat NIET gevonden is

---

## Stap 4 — Verificatiestap (wachten op bevestiging)

Presenteer een samenvatting van de research en wacht op bevestiging voordat je verdergaat:

```
## Gevonden over [Bedrijfsnaam]

**Bronnen:** [lijst van URLs]

- **Sector:** ...
- **Omvang:** ... medewerkers / ... omzet
- **Kernactiviteiten:** ...
- **Technologie/systemen:** ...
- **Recent nieuws/uitdagingen:** ...
- **Strategische prioriteiten:** ...

**Niet gevonden:** [onderwerpen waarvoor geen betrouwbare info beschikbaar was]

---
Klopt dit? Wil je iets toevoegen of corrigeren voordat ik de SPIN-vragen maak?
*(Typ "doorgaan" om direct verder te gaan)*
```

Wacht op reactie. Verwerk correcties of aanvullingen. Ga pas naar stap 5 wanneer de gebruiker akkoord gaat of "doorgaan" typt.

---

## Stap 5 — Analyse (intern, niet tonen aan gebruiker)

Bepaal op basis van de bevestigde research:

**Waarschijnlijke huidige situatie:**
- Hoe werkt dit bedrijf nu waarschijnlijk? Welke processen zijn handmatig of inefficiënt?
- Welke systemen gebruiken ze (of ontbreken ze)?
- Waar zitten typische pijnpunten voor een bedrijf van deze omvang in deze sector?

**Meest relevante Agyle-diensten** (gebruik het onderstaande propositie-referentiekader):

### Agyle Propositie-referentiekader (intern gebruik)

Agyle helpt organisaties met:
- **Automatisering van repetitieve processen** (RPA, workflow automatisering) — relevant als er veel handmatig kopieerwerk, Excel-gebruik of trage rapportages zijn
- **AI-implementaties** (LLM-toepassingen, documentverwerking, chatbots, slimme workflows) — relevant als er kennisintensieve processen, grote documentstromen of klantvragen zijn
- **Data-integratie** (koppelen van systemen, dashboards, realtime inzichten) — relevant als er datasilo's, trage besluitvorming of rapportage-overhead is
- **Procesanalyse & change management** — relevant bij groei, reorganisatie, of als technologie-adoptie stagneert

**Typische "before state" die Agyle oplost:**
- Medewerkers kopiëren data tussen systemen (Excel, e-mail, CRM)
- Rapportages kosten dagelijks uren handmatig werk
- Onboarding of klantprocessen zijn inconsistent en foutgevoelig
- Beslissingen worden genomen zonder actuele data
- IT-capaciteit is het knelpunt voor elke verbetering

---

## Stap 6 — SPIN-vragen genereren

Genereer bedrijfsspecifieke SPIN-vragen. **Geen generieke placeholders.** Gebruik de bedrijfsnaam, sector, bekende systemen, en gevonden uitdagingen expliciet in de vragen.

### Richtlijnen per categorie:

**Situation (4-6 vragen)** — feiten valideren, hoe werkt het nu?
- Concrete vragen over hun huidige werkwijze, tools, processen
- Opent het gesprek, bouwt vertrouwen, verzamelt context
- Voorbeeld toon: "Hoe is jullie [specifiek proces] op dit moment ingericht?"

**Problem (4-6 vragen)** — pijnpunten en frustraties blootleggen
- Richt op de meest waarschijnlijke knelpunten voor dit bedrijf
- Vraag naar frustraties, bottlenecks, dingen die "niet lekker lopen"
- Voorbeeld toon: "Welke uitdagingen ervaren jullie bij [specifiek pijnpunt]?"

**Implication (6-8 vragen — meest kritisch, meest gedetailleerd)** — de pijn verdiepen
- Dit zijn de krachtigste vragen. Ze laten de prospect de échte impact voelen.
- Dek meerdere impact-dimensies:
  - **Financieel**: wat kost het probleem in tijd, geld, fouten?
  - **Operationeel**: wat vertraagt het? Welke andere processen lijden hieronder?
  - **Strategisch**: wat kunnen ze NIET doen terwijl dit speelt?
  - **Reputatie/klanttevredenheid**: hoe merken klanten of partners dit?
  - **Concurrentie**: wat doen concurrenten die zij nog niet doen?
  - **Medewerkers**: wat is het effect op motivatie, capaciteit, retentie?
- Voorbeeld toon: "Als [probleem] blijft bestaan, wat betekent dat dan voor [impact-dimensie]?"

**Need-Payoff (4-6 vragen)** — de gewenste toekomst, verwoord door de prospect zelf
- Hypothetisch geformuleerd: "Als...", "Stel dat...", "Wat zou het betekenen als..."
- Laat de prospect de waarde benoemen — niet jij
- Richt op concrete voordelen die voor hén het meest relevant zijn
- Voorbeeld toon: "Als jullie [pijnpunt] volledig geautomatiseerd zouden hebben, wat zou dat concreet opleveren?"

---

## Stap 7 — Kwaliteitscontrole (zelf-check vóór opslaan)

Controleer het document op de volgende punten voordat je opslaat. Als iets ontbreekt, verbeter je het eerst:

- [ ] Alle SPIN-vragen zijn specifiek voor dit bedrijf (geen generieke "[bedrijf]" placeholders)
- [ ] Minimaal 6 Implication-vragen, verspreid over meerdere impact-dimensies
- [ ] Need-Payoff vragen zijn hypothetisch geformuleerd ("Als...", "Stel dat...")
- [ ] Bedrijfsprofiel is gebaseerd op daadwerkelijk gevonden informatie (niet verzonnen)
- [ ] Aannames zijn gelabeld als "aanname" of "te valideren"
- [ ] Gespreksflow Tips zijn praktisch en specifiek voor deze klant/sector

---

## Stap 8 — Document schrijven en opslaan

Schrijf het document met de onderstaande structuur en sla het op als:

`<prep_output_dir>/[Bedrijfsnaam] - [YYYY-MM-DD].md`

waarbij `<prep_output_dir>` het pad is uit `prep_output_dir` in
`~/.claude/agyle-persoon.json`. Ontbreekt dat bestand, vraag dan waar het document heen moet.

Gebruik de datum van vandaag als `[YYYY-MM-DD]` tenzij de gebruiker een gespreksdatum heeft opgegeven.

---

## Output Document Template

```markdown
# Klantvoorbereiding: [Bedrijfsnaam]

| | |
|---|---|
| **Gespreksdatum** | [datum of "nog niet bekend"] |
| **Type gesprek** | [kennismaking / demo / voorstelgesprek / follow-up] |
| **Contactpersoon** | [naam + functie of "onbekend"] |
| **Datum opgesteld** | [vandaag] |

---

## Bedrijfsprofiel

**Sector:** [sector/branche]
**Omvang:** [aantal medewerkers / omzet indien bekend]
**Kernactiviteiten:** [wat doet het bedrijf]
**Technologische volwassenheid:** [laag / gemiddeld / hoog — gebaseerd op gevonden info, gelabeld als aanname indien onzeker]
**Recente ontwikkelingen:** [nieuws, groei, uitdagingen, strategische prioriteiten]

**Bronnen:**
- [URL 1]
- [URL 2]
- [etc.]

---

## Waarschijnlijke Situatie (aannames te valideren)

**Huidige werkwijze (aanname):**
[Beschrijving van hoe ze waarschijnlijk werken op basis van sector en omvang]

**Waarschijnlijke systemen/tools (aanname):**
[Wat ze waarschijnlijk gebruiken of juist missen]

**Meest waarschijnlijke pijnpunten (aanname):**
[Top 3-5 pijnpunten die relevant zijn voor dit type bedrijf]

**Meest relevante Agyle-diensten voor deze klant:**
[Welke diensten het beste aansluiten en waarom]

---

## SPIN Vragen

### Situation — Feiten verzamelen

*Doel: valideer je aannames, begrijp de huidige werkwijze*

1. [Specifieke situatievraag]
2. [Specifieke situatievraag]
3. [Specifieke situatievraag]
4. [Specifieke situatievraag]
5. [Specifieke situatievraag indien van toepassing]

### Problem — Pijnpunten blootleggen

*Doel: laat de prospect de uitdagingen benoemen*

1. [Specifieke probleemvraag]
2. [Specifieke probleemvraag]
3. [Specifieke probleemvraag]
4. [Specifieke probleemvraag]
5. [Specifieke probleemvraag indien van toepassing]

### Implication — De pijn verdiepen

*Doel: de impact van het probleem voelbaar maken — dit zijn de krachtigste vragen*

**Financiële impact:**
1. [Implication vraag — financieel]
2. [Implication vraag — financieel]

**Operationele impact:**
3. [Implication vraag — operationeel]
4. [Implication vraag — operationeel]

**Strategische impact:**
5. [Implication vraag — strategisch]
6. [Implication vraag — strategisch]

**Concurrentie- of reputatie-impact:**
7. [Implication vraag — concurrentie/reputatie]
8. [Implication vraag — medewerkers/capaciteit indien relevant]

### Need-Payoff — De gewenste toekomst

*Doel: laat de prospect zelf de waarde van de oplossing verwoorden*

1. [Need-Payoff vraag — hypothetisch]
2. [Need-Payoff vraag — hypothetisch]
3. [Need-Payoff vraag — hypothetisch]
4. [Need-Payoff vraag — hypothetisch]
5. [Need-Payoff vraag — hypothetisch indien van toepassing]

---

## Gespreksflow Tips

**Opening:**
[Hoe je het gesprek kunt beginnen — specifiek voor dit bedrijf/type gesprek]

**Aanbevolen volgorde:**
[Welke vragen te stellen in welke volgorde — niet alle vragen hoeven aan bod te komen]

**Aandachtspunten:**
[Specifieke dingen om op te letten bij dit bedrijf of deze sector]

**Verwachte bezwaren:**
- [Bezwaar 1] → [Hoe hierop in te spelen]
- [Bezwaar 2] → [Hoe hierop in te spelen]

**Aanbevolen next step:**
[Wat je aan het einde van het gesprek wilt afsluiten als concrete vervolgstap]
```

---

## Afsluiting

Na het opslaan van het .md bestand, genereer je automatisch een professionele PDF:

1. Voer het volgende Bash-commando uit om de PDF te genereren:
   ```bash
   python "$HOME/.claude/skills/prep-klant/md_to_pdf.py" "[pad naar .md bestand]"
   ```
   Dit genereert een PDF met dezelfde naam naast het .md bestand, met professionele opmaak (gestylede tabellen, Agyle branding, paginanummering).

2. Bevestig aan de gebruiker:

> "Klantvoorbereiding opgeslagen als PDF: `[Bedrijfsnaam] - [YYYY-MM-DD].pdf`
>
> **Korte samenvatting:**
> - [2-3 zinnen over de meest relevante bevindingen en focus voor het gesprek]
>
> Succes met het gesprek!"
