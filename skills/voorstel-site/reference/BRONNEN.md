# Bronnen achter dit playbook

Alles staat in `agyle-business/clients/Harwig/wervingssysteem/documenten/achtergrond/clark-teardown/`.

## De bron — Clark's voorstel voor Harwig

`https://voorstel.clark.amsterdam/harwig/`, pincode **2605**. Lokaal gearchiveerd in `bron/`:

| Bestand | Regels | Wat |
|---|---:|---|
| `voorstel-harwig.html` | 1420 | de complete pagina, 13 secties, 13 SVG's, 54 inline styles |
| `css/voorstel.css` | 1856 | het zware werk — 47% van alle regels, 242 clamps |
| `css/base.css` | 175 | tokens, Youth-font (5 gewichten), 8-staps type-scale |
| `css/pincode.css` | 140 | de gate |
| `js/voorstel.js` | 178 | observer, accordeon, timeline, PDF |
| `js/pincode.js` | 153 | gating-logica, ES5 |
| `svg/*.svg` | — | 7 iconen en logo's |
| `Algemene_Voorwaarden_CLARK_2026.pdf` | 2,0 MB | het sterkste materiaal: spreekt twee kernbeloften van de pagina tegen |

Totaal 3.922 handgeschreven regels, ~141 KB, geen build-step, 2 CDN-scripts (signature_pad 4.1.7,
jsPDF 2.5.1). De live pagina was op 2026-08-05 byte-identiek aan de capture van juli.

**Herkomst:** Maureen Nederhoed (algemeen directeur Harwig) mailde de link door op 29-05-2026 met de
vraag *"kun jij hun werkwijze eens platslaan?"*. Clark bezocht Harwig op 26-05-2026; Hans Weehuizen
(unitystaffinggroup.com) organiseerde, met guan@ en julian@clark.amsterdam.

## De analyses

| # | Bestand | Dimensie |
|---|---|---|
| 01 | `narratief-en-overtuiging.md` | sectie-architectuur, betoogmodel, personalisatie, bewijsvoering, toon |
| 02 | `designsysteem.md` | kleurtokens, type-scale, ruimte, layout, componenten, premium-tells |
| 03 | `motion-en-interactie.md` | keyframes, easing, reveal-systeem, JS regel voor regel |
| 04 | `dataviz-en-grafieken.md` | alle 13 SVG's, gereconstrueerde datapunten, data-eerlijkheid |
| 05 | `tech-en-wow-mechaniek.md` | stack, gate, handtekening, jsPDF, kwetsbaarheden |
| 06 | `commercieel-model.md` | propositie, prijsopbouw, garantie, lock-in, partijenstructuur |
| 07 | `kritiek.md` | **correctie-instantie** — corrigeert 01–06, volg dit bij tegenspraak |
| 08 | `effect-analyse.md` | waarom het indruk maakt, effect-dragers op rendement |

Samen ~380 KB. `PLAYBOOK.md` is de synthese; deze acht zijn de onderbouwing als je een detail wilt
natrekken.

## Steekproef — eigen verificatie van de kernclaims

Nagerekend op de bron, niet overgenomen van een agent:

```
box-shadow in het componentsysteem   0
clamp() in voorstel.css            242
media queries totaal                 3   (alle drie @768px, dus één breakpoint)
elementen met .reveal in class      83   (waarvan 5 .reveal-stagger-containers → 78 echte)
aria-attributen in 1420 regels HTML  1
prefers-reduced-motion               0
inline style="..."                  54
```
