# Source Notes

These notes are intentionally high level so the skill stays resilient as site layouts change.

## Trustpilot

- Capture the business profile URL exactly as shown.
- Record the displayed total review count near the business rating summary before paginating.
- Preserve labels such as verified, invited, or company reply when visible.
- Capture `date of experience` separately from publication date when the site shows both.
- Watch for language, market, or sort changes that can alter which reviews are visible.
- If a review body is collapsed, expand it before saving the final row text.
- Keep the default listing URL and the final page URL in the run summary.

## BBB

- Separate customer reviews from complaints unless the user explicitly wants both datasets.
- Do not mix accreditation or business profile metadata into review rows; keep that in the run summary if needed.
- Capture review status, business response text, and response date when available.
- Record the displayed review count for the specific section being collected.
- Some BBB pages surface only a subset of profile content unless the correct tab or section is active; verify the active section before counting.

## Other Review Sources

For Google, Yelp, G2, Capterra, or similar sources, reuse the same pattern:

- lock the exact listing URL
- capture the visible total count early
- log sort and filter state
- paginate until the end of the accessible set
- dedupe and reconcile before stopping

## Common Failure Modes

- total review count was captured from the wrong tab or section
- the site defaulted to a locale-specific page that hides part of the dataset
- only the first batch of load-more results was saved
- collapsed review text was not expanded before extraction
- seller responses were captured inconsistently
- duplicate rows were created after refresh or back navigation

When counts are off, check those issues before concluding the site is incomplete.
