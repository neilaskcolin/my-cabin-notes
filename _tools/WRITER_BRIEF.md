# Writer brief: My Cabin Notes, block 1

My Cabin Notes (mycabinnotes.com) is a brand-new cruise guide for Canadian and US cruisers. Tagline: "Real answers for cruisers." Edited by Neil, a Canadian living in London who has been on a lot of cruises.

You are writing a fresh page on a topic an older site (cruisequestionscanada.com) already covers. That old page is a FACT SOURCE ONLY. The new page must be written from scratch: new title, new structure, new sentences. Google must never see the two as duplicates. Never copy a sentence or a table from the old page. Reuse facts, not wording.

## Files
- Old page (facts only): /home/claude/cqc/_content/articles/<old_slug>.md
- Write the new page to: /home/claude/mcn/_content/notes/<new_slug>.md
- Topic map: /home/claude/mcn/_tools/block1.tsv
- Checker: `python3 /home/claude/mcn/_tools/check_note.py <new_slug> ...` must print OK for every page.

## Length and depth
750–1,400 body words (over 1,000 when the topic deserves it). These topics already proved Google wants them, so each page must be the best answer on the web for its question: complete, specific, practical. Never pad.

## Audience
Canadian AND US cruisers. Prices in USD first (how lines charge on board) with a rough CAD equivalent where useful ("about US$20, roughly C$27–28"). Cover US and Canadian specifics where they differ: home ports (Seattle, Vancouver, Miami, Port Canaveral, Galveston, New York), documents, US CBP vs Canada's CBSA rules, insurance. Some topics are inherently Canadian (CAD vs USD, ESTA for Canadians, Toronto to Miami): keep the Canadian focus but write so a US reader follows.

## Voice
Clear, friendly, practical notes from someone who knows ships. Use "you". Do NOT invent personal anecdotes, quotes, statistics or named people. No "when I sailed". The "notes" feel comes from crisp, scannable, specific writing, not fake stories. Short paragraphs (2–4 sentences). Canadian spelling. Avoid: delve, in conclusion, whether you're, it's important to note, navigate, embark on, look no further, game-changer, seamless. Few em dashes.

## Accuracy
Prices and policies change: give ranges, say "at recent prices" / "check for your sailing". Keep facts consistent with the old page (recently fact-checked); if you know something there is wrong, fix it and say so in your reply. Never invent.

## Structure
- First paragraph answers the question directly in 2–3 sentences.
- 5–8 `## ` sections phrased like real searches; `### ` where useful. Vary structure from page to page.
- At least 3 of: table, numbered list, bullet list, callouts. Callout = one line `> **Label:** text`, Label one of: Tip, Watch out, Good to know, Example, Quick math, For Canadians, For Americans. 2–4 per page.
- Exactly one line `[[EXPERT]]` near the end, before a short closing section.
- 2–4 links to OTHER pages in block1.tsv, as `[descriptive anchor](/<new_slug>/)`. No other links. No links to the old site.
- No H1 in the body.

## Front matter (one line each)
title: <new, compelling, under 60 chars, different from the old title>
slug: <new_slug>
category: <from block1.tsv>
description: <140–155 chars, makes someone click>
answer: <direct answer, under 55 words>
faq1q / faq1a / faq2q / faq2a / faq3q / faq3a: <three genuinely different questions, 1–3 sentence answers>
imgmotif: <2–4 from: ship, iceberg, mountains, whale, sun, palm, suitcase, passport, plane, money, calendar, map, compass, anchor, lifering, wifi, phone, cocktail, wine, food, bed, family, couple, group, wheelchair, medical, umbrella, snowflake, camera, binoculars, bear, train, car, document, checklist, clock, gift, bowtie, nosmoke, plug, shirt, bag, ticket, island, lighthouse, star>
published: 2026-11-14

Then a line `---` then the body.

## Finish
Run the checker on all your pages until every one prints OK. Reply with a table (new slug, title, words) and any factual doubts.
