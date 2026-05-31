# Conversion Guide

The original archive files are useful, but binary files are not very GitHub-friendly.

This guide shows how to turn the source files into Markdown so the repo becomes easier to browse, search, review, and maintain.

---

## Source files

The source archive currently lives in the repo root:

- `List of 1,395 Google Custom Search Engines (CSEs).xlsx`
- `List of 490 Chrome Extensions (Applicable to Talent Sourcing).docx`

---

## Generated output

The conversion script writes Markdown files to:

```text
resources/generated/google-cses.md
resources/generated/chrome-extensions.md
```

These generated files are meant to be reviewed before committing.

---

## Local setup

From the repo root, install the needed Python packages:

```bash
python -m pip install pandas openpyxl python-docx
```

Then run:

```bash
python scripts/convert_resources_to_markdown.py
```

---

## After conversion

Review the generated files and look for:

- Broken or malformed links
- Empty rows
- Duplicate resources
- Weird formatting from the Word document
- Tools that look abandoned or risky
- Resources that should be tagged or moved into a caution zone

---

## Suggested cleanup columns

When polishing the generated Markdown, consider adding:

| Column | Why it matters |
|---|---|
| Category | Makes the list browsable by use case |
| Tags | Makes search/filtering easier |
| Best for | Explains how a sourcer would actually use it |
| Risk level | Helps flag sensitive tools or browser extensions |
| Maintenance status | Shows whether the resource still appears active |
| Notes | Adds human context that raw links cannot provide |

---

## Practical recommendation

Do not try to perfect all 1,885 resources in one pass.

Start with one generated file, tag the top 50 most useful resources, and build from there. A clean shortlist beats a beautiful graveyard of links every time.
