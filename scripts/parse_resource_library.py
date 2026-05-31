#!/usr/bin/env python3
"""
Parse docs/resource-library.md into the structured data layer (data/site.yaml).

Lossless round-trip: every section is an ordered list of blocks.
  - {entry: {...}}   a parsed resource line  - [Name](url) — desc
  - {raw: "..."}     any other line, preserved verbatim

Tool entries get derived tags (pricing, favorite, new_2026, type, region, status,
format) so the website and digests can filter them.
"""
import re, os, yaml

SRC = "docs/resource-library.md"
OUT = "data/site.yaml"

ENTRY_RE = re.compile(r'^(\s*)- \[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\)(?P<rest>.*)$')

def derive_tags(rest):
    rest_l = rest.lower()
    tags = {}
    tags['pricing'] = 'paid' if '\U0001F4B0' in rest else 'free'   # 💰
    tags['favorite'] = '❤️' in rest                       # ❤️
    tags['new_2026'] = ('2026' in rest) and any(w in rest_l for w in ['new', 'launched', 'edition'])
    tags['status'] = 'acquired' if any(w in rest_l for w in
        ['acquired', 'now part of', 'rebrand', 'now icims', 'formerly', 'folded']) else 'active'
    region = []
    if any(w in rest_l for w in ['european', 'europe', 'emea', ' eu ']):
        region.append('eu')
    if 'apac' in rest_l:
        region.append('apac')
    tags['region'] = region or ['global']
    m = re.search(r'—\s*(IRL|Virtual|Hybrid)\s*—', rest)
    if m:
        tags['format'] = m.group(1).lower()
    return tags

def clean_desc(rest):
    r = rest.strip()
    if r.startswith('—'):   # leading em dash
        r = r[1:].strip()
    return r

# Enrichment fields are hand-curated or rule-added on top of the parsed data; they
# don't live in the Markdown. Preserve them across re-parses by keying on name|url.
PRESERVE = ('caution', 'review', 'sunset_note')

def load_enrichment():
    if not os.path.exists(OUT):
        return {}
    try:
        prev = yaml.safe_load(open(OUT, encoding='utf-8')) or {}
    except Exception:
        return {}
    keep = {}
    for s in prev.get('sections', []):
        for b in s.get('blocks', []):
            e = b.get('entry') if isinstance(b, dict) else None
            if not e:
                continue
            extra = {k: e[k] for k in PRESERVE if k in e}
            if extra:
                keep[e.get('name', '') + '|' + e.get('url', '')] = extra
    return keep

def parse():
    enrich = load_enrichment()
    lines = open(SRC, encoding='utf-8').read().split('\n')
    doc = {'frontmatter': [], 'sections': []}
    cur = None
    in_front = True
    for line in lines:
        if line.startswith('## '):
            in_front = False
            cur = {'heading': line, 'blocks': []}
            doc['sections'].append(cur)
            continue
        if in_front:
            doc['frontmatter'].append(line)
            continue
        m = ENTRY_RE.match(line)
        is_toc = 'Overview' in cur['heading']
        if m and m.group(1) == '' and not is_toc:
            e = {'name': m.group('name'), 'url': m.group('url'), 'desc': clean_desc(m.group('rest'))}
            e.update(derive_tags(m.group('rest')))
            e['_raw'] = line
            # restore any preserved enrichment for this entry
            extra = enrich.get(e['name'] + '|' + e['url'])
            if extra:
                e.update(extra)
            cur['blocks'].append({'entry': e})
        else:
            cur['blocks'].append({'raw': line})
    return doc

def main():
    doc = parse()
    yaml.safe_dump(doc, open(OUT, 'w', encoding='utf-8'),
                   allow_unicode=True, sort_keys=False, width=1000)
    n = sum(1 for s in doc['sections'] for b in s['blocks'] if 'entry' in b)
    print(f"sections: {len(doc['sections'])}  entries: {n}  ->  {OUT}")

if __name__ == '__main__':
    main()
