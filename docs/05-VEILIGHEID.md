# Veiligheid en vertrouwelijkheid

Kort document, maar dit zijn de dingen die een klant geld of vertrouwen kosten als ze
misgaan. Lees het één keer goed.

---

## Mail: alleen concepten, nooit verzenden

Wij gebruiken uitsluitend de conceptfunctie (`Mail.ReadWrite`). De verzendrechten
(`Mail.Send`) zetten we bewust niet aan.

Waarom: een mail die automatisch naar een klant vertrekt kun je niet terughalen, en de
toon van klantcommunicatie is hier belangrijk genoeg om er zelf nog naar te kijken.
Claude zet de concept klaar, jij leest hem na en drukt op verzenden.

## Geen prijzen in klant-facing documenten

Offertes, voorstellen en dossiers die naar de klant gaan bevatten geen tarieven of
bedragen, tenzij Abdul dat expliciet vraagt. Noem hooguit scope en doorlooptijd.

Houd twee versies: een interne mét bedragen, een klantversie zonder. Bij Harwig is dat
bijvoorbeeld het verschil tussen het bouwvoorstel (intern) en het ideeëndocument
(klantversie).

Dit is twee keer misgegaan en moest achteraf gerepareerd worden. Vandaar dat het hier
staat.

## Klantdata is read-only

Aangeleverde exports, tekeningen en referentieprojecten bewerk je niet. Ze zijn de
meetlat waartegen we ons werk verifiëren — verandert de meetlat, dan kun je niets meer
aantonen. Werk met kopieën.

## Geen sleutels in de repository

API-keys, tokens en wachtwoorden horen niet in git en niet in een skill-map. Gebruik een
`.env` die in `.gitignore` staat, of een omgevingsvariabele.

Kom je een sleutel tegen die wél gecommitteerd is: **melden, niet stilletjes
verwijderen.** Een key die ooit in de geschiedenis heeft gestaan moet geroteerd worden;
weghalen uit het laatste bestand is niet genoeg.

Deel ook geen configuratiebestanden zonder te kijken wat erin staat. `~/.claude.json`
bevat bijvoorbeeld tokens van al je MCP-servers.

## Verifieer voordat je iets naar de klant zegt

Denk je een fout in de klantdata gevonden te hebben, of meldt een tool iets opvallends:
controleer het eerst zelf handmatig. Formuleer het daarna als vraag, niet als
constatering — "klopt het dat X hier Y is?" in plaats van "jullie bestand bevat een
fout".

Dat geldt ook voor resultaten die je zelf niet hebt gedraaid. Testuitslagen en
tussenrapportages van tools neem je niet op gezag over in een klantmail.

## Wat vertrouwelijk is

Klantnamen, contactpersonen, tarieven, transcripties en alle inhoud van `clients/` zijn
vertrouwelijk. Niet delen buiten Agyle, niet in publieke repositories, niet als voorbeeld
in een gesprek met een andere klant.

Bij Van den Pol geldt daarbovenop een contractuele afspraak: klantspecifiek werk is
gezamenlijk eigendom en mag alleen met wederzijdse toestemming buiten de Eiffage-groep
verstrekt worden.

## Twijfel je?

Vraag het. Bij dit onderwerp is een overbodige vraag altijd goedkoper dan een verkeerde
aanname.
