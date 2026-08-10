#!/usr/bin/env python3
"""
update_progress.py  —  Globale Claude Code Stop-hook
-----------------------------------------------------
Leest het sessietranscript en schrijft een Nederlandstalige samenvatting
naar de juiste PROGRESS.md — mét urenschatting.

v2 (2026-07-29):
- Per gewijzigd bestand wordt omhoog gezocht naar de dichtstbijzijnde
  PROGRESS.md, zodat cross-project werk vanuit één chat in de júiste
  projectlog belandt (niet alleen de cwd-log).
- Urenschatting per entry op basis van transcript-tijdstempels, bij
  meerdere projecten in één sessie naar rato van het aantal geraakte
  bestanden verdeeld. Format: "±X,X u [schatting]".
- Wijzigingen aan PROGRESS.md-bestanden zelf worden genegeerd (geen
  log-over-het-log).

v3 (2026-07-30) — drie bugs uit v2 gerepareerd:
1. Uren waren wandkloktijd (laatste minus eerste tijdstempel), dus een
   sessie die openstond tijdens een nacht of vakantie logde honderden uren
   (gemeten: ±308,5 u en ±304,75 u). Nu: ACTIEVE tijd — som van de gaten
   tussen opeenvolgende events, waarbij een gat > MAX_GAP_MIN als pauze
   geldt. Plus een harde bovengrens van MAX_SESSION_H per entry.
2. De Stop-hook vuurt per assistent-beurt, niet per sessie, en het hele
   transcript werd elke keer opnieuw gelezen. Eén document kon zo vijf keer
   geboekt worden. Nu: state per transcript (welke bestanden al gelogd zijn
   en tot welk tijdstip), en alleen nieuw werk wordt toegevoegd.
3. De fallback stuurde bestanden zónder eigen PROGRESS.md naar de log van de
   wérkmap. Daardoor belandde bijvoorbeeld werk aan deze hook zelf in een
   klantproject-log. Fallback is verwijderd: geen eigen PROGRESS.md erboven
   betekent niet loggen.

Entries worden onder een vaste marker gezet (AUTOLOG_MARKER), gescheiden van
een eventueel handmatig bijgehouden log, zodat een totaalregel niet meer
onder de auto-entries verdwijnt.

Werkt voor elk project waar `/setup-progress` eerder is gedraaid
(d.w.z. PROGRESS.md bestaat). Andere bestanden worden stilletjes overgeslagen.
"""
import datetime
import hashlib
import json
import sys
from pathlib import Path

MAX_WALK_UP = 8       # hoeveel mapniveaus omhoog we zoeken naar PROGRESS.md
MAX_GAP_MIN = 10      # gat tussen events groter dan dit = pauze, geen werk
MAX_SESSION_H = 4.0   # harde bovengrens per entry (vangnet tegen uitschieters)
STATE_DIR = Path.home() / ".claude" / "hooks" / ".progress_state"
AUTOLOG_MARKER = "<!-- autolog -->"
AUTOLOG_HEADER = "## Automatisch gelogd (nog te consolideren)"


def week_label(dt: datetime.datetime) -> str:
    MONTHS_NL = [
        "januari", "februari", "maart", "april", "mei", "juni",
        "juli", "augustus", "september", "oktober", "november", "december",
    ]
    monday = dt - datetime.timedelta(days=dt.weekday())
    return f"{monday.day} {MONTHS_NL[monday.month - 1]} {monday.year}"


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


# ---------------------------------------------------------------- state

def state_path(transcript_path: str) -> Path:
    key = hashlib.sha1(transcript_path.encode("utf-8")).hexdigest()[:16]
    return STATE_DIR / f"{key}.json"


def load_state(transcript_path: str) -> dict:
    try:
        return json.loads(state_path(transcript_path).read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {"logged_files": [], "last_ts": None}


def save_state(transcript_path: str, logged_files: set, last_ts) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        state_path(transcript_path).write_text(
            json.dumps({
                "logged_files": sorted(logged_files),
                "last_ts": last_ts.isoformat() if last_ts else None,
            }),
            encoding="utf-8",
        )
    except OSError:
        pass  # state is een optimalisatie, geen harde eis


# ---------------------------------------------------------------- extractie

def active_hours(timestamps: list) -> float:
    """Som van de gaten tussen opeenvolgende events, pauzes uitgezonderd.

    Wandkloktijd (laatste - eerste) is onbruikbaar: een sessie die 's nachts
    openstaat levert dan 17 uur 'werk'. Alleen gaten tot MAX_GAP_MIN tellen
    als aaneengesloten werk.
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
    """Verzamel gewijzigde/nieuwe bestanden en actieve tijd.

    `since` begrenst de urenberekening tot events ná het vorige logmoment,
    zodat opeenvolgende Stop-events binnen één sessie niet dezelfde tijd
    nogmaals boeken.
    """
    edited, created, messages = set(), set(), []
    timestamps, last_ts = [], None

    for ev in events:
        ts = _parse_ts(ev.get("timestamp") or ev.get("created_at") or ev.get("ts"))
        if ts:
            if last_ts is None or ts > last_ts:
                last_ts = ts
            if since is None or ts > since:
                timestamps.append(ts)

        tool_name = ev.get("toolName") or ""
        tool_input = ev.get("toolInput") or {}
        if not tool_name:
            tool = ev.get("tool") or {}
            tool_name = tool.get("name") or ""
            tool_input = tool.get("input") or {}
        # transcript-formaat met message.content tool_use-blokken
        if not tool_name:
            msg = ev.get("message") or {}
            content = msg.get("content")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        name = block.get("name") or ""
                        inp = block.get("input") or {}
                        if name == "Edit" and inp.get("file_path"):
                            edited.add(inp["file_path"])
                        elif name == "Write" and inp.get("file_path"):
                            created.add(inp["file_path"])

        if tool_name == "Edit":
            p = tool_input.get("file_path", "")
            if p:
                edited.add(p)
        elif tool_name == "Write":
            p = tool_input.get("file_path", "")
            if p:
                created.add(p)

        role = ev.get("role") or ev.get("type") or ""
        if role == "assistant":
            content = ev.get("content", "")
            if not content:
                content = (ev.get("message") or {}).get("content", "")
            if isinstance(content, str) and content.strip():
                messages.append(content.strip()[:400])
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = block.get("text", "").strip()
                        if text:
                            messages.append(text[:400])

    # PROGRESS.md-wijzigingen zelf niet loggen
    edited = {p for p in edited if Path(p).name != "PROGRESS.md"}
    created = {p for p in created if Path(p).name != "PROGRESS.md"}

    return edited, created, messages, active_hours(timestamps), last_ts


def nearest_progress(path_str: str):
    """Zoek vanaf de map van `path_str` omhoog naar de dichtstbijzijnde PROGRESS.md.

    Geen fallback naar de werkmap: een bestand zonder eigen PROGRESS.md erboven
    hoort niet in de log van een willekeurig ander project (v2-bug).
    """
    try:
        p = Path(path_str).resolve()
    except (OSError, ValueError):
        return None
    parent = p.parent
    for _ in range(MAX_WALK_UP):
        candidate = parent / "PROGRESS.md"
        try:
            if candidate.exists():
                return candidate
        except OSError:
            return None
        if parent.parent == parent:  # schijf-root bereikt
            break
        parent = parent.parent
    return None


def group_by_progress(edited: set, created: set) -> dict:
    """{progress_path: {"edited": set, "created": set}}"""
    groups: dict = {}
    for bucket, paths in (("edited", edited), ("created", created)):
        for p in paths:
            target = nearest_progress(p)
            if target is None:
                continue
            entry = groups.setdefault(target, {"edited": set(), "created": set()})
            entry[bucket].add(p)
    return groups


def fmt_hours(h: float) -> str:
    # afronden op kwartier, minimum een kwartier
    h = max(0.25, round(h * 4) / 4)
    return f"±{h:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " u"


def ai_summary(edited: set, created: set, messages: list) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic()
        context = "\n".join([
            f"Gewijzigde bestanden: {', '.join(sorted(edited)) or 'geen'}",
            f"Nieuwe bestanden:     {', '.join(sorted(created)) or 'geen'}",
            "",
            "Recente assistent-berichten (voor context):",
            *[f"  - {m}" for m in messages[-6:]],
        ])
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            messages=[{"role": "user", "content": (
                "Je output wordt LETTERLIJK in een voortgangslogbestand geschreven. "
                "Schrijf 1 tot 4 Nederlandstalige bullet points over wat er in deze "
                "Claude Code-sessie is gedaan aan de hieronder genoemde bestanden van dit "
                "project (negeer bestanden van andere projecten in de berichten-context).\n"
                "Regels: ALTIJD bullets opleveren — nooit vragen stellen, nooit disclaimers "
                "of meta-commentaar. Is de context dun, beschrijf dan op bestandsnaam-niveau "
                "('X aangemaakt', 'Y aangepast'). Formaat per regel:\n"
                "- [categorie]: beschrijving\n"
                "Categorieën: Nieuwe functie | Bugfix | Verbetering | Analyse | Documentatie\n\n"
                + context
            )}],
        )
        return resp.content[0].text.strip()
    except Exception as exc:
        lines = []
        for f in sorted(edited)[:6]:
            lines.append(f"- Verbetering: `{Path(f).name}` aangepast")
        for f in sorted(created)[:4]:
            lines.append(f"- Nieuwe functie: `{Path(f).name}` aangemaakt")
        if not lines:
            lines.append(f"- Sessie afgerond (API niet beschikbaar: {exc})")
        return "\n".join(lines)


def append_to_progress(summary: str, progress_path: Path, hours_label: str) -> None:
    """Zet de entry onder de autolog-marker, niet onderaan het bestand.

    v2 plakte entries aan het eind, waardoor ze ónder een handmatige
    totaalregel belandden en het bestand twee losse logs kreeg.
    """
    week = week_label(datetime.datetime.now())
    time_str = datetime.datetime.now().strftime("%d/%m %H:%M")
    entry = f"\n*Sessie {time_str} (week van {week})* — {hours_label} [schatting]\n{summary}\n"

    text = progress_path.read_text(encoding="utf-8")

    if AUTOLOG_MARKER in text:
        text = text.replace(AUTOLOG_MARKER, AUTOLOG_MARKER + entry, 1)
    else:
        text = (
            text.rstrip()
            + f"\n\n---\n\n{AUTOLOG_HEADER}\n{AUTOLOG_MARKER}\n{entry}"
        )

    progress_path.write_text(text, encoding="utf-8")
    print(f"[update_progress] Entry toegevoegd aan {progress_path}", file=sys.stderr)


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    if data.get("stop_hook_active"):
        sys.exit(0)

    transcript_path = data.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    state = load_state(transcript_path)
    already = set(state.get("logged_files") or [])
    since = _parse_ts(state.get("last_ts"))

    events = parse_transcript(transcript_path)
    edited, created, messages, session_h, last_ts = extract_changes(events, since=since)

    # alleen nieuw werk: wat al gelogd is voor dit transcript niet opnieuw boeken
    edited = {p for p in edited if p not in already}
    created = {p for p in created if p not in already}
    if not edited and not created:
        sys.exit(0)

    groups = group_by_progress(edited, created)
    if not groups:
        # niets loggen, maar wel bijhouden dat we deze bestanden gezien hebben
        save_state(transcript_path, already | edited | created, last_ts)
        sys.exit(0)

    total_files = sum(len(g["edited"]) + len(g["created"]) for g in groups.values()) or 1
    if not session_h:
        session_h = 0.25  # geen bruikbare tijdstempels -> conservatief kwartier

    for progress_path, group in groups.items():
        share = (len(group["edited"]) + len(group["created"])) / total_files
        hours_label = fmt_hours(session_h * share)
        summary = ai_summary(group["edited"], group["created"], messages)
        append_to_progress(summary, progress_path, hours_label)

    save_state(transcript_path, already | edited | created, last_ts)
    sys.exit(0)


if __name__ == "__main__":
    main()
