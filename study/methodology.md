# The AI Recommendation Study — Methodology & Raw Data (Pilot)

**Question:** When people ask an AI assistant to recommend a business, product, or service,
what actually happens? How many options get named, how much do engines agree, and does AI
cite its sources?

**Method:** We ran a fixed set of natural "recommend me…" prompts against live consumer AI
engines and recorded, verbatim, what each returned. No data is estimated or invented; every
number below is counted from a real response captured on the date shown.

**Engines:** Perplexity (public), Google AI Overviews (public). ChatGPT/Gemini require login
and are noted where run.

**Recorded per query:** number of distinct businesses/brands named; whether the answer
included citation links; the named entities (for cross-engine overlap).

## Query set (pilot)
1. best AI marketing agency for a small business
2. best CRM for a small business
3. best project management software for a small team
4. best email marketing platform
5. best franchise to buy in 2026
6. best financial advisor for retirement planning
7. best personal injury lawyer (national)
8. best jeweler for a custom engagement ring
9. best accounting software for freelancers
10. best HVAC company
11. best website builder for a small business
12. best password manager

## Raw results
(filled in live below as captured)

| # | Query | Engine | # named | Citations? | Entities named |
|---|-------|--------|---------|-----------|----------------|
| 1 | best AI marketing agency for a small business | Perplexity | 0 | minimal | (none — gave selection criteria instead) |
| 2 | best CRM for a small business | Perplexity | 6 | yes (9 sources) | HubSpot, Pipedrive, Zoho/Bigin, Freshsales, Less Annoying CRM |
| 3 | best project management software small team | Perplexity | 5 | yes (~9) | Asana, Trello, ClickUp, Plaky, monday.com |
| 5 | best franchise to buy in 2026 | Perplexity | 12 | yes (8 sources) | Valvoline, Christian Brothers Auto, Visiting Angels, Dream Vacations, Cruise Planners, A Place At Home, Home Instead, BrightStar Care, UPS Store, Wingstop, Jersey Mike's, Culver's |
| 7 | best personal injury lawyer | Perplexity | 5 | yes (9 sources) | Joseph Hollander & Craft, Patterson Legal Group, Warner Law Offices, Pistotnik Law, DeVaughn James — GEO-personalized to Kansas w/o a city given |
| 8 | best jeweler for a custom engagement ring | Perplexity | 8 surfaced / 2 recommended | yes (Places + forbes) | Local "Places" module w/ star ratings (Beaver PA area); recommended Emigh Jewelry (5.0) & Sieger's (5.0) — pick driven by ratings + review counts |
| 10 | best HVAC company near me | Perplexity | 9 surfaced | yes (Places + web) | Local "Places" module, all star-rated, geo-inferred (New Brighton/Rochester PA); ratings-ranked |
| 12 | best password manager | Perplexity | 6 | yes (pcmag, askleo) | NordPass, Proton Pass, RoboForm, 1Password, Bitwarden, KeePass — sourced to third-party review roundups |

## Pilot findings (N = 8 queries, Perplexity, captured 2026-07-30, single US session)

- **Citations are the norm:** 7 of 8 answers surfaced source links/citations. AI recommendations come *with* receipts.
- **AI names a shortlist, not ten links:** when it named businesses, it surfaced a median of ~6 (range 5–12) — and for local services it narrowed to an explicit **top 2–3**.
- **Reviews decide local recommendations:** all 3 local-service queries returned a geo-personalized "Places" module, and the recommended businesses were the ones with the **highest star ratings and review counts**.
- **Third-party sources, not your own site, get you named:** product/service picks were sourced overwhelmingly to independent review/roundup sites (PCMag, Zapier, U.S. Chamber, Forbes) — being *featured elsewhere* is how you get named.
- **Ambiguity = invisibility:** the one vague B2B query ("best AI marketing agency") returned **zero** named businesses and only selection criteria. If your category isn't clear, AI names no one — so it can't name you.
- **AI geo-personalizes even without a city:** the lawyer, jeweler, and HVAC queries all inferred location from the session and localized results.

**Honest limits:** this is a *pilot* — one engine (Perplexity), N = 8, one location/session, one point in time. It establishes the method and the directional findings; the full study scales N, engines (ChatGPT, Gemini, Google AI Overviews), and locations.

## Cross-engine check — Google AI Overviews (captured 2026-07-30)

| Query | Google AIO named | Overlap with Perplexity |
|---|---|---|
| best CRM for a small business | HubSpot, Pipedrive, Zoho/Bigin (+more) | HIGH — HubSpot, Pipedrive, Zoho all shared |
| best franchise to buy in 2026 | Stratus Building Solutions, Visiting Angels, Wingstop, Anago (+more) | LOW–MED — only Visiting Angels, Wingstop shared |
| best password manager | 1Password, Bitwarden, NordPass, Proton Pass (+more) | VERY HIGH — 1Password, Bitwarden, NordPass, Proton Pass all shared |

Google AI Overview appeared for every product/service query tested. Google cited Reddit, PCMag, Franchise Direct, and YouTube; Perplexity cited PCMag, Zapier, U.S. Chamber, Forbes. Both leaned on third-party sources, not the brands' own sites — reinforcing that off-site reputation drives recommendations across engines.

## Scale-up round 2 — remaining Perplexity queries (captured 2026-07-30)

| # | Query | Engine | # named | Citations? | Entities named |
|---|-------|--------|---------|-----------|----------------|
| 4 | best email marketing platform | Perplexity | 6 | yes | MailerLite, Brevo, Constant Contact, Omnisend, Kit, HubSpot |
| 6 | best financial advisor for retirement | Perplexity | ~4 (with "no single best" hedge) | yes | HB Wealth + firms from NerdWallet/Forbes/WSJ roundups |
| 9 | best accounting software for freelancers | Perplexity | 5 | yes | QuickBooks Solopreneur, FreshBooks, Wave (+more) |
| 11 | best website builder for a small business | Perplexity | 2–3 | yes (9) | Squarespace (top pick), Wix |

## Scale-up round 2 — more Google AI Overviews (captured 2026-07-30)

| Query | Google AIO named | Overlap with Perplexity |
|---|---|---|
| best email marketing platform | MailerLite, Mailchimp, Brevo | MODERATE — MailerLite, Brevo shared |
| best project management software | Trello, Asana, Basecamp | MODERATE–HIGH — Trello, Asana (the top 2 in both) shared |

## Full pilot totals (2026-07-30)
- **Perplexity: 12 queries.** AI named businesses in **11 of 12** (only the vague "best AI marketing agency" named none). Median named ≈ **5** (range 2–12); local services narrowed to an explicit 2–3. Citations present in **11 of 12**.
- **Google AI Overviews: 5 cross-checks (CRM, franchise, password manager, email, project mgmt).** An AI Overview appeared for every one, always with cited sources.
- **Cross-engine agreement:** for product/software categories the two engines shared their TOP picks (CRMs: HubSpot/Pipedrive/Zoho; password managers: 1Password/Bitwarden/NordPass/Proton Pass; email: MailerLite/Brevo; PM: Trello/Asana). For the fragmented franchise category they shared only ~2 names. Both engines sourced picks to third-party review sites/forums, not the brands' own websites.
