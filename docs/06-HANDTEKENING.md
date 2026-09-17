# Handtekening onder mails die je agent klaarzet

Voor iedereen die via de ms365-MCP mails laat opstellen en merkt dat de Agyle-handtekening
ontbreekt. Dit document legt uit waarom dat gebeurt en hoe je het in een kwartier oplost.

## Waarom je handtekening ontbreekt

De handtekening die je in Outlook hebt ingesteld, wordt door Outlook zelf onder een mail
geplakt op het moment dat jíj op "nieuw bericht" klikt. Een mail die via de Microsoft Graph
API wordt aangemaakt (en dat doet de MCP) slaat die stap over: Graph maakt het bericht aan
met precies de body die de agent meegeeft, niets meer. Er is geen instelling die dit
verandert. De handtekening moet dus in de body zelf zitten, als HTML, en de agent moet die
er elke keer onder plakken.

Twee dingen gaan daarbij standaard mis, en die hebben we al een keer opgelost:

1. **Plaatjes als inline-bijlage (cid).** Outlook Web dupliceert die bij elke autosave en
   tekent bij de ontvanger lege blokken. Daarom staan de plaatjes gehost op een https-URL:
   `https://agyle-email-assets.vercel.app/{logo,blok,booking}.png`. Die URL's zijn voor
   iedereen gelijk.
2. **Bodytekst in Times New Roman, handtekening in Aptos.** Graph zet geen standaardfont.
   Daarom gaat de bodytekst in een `<div>` met een expliciete Aptos-fontstack.

## Route A: het hele pakket installeren (aanbevolen)

Dan krijg je `/mail` erbij, dat dit allemaal zelf afhandelt, plus de rest van de werkwijze.

1. Clone `https://github.com/staalmeesters19/agyle-werkwijze` (vraag Abdul om toegang).
2. `Copy-Item config\persoon.example.json config\persoon.json` en vul naam, functie,
   e-mail, telefoon en je Bookings-link in. Geen Bookings-link? Laat leeg, dan wordt het
   boekingsblok weggelaten.
3. `.\INSTALL.ps1` en daarna `.\VALIDATE.ps1`.
4. Claude Code herstarten. Zeg dan bijvoorbeeld: `/mail Joris — even bijpraten deze week`.

De installer schrijft je persoonlijke handtekening naar
`~/.claude/assets/agyle-signature-url.html`. Bewerk dat bestand niet met de hand; pas
`persoon.json` aan en draai de installer opnieuw.

## Route B: alleen de handtekening (zonder het pakket)

Voor wie al een eigen mail-setup heeft en alleen de handtekening mist.

1. Kopieer `templates/agyle-signature-url.template.html` naar
   `~/.claude/assets/agyle-signature-url.html`.
2. Vervang in dat bestand de placeholders:

   | Placeholder | Voorbeeld |
   |---|---|
   | `{{NAAM}}` | `Joris Merkx` |
   | `{{FUNCTIE}}` | `AI CONSULTANT` (hoofdletters, zo staat het in de huisstijl) |
   | `{{EMAIL}}` | `joris.merkx@agyle.nl` (komt twee keer voor) |
   | `{{TELEFOON}}` | `+31612345678` (komt twee keer voor, zonder spaties) |
   | `{{BOOKINGS_URL}}` | je link van outlook.office.com/bookwithme, via "Delen" (komt twee keer voor) |

   Geen Bookings-link? Verwijder alles tussen `<!-- BOOKINGS-START -->` en
   `<!-- BOOKINGS-END -->`, inclusief die twee regels.
3. Zet onderstaand blok in je `~/.claude/CLAUDE.md` (of in de systeeminstructie van welke
   agent je ook gebruikt):

```markdown
## Mail via ms365-MCP

- Alleen concepten: `create-draft-email`, `create-reply-draft`, `create-reply-all-draft`.
  Nooit `send-mail` of `Mail.Send`; ik verstuur zelf vanuit Outlook.
- Body is HTML. Elke regel een `<div>…</div>`, elke witregel een expliciete
  `<div><br></div>`. Geen `<p>` (Outlook Web plet de marges), geen platte tekst met
  newlines (die collapsen).
- Wikkel de hele bodytekst in:
  `<div style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">…</div>`
  Zonder deze wrapper staat de tekst in Times New Roman en de handtekening in Aptos.
- Handtekening: lees `~/.claude/assets/agyle-signature-url.html` en plak de inhoud
  letterlijk ná de wrapper, als laatste stuk van de body. Bij een reply gaat hij in
  `Comment`, na de reply-tekst.
- Nooit `add-mail-attachment` voor de handtekening. De plaatjes zijn gehost; er zijn
  geen bijlagen nodig.
- Geen eigen afsluiting typen. "Met vriendelijke groet," en mijn naam staan al in het
  handtekeningblok.
- `create-draft-email` heeft één top-level parameter `body` die het hele message-object
  is: `{ subject, toRecipients:[{emailAddress:{address,name}}], body:{contentType:"html", content:"…"} }`.
  `toRecipients` op het top-level geeft een 400.
```

4. Test: laat je agent een conceptmail aan jezelf klaarzetten, open hem in Outlook, en
   controleer dat de bodytekst en de handtekening in hetzelfde font staan en dat de
   plaatjes laden.

## Wat je kunt verwachten bij ontvangers

Sommige externe ontvangers zien de plaatjes pas na één keer "afbeeldingen weergeven".
Dat is normaal voor gehoste afbeeldingen en gebeurt ook bij handtekeningen die Outlook
zelf plakt. Intern (Outlook naar Outlook) laden ze direct.

## Als het niet werkt

- **Handtekening dubbel, of "Groet, <naam>" twee keer.** De agent typt zelf een
  afsluiting. Regel "Geen eigen afsluiting" ontbreekt in zijn instructies.
- **Bodytekst in ander font dan de handtekening.** De Aptos-wrapper ontbreekt.
- **Lege blokken waar plaatjes horen, of tientallen bijlagen.** Iemand heeft alsnog
  inline-bijlagen toegevoegd. Draft weggooien, opnieuw laten maken zonder
  `add-mail-attachment`.
- **400 op `create-draft-email`.** `toRecipients` staat naast `body` in plaats van erin.
