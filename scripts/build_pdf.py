#!/usr/bin/env python3
"""Build the report using the reference ReportLab layout and MkDocs navigation."""

from pathlib import Path
import html
import re
import os
import yaml

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "whrg-report.pdf"
CONFIG = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))


def nav_docs(items):
    for item in items:
        if isinstance(item, str):
            yield item
        elif isinstance(item, dict):
            for value in item.values():
                yield from nav_docs(value if isinstance(value, list) else [value])


DOCS = list(nav_docs(CONFIG["nav"]))
FONT = "ReportFont" if os.environ.get("REPORT_FONT") else "Helvetica"


def markup(text: str, namespace: str = "") -> str:
    text = html.escape(text.strip())
    text = re.sub(
        r'&lt;a id=&quot;(ref-\d+)&quot;&gt;&lt;/a&gt;',
        lambda m: f'<a name="{namespace}{m.group(1)}"/>',
        text,
    )
    text = re.sub(
        r'\[\[(\d+)\]\]\(#(ref-\d+)\)',
        lambda m: f'<a href="#{namespace}{m.group(2)}" color="#2457a6">[{m.group(1)}]</a>',
        text,
    )
    text = re.sub(r"\[([^]]+)\]\((https?://[^)]+)\)", r'<a href="\2" color="#2457a6">\1</a>', text)
    text = re.sub(r"`([^`]+)`", lambda m: f'<font name="{FONT}">{m.group(1)}</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(20 * mm, 12 * mm, CONFIG["site_name"])
    canvas.drawRightString(190 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if os.environ.get("REPORT_FONT"):
        pdfmetrics.registerFont(TTFont(FONT, os.environ["REPORT_FONT"]))
    pdfmetrics.registerFontFamily(FONT, normal=FONT, bold=FONT, italic=FONT, boldItalic=FONT)
    body = ParagraphStyle("JPBody", fontName=FONT, fontSize=9.3, leading=14.5, spaceAfter=5, wordWrap="CJK", textColor=colors.HexColor("#20242a"))
    reference = ParagraphStyle("JPReference", parent=body, fontSize=7, leading=7.5, spaceAfter=0)
    h1 = ParagraphStyle("JPH1", parent=body, fontSize=19, leading=27, spaceAfter=12, textColor=colors.HexColor("#173f70"))
    h2 = ParagraphStyle("JPH2", parent=body, fontSize=13, leading=19, spaceBefore=10, spaceAfter=6, keepWithNext=True, textColor=colors.HexColor("#245b91"))
    reference_heading = ParagraphStyle("JPReferenceHeading", parent=h2, fontSize=10.5, leading=12, spaceBefore=4, spaceAfter=1, keepWithNext=True)
    h3 = ParagraphStyle("JPH3", parent=body, fontSize=11, leading=17, spaceBefore=7, spaceAfter=4, keepWithNext=True)
    bullet = ParagraphStyle("JPBullet", parent=body, leftIndent=5 * mm, firstLineIndent=-3 * mm)
    story = []

    for doc_index, name in enumerate(DOCS):
        path = (ROOT / "docs" / name).resolve()
        if not path.is_relative_to((ROOT / "docs").resolve()) or path.suffix != ".md":
            raise ValueError(f"Unsupported PDF navigation target: {name}")
        content = path.read_text(encoding="utf-8")
        if FONT == "Helvetica" and not content.isascii():
            raise ValueError("Non-ASCII report text requires REPORT_FONT with appropriate glyph coverage")
        lines = content.splitlines()
        for line in lines:
            if re.search(r"^\s*(```|~~~|!!!|\?\?\?|--8<--|####)|!\[|\[\^|<img|<iframe|<video|\{[:.#]", line):
                raise ValueError(f"Unsupported PDF Markdown in {name}: {line}")
            for target in re.findall(r"\]\(([^)]+)\)", line):
                if not target.startswith(("https://", "http://", "#ref-")):
                    raise ValueError(f"Unsupported PDF link in {name}: {target}")
        chapter_body = body
        chapter_markup = lambda text: markup(text, name.replace("/", "-") + "-")
        i = 0
        in_references = False
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1; continue
            if line.startswith('--8<--'):
                i += 1; continue
            if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-+", lines[i + 1].strip().lstrip("|")):
                rows = [[chapter_markup(c) for c in line.strip("|").split("|")]]
                i += 2
                while i < len(lines) and lines[i].strip().startswith("|"):
                    rows.append([chapter_markup(c) for c in lines[i].strip().strip("|").split("|")]); i += 1
                table = Table([[Paragraph(c, chapter_body) for c in row] for row in rows], repeatRows=1, hAlign="LEFT")
                table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#dce8f4")), ("GRID", (0,0), (-1,-1), .35, colors.HexColor("#9aa7b3")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4)]))
                story.extend([table, Spacer(1, 4 * mm)]); continue
            if line.startswith("# "):
                if doc_index: story.append(PageBreak())
                story.append(Paragraph(chapter_markup(line[2:]), h1))
            elif line.startswith("## "):
                in_references = line[3:] in {"References", "\u53c2\u8003\u6587\u732e"}
                story.append(Paragraph(chapter_markup(line[3:]), reference_heading if in_references else h2))
            elif line.startswith("### "): story.append(Paragraph(chapter_markup(line[4:]), h3))
            elif re.match(r"^[-*] ", line): story.append(Paragraph("- " + chapter_markup(line[2:]), bullet))
            elif re.match(r"^\d+\. ", line): story.append(Paragraph(chapter_markup(line), bullet))
            else: story.append(Paragraph(chapter_markup(line), reference if in_references else chapter_body))
            i += 1
    SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=17*mm, bottomMargin=19*mm, title=CONFIG["site_name"]).build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT)


if __name__ == "__main__": build()
