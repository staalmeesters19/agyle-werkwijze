# Contractstructuur — 11 artikelen

De vaste indeling van een Agyle-onderhoudsovereenkomst. Per artikel: het doel, de kern en de valkuil. De voorbeeldzinnen komen uit een echt getekend traject (SaaS-achtige applicatie in beheer bij de klant) — vervang de inhoud, houd de vorm.

Bovenaan het document (vóór de artikelen):

```markdown
# Onderhoudsovereenkomst <Dienst>

**Ondertitel:** <Dienst> — beheer, hosting en beschikbaarheid
**Betreft:** Onderhoud, beheer en beschikbaarheid <dienst> (vervolg op <eerdere offerte, datum>)
**Datum:** <maand jaar>
**Gericht aan:** <Naam ondertekenaar>, <Klant B.V.> (<e-mail>)
**Inhoudelijk contact:** <naam>

---

Geachte heer/mevrouw <achternaam>,

<Openingsalinea: de dienst is de pilotfase voorbij, draait in productie, en verdient
een operationeel kader. Eén alinea, geen opsomming.>
```

De meta-regels (alles tot de `---`) worden de grijze meta-tabel in de PDF. `**Ondertitel:**` verschijnt onder de titel, niet in de tabel.

---

## 1. Introductie en context

**Doel:** waarom deze overeenkomst nu bestaat — de overgang van projectmatig/uurbasis naar een operationele dienst.

Benoem wat de dienst technisch doet, dat de ontwikkeling op uurbasis verliep, en dat continuïteit nu iets anders vraagt: beschikbaar blijven, meebewegen met kleine wijzigingen, snel oppakken bij storing. Sluit af met "als aanvulling op de getekende offerte van <datum>".

**Valkuil:** hier al over prijzen beginnen.

## 2. Opzet: drie pilaren

**Doel:** het aanbod in drie woorden begrijpelijk maken.

- **Hosting** — waar draait het, wie neemt het af, wat doet de leverancier daarop.
- **Onderhoud** — beschikbaar houden, monitoring, periodieke beveiligingscontroles, verstoringen oplossen.
- **Updates** — kleine aanpassingen, beveiligingsupdates, doorontwikkeling binnen het urenkader.

**Valkuil:** een vierde en vijfde pilaar toevoegen. Drie is het maximum dat een lezer onthoudt.

## 3. Onderhoudspakketten

**Doel:** de keuze presenteren. Standaard twee pakketten, met een gunstiger uurtarief op het grootste.

```markdown
| Pakket | Uren per maand | Tarief | Maandbedrag (excl. btw) |
|---|---|---|---|
| **Basis** | ca. 5 uur | € 175 / uur | € 875 |
| **Uitgebreid** | ca. 10 uur | € 160 / uur | € 1.600 |
```

Eén zin waarom het grootste pakket goedkoper per uur is ("tegenprestatie voor het grotere maandelijkse volume"). Daarna, optioneel, één box:

```markdown
:::teal
**Ter overweging.** <Feitelijke schets van de groei: aantal productie-omgevingen nu,
verwachting daarna. Wat het kleine pakket doet, wat het grote pakket extra mogelijk
maakt — nieuwe deployment, maandelijkse scan en rapportage, kleine aanpassingen —
tegen een gunstiger uurtarief.>
:::
```

Schrijf "ca. X uur", niet "X uur": het is een kader, geen strippenkaart met harde afrekening.

**Valkuil:** drie of meer pakketten (keuzestress), of korting op het kleinste pakket.

## 4. Wat valt binnen het pakket, en wat erbuiten

**Doel:** scopegrens. Dit artikel voorkomt de meeste discussies achteraf.

**Binnen het pakket** — beschikbaar houden en monitoring; verstoringen oplossen; kleine aanpassingen, correcties en configuratiewijzigingen; deployment na akkoord; een **maandelijkse kwetsbaarheidsscan** (bijv. Docker Scout) plus beveiligingsupdates; een **korte maandelijkse rapportage** van de uitgevoerde controles.

Die laatste twee zijn bewust in-pakket: ze maken proactief onderhoud zichtbaar en rechtvaardigen het maandbedrag zonder dat er storingen hoeven te zijn.

**Buiten het pakket (op uurbasis)** — grotere wijzigingen en nieuwe functionaliteit; werk dat de pakketuren structureel overstijgt; nieuwe trajecten/losstaande scopes.

Sluit af: buiten-pakket-werk wordt vooraf afgestemd en gefactureerd tegen het **volle** uurtarief, conform de systematiek van de eerdere offerte. Grotere wijzigingen waar nodig als aparte scope begroot.

**Valkuil:** het kortingstarief laten doorlopen naar meerwerk.

## 5. Beschikbaarheid en werkwijze

**Doel:** een licht SLA-kader zonder juridische zwaarte.

- **Beschikbaarheid:** bedoeld voor continu gebruik; leverancier bewaakt en grijpt in.
- **Reactietijd:** meldingen binnen één werkdag opgepakt; blokkerende verstoring met voorrang, waar mogelijk dezelfde werkdag.
- **Bereikbaarheid:** kantooruren op werkdagen, via een vast aanspreekpunt.
- **Beveiliging:** zo veilig mogelijk houden via periodieke scans en tijdige updates — *inspanning, geen absolute garantie*.
- **Kleine aanpassingen** worden in overleg ingepland binnen de pakketuren.

Afsluitende zin: inspanningsverplichting, passend bij de open samenwerking; geen vaste boeteclausules.

**Valkuil:** uptime-percentages of penalty's beloven. Zodra de klant hardere garanties wil, is dat een reden voor een zwaarder pakket — niet iets om gratis mee te nemen.

## 6. Hosting en eenmalige inrichting

**Doel:** de scherpste rolverdeling in het document, plus het eenmalige werk bij livegang.

Drie alinea's:

1. **Wie is waarvoor verantwoordelijk.** Klant: hostingomgeving, netwerk, onderliggende server, code-repository en deployment-pipeline. Leverancier: de applicatie — (code-)updates aanleveren en inchecken, containerbeheer, de controles en rapportage uit artikel 4. Hostingkosten vallen buiten deze overeenkomst.
2. **Hoe updates landen.** Via de door de klant beschikbaar gestelde repository en geautomatiseerde pipeline. Benoem dat de applicatie binnen het eigen netwerk draait en niet vanaf internet benaderbaar is; externe ontsluiting is een keuze én verantwoordelijkheid van de klant.
3. **Eenmalige inrichting bij livegang.** Wat er al klaar is (containerisatie, healthchecks, auto-updates) en wat er nog moet gebeuren: repository en pipeline opzetten, gecontroleerde deployment in de klantomgeving, verifiëren dat het gelijkwaardig functioneert aan de huidige omgeving.

Daarna in een box:

```markdown
:::box
Deze eenmalige inrichting wordt uitgevoerd op uurbasis tegen **€ 175 per uur (excl. btw)**
en wordt richtinggevend geschat op **6 tot 10 uur (circa één werkdag)**, afhankelijk van de
gereedheid van de omgeving (Docker-installatie, netwerk- en poortconfiguratie, repository en
pipeline, DNS en SSL). Er worden uitsluitend de daadwerkelijk bestede uren gefactureerd;
deze inrichting valt buiten het maandelijkse onderhoudspakket.
:::
```

Altijd een **band** (6–10 u), nooit een vast bedrag: de onbekenden zitten in de klantomgeving. Benoem die onbekenden expliciet — dat maakt de band geloofwaardig in plaats van vrijblijvend.

**Valkuil:** "wij verzorgen de hosting" schrijven terwijl de klant de omgeving afneemt. Dan koop je infra-risico zonder infra-marge.

## 7. Looptijd, verlenging en opzegging

Ingangsdatum koppelen aan een gebeurtenis (livegang na afronding van de migratie), niet aan een kalenderdatum die kan schuiven. Standaard: **twaalf (12) maanden**, daarna stilzwijgend door en **maandelijks opzegbaar** met één maand opzegtermijn, schriftelijk. Verwijs naar het continuïteitsartikel voor wat er bij beëindiging gebeurt.

**Valkuil:** vanaf dag één maandelijks opzegbaar. Terugvalpositie in de onderhandeling is 6 maanden, niet 0.

## 8. Indexatie

Uurtarieven en maandbedrag jaarlijks per 1 januari geïndexeerd op de CBS-Dienstverleningsprijzenindex (DPI), met een vervangende index als de DPI verdwijnt. Eén zin waarom: transparant en marktconform blijven.

## 9. Randvoorwaarden opdrachtgever

Wat de klant moet leveren wil de leverancier kunnen presteren: beschikbaarheid en beheer van omgeving/netwerk/repository; een IT-verantwoordelijke als aanspreekpunt; tijdige aanlevering van informatie, documentatie en toegangen; een inhoudelijk aanspreekpunt voor besluitvorming; toegang tot systemen, testomgevingen en stakeholders.

Sluit af: worden deze niet tijdig vervuld, dan kan dat invloed hebben op beschikbaarheid, planning en kosten.

## 10. Uitsluitingen en risicoverdeling

Inspanningsverplichting, geen gegarandeerd resultaat. Niet verantwoordelijk voor verstoringen door: onvolledige klantinformatie, beperkingen of uitval van de door de klant afgenomen omgeving/netwerk/pipeline, wijzigingen vanuit de klant, of afhankelijkheden bij derden. Werk boven de pakketuren of buiten scope wordt aanvullend op uurbasis gefactureerd.

Eén compacte alinea. Dit is het spiegelbeeld van artikel 6 en 9 — houd de bewoordingen consistent met die artikelen.

## 11. Algemene voorwaarden, intellectueel eigendom en continuïteit

Alinea 1: welke algemene voorwaarden gelden (bijv. de meest recente NL Digital Voorwaarden, gedeponeerd bij de KvK onder nummer 30174840), plus de eigendoms-/exploitatiebepalingen uit de eerdere offerte. Rangorde vastleggen: bij tegenstrijdigheid prevaleert deze overeenkomst.

Alinea 2 — **continuïteitsclausule**, het vertrouwensanker: bij beëindiging van de leverancier worden alle noodzakelijke onderdelen onvoorwaardelijk en zonder aanvullende vergoeding overgedragen — broncode, technische en functionele documentatie, configuratiebestanden, scripts, software- en cloudcomponenten, en de benodigde toegangen. De klant mag de oplossing daarna zelfstandig of via een derde beheren.

Deze clausule kost niets en neemt de grootste bezwaren bij een kleine leverancier weg. Altijd opnemen.

---

## Ondertekenblok

Sluit het document hiermee af (de `---` ervoor is optioneel):

```markdown
**Voor akkoord,**

| Te leveren door | Te leveren aan |
|---|---|
| Datum: | Datum: |
| Handtekening: | Handtekening: |
| **Abdul Malik** — Director / Founder | **<Naam klant>** — <Functie> |
| Agyle B.V., Veldzigt 2, 3454 PW Utrecht | <Klant B.V.>, <adres, postcode plaats> |
```

De generator herkent deze tabel aan de kop en rendert hem als twee kaders. Houd de regelvolgorde aan: `Datum:`, `Handtekening:`, naam+functie, bedrijf+adres (bedrijfsnaam vóór de eerste komma komt op een eigen regel).

---

## Opmaak-cheatsheet

| Markdown | Resultaat in de PDF |
|---|---|
| `# Titel` | koptitel linksboven, naast het logo |
| `**Ondertitel:** …` | grijze subtitel onder de titel |
| `**Betreft:** …` (vóór de eerste `---`) | rij in de meta-tabel |
| `## 4. Titel` | artikelkop met zwarte genummerde badge |
| `### Subkop` | vette subkop zonder badge |
| `**Binnen het pakket:**` (hele alinea vet) | vetgedrukte tussenregel |
| `- punt` | bullet |
| tabel | zwarte kop, lichtblauwe zebra-rijen |
| `:::teal … :::` | box met zwarte rand op lichtblauw — voor "Ter overweging" |
| `:::box … :::` of `> …` | grijze box met zwarte linkerbalk — voor voorwaarden/bedragen |
| `| Te leveren door | Te leveren aan |` | ondertekenblok met twee kaders |

Bedragen schrijf je als `€ 175` en `€ 1.600` (spatie na het euroteken, punt als duizendtal). Gebruik echte em-dashes (—) in lopende tekst.
