# Review CSV Schema

Use this schema for `reviews.csv` unless the user asks for a smaller export.

## Recommended Columns

| Column | Required | Notes |
| --- | --- | --- |
| `run_id` | Yes | Stable identifier for the collection run. |
| `source_site` | Yes | Example: `trustpilot`, `bbb`. |
| `brand_name` | Yes | Target business or brand. |
| `business_review_page_url` | Yes | Canonical listing page for the brand on that source. |
| `source_page_url` | Yes | Exact page URL where this row was collected. |
| `source_page_number` | No | Numbered page index if the site exposes it. |
| `source_position` | No | Row position on the page or batch. |
| `review_id` | Preferred | Source-native review identifier when visible. |
| `review_fingerprint` | Yes | Stable fallback dedupe key if `review_id` is absent. |
| `reviewer_name` | Yes | Visible display name only. |
| `reviewer_location` | No | Country, city, or profile location if shown. |
| `review_language` | No | Language label if shown or inferred from the page. |
| `rating_value` | Yes | Numeric rating value. |
| `rating_scale` | Yes | Usually `5`. |
| `review_title` | No | Title or headline if present. |
| `review_comment` | Yes | Body text. Preserve line breaks if practical. |
| `review_date` | Yes | Publication date shown by the site. |
| `experience_date` | No | Capture separately when sites expose date of experience. |
| `review_labels` | No | Pipe-delimited labels such as `verified|invited`. |
| `verified_flag` | No | `true` or `false` when a verification badge is visible. |
| `business_response` | No | Seller or business reply text. |
| `business_response_date` | No | Reply date if visible. |
| `helpful_count` | No | Helpful or useful vote count if visible. |
| `sort_order` | No | Example: `most-recent`, `default`. |
| `collected_at_utc` | Yes | ISO-8601 UTC timestamp for when the row was saved. |
| `notes` | No | Free text for row-level oddities. |

## Dedupe Guidance

Preferred order:

1. `review_id`
2. stable site URL to the review
3. fingerprint of normalized reviewer name, date, rating, and text

If using a fingerprint, normalize whitespace, casing, and obvious punctuation variants before generating it.

## Minimum Viable Export

If the user wants a lighter CSV, keep at least:

- `source_site`
- `brand_name`
- `business_review_page_url`
- `source_page_url`
- `review_id` or `review_fingerprint`
- `reviewer_name`
- `rating_value`
- `review_comment`
- `review_date`
- `collected_at_utc`

## Page Log Schema

Use `page-log.csv` to track traversal and resume points.

Recommended columns:

| Column | Required | Notes |
| --- | --- | --- |
| `run_id` | Yes | Same value used in `reviews.csv`. |
| `source_site` | Yes | Source name. |
| `brand_name` | Yes | Target brand. |
| `page_sequence` | Yes | Monotonic traversal index. |
| `source_page_number` | No | Page number if visible. |
| `source_page_url` | Yes | Exact URL visited. |
| `visible_review_count_on_page` | No | Count of rows seen on that page or batch. |
| `collected_unique_total_after_page` | Yes | Running unique total after processing the page. |
| `next_action` | No | Example: `next-click`, `load-more`, `end-of-list`. |
| `captured_at_utc` | Yes | ISO-8601 UTC timestamp. |
| `notes` | No | Retry, block, or mismatch notes. |
