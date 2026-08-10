"""
Markdown to Professional PDF converter for Agyle client preparations.
Uses Playwright (Chromium) for perfect CSS/table rendering.

Usage:
    python md_to_pdf.py input.md [output.pdf]

If output is omitted, saves as input.pdf in the same directory.
"""

import sys
import os
import markdown
from playwright.sync_api import sync_playwright

CSS = """
@page {
    size: A4;
    margin: 20mm 18mm 25mm 18mm;
}

@media print {
    body { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
}

* { box-sizing: border-box; }

body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1a1a2e;
    max-width: 100%;
    margin: 0;
    padding: 0;
}

/* --- Headings --- */
h1 {
    font-size: 20pt;
    font-weight: 700;
    color: #0f1b4c;
    border-bottom: 3px solid #2563eb;
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 16px;
}

h2 {
    font-size: 14pt;
    font-weight: 600;
    color: #1e3a5f;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 5px;
    margin-top: 28px;
    margin-bottom: 12px;
    page-break-after: avoid;
}

h3 {
    font-size: 12pt;
    font-weight: 600;
    color: #2563eb;
    margin-top: 22px;
    margin-bottom: 8px;
    page-break-after: avoid;
}

h4 {
    font-size: 10.5pt;
    font-weight: 600;
    color: #475569;
    margin-top: 16px;
    margin-bottom: 6px;
    page-break-after: avoid;
}

/* --- Tables --- */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 18px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

thead th,
th {
    background-color: #0f1b4c;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #0f1b4c;
}

td {
    padding: 7px 10px;
    border: 1px solid #d1d5db;
    vertical-align: top;
}

tr:nth-child(even) td {
    background-color: #f1f5f9;
}

tr:hover td {
    background-color: #e8f0fe;
}

/* First column bold for key-value tables */
td:first-child {
    font-weight: 500;
    white-space: nowrap;
}

/* --- Lists --- */
ul, ol {
    margin: 6px 0 12px 0;
    padding-left: 22px;
}

li {
    margin-bottom: 4px;
}

li ul, li ol {
    margin: 2px 0 2px 0;
}

/* --- Horizontal rules --- */
hr {
    border: none;
    border-top: 1.5px solid #e2e8f0;
    margin: 20px 0;
}

/* --- Inline styles --- */
strong {
    font-weight: 600;
    color: #0f172a;
}

em {
    color: #475569;
    font-style: italic;
}

code {
    background-color: #f1f5f9;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 9pt;
    font-family: 'Cascadia Code', 'Consolas', monospace;
}

/* --- Blockquotes (used for tips/notes) --- */
blockquote {
    border-left: 4px solid #2563eb;
    background-color: #eff6ff;
    margin: 12px 0;
    padding: 10px 16px;
    color: #1e40af;
    font-size: 10pt;
}

blockquote p { margin: 0; }

/* --- Paragraphs --- */
p {
    margin: 6px 0;
}

/* --- Print optimization --- */
h2, h3, h4 {
    page-break-after: avoid;
}

table, blockquote {
    page-break-inside: avoid;
}

li {
    page-break-inside: avoid;
}
"""

HEADER_HTML = """
<div style="font-size: 7.5pt; color: #94a3b8; text-align: right; width: 100%; padding-bottom: 4px; border-bottom: 0.5px solid #e2e8f0;">
    Agyle &mdash; Klantvoorbereiding
</div>
"""

FOOTER_HTML = """
<div style="font-size: 7.5pt; color: #94a3b8; text-align: center; width: 100%; padding-top: 4px; border-top: 0.5px solid #e2e8f0;">
    Vertrouwelijk &mdash; Agyle &nbsp;&bull;&nbsp; Pagina <span class="pageNumber"></span> van <span class="totalPages"></span>
</div>
"""


def md_to_html(md_text: str) -> str:
    """Convert markdown to full HTML document with styling."""
    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    )
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="utf-8">
    <style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""


def html_to_pdf(html: str, output_path: str) -> None:
    """Render HTML to PDF using Playwright Chromium."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        page.pdf(
            path=output_path,
            format="A4",
            margin={"top": "25mm", "right": "18mm", "bottom": "30mm", "left": "18mm"},
            print_background=True,
            display_header_footer=True,
            header_template=HEADER_HTML,
            footer_template=FOOTER_HTML,
        )
        browser.close()


def convert(input_path: str, output_path: str | None = None) -> str:
    """Convert a markdown file to PDF. Returns the output path."""
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".pdf"

    with open(input_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html = md_to_html(md_text)
    html_to_pdf(html, output_path)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_pdf.py input.md [output.pdf]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    result = convert(input_file, output_file)
    print(f"PDF generated: {result}")
