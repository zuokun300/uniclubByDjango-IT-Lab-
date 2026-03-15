from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def build_pdf(source_path: Path, target_path: Path) -> None:
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        spaceAfter=6,
    )
    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        spaceBefore=8,
        spaceAfter=8,
    )

    story = []
    for raw_line in source_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            story.append(Spacer(1, 4))
            continue

        if line.startswith("#"):
            clean = line.lstrip("#").strip()
            story.append(Paragraph(clean, heading))
        else:
            story.append(Paragraph(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), body))

    doc = SimpleDocTemplate(
        str(target_path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )
    doc.build(story)


def main():
    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    build_pdf(docs_dir / "coursework_report.md", docs_dir / "coursework_report.pdf")
    print((docs_dir / "coursework_report.pdf").resolve())


if __name__ == "__main__":
    main()
