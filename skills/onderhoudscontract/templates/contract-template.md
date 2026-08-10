# Onderhoudsovereenkomst <DIENST>

**Ondertitel:** <DIENST> — beheer, hosting en beschikbaarheid
**Betreft:** Onderhoud, beheer en beschikbaarheid <DIENST> (vervolg op <EERDERE OFFERTE, DATUM>)
**Datum:** <MAAND JAAR>
**Gericht aan:** <ONDERTEKENAAR KLANT>, <KLANT B.V.> (<E-MAIL>)
**Inhoudelijk contact:** <CONTACTPERSOON>

---

Geachte heer/mevrouw <ACHTERNAAM>,

<Openingsalinea: de dienst is de pilotfase voorbij, draait in productie (<welke omgevingen>), en verdient nu een operationeel kader. Doel is een definitieve, operationele dienst met een vast maandelijks kader voor beheer en kleine aanpassingen — geen pilot die blijft hangen.>

## 1. Introductie en context

<Wat de dienst technisch doet en waar die draait. Ontwikkeling verliep projectmatig op uurbasis; een operationele dienst vraagt continuïteit: beschikbaar blijven, meebewegen met kleine wijzigingen, snel oppakken bij verstoring. Deze overeenkomst legt dat vast als aanvulling op de getekende offerte van <DATUM>.>

## 2. Opzet: drie pilaren

De dienst rust op drie pilaren:

- **Hosting** — <waar draait het, wie neemt het af, wat doet de leverancier daarop>.
- **Onderhoud** — het geborgd beschikbaar houden van de dienst, monitoring, periodieke beveiligingscontroles en het oplossen van verstoringen.
- **Updates** — kleine aanpassingen, beveiligingsupdates en doorontwikkelingen die binnen het maandelijkse urenkader passen.

## 3. Onderhoudspakketten

<KLANT> kiest een van de volgende maandpakketten. De pakketuren zijn bedoeld voor beheer, beschikbaarheid en kleine aanpassingen.

| Pakket | Uren per maand | Tarief | Maandbedrag (excl. btw) |
|---|---|---|---|
| **Basis** | ca. <5> uur | € <175> / uur | € <875> |
| **Uitgebreid** | ca. <10> uur | € <160> / uur | € <1.600> |

Bij het Uitgebreide pakket geldt een gunstiger uurtarief als tegenprestatie voor het grotere maandelijkse volume.

:::teal
**Ter overweging.** <Feitelijke schets van de groei en wat elk pakket daarin betekent. Het Basispakket houdt de bestaande omgeving draaiend en beschikbaar; het Uitgebreide pakket biedt daarnaast ruimte om mee te bewegen — een nieuwe deployment, de maandelijkse kwetsbaarheidsscan en rapportage, en kleine aanpassingen — tegen een gunstiger uurtarief.>
:::

## 4. Wat valt binnen het pakket, en wat erbuiten

**Binnen het pakket:**

- Beschikbaar houden van de dienst en monitoring op het functioneren.
- Oplossen van verstoringen en het herstellen van beschikbaarheid.
- Kleine aanpassingen, correcties en configuratiewijzigingen.
- Deployment van de applicatie na een akkoord op wijzigingen.
- Een maandelijkse kwetsbaarheidsscan van de container (bijvoorbeeld via Docker Scout) en het toepassen van beschikbare beveiligingsupdates.
- Een korte maandelijkse rapportage van de uitgevoerde controles en het onderhoud.

**Buiten het pakket (op uurbasis):**

- Grotere wijzigingen, nieuwe functionaliteit en niet-standaard uitbreidingen.
- Werk dat de pakketuren in een maand structureel overstijgt.
- <Nieuwe trajecten of losstaande scopes>.

Werkzaamheden buiten het pakket worden vooraf in overleg afgestemd en aanvullend gefactureerd tegen het geldende uurtarief van **€ <175> per uur (excl. btw)**, conform de systematiek van de offerte van <DATUM>. Grotere wijzigingen worden waar nodig als aparte scope begroot.

## 5. Beschikbaarheid en werkwijze

<LEVERANCIER> spant zich in om <DIENST> operationeel en beschikbaar te houden. Concreet:

- **Beschikbaarheid:** de dienst is bedoeld voor continu gebruik; <LEVERANCIER> bewaakt het functioneren en grijpt in bij verstoringen.
- **Reactietijd:** meldingen worden binnen één werkdag opgepakt. Een verstoring die het gebruik blokkeert, wordt met voorrang en waar mogelijk dezelfde werkdag opgepakt.
- **Bereikbaarheid:** tijdens kantooruren (werkdagen), via een vast aanspreekpunt.
- **Beveiliging:** <LEVERANCIER> houdt de applicatie zo veilig mogelijk door periodieke kwetsbaarheidsscans en het tijdig toepassen van beschikbare beveiligingsupdates. Dit betreft een inspanning, geen absolute garantie.
- **Kleine aanpassingen** worden in overleg ingepland en binnen de pakketuren uitgevoerd.

Deze afspraken gelden als inspanningsverplichting, passend bij de open samenwerking tussen partijen; er gelden geen vaste boeteclausules.

## 6. Hosting en eenmalige inrichting

<Rolverdeling: wie is verantwoordelijk voor hostingomgeving, netwerk, server, repository en pipeline; wie voor de applicatie, updates, containerbeheer, controles en rapportage. Hostingkosten vallen buiten deze overeenkomst.>

<Hoe updates landen: via repository en geautomatiseerde deployment-pipeline. De applicatie draait binnen het eigen netwerk van <KLANT> en is niet vanaf internet benaderbaar; externe ontsluiting is een keuze en verantwoordelijkheid van <KLANT>.>

**Eenmalige inrichting (bij livegang).** <Wat er al klaar is, en wat er bij livegang gebeurt: repository en pipeline opzetten, gecontroleerde deployment in de klantomgeving, verifiëren dat het gelijkwaardig functioneert aan de huidige omgeving.>

:::box
Deze eenmalige inrichting wordt uitgevoerd op uurbasis tegen **€ <175> per uur (excl. btw)** en wordt richtinggevend geschat op **<6 tot 10> uur (circa <één werkdag>)**, afhankelijk van de gereedheid van de omgeving (<Docker-installatie, netwerk- en poortconfiguratie, repository en pipeline, DNS en SSL>). Er worden uitsluitend de daadwerkelijk bestede uren gefactureerd; deze inrichting valt buiten het maandelijkse onderhoudspakket.
:::

## 7. Looptijd, verlenging en opzegging

De overeenkomst gaat in bij <livegang van DIENST op de omgeving van KLANT, na afronding van de eenmalige migratie> en heeft een looptijd van **twaalf (12) maanden**. Na deze periode loopt de overeenkomst stilzwijgend door en is deze **maandelijks opzegbaar** met een opzegtermijn van één maand. Opzegging vindt schriftelijk plaats. Bij beëindiging gelden de continuïteits- en overdrachtsafspraken uit artikel 11.

## 8. Indexatie

Alle uurtarieven en het maandbedrag worden jaarlijks per 1 januari geïndexeerd op basis van de CBS-Dienstverleningsprijzenindex (DPI). Mocht de CBS-DPI niet langer beschikbaar zijn, dan wordt een vergelijkbare, algemeen geaccepteerde index gehanteerd. Zo blijft het prijsniveau transparant en marktconform.

## 9. Randvoorwaarden opdrachtgever

Voor een soepele uitvoering gelden de volgende randvoorwaarden aan de zijde van <KLANT>:

- Beschikbaarheid en beheer van de hostingomgeving, het netwerk en de code-repository/deployment-pipeline waarop de applicatie draait en wordt bijgewerkt.
- Beschikbaarheid van een IT-verantwoordelijke als aanspreekpunt voor de inrichting en het beheer van omgeving en pipeline.
- Tijdige en volledige aanlevering van benodigde informatie, documentatie en toegangen.
- Beschikbaarheid van een inhoudelijk aanspreekpunt voor afstemming en besluitvorming.
- Toegang tot relevante systemen, testomgevingen en stakeholders.

Wanneer randvoorwaarden niet tijdig worden vervuld, kan dit invloed hebben op beschikbaarheid, planning en kosten.

## 10. Uitsluitingen en risicoverdeling

<LEVERANCIER> werkt op basis van een inspanningsverplichting, niet op basis van gegarandeerd resultaat. <LEVERANCIER> is niet verantwoordelijk voor verstoringen of afwijkingen die ontstaan door onvolledige klantinformatie, beperkingen of uitval van de door <KLANT> afgenomen hostingomgeving, het netwerk of de repository/deployment-pipeline, wijzigingen vanuit <KLANT> of afhankelijkheden bij derden. Werkzaamheden die de pakketuren overstijgen of buiten de afgesproken scope vallen, worden aanvullend op uurbasis gefactureerd.

## 11. Algemene voorwaarden, intellectueel eigendom en continuïteit

Op deze overeenkomst zijn de meest recente versie van de <NL Digital Voorwaarden> van toepassing, zoals gedeponeerd bij de Kamer van Koophandel onder nummer <30174840>, alsook de bepalingen over eigendom, exploitatie en continuïteit zoals vastgelegd in de offerte van <DATUM>. Bij tegenstrijdigheden prevaleren de afspraken uit deze overeenkomst.

In het kader van continuïteit geldt dat bij beëindiging van <LEVERANCIER B.V.> alle noodzakelijke onderdelen van de dienst onvoorwaardelijk en zonder aanvullende vergoeding worden overgedragen aan <KLANT>, waaronder broncode, technische en functionele documentatie, configuratiebestanden, scripts, software- en cloudcomponenten en de benodigde toegangen. <KLANT> verkrijgt hiermee het recht de oplossing zelfstandig of via een aangewezen derde partij te beheren en te onderhouden.

---

**Voor akkoord,**

| Te leveren door | Te leveren aan |
|---|---|
| Datum: | Datum: |
| Handtekening: | Handtekening: |
| **<NAAM LEVERANCIER>** — <FUNCTIE> | **<NAAM KLANT>** — <FUNCTIE> |
| <LEVERANCIER B.V.>, <adres, postcode plaats> | <KLANT B.V.>, <adres, postcode plaats> |
