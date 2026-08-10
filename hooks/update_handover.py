#!/usr/bin/env python3
"""
update_handover.py  —  Stop-hook die HANDOVER.md automatisch laat bijwerken
---------------------------------------------------------------------------
Tegenhanger van update_progress.py. Waar die hook zelf een regel wegschrijft,
doet deze dat bewust NIET: een HANDOVER is geen logboek maar een toestand
(open punten, waar we op wachten, herstartrecept). Een Python-script kan daar
alleen een bestandslijst van maken, en dan heb je een tweede PROGRESS.md.

Daarom gebruikt deze hook het Stop-hook-blokkeermechanisme: hij geeft
{"decision": "block", "reason": "..."} terug, waarna Claude zelf de HANDOVER
bijwerkt mét de volledige sessiecontext. De volgende Stop komt binnen met
stop_hook_active=true en dan stapt de hook er meteen uit.

Gates, in volgorde — elke gate is een snelle uitstap zodat de hook alleen bij
een echte werksessie iets doet:
  1. stop_hook_active gezet            -> uit (voorkomt de lus)
  2. geen transcript                    -> uit
  3. geen nieuwe bewerkte bestanden     -> uit
  4. geen HANDOVER.md boven die bestanden -> uit (projecten zonder handover
     merken hier niets van)
  5. minder dan MIN_ACTIVE_H actieve tijd -> uit (een typfix hoort geen
     handover-ronde te veroorzaken)

Installatie: zie INSTALL.ps1. Registreert zich als Stop-hook naast
update_progress.py.
"""
import datetime
import hashlib
import json
import sys
from pathlib import Path

MAX_WALK_UP = 8        # mapniveaus omhoog zoeken naar HANDOVER.md
MAX_GAP_MIN = 10       # gat tussen events groter dan dit = pauze
MAX_SESSION_H = 4.0    # bovengrens per meting (vangnet)
MIN_ACTIVE_H = 0.25    # drempel: minder dan een kwartier werk -> niet vragen
MIN_FILES = 1          # minimaal aantal nieuwe bestanden
STATE_DIR = Path.home() / ".claude" / "hooks" / ".handover_state"

SKIP_NAMES = {"PROGRESS.md", "HANDOVER.md"}


# ---------------------------------------------------------------- transcript

def parse_transcript(path: str) -> list:
    events = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except (FileNotFoundError, OSError):
        pass
    return events


def _parse_ts(value):
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def active_hours(timestamps: list) -> float:
    """Actieve tijd: som van de gaten tussen events, pauzes uitgezonderd.

    Zelfde aanpak als update_progress.py v3. Wandkloktijd is onbruikbaar —
    een sessie die 's nachts openstaat levert anders zeventien uur 'werk'.
    """
    ts = sorted(t for t in timestamps if t)
    if len(ts) < 2:
        return 0.0
    max_gap_h = MAX_GAP_MIN / 60.0
    total = 0.0
    for a, b in zip(ts, ts[1:]):
        gap = (b - a).total_seconds() / 3600.0
        if 0 < gap <= max_gap_h:
            total += gap
    return min(total, MAX_SESSION_H)


def extract_changes(events: list, since=None):
    """Bewerkte/nieuwe bestanden en actieve tijd sinds het vorige logmoment."""
    touched = set()
    timestamps, last_ts = [], None

    for ev in events:
        ts = _parse_ts(ev.get("timestamp") or ev.get("created_at") or ev.get("ts"))
        if ts:
            if last_ts is None or ts > last_ts:
                last_ts = ts
            if since is None or ts > since:
                timestamps.append(ts)

        msg = ev.get("message") or {}
        content = msg.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    name = block.get("name") or ""
                    inp = block.get("input") or {}
                    if name in ("Edit", "Write", "NotebookEdit") and inp.get("file_path"):
                        touched.add(inp["file_path"])

        # ouder transcriptformaat
        tool_name = ev.get("toolName") or ""
        tool_input = ev.get("toolInput") or {}
        if tool_name in ("Edit", "Write") and tool_input.get("file_path"):
            touched.add(tool_input["file_path"])

    touched = {p for p in touched if Path(p).name not in SKIP_NAMES}
    return touched, active_hours(timestamps), last_ts


# ---------------------------------------------------------------- state

def state_path(transcript_path: str) -> Path:
    key = hashlib.sha1(transcript_path.encode("utf-8")).hexdigest()[:16]
    return STATE_DIR / f"{key}.json"


def load_state(transcript_path: str) -> dict:
    try:
        return json.loads(state_path(transcript_path).read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {"prompted_files": [], "last_ts": None}


def save_state(transcript_path: str, prompted: set, last_ts) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        state_path(transcript_path).write_text(
            json.dumps({
                "prompted_files": sorted(prompted),
                "last_ts": last_ts.isoformat() if last_ts else None,
            }),
            encoding="utf-8",
        )
    except OSError:
        pass  # state is een optimalisatie, geen harde eis


# ---------------------------------------------------------------- handover

def nearest_handover(path_str: str):
    """Dichtstbijzijnde HANDOVER.md boven dit bestand.

    Geen fallback naar de werkmap: een bestand zonder eigen HANDOVER.md erboven
    hoort niet in de handover van een willekeurig ander project te belanden.
    Dat was bug 3 in update_progress.py v2 en die maken we hier niet opnieuw.
    """
    try:
        p = Path(path_str).resolve()
    except (OSError, ValueError):
        return None
    parent = p.parent
    for _ in range(MAX_WALK_UP):
        candidate = parent / "HANDOVER.md"
        try:
            if candidate.exists():
                return candidate
        except OSError:
            return None
        if parent.parent == parent:
            break
        parent = parent.parent
    return None


def group_by_handover(touched: set) -> dict:
    groups: dict = {}
    for p in touched:
        target = nearest_handover(p)
        if target is None:
            continue
        groups.setdefault(target, set()).add(p)
    return groups


def build_reason(groups: dict, hours: float) -> str:
    vandaag = datetime.date.today().isoformat()
    uren_nl = f"{hours:.2f}".replace(".", ",")  # alleen het getal, niet de zin
    regels = [
        "Voordat deze sessie eindigt: werk de HANDOVER.md bij van de projecten waaraan "
        "gewerkt is. Dit gebeurt automatisch aan het eind van elke werksessie — de "
        "gebruiker hoeft er niet om te vragen en heeft er ook niet om gevraagd.",
        "",
        f"Datum: {vandaag}. Geschatte actieve tijd deze sessie: {uren_nl} u.",
        "",
        "Bij te werken bestanden:",
    ]
    for handover_path, files in sorted(groups.items(), key=lambda kv: str(kv[0])):
        namen = sorted(Path(f).name for f in files)
        toon = ", ".join(namen[:8]) + (f" (+{len(namen) - 8} meer)" if len(namen) > 8 else "")
        regels.append(f"- {handover_path}  — geraakt: {toon}")

    regels += [
        "",
        "Houd de bestaande kopstructuur aan en respecteer per sectie de bedoeling:",
        "",
        "- **Waar we gebleven zijn** — VERVANG de inhoud. Twee tot vijf zinnen: wat is de "
        "stand, wat was de laatste stap, wat is de eerstvolgende.",
        "- **Open punten** — werk de checkboxlijst bij. Vink af wat af is (`- [x]` met "
        "datum), voeg toe wat nieuw is. Maak geen duplicaten van punten die er al staan.",
        "- **Waar we op wachten** — wat, van wie, sinds wanneer. Haal weg wat binnen is.",
        "- **Herstartrecept** — alleen bijwerken als er iets veranderd is aan hoe je dit "
        "project draaiend krijgt (commando's, poorten, branches, namen van "
        "omgevingsvariabelen). Nooit sleutels of wachtwoorden opnemen.",
        "- **Lessons learned** — alleen aanvullen, nooit vervangen, en alleen als er echt "
        "iets geleerd is dat je een tweede keer zou laten struikelen.",
        "",
        "Regels: HANDOVER is intern, maar de taalregel geldt onverkort — schrijf niet "
        "\"af\", \"werkt\", \"gevalideerd\", \"opgelost\" of \"production-ready\" zonder dat de "
        "klant dat bevestigd heeft. Schrijf in het Nederlands. Verzin niets: staat iets "
        "niet vast, noteer het als open punt.",
        "",
        "Bestaat een van de genoemde bestanden niet meer, sla dat bestand dan over. "
        "Rond daarna gewoon af met een korte melding van wat je hebt bijgewerkt — geen "
        "uitgebreide samenvatting.",
    ]
    return "\n".join(regels)


# ---------------------------------------------------------------- main

def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    # Gate 1 — wij hebben deze beurt al geblokkeerd; niet nog een keer.
    if data.get("stop_hook_active"):
        sys.exit(0)

    # Gate 2 — zonder transcript valt er niets vast te stellen.
    transcript_path = data.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    state = load_state(transcript_path)
    prompted = set(state.get("prompted_files") or [])
    since = _parse_ts(state.get("last_ts"))

    events = parse_transcript(transcript_path)
    touched, hours, last_ts = extract_changes(events, since=since)

    # Gate 3 — alleen bestanden waar we nog niet over gevraagd hebben.
    nieuw = {p for p in touched if p not in prompted}
    if len(nieuw) < MIN_FILES:
        sys.exit(0)

    # Gate 4 — geen HANDOVER.md in de buurt: stil overslaan.
    groups = group_by_handover(nieuw)
    if not groups:
        save_state(transcript_path, prompted | nieuw, last_ts)
        sys.exit(0)

    # Gate 5 — te weinig werk om een handover-ronde te rechtvaardigen.
    if hours < MIN_ACTIVE_H:
        save_state(transcript_path, prompted | nieuw, last_ts)
        sys.exit(0)

    # Markeer vóór het blokkeren: mocht Claude niets doen, dan vragen we het
    # niet eindeloos opnieuw voor dezelfde bestanden.
    save_state(transcript_path, prompted | nieuw, last_ts)

    # ensure_ascii=True is hier geen stijlkeuze maar een bugfix: op Windows
    # schrijft Python standaard cp1252 naar stdout, waardoor een em-dash in de
    # instructie ongeldige UTF-8 oplevert en de JSON onleesbaar wordt voor wie
    # hem uitleest. ASCII-only JSON is byte-identiek onder elke console-codering.
    print(json.dumps({
        "decision": "block",
        "reason": build_reason(groups, hours),
    }, ensure_ascii=True))
    sys.exit(0)


if __name__ == "__main__":
    main()
