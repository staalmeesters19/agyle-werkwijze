# {{KLANT}} — klantinstructies{{TRAJECT_SUFFIX}}

<!--
TEMPLATE. /nieuwe-klant vult dit in. Vul je het met de hand in: houd de zeven secties
aan en gooi weg wat niet van toepassing is. Liever een korte sectie dan een lege kop.
-->

Laadt NA `~/.claude/CLAUDE.md` en `agyle-business/CLAUDE.md`. Conflicteert een regel
hier met de business-CLAUDE.md, beargumenteer dat expliciet — stilzwijgend overschrijven
doen we niet.

## Contacten

| Naam | Rol | Mail |
|---|---|---|
| {{CONTACT_NAAM}} | {{CONTACT_ROL}} | {{CONTACT_MAIL}} |

<!-- Vermeld per contact waar hij/zij over gaat: inhoudelijk, commercieel, facturen.
     Dat scheelt later een verkeerd geadresseerde mail. -->

## Waar staat wat

- [`PROGRESS.md`](PROGRESS.md) — wat er is gedaan, per sessie, met urenschatting
- [`HANDOVER.md`](HANDOVER.md) — open punten en wat de volgende sessie moet weten
- [`mail_{{CONTACT_SLUG}}.md`](mail_{{CONTACT_SLUG}}.md) — communicatietijdlijn
- `vergaderingen/` — transcripten, notulen (md + pdf), briefings
- `documenten/` — analyses en technische stukken
- `offertes/` — uitgebrachte offertes

## De opdracht

{{OPDRACHT}}

**Acceptatiecriterium van de klant:** {{ACCEPTATIECRITERIUM}}

<!-- Dit veld is belangrijker dan het lijkt. Bij Bohn was het letterlijk "we have to come
     to the same results" als hun eigen engineer — dat bepaalt hoe je alles verifieert. -->

## Contractuele basis

{{CONTRACT}}

<!-- Tarief, budget, facturatieritme, eigendom van het opgeleverde werk, en waar de
     getekende offerte staat. Ontbreekt dat nog: schrijf "nog niet vastgelegd" en laat
     het staan als open punt in HANDOVER.md. -->

## Kernprincipe

{{KERNPRINCIPE}}

<!-- Het niet-onderhandelbare uitgangspunt van dit project. Eén alinea. Voorbeeld uit het
     Bohn-dossier: "SCHAALBAARHEID BOVEN ALLES — we maken een schaalbaar product dat ook
     bij andere projecten en klanten werkt, geen oplossing die toevallig op de vijf
     voorbeelden past." Weet je het nog niet, laat de sectie dan weg tot je het weet. -->

## Conventies

- Meeting-artefacten in `vergaderingen/`, nooit los in de klantroot.
- Klant-facing documenten bevatten geen tarieven; houd een aparte interne versie.
- Uren boeken op het juiste project in het Agyle CRM.
- Aangeleverde klantdata is read-only.
- {{TAAL_REGEL}}
