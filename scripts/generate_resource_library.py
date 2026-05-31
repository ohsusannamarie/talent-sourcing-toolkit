#!/usr/bin/env python3
"""
Regenerate docs/resource-library.md from the data layer (data/site.yaml).

Lossless: re-emits each entry's preserved `_raw` line, so output is byte-identical
to the source. Drop `_raw` on an entry to render it from structured fields instead.
"""
import yaml

SRC = "data/site.yaml"
OUT = "docs/resource-library.generated.md"

def render_entry(e):
    if e.get('_raw') is not None:
        return e['_raw']
    markers = ''
    if e.get('pricing') == 'paid':
        markers += '\U0001F4B0 '   # 💰
    if e.get('favorite'):
        markers += '❤️ '
    desc = e.get('desc', '')
    tail = f" — {markers}{desc}".rstrip() if (markers or desc) else ''
    return f"- [{e['name']}]({e['url']}){tail}"

def main():
    doc = yaml.safe_load(open(SRC, encoding='utf-8'))
    out = list(doc['frontmatter'])
    for s in doc['sections']:
        out.append(s['heading'])
        for b in s['blocks']:
            out.append(render_entry(b['entry']) if 'entry' in b else b['raw'])
    open(OUT, 'w', encoding='utf-8').write('\n'.join(out))
    print(f"wrote {OUT} ({len(out)} lines)")

if __name__ == '__main__':
    main()
