"""Shared Agyle HTML -> PDF helper via headless Edge/Chrome.

Used by verwerk-meeting (notulen, verdieping) and urenverantwoording
(uren, toelichting) skills. Single source of truth for Agyle-branded PDF output.
"""

import os
import subprocess
import tempfile
from pathlib import Path

BRANDING_DIR = Path(__file__).parent
LOGO_BASE64_PATH = BRANDING_DIR / "logo_base64.txt"
TEMPLATES_DIR = BRANDING_DIR / "templates"

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def find_browser():
    for path in EDGE_PATHS:
        if os.path.exists(path):
            return path
    return None


def load_logo_base64() -> str:
    if LOGO_BASE64_PATH.exists():
        return LOGO_BASE64_PATH.read_text().strip()
    return ""


def html_to_pdf(html_content: str, output_path: str) -> bool:
    browser = find_browser()
    if not browser:
        print("FOUT: Geen Edge of Chrome gevonden voor PDF-generatie.")
        return False

    output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        print(f"FOUT: output-folder bestaat niet: {output_dir}")
        return False

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    ) as f:
        f.write(html_content)
        temp_html = f.name

    try:
        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            f"--print-to-pdf={output_path}",
            "--no-pdf-header-footer",
            temp_html,
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if Path(output_path).exists() and Path(output_path).stat().st_size > 0:
            print(f"PDF gegenereerd: {output_path}")
            return True
        else:
            print(f"FOUT bij PDF-generatie: {result.stderr}")
            return False

    finally:
        os.unlink(temp_html)