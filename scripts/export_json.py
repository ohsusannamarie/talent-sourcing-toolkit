#!/usr/bin/env python3
"""
Export a flat tools.json for the searchable site / digests / filters.
Writes both data/tools.json (canonical) and site/tools.json (served by Pages).
One record per structured entry, carrying section + subsection + derived tags.
"""
import yaml, json, re, shutil, os

def clean_heading(h):
    return re.sub(r'^#+\s*', '', h).strip()

def clean_desc(d):
    # Strip inline markers (💰 ❤️) and markdown italics for the card UI; badges
    # already convey pricing/favourite, and the IRL/Virtual/Hybrid prefix is a tag.
    d = d.replace('\U0001F4B0', '').replace('❤️', '')
    d = re.sub(r'^\s*(IRL|Virtual|Hybrid)\s*—\s*', '', d)
    d = re.sub(r'\*([^*]+)\*', r'\1', d)
    d = re.sub(r'\s{2,}', ' ', d).strip(' —').strip()
    return d

def main():
    doc = yaml.safe_load(open("data/site.yaml", encoding='utf-8'))
    records = []
    for s in doc['sections']:
        section = clean_heading(s['heading'])
        subsection = None
        for b in s['blocks']:
            if 'raw' in b:
                r = b['raw']
                if r.startswith('#### ') or r.startswith('### '):
                    subsection = clean_heading(r)
                continue
            e = b['entry']
            records.append({
                'name': e['name'], 'url': e['url'],
                'section': section, 'subsection': subsection,
                'desc': clean_desc(e.get('desc', '')),
                'pricing': e.get('pricing'), 'favorite': e.get('favorite', False),
                'new_2026': e.get('new_2026', False), 'status': e.get('status', 'active'),
                'region': e.get('region', ['global']), 'format': e.get('format'),
                'caution': e.get('caution', []),
                'review': e.get('review'),
            })
    os.makedirs("data", exist_ok=True)
    json.dump(records, open("data/tools.json", 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    os.makedirs("site", exist_ok=True)
    shutil.copy("data/tools.json", "site/tools.json")
    from collections import Counter
    print(f"records: {len(records)}  pricing: {dict(Counter(r['pricing'] for r in records))}  "
          f"favorites: {sum(r['favorite'] for r in records)}  "
          f"acquired: {sum(r['status']!='active' for r in records)}")
    print("wrote data/tools.json + site/tools.json")

if __name__ == '__main__':
    main()
