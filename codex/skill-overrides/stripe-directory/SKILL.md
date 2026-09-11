---
name: stripe-directory
description: Search Stripe Directory when the user explicitly wants to use that directory to find or compare service providers.
---

# Stripe Directory

Use this skill for an explicit Stripe Directory discovery request. Ordinary hosting, database, vendor or product research should use the available sources best suited to the task; it does not require Stripe Directory.

Use the installed Stripe CLI's `stripe directory search "<query>" --format json` when available. Consult its current help for filters needed by the request. Search with the user's requirements, compare the returned providers, and link the evidence supporting recommendations. Report sparse or inconclusive results rather than padding the list.

Discovery does not authorize purchases or provisioning. If the user asks to buy or provision a service, establish the actual price, account and intended action, and follow the relevant supported workflow within the user's authorization. Do not install tools, create accounts or move money merely to complete a provider search.
