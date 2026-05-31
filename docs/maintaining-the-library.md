# Maintaining the resource library

The resource library is **data-driven**. You edit one file; everything else regenerates.

## The flow

```
data/site.yaml                         ← edit this (source of truth)
  │
  ├─ scripts/generate_resource_library.py  →  docs/resource-library.md  (the guide)
  └─ scripts/export_json.py                →  data/tools.json + site/tools.json  (the app)
```

Never hand-edit `docs/resource-library.md` — it's generated, and CI will fail the build
if it drifts from the data layer.

## Add / change / remove a resource

1. Edit the entry in `data/site.yaml`.
2. Regenerate and refresh data:
   ```bash
   pip install pyyaml
   python3 scripts/generate_resource_library.py
   mv docs/resource-library.generated.md docs/resource-library.md
   python3 scripts/export_json.py
   ```
3. Commit. On push, `build.yml` verifies the Markdown matches the data layer,
   and `pages.yml` redeploys the site.

## Entry schema

```yaml
- name: SourceWhale
  url: https://sourcewhale.com
  desc: Multi-step outreach across email, LinkedIn, SMS, WhatsApp, and phone.
  pricing: paid          # free | paid  (paid renders the 💰 marker)
  favorite: true         # the ❤️ flag
  new_2026: false
  status: active         # active | acquired
  region: [global]       # global | eu | apac
  format: hybrid         # conferences only: irl | virtual | hybrid
  _raw: "- [SourceWhale](https://sourcewhale.com) — ❤️ 💰 Multi-step outreach…"
```

`_raw` preserves the exact Markdown line so regeneration is byte-identical. When you
change an entry, either update `_raw` too, or delete `_raw` and the generator will
render the line from the structured fields.

### Caution flags (site-only)

Entries may carry a `caution` list — `scraping`, `privacy-data`, and/or `ai-screening`.
These render as ⚠ badges on the site and are **metadata only**: they don't touch the
Markdown, so the round-trip stays byte-identical. Regenerate them any time with:

```bash
python3 scripts/enrich_caution.py   # rule-derived, idempotent
```

The rules are conservative (section, name, and description heuristics). To override —
add or remove a flag on a specific entry — edit its `caution:` list in `data/site.yaml`
directly; `enrich_caution.py` only *adds*, so hand-set flags survive. See
[disclosure.md](disclosure.md) for what each flag means.

### Retiring a tool (the graveyard)

Don't delete a dead tool — set `status: sunset` on its entry, add a `sunset_note`, and
move its row into [retired-tools.md](retired-tools.md). The active library and site drop
it automatically while the history survives.

## Tags are auto-derived

`parse_resource_library.py` derives `pricing`, `favorite`, `new_2026`, `status`,
`region`, and `format` from the existing 💰 / ❤️ markers and description text — so a
one-time re-parse keeps tags in sync if you ever bulk-edit the Markdown directly:

```bash
python3 scripts/parse_resource_library.py   # docs/resource-library.md -> data/site.yaml
```

## The workflows

- `.github/workflows/build.yml` — every push: regenerate + verify the Markdown is in
  sync with the data layer. Fails if they drift.
- `.github/workflows/links.yml` — Mondays: link-check the library, open a `link-rot`
  issue on breakage.
- `.github/workflows/pages.yml` — every push touching `site/` or the data: deploy the
  searchable app to GitHub Pages.
- `.github/workflows/digest.yml` — 1st of the month: refresh the contributor wall and
  generate a "what changed" digest from data-layer snapshots.
- `.github/workflows/submission.yml` — when an issue gets the `new-entry` label: parse
  the form, add the entry to `data/site.yaml`, and open a PR for review.

## Community loop

- **Submissions** — the [Add a tool issue form](../../issues/new/choose) auto-drafts a PR
  via `scripts/issue_to_entry.py`. Nothing auto-merges; you review the diff.
- **Reviews** — an entry's `review: {quote, by}` field renders as a quote on the site and
  credits the reviewer on the wall. Preserved across re-parses.
- **Contributor wall** — `scripts/contributors.py` builds `docs/CONTRIBUTORS.md` from git
  authors + reviewers.
- **Digest** — `scripts/digest.py` snapshots the data monthly and diffs against the prior
  month into `docs/digest/<month>.md`. First run seeds a baseline; digests start the
  following month.

> Note: re-parsing the Markdown preserves enrichment fields (`review`, `caution`,
> `sunset_note`) by matching on name+url, so hand-curated metadata is never lost.

## First-time Pages setup

Settings → Pages → Build and deployment → Source: **GitHub Actions**. The `pages.yml`
workflow handles the rest. Site goes live at
`https://ohsusannamarie.github.io/talent-sourcing-toolkit/`.
