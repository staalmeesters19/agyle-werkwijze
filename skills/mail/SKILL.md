---
name: mail
description: Zet in één keer een schone, ondertekende Outlook-conceptmail klaar (nieuwe mail of reply) — Agyle-handtekening via gehoste afbeeldingen, nooit verzonden. Gebruik wanneer de gebruiker "mail naar X over Y", "stuur een mailtje", "reply op die thread" o.i.d. vraagt. Vervangt het handmatige mail-klaarzetten.
allowed-tools: Read, ToolSearch, mcp__ms365__create-draft-email, mcp__ms365__create-reply-draft, mcp__ms365__create-reply-all-draft, mcp__ms365__update-mail-message, mcp__ms365__list-users, mcp__ms365__list-mail-messages, mcp__ms365__list-mail-folder-messages, mcp__ms365__get-mail-message, mcp__ms365__list-outlook-contacts
---

# Skill: `/mail` — schone ondertekende Outlook-conceptmail

**Aanroep:** `/mail <aan wie> — <waar gaat het over>`
Voorbeelden: `/mail Joris — even bijpraten deze week`, `/mail Cornée Fokkema — FDS-status, vraag of hosting-migratie akkoord is`, `/mail reply op de laatste van Jos over de factuur`.

Doel: binnen één beurt een verzendklare **concept**mail in Outlook, met de handtekening van de
gebruiker correct eronder. **Nooit verzenden** (`Mail.Send` verboden) — de gebruiker reviewt en
verstuurt zelf.

## Kernregels (niet-onderhandelbaar)

1. **Handtekening = gehoste-URL-blok, GEEN bijlagen.** Lees `~/.claude/assets/agyle-signature-url.html` en plak dat één-op-één onderaan de body. Roep **nooit** `add-mail-attachment` aan. (Waarom: inline-cid-plaatjes worden door OWA gedupliceerd/verminkt.) Dat bestand is per persoon gegenereerd door `INSTALL.ps1` en bevat de naam, het mailadres en de boekingslink van de huidige gebruiker. Ontbreekt het: stop en meld dat `INSTALL.ps1` nog moet draaien — verzin nooit zelf een handtekening.
2. **Body-HTML:** losse regels als `<div>…</div>`, witregels als expliciete `<div><br></div>`. Géén `<p>` (OWA plet alinea's), géén platte tekst met `\n` (collapsen).
   **Font = Aptos, verplicht.** Wikkel de complete bodytekst (alles vóór het handtekeningblok) in één wrapper: `<div style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)"> …body-divs… </div>`. Zonder deze wrapper rendert de body bij ontvangers in Times New Roman terwijl de handtekening in Aptos staat — dat mag nooit.
3. **Geen eigen afsluiting** in de bodytekst. Het handtekeningblok bevat al "Met vriendelijke groet," plus de naam van de afzender. Laatste bodyzin = de laatste inhoudelijke zin.
4. **Taal:** Nederlands tenzij de thread of de ontvanger Engels is. Voor toon en lengte geldt het blok hieronder — dat is bindend, niet adviserend.
5. **Nooit een afbeelding-base64 door een tool-call duwen.** De plaatjes zijn al gehost; de skill raakt geen base64 aan.

## Toon en lengte (bindend — hier wordt op afgerekend)

Deze regels komen uit echte kritiek: onze mails waren te lang en voelden AI-geschreven. De
tegenpartij schrijft vier regels, wij schreven er twintig. Hieronder staat het antwoord daarop.

### Woordplafond, exclusief handtekening

| Soort mail | Max |
|---|---|
| Iets doorsturen, bevestigen, akkoord geven | **40 woorden** |
| Een vraag stellen of iets opvragen | **80 woorden** |
| Voorstel, toelichting, meerdere punten | **150 woorden** — meer dan dat wordt een bijlage of een belafspraak |

Tel ze. Zit je erboven, schrap; herschrijf niet.

### Structuur

- **Vraag of verzoek in de eerste zin.** Geen aanloop, geen context vooraf. Context komt eronder, als
  die er al moet zijn.
- **Geen samenvattende slotalinea.** Laatste zin is de laatste inhoudelijke zin.
- Meerdere punten → korte streepjes, niet uitgeschreven alinea's.
- Eén mail, één onderwerp. Twee onderwerpen zijn twee mails.

### Verboden (harde lijst)

- **Het kastlijntje `—`.** Nooit. Gebruik een komma, een dubbele punt, of een nieuwe zin. Dit is de
  sterkste AI-verklikker in Nederlandse zakelijke mail.
- **Drieslagen.** "Niet A, niet B, niet C." Ritmische opsommingen van drie zijn een machinehandtekening.
- **Signaalzinnen.** "Voor de goede orde", "kort samengevat", "twee dingen die jou raken", "daarnaast",
  "tot slot", "hierbij het volgende".
- **Gepolijste afsluiters.** "Horen graag of dit zo werkt", "dan scherpen wij het aan", "ik hoor graag
  je gedachten". Vervang door "laat maar weten", of laat weg.
- **Schrijftaal.** Geen "wij" waar "we" kan, geen "reeds", "middels", "derhalve", "aangaande".
- **Uitleg die de ontvanger al weet.** Een HR-manager weet wat een loonheffingsformulier is.

### Wel doen

- Aanspreken met "Hoi <voornaam>," — "Beste" alleen bij formele externe eerste contacten.
- Halve zinnen mogen. "Klopt." "Prima zo." "Zie bijlage."
- Eén directe vraag is beter dan drie beleefde.
- Bijlagen benoemen in vier woorden, niet in een alinea.

### IJkpunt vóór opslaan

Lees de mail terug en vraag: **zou een ervaren zakelijke correspondent het zo schrijven?** Die
schrijven "Zie bijlage met mijn opmerkingen. Daar kunnen we echt wel iets beters van maken." en "Wil
je deze even nakijken en bij akkoord door Remko laten tekenen?" Meer is het niet. Haalt jouw versie
dat niet, schrap dan tot het wel zo is.

## Stappen

**1 — Ontvanger + adres bepalen. NOOIT om een adres vragen dat je zelf kunt opzoeken — zoeken is de reflex, vragen is het laatste redmiddel.**
- E-mailadres bekend/genoemd → gebruik dat.
- Alleen een naam (ook een informele roepnaam als "Quirijn", "Cornée") → zélf resolven, in deze volgorde tot je een treffer hebt:
  1. `list-mail-messages` (`$search="<naam>"`) — vindt het adres in een recente thread; werkt ook voor externe contacten. Meestal de snelste treffer.
  2. `list-users` (`$search="displayName:<naam>"`, header ConsistencyLevel: eventual) — voor interne Agyle-collega's.
  3. `list-outlook-contacts` (`$search="<naam>"`) — persoonlijke contacten buiten de directory.
- Nooit een adres verzinnen; nooit stoppen en om het adres vragen zolang bovenstaande nog niet geprobeerd is.
- Blijft het na zoeken écht ambigu (meerdere personen met die naam) → één korte keuzevraag, anders doorgaan.

**2 — Inhoud opstellen.** Volg het blok "Toon en lengte" hierboven letterlijk: woorden tellen, verzoek
in de eerste zin, geen kastlijntjes, geen signaalzinnen, geen slotalinea. Raakt de mail klantstrategie
of prijzen, lees dan eerst de klantcontext uit de klantmap voordat je schrijft — en houd je aan de
regel dat er geen tarieven in klant-facing berichten staan (zie `docs/02-WERKWIJZE.md` regel 4). Bij
twijfel over de kernboodschap: één scherpe vraag aan de gebruiker, geen aannames in de mail verwerken.

Vóór het aanmaken van de draft: lees je eigen tekst één keer terug en schrap alles wat de ontvanger al
weet of niet nodig heeft om te antwoorden. Bijna altijd kan er nog een derde af.

**3a — Nieuwe mail:** `create-draft-email`. **Payload-valkuil:** de tool heeft één top-level parameter `body` die het héle message-object is — nest `subject`, `toRecipients` (+ evt. `ccRecipients`) én de eigenlijke mailbody dáárbinnen. Dus: `body = { subject, toRecipients:[{emailAddress:{address,name}}], body: { contentType:"html", content: [Aptos-wrapper met bodytekst-divs] + [inhoud van agyle-signature-url.html] } }`. `toRecipients` op het top-level meegeven → `400 … toRecipients … does not match schema`. Eén call, klaar. Geen bijlagen.

**3b — Reply / reply-all:** `create-reply-draft` of `create-reply-all-draft` op het juiste bericht, met `Comment` = [Aptos-wrapper met reply-tekst-divs] + [`agyle-signature-url.html`-blok]. Zet CC's zo nodig opnieuw (`ccRecipients` overschrijft de hele lijst). Reply-all faalt op een eigen verzonden bericht → wijk uit naar het laatste bericht van de tegenpartij in dezelfde thread.

**4 — Rapporteer:** onderwerp, ontvanger(s), en dat de draft klaarstaat en niet is verzonden. Eén regel. Geen base64/HTML in de terugkoppeling.

## Handtekening-feiten (voor referentie)

- De handtekening is per persoon: `INSTALL.ps1` genereert `~/.claude/assets/agyle-signature-url.html` uit `config/persoon.json`. Klopt er iets niet aan je naam, functie of boekingslink, pas dan `persoon.json` aan en draai `INSTALL.ps1` opnieuw. Bewerk het gegenereerde bestand niet met de hand.
- Plaatjes: `https://agyle-email-assets.vercel.app/{logo,blok,booking}.png` (Vercel-project `agyle-email-assets`, team `staals-projects`). Deze zijn voor iedereen gelijk. Het logo is een compacte palet-PNG onder 1 KB. Niet weggooien.
- Externe-afbeeldingen-caveat: sommige externe ontvangers moeten afbeeldingen één keer "tonen"; intern laadt het direct.
- Wil je later een nette bron in plaats van `vercel.app`: zet de plaatjes onder een subdomein van `agyle.nl` en pas de URL's aan in `templates/agyle-signature-url.template.html`.
