# My Cabin Notes (mycabinnotes.com)

Static cruise Q&A site for Canadian and US cruisers. Editor: Neil. Netlify publishes the `site/` folder from `main`; there is no Netlify build step, so `site/` must be rebuilt and committed whenever content changes.

## Layout
- `_content/notes/*.md` — one markdown file per note (front matter + body). Slug = filename = URL `/<slug>/`.
- `_content/img/<slug>.svg|png` — sketch illustration per note (generated).
- `_tools/build.py` — builds everything into `site/` (`python3 _tools/build.py`).
- `_tools/check_note.py` — per-page checks (`--all`) and cross-page structure check (`--structure`). Both must pass before committing.
- `_tools/sketches.py --png <slug>` — renders the sketch for a new note.
- `_tools/WRITER_BRIEF.md` — the writing rules for every note. Read before writing or editing.
- `_tools/BUILD_BRIEF.md` — the site brief: what went wrong on the old site and the rules that stop it happening again.
- `_tools/page-blocks.csv` — the remaining ~380 topics in priority order (Block, Order). Block 1 is live. Take the next unused row in Block order when adding a page. Column "Old URL" points to the old site (cruisequestionscanada.com) as a FACT source only; never copy its wording.
- `_static/*` — files copied to the site root as-is (Google verification file). Do not remove.
- `_brand/` — logo, favicons, share image.

## Rules that are not negotiable
1. Never change a slug or URL after publishing. Never add redirects for content moves; there are none.
2. New pages: TWO per daily run, so up to 14 in any 7 days (Neil's decision, 17 Nov 2026, against the slower pace in BUILD_BRIEF). Never more than two in a run. Quality rules below still apply to every page.
3. Every page passes `check_note.py --all` and `--structure` (no two pages share headings or shape; <3% 8-word overlap with the old page).
4. Exactly one `[[EXPERT]]` link per note. No floating buttons, no extra sales copy. Never name the consultant on the site.
5. Real dates only: `published` is the day it first went live; `updated` only when the body materially changes. No backdating.
6. No `data-nosnippet`. Never hide the answer from Google.
7. Fresh wording. Reuse facts, never sentences, from the old site or other notes.
8. Never invent experiences, quotes, people, prices or statistics. Prices "at recent prices" with ranges.
9. Work on a branch; `main` deploys to production.

## Build and check
```
python3 _tools/check_note.py --all
python3 _tools/check_note.py --structure
python3 _tools/sketches.py --png <new-slug>   # new notes only
python3 _tools/build.py                        # regenerates site/ incl. sitemap.xml
```
Commit `_content`, `_tools`, `_static`, `_brand` and the rebuilt `site/` together.
