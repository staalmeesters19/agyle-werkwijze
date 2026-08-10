---
name: mail
description: Zet in één keer een schone, ondertekende Outlook-conceptmail namens Abdul klaar (nieuwe mail of reply) — Agyle-handtekening via gehoste afbeeldingen, nooit verzonden. Gebruik wanneer Abdul "mail naar X over Y", "stuur een mailtje", "reply op die thread" o.i.d. vraagt. Vervangt het handmatige mail-klaarzetten.
allowed-tools: Read, ToolSearch, mcp__ms365__create-draft-email, mcp__ms365__create-reply-draft, mcp__ms365__create-reply-all-draft, mcp__ms365__update-mail-message, mcp__ms365__list-users, mcp__ms365__list-mail-messages, mcp__ms365__list-mail-folder-messages, mcp__ms365__get-mail-message, mcp__ms365__list-outlook-contacts
---

# Skill: `/mail` — schone ondertekende Outlook-conceptmail

**Aanroep:** `/mail <aan wie> — <waar gaat het over>`
Voorbeelden: `/mail Joris — even bijpraten deze week`, `/mail Cornée van Ende — FDS-status, vraag of hosting-migratie akkoord is`, `/mail reply op de laatste van Jos over de factuur`.

Doel: binnen één beurt een verzendklare **concept**mail in Outlook, met Abdul's handtekening correct erboven. **Nooit verzenden** (`Mail.Send` verboden) — Abdul reviewt en verstuurt zelf.

## Kernregels (niet-onderhandelbaar)

1. **Handtekening = gehoste-URL-blok, GEEN bijlagen.** Lees `~/.claude/assets/agyle-signature-url.html` en plak dat één-op-één onderaan de body. Roep **nooit** `add-mail-attachment` aan. (Waarom: inline-cid-plaatjes worden door OWA gedupliceerd/verminkt — zie CLAUDE.md.)
2. **Body-HTML:** losse regels als `<div>…</div>`, witregels als expliciete `<div><br></div>`. Géén `<p>` (OWA plet alinea's), géén platte tekst met `\n` (collapsen).
   **Font = Aptos, verplicht.** Wikkel de complete bodytekst (alles vóór het handtekeningblok) in één wrapper: `<div style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)"> …body-divs… </div>`. Zonder deze wrapper rendert de body bij ontvangers in Times New Roman terwijl de handtekening in Aptos staat — dat mag nooit.
3. **Geen eigen afsluiting** in de bodytekst. Het handtekeningblok bevat al "Met vriendelijke groet, / Abdul Malik". Laatste bodyzin = de laatste inhoudelijke zin.
4. **Taal/toon:** Nederlands tenzij de thread/ontvanger Engels is. Kort en zakelijk, geen opgeklopte inleiding, underpromise/overdeliver richting klant.
5. **Nooit een afbeelding-base64 door een tool-call duwen.** De plaatjes zijn al gehost; de skill raakt geen base64 aan.

## Stappen

**1 — Ontvanger + adres bepalen. NOOIT om een adres vragen dat je zelf kunt opzoeken — zoeken is de reflex, vragen is het laatste redmiddel.**
- E-mailadres bekend/genoemd → gebruik dat.
- Alleen een naam (ook een informele/roepnaam als "Quirijn", "Cornée") → zélf resolven, in deze volgorde tot je een treffer hebt:
  1. `list-mail-messages` (`$search="<naam>"`) — vindt het adres in een recente thread; werkt ook voor externe contacten. Meestal de snelste treffer.
  2. `list-users` (`$search="displayName:<naam>"`, header ConsistencyLevel: eventual) — voor interne Agyle-collega's.
  3. `list-outlook-contacts` (`$search="<naam>"`) — persoonlijke contacten buiten de directory.
- Nooit een adres verzinnen; nooit stoppen en om het adres vragen zolang bovenstaande nog niet geprobeerd is.
- Blijft het na zoeken écht ambigu (meerdere personen met die naam) → één korte keuzevraag, anders doorgaan.

**2 — Inhoud opstellen.** Korte NL-mail conform de toon-regels. Als de taak klantstrategie/prijzen raakt: eerst de klantcontext uit de klantmap lezen vóór je schrijft (zie CLAUDE.md "Verifieer vóór uitvoeren"). Bij twijfel over kernboodschap: één scherpe vraag.

**3a — Nieuwe mail:** `create-draft-email`. **Payload-valkuil:** de tool heeft één top-level parameter `body` die het héle message-object is — nest `subject`, `toRecipients` (+ evt. `ccRecipients`) én de eigenlijke mailbody dáárbinnen. Dus: `body = { subject, toRecipients:[{emailAddress:{address,name}}], body: { contentType:"html", content: [Aptos-wrapper met bodytekst-divs] + [inhoud van agyle-signature-url.html] } }`. `toRecipients` op het top-level meegeven → `400 … toRecipients … does not match schema`. Eén call, klaar. Geen bijlagen.

**3b — Reply / reply-all:** `create-reply-draft` of `create-reply-all-draft` op het juiste bericht, met `Comment` = [Aptos-wrapper met reply-tekst-divs] + [`agyle-signature-url.html`-blok]. Zet CC's zo nodig opnieuw (`ccRecipients` overschrijft de hele lijst). Reply-all faalt op een eigen verzonden bericht → wijk uit naar het laatste bericht van de tegenpartij in dezelfde thread.

**4 — Rapporteer:** onderwerp, ontvanger(s), en dat de draft klaarstaat en niet is verzonden. Eén regel. Geen base64/HTML in de terugkoppeling.

## Handtekening-feiten (voor referentie)
- Plaatjes: `https://agyle-email-assets.vercel.app/{logo,blok,booking}.png` (Vercel-project `agyle-email-assets`, team `staals-projects`). Logo is een compacte palet-PNG (< 1KB). Niet weggooien.
- Externe-afbeeldingen-caveat: sommige externe ontvangers moeten afbeeldingen één keer "tonen"; intern laadt het direct.
- Wil je later een nette bron i.p.v. `vercel.app`: plaatjes onder een subdomein van `agyle.nl` zetten en de URL's in `agyle-signature-url.html` aanpassen.
