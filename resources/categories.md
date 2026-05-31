# Categories & Tags

This guide gives the toolkit a practical organizing system.

The goal is not to create a perfect taxonomy. The goal is to make the resources easier to search, filter, audit, and turn into recruiter enablement materials.

---

## Tagging principles

### Tag by use case, not vendor hype

Bad tag: `AI-powered super sourcing magic`

Good tag: `contact-finding`, `profile-enrichment`, `technical-sourcing`, `company-research`

### Use multiple tags when needed

A tool can belong to more than one category. For example, a Chrome extension may support both `productivity` and `candidate-discovery`.

### Include risk and maintenance notes

A useful tool can still be risky, outdated, or blocked by company policy. Tagging those concerns makes the library more trustworthy.

---

## Core taxonomy

| Dimension | What it answers | Example tags |
|---|---|---|
| Resource type | What kind of resource is it? | `chrome-extension`, `google-cse`, `website`, `database`, `guide`, `template` |
| Workflow stage | Where does it fit in sourcing? | `discovery`, `research`, `enrichment`, `outreach-prep`, `tracking`, `cleanup` |
| Talent focus | What kind of talent is it useful for? | `technical-sourcing`, `executive-search`, `academic-research`, `diversity-sourcing` |
| Research depth | How deep or advanced is it? | `basic`, `intermediate`, `advanced`, `osint-adjacent` |
| Risk level | How carefully should it be reviewed? | `low-risk`, `review-needed`, `high-permission`, `privacy-sensitive` |
| Maintenance status | Is it still usable? | `active`, `unknown`, `deprecated`, `dead-link`, `needs-review` |

---

## Chrome extension categories

| Category | Use it for | Example search terms |
|---|---|---|
| Candidate discovery | Finding profiles, people, resumes, public pages | `profile`, `people`, `resume`, `LinkedIn`, `search` |
| Contact finding | Finding or validating contact information | `email`, `contact`, `phone`, `lookup`, `verify` |
| Profile enrichment | Adding context to candidate profiles | `enrich`, `company`, `social`, `data`, `profile` |
| Technical sourcing | Researching engineers, developers, and technical communities | `GitHub`, `developer`, `Stack Overflow`, `code`, `repo` |
| Productivity | Reducing browser, tab, and workflow chaos | `tab`, `clipboard`, `text`, `notes`, `session` |
| Data cleanup | Cleaning, formatting, exporting, or deduplicating data | `export`, `csv`, `dedupe`, `format`, `scrape` |
| Research / OSINT | Public web research and deeper investigation | `osint`, `metadata`, `username`, `domain`, `image` |
| Automation | Repetitive browser actions or workflow shortcuts | `automation`, `macro`, `shortcut`, `workflow` |
| Caution zone | Tools needing extra review before use | `permissions`, `privacy`, `cookies`, `read data`, `abandoned` |

---

## Google CSE categories

| Category | Use it for | Example search terms |
|---|---|---|
| People search | Finding public profiles and bio pages | `profile`, `bio`, `people`, `about` |
| Resume search | Finding resumes, CVs, and portfolios | `resume`, `CV`, `portfolio`, `vitae` |
| Technical talent | Finding engineers, researchers, builders, and contributors | `GitHub`, `developer`, `engineering`, `code`, `open source` |
| Academic / research | Finding faculty, labs, researchers, papers, and publications | `faculty`, `lab`, `paper`, `publication`, `research` |
| Company research | Finding org charts, team pages, press releases, and company context | `company`, `team`, `leadership`, `press release` |
| Conference research | Finding speakers, panels, abstracts, and event pages | `speaker`, `conference`, `agenda`, `panel`, `session` |
| Diversity sourcing | Finding associations, affinity groups, conferences, and communities | `association`, `community`, `women`, `black`, `latinx`, `veteran` |
| Geographic sourcing | Finding local directories, regional groups, and location-specific talent | `city`, `state`, `region`, `directory`, `local` |
| Niche communities | Finding specialized groups and hard-to-map talent pools | `forum`, `community`, `slack`, `discord`, `meetup` |

---

## Suggested row format

When turning the archive into Markdown or a searchable table, use this structure:

| Field | Purpose |
|---|---|
| Name | Resource/tool/search engine name |
| Link | Direct URL |
| Type | Chrome extension, Google CSE, website, guide, etc. |
| Category | Primary category |
| Tags | Additional searchable labels |
| Best for | Practical use case |
| Risk level | Low, review needed, high-permission, privacy-sensitive |
| Maintenance status | Active, unknown, deprecated, dead link, needs review |
| Notes | Human context, caveats, or examples |

---

## Example tags

```text
resource:chrome-extension
category:candidate-discovery
workflow:research
focus:technical-sourcing
risk:review-needed
status:unknown
```

```text
resource:google-cse
category:conference-research
workflow:discovery
focus:executive-search
risk:low-risk
status:active
```

---

## Naming conventions

Use lowercase, hyphenated tags.

Good:

```text
technical-sourcing
candidate-discovery
company-research
high-permission
needs-review
```

Avoid:

```text
Technical Sourcing
Candidate Discovery!!!
Random useful stuff
misc
```

`misc` is where information goes to die.

---

## Recommended minimum tags

Every resource should eventually have at least:

- `resource:*`
- `category:*`
- `workflow:*`
- `risk:*`
- `status:*`

That is enough structure to make the toolkit searchable without turning it into a taxonomy swamp.
