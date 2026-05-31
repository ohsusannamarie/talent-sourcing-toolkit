#!/usr/bin/env python3
"""
Convert the Talent Sourcing Toolkit source files into GitHub-readable Markdown.

Run from the repository root:

    python -m pip install pandas openpyxl python-docx
    python scripts/convert_resources_to_markdown.py

Generated files:

    resources/generated/google-cses.md
    resources/generated/chrome-extensions.md

Review generated files before committing. The script does not decide what is safe,
current, or recommended. It only converts the archive into a more readable format.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List

import pandas as pd
from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "resources" / "generated"

CSE_FILE = ROOT / "List of 1,395 Google Custom Search Engines (CSEs).xlsx"
EXTENSIONS_FILE = ROOT / "List of 490 Chrome Extensions (Applicable to Talent Sourcing).docx"

CSE_OUTPUT = OUT_DIR / "google-cses.md"
EXTENSIONS_OUTPUT = OUT_DIR / "chrome-extensions.md"


def clean_text(value: object) -> str:
    """Normalize text for Markdown table cells."""
    if value is None:
        return ""

    text = str(value).strip()
    if text.lower() in {"nan", "none", "null"}:
        return ""

    text = re.sub(r"\s+", " ", text)
    text = text.replace("|", "\\|")
    return text


def safe_heading(text: str, fallback: str = "Untitled") -> str:
    text = clean_text(text)
    return text if text else fallback


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Convert a dataframe to a Markdown table with cleaned cells."""
    df = df.copy()
    df = df.dropna(how="all").dropna(axis=1, how="all")

    if df.empty:
        return "_No rows found._\n"

    cleaned_columns: List[str] = []
    for index, column in enumerate(df.columns, start=1):
        column_name = clean_text(column)
        if not column_name or column_name.startswith("Unnamed:"):
            column_name = f"Column {index}"
        cleaned_columns.append(column_name)

    df.columns = cleaned_columns
    df = df.fillna("")

    lines: List[str] = []
    lines.append("| " + " | ".join(clean_text(col) for col in df.columns) + " |")
    lines.append("| " + " | ".join("---" for _ in df.columns) + " |")

    for _, row in df.iterrows():
        lines.append("| " + " | ".join(clean_text(cell) for cell in row.tolist()) + " |")

    return "\n".join(lines) + "\n"


def convert_google_cses() -> None:
    if not CSE_FILE.exists():
        raise FileNotFoundError(f"Missing source file: {CSE_FILE}")

    sheets = pd.read_excel(CSE_FILE, sheet_name=None, dtype=str)

    content: List[str] = [
        "# Google Custom Search Engines",
        "",
        f"Generated from `{CSE_FILE.name}`.",
        "",
        "> Review links, categories, and maintenance status before treating any resource as recommended.",
        "",
    ]

    for sheet_name, df in sheets.items():
        content.extend(
            [
                f"## {safe_heading(sheet_name, 'Sheet')}",
                "",
                f"Rows found: **{len(df.dropna(how='all'))}**",
                "",
                dataframe_to_markdown(df),
                "",
            ]
        )

    CSE_OUTPUT.write_text("\n".join(content).strip() + "\n", encoding="utf-8")


def iter_block_items(document: Document) -> Iterable[Paragraph | Table]:
    """Yield paragraphs and tables in document order."""
    parent_element = document.element.body

    for child in parent_element.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, document)
        elif isinstance(child, CT_Tbl):
            yield Table(child, document)


def table_to_markdown(table: Table) -> str:
    rows = []
    for row in table.rows:
        rows.append([clean_text(cell.text) for cell in row.cells])

    rows = [row for row in rows if any(cell for cell in row)]
    if not rows:
        return ""

    max_cols = max(len(row) for row in rows)
    normalized = [row + [""] * (max_cols - len(row)) for row in rows]

    header = normalized[0]
    body = normalized[1:]

    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]

    for row in body:
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines) + "\n"


def convert_chrome_extensions() -> None:
    if not EXTENSIONS_FILE.exists():
        raise FileNotFoundError(f"Missing source file: {EXTENSIONS_FILE}")

    document = Document(EXTENSIONS_FILE)

    content: List[str] = [
        "# Chrome Extensions Applicable to Talent Sourcing",
        "",
        f"Generated from `{EXTENSIONS_FILE.name}`.",
        "",
        "> Review extension permissions, privacy policies, ownership, and maintenance status before installing or recommending anything here.",
        "",
    ]

    table_count = 0
    paragraph_count = 0

    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            text = clean_text(block.text)
            if not text:
                continue

            paragraph_count += 1
            style_name = getattr(block.style, "name", "") or ""

            if style_name.lower().startswith("heading"):
                level_match = re.search(r"(\d+)", style_name)
                level = int(level_match.group(1)) if level_match else 2
                level = min(max(level, 2), 4)
                content.append(f"{'#' * level} {text}")
            else:
                content.append(text)
            content.append("")

        elif isinstance(block, Table):
            markdown_table = table_to_markdown(block)
            if markdown_table:
                table_count += 1
                content.append(markdown_table)
                content.append("")

    content.extend(
        [
            "---",
            "",
            "## Conversion summary",
            "",
            f"- Paragraph blocks converted: **{paragraph_count}**",
            f"- Tables converted: **{table_count}**",
            "",
        ]
    )

    EXTENSIONS_OUTPUT.write_text("\n".join(content).strip() + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Converting Google CSE archive...")
    convert_google_cses()
    print(f"Wrote {CSE_OUTPUT.relative_to(ROOT)}")

    print("Converting Chrome extension archive...")
    convert_chrome_extensions()
    print(f"Wrote {EXTENSIONS_OUTPUT.relative_to(ROOT)}")

    print("Done. Review generated Markdown before committing.")


if __name__ == "__main__":
    main()
