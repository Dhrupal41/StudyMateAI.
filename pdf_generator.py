import re
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    Preformatted,
    HRFlowable
)


def inline_markup(text):
    """Convert a small, safe subset of Markdown to ReportLab markup."""
    text = escape(text)

    # Inline code
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)

    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

    # Italic
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)

    return text


def markdown_to_pdf_elements(content, styles):
    elements = []
    lines = content.splitlines()
    paragraph_lines = []
    bullet_items = []
    numbered_items = []
    in_code_block = False
    code_lines = []

    def flush_paragraph():
        nonlocal paragraph_lines
        if paragraph_lines:
            text = " ".join(line.strip() for line in paragraph_lines)
            elements.append(Paragraph(inline_markup(text), styles["BodyTextCustom"]))
            elements.append(Spacer(1, 5))
            paragraph_lines = []

    def flush_bullets():
        nonlocal bullet_items
        if bullet_items:
            items = [
                ListItem(
                    Paragraph(inline_markup(item), styles["BodyTextCustom"]),
                    leftIndent=10
                )
                for item in bullet_items
            ]
            elements.append(ListFlowable(
                items,
                bulletType="bullet",
                leftIndent=18,
                bulletFontName="Helvetica"
            ))
            elements.append(Spacer(1, 5))
            bullet_items = []

    def flush_numbered():
        nonlocal numbered_items
        if numbered_items:
            items = [
                ListItem(
                    Paragraph(inline_markup(item), styles["BodyTextCustom"]),
                    leftIndent=10
                )
                for item in numbered_items
            ]
            elements.append(ListFlowable(
                items,
                bulletType="1",
                leftIndent=20
            ))
            elements.append(Spacer(1, 5))
            numbered_items = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_bullets()
            flush_numbered()

            if in_code_block:
                elements.append(Preformatted(
                    "\n".join(code_lines),
                    styles["CodeBlockCustom"]
                ))
                elements.append(Spacer(1, 7))
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not stripped:
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            continue

        if stripped == "---":
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            elements.append(HRFlowable(
                width="100%",
                thickness=0.7,
                color=colors.HexColor("#CBD5E1")
            ))
            elements.append(Spacer(1, 7))
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            elements.append(Paragraph(
                inline_markup(stripped[2:]),
                styles["TitleCustom"]
            ))
            elements.append(Spacer(1, 7))
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            elements.append(Paragraph(
                inline_markup(stripped[3:]),
                styles["Heading2Custom"]
            ))
            elements.append(Spacer(1, 4))
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            elements.append(Paragraph(
                inline_markup(stripped[4:]),
                styles["Heading3Custom"]
            ))
            elements.append(Spacer(1, 3))
            continue

        if stripped.startswith("> "):
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            elements.append(Paragraph(
                inline_markup(stripped[2:]),
                styles["QuoteCustom"]
            ))
            elements.append(Spacer(1, 5))
            continue

        if stripped.startswith(("- ", "* ")):
            flush_paragraph()
            flush_numbered()
            bullet_items.append(stripped[2:])
            continue

        numbered_match = re.match(r"^\d+[\.)]\s+(.*)", stripped)
        if numbered_match:
            flush_paragraph()
            flush_bullets()
            numbered_items.append(numbered_match.group(1))
            continue

        paragraph_lines.append(stripped)

    if in_code_block and code_lines:
        elements.append(Preformatted(
            "\n".join(code_lines),
            styles["CodeBlockCustom"]
        ))

    flush_paragraph()
    flush_bullets()
    flush_numbered()

    return elements


def generate_notes_pdf(content, subject, level, topic):
    """Create a PDF in memory and return it for Streamlit's download button."""
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"StudyMate AI - {topic}",
        author="StudyMate AI"
    )

    base_styles = getSampleStyleSheet()

    styles = {
        "TitleCustom": ParagraphStyle(
            "TitleCustom",
            parent=base_styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=25,
            textColor=colors.HexColor("#1D4ED8"),
            alignment=TA_CENTER,
            spaceAfter=10
        ),
        "Heading2Custom": ParagraphStyle(
            "Heading2Custom",
            parent=base_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#1E3A8A"),
            spaceBefore=9,
            spaceAfter=5
        ),
        "Heading3Custom": ParagraphStyle(
            "Heading3Custom",
            parent=base_styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#334155"),
            spaceBefore=6,
            spaceAfter=3
        ),
        "BodyTextCustom": ParagraphStyle(
            "BodyTextCustom",
            parent=base_styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#1F2937")
        ),
        "QuoteCustom": ParagraphStyle(
            "QuoteCustom",
            parent=base_styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=13,
            leftIndent=12,
            textColor=colors.HexColor("#475569"),
            borderColor=colors.HexColor("#93C5FD"),
            borderWidth=1,
            borderPadding=6
        ),
        "CodeBlockCustom": ParagraphStyle(
            "CodeBlockCustom",
            fontName="Courier",
            fontSize=8,
            leading=11,
            leftIndent=8,
            rightIndent=8,
            backColor=colors.HexColor("#F1F5F9"),
            borderColor=colors.HexColor("#CBD5E1"),
            borderWidth=0.5,
            borderPadding=7
        )
    }

    story = [
        Paragraph("StudyMate AI", styles["TitleCustom"]),
        Paragraph(
            f"<b>Subject:</b> {escape(subject)} &nbsp;&nbsp; "
            f"<b>Level:</b> {escape(level)}",
            styles["BodyTextCustom"]
        ),
        Paragraph(
            f"<b>Topic:</b> {escape(topic)}",
            styles["BodyTextCustom"]
        ),
        Spacer(1, 12),
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#2563EB")
        ),
        Spacer(1, 12)
    ]

    story.extend(markdown_to_pdf_elements(content, styles))

    document.build(story)
    buffer.seek(0)

    return buffer.getvalue()
