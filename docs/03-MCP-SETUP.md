# MCP-servers opzetten

MCP-servers zijn de koppelingen tussen Claude Code en de systemen waar wij mee werken:
je mailbox, de agenda, het CRM, GitHub. Zonder deze stap werken `/mail`, `/notulen` en
`/briefing` niet of maar half.

Reken op een half uur, vooral door de inlogschermen. Je doet dit één keer.

> **Alles op `--scope user`.** Dan staan de servers in elk project tot je beschikking en
> hoef je dit niet per klantmap te herhalen.

---

## Volgorde

Begin met `chrome-devtools` (geen inloggedoe, meteen resultaat — goede controle dat het
mechanisme werkt), dan `ms365` (het meeste werk), dan de rest.

## 1. chrome-devtools — geen authenticatie

```bash
claude mcp add --scope user --transport stdio chrome-devtools -- cmd /c npx -y chrome-devtools-mcp@latest
```

Laat Claude een browser aansturen: pagina's openen, screenshots maken, netwerkverkeer
bekijken. Gebruikt bij demo's en bij het controleren van opgeleverde websites.

## 2. ms365 — je Agyle-mailbox en agenda

Dit is de belangrijkste. Vraag Abdul om de `CLIENT_ID` en `TENANT_ID` van de Agyle
Entra-app; die zijn voor iedereen gelijk. De twee padvariabelen zijn **per persoon** —
zet ze op een pad in je eigen profiel, want twee mensen op hetzelfde pad delen elkaars
mailboxtoken.

```bash
claude mcp add --scope user --transport stdio ms365 \
  --env MS365_MCP_CLIENT_ID=<vraag Abdul> \
  --env MS365_MCP_TENANT_ID=<vraag Abdul> \
  --env MS365_MCP_TOKEN_CACHE_PATH=C:\Users\<jij>\.claude\.ms365-token-cache.json \
  --env MS365_MCP_SELECTED_ACCOUNT_PATH=C:\Users\<jij>\.claude\.ms365-account.json \
  -- npx -y @softeria/ms-365-mcp-server --org-mode
```

Daarna in Claude Code: roep de `login`-tool van ms365 aan en volg de apparaatcode-flow in
je browser. Controleer met `verify-login` en `get-current-user` dat je je eigen account
ziet.

> **Nooit `Mail.Send`.** Wij zetten concepten klaar en versturen ze handmatig. Zie
> [`05-VEILIGHEID.md`](05-VEILIGHEID.md).

## 3. agyle — het CRM

```bash
claude mcp add --scope user --transport http agyle https://agyle-crm-epfvguhbgwccevga.westeurope-01.azurewebsites.net/api/mcp
```

Hier boek je je uren en vind je projecten, deals en contactpersonen. De server doet bij
sessiestart automatisch een controle op wie je bent en welke rechten je hebt. Vraag Abdul
om een account als je nog geen login hebt.

## 4. github — repositories, PR's, issues

```bash
claude mcp add --scope user --transport http github https://api.githubcopilot.com/mcp/
```

Authenticeren met **je eigen** Personal Access Token. Belangrijk: bij Agyle lopen alle
GitHub-acties via deze MCP, niet via de `gh`-commandline (die staat niet geïnstalleerd).
Lokale git-commando's — `commit`, `push`, `branch`, `checkout` — doe je gewoon in de
terminal; dat is werkkopiebeheer, geen GitHub-API.

## 5. plaud — vergaderopnames

```bash
claude mcp add --scope user --transport http plaud https://mcp.plaud.ai/mcp
```

Hier komen de opnames vandaan die `/notulen` verwerkt.

> ⚠️ **Let op:** een eigen Plaud-account ziet alleen je eigen opnames. Wil je meetings
> verwerken die Abdul heeft opgenomen, dan moet hij die delen of moet je op zijn account
> werken. Bespreek dit vóórdat je je eerste notulen moet maken. Zonder Plaud werkt
> `/notulen` alleen via de losse-audiobestand-route, en daar heb je een eigen
> AssemblyAI-key voor nodig.

## 6. vercel en supabase — alleen als je aan websites of apps werkt

```bash
claude mcp add --scope user --transport http vercel https://mcp.vercel.com
claude mcp add --scope user --transport http supabase https://mcp.supabase.com/mcp
```

Sla over tot je ze nodig hebt.

---

## Controleren

```bash
claude mcp list
```

Of open `/mcp` in Claude Code voor de status per server. Servers die op authenticatie
wachten zie je daar meteen. `VALIDATE.ps1` controleert of de servers geconfigureerd zijn,
maar kan niet zien of je ingelogd bent — dat doe je met `/mcp`.

## Wat persoonsgebonden is

| Server | Eigen login nodig? |
|---|---|
| ms365 | ja — eigen mailbox, eigen tokencache-pad |
| agyle CRM | ja — eigen gebruiker met eigen rol |
| github | ja — eigen PAT |
| plaud | ja — eigen account, ziet andermans opnames niet |
| vercel, supabase | eigen login, gedeelde resources |
| chrome-devtools | nee, draait lokaal |

## Als een server niet verbindt

Kijk eerst in `/mcp` — daar staat de foutmelding. Meestal is het een verlopen login
(opnieuw inloggen) of ontbreekt `npx` (Node.js installeren). Blijft het hangen: vraag
Abdul, en plak de melding uit `/mcp` erbij.
