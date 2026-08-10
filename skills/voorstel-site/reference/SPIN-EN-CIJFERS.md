# De rekenlaag — van pijn naar bedrag

Het playbook regelt de vorm. Dit bestand regelt het betoog: hoe je de implicatie kwantificeert,
saldeert en presenteert zonder in Clark's val te lopen.

**De regel:** *elk bedrag dat de pijn beschrijft komt uit de klant. Elk bedrag dat de oplossing
beschrijft komt uit ons. Ze staan in één tabel op één scherm.*

Clark zet de besparing (€11.000–13.000 LinkedIn) en de nieuwe last (€3.600–6.000 Krypton-licentie)
allebei op de pagina, ~5000px uit elkaar, en saldeert nooit. Daar zit het gat.

---

## 1. Discovery — de kostenposten die je móét ophalen

Naast de 25 klantfeiten uit SKILL.md stap 1: zonder deze zes bestaat er geen rekensom. Vraag ze
letterlijk uit, in het gesprek, en noteer wie het zei.

| # | Post | Vraag die je stelt |
|---|---|---|
| 1 | **Frequentie** | Hoe vaak gebeurt dit? Per week, per maand, per jaar? |
| 2 | **Tijd per keer** | Hoe lang ben je er dan mee bezig — en wie doet het? |
| 3 | **Uurtarief van die persoon** | Intern tarief of loonkosten+opslag. Vraag het, gok het niet |
| 4 | **Directe uitgaven nu** | Tooling, licenties, bureaus, uitzendfees, advertentiebudget — met bedrag en looptijd |
| 5 | **Gemiste opbrengst** | Wat gaat er niet door omdat dit niet lukt? Orders, capaciteit, projecten |
| 6 | **Hoe lang al** | De duur is de vermenigvuldiger. "Vier jaar open" is de hele implicatie in drie woorden |

**Als de klant het niet weet:** dat is zelf een bevinding, geen probleem. Zet in het voorstel
*"jullie meten dit nu niet"* en maak het meetbaar-maken onderdeel van fase 1. Nooit een getal
verzinnen om de tabel vol te krijgen.

---

## 2. De implicatie-rekensom

De I van SPIN is een vermenigvuldiging, geen bijvoeglijk naamwoord. "Dit kost veel tijd" is geen
implicatie; **€3.400 per maand** is een implicatie.

### De drie sommen die je altijd maakt

```
A  Kosten van niets doen, per jaar
   = (frequentie/jr × tijd per keer × uurtarief)        ← verborgen uren
   + directe uitgaven nu                                 ← wat ze al betalen
   + gemiste opbrengst                                    ← alleen als de klant hem zelf noemt

B  Nieuwe last, per jaar — ALLES, ook wat wij liever niet tonen
   = onze fee
   + licenties/tooling die doorlopen
   + advertentie- of verbruiksbudget
   + interne uren die het van de klant vraagt × hun tarief

C  Netto per jaar = A − B          Terugverdientijd = eenmalige investering ÷ (A − B) × 12
```

**Post B4 is de post die iedereen weglaat en die elke klant zelf uitrekent.** Zet hem er zelf in;
dat je hem noemt is meer waard dan wat hij kost. Het is dezelfde beweging als de
tijdsinvestering-sectie: het bezwaar preëmptief adresseren.

### Conservatief rekenen — underpromise, hard

| Regel | Waarom |
|---|---|
| **Bandbreedtes, geen puntgetallen** | €28.000–34.000 is geloofwaardig; €31.427 is verzonnen precisie en één navraag van instorten |
| **Reken A met de ondergrens, B met de bovengrens** | Dan is de netto-uitkomst je vloer, niet je plafond. Alles wat beter gaat is meevaller |
| **Gemiste opbrengst alleen als de klant hem noemde** | Anders is het jouw aanname in hun mond. De zwakste post in elke business case |
| **Vermeld het jaar en de bron per regel** | "Opgave Mariël, gesprek 09-07" onder de tabel. Eén regel, en de hele tabel wordt navraagbaar |
| **Btw expliciet** | Eén keer, bij de prijs. Niet verstopt in een voetnoot of pas in de PDF |

---

## 3. De saldering — één tabel, één scherm

Dit is het blok dat Clark niet heeft. Het hoort in de kostensectie, direct onder het bedrag.

| | Nu | Met ons | Verschil |
|---|---:|---:|---:|
| Tooling / licenties | € … | € … | |
| Bureau- of inhuurkosten | € … | € … | |
| Interne uren (… u × € …) | € … | € … | |
| Onze fee | — | € … | |
| Advertentie-/verbruiksbudget | € … | € … | |
| **Totaal per jaar** | **€ …** | **€ …** | **€ …** |

Daaronder, verplicht, drie regels:

- **Eenmalig:** € … (opstart)
- **Terugverdiend na:** … maanden
- **Totaal over de looptijd van … maanden:** € … excl. btw

Die laatste regel is het duurste vastgoed op een offerte. Clark laat hem leeg en vult hem met een
belofte in plaats van een getal — dat is de reden dat hun samenvatting visueel als een totaal leest
maar er geen is. Zet daar een bedrag.

**Presentatie:** de "nu"-kolom in `--muted`, de "met ons"-kolom in `--on-dark`, het verschil in
`--ok` of `--sky`. Nul extra kleuren nodig. Totaalrij `border-top: 2px`, `tabular-nums`, en de
eenheid in dezelfde grootte als het getal.

---

## 4. Grafiek of drie getallen

Alleen een grafiek als de vier voorwaarden uit playbook §6.1 haalbaar zijn. Bij een besparingscurve
komt daar één voorwaarde bij:

> **De curve moet doorlopen tot voorbij het punt waar jouw kosten stoppen te dalen.**

Clarks kostencurve loopt naar nul terwijl er een licentie doorloopt — de grafiek spreekt de prijskaart
dertig centimeter rechts ervan tegen. Als er een structurele last blijft, dan vlakt de curve daarop
af en dat is zichtbaar. Een eerlijke asymptoot is overtuigender dan een dalende lijn naar nul, omdat
iedereen weet dat nul niet bestaat.

**Anders: drie getallen op een rij** (`clamp(40px, 4.5vw, 96px)`, weight 900) met één zin eronder.

```
  € 34.000          11 maanden           2 uur
  netto per jaar    terugverdiend        per week van jullie
```

Dat leest sneller dan elke grafiek en is niet aan te vallen.

---

## 5. Need-payoff — de N die je niet zelf invult

De sterkste zin in de hele Clark-pagina gaat tegen hun eigen belang in:
*"Het doel is altijd hetzelfde. Dat jullie ons op een gegeven moment niet meer nodig hebben."*
Dat is de enige zin die volledig geloofd wordt.

Vertaling naar de rekenlaag: **de laatste stap zet je niet in cijfers, maar in een vraag aan de
klant.** Sluit de kostensectie niet af met "dus u bespaart X", maar met de vraag die zij zelf
beantwoorden:

> *"Als deze rollen over negen maanden gevuld zijn en het proces staat bij jullie op de plank —
> wat doet dat met de planning voor 2027?"*

Zij noemen dan een getal dat groter is dan het jouwe, en het is van hen. Dat is de N van SPIN, en
het is de enige plek in het document waar je een bedrag mag suggereren zonder het te onderbouwen —
juist omdat je het niet opschrijft.

---

## 6. Route B — kwantificeren zonder je eigen prijs te tonen

Kies je route B uit SKILL.md stap 0 (geen tarieven in het klantstuk), dan vervalt de rekensom níet.
Kolom A is namelijk **hun** geld, niet jouw tarief.

- Toon **"Nu"** volledig: wat het probleem hen vandaag kost, met bron per regel.
- Vervang **"Met ons"** door **scope + doorlooptijd + tijdsinvestering**.
- Vervang **terugverdientijd** door *"we spreken vooraf af waar de norm ligt waaronder we zakken"*.
- Het totaal en de netto-besparing leven in de interne versie.

De implicatie blijft daarmee volledig overeind — je laat alleen de laatste kolom leeg. In de
praktijk vraagt de klant er dan zelf om, en dat is een betere positie dan hem ongevraagd geven.

---

## 7. Checklist vóór levering

- [ ] Elke pijn in de pijnmuur heeft een getal, een duur of een naam die de klant zelf noemde
- [ ] Kolom A is opgebouwd uit klantopgaven, met bron en datum per regel
- [ ] Kolom B bevat **alle** posten, inclusief onze fee, doorlopende licenties, verbruiksbudget en
      de interne uren die wij van de klant vragen
- [ ] Netto per jaar, terugverdientijd en **totaal over de looptijd** staan alle drie op de pagina
- [ ] Bandbreedtes, geen puntgetallen; A op de ondergrens, B op de bovengrens
- [ ] Btw genoemd bij de prijs, niet in een voetnoot
- [ ] Als er een curve staat: hij vlakt af op de structurele last, hij loopt niet naar nul
- [ ] Alle bedragen komen uit één constantenobject — pagina, samenvatting en export renderen daaruit
- [ ] De kostensectie eindigt op een vraag aan de klant, niet op een conclusie van ons
