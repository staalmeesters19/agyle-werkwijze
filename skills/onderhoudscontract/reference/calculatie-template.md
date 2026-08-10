# INTERN — Onderhoudscontract <dienst> — calculatie & onderhandelruimte

> **Niet naar de klant.** Interne tegenhanger van het concept-onderhoudscontract. Bevat marge-onderbouwing en onderhandelposities. Klantversie: `Onderhoudscontract <Leverancier> - <Klant> - <Dienst> (concept).md`.

## Gekozen commerciële uitgangspunten (bevestigd <naam>, <datum>)

- **Prijsmodel:** <volume-staffel / vast bedrag / …>. Klein pakket tegen vol tarief €<X>/u; groot pakket tegen €<Y>/u.
- **Hosting:** <wie neemt de omgeving af> → <welk risico ligt daarmee waar>.
- **Looptijd:** <12 mnd vast, daarna maandelijks opzegbaar (1 mnd)>.

## Pakketopbouw

| Pakket | Uren/mnd | Uurtarief | Maandbedrag | Jaaromzet (12 mnd) |
|---|---|---|---|---|
| Basis | <5> | € <175> | € <875> | € <10.500> |
| Uitgebreid | <10> | € <160> | € <1.600> | € <19.200> |

- Impliciete korting op het grote pakket: €<15>/u × <10>u = **€<150>/mnd** t.o.v. vol tarief (€<1.750>). ≈ <8,6>% volumekorting. Verdedigbaar als commitment-beloning.
- Buiten-pakket uren: **€<175>/u** (vol tarief, geldende indexatie). Grotere wijzigingen als aparte scope begroten.

## Eenmalige inrichting (bij livegang)

- **Op uurbasis €<175>/u, richtinggevend <6–10> uur** → indicatief **€<1.050>–€<1.750>** eenmalig. Buiten het maandpakket.
- Waarom die band: <wat er al klaar is — containerisatie, healthchecks, auto-update, deploydocs>. Het zware werk is gedaan; resterend = <provisioning, env/secrets, DNS+SSL, parity-test>.
- Risicoposten die de band naar boven duwen: <firewall/poorten, SSL, DNS-propagatie, eigenaardigheden van de host>. Daarom band i.p.v. vast bedrag.
- Uitvoering: <naam>.

## Marge-overwegingen

- <Welke doorlopende kosten liggen bij de leverancier? Bij klant-afgenomen hosting: geen — het hele maandbedrag is dienstverlening.>
- Break-even zit in de bestede uren; bij een rustige maand loopt de marge op. Ongebruikte uren vervallen — expliciet maken zodra de klant erom vraagt.
- Risico: kost beheer structureel méér dan de pakketuren → tijdig signaleren en een pakket-upgrade voorstellen, niet stilzwijgend meewerken.

## Onderhandelruimte

- **Tarief groot pakket:** €<160> is voorstel. Bandbreedte €<150>–<170>. Onder €<150> niet gaan.
- **Klein pakket:** vol tarief vasthouden — niet weggeven op het kleinste pakket.
- **Looptijd:** <12> mnd is comfortabel; terugvalpositie <6> mnd minimum.
- **SLA:** bewust licht (geen boeteclausules). Wil de klant hardere garanties → hoger pakket/tarief, niet gratis meenemen.

## Beslissingen bevestigd (<naam>, <datum>)

1. **Ondertekenaar:** <naam, functie>. ✓
2. **Tarief groot pakket:** €<160>/u → €<1.600>/mnd. ✓
3. **Reactietijden** art. 5: <akkoord>. ✓
4. **Startdatum:** <bij livegang, na afronding migratie>. ✓
5. **Branded PDF** gegenereerd → `<bestandsnaam>.pdf`. ✓

## Bewust NIET in het contract

- <Variabele kosten, bijv. API-/tokenverbruik> → aparte doorbelasting of klant-eigen key. Hoort niet in een vast maandbedrag.
- <Aparte scopes / nieuwe trajecten> → los begroten.

## Positionering voor de begeleidende mail (niet de contracttekst)

- <Groot pakket> actief aanbevelen; downgrade na de eerste termijn als comfort-argument ("je zit nergens aan vast").
- Uren-onderbouwing = proactieve security + rapportage + deployment-buffer (±<8>u effectieve inzet), niet "aantal storingen".

## Nog te doen

- [ ] <Concept reviewen, definitief maken (datum/versie), versturen naar <naam> (cc <naam>)>.
