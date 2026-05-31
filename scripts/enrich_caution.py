#!/usr/bin/env python3
"""
Phase 2: add caution metadata to the data layer (data/site.yaml).

Caution flags are SITE-ONLY metadata — they do NOT change the Markdown line, so
the resource-library round-trip stays byte-identical. They surface as badges on
the searchable site and map to the repo's existing Compliance & Ethics lens.

Flags (conservative, rule-derived — review and hand-tune in site.yaml as needed):
  scraping     — scrapes/automates platforms (esp. LinkedIn); may violate ToS
  privacy-data — surfaces personal contact data (email/phone); GDPR/CCPA care
  ai-screening — uses AI to rank/score/screen/reject candidates; bias + adverse-impact care

These are caution-to-consider markers, not accusations. The point is to make users
go in eyes-open, per docs/compliance-and-ethics.md.
"""
import yaml

SRC = "data/site.yaml"

# Section-level rules (broad strokes)
SECTION_RULES = {
    "Scraping & Automation": ["scraping"],
    "Contact Info & Enrichment": ["privacy-data"],
}
SUBSECTION_RULES = {
    "AI Screening & Conversational Recruiting": ["ai-screening"],
}

# Name-level rules for tools that sit OUTSIDE the obvious sections
NAME_SCRAPING = {
    "Phantombuster", "Waalaxy", "Expandi", "Dripify", "Captain Data", "Browse AI",
    "Instant Data Scraper", "Bardeen", "Apify", "Scrapy",
}
# Description keywords that imply AI-driven candidate ranking/scoring
DESC_AI_SCREEN = ["rank candidate", "score candidate", "scores candidate", "ranks candidate",
                  "ai assessment", "screens and ranks", "screen and rank", "scores resumes",
                  "ranks them by fit", "scores candidates"]

def section_of(heading):
    import re
    return re.sub(r'^#+\s*', '', heading).strip()

def main():
    doc = yaml.safe_load(open(SRC, encoding='utf-8'))
    n = 0
    for s in doc['sections']:
        section = section_of(s['heading'])
        subsection = None
        for b in s['blocks']:
            if 'raw' in b:
                r = b['raw']
                if r.startswith(('#### ', '### ')):
                    subsection = section_of(r)
                continue
            e = b['entry']
            flags = set(e.get('caution', []))
            # section / subsection rules
            for sec_key, fl in SECTION_RULES.items():
                if sec_key in section:
                    flags.update(fl)
            for sub_key, fl in SUBSECTION_RULES.items():
                if subsection and sub_key in sub_key and subsection == sub_key:
                    flags.update(fl)
            # name rule (scraping tools that live in other sections too)
            if e['name'] in NAME_SCRAPING:
                flags.add("scraping")
            # description-driven AI screening
            dl = e.get('desc', '').lower()
            if any(k in dl for k in DESC_AI_SCREEN):
                flags.add("ai-screening")
            if flags:
                e['caution'] = sorted(flags)
                n += 1
    yaml.safe_dump(doc, open(SRC, 'w', encoding='utf-8'),
                   allow_unicode=True, sort_keys=False, width=1000)
    print(f"entries flagged: {n}  ->  {SRC}")

if __name__ == '__main__':
    main()
