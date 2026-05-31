# Chrome Extension Vetting Guide

Chrome extensions can be incredibly useful for sourcing. They can also be tiny little permission goblins living in your browser.

Use this guide before installing or recommending any extension from the archive.

---

## Fast vetting checklist

Before installing a Chrome extension, check:

- Who built it?
- Does the developer have a real website?
- Is there a privacy policy?
- When was it last updated?
- How many users does it have?
- What do recent reviews say?
- What permissions does it request?
- Does it read or change data on websites?
- Does it interact with LinkedIn, email, cookies, contacts, or candidate data?
- Would your company allow it?

If you cannot answer those questions quickly, it belongs in `needs-review`.

---

## Permission risk ladder

| Risk level | What it usually means | Suggested tag |
|---|---|---|
| Low | Narrow permissions, simple utility, no sensitive data access | `risk:low-risk` |
| Medium | Reads page content, modifies tabs, interacts with specific sites | `risk:review-needed` |
| High | Reads/changes data across many sites, touches cookies/email/contacts, unclear vendor | `risk:high-permission` |
| Very high | Unclear ownership, suspicious redirects, abandoned extension, invasive permissions | `risk:privacy-sensitive` |

---

## Red flags

Be careful with extensions that:

- Request access to all websites
- Read or change data on every page you visit
- Touch email, LinkedIn, cookies, contacts, or candidate data
- Have no clear developer or company behind them
- Have no privacy policy
- Have not been updated in years
- Have recent reviews mentioning breakage, spam, redirects, or unexpected behavior
- Were acquired or changed ownership without clear disclosure
- Promise suspiciously magical data extraction

The more sensitive the data, the less cute the shortcut becomes.

---

## Recruiting-specific caution

Recruiters often work with candidate data, internal hiring data, company systems, and sourcing platforms. That makes browser tools extra sensitive.

Use extra caution with anything that interacts with:

- LinkedIn
- Gmail or Outlook
- ATS/CRM systems
- Candidate profiles
- Contact-finding workflows
- Cookies or logged-in sessions
- Internal company pages
- Downloaded candidate lists

A tool might be fine for personal browsing and still be inappropriate for a corporate recruiting workflow.

---

## Suggested review workflow

### 1. Identify the use case

What is the extension supposed to help with?

Examples:

- Save tabs
- Copy links
- Find emails
- Export profiles
- Capture notes
- Clean data
- Search faster

If the use case is vague, the risk is harder to justify.

### 2. Review permissions

Ask:

- Does the permission match the job?
- Is it asking for more than it needs?
- Could this expose candidate or company data?

### 3. Check maintenance

Look for:

- Last updated date
- Recent reviews
- Developer activity
- Website status
- Support/contact information

### 4. Test safely

If testing is appropriate:

- Use a non-work browser profile first
- Avoid logged-in company systems
- Do not test on sensitive candidate data
- Remove it if anything feels off

### 5. Tag it

Use tags like:

```text
resource:chrome-extension
category:productivity
workflow:research
risk:review-needed
status:unknown
```

---

## Recommended status labels

| Status | Meaning |
|---|---|
| `active` | Appears maintained and usable |
| `unknown` | Not enough information yet |
| `needs-review` | Should be checked before recommending |
| `deprecated` | No longer recommended or replaced by something better |
| `dead-link` | Link no longer works |
| `blocked-by-policy` | May violate company or platform policy |

---

## When to remove or flag an extension

Move it to caution zone, flag it, or remove it if:

- It no longer exists
- It redirects to something unrelated
- It appears abandoned
- It has suspicious reviews
- It requests excessive permissions
- It touches sensitive data without a clear reason
- It violates platform or company policy

---

## Bottom line

The best sourcing stack is not the biggest stack. It is the stack you can trust.

Install fewer things. Understand what they do. Keep the useful ones. Ruthlessly eject the weird ones.
