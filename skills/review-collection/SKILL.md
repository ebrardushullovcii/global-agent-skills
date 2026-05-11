---
name: review-collection
description: Collect public business reviews from sites like Trustpilot and BBB into local CSV files with completeness checks, resume-safe progress tracking, and supervised Chrome-based navigation. Use when the user needs review research, review archiving, pagination coverage, total review reconciliation, brand review pages, or browser-assisted collection from dynamic review sites. This skill does not bypass anti-bot, CAPTCHA, paywalls, or authentication controls.
compatibility: Works best in OpenClaw or OpenCode with local Chrome, filesystem access, internet access, and agent-browser or a compatible Chrome CDP or MCP browser tool.
license: Internal team draft unless replaced by your team
metadata:
  author: opencode
  version: "1.0.0"
---

# Review Collection

This skill helps an agent collect public reviews into local CSV files without losing progress, skipping count reconciliation, or stopping early on dynamic review sites.

Use it for review sources like Trustpilot and BBB when the user wants a local archive of reviews, page coverage, and a clean handoff for analysis.

## What This Skill Optimizes For

- Complete local capture of all accessible reviews for a target brand and source.
- Resume-safe collection with page logs and run summaries.
- Chrome-based browsing for dynamic pages, including attachment to the user's local Chrome session when appropriate.
- CSV outputs that are ready for analysis, QA, and downstream enrichment.

## Hard Guardrails

- Only collect reviews the user is allowed to access.
- Respect the target site's terms, robots guidance, rate limits, and visible access controls.
- Do not bypass CAPTCHAs, bot checks, paywalls, login walls, or other technical restrictions.
- Do not use proxy rotation, fingerprint spoofing, stealth plugins, or challenge-solving services to evade detection.
- If a site blocks access or requires a human step, pause and ask for manual intervention or switch to an official export or API.

## OpenClaw Skill Pattern

Agent skills are simple directories with a `SKILL.md` file plus optional `references/`, `assets/`, and `scripts/` folders.

This skill follows that pattern:

- `SKILL.md` contains activation guidance and the operating workflow.
- `references/csv-schema.md` defines the recommended export columns.
- `references/browser-playbook.md` explains safe Chrome, CDP, and agent-browser usage.
- `references/source-notes.md` captures source-specific reminders for Trustpilot, BBB, and similar sites.
- `assets/` includes ready-to-copy CSV and JSON templates.

## When To Use This Skill

Use this skill when the user asks to:

- collect reviews from Trustpilot, BBB, or similar review sites
- save all reviews locally as CSV files
- keep going until the full review set is captured
- capture total review count and reconcile it against collected rows
- use Chrome, Chrome MCP, remote debugging, or agent-browser to work through dynamic pages
- archive reviewer name, rating, comment, page URL, and related review metadata

## When Not To Use This Skill

Do not use this skill for:

- bypassing anti-bot systems or site defenses
- scraping private or authenticated content without permission
- collecting hidden fields that are not visible to the user
- mass collection from sites that explicitly disallow this workflow when no approved export path exists

## Preferred Tooling Order

Pick the least brittle and most compliant route first:

1. Official export, API, or user-provided dataset.
2. Direct public HTML or JSON endpoints that the site already exposes to normal browsing.
3. Headed local Chrome through `agent-browser`, Chrome MCP, or another CDP-capable browser tool.
4. Optional local parsing or cleanup with Scrapling or another parser after content is already captured.

Treat Scrapling as an optional parser or fetcher for approved workflows, not as a bypass mechanism.

If your team uses skills from `skills.sh`, the best companion browser skill for this workflow is `vercel-labs/agent-browser`.

## One-Time Setup Per Collection Run

For each brand and source, create a working folder such as:

```text
reviews/<brand>/<source>/
```

Recommended files in that folder:

- `reviews.csv` using `assets/reviews-template.csv`
- `page-log.csv` using `assets/page-log-template.csv`
- `run-summary.json` using `assets/run-summary-template.json`
- optional screenshots that prove the visible total count and final page reached

## Required Output Fields

At minimum, collect:

- brand name
- source site
- business review page URL
- source page URL where the review was seen
- reviewer name
- rating
- review title if present
- review comment or body
- review date
- review identifier if visible, otherwise a stable hashable fingerprint
- page number or ordinal position
- collected timestamp

See `references/csv-schema.md` for the full schema.

## Browser Workflow

If the page is dynamic, prefer a visible Chrome session.

Typical workflow with `agent-browser`:

```bash
agent-browser --headed --session-name brand-source open "<review-page-url>"
agent-browser wait --load networkidle
agent-browser snapshot -i --json
agent-browser screenshot --annotate
```

If the user wants the agent to work through their existing local Chrome session, connect to Chrome via remote debugging on a trusted local machine:

```bash
agent-browser --auto-connect snapshot -i --json
agent-browser --cdp 9222 snapshot -i --json
```

Notes:

- Chrome 144+ may expose remote debugging through a dynamic port; `--auto-connect` is the simplest attachment path when Chrome remote debugging is already enabled.
- Keep remote debugging bound to localhost on a trusted machine only.
- Close the shared Chrome or disable remote debugging after the run.

More operating guidance lives in `references/browser-playbook.md`.

## Collection Workflow

### Step 1: Scope The Run

Before collecting anything, lock these values:

- target brand name
- source site name
- exact review listing URL
- locale or market variant if the site has multiple versions
- sort order in use
- whether the user wants only reviews, or reviews plus seller responses and summary metrics

On BBB, separate customer reviews from complaints unless the user explicitly wants both.

### Step 2: Capture Baseline State

Before paginating, record:

- visible total review count
- overall score if visible
- current sort and filters
- landing page URL
- a screenshot or page snapshot proving the baseline numbers

Write these values to `run-summary.json` immediately.

### Step 3: Decide The Page Traversal Mode

Identify whether the site uses:

- numbered pagination
- next or previous links
- load more buttons
- infinite scroll
- nested review detail pages

Always prefer the site's visible navigation over brittle DOM-only shortcuts.

Avoid writing page-specific scraping scripts unless repeated runs justify that extra maintenance cost.

### Step 4: Collect Reviews Incrementally

On each page or batch:

- extract the visible review rows
- normalize the fields into the CSV schema
- append rows to `reviews.csv` immediately
- append the visited page state to `page-log.csv`
- update `run-summary.json` with current counts and last page reached

Do not keep everything in memory until the end.

### Step 5: Re-Snapshot After Every Page Change

When using Chrome tooling, re-snapshot after:

- clicking next page
- expanding a collapsed review
- applying a sort or filter
- loading more rows
- any navigation that changes the DOM or URL

Use the fresh refs from the latest snapshot only.

### Step 6: Continue Until Reconciliation Is Done

Do not stop just because a batch was collected successfully.

Keep going until one of these is true:

- there is no next page or load-more path left and the site clearly shows you are at the end
- collected unique reviews matches or exceeds the visible total review count
- the remaining mismatch has been documented after retrying the obvious gaps

## Completeness Rules

The agent must actively reconcile expected versus collected data.

Minimum checks:

1. Capture the displayed total review count before or early in the run.
2. Track unique collected reviews, not raw rows.
3. Dedupe by `review_id` when present, otherwise by a stable fingerprint such as source plus reviewer plus date plus rating plus normalized text.
4. Compare `expected_total_reviews` to `collected_unique_reviews` before declaring success.
5. If counts do not match, revisit likely gaps:
   - incomplete pagination
   - hidden translated text or collapsed bodies
   - locale switches
   - default sort order hiding older reviews
   - pinned or featured reviews
   - transient page load failures
6. Only finish with a mismatch if the summary clearly explains why.

## Human-Supervised Browser Behavior

If the user wants the browser to behave more like their regular browsing environment, do this safely:

- use headed Chrome instead of an invisible bursty workflow
- attach to an existing user-owned Chrome session when appropriate
- keep concurrency low, usually one tab per site session
- wait for visible page readiness instead of hammering refresh or retry loops
- use normal page navigation and visible controls first
- let the user take over for CAPTCHA, login, consent, or challenge steps

This skill aims for stable, respectful automation, not stealth or detection evasion.

## Final Deliverables

A complete run should leave behind:

- `reviews.csv`
- `page-log.csv`
- `run-summary.json`
- optional screenshots for baseline count and end-of-run proof

The summary should say whether the run is:

- `completed`
- `completed-with-notes`
- `partial-blocked`
- `partial-site-limit`

## Source-Specific Reminders

See `references/source-notes.md` for practical reminders about Trustpilot, BBB, and similar review portals.

## Quick Activation Checklist

- Confirm the user is allowed to collect the target data.
- Prefer official export paths first.
- Capture the visible total review count early.
- Append locally after each page.
- Reconcile unique rows against the expected total before stopping.
- Stop for manual help instead of bypassing protections.
