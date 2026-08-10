# -*- coding: utf-8 -*-
"""build_contract_pdf.py — markdown onderhoudscontract -> Agyle-branded PDF.

Zelfde template/opmaak als het FDS-onderhoudscontract (Van den Pol, juli 2026):
accentbalk, logo rechtsboven, meta-tabel, genummerde artikel-badges, zwarte
tabelkoppen, callout-boxen, twee-koloms ondertekenblok en Agyle-footer.

Geen pip-dependencies: eigen mini-markdown-parser + headless Edge/Chrome voor
de PDF-render.

Gebruik:
    python build_contract_pdf.py "Onderhoudscontract - Klant - Dienst.md"
    python build_contract_pdf.py contract.md -o "contract (concept).pdf"
    python build_contract_pdf.py body.html -o out.pdf     # escape hatch, zie README

Markdown-conventies (zie ../reference/contract-structuur.md):
    # Titel                          -> koptitel linksboven
    **Ondertitel:** ...              -> subtitel onder de titel (optioneel)
    **Betreft:** / **Datum:** / ...  -> meta-tabel (alles tot de eerste ---)
    ---                              -> einde meta-blok
    ## 3. Onderhoudspakketten        -> artikel met genummerde badge
    ### Subkop                       -> subkop binnen een artikel
    | a | b |                        -> tabel (zwarte kop, zebra)
    - punt                           -> bullet
    **Binnen het pakket:**           -> vetgedrukte tussenregel (lead)
    :::teal ... :::                  -> opvallende box (advies / ter overweging)
    :::box ... :::  of  > ...        -> rustige box (voorwaarde / toelichting)
    tabel met kop | Te leveren door | Te leveren aan |  -> ondertekenblok
"""

import argparse
import html as html_mod
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGO_CANDIDATES = [
    HERE.parent / "assets" / "logo_base64.txt",
    Path.home() / ".claude" / "skills" / "_agyle_branding" / "logo_base64.txt",
]

BROWSER_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/microsoft-edge",
    "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

CSS = """
@page { size: A4; margin: 18mm 20mm 22mm 20mm; }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif; font-size:10.5pt;
       line-height:1.6; color:#1a1a1a; background:#fff; }
.accent-bar { width:100%; height:4px;
       background:linear-gradient(90deg,#7ec8e3 0%,#000 100%); margin-bottom:18px; }
.header { display:flex; justify-content:space-between; align-items:flex-start;
       padding-bottom:14px; border-bottom:3px solid #000; margin-bottom:14px; }
.header-left h1 { font-size:19pt; font-weight:700; color:#000; letter-spacing:-0.5px; }
.header-left .subtitle { font-size:11pt; color:#555; margin-top:2px; }
.header-right img { height:38px; width:auto; }
.meta { font-size:10pt; color:#333; margin-bottom:18px; }
.meta table { border-collapse:collapse; }
.meta td { padding:2px 10px 2px 0; vertical-align:top; }
.meta td.k { color:#888; font-weight:600; white-space:nowrap; }
.aanhef { margin-bottom:6px; }
h2 { font-size:14pt; font-weight:700; color:#000; margin-top:24px; margin-bottom:12px;
       padding-bottom:6px; border-bottom:2px solid #7ec8e3; page-break-after:avoid; }
h3 { font-size:11.5pt; font-weight:700; color:#000; margin-top:16px; margin-bottom:6px;
       page-break-after:avoid; }
.section-number { display:inline-block; background:#000; color:#7ec8e3; font-size:10.5pt;
       font-weight:700; width:26px; height:26px; line-height:26px; text-align:center;
       border-radius:4px; margin-right:9px; vertical-align:middle; }
p { margin-bottom:9px; }
ul { margin-left:20px; margin-bottom:11px; }
ul li { margin-bottom:5px; }
.lead { font-weight:600; color:#000; margin-top:6px; margin-bottom:4px; }
table.price { width:100%; border-collapse:collapse; margin:8px 0 14px 0; font-size:10pt;
       page-break-inside:avoid; }
table.price th { background:#000; color:#7ec8e3; text-align:left; padding:8px 12px; font-weight:700; }
table.price td { border:1px solid #e0e0e0; padding:8px 12px; }
table.price tr:nth-child(even) td { background:#f7fbfd; }
.box { border:1px solid #e0e0e0; border-left:4px solid #000; padding:12px 16px;
       margin:12px 0 16px 0; background:#fafafa; font-size:10pt; page-break-inside:avoid; }
.box strong { color:#000; }
.box-teal { border:2px solid #000; background:#f7fbfd; padding:14px 18px; margin:14px 0;
       page-break-inside:avoid; }
.sign { display:flex; gap:20px; margin-top:22px; page-break-inside:avoid; }
.sign .col { flex:1; border:1px solid #999; padding:14px 16px; min-height:150px; }
.sign .col .label { font-weight:700; color:#000; margin-bottom:14px; }
.sign .col .row { color:#555; margin-bottom:22px; }
.sign .col .name { font-weight:700; color:#000; margin-top:8px; }
.sign .col .role { font-style:italic; color:#333; font-size:9.5pt; }
.sign .col .addr { color:#777; font-size:9pt; margin-top:6px; line-height:1.4; }
.footer { margin-top:40px; padding-top:12px; border-top:2px solid #000; font-size:9pt;
       color:#888; display:flex; justify-content:space-between; }
.footer-brand { font-weight:600; color:#555; letter-spacing:2px; }
"""

SIGN_HEADERS = ("te leveren door", "te leveren aan")
BLOCK_STARTS = ("#", "|", "- ", "* ", ">", ":::", "---")


# --------------------------------------------------------------------------- #
# markdown -> html
# --------------------------------------------------------------------------- #

def inline(text: str) -> str:
    """Escape HTML, dan **vet**, *cursief* en `code` terugzetten."""
    out = html_mod.escape(text, quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = out.replace("&lt;br&gt;", "<br>").replace("&lt;br/&gt;", "<br>")
    return out


def is_block_start(stripped: str) -> bool:
    return any(stripped.startswith(p) for p in BLOCK_STARTS)


def split_row(row: str) -> list:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def is_separator_row(row: str) -> bool:
    return bool(re.fullmatch(r"[\s|:\-]+", row.strip())) and "-" in row


def render_sign_block(header: list, rows: list) -> str:
    """Twee-koloms ondertekenblok uit een | Te leveren door | Te leveren aan |-tabel."""
    cols = []
    for idx, label in enumerate(header):
        parts = [f'<div class="label">{inline(label)}</div>']
        for row in rows:
            cell = row[idx] if idx < len(row) else ""
            if not cell:
                continue
            if re.match(r"^(datum|handtekening|naam|functie)\s*:", cell, re.I):
                parts.append(f'<div class="row">{inline(cell)}</div>')
                continue
            name_match = re.match(r"^\*\*(.+?)\*\*\s*[—–-]\s*(.+)$", cell)
            if name_match:
                parts.append(f'<div class="name">{inline(name_match.group(1))}</div>')
                parts.append(f'<div class="role">{inline(name_match.group(2))}</div>')
                continue
            if cell.startswith("**") and cell.endswith("**"):
                parts.append(f'<div class="name">{inline(cell.strip("*"))}</div>')
                continue
            company, _, address = cell.partition(",")
            addr = inline(company.strip())
            if address.strip():
                addr += "<br>" + inline(address.strip())
            parts.append(f'<div class="addr">{addr}</div>')
        cols.append('<div class="col">' + "".join(parts) + "</div>")
    return '<div class="sign">' + "".join(cols) + "</div>"


def render_table(raw_rows: list) -> str:
    rows = [split_row(r) for r in raw_rows if not is_separator_row(r)]
    if not rows:
        return ""
    header, body = rows[0], rows[1:]
    if [h.lower().strip("*") for h in header] == list(SIGN_HEADERS):
        return render_sign_block(header, body)
    out = ['<table class="price">']
    out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr>")
    for row in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
    out.append("</table>")
    return "".join(out)


def parse_head(lines: list) -> tuple:
    """Titel, ondertitel, meta-paren; retourneert ook de index waar de body begint."""
    i, n = 0, len(lines)
    title, subtitle, meta = "", "", []

    while i < n and not lines[i].strip():
        i += 1
    if i < n and lines[i].startswith("# "):
        title = lines[i][2:].strip()
        i += 1

    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s == "---":
            i += 1
            break
        m = re.fullmatch(r"\*\*(.+?):\*\*\s*(.*)", s)
        if not m:
            break
        key, value = m.group(1).strip(), m.group(2).strip()
        if key.lower() in ("ondertitel", "subtitel", "subtitle"):
            subtitle = value
        else:
            meta.append((key, value))
        i += 1

    return title, subtitle, meta, i


def render_body(lines: list) -> str:
    out, i, n = [], 0, len(lines)
    seen_heading = False
    first_paragraph = True

    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue

        if s.startswith(":::"):
            kind = s[3:].strip().lower()
            buf = []
            i += 1
            while i < n and lines[i].strip() != ":::":
                buf.append(lines[i].strip())
                i += 1
            i += 1
            cls = "box-teal" if kind in ("teal", "advies", "overweging", "highlight") else "box"
            out.append(f'<div class="{cls}">{inline(" ".join(buf))}</div>')
            continue

        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f'<div class="box">{inline(" ".join(buf))}</div>')
            continue

        if s.startswith("## "):
            seen_heading = True
            heading = s[3:].strip()
            m = re.fullmatch(r"(\d+)[.)]\s*(.+)", heading)
            if m:
                out.append(
                    f'<h2><span class="section-number">{m.group(1)}</span>'
                    f"{inline(m.group(2))}</h2>"
                )
            else:
                out.append(f"<h2>{inline(heading)}</h2>")
            i += 1
            continue

        if s.startswith("### "):
            out.append(f"<h3>{inline(s[4:].strip())}</h3>")
            i += 1
            continue

        if s.startswith("|"):
            raw = []
            while i < n and lines[i].strip().startswith("|"):
                raw.append(lines[i])
                i += 1
            out.append(render_table(raw))
            continue

        if s.startswith("- ") or s.startswith("* "):
            items = []
            while i < n and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ul>")
            continue

        if s == "---":
            i += 1
            continue

        buf = []
        while i < n and lines[i].strip() and not is_block_start(lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        text = " ".join(buf)
        if re.fullmatch(r"\*\*.+?\*\*[:,.]?", text):
            cls = ' class="lead"'
        elif first_paragraph and not seen_heading:
            cls = ' class="aanhef"'
        else:
            cls = ""
        out.append(f"<p{cls}>{inline(text)}</p>")
        first_paragraph = False

    return "\n".join(out)


def build_html(md_text: str, logo_b64: str, footer_note: str, brand: str) -> str:
    lines = md_text.replace("\r\n", "\n").split("\n")
    title, subtitle, meta, start = parse_head(lines)
    body = render_body(lines[start:])

    logo_html = (
        f'<div class="header-right"><img src="data:image/png;base64,{logo_b64}" alt="{brand}"></div>'
        if logo_b64
        else ""
    )
    subtitle_html = f'<div class="subtitle">{inline(subtitle)}</div>' if subtitle else ""
    meta_html = ""
    if meta:
        rows = "".join(
            f'<tr><td class="k">{inline(k)}</td><td>{inline(v)}</td></tr>' for k, v in meta
        )
        meta_html = f'<div class="meta"><table>{rows}</table></div>'

    return f"""<!DOCTYPE html>
<html lang="nl">
<head><meta charset="UTF-8"><title>{html_mod.escape(title)}</title><style>{CSS}</style></head>
<body>
<div class="accent-bar"></div>
<div class="header">
  <div class="header-left"><h1>{inline(title)}</h1>{subtitle_html}</div>
  {logo_html}
</div>
{meta_html}
{body}
<div class="footer">
  <div class="footer-brand">{html_mod.escape(brand)}</div>
  <div>{html_mod.escape(footer_note)}</div>
</div>
</body>
</html>"""


# --------------------------------------------------------------------------- #
# pdf
# --------------------------------------------------------------------------- #

def find_browser() -> str:
    override = os.environ.get("CONTRACT_PDF_BROWSER")
    if override and os.path.exists(override):
        return override
    for path in BROWSER_CANDIDATES:
        if os.path.exists(path):
            return path
    return ""


def load_logo(explicit: str) -> str:
    candidates = [Path(explicit)] if explicit else LOGO_CANDIDATES
    for path in candidates:
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
    print("LET OP: geen logo_base64.txt gevonden — PDF wordt zonder logo gerenderd.")
    return ""


def html_to_pdf(html_content: str, output_path: str) -> bool:
    browser = find_browser()
    if not browser:
        print("FOUT: geen Edge/Chrome gevonden. Zet CONTRACT_PDF_BROWSER naar het pad van de browser.")
        return False

    output_path = os.path.abspath(output_path)
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.isdir(out_dir):
        print(f"FOUT: output-map bestaat niet: {out_dir}")
        return False

    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_content)
        temp_html = f.name

    # Eigen profielmap: anders botst een headless run met een al draaiende
    # Edge/Chrome-sessie en blijft het proces hangen.
    profile_dir = tempfile.mkdtemp(prefix="contractpdf-")
    stderr = ""
    try:
        try:
            result = subprocess.run(
                [
                    browser,
                    "--headless=new",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--no-first-run",
                    "--disable-extensions",
                    f"--user-data-dir={profile_dir}",
                    f"--print-to-pdf={output_path}",
                    "--no-pdf-header-footer",
                    temp_html,
                ],
                capture_output=True,
                text=True,
                timeout=90,
            )
            stderr = (result.stderr or "").strip()
        except subprocess.TimeoutExpired:
            stderr = "browser-timeout (90s)"

        out = Path(output_path)
        if out.exists() and out.stat().st_size > 0:
            print(f"PDF gegenereerd: {output_path}")
            return True
        print(f"FOUT bij PDF-generatie: {stderr[:500]}")
        return False
    finally:
        os.unlink(temp_html)
        shutil.rmtree(profile_dir, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown onderhoudscontract -> branded PDF")
    parser.add_argument("input", help="contract.md (of een .html body als escape hatch)")
    parser.add_argument("-o", "--output", help="pad van de PDF (default: naast de input)")
    parser.add_argument("--logo", default="", help="pad naar logo_base64.txt")
    parser.add_argument(
        "--footer",
        default="Dit document is opgesteld door Agyle. Voor vragen, neem contact op via abdul.malik@agyle.nl",
        help="footer-regel rechtsonder",
    )
    parser.add_argument("--brand", default="A G Y L E", help="merknaam linksonder")
    parser.add_argument("--keep-html", action="store_true", help="schrijf ook de tussen-HTML weg")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"FOUT: bestand niet gevonden: {src}")
        return 1

    logo = load_logo(args.logo)
    text = src.read_text(encoding="utf-8")

    if src.suffix.lower() in (".html", ".htm"):
        body = text.replace("{{LOGO}}", logo).replace("{LOGO}", logo)
        html_doc = (
            "<!DOCTYPE html><html lang='nl'><head><meta charset='UTF-8'>"
            f"<style>{CSS}</style></head><body>{body}</body></html>"
        )
    else:
        html_doc = build_html(text, logo, args.footer, args.brand)

    output = Path(args.output) if args.output else src.with_suffix(".pdf")
    if args.keep_html:
        html_path = output.with_suffix(".html")
        html_path.write_text(html_doc, encoding="utf-8")
        print(f"HTML weggeschreven: {html_path}")

    return 0 if html_to_pdf(html_doc, str(output)) else 1


if __name__ == "__main__":
    sys.exit(main())
