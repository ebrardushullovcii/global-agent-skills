# Browser Playbook

Use this playbook when the review source is dynamic or hard to capture with simple HTTP requests.

## Preferred Browser Mode

Start with a visible local Chrome session when possible.

Why:

- easier debugging
- clearer handoff if the user needs to take over
- better fit for dynamic pages with expanding panels, lazy loading, and consent flows

## Safe Chrome Attachment Options

### Option 1: Attach To Existing Local Chrome

Use this when the user already has Chrome open on a trusted machine.

With `agent-browser`:

```bash
agent-browser --auto-connect snapshot -i --json
```

This is especially useful when Chrome remote debugging is already enabled and the port is dynamic.

### Option 2: Connect By Explicit CDP Port

Use this when Chrome was launched with a fixed localhost port such as `9222`.

```bash
agent-browser --cdp 9222 snapshot -i --json
```

### Option 3: Persistent Session Name

Use a named session for resume-safe work:

```bash
agent-browser --headed --session-name brand-source open "<url>"
```

If your environment exposes Chrome through an MCP server instead of `agent-browser`, use the same operating loop: attach to local Chrome, open the listing page, wait for load, capture the visible state, append extracted rows locally, paginate, then reconcile counts before stopping.

## Security Notes For Remote Debugging

- Only enable remote debugging on a trusted local machine.
- Keep the debugging endpoint on localhost only.
- Remember that CDP grants broad browser control.
- Turn off remote debugging or close the browser after the run.

## Practical Navigation Pattern

Use this loop:

1. Open the listing page.
2. Wait for the page to settle.
3. Take a snapshot of interactive elements.
4. Extract visible reviews.
5. Click the next visible control.
6. Wait again.
7. Re-snapshot.
8. Append locally.

Example:

```bash
agent-browser --headed --session-name trustpilot-acme open "<url>"
agent-browser wait --load networkidle
agent-browser snapshot -i --json
agent-browser screenshot --annotate
```

After any navigation or major DOM change, refresh refs with a new snapshot.

## Browser Behavior Best Practices

Aim for stable, respectful automation:

- use one session per source run
- keep concurrency low
- prefer explicit waits over tight retry loops
- interact through visible controls before resorting to JS evaluation
- append results to disk after each page or batch
- keep screenshots or snapshots for QA when counts matter

## What To Do If The Site Pushes Back

If you hit:

- CAPTCHA
- abuse or bot challenge pages
- forced login
- repeated hard blocks
- terms or consent flows that require a human decision

Then:

1. stop automated progression
2. ask the user to complete the step manually if allowed
3. resume after the user confirms the browser is ready
4. if the site still blocks the workflow, switch to an approved export or API path

Do not introduce stealth tooling, challenge solvers, or evasion techniques.

## Optional Use Of Scrapling

Scrapling can be useful after content is already available to parse locally or through an approved fetch path.

Good uses:

- normalize saved HTML
- extract fields from already captured pages
- run adaptive selectors on locally saved content

Avoid using Scrapling features whose purpose is to bypass anti-bot systems for this workflow.
