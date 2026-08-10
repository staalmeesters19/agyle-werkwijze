# Playbook — het premium voorstel-artefact

**Wat dit is.** Een operationeel bouwrecept voor een Agyle-voorstelsite die minstens zo
indrukwekkend is als `voorstel.clark.amsterdam/harwig/`, maar eerlijker en in Agyle-huisstijl
(zwart `#000000` + sky blue `#97D4E8`). Geen samenvatting van de teardown — een bouwinstructie.

**Bron.** `clark-teardown/bron/` (6 handgeschreven bestanden, 3.922 regels, 141.483 bytes) en de
analyses 01–08 in `clark-teardown/analyse/`. Elke bewering over Clark draagt een selector,
regelnummer of letterlijke waarde.

**Correctiebeleid.** Waar `07-kritiek.md` een eerdere analyse tegenspreekt, volgt dit playbook 07.
De vijf correcties die het meest meereizen:

| Onderwerp | Wat 01/02/03/05 zeiden | Wat waar is (07) |
|---|---|---|
| Aantal reveal-elementen | 83 | **78**; `reveal` komt 83× voor als woord, 5 daarvan zijn `.reveal-stagger`-containers zonder `.reveal` |
| 6× `style="color: var(--pink-light)"` op `.section-title` | "reparatie van een ontbrekende CSS-regel" | **No-ops**. `.voorstel-section--dark/--red/--krypton` zetten zelf al `color: var(--pink-light)` (voorstel.css 191-206) en de `<h2>` erft dat |
| Ontwerpframe | 1512px (5 handgekozen waarden uit dode CSS) | Getest op alle 242 levende clamps: **1600 = 55%**, 1280 = 29%, 1440 = 27%, 1512 = **18%** (slechtst) |
| Ruimte-regel | `vw = max ÷ 20`, top-out 2000px | **`vw = max ÷ 18`**, mediane top-out 1800px, mediane `max/min` = 1,67 |
| Eén breakpoint volstaat | ja | **nee** — één inline `style="grid-template-columns: repeat(2,1fr)"` (html r. 315) verslaat de enige media query, dus vacaturekaarten blijven op 375px twee kolommen van ~107px tekstbreedte |

---

## 1. Wat Clark bouwde

### 1.1 Het bouwwerk in cijfers

| | Waarde | Bewijs |
|---|---|---|
| Bestanden, handgeschreven | 6 (1 html, 3 css, 2 js) + 7 svg | `bron/` |
| Regels totaal | **3.922** | html 1420 · voorstel.css 1856 · base.css 175 · pincode.css 140 · voorstel.js 178 · pincode.js 153 |
| Bytes totaal | ~141 KB excl. fonts/beeld/CDN | idem |
| Verdeling | **CSS 60% · markup 22% · JS 17%** | 2.352 / ±880 / 670 regels |
| Zwaarste bestand | `voorstel.css` — 1856 r / 39,8 KB / **47% van alle regels** | |
| Build-step | **geen** | handmatige cache-busting `base.css?v=6`, `voorstel.css?v=11`, `pincode.js?v=3` (html r. 8-10, 1077) |
| `clamp()`-aanroepen | **306** (voorstel.css 242, html 43, pincode.css 12, base.css 9) | |
| Media queries | **1** — `@media (max-width: 768px)` in 3 bestanden | base.css 165, pincode.css 136, voorstel.css 1741 |
| `<section>`-tags | 13, waarvan 11 met expliciete achtergrondklasse | |
| `.reveal`-elementen | **78** | `querySelectorAll('.reveal').length` |
| `box-shadow` in het componentsysteem | **0** | grep over base.css + voorstel.css |
| `aria-*`-attributen in 1421 regels HTML | **1** (`aria-label` op de SVG-grafiek, r. 740) | |
| `prefers-reduced-motion` | **0** in alle CSS-bestanden | |
| `@media print` | 1 regel: `.signature-modal { display: none }` (html r. 194) | |
| Dode CSS | 39 klassen 0× gebruikt, ±19-35% van voorstel.css | `.cal__*` (127 r), `.opstart-tab*` (66 r), `.stat-card*`, `.month-table`, `.next-step*` |
| Externe dependencies | 2 CDN-scripts, ~372 KB, render-blocking, **geen SRI** | html r. 12-13 |

### 1.2 Bouwtijd en architectuur

Het echte product is niet de pagina maar het **chassis + map-per-klant**:

```
voorstel.clark.amsterdam/
├── css/  js/  assets/{fonts,images,icons}     ← gedeeld chassis, één keer gebouwd
├── get-ip.php   send-signed-proposal.php      ← gedeeld
└── harwig/
    ├── index.html                             ← per klant
    └── images/                                ← per klant
```

| | Handmatig | LLM-geassisteerd |
|---|---|---|
| Chassis (eenmalig) | 44–75 u | **25–40 u** |
| Per klant | **6–12 u** | idem |

Bewijs voor LLM-assistentie: **drie JavaScript-dialecten in één pagina** — `pincode.js` volledig ES5
(`var`, `function(){}`), `voorstel.js` volledig modern (`const`, arrows), inline script een
mengelmoes (`let` r. 1081, `const` r. 1084, `var` r. 1210, `async/await` r. 1204).

### 1.3 Het effect, in één zin

Een PDF is een afbeelding van een document; deze pagina is een **ruimte** — je gaat ergens naar
binnen (gate), je beweegt erdoorheen (scroll-reveal), dingen blijven staan terwijl jij loopt
(sticky), en aan het eind is er een deur (Accorderen). Geen van die vier is uit te drukken in
pagina's. Dát is waarom het indruk maakt, en het kost samen ~4 uur bouwtijd.

---

## 2. Waarom het werkt — effect-dragers op rendement

Ratio = (duur-score / 10) ÷ bouwuren de eerste keer. Uit `08-effect-analyse.md` §2, gecorrigeerd
op het reveal-aantal.

| # | Effect-drager | Uren (1e keer) | Herbruik | Duur-score | **Ratio** |
|---|---|---:|---:|---:|---:|
| 1 | **Eigen webfont** (5 gewichten, self-hosted woff2) | 0,5 | 100% | 8 | **16,0** |
| 2 | **Sticky zijkolom** — `position: sticky; top: calc(80px + clamp(40px,4vw,80px))` | 0,5 | 100% | 7 | **14,0** |
| 3 | **Full-bleed sectiekleuren** (5 tokens, 11 secties, 242px lucht) | 1,0 | 100% | 8 | **8,0** |
| 4 | **`.reveal` + IntersectionObserver** (19 r CSS + 18 r JS, 78× toegepast) | 1,0 | 100% | 8 | **8,0** |
| 5 | **Header die wegduikt bij scroll** (21 r JS) | 0,5 | 100% | 4 | **8,0** |
| 6 | **Hero-collage** (2 foto's + 3 CSS-vormen, ~30 r) | 0,75 | 90% | 6 | **8,0** |
| 7 | **Accordeon** (progressive disclosure, eerste item open) | 1,0 | 100% | 5 | **5,0** |
| 8 | **Fluid type-scale uit één ontwerpframe** | 1,5 | 100% | 7 | **4,7** |
| 9 | **Pincode-gate** (293 r) | 2,5 | 100% | 9 | **3,6** |
| 10 | **Scroll-gedreven tijdlijnvulling** | 1,5 | 90% | 6 | **3,6** |
| 11 | **Cirkel-funnel met overshoot** (122 r CSS) | 1,5 | 60% | 5 | **2,0** |
| 12 | **Klantspecifieke feitendichtheid** (6 pijnkaarten, 27× voornamen, 5 concurrenten) | 6,0 | **0%** | 9 | **1,5** |
| 13 | **Custom SVG-verhaalgrafiek** (54 r inline SVG) | 3,5 | 20% | 7 | **1,4** |
| 14 | **Handtekening + client-side PDF** (338 r + 2 CDN-libs) | 9,0 | 80% | 4 | **0,4** |

**Wat de tabel je vertelt.**

1. De **top-6 kost samen ~4,25 uur** en levert het overgrote deel van het duur-gevoel. Nummer 11,
   13 en 14 kosten samen ~14 uur en leveren marginaal — of negatief (de grafiek ondermijnt het
   document zodra iemand kijkt waar het omslagpunt staat).
2. **Klantfeiten hebben de laagste ratio (1,5) en het hoogste plafond.** Zonder de vormlaag wordt
   het niet gelezen; zonder de feitenlaag wordt het gelezen en niet geloofd. Vorm koopt aandacht,
   feiten kopen geloofwaardigheid. Wie alleen op ratio optimaliseert bouwt een mooie lege huls.
3. Het font is de grootste hefboom die bestaat en tegelijk het **enige juridisch blokkerende**
   onderdeel — 'Youth' is een commerciële licentie, self-hosted vanaf `../assets/fonts/`, zonder
   licentiecomment. Dat kopieer je niet; je koopt of kiest je eigen.

---

## 3. Het designsysteem — plakbare tokenset in Agyle-kleuren

### 3.1 De vier formules waar alles uit volgt

| Wat | Formule | Waarom |
|---|---|---|
| **Type-clamp** | `vw = designwaarde_px ÷ (frame ÷ 100)` | Reproduceert de designwaarde exact op je ontwerpframe. Clark: `--pad-x: 5.29vw × 1512 = 80,0px` exact |
| **Type-max** | `max = designwaarde × (--max-w ÷ frame)` | Dan doet je max ook echt iets. **Clarks fout:** 7 van 8 maxima worden pas op 2100–2400px bereikt terwijl `--max-w: 1920px` |
| **Ruimte-clamp** | `max = 2 × min`, `vw = max ÷ (--max-w ÷ 100)` | Elke ruimtewaarde topt precies bij je `--max-w` af. Clark landt op 1800px (mediaan `max/vw` = 18,0) |
| **Mobiele min** | grote stappen ~0,55× designwaarde, kleine ~0,78× | Empirisch bij Clark: display 0,55× · h1 0,56× · h2 0,58× · h3 0,69× · body 0,70× · label 0,78× |

**Gekozen voor Agyle:** ontwerpframe **1440px**, `--max-w: 1600px`. Alle maxima worden dan bereikt
tussen 1580 en 1640px — precies waar de content stopt met groeien.

### 3.2 Het `:root{}`-blok — kopieer dit

```css
:root {
  /* ---------- KLEUR: 3 dragend + 1 functioneel. Nooit een nieuwe hex bijmaken. ---------- */
  --brand-black:  #000000;   /* alleen logo/merkvlak — het officiële Agyle-zwart */
  --ink:          #070C0E;   /* PAGINAZWART: sky-getint (R7 G12 B14). Zie 3.3 */
  --sky:          #97D4E8;   /* Agyle sky blue, Pantone 2975 C — accent + "goed" */
  --sky-ink:      #10596E;   /* sky, donker genoeg voor tekst op licht (7:1 op wit) */
  --paper:        #EDF6F9;   /* sky op 20% over wit — de rustkleur, Clarks --cream-equivalent */
  --off-white:    #F7FBFD;   /* kaartvlak op --paper */
  --on-dark:      #F2FBFE;   /* TEKST OP DONKER — géén #FFFFFF. Zie 3.3 */
  --card-dark:    #202527;   /* kaart op --ink: exact 25 punten lichter, zonder rand */
  --ok:           #35A96F;   /* enige functionele kleur: goed / gedaan / akkoord */

  /* Secundaire tekst = dezelfde kleur op alfa, nooit een eigen hex */
  --muted:        #5A6A70;   /* secundaire tekst op licht (5,4:1 op --paper) */
  --muted-light:  #B9C6CB;   /* secundaire tekst op donker */
  --muted-mid:    #8A979C;   /* tertiaire tekst, beide kanten */
  --line:         #D3E0E5;   /* hairline op licht */

  /* ---------- MAAT ---------- */
  --max-w: 1600px;
  --pad-x: clamp(24px, 5.55vw, 89px);      /* 80px @1440, topt af @1604 */
  --header-h: 80px;                         /* nooit hardcoden in calc(), altijd deze var */

  /* ---------- TYPE: frame 1440, coëfficiënt = design ÷ 14.4 ---------- */
  --t-display: clamp(48px, 6.11vw, 98px);   /* 88 @1440 */
  --t-h1:      clamp(36px, 4.44vw, 71px);   /* 64 */
  --t-h2:      clamp(28px, 3.33vw, 53px);   /* 48 */
  --t-h3:      clamp(22px, 2.22vw, 36px);   /* 32 */
  --t-h4:      clamp(16px, 1.67vw, 27px);   /* 24 */
  --t-body:    clamp(16px, 1.39vw, 22px);   /* 20 */
  --t-small:   clamp(12px, 1.04vw, 17px);   /* 15 */
  --t-label:   clamp(13px, 1.11vw, 18px);   /* 16, uppercase */

  /* ---------- RUIMTE: max = 2 × min, vw = max ÷ 16 ---------- */
  --sp-section: clamp(64px, 8vw, 128px);    /* 115 @1440 — de sectie-lucht */
  --sp-block:   clamp(32px, 4vw, 64px);     /* 58 */
  --sp-card:    clamp(16px, 1.66vw, 27px);  /* 24 — gap tussen kaarten */
  --sp-tight:   clamp(10px, 1.11vw, 18px);  /* 16 */

  /* ---------- VORM ---------- */
  --radius:     clamp(16px, 1.66vw, 27px);  /* ÉÉN kaartradius, vloeiend */
  --radius-pill: 32px;                       /* knoppen, vast */

  /* ---------- MOTION ---------- */
  --ease-out-expo:  cubic-bezier(0.19, 1, 0.22, 1);      /* reveals, sheets */
  --ease-overshoot: cubic-bezier(0.34, 1.56, 0.64, 1);   /* alleen vormen, nooit tekst */
  --d-micro:  0.2s;    --d-state: 0.3s;
  --d-panel:  0.38s;   --d-reveal: 0.7s;
}

@media (max-width: 768px) { :root { --pad-x: 24px; --header-h: 64px; } }
```

### 3.3 Toelichting per beslissing — waarom die waarde

| Token | Waarom |
|---|---|
| `--ink: #070C0E` i.p.v. `#000000` | Clark's merkzwart is `#0D0707` — R13 G7 B7, **rood-getint** naar hun merkkleur. Dat is waar "duur" vandaan komt; met puur `#000` haal je het nooit. Agyle's sky is cyaan (hue ~194°), dus B en G omhoog: R7 G12 B14. `#000000` blijft het officiële merkzwart voor logo en drukwerk — het paginazwart is een afgeleide. |
| `--on-dark: #F2FBFE` i.p.v. `#FFFFFF` | Clark gebruikt `--pink-light: #FFF2F2` op alle rode en zwarte vlakken. Zuiver wit op verzadigde kleur schreeuwt; gebroken wit fluistert. Kost 10 seconden per token en is het verschil tussen formulier en interface. |
| `--card-dark: #202527` | Clark: `--black #0D0707` → `--card-dark #262222`, exact **25 punten lichter per kanaal**, en er staat **geen rand** op `.vacancy-card`, `.pricing-card`, `.guarantee`. Genoeg om af te tekenen, niet genoeg om als kader te lezen. |
| `--sky-ink: #10596E` | `#97D4E8` op wit haalt ~1,9:1 contrast — onbruikbaar voor tekst. Sky is een **vlak- en accentkleur**, geen tekstkleur op licht. Dit is het punt waar Agyle van Clark afwijkt: `#DC0000` kán tekst zijn, `#97D4E8` niet. |
| `--paper: #EDF6F9` | Clark's `--cream #F0E4D8` is de "rustkleur" en draagt 3 van de 13 secties. Agyle-equivalent = sky op 20% over wit. Nooit als tekstachtergrond voor sky-tekst gebruiken. |
| `--ok: #35A96F` | Clark heeft precies **één** functionele kleur, `--green #4CC87D`, en gebruikt hem nergens anders voor: vinkjes, effort-pips, pincode-succes, garantie-rand. Die discipline is het punt, niet de tint. |
| Eén `--radius` | Clark heeft **12 verschillende radius-waarden** plus twee eigen schalen inline (`clamp(16px,1.4vw,22px)` naast systeemwaarde `clamp(16px,1.5vw,24px)`). Dat is drift. Eén vloeiende kaartradius + één pill-radius, meer niet. |
| `--header-h` | Clark hardcodeert `top: calc(80px + …)` op twee plekken (voorstel.css 268, 457) terwijl de header op ≤768px 64px is (r. 1742). 16px scheef. Custom property lost dat op. |

### 3.4 De alfa-ladder — 13 tokens die als 40 kleuren voelen

Er is **geen enkele extra hex** voor secundaire tekst op gekleurde vlakken. In plaats daarvan een
consequente trap. Neem deze exact over:

```css
/* tekst op donker/gekleurd — nooit een nieuwe hex */
--a-primary:   rgba(255,255,255,0.85);   /* hero-subtitel */
--a-intro:     rgba(255,255,255,0.80);   /* section-intro op donker */
--a-secondary: rgba(255,255,255,0.60);   /* eyebrow */
--a-label:     rgba(255,255,255,0.50);   /* eenheid, inactieve tab, section-label--light */
--a-quiet:     rgba(255,255,255,0.45);   /* gate-label */
--a-hairline:  rgba(255,255,255,0.08);   /* DE standaard-hairline op donker */
--a-hairline-strong: rgba(255,255,255,0.15);
--a-surface:   rgba(255,255,255,0.05);   /* nauwelijks-zichtbaar vlak */
```

**De accent-triade — één hex, drie oppervlakken.** Toepassen op élke chip, badge en callout:

```css
.chip {
  background: rgba(151, 212, 232, 0.12);   /* accent @ .08–.15 */
  border: 1px solid rgba(151, 212, 232, 0.25);   /* accent @ .2–.25 */
  color: var(--sky);                        /* op donker; op licht: var(--sky-ink) */
}
```

Clark dekt hiermee ~40 gevoelde kleuren met 13 tokens (`.vacancy-card__priority--high`,
`.roadmap-callout`, `.effort-pip`, alle hairlines).

### 3.5 Typografie-regels — de meest consistente laag bij Clark

```css
/* Line-height in drie registers, streng. Clark: 17× line-height 1.5 als body-standaard. */
h1,h2,.display { line-height: 1.1; }    /* koppen 1,05–1,2 */
p, li          { line-height: 1.5; }    /* lopende tekst 1,4–1,6 */
.amount        { line-height: 1.0; }    /* grote cijfers exact 1,0 */

/* Elke uppercase krijgt tracking, lopende tekst nooit. Clark: 22 uppercase-declaraties,
   22 keer tracking, geen enkele uitzondering. */
.label, .eyebrow { text-transform: uppercase; letter-spacing: 0.06em; }
.display         { letter-spacing: -0.01em; }   /* koppen >40px: lichte negatieve tracking */

/* Globaal, op de universele selector — Clark base.css 73-79 */
*, *::before, *::after {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Verplicht bij élk bedrag en élke count-up. Clark heeft dit 0× en het rafelt in
   .signature-summary-row — het scherm waar de klant tekent. */
.amount, .summary-row strong { font-variant-numeric: tabular-nums; }
```

**Gewichten:** declareer alleen gewichten die je écht bezit. Clark declareert `font-weight: 600`
8× en `800` 1× terwijl Youth alleen 300/400/500/700/900 levert → die snappen stil naar 700/900.
En `font-style: italic` staat 4× (voorstel.css 283, 524, html 653, 825) zonder italic-bestand →
faux italic, zichtbaar lelijk bij een licentiefont.

### 3.6 Meetregel — waar leesbaarheid vandaan komt

De container mag zo breed als je wil (`--max-w: 1600px`), maar **elk tekstblok krijgt zijn eigen
`max-width` van 640–820px**. Dat is de discipline, niet een smalle container.

| Component | Clark's waarde | Agyle |
|---|---|---|
| `.section-intro` | `clamp(400px, 55vw, 800px)` | idem |
| hero-subtitel | `clamp(320px, 50vw, 720px)` | idem |
| fase-subtitel | `640px` | idem |
| voetnoot / disclaimer | `780px` / `820px` | `800px` |

### 3.7 De premium-tells — 8 details die het verschil maken

1. **Nul `box-shadow` in het componentsysteem.** `grep -c box-shadow css/*.css` → **0**. Diepte komt
   uit full-bleed kleurvlakken + hairlines. Dit is het meest bepalende verschil met een
   Bootstrap-template. (Alle 10 schaduwen bij Clark zitten in de later opgeplakte modal en in de
   5 inline gestylede kaarten van één sectie — de sectie die als laatste is toegevoegd.)
2. **Vloeiende border-radius.** `clamp(16px, 1.66vw, 27px)`: 16px op mobiel, 27px op 1600. Vrijwel
   niemand doet dit; het voorkomt dat kaarten op groot scherm frutselig ogen.
3. **Stroke-register, streng gescheiden.** `1px` = data/scheiding · `2px` = structuur (headerrand,
   knoprand, kader) · `4px` = accent (`.vacancy-card--urgent::before`). Nooit iets anders.
4. **Hover = uitsluitend `opacity: .85`** op de knop. Clark heeft 7 hover-selectors op de hele
   pagina, waarvan er **twee levend en buiten de modal** zijn. Nul kaart-hovers. (Dit is óók een
   zwakte — zie §10.)
5. **Sticky-offsets uit het ritme, geen magic number.** `top: calc(var(--header-h) + var(--sp-block))`.
6. **Optische correcties die niemand ziet maar iedereen voelt:**
   - `margin-top: clamp(-140px, -9.5vw, -70px)` om een portret optisch te liften (voorstel.css 462)
   - `margin: -1px` op blokken met `border: 2px` zodat aangrenzende randen samenvallen tot één lijn
   - `margin-top: auto` op kaartlijsten zodat ze onderaan uitlijnen over ongelijke kaarthoogtes
   - één logo in een trust-row ~15% bumpen omdat het optisch lichter is
7. **Full-bleed sectie, begrensde inner.** Kleur loopt tot de schermrand, content nooit. Harde
   stuiknaden — geen dividers, golven of gradients. Dit is de belangrijkste enkele beslissing in
   het hele ontwerp.
8. **242px lucht tussen inhoudsblokken** (`padding: clamp(80px,8vw,160px) 0` = 115px boven én onder
   op 1440). Goedkoop drukwerk is vol, duur drukwerk is leeg.

---

## 4. De sectie-grammatica

### 4.1 De molecule — 8 van de 12 contentsecties volgen hem strikt

```html
<section class="sec sec--dark">
  <div class="sec__inner">
    <p  class="eyebrow eyebrow--light reveal">JULLIE SITUATIE</p>
    <h2 class="sec-title reveal">Kop die het probleem benoemt</h2>
    <p  class="sec-intro sec-intro--light reveal">Intro van 1–3 zinnen, max 800px breed.</p>
    <!-- content -->
  </div>
</section>
```

```css
.sec        { padding: var(--sp-section) 0; }
.sec--dark  { background: var(--ink);      color: var(--on-dark); }
.sec--sky   { background: var(--sky);      color: var(--ink); }      /* sky = vlak, tekst zwart */
.sec--paper { background: var(--paper);    color: var(--ink); }
.sec--white { background: var(--off-white);color: var(--ink); }
.sec__inner { max-width: var(--max-w); margin: 0 auto; padding: 0 var(--pad-x); }

.eyebrow   { font-weight: 500; font-size: var(--t-label); text-transform: uppercase;
             letter-spacing: .06em; margin-bottom: clamp(12px, 1vw, 20px); }
.sec-title { font-weight: 700; font-size: clamp(36px, 4.5vw, 72px); line-height: 1.1;
             margin-bottom: clamp(32px, 3vw, 64px); }
.sec-intro { font-weight: 400; font-size: clamp(16px, 1.3vw, 26px); line-height: 1.5;
             max-width: clamp(400px, 55vw, 800px); margin-bottom: clamp(40px, 4vw, 80px); }

.eyebrow--light   { color: rgba(255,255,255,.5); }
.eyebrow--muted   { color: var(--muted); }
.sec-intro--light { color: rgba(255,255,255,.8); }
.sec-intro--muted { color: var(--muted); }
```

> **Zet `color` op de sectievariant, niet op de kop.** Clark heeft 6× `style="color: var(--pink-light)"`
> op `.section-title` staan (r. 312, 348, 425, 488, 662, 869) — allemaal **no-ops**, want de
> sectievarianten zetten de kleur al en de `<h2>` erft. Restanten, geen reparaties.

### 4.2 Sectie-inventaris als checklist

De volgorde van Clark, met de functie in het betoog en de kleurpartituur. Vink af bij elk voorstel.

| # | Eyebrow | Functie in het betoog | Kleur | Scroll-diepte |
|---|---|---|---|---|
| 0 | *Vertrouwelijk document* | Toegangsritueel — gate, `body{overflow:hidden}` | merkvlak | pre-scroll |
| 1 | *Plan van aanpak* | **Hero.** Kop = resultaat van de klant + klantnaam. Subtitle bevat hun eigen groeicijfer | merkvlak, `100svh` | 0–7% |
| 2 | *Jullie situatie* | **Probleem + agitatie.** 5–7 pijnkaarten, laatste is een compliment | licht | 7–17% |
| 3 | *Prioriteiten* | **Scope-inperking = geloofwaardigheid.** Wat je wél en niet doet | donker | 17–23% |
| 4 | *Onze aanpak* | **Oplossing.** Twee sporen, met sticky visual rechts | merkvlak | 23–31% |
| 5 | *Onze werkwijze* | Methodologie. ⚠ Clark vult dit met een piramide van 6 woorden — zie §10 | merkvlak | 31–36% |
| 6 | *In de praktijk* | **Mechanisme.** Hoe het concreet werkt | donker | 36–42% |
| 7 | *Het platform* | Product. Accordeon, **eerste item vooraf open** | eigen sub-brandkleur | 42–48% |
| 8 | *Fasering & tijdlijn* | **Risicoreductie via plan.** Hoogste sectie van de pagina | licht | 48–63% |
| 9 | *Kosten* | **Prijs + anker.** Kop kiest zelf de vergelijkingsnoemer | donker | 63–71% |
| 10 | *De lange termijn* | **Waarde-over-tijd + exit-belofte.** Hier hoort de grafiek | licht | 71–81% |
| 11 | *Rolverdeling* | **Commitment & consistentie.** Kaart per persoon, bij voornaam | off-white | 81–86% |
| 12 | *Tijdsinvestering [klant]* | **Bezwaar-preëmptie op capaciteit.** "Maximaal 2 uur per week" | donker | 86–95% |
| 13 | — | **Sluiting via omkering.** Eén CTA | merkvlak | 95–99% |

**Kleur als partituur (Clarks vondst, letterlijk):** elke keer dat de pagina **geld of inspanning
vraagt** (vacatures, campagne, kosten, tijdsinvestering) staat de sectie op `--black`; elke keer
dat ze **rust of eigendom belooft** (situatie, tijdlijn, onafhankelijkheid, rolverdeling) op
`--cream`/`--off-white`. Merkkleur alleen bij hero, aanpak en CTA.

**Harde regel die Clark zelf breekt:** nooit twee identieke achtergronden achter elkaar. Aanpak
(r. 345) en Bouwstenen (r. 422) staan beide op `#DC0000` met elk `padding: clamp(80px,8vw,160px) 0`
→ 230px leeg rood tussen twee secties, zonder naad. Loop de volgorde na vóór publicatie.

### 4.3 Het narratieve model — 8 regels die je overneemt

1. **Zet het argumentatieskelet in de eyebrows.** "Jullie situatie" → "Prioriteiten" → "Onze
   aanpak" → "Kosten" → "De lange termijn" → "Tijdsinvestering [klant]". De lezer voelt dat hij
   een redenering volgt in plaats van een verkooppraatje te lezen. Dit is letterlijk een
   zichtbaar gemaakt SPIN-skelet — precies Abduls eigen methode.
2. **De pijnmuur eindigt op een compliment.** Vijf kaarten die tekortdoen, en dan als zesde:
   > *"Het fundament staat al sterker dan het lijkt — [drie verifieerbare sterktes]. Wat ontbreekt
   > is de wervingsmachine die dat fundament op kan schalen zonder dat het PZ-team aan capaciteit
   > hoeft in te leveren."*

   Dit is de scharnierzin van de hele pagina: de diagnose wordt omgedraaid, en **de koper hoeft
   geen falen toe te geven om te kopen.** Eindig een probleemsectie nooit op een probleem.
3. **De vijand is nooit de klant, altijd hun leveranciers.** Aanvallen gaan naar de incumbent-tool
   ("twee plaatsingen in drie jaar"), losse bureaus, en vijf concurrenten bij naam. Het eigen
   proces van de klant wordt expliciet gespaard: *"De mailbox blijft heilig, maar krijgt er een
   datalaag bovenop"* · *"Het bord op kantoor mag blijven, maar krijgt zijn digitale tegenhanger."*
   Dát koopt het recht om alles eromheen te vervangen, zonder defensiviteit bij de lezer.
4. **Spiegel minimaal 10× het vakjargon van de kóper** en pik minstens één idioom letterlijk uit
   het gespreksverslag. Clark: *BBL, E tot W, CAO Techniek vs. industriële CAO, werkvoorbereider,
   "van bus tot gereedschap", "ladders liggen daar wat lager".* Die laatste is het beste zinnetje
   van het hele voorstel en hij is gratis. **Jargon-spiegeling is het goedkoopste bewijs-van-
   geluisterd dat bestaat** en compenseert deels de ontbrekende cases.
5. **Quotum voor de inhoudslaag:** elke kaart of blok bevat minimaal één getal, jaartal, eigennaam
   of bedrag dat de klant zelf heeft genoemd. Clarks referentieniveau: *"staat al bijna 4 jaar
   open"*, *"twee plaatsingen in drie jaar"*, *"25 nieuwe collega's vorig jaar via eigen kanalen"*,
   *"de €11.000 tot €13.000 die jullie per jaar betalen"*, vijf concurrenten bij naam.
6. **Schrijf de medewerkers van de klant bij voornaam een toekomstige rol toe.** Clark noemt
   Mariel / Marit / Sabine elk 9×, plus een stakeholderkaart per persoon. Ze staan in het plan
   geschreven vóórdat er getekend is.
7. **Verkoop de exit als het product.** Voordoen → meedoen → zelfdoen, met een expliciete
   restwaarde-fase erachter, en sluit af met een omkering in plaats van een push:
   *"Het doel is altijd hetzelfde. Dat jullie ons op een gegeven moment niet meer nodig hebben."*
   Dat is de enige zin in het document die tegen het eigen belang ingaat, en daarom de enige die
   volledig geloofd wordt.
8. **Schaarste bewust weglaten.** Geen deadline, geen "geldig tot", geen aftelklok. De enige
   urgentie is die van de klant zelf. Regel: **als je exit verkoopt, mag je geen druk zetten.**

**Toon en ritme, meetbaar:** consequent "jullie" (nooit "u", nooit "je"), gemiddelde zinslengte
12–14 woorden, hoge dichtheid werkwoordloze fragmenten als ritmische klap (*"De stroom die nooit
stopt."* · *"Aan en uit per knop, per rol, per regio."*), en elk Engels leenwoord krijgt in
dezelfde zin een Nederlandse verankering. Koppen altijd Nederlands.

> **Registerbreuk-waarschuwing.** Clark breekt zijn eigen "jullie"-regel uitgerekend in de
> kostensectie: *"Voor dit traject **krijg je** een volledig recruitment team…"* (r. 663) — en
> daarna in de hele ondertekenmodal. Loop je copy één keer na op `\bje\b` en `\bu\b` vóór levering.

---

## 5. Motion-recept

### 5.1 De reveal — één primitief, overal toegepast

Clark past 9 regels CSS 78× toe. Neem dat over, met **één verbetering**: de easing.

```css
.reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity var(--d-reveal) var(--ease-out-expo),
              transform var(--d-reveal) var(--ease-out-expo);
}
.reveal.is-visible { opacity: 1; transform: none; }

@media (max-width: 768px) {
  .reveal { transform: translateY(30px); transition-duration: 0.6s; }
}
```

```js
const io = new IntersectionObserver((entries, obs) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('is-visible');
    obs.unobserve(e.target);          // eenrichtingsverkeer
  });
}, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => io.observe(el));
```

**Waarom precies deze vier parameters chic zijn i.p.v. goedkoop:**

| Parameter | Waarde | Waarom |
|---|---|---|
| Afstand | **40px**, niet 100 | Grote translate-afstanden lezen als PowerPoint-overgang. 40px lees je als "het stond er al bijna" |
| Duur | **0,7s**, niet 0,3 | Onder ~0,5s voelt het als een hik; boven ~1s wacht je erop |
| Herhaling | **`unobserve` na één keer** | Terugscrollen animeert níets opnieuw. Herhaling is het snelste pad naar "goedkope website" |
| `rootMargin` | **`-40px` onderaan** | Elementen mogen 40px de viewport in voordat ze triggeren — je ziet de animatie *starten*, niet halverwege inhaken |

**De easing is Clarks grootste gemiste kans.** `cubic-bezier(0.19, 1, 0.22, 1)` is easeOutExpo:
het eerste controlepunt heeft y=1.0 bij x=0.19, dus ~80% van de afstand in de eerste ~25% van de
duur, met een lange vlakke staart. Duur, zwaar, cinematografisch — dezelfde curve die Apple voor
sheets gebruikt. Clark gebruikt hem **precies één keer**, op de signature-modal (html r. 45), en
laat de 78 reveals die iedereen ziet op de browser-default `ease` draaien. Investeer je enige
goede easing in wat iedereen ziet.

### 5.2 Stagger via de container, niet via de kinderen

Clarks `.reveal-stagger > .reveal:nth-child(1..8)` (base.css 147-154) heeft drie zwaktes: harde cap
bij 8 kinderen, `nth-child` telt niet-revealende siblings mee, en — de echte — **de trigger zit óók
per kind**, dus bij verticale lijsten (`.situatie-split__cards` met 6 kaarten, `.roadmap` met 4
rijen) kruist elk kind de drempel honderden pixels na het vorige en is de delay betekenisloos.
Alleen de horizontale grids tonen een echte cascade; op mobiel valt die overal weg.

```css
.reveal-group > * {
  opacity: 0; transform: translateY(40px);
  transition: opacity var(--d-reveal) var(--ease-out-expo),
              transform var(--d-reveal) var(--ease-out-expo);
  transition-delay: calc(var(--i, 0) * 70ms);   /* onbegrensd, geen nth-child */
}
.reveal-group.is-visible > * { opacity: 1; transform: none; }
```

```js
document.querySelectorAll('.reveal-group').forEach(g => {
  [...g.children].forEach((c, i) => c.style.setProperty('--i', i));
  io.observe(g);                                 // ← de CONTAINER, niet de kinderen
});
```

Dit repareert alle drie de zwaktes tegelijk.

### 5.3 Scheid het in-viewport-**signaal** van het in-viewport-**effect**

De slimste truc in het hele Clark-bestand (voorstel.css 1641-1648), en het beste steelbare patroon
van de site:

```css
/* het reveal-EFFECT annuleren, de reveal-KLASSE als vlag behouden */
.choreo.reveal { opacity: 1; transform: none; }

/* gepauzeerde keyframes die de observer straks unpauzeert */
.choreo__item {
  opacity: 0; transform: scale(0);
  animation: popIn .6s var(--ease-overshoot) forwards;
  animation-play-state: paused;
}
.choreo.is-visible .choreo__item { animation-play-state: running; }

.choreo__item:nth-child(1) { animation-delay: 0s;    }
.choreo__item:nth-child(2) { animation-delay: .15s;  }
.choreo__item:nth-child(3) { animation-delay: .30s;  }
/* bijschriften lopen 0,3s achter de vormen aan via transition-delay */

@keyframes popIn { from { opacity:0; transform:scale(0); } to { opacity:1; transform:scale(1); } }
```

Eén observer, willekeurig veel choreografieën, nul extra JS. De timing blijft in CSS; JS zet alleen
een klasse.

### 5.4 De easing- en timing-ladder

| Curve | Waarde | Waarvoor | Waarom |
|---|---|---|---|
| easeOutExpo | `cubic-bezier(0.19, 1, 0.22, 1)` | reveals, modals, sheets | ~80% van de beweging in de eerste ~25% van de tijd, lange staart = duur/cinematografisch |
| overshoot | `cubic-bezier(0.34, 1.56, 0.64, 1)` | **alleen objecten met een eigen vorm** (cirkels, badges) | y=1.56 → schaalt rond t≈0.62 tot ~1.09 en veert terug. **Nooit op tekst** — daar leest overshoot als renderfout |
| linear | `linear` | spinners | een spinner met easing hikt |

| Duur | Waarvoor |
|---|---|
| **0,2s** | micro-interactie (modal-knoppen, inputs) |
| **0,3s** | state-flip (icoon, kleur, chip) |
| **0,35–0,4s** | paneel, accordeon, header |
| **0,6–0,7s** | scroll-reveal |
| **~1,5s** | precies één lange choreografie, op de belangrijkste sectie |
| **~1,0s** | de toegangsceremonie (zie §7.1) |

Wijk hier niet van af. Vier duurwaarden voor interactie is een leerbare ladder; Clark houdt zich
er consequent aan, en dat is een deel van waarom het "af" oogt.

### 5.5 Wat je wél en niet animeert

**Wel:** `opacity` en `transform`. Punt.

**Niet:** `height`, `max-height`, `top`, `width` — zeker niet in een rAF-loop. Clarks slechtste code
is `updateFill()` (voorstel.js 115-124): een oneindige `requestAnimationFrame`-lus die elke frame
`getBoundingClientRect()` doet (forced synchronous layout), `.closest('.timeline')` opnieuw
traverseert, en `fill.style.height` zet — een layout-property. Nooit gecancelled, geen
`document.hidden`-check, draait ook als de timeline acht schermen boven je staat.

| In plaats van | Doe dit |
|---|---|
| `max-height: 0 → scrollHeight` voor accordeons | `grid-template-rows: 0fr → 1fr` — geen JS-meting die na font-swap en na resize niet meer klopt |
| rAF-lus die `height` zet voor scroll-progress | `transform: scaleY()`, of `animation-timeline: scroll()` met nul JS |
| Kaart-hovers op mobiel | niets; hover bestaat daar niet |

**Ambient motion: houd er precies één op de hele pagina.** Bij Clark is dat een pijltje dat 6px op
en neer gaat (`scroll-bounce 2s ease-in-out infinite`). Alle andere beweging heeft een trigger.
Die schaarste is de reden dat het duur oogt — geen parallax, geen marquee, geen cursor-effecten.
En de scroll-hint is onmisbaar: de hero is `100svh`, dus er is geen andere hint dat er iets onder zit.

### 5.6 De twee blokken die Clark volledig vergeet

```css
/* 1 — reduced motion. NIET met de universele-selector-sledgehammer, want die sloopt de
   animation-play-state-truc uit 5.3. Target de klassen. */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .reveal, .reveal-group > * {
    opacity: 1 !important; transform: none !important; transition: none !important;
  }
  .choreo__item {
    animation: none !important; opacity: 1 !important; transform: none !important;
  }
  .ambient { animation: none !important; }
}
```

```html
<!-- 2 — nooit een pagina die zonder JS op opacity:0 staat -->
<html lang="nl" class="no-js">
<script>document.documentElement.classList.replace('no-js','js')</script>
```
```css
.no-js .reveal, .no-js .reveal-group > * { opacity: 1; transform: none; }
```

En wikkel élke init-functie in `try/catch`. Bij Clark staat `initReveals()` als eerste in de
`DOMContentLoaded`-keten zonder guard: één exception en de hele pagina blijft op `opacity: 0`.
Er zijn twee onafhankelijke single-points-of-failure — valt `pincode.js` weg, dan blijft de gate
(`position:fixed; inset:0; z-index:10000`, standaard zichtbaar) er permanent overheen staan.

### 5.7 Het diavoorstelling-gevoel — zonder scroll-snap, zonder library

`scroll-snap` komt **0×** voor in de hele Clark-codebase. Het gevoel komt uit vijf simpele dingen:

1. **Full-bleed kleurbanden** uit een palet van 4–5, die per sectie wisselen — 13 kleurwissels over
   de pagina. De kleur *ís* de sectiescheiding.
2. **`padding: var(--sp-section) 0`** zodat er nooit twee banden tegelijk in beeld staan.
3. **`min-height: 100svh`** op de hero, met `min-height: 100vh` als fallback erboven — dat
   elimineert de sprong door de mobiele URL-balk. Clark doet dit correct (voorstel.css 63-64).
4. **Header die wegduikt.** `scrollY > 200 && scrollY > lastY` → `translateY(-100%)`, met
   `transition: transform 0.35s ease`. Zodra de chrome weg is leest het brein "presentatie", niet
   "website". Verbeter Clark met `{ passive: true }` op de listener en een delta-drempel van 8px
   tegen jitter bij rubber-band-scroll, en gebruik een klasse in plaats van een inline style.
5. **Eén sticky kolom per split-sectie.** `position: sticky; top: calc(var(--header-h) + var(--sp-block))`.
   Twee CSS-regels, en het is het enige effect dat de lezer niet kan verklaren zonder aan het
   medium te denken — dus het sterkste signaal dat het medium bewust gekozen is in plaats van
   overgenomen van een PDF.

---

## 6. Dataviz-recept

### 6.1 De vier voorwaarden — alle vier, of geen grafiek

Clark schendt drie van de vier. Bij twijfel: **vervang de grafiek door drie getallen op een rij**
(`clamp(40px, 4.5vw, 96px)`, weight 900) met één zin eronder. Dat is eerlijker en leest sneller.

| Voorwaarde | Clarks overtreding |
|---|---|
| **Zelfde font als de pagina** | Alle drie de tekstgroepen dragen `font-family="'IBM Plex Sans', Helvetica, Arial"` (html r. 765, 770, 775) terwijl de hele pagina Youth is en Plex nergens wordt geladen. Het paradepaardje is het enige object in een vreemd lettertype |
| **Assen met eenheden** | Er is **geen y-as**: geen tick, geen label, geen eenheid. Alleen een baseline en 3 verticale stippellijnen die fasegrenzen coderen, geen waarden |
| **Eén grootheid per as** | Euro's ("Kosten") staan tegen een niet-gedefinieerde grootheid ("Automatisering & output") op dezelfde naamloze y-as. *"Output > kosten"* is daarmee een betekenisloze uitspraak |
| **Marker klopt met bijschrift** | Het "OMSLAGPUNT" staat op `cx="488"` — binnen de MEEDOEN-band (x 260–500, ~maand 7), terwijl de tekst eronder "vanaf maand 10" zegt. *(NB: 04 claimde dat de marker naast de curves ligt; 07 weerlegt dat — de afwijking is ~5 viewBox-eenheden en visueel gedekt. De fasefout is echt.)* |

Plus: de x-as is geen lineaire tijdas (60 · 60 · 73 · ∞ px/maand), maand 7 wordt dubbel geteld
(3+4+3=10 verkocht als 9), en de disclaimer *"De grafiek is illustratief"* staat 800–1000px
ónder de grafiek in 14px cursief, terwijl de grafiek in een witte kaart met slagschaduw staat.
Aandachtsverhouding ruwweg 100:1.

**Agyle-regels, hard:**
- één eenheid per as; y-as vanaf nul of expliciet gebroken
- lineaire x-as, of een expliciet gelabelde bandbreuk
- alle kosten in de grafiek — inclusief advertentiebudget, eigen uren en btw
- altijd een **status-quo-baseline uit de eigen data van de klant**
- disclaimer **boven of náást** de conclusie, in dezelfde kaart, niet 900px eronder
- één regel bronvermelding onder de figuur

### 6.2 Het SVG-skelet — handgebouwd, geen library

```html
<svg viewBox="0 0 1000 460" preserveAspectRatio="xMidYMid meet" role="img"
     style="width:100%; height:auto; display:block; overflow:visible">
  <title>Cumulatieve kosten per aanwerving, status quo versus voorstel</title>
  <desc>Bron: eigen registratie klant 2024–2025, aannames onder de figuur.</desc>
  <!-- z-order = documentvolgorde -->
</svg>
```

| Laag | Volgorde | Spec |
|---|---|---|
| 1 | achtergrondbanden | `<rect y="60" height="320">`, alpha-ramp in merkkleur: `.08 → .05 → .02 → rgba(0,0,0,.02)` |
| 2 | fasegrenzen | verticale `stroke-dasharray="4 5"`, `stroke-opacity="0.12"` |
| 3 | baseline | `<line x1="80" y1="380" x2="920" y2="380" stroke-opacity="0.18" stroke-width="1">` |
| 4 | area-fills | kopieer de `d` van de stroke, plak `L 920,380 L 80,380 Z` erachter, vul op **4–7% alpha** |
| 5 | strokes | `stroke-width="3.5"`, `stroke-linecap="round"`, `stroke-linejoin="round"` |
| 6 | annotatie | zie 6.3 |
| 7 | tekstgroepen | zie 6.4 |

Plotgebied: **x 80 → 920**, **y 60 (top) → 380 (baseline)**. Fontgroottes 11–14 in viewBox-eenheden
landen bij ~1200px render op ~13–17 CSS-px.

**De alpha-ramp op de achtergrond is het slimste onderdeel van de hele Clark-grafiek en volstrekt
eerlijk:** een dalende dekking in de merkkleur leest als "onze aanwezigheid dooft uit", en de vierde
band wisselt naar neutraal = "hier zijn wij weg". De achtergrond draagt het narratief, de lijnen
leveren alleen het bewijs. Nul extra inkt.

### 6.3 Geannoteerd punt

```html
<circle cx="488" cy="227" r="22" fill="#fff" stroke="var(--sky-ink)" stroke-width="2" stroke-opacity="0.35"/>
<circle cx="488" cy="227" r="9"  fill="var(--sky-ink)"/>
<line x1="488" y1="227" x2="488" y2="135" stroke="var(--sky-ink)" stroke-opacity="0.35"
      stroke-width="1" stroke-dasharray="3 4"/>
<text x="488" y="115" text-anchor="middle" font-size="14" font-weight="700"
      letter-spacing="0.04em">OMSLAGPUNT</text>
<text x="488" y="130" text-anchor="middle" font-size="12" opacity="0.85">Kosten per hire onder de huidige</text>
```

Halo:kern-verhouding **2,4 : 1** (r=22 / r=9). De witte halo-fill dekt de curves eronder af zodat de
ring schoon leest. De leader eindigt 5px onder de baseline van de onderste labelregel.
**Gebruik `var(--…)` en niet hardcoded hexes** — Clark hardcodeert `#0F0F0F` in de grafiek terwijl
het merkzwart `#0D0707` is, een derde off-palette bijna-zwart, en de omringende HTML in dezelfde
sectie wél `var(--red)` gebruikt.

### 6.4 De drieregelige x-as-stack

Verticale ritme vanaf de baseline (y=380): **+28 / +47 / +63**.

| Regel | Stijl | Inhoud |
|---|---|---|
| y=408 | 13px / 700 / `letter-spacing="0.08em"` / caps | **VOORDOEN** |
| y=427 | 11px / `rgba(0,0,0,0.55)` | Maand 1 t/m 3 |
| y=443 | 11px / `rgba(0,0,0,0.55)` | *Clark draait alles* |

Die derde regel — **wat het betekent in mensentaal** — is wat deze as beter maakt dan 99% van de
business-grafieken: hij vertaalt de tijdas naar rolverdeling. Goedkoopste kwaliteitswinst in het
hele recept.

### 6.5 Dubbele legenda, gelijk benoemd

HTML-swatchrij **bóven** de SVG voor mobiele leesbaarheid, plus end-of-line `<text>`-labels **ín**
de SVG voor desktop. Clark doet dit correct maar noemt dezelfde serie in de twee legenda's anders
("Automatisering & output" vs "Output ↗"). Gebruik identieke namen.

```html
<span style="display:inline-block;width:28px;height:4px;background:var(--sky-ink);border-radius:2px"></span>
<span style="font-weight:700;font-size:clamp(13px,0.95vw,16px);text-transform:uppercase;
             letter-spacing:0.06em">Kosten per aanwerving</span>
```

28×4px staafje met `border-radius: 2px` — rustiger dan een vierkantje of een lijn met een puntje.

### 6.6 Geldtypografie — vier contrasten op één regel

```css
.amount        { font-weight: 900; font-size: clamp(32px, 3.2vw, 64px); line-height: 1.1;
                 letter-spacing: -0.01em; color: var(--on-dark);
                 font-variant-numeric: tabular-nums; }
.amount span   { font-weight: 400; font-size: clamp(14px, 1.2vw, 22px);
                 color: rgba(255,255,255,0.5); }
.amount-kicker { font-weight: 600; font-size: clamp(11px, 0.85vw, 14px);
                 letter-spacing: 0.12em; text-transform: uppercase; opacity: 0.85; }
```

Vier contrasten tegelijk: **gewicht** 500 eenheden · **grootte** 2,9× · **dekking** 2× · **donkere
kaart in een donkere sectie**, waardoor het roomwitte cijfer het enige lichtpunt is.

**Hetzelfde bedrag, twee registers.** Groot/900/licht in de verkoopsectie; halve grootte/700/zwart
in de geruststellingssectie. Zelfde getal, tegengestelde emotie, nul extra copy. Clark doet dit met
€5.500: `clamp(32,3.2vw,64px)` weight 900 op de prijskaart (r. 681) tegenover
`clamp(22,1.8vw,32px)` weight 700 zwart-op-cream in de lange-termijnkaarten (r. 800/806/812).

> **Agyle-uitzondering.** Bij Clark wordt deze truc ook gebruikt om de recurrentie te verbergen —
> "5.500" op 64px/900, "p.m." op 22px/400 bij 50% opacity. Zie §8.2: bij Agyle staat de eenheid in
> dezelfde grootte als het getal.

### 6.7 Count-up en micro-meter

```js
const target = parseInt(el.dataset.count, 10);
const eased  = 1 - Math.pow(1 - progress, 3);            // easeOutCubic, duration 1200ms
el.textContent = (el.dataset.prefix||'') +
                 Math.round(eased*target).toLocaleString('nl-NL') +
                 (el.dataset.suffix||'');
// IntersectionObserver { threshold: 0.5 }, unobserve direct na trigger
```

**Harde voorwaarde:** `font-variant-numeric: tabular-nums` plus een gereserveerde breedte in `ch`,
anders springt de layout per frame. Clark heeft de hele machinerie klaarliggen (`initCountUp`,
33 regels) en gebruikt hem 0× — `data-count` komt 0× voor in de HTML.

**Ordinale micro-meter zonder chart:** 4 pips van `clamp(8px, 0.7vw, 12px)`, `border-radius: 3px`,
gap 4–5px, gevuld = `--ok`, leeg = `rgba(255,255,255,0.12)`, met een legendarij die alle vier de
niveaus benoemt. **Harde voorwaarde: één semantische dimensie per schaal.** Clark meet posities 1–3
als werklast (Minimaal → Beperkt → Gemiddeld) en positie 4 als autonomie ("Zelfstandig"), onder de
kop "Tijdsinvestering Harwig" — waardoor ■■■■ leest als maximale belasting terwijl het bedoeld is
als "jullie doen het nu zelf". De boodschap keert om op het moment dat hij het meest telt.

---

## 7. De wow-mechaniek — met oordeel per truc

| Truc | Oordeel |
|---|---|
| Pincode-gate als frame-setter | **Doen** — maar zet er échte bescherming onder |
| Gate-achtergrond = hero-achtergrond | **Doen** — nul kosten, groot verschil |
| Ceremonie-pauze van 500ms vóór de fade | **Doen** — dat pauze-moment *ís* het effect |
| Kunstmatige spinner vóór PDF-generatie | **Doen** — 400–600ms, vertrouwens-theater dat werkt |
| Ondertekenen ín de pagina (canvas + 3 velden) | **Doen** — nul klikken tussen ja-zeggen en ja-doen |
| Voorgedrukte tegenhandtekening | **Anders doen** — beide partijen tekenen echt, of geen van beide |
| Canvas-setup | **Anders doen** — Clark levert een wazige, uitgerekte handtekening |
| Succesbeeld tonen | **Anders doen** — pas ná serverbevestiging |
| Client-side pincode als "vertrouwelijk" | **Anders doen** — `.htpasswd` of signed token eronder |
| jsPDF als tweede document in Helvetica | **Laten** — print-stylesheet of Playwright `page.pdf()` |
| Render-blocking CDN's zonder SRI | **Laten** — lazy-load bij modal-opening, mét SRI |

### 7.1 De gate — 293 regels, hoogste waargenomen-waarde-per-regel

**Wat het doet.** Vóór er één woord inhoud is gelezen staat het frame: *dit document is het
beschermen waard, ik ben één van de weinigen die het mag zien, hier zit geld achter.* Reciprociteit
+ schaarste + commitment in één scherm. Een PDF-bijlage heeft dat frame nul.

**Het bouwrecept, exact:**

```css
.gate { position: fixed; inset: 0; z-index: 10000; background: var(--ink);
        display: flex; align-items: center; justify-content: center;
        transition: opacity .5s ease, visibility .5s ease; }
.gate.is-hidden { opacity: 0; visibility: hidden; pointer-events: none; }

.gate__logo  { height: clamp(48px, 5vw, 72px); margin-bottom: clamp(48px, 6vw, 96px); }
.gate__label { font-size: clamp(12px, 1vw, 18px); text-transform: uppercase;
               letter-spacing: .08em; color: rgba(255,255,255,.45); }
.gate__title { font-size: clamp(24px, 2.8vw, 44px); font-weight: 700; color: var(--on-dark); }

.gate__digit { width: clamp(56px, 6vw, 80px); height: clamp(64px, 7vw, 96px);  /* hóger dan breed */
               border: 2px solid rgba(255,255,255,.25); border-radius: clamp(12px, 1.2vw, 18px);
               background: rgba(255,255,255,.08); color: var(--on-dark);
               font-weight: 700; font-size: clamp(28px, 3vw, 44px); text-align: center;
               caret-color: transparent;                       /* ← de sleutel-microbeslissing */
               transition: border-color .3s ease, background .3s ease; }
.gate__digit.is-filled { border-color: rgba(255,255,255,.5); }

@keyframes pinShake {                    /* DEMPEND, niet symmetrisch */
  0%,100% { transform: translateX(0);  }
  20% { transform: translateX(-12px); }  40% { transform: translateX(10px); }
  60% { transform: translateX(-8px);  }  80% { transform: translateX(6px);  }
}
.gate__inputs.is-error   { animation: pinShake .45s ease; }
.gate__inputs.is-success .gate__digit { border-color: var(--ok);
                                        background: rgba(53,169,111,.15);
                                        animation: pinSuccess .35s ease; }
@keyframes pinSuccess { 0%{transform:scale(1)} 50%{transform:scale(1.08)} 100%{transform:scale(1)} }
```

```js
// de choreografie na de juiste code — 1,0s visueel, 1,1s tot uit de DOM
inputsWrap.classList.add('is-success');
setTimeout(function () {
  gate.classList.add('is-hidden');            // CSS-fade 0,5s
  document.body.style.overflow = '';
  setUnlocked();                              // sessionStorage, per pad
  setTimeout(function () { gate.remove(); }, 600);   // loopt PARALLEL aan de fade
}, 500);
```

**De vijf microbeslissingen die het optillen:**

1. **`caret-color: transparent`.** Met een knipperende cursor is dit een formulierveld; zonder is het
   een slot. Eén CSS-regel.
2. **Vier losse inputs i.p.v. één met `maxlength=4`.** Functioneel identiek, ervaringsmatig een
   andere wereld. Het patroon komt uit 2FA-flows van banken en Apple; het leent hun autoriteit gratis.
3. **De 500ms pauze tussen groen-worden en opengaan.** Zonder die `setTimeout` is het een formulier
   dat submit; mét is het een kluis die ontgrendelt en dan pas opengaat.
4. **Dempende shake** (−12 / +10 / −8 / +6), geen symmetrische wiebel.
5. **Gate-achtergrond = hero-achtergrond.** Bij Clark zijn `.pincode-gate` (pincode.css 9) en
   `.voorstel-hero` (voorstel.css 67) allebei `var(--red)`. De deur lost op ín het eerste scherm;
   het voelt als een masker dat afvalt, niet als scherm A → scherm B.

**UX-details die je meeneemt:** auto-advance bij invoer, Backspace springt terug en wist, pijltjes
navigeren, `focus` doet `this.select()`, **paste vult alle vier de vakjes in één keer en submit**
(dat detail vergeten de meeste implementaties), `type="tel"` + `inputmode="numeric"` voor het
numerieke toetsenbord, `sessionStorage` met een pad-specifieke sleutel in `try/catch` voor private
browsing, `body.style.overflow='hidden'` zolang de gate staat.

**Wat je ANDERS doet:**

| Clark | Agyle |
|---|---|
| `data-pin="2605"` als attribuut op de `<script>`-tag die hem valideert (r. 1077), fallback `'2026'` | Server-side gate: `.htpasswd` op de map of een signed token in de URL. Behoud de vórm 100%, zet er echte bescherming onder |
| Gate is een DOM-overlay bovenop volledig geladen content — `curl` levert alles | Content wordt pas geserveerd ná authenticatie |
| "Vertrouwelijk document" op een pagina die publiek is met de URL | Claim geen vertrouwelijkheid die je niet levert |
| Globale Escape-handler heft de scroll-lock van de gate op (html 1117-1121 vs pincode.js 38) | Eén eigenaar per globale style-property |
| Geen `role="dialog"`, geen focus-trap — je kunt eruit tabben naar de onzichtbare pagina | `role="dialog"` + `aria-modal` + focus-trap |

**Praktisch:** leg in de begeleidende mail de code uit **én zeg erbij dat hij deelbaar is**. Anders
is de gate een frictiepunt zodra de directie het wil doorsturen (`sessionStorage` is per browser
per tab).

### 7.2 De handtekening-flow

**Wat je bouwt:** lezen → "Accorderen" → modal met 3 verplichte velden + `signature_pad`-canvas +
akkoordvinkje → spinner → jsPDF → download, zonder de browser te verlaten.

**De vier correcties op Clark, in volgorde van belang:**

```js
// 1 — canvas met devicePixelRatio. Clark: canvas.height = 150 terwijl CSS 140px zegt (7% indruk),
//     geen DPR-scaling (1× raster op retina), en jsPDF forceert 85×30mm (2,83:1) op een canvas
//     van ~3,2:1 → nog eens ~12% verticale rek in het énige artefact dat contractueel telt.
const r = Math.max(window.devicePixelRatio || 1, 1);
canvas.width  = container.offsetWidth * r;
canvas.height = CANVAS_CSS_HEIGHT * r;          // exact de CSS-hoogte, niet een ander getal
canvas.getContext('2d').scale(r, r);
signaturePad.clear();
new ResizeObserver(() => { /* herhaal bovenstaande */ }).observe(container);

// 2 — één bron van waarheid voor alle bedragen. Clark tikt €1.750 op r. 668, 1036 én 1271,
//     en €5.500 op r. 681, 1040 én 1294. Wijzig er één en de getekende PDF wijkt af van
//     de pagina waarop de klant tekende.
const OFFERTE = { opstart: 1750, maand: 5500, looptijd: 9, adsMin: 500, adsMax: 750 };
// pagina, modal-samenvatting én PDF renderen hieruit. Diff ze in een test.

// 3 — succes pas ná serverbevestiging
const res = await fetch('/api/signed', { method: 'POST', body });
if (!res.ok) throw new Error(res.status);
showSuccess();
// faalt hij: expliciete fallbacktekst ("download je PDF en mail hem naar …") + retry
//            + alert naar jezelf. Beloof nooit een mail die je niet kunt garanderen.

// 4 — log het akkoordvinkje. Clark laat het enige veld met juridische betekenis nergens
//     een spoor na: niet in de PDF, niet in de JSON.
body.append('agreed', document.getElementById('signatureAgree').checked);
```

**Clarks stille faalmodus, letterlijk:** `saveSignedProposal()` wordt pas ná stap 3 aangeroepen
("Goed samen te werken!" + "Een kopie wordt ook naar jullie verstuurd", r. 1068-1071) en de catch
is `console.log('Server save failed (PDF download still works):', err)` (r. 1414-1416). POST
mislukt = klant heeft getekend, Clark heeft niets, niemand merkt het.

**En twee faalmodi die geen enkele analyse vond behalve 07:** valt `signature_pad` weg, dan gooit
`signaturePad.isEmpty()` ná `e.preventDefault()` — de knop "Ondertekenen & PDF genereren" doet
letterlijk niets, zonder melding. Valt `jsPDF` weg, dan is de spinner al getoond en kijkt de klant
oneindig naar een draaiend wieltje onder de kop "Voorstel ondertekend!". Er zit geen `try/catch` om
de submit-flow. **Lazy-load beide libs pas bij het openen van de modal, mét SRI, in try/catch.**

**Juridisch eerlijk zijn.** Dit is een gewone elektronische handtekening (SES, eIDAS art. 3 lid 10),
aantoonbaar geen AdES of QES: alle bewijsmetadata is client-bepaald (`new Date().toISOString()` =
de klok van de ondertekenaar; `ipAddress` opgehaald bij een eigen endpoint en daarna als gewoon
formulierveld behandeld; `userAgent` triviaal te spoofen; de PDF wordt gebouwd in de browser van
de tegenpartij). Werkt uitstekend als **commitment-instrument**, is nul waard als bewijs.
→ Wil je écht rechtsgeldig: laatste stap naar een e-signing-provider. Wil je alleen commitment:
noem het "akkoord geven", niet "rechtsgeldig ondertekenen".

### 7.3 Het exportbestand — hier keert Clark zijn eigen werk om

**Clarks grootste verzadigingsfout, precies op het moment van maximale betrokkenheid:**
`generatePDF()` (199 regels, r. 1204-1402) bouwt drie A4's in **`helvetica`** — het gelicentieerde
huisletter zit niet in de PDF — met volvlak rood, een 🚀-emoji in de succesmodal, en op pagina 3 in
28pt *"Great working together!"* in het Engels, in een volledig Nederlands document. Alles wat 25
minuten lang is opgebouwd verdampt in de twee seconden waarin de PDF opent. **En dát bestand gaat
naar de directie, de controller en het inkoopsysteem.**

Erger nog (07, G5): de PDF-bullets zijn **herschreven** ten opzichte van de pagina. Zes van de
dertien verschillen, en de hele bulletlijst van de advertentiekaart verdwijnt — inclusief *"Budget
naar de platforms, niet naar ons"*, precies de zin die door hun eigen AV art. 5.2/5.3 wordt
tegengesproken. De pagina en het ondertekende document beschrijven andere leveringen.

**Agyle-route, twee opties, allebei goed:**

1. **Print-stylesheet** — `@page`, `break-inside: avoid` op kaarten, reveals geforceerd zichtbaar,
   accordions open, `print-color-adjust: exact`, fixed header naar `static`.
2. **Playwright/Puppeteer `page.pdf()` server-side** — dan is het bestand hetzelfde object.

**Verplichte print-gate vóór élke verzending.** Clark heeft één printregel in het hele project
(`@media print { .signature-modal { display: none } }`, html r. 194) met drie gevolgen: (a) 78
elementen staan op `opacity: 0` tot de observer ze raakt, dus alles waar nog niet langs gescrold is
print blanco; (b) `.accordion__body { max-height: 0; overflow: hidden }` → 4 van de 5 panelen
printen niet, inclusief de €11.000–13.000-besparing, het enige door de klant verifieerbare getal;
(c) browsers printen achtergronden standaard niet, dus de zes zwarte en drie rode banden printen
als bijna-wit op wit — kostensectie, garantiebanner en CTA zijn op papier leeg.

```css
@media print {
  .reveal, .reveal-group > * { opacity: 1 !important; transform: none !important; }
  .accordion__body { max-height: none !important; overflow: visible !important; }
  .sec, .card { print-color-adjust: exact; -webkit-print-color-adjust: exact;
                break-inside: avoid; }
  .header { position: static !important; }
  .gate, .modal { display: none !important; }
}
```

**Als je tóch een gegenereerde PDF wil:** houd hem als **samenvatting**, niet als kopie. Clarks
keuze — p1 commercieel, p2 handtekening + auditregels, p3 merkafsluiter — is strategisch juist: de
webpagina blijft het canonieke artefact, wie het verhaal wil herlezen moet terug naar de URL. Maar
embed dan wél je huisletter via `doc.addFileToVFS()` + `doc.addFont()` (±100 KB per gewicht) en
gebruik `doc.splitTextToSize()` — Clark doet dat nergens en positioneert elke regel met de hand.

### 7.4 De SVG-naar-PDF-truc — wél stelen, wel verbeteren

jsPDF kan geen SVG. Clarks `loadSVGAsWhite()` (r. 1176-1195) is de enige echt slimme code op de
pagina:

```js
// Verbeterde versie: currentColor i.p.v. Clarks brosse hex-replace
// (Clark vervangt zowel #0D0808 als #0D0707 omdat iemand niet wist welke in het bestand stond)
async function svgToPng(src, hex, scale = Math.max(2, devicePixelRatio * 2)) {
  const svg  = (await (await fetch(src)).text()).replace(/currentColor/g, hex);
  const url  = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
  const img  = await new Promise(res => { const i = new Image(); i.onload = () => res(i); i.src = url; });
  const c    = Object.assign(document.createElement('canvas'),
                             { width: img.width * scale, height: img.height * scale });
  c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
  URL.revokeObjectURL(url);
  return c.toDataURL('image/png');
}
```

Eén logo-asset, willekeurig veel kleurvarianten. **Preload elk asset in een eigen `try/catch` met
tekstuele fallback** — Clark zet beide preloads in één try-blok, dus faalt de eerste dan slaat de
tweede stil over.

---

## 8. Commerciële verpakking

### 8.1 Acht dingen die Clark goed doet en die Agyle overneemt

| # | Wat | Bewijs |
|---|---|---|
| 1 | **Prijs pas ná de diagnose.** De kostensectie staat op r. 659, ná zes secties situatie/aanpak/platform/tijdlijn. Bij het bedrag heeft de lezer al zes keer ja geknikt | volgorde in de HTML |
| 2 | **Kies zelf de noemer waartegen je prijs wordt vergeleken.** Zonder frame vergelijkt de klant met een uurtarief | sectiekop *"Altijd minder dan één FTE"* (r. 662) |
| 3 | **Leg uit waarom de instapprijs laag is**, zodat goedkoop niet als goedkoop leest | *"De eerste fase is voor ons de grootste investering… Daarom dit instaptarief"* (r. 663) |
| 4 | **Noem de klantmedewerkers bij naam in de deliverables** | *"zodat Mariel, Marit en Sabine in één knop nieuwe campagnes kunnen aanzetten"* (r. 402) |
| 5 | **Begroot de tijdsinvestering van de klant met een visuele schaal**, en zet die sectie **ná** de prijs | *"Maximaal 2 uur per week"* (r. 896) op 86-95% diepte, prijs op 63-71% |
| 6 | **Fase-opzegbaarheid als vertrouwenssignaal** | *"Na elke fase evalueren we samen of we doorgaan"* (r. 714) |
| 7 | **Draai het risicogesprek om met doorwerken i.p.v. geld terug.** Geld terug erkent falen; doorwerken framet falen als toewijding | *"Dan zetten we de facturatie op pauze en werken we kosteloos door"* (r. 712) |
| 8 | **Twee cursieve zelfcorrecties in de tekst.** Toegeven wat illustratief is kost niets en koopt veel | r. 653, r. 825 |

**De volgorde van 5 is het punt.** Prijs op 63–71%, tijdsinvestering op 86–95%. De laatste zorg die
je wegneemt is niet geld maar **capaciteit** — bij een PZ-afdeling van drie mensen is dat het echte
bezwaar.

### 8.2 De grens die Agyle's underpromise/overdeliver stelt

| # | Wat Clark doet | Waarom dat bij Agyle niet kan |
|---|---|---|
| 1 | **Nergens een totaalbedrag.** `grep -on "51\.250\|49\.500\|totaal"` → nul treffers | Een offerte zonder som is geen offerte |
| 2 | **De totaalregel is gevuld met een belofte.** `.signature-summary-total` (r. 1046-1049) heeft `border-top: 2px solid` en `font-size: 17px` — de exacte visuele grammatica van een totaal — en bevat *"Garantie: Rollen ingevuld in 9 mnd"* | Op die regel hoort een getal. De laatste rij van een samenvatting is het duurste vastgoed op een offerte |
| 3 | **"Excl. btw" staat één keer in de hele bron: r. 1228, in de PDF die pas ná ondertekening ontstaat** | Btw-vermelding hoort bij de prijs |
| 4 | **"p.m." op 22px/400/50% opacity naast een getal van 64px/900** — de vermenigvuldiger typografisch weggeregeld tot bijschrift | Bij Agyle staat de eenheid in dezelfde grootte als het getal |
| 5 | **Twee kernbeloften worden woord voor woord door de eigen AV tegengesproken:** *"Budget naar de platforms, niet naar ons"* (r. 700) vs AV 5.2 (doorbelasting +10% administratiekosten) en 5.3 (advertenties via Clarks eigen accounts); *"het systeem blijft volledig in jullie eigendom"* (r. 825) vs AV 8.1 (alle IE blijft bij Clark) en 8.2 (licentie **voor de duur van de overeenkomst**) | **Harde Agyle-gate: laat elk voorstel vóór verzending langs de eigen algemene voorwaarden lopen.** Eén klant die dit ontdekt kost meer dan tien deals opleveren |
| 6 | **Twee onverenigbare garanties.** Pagina: rollen gevuld in 9 maanden. AV 6.1: één geschikte kandidaat binnen 49 dagen, 6.2: geen garantie op indiensttreding, 6.3: vervalt bij o.a. "profielwijzigingen tijdens de campagne", 9.2: aansprakelijkheid gecapt op één maandfactuur (€5.500) op een verplichting van €51.250 | Definieer "geleverd", noem het maximum, noem de einddatum, noem de compensatie in euro's — in hetzelfde document |
| 7 | **Zeven leveringen, nul meetbare eenheden** (r. 684-690): geen uren, geen aantal campagnes, geen aantal voorgestelde kandidaten, geen rapportagedeadline | Zonder norm bestaat er geen onderprestatie en dus geen kwaliteit |
| 8 | **De besparing wordt nooit gesaldeerd.** €11.000–13.000/jr LinkedIn eraf, €3.600–6.000/jr Krypton-licentie er permanent bij — beide op de pagina, ~5000px uit elkaar | Salderen wat gesaldeerd hoort, in één tabel |
| 9 | **Kostencurve naar nul terwijl er een licentie doorloopt** — de grafiek spreekt de prijskaart 30 cm rechts ervan tegen | *"De grafiek is illustratief"* repareert dat niet |
| 10 | **Verkeerde klantnaam:** `alt="Harwig Beveiligingstechniek"` (r. 224) terwijl het Harwig **Installatietechniek** is — op een document dat zijn hele geloofwaardigheid ontleent aan aangetoonde aandacht | Naam-check als laatste gate |
| 11 | **Eenzijdig ondertekend stuk + eenzijdige bewijsvergaring.** IP en user-agent van de klant vastleggen terwijl je zelf alleen een getypte naam levert | Beide handtekeningen of geen |

### 8.3 De drie vragen die élk Agyle-voorstel expliciet beantwoordt

Afgeleid uit precies wat Clark laat liggen — en dit is het gat om in te gaan staan:

1. **Wat is het totaal over de volledige looptijd, inclusief alles wat wij buiten de hoofdprijs
   houden?** Eén getal, op de pagina.
2. **Wat gebeurt er met het gebouwde als de samenwerking stopt?** Eén alinea, in de offerte én in
   de voorwaarden, met dezelfde strekking.
3. **Waar staat de norm waaronder wij zakken?** Eén meetbare zin.

Clark scoort op geen van de drie. Vorm overtreffen is haalbaar; **eerlijkheid overtreffen is hier
goedkoop.**

### 8.4 Botsing met de Agyle-prijsregel — expliciet oplossen

`agyle-business/CLAUDE.md` zegt: *"Geen prijzen in klant-facing documenten — offertes, voorstellen
en dossiers die naar de klant gaan bevatten géén tarieven of bedragen tenzij Abdul dat expliciet
vraagt."* Clark zet €1.750 / €5.500 / €500-750 full-page neer. Dat is een directe botsing en die
moet je vóór de bouw beslechten, niet halverwege.

| Route | Wat je doet |
|---|---|
| **A — regel bewust openbreken voor dit formaat** (aanbevolen) | Een ondertekenbare voorstelsite zónder prijs is intern inconsistent: je kunt niet laten accorderen wat je niet toont. Als Abdul dit format kiest, dan mét prijs, mét totaal, mét btw en mét meerjarenlast. Vraag dat één keer expliciet en leg het vast |
| **B — regel handhaven** | Vervang de kostensectie door **scope + doorlooptijd + tijdsinvestering**. De anker-truc (drie kaarten, middelste gemarkeerd, headline "Altijd minder dan één FTE") vervalt en wordt een scope-vergelijking. De CTA wordt "Akkoord op scope", niet "Accorderen" op een bedrag. Prijzen leven in een aparte interne versie |

Niet doen: half. Een voorstel met twee van de drie prijzen is slechter dan beide varianten.

---

## 9. Bouwvolgorde — van leeg bestand naar opgeleverde site

**Fase A is chassis: eenmalig, kost €0 bij elk volgend voorstel. Fase B is per klant.**

### Fase A — chassis (eenmalig, 22–34 u)

| # | Stap | Uren | Klaar als |
|---|---|---:|---|
| A1 | **Font kiezen en licentie regelen.** Zelfde hefboom als bij Clark (ratio 16,0), en het enige juridisch blokkerende onderdeel. Self-host woff2+woff, 4 gewichten die je écht bezit (400/500/700/900), `font-display: swap` | 1–3 | `@font-face`-blok staat, geen 600/800 gedeclareerd, geen faux italic |
| A2 | **Tokenlaag + fluid schaal** — het `:root{}`-blok uit §3.2, letterlijk plakken en de kleuren checken op contrast | 2 | Elke maat is een clamp, elk maximum topt af tussen 1580 en 1640px |
| A3 | **Sectie-chassis** — `.sec`, 5 achtergrondvarianten, `.sec__inner`, de molecule (eyebrow → titel → intro), `color` op de sectievariant | 1,5 | Vijf lege secties in wisselende kleuren scrollen als hoofdstukken |
| A4 | **Motion-laag** — reveal-primitief, één observer, container-stagger met `--i`, de play-state-truc, `prefers-reduced-motion`, `.no-js` | 1,5 | Reveals draaien op easeOutExpo, reduced-motion-test slaagt, JS uit = pagina leesbaar |
| A5 | **Chrome** — fixed header met wegduik-gedrag (`{passive:true}`, delta-drempel 8px, klasse i.p.v. inline style), `--header-h`, sticky-offset-helper | 1 | Header verdwijnt bij scroll-down, komt terug bij scroll-up, geen jitter |
| A6 | **Componentbibliotheek** — kaart, prijskaart, chip/badge, accordeon (`grid-template-rows: 0fr→1fr`, eerste item open, **`<button>` met `aria-expanded`**), timeline, effort-pips, stakeholderkaart, split-layout met sticky kolom, 3-koloms `clamp() 1fr clamp()`-rij | 6–8 | Elke component is een klasse, nul inline `style=` |
| A7 | **De gate** — CSS + JS uit §7.1, plus `.htpasswd` of signed token op de map | 3 | Vier vakjes, shake, 500ms-pauze, server-side afgedwongen |
| A8 | **Ondertekenflow** — modal met `role="dialog"` + focus-trap, DPR-correcte canvas met ResizeObserver, `OFFERTE`-constantenobject, POST-eerst-dan-succes, lazy libs met SRI | 5–8 | Handtekening scherp op retina, faalpad toont melding, akkoordvinkje wordt gelogd |
| A9 | **Print/export-laag** — `@media print`-blok uit §7.3, of Playwright-route | 1,5 | Geprinte pagina toont álle secties, alle accordeons open, kleurvlakken zichtbaar |

**Verificatie-gate vóór A klaar is:** render op **375 / 800 / 1024 / 1440 / 1920 px plus een
printvoorbeeld** en kijk ernaar. Zes analyses van 260 KB over een visueel document zonder één
rendering hebben vier van de grootste defecten gemist (mobiele twee-koloms grid, geen printstijl,
de zwakste viewport, de mobiele ervaring als geheel). Dit is de goedkoopste QA die bestaat.

### Fase B — per klant (7–13 u)

| # | Stap | Uren | Klaar als |
|---|---|---:|---|
| B1 | **Discovery-oogst.** Uit 1–2 gesprekken van een uur haal je alles wat Clark's 33 personalisatiemomenten voedt: openstaande rollen + hoe lang, incumbent-tool + kosten + resultaat, concurrenten bij naam, mensen op de afdeling + rol, groeidoel, en **minstens één letterlijk idioom uit het transcript** | 1 | Lijstje van ≥25 verifieerbare klantfeiten |
| B2 | **Copy schrijven op het skelet.** Eyebrows eerst (dat is je argumentatie), dan de pijnmuur met het compliment als laatste kaart, dan de rest | 4–6 | Elke kaart bevat ≥1 klantgetal/naam/jaartal. Nul "u", nul "je" |
| B3 | **Kleurpartituur nalopen.** Donker = wij vragen iets, licht = jullie krijgen iets, merkvlak alleen hero/aanpak/CTA. **Nooit twee identieke achtergronden achter elkaar** | 0,25 | Sequentie op papier gecheckt |
| B4 | **Beeld.** Klantlogo in de header naast het jouwe, hero-collage (2 foto's + 3 CSS-vormen), portret met los onderschriftkaartje | 1 | Alt-teksten kloppen — inclusief de bedrijfsnaam |
| B5 | **De grafiek — of drie getallen.** Alleen bouwen als alle vier de voorwaarden uit §6.1 haalbaar zijn. Anders drie cijfers op een rij | 0,5–3 | Eenheid op de as, baseline uit klantdata, bron eronder |
| B6 | **Cijfers invullen** in het `OFFERTE`-object; pagina, samenvatting en PDF renderen daaruit | 0,25 | Eén bron, drie renders, diff-test groen |
| B7 | **Dode componenten strippen** die deze klant niet gebruikt | 0,25 | Geen 0×-gebruikte klasse in de geleverde CSS |
| B8 | **AV-kruistabel.** Leg webpagina, exportbestand en algemene voorwaarden naast elkaar in **één tabel met drie kolommen**. De belangrijkste vondst van de hele teardown viel tussen twee analyses in omdat niemand alle drie tegelijk las | 0,5 | Geen belofte op de pagina die de AV tegenspreekt |
| B9 | **Leveringscheck.** Drie vragen uit §8.3 beantwoord? Totaal op de pagina? Btw genoemd? Meetbare eenheden per levering? | 0,25 | Alle vier ja |
| B10 | **Render-QA op 5 breedtes + print**, en één keer met JS uit en één keer met reduced-motion aan | 0,5 | Geen horizontale scroll, geen blanco printsectie |

**Marginale kosten van voorstel nummer 20 ≈ nul, terwijl elke klant een microsite op maat ziet.**
Dat is de eigenlijke business-innovatie van Clark, niet de techniek.

---

## 10. Anti-patronen — wat je NIET overneemt

### 10.1 Inhoudelijk

| Anti-patroon | Waarom niet |
|---|---|
| **Contentvrije diagrammen** | Clarks `.pyramid` (4 rijen: Top Talent / Optimalisatie / Rapportage+Reflectie / Passieve+Actieve Recruitment) en het hex-"radar"-diagram (Groei / DNA / Talent / Overzicht) zijn vorm zonder mechanisme. De hex-visual is twee statische `<img>`'s met `left:22%; width:66%; height:77%` — bewust niet-gecentreerd zodat de vorm asymmetrisch leest als *meetresultaat*. Precies de technische, kritische lezer die Agyle wil, zoekt in een diagram naar een mechanisme; vindt hij dat niet, dan is het diagram geen neutrale versiering maar een **min**. *(NB: 07 corrigeert 01 en 06 — de piramide hééft wél een toelichting mét klantnamen op r. 426. Het punt blijft: er wordt niet uitgelegd waaróm de lagen in die volgorde staan.)* |
| **Nul bewijsvoering** | Geen klantcase, geen referentie, geen plaatsingscijfer, geen klantlogo. De enige logo's zijn Meta, LinkedIn en het eigen Krypton — **leverancierslogo's**. De enige quote is van een eigen medewerker. Clark heeft de `.stat-grid`/`.stat-card__number`-component én `initCountUp()` in het chassis en laat ze leeg: ze hebben de cijfers niet. **Eén echte case met echte cijfers slaat dit hele blok uit elkaar.** |
| **De verkoper sticky in beeld** | `.aanpak-split__julian` staat twee schermen lang te kijken, met een quote waarin de verkoper zichzelf verkoopt — de zwakste vorm van bewijs die er is. Vervang door een klantquote of een concreet resultaat |
| **Verzadigde merkkleur over vier volle schermen** | Hero + Aanpak + Bouwstenen + CTA staan alle vier op `#DC0000` full-bleed, plus de gate, plus de highlight-prijskaart, plus alle drie PDF-pagina's. Bij een installateur die zelf navy en grijs draagt leest dat als "marketingbureau". **`#97D4E8` is bovendien te licht voor witte tekst** — sky werkt als accent en als tint, niet als tekstvlak. Zwart draagt full-bleed veel verder dan een primaire kleur |
| **Jargondichtheid** | *datalaag, meetlaag, sourcing engine, multi-touch flow, funnel, brand guide, tone of voice, knowledgebase, arbeidsmarktcommunicatieplan* — elk woord apart verdedigbaar, samen creëren ze afstand bij precies de doelgroep waarvan Clark zelf schrijft dat die "überhaupt niet op LinkedIn zit". En het botst met hun eigen sterkste zinnen, die juist plat en concreet zijn |
| **Te lang om je eigen belofte waar te maken** | 4.960 woorden ≈ 22-25 minuten, in een document dat "maximaal 2 uur per week" belooft aan hetzelfde team. Geen samenvatting, geen "in het kort", geen leeswijzer. Bouw een leeswijzer of een TL;DR-blok bovenaan |
| **Eigennamen zonder inhoud eronder** | "Krypton" is een anti-benchmarkinstrument: zolang het zo heet kan de klant geen tweede offerte voor Krypton opvragen. Gebruik dit bewust en spaarzaam — en zorg dat er iets echts onder zit |

### 10.2 Technisch

| Anti-patroon | Bewijs |
|---|---|
| **Inline `style=` op een layout-property** | `<div class="vacancy-grid reveal-stagger" style="grid-template-columns: repeat(2, 1fr);">` (html r. 315) verslaat `@media (max-width:768px){ .vacancy-grid{grid-template-columns:1fr} }` (voorstel.css 1771), want inline wint van élke stylesheetregel. Op 375px: ~155px per kaart min 2×24px padding = **~107px tekstbreedte** voor koppen als "Servicemonteurs & Servicetechnici". Het bewijs dat ze het zagen maar niet fixten is de allereerste regel van de inline `<style>` in de head: `.vacancy-card__title { overflow-wrap: break-word; hyphens: auto; }` (r. 16-19). **Layout-uitzonderingen krijgen een modifier-klasse, nooit een attribuut** |
| **54 inline `style=`-attributen totaal** | Een hele sectie (r. 727-823) is volledig inline gestyled, mét een eigen radius-schaal `clamp(16px,1.4vw,22px)` die net niet gelijk is aan de systeemwaarde. Dat is waar de deadline zichtbaar wordt |
| **Een type-schaal die je niet gebruikt** | `.text-display` … `.text-label` (base.css 100-107) komen **0×** voor in de HTML. In plaats daarvan 242 losse clamps in voorstel.css + 43 inline. Het "designsysteem" is een tokenbestand dat de pagina niet consumeert. *(De bruikbare vorm is de tripletten-woordenlijst: 242 clamps = 109 unieke tripletten, top-6 dekt ~25% van al het gebruik. De workhorse is `clamp(14px, 1.1vw, 20px)`, 15× gebruikt, 15,8px op 1440.)* |
| **Eén breakpoint op 768 voor tweekoloms layouts** | Op 1024px staat de layout al in desktop-tweekolommen terwijl **148 van 242 clamps (61%) nog op hun telefoonwaarde staat**; op 768 is dat 227/242 (94%). Klap splits pas om bij **1080px**, niet 768 |
| **`transition: all`** | Staat op `a`, `button`, `.btn` (base.css 93, 94, 122) en vijf modal-selectors. Onbedoelde properties worden meegeanimeerd; de scroll-hint moest er al omheen werken met een eigen `transition: color 0.3s` override |
| **Layout-properties in een rAF-loop** | `updateFill()` — zie §5.5 |
| **Nul focus-styling** | `input { outline: none }` staat globaal in base.css:95 zonder vervanging, buttons hebben geen enkele focus-stijl, `:focus-visible` komt 0× voor. Tab-navigatie is onzichtbaar |
| **`<div>` met click-listener als accordeon-header** | html r. 493 + voorstel.js 75: geen `<button>`, geen `tabindex`, geen `role`, geen `aria-expanded`, geen Enter/Space. Vijf panelen die met toetsenbord niet te openen zijn. En `body.scrollHeight` wordt gemeten op `DOMContentLoaded`, dus vóór de font-swap → het standaard-open paneel klopt niet na font-load |
| **`<a href="javascript:void(0)" onclick="…">` als CTA** | html r. 970. De belangrijkste knop van het document. Hoort een `<button>` te zijn |
| **Render-blocking CDN's zonder SRI op een ondertekenbaar document** | ~372 KB in de `<head>` voor functionaliteit achter een klik. Een compromised bestand kan de formuliervelden uitlezen of de handtekening-dataURL exfiltreren |
| **Hardcoded token als enige toegangscontrole** | `body.append('token', 'clark-voorstel-2026')` (r. 1409) op het upload-endpoint, in de broncode van élke voorstelpagina |
| **Dode kit-resten meeleveren** | 39 klassen + 2 JS-functies dood. Ziet de klant niet, maar het is het verschil tussen een kit die je vertrouwt en een kit die je elke keer opnieuw moet controleren |
| **Nul hover op contentkaarten** | Zes hover-regels op de hele pagina, vier daarvan in een modal. Desktop voelt dood. Een `.card:hover { transform: translateY(-4px) }` op dezelfde 0,3s-ladder tilt de hele desktop-ervaring op voor twaalf regels CSS |
| **Twee modules die dezelfde globale style-property schrijven** | `pincode.js:38` zet `body.style.overflow='hidden'`; de onvoorwaardelijke Escape-handler (html 1117-1121) roept `closeSignatureModal()` aan die hem op `''` zet. Eén druk op Escape op het pincodescherm heft de scroll-lock op |

### 10.3 Methodisch — voor wie dit playbook toepast

- **Render eerst, analyseer daarna.** Screenshots op 375 / 800 / 1024 / 1440 / 1920 plus een
  printvoorbeeld, vóór er één regel over "het oogt duur" wordt geschreven.
- **Meet nooit een regel aan CSS waarvan je zelf hebt aangetoond dat ze 0× gebruikt wordt.** Splits
  élke inventaris in levend en dood en trek conclusies alleen uit de levende helft. Twee van de
  meest geciteerde "recepten" uit deze teardown (het 1512-frame, de ÷20-ruimteregel) zijn gemeten
  op dode CSS en houden geen stand.
- **Test elke gereconstrueerde ontwerpregel op de hele populatie**, niet op vijf handgekozen waarden.
- **Vermeld bij élke telling het bereik** (heel bestand / zichtbare body / exclusief CSS-klassen en
  JS-strings). Twee analyses gaven 19 en 14 voor hetzelfde woord; zonder bereik is geen enkel
  telgetal citeerbaar richting een klant.
- **Label interpretatie streng.** Een MD5-bestandsnaam, een KvK-nummer of een versiestring is een
  aanwijzing, geen feit.
- **Archiveer élke bron waar je uit citeert lokaal vóór je erin citeert** — assets, fonts, PDF's,
  endpoints. Het sterkste juridische materiaal van deze teardown rust nu op één niet-bewaarde fetch.

---

## Bijlage — snelle referentie

```
KLEUR         --ink #070C0E · --sky #97D4E8 · --sky-ink #10596E · --paper #EDF6F9
              --on-dark #F2FBFE · --card-dark #202527 · --ok #35A96F
FRAME         ontwerp 1440px · --max-w 1600px · --pad-x clamp(24px, 5.55vw, 89px)
TYPE-FORMULE  vw = design ÷ 14.4   ·   max = design × 1.111   ·   min = 0,55–0,78 × design
RUIMTE        max = 2 × min · vw = max ÷ 16 · sectie clamp(64px, 8vw, 128px)
RADIUS        clamp(16px, 1.66vw, 27px) — één kaartradius, vloeiend
STROKE        1px = data · 2px = structuur · 4px = accent
SCHADUW       geen. Diepte = full-bleed kleurvlak + hairline
REVEAL        translateY(40px) · 0.7s cubic-bezier(0.19,1,0.22,1) · mobiel 30px/0.6s
OBSERVER      threshold 0.15 · rootMargin '0px 0px -40px 0px' · unobserve na 1×
STAGGER       container observeren · --i per kind · transition-delay calc(var(--i) * 70ms)
EASING        expo-out (0.19,1,0.22,1) alles · overshoot (0.34,1.56,0.64,1) alleen vormen
TIMING        0.2 micro · 0.3 state · 0.38 paneel · 0.7 reveal · 1.5 choreografie · 1.0 gate
STICKY        top: calc(var(--header-h) + var(--sp-block))
HERO          min-height: 100vh; min-height: 100svh   (in die volgorde)
HEADER        scrollY > 200 && scrollY > lastY → translateY(-100%), 0.35s, {passive:true}, Δ≥8px
GATE          500ms pauze → 0.5s fade → remove na 600ms (parallel) = 1,0s ceremonie
BREAKPOINTS   768 (telefoon-topologie) + 1080 (splits klappen om). Nooit inline layout-overrides
VERPLICHT     prefers-reduced-motion · .no-js fallback · @media print · tabular-nums · try/catch
```

**Bronbestanden:**
`clark-teardown/bron/{voorstel-harwig.html, css/{base,voorstel,pincode}.css, js/{voorstel,pincode}.js, svg/*}`
**Analyses:** `clark-teardown/analyse/01` t/m `08`, met `07-kritiek.md` als correctie-instantie.
