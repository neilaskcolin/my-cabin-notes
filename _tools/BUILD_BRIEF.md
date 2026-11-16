# My Cabin Notes: build brief

**Domain:** mycabinnotes.com (bought).
**Tagline:** Real answers for cruisers.
**Audience:** Canadian and US cruisers. Prices in USD first (how cruise lines charge), with rough CAD where useful.
**Purpose:** a genuinely useful cruise Q&A guide that earns search traffic, sends enquiries to a licensed cruise consultant through one "ask an expert" link per page, and later sells a printable cruise planner.
**Editor:** Neil, a Canadian living in London who has been on a lot of cruises. (First name only. Never invent credentials.)

This brief exists because the previous site, cruisequestionscanada.com, grew to ~300 impressions a day in three weeks and then fell to near zero on 14 October 2026. The most likely cause was Google's scaled content abuse policy: ~400 AI-written, same-shaped pages published in three weeks on a brand-new domain, no author, no real links, every page funnelling to one referral link. The old site stays live untouched. The new site must not repeat the pattern.

---

## 1. The rules that are not negotiable

1. **Slow.** Launch with 20 pages. Then add 2 to 3 pages a week, never a batch. No more than ~15 new pages in any month.
2. **Small.** Fewer, deeper pages. 750–1,200 words of real substance each. Nothing under 700.
3. **Real.** Every page carries first-hand detail where possible: Neil's own cruise photos, what a cabin thermostat actually looks like, a photo of a daily programme, a real receipt with the price blurred. Photos beat sketches. Never invent experiences, quotes, people or statistics.
4. **Different shapes.** Pages must not share a template. Vary openings, sections, tables, lists, callouts and length. No two pages with the same set of H2s.
5. **One expert link per page**, plain text, marked `rel="sponsored nofollow"`, going via a `/go/` page that is set to noindex and disallowed in robots.txt. No floating buttons. No repeated sales copy.
6. **Fresh wording.** Nothing copied from the old site. Reuse facts, not sentences. New titles, new addresses.
7. **Clean addresses from day one, never changed:** `mycabinnotes.com/cruise-cabin-temperature/` (root level, trailing slash). Sitemap, canonical tags and internal links all use exactly this form.
8. **Honest dates.** Each page shows its real published date and real updated date. No backdating.
9. **Never block Google quoting the answer.** No `data-nosnippet`.
10. **Deploy from GitHub, not drag-and-drop**, so Netlify Functions work (click dashboard) and nothing is ever "uploaded but not published".

---

## 2. Brand and design

- **Name:** My Cabin Notes. Logo: a simple notebook or luggage-tag mark. Keep it clean.
- **Feel:** a well-kept notebook. Calm, trustworthy, slightly premium. Not a sales site.
- **Colours:** deep navy ink (#1f2d3d), cream paper (#faf7f1), one accent (sea teal #0f8b8d), a warm highlight (#e0a458). Dark mode supported.
- **Type:** a readable serif for headings (e.g. Fraunces or Source Serif), a clean sans for body (Inter or Source Sans).
- **Layout:** single column, 720px max text width, generous spacing. Mobile first.
- **Page parts (vary the order and presence from page to page):** title; byline "By Neil · Updated 9 Nov 2026"; a direct answer in the first paragraph (no "Quick answer" box); photo or illustration with real alt text; 5–8 H2 sections; tables / numbered steps / bullets / callouts; 3 FAQs; "About the editor" box; related notes (3–5 links); one expert link; footer.
- **Callout labels:** Tip, Watch out, Good to know, Example, Quick math, For Canadians, For Americans.
- **Structured data:** Article (author = Person "Neil"), FAQPage, BreadcrumbList, ImageObject.
- **Pages beyond articles:** Home (latest notes + topics), About (who Neil is, how notes are researched, how the site is funded, in plain words), Contact, Privacy, Ask an expert (the `/go/` redirect), Planner (later), 404.

---

## 3. Site setup, step by step

1. **GitHub.** Create a private repo `my-cabin-notes`. Put the whole site in it (static HTML built by a small Python generator, same approach as before; or Astro if preferred).
2. **Netlify.** New site from the GitHub repo. Build command and publish folder set in `netlify.toml`. Check "auto publishing" is on.
3. **Domain.** In Netlify: Domain management, add mycabinnotes.com. At the registrar: point nameservers to Netlify's four nameservers (dns1–dns4.p0x.nsone.net as shown by Netlify). Remove any parking records. Wait for HTTPS to show "Netlify certificate active".
4. **Canonical host.** Netlify: set `https://mycabinnotes.com` as primary so `www` and `http` redirect to it.
5. **Files at the root:** `robots.txt` (Allow all, Disallow /go/, Sitemap line), `sitemap.xml`, `_redirects` (only `/go/expert /go/expert/ 301` style housekeeping, nothing else), `404.html`, favicons, `site.webmanifest`.
6. **Analytics:** Cloudflare Web Analytics beacon (cookieless) on every page. Beacon also on the `/go/` page so expert clicks are counted.
7. **Click dashboard:** copy the Cornwall build (Netlify Function + Blobs + `/dashboard/` page). Event types: `expert` (click on the expert link, with the page), `share`, `planner`. Set `TRACK_KEY` with context `production`, then redeploy.
8. **Search Console.** Add a Domain property for mycabinnotes.com (DNS TXT verification). Also add a URL-prefix property `https://mycabinnotes.com/` (needed for the disavow tool). Submit `sitemap.xml`.
9. **Bing Webmaster Tools.** Import from Search Console (free, two clicks).
10. **Email list.** Free tier of MailerLite or Buttondown. One sign-up box in the footer: "One short email a month with the price drops worth knowing."
11. **Pinterest.** Business account, boards: Cruise Cabin Tips, Alaska Cruise Planning, Cruise Money & Booking, First Cruise. Pin every new page with its photo.

---

## 4. Launch content: block 1 (the 20 topics that already proved demand)

These ranked on page 1 or drew the most searches on the old site before 14 October. Write each from scratch with a new title and address. Old slugs are listed only as a fact source.

| # | New address | Topic | Old page (facts only) |
|---|---|---|---|
| 1 | /cruise-ship-emergency-announcements/ | What ship announcements and codes mean | cruise-ship-emergency-announcements-explained |
| 2 | /pay-for-cruise-cad-or-usd/ | Paying in CAD or USD | paying-cad-vs-usd-cruise |
| 3 | /cruise-cabin-temperature/ | Why cabins run hot or cold, thermostat tricks | cruise-cabin-temperature-control-thermostat |
| 4 | /cruise-military-discounts/ | Military, first-responder and senior discounts by line | military-first-responder-senior-discounts-cruise |
| 5 | /cruise-vs-land-vacation-cost/ | Cruise vs flight-and-hotel, real comparison | cruise-vs-flight-hotel-vacation-cost-compare |
| 6 | /alaska-cruise-from-vancouver-cost/ | Alaska from Vancouver, real budget | alaska-cruise-cost-vancouver-realistic-budget |
| 7 | /noisy-cruise-cabin/ | Noisy cabin: what to do, what you can ask for | cruise-cabin-noise-complaints-what-to-do |
| 8 | /send-postcards-from-cruise-ship/ | Mail and stamps at sea | cruise-ship-mailbox-postcards-stamps |
| 9 | /cruise-ship-time-zones/ | Ship's time and time zones | cruise-cabin-jet-lag-time-zones |
| 10 | /cruise-ship-duty-free/ | Is duty-free cheaper; US and Canadian limits | cruise-shopping-onboard-duty-free |
| 11 | /toronto-to-miami-cruise/ | Toronto to Miami for a cruise | toronto-miami-caribbean-cruise |
| 12 | /cruising-with-hearing-or-vision-loss/ | What ships provide | cruising-hearing-vision-impairments |
| 13 | /cruise-ship-photo-etiquette/ | Photographing crew and guests | cruise-ship-photography-etiquette-crew-guests |
| 14 | /do-canadians-need-esta-for-cruise/ | Documents for Canadians sailing from US ports | canadians-visa-esta-cruise-us-port |
| 15 | /large-group-dining-on-a-cruise/ | Seating a group of 20 | group-dining-cruises-20-people |
| 16 | /cruise-cancelled-by-cruise-line/ | When the line cancels: refunds and rights | what-happens-cruise-cancelled-by-line |
| 17 | /sail-away-party/ | What it is, where to stand | sail-away-party-what-is-it |
| 18 | /how-many-shore-excursions/ | How many excursions to book | how-many-excursions-book-per-cruise |
| 19 | /cpap-on-a-cruise/ | CPAP rules by line (biggest search demand) | bringing-cpap-machine-cruise-ship |
| 20 | /cruise-terms-explained/ | Cruise words decoded | cruise-terminology-decoded |

The remaining 380 topics, ranked by past performance and already split into blocks of 20, are in `my-cabin-notes-page-blocks.csv`. Release them at 2–3 a week, best first, rewritten fresh each time.

---

## 5. Writing brief for every page

- **Open with the answer** in 2–3 sentences. Then earn the depth.
- **750–1,200 words.** 5–8 H2s phrased the way people search. H3s where useful.
- **At least three of:** table, numbered steps, bullets, callouts. Vary which, page to page.
- **Something first-hand** on every page where possible: a photo Neil took, a specific observation, a real price seen on a real sailing (month and ship named, numbers rounded).
- **Both audiences:** US and Canadian ports, documents, border rules, insurance where they differ. Prices "at recent prices", with "check for your sailing".
- **Accuracy over confidence.** Ranges, not fake precision. Fix anything the old page got wrong. Never invent.
- **Voice:** clear, friendly, practical notes. "You." No filler ("delve", "whether you're", "it's important to note", "seamless", "game-changer"). Sparse em dashes.
- **Links:** 2–4 to other notes on the site, descriptive anchors. One expert link. No links to the old site.
- **Front matter:** title (under 60 chars), description (140–155 chars), category, published, updated, image, alt text, 3 FAQs.
- **Checker before publish:** word count, one expert link, no banned phrases, no sentence shared with any other page, all links resolve, image present.

---

## 6. Launch sequence

1. Build the template, home, about, contact, privacy, 404, `/go/` page.
2. Write block 1 (20 pages). Add real photos where Neil has them.
3. Checks: every page passes the checker; mobile and dark-mode screenshots; no duplicate sentences across pages; every link works.
4. Go live. Submit sitemap in Search Console and Bing. Request indexing for all 20 over two days.
5. Add one natural in-text link from Cornwall Days Out and one from Devon Days Out to the new site (one page each, not sitewide, not reciprocal).
6. Pin all 20 pages on Pinterest. Post two genuinely helpful answers in cruise groups, linking only where it answers the question.
7. Week 2 onwards: 2–3 new pages a week from the blocks file, each with indexing requested on publish. Resubmit sitemap after each.
8. Monthly: export Search Console (Pages, Queries, Chart), compare, deepen the pages that get impressions but few clicks (titles and descriptions first).
9. Month 3: add the planner page and the email list offer.

---

## 7. Things never to do on this site

- Publish more than ~15 pages in a month.
- Change page addresses after launch.
- Backdate anything.
- Buy links, guest posts on general "anything" blogs, directory packages, or "speedy indexing" services.
- Copy wording between pages or from the old site.
- Add a floating sales button or more than one expert link per page.
- Put the real consultant's name anywhere on the site.

---

## 8. What success looks like

- **Month 1:** indexed, crawled regularly (Search Console crawl stats rising), 20–40 pages live.
- **Month 3:** first page-1 rankings on cabin and money topics; 50–150 impressions a day; first expert clicks in the dashboard.
- **Month 6:** 300+ impressions a day, a few clicks a day, planner on sale, list growing.

If a Google update knocks it back, do not react within the week. Check crawl stats and the comparison export, fix only what is clearly wrong, and keep publishing slowly.
