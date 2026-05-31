#!/usr/bin/env python3
"""
Phase 4: generate docs/CONTRIBUTORS.md from git history + any reviewer credits in
the data layer.

- Git authors: everyone who has committed (excluding the CI bot).
- Reviewers: anyone credited in an entry's `review.by` field (the "why I use it" notes).

Run in CI after merges, or locally. Degrades gracefully if git isn't available.
"""
import subprocess, yaml, os, collections

OUT = "docs/CONTRIBUTORS.md"
BOTS = {"github-actions[bot]", "github-actions"}

def git_authors():
    try:
        out = subprocess.check_output(
            ["git", "log", "--format=%aN"], text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return []
    counts = collections.Counter(
        a.strip() for a in out.splitlines() if a.strip() and a.strip() not in BOTS)
    return [name for name, _ in counts.most_common()]

def reviewers():
    try:
        doc = yaml.safe_load(open("data/site.yaml", encoding="utf-8"))
    except Exception:
        return []
    names = []
    for s in doc.get("sections", []):
        for b in s.get("blocks", []):
            e = b.get("entry") if isinstance(b, dict) else None
            if e and isinstance(e.get("review"), dict) and e["review"].get("by"):
                names.append(e["review"]["by"])
    # de-dupe preserving order
    seen, out = set(), []
    for n in names:
        if n not in seen:
            seen.add(n); out.append(n)
    return out

def main():
    authors = git_authors()
    revs = reviewers()
    lines = ["# Contributors", "",
             "This library is kept alive by the people who add tools, fix links, and share "
             "what actually works. Thank you.", ""]
    if authors:
        lines += ["## Code & content", ""]
        lines += [f"- {a}" for a in authors]
        lines.append("")
    if revs:
        lines += ["## Practitioner reviews", "",
                  "Sourcers and recruiters who shared a \"why I use it\" note:", ""]
        lines += [f"- {r}" for r in revs]
        lines.append("")
    lines += ["---", "",
              "Want on this list? Add a tool via the "
              "[issue form](../../issues/new/choose) or open a PR editing `data/site.yaml`."]
    os.makedirs("docs", exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"wrote {OUT}: {len(authors)} authors, {len(revs)} reviewers")

if __name__ == "__main__":
    main()
