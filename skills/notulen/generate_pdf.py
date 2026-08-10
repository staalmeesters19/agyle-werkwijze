"""PDF Generator voor Meeting Notulen (Agyle branded).

Thin wrapper rond de gedeelde Agyle-branding assets in
`~/.claude/skills/_agyle_branding/`. Templates + logo + html-to-pdf helper
worden daar centraal beheerd zodat de urenverantwoording-skill en deze skill
dezelfde brand-canon delen.
"""

import sys
from pathlib import Path

BRANDING_DIR = Path.home() / ".claude" / "skills" / "_agyle_branding"
sys.path.insert(0, str(BRANDING_DIR))

from html_to_pdf import html_to_pdf, load_logo_base64  # noqa: E402

TEMPLATE_PATH = BRANDING_DIR / "templates" / "notulen.html"
VERDIEPING_TEMPLATE_PATH = BRANDING_DIR / "templates" / "verdieping.html"


def generate_notulen_html(
    titel: str,
    datum: str,
    locatie: str,
    deelnemers: str,
    type_meeting: str,
    duur: str,
    onderwerpen_html: str,
    actiepunten_html: str,
    vervolgstappen_html: str,
) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    logo_b64 = load_logo_base64()

    html = template.replace("{{TITEL}}", titel)
    html = html.replace("{{DATUM}}", datum)
    html = html.replace("{{LOCATIE}}", locatie)
    html = html.replace("{{DEELNEMERS}}", deelnemers)
    html = html.replace("{{TYPE_MEETING}}", type_meeting)
    html = html.replace("{{DUUR}}", duur)
    html = html.replace("{{LOGO_BASE64}}", logo_b64)
    html = html.replace("{{ONDERWERPEN}}", onderwerpen_html)
    html = html.replace("{{ACTIEPUNTEN}}", actiepunten_html)
    html = html.replace("{{VERVOLGSTAPPEN}}", vervolgstappen_html)

    return html


def generate_notulen_pdf(
    output_path: str,
    titel: str,
    datum: str,
    locatie: str,
    deelnemers: str,
    type_meeting: str,
    duur: str,
    onderwerpen_html: str,
    actiepunten_html: str,
    vervolgstappen_html: str,
) -> bool:
    html = generate_notulen_html(
        titel=titel,
        datum=datum,
        locatie=locatie,
        deelnemers=deelnemers,
        type_meeting=type_meeting,
        duur=duur,
        onderwerpen_html=onderwerpen_html,
        actiepunten_html=actiepunten_html,
        vervolgstappen_html=vervolgstappen_html,
    )

    return html_to_pdf(html, output_path)


def generate_verdieping_pdf(
    output_path: str,
    titel: str,
    datum: str,
    locatie: str,
    gehoord_html: str,
    betekenis_html: str,
    eerste_stap_html: str,
) -> bool:
    template = VERDIEPING_TEMPLATE_PATH.read_text(encoding="utf-8")
    logo_b64 = load_logo_base64()

    html = template.replace("{{TITEL}}", titel)
    html = html.replace("{{DATUM}}", datum)
    html = html.replace("{{LOCATIE}}", locatie)
    html = html.replace("{{LOGO_BASE64}}", logo_b64)
    html = html.replace("{{GEHOORD_HTML}}", gehoord_html)
    html = html.replace("{{BETEKENIS_HTML}}", betekenis_html)
    html = html.replace("{{EERSTE_STAP_HTML}}", eerste_stap_html)

    return html_to_pdf(html, output_path)


if __name__ == "__main__":
    test_onderwerpen = """
    <h3>1. Kennismaking en positionering</h3>
    <p>Agyle heeft zich voorgesteld als onderdeel van de Eiffage-groep,
    gespecialiseerd in AI-implementatie en procesautomatisering.</p>

    <h3>2. Technische demonstratie</h3>
    <p>Demonstratie van de slimme optische sensor (SOS) met AI-detectie
    voor bewonersmonitoring in zorginstellingen.</p>
    """

    test_actiepunten = """
    <tr><td>Agyle</td><td>Vervolgafspraak plannen</td><td>Week 15</td></tr>
    <tr><td>Sciva</td><td>Concept delen met productmanager</td><td>Nader te bepalen</td></tr>
    """

    test_vervolgstappen = """
    <p>Er wordt een vervolgafspraak gepland om concreet te kijken naar
    samenwerkingsmogelijkheden.</p>
    """

    output = str(Path(__file__).parent / "test_notulen.pdf")

    success = generate_notulen_pdf(
        output_path=output,
        titel="Kennismaking Avics, OpenXS & Sciva",
        datum="31 maart 2026",
        locatie="Handelsweg 6, Tynaarlo",
        deelnemers="Igor Stalpers-Croeze (Avics), Alan Zenderink (Avics), Peter van Waardenburg (Sciva), Dennis (Agyle), Abdul Malik (Agyle)",
        type_meeting="Kennismaking",
        duur="69 minuten",
        onderwerpen_html=test_onderwerpen,
        actiepunten_html=test_actiepunten,
        vervolgstappen_html=test_vervolgstappen,
    )

    if success:
        print("Test geslaagd!")
    else:
        print("Test mislukt.")
