#!/usr/bin/env python3
"""
Phase 4: monthly "what changed" digest, generated from the data layer.

Keeps a snapshot of the resource set under data/.snapshots/<YYYY-MM>.json and diffs
the current data against the most recent prior snapshot. Writes:
  - docs/digest/<YYYY-MM>.md   a human-readable digest for that month
  - updates docs/digest/README.md index

Run monthly (CI) or on demand. First run just seeds the baseline snapshot.
"""
import json, os, glob, datetime, sys

DATA = "data/tools.json"
SNAPDIR = "data/.snapshots"
OUTDIR = "docs/digest"

def load(path):
    return json.load(open(path, encoding="utf-8"))

def key(r):
    return r["name"] + "|" + r["url"]

def latest_prior_snapshot(this_month):
    os.makedirs(SNAPDIR, exist_ok=True)
    snaps = sorted(glob.glob(os.path.join(SNAPDIR, "*.json")))
    snaps = [s for s in snaps if os.path.basename(s)[:-5] < this_month]
    return snaps[-1] if snaps else None

def diff(prev, cur):
    pk = {key(r): r for r in prev}
    ck = {key(r): r for r in cur}
    added = [ck[k] for k in ck if k not in pk]
    removed = [pk[k] for k in pk if k not in ck]
    # status / pricing changes on entries present in both
    changed = []
    for k in ck:
        if k in pk:
            a, b = pk[k], ck[k]
            deltas = []
            if a.get("status") != b.get("status"):
                deltas.append(f"status {a.get('status')} → {b.get('status')}")
            if a.get("pricing") != b.get("pricing"):
                deltas.append(f"pricing {a.get('pricing')} → {b.get('pricing')}")
            if deltas:
                changed.append((b, deltas))
    return added, removed, changed

def write_digest(month, added, removed, changed, total):
    os.makedirs(OUTDIR, exist_ok=True)
    lines = [f"# Resource library digest — {month}", ""]
    if not (added or removed or changed):
        lines.append("No changes this period. The library held steady.")
    else:
        if added:
            lines += [f"## Added ({len(added)})", ""]
            for r in sorted(added, key=lambda r: r["name"].lower()):
                lines.append(f"- **{r['name']}** — {r.get('desc','')}  _({r['section']})_")
            lines.append("")
        if changed:
            lines += [f"## Updated ({len(changed)})", ""]
            for r, d in sorted(changed, key=lambda x: x[0]["name"].lower()):
                lines.append(f"- **{r['name']}** — {'; '.join(d)}")
            lines.append("")
        if removed:
            lines += [f"## Removed ({len(removed)})", ""]
            for r in sorted(removed, key=lambda r: r["name"].lower()):
                lines.append(f"- **{r['name']}** — was in {r['section']}")
            lines.append("")
    lines.append(f"_Library now lists {total} resources._")
    open(os.path.join(OUTDIR, f"{month}.md"), "w", encoding="utf-8").write("\n".join(lines))

def update_index():
    os.makedirs(OUTDIR, exist_ok=True)
    months = sorted([os.path.basename(f)[:-3] for f in glob.glob(os.path.join(OUTDIR, "20*.md"))], reverse=True)
    idx = ["# Monthly digests", "", "Auto-generated summaries of what changed in the resource library.", ""]
    for m in months:
        idx.append(f"- [{m}]({m}.md)")
    open(os.path.join(OUTDIR, "README.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")

def main():
    cur = load(DATA)
    month = datetime.date.today().strftime("%Y-%m")
    prior = latest_prior_snapshot(month)
    if prior is None:
        # seed baseline, no digest yet
        json.dump(cur, open(os.path.join(SNAPDIR, f"{month}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print(f"seeded baseline snapshot {month}.json ({len(cur)} records); no prior month to diff")
        return
    prev = load(prior)
    added, removed, changed = diff(prev, cur)
    write_digest(month, added, removed, changed, len(cur))
    update_index()
    # save this month's snapshot
    json.dump(cur, open(os.path.join(SNAPDIR, f"{month}.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"digest {month}: +{len(added)} added, ~{len(changed)} changed, -{len(removed)} removed "
          f"(vs {os.path.basename(prior)[:-5]})")

if __name__ == "__main__":
    main()
