#!/usr/bin/env python3
"""
Phase 4: turn a parsed "Add a tool" issue into a draft data-layer entry.

Reads the issue body fields (passed as a JSON file by the workflow) and appends a
new entry to the right section in data/site.yaml, then regenerates the library.
The workflow opens a PR with the result for human review — nothing auto-merges.

Usage (in CI): python3 scripts/issue_to_entry.py issue.json
issue.json shape (produced by the workflow from the issue form):
  {"name":..., "url":..., "category":..., "pricing":..., "desc":..., "why":..., "submitter":...}
"""
import sys, json, yaml, re

SITE = "data/site.yaml"

# map issue-form category -> the section heading substring in site.yaml
CAT_TO_SECTION = {
    "AI Sourcing Platforms": "AI Sourcing Platforms",
    "Search & OSINT": "Search & OSINT",
    "Contact Info & Enrichment": "Contact Info & Enrichment",
    "Outreach & Email": "Outreach & Email",
    "Talent Intelligence": "Talent Intelligence",
    "ATS, CRM & Recruiting Ops": "ATS, CRM & Recruiting Ops",
    "Job Descriptions & Inclusive Hiring": "Job Descriptions & Inclusive Hiring",
    "Screening & Interviews": "Screening & Interviews",
    "Scraping & Automation": "Scraping & Automation",
    "AI Writing & Productivity": "AI Writing & Productivity",
    "Employer Brand & Job Marketing": "Employer Brand & Job Marketing",
    "Productivity & Browser Tools": "Productivity & Browser Tools",
    "Learning & Community": "Learning & Community",
    "Reports & Research": "Reports & Research",
}

def build_raw(name, url, pricing, desc):
    marker = "\U0001F4B0 " if pricing == "paid" else ""   # 💰
    return f"- [{name}]({url}) — {marker}{desc}".rstrip()

def main(path):
    f = json.load(open(path, encoding="utf-8"))
    doc = yaml.safe_load(open(SITE, encoding="utf-8"))
    section_key = CAT_TO_SECTION.get(f.get("category", ""), "")
    target = None
    for s in doc["sections"]:
        if section_key and section_key in s["heading"]:
            target = s
            break
    if target is None:
        # fall back: append under Learning & Community
        target = next(s for s in doc["sections"] if "Learning & Community" in s["heading"])

    pricing = "paid" if f.get("pricing") == "paid" else "free"
    entry = {
        "name": f["name"].strip(),
        "url": f["url"].strip(),
        "desc": f.get("desc", "").strip(),
        "pricing": pricing,
        "favorite": False,
        "new_2026": True,
        "status": "active",
        "region": ["global"],
        "_raw": build_raw(f["name"].strip(), f["url"].strip(), pricing, f.get("desc", "").strip()),
    }
    if f.get("why") and f.get("submitter"):
        entry["review"] = {"quote": f["why"].strip(), "by": f["submitter"].strip()}

    # insert before the first trailing raw/blank block so it sits with the list
    insert_at = len(target["blocks"])
    for i in range(len(target["blocks"]) - 1, -1, -1):
        if "entry" in target["blocks"][i]:
            insert_at = i + 1
            break
    target["blocks"].insert(insert_at, {"entry": entry})

    yaml.safe_dump(doc, open(SITE, "w", encoding="utf-8"),
                   allow_unicode=True, sort_keys=False, width=1000)
    print(f"added '{entry['name']}' to section: {target['heading']}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "issue.json")
