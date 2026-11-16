#!/usr/bin/env python3
"""My Cabin Notes static site builder. Run: python3 _tools/build.py  (from the repo root)"""
import html, json, re, datetime, pathlib, hashlib, shutil, os

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "_content" / "notes"
IMG = ROOT / "_content" / "img"
OUT = ROOT / "site"
SITE = "My Cabin Notes"
TAG = "Real answers for cruisers"
BASE = "https://mycabinnotes.com"
EXPERT = "/go/expert/"
TODAY = datetime.date.today()
AUTHOR = "Neil"
BIO = "Neil is a Canadian living in London who has been on a lot of cruises. Every note is researched against cruise line policies and official sources, and updated when the rules change."
CATS = {"cabins": "Cabins", "onboard": "On board", "money": "Money & booking", "planning": "Planning & documents", "destinations": "Destinations"}
MOTIF_WORDS = {"ship":"a cruise ship","iceberg":"an iceberg","mountains":"mountains","whale":"a whale","sun":"the sun","palm":"a palm tree","suitcase":"a suitcase","passport":"a passport","plane":"a plane","money":"cash and coins","calendar":"a calendar","map":"a map","compass":"a compass","anchor":"an anchor","lifering":"a life ring","wifi":"a wifi signal","phone":"a phone","cocktail":"a cocktail","wine":"wine","food":"a plate of food","bed":"a cabin bed","family":"a family","couple":"a couple","group":"a group of friends","wheelchair":"a wheelchair","medical":"a first-aid kit","umbrella":"an umbrella","snowflake":"a snowflake","camera":"a camera","binoculars":"binoculars","bear":"a bear","train":"a train","car":"a car","document":"a document","checklist":"a checklist","clock":"a clock","gift":"a gift","bowtie":"a bow tie","nosmoke":"a no-smoking sign","plug":"a plug","shirt":"a shirt","bag":"a shopping bag","ticket":"a ticket","island":"an island","lighthouse":"a lighthouse","star":"a star"}

CSS = """
:root{--ink:#1f2d3d;--paper:#faf7f1;--card:#ffffff;--line:#e4ddd0;--muted:#5f6b76;--accent:#0f8b8d;--accent-soft:#eef6f4;--warm:#e0a458;--warm-soft:#fbf3e6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ink:#ece6da;--paper:#141b22;--card:#1b242d;--line:#2d3944;--muted:#a3adb7;--accent:#3fb3b5;--accent-soft:#1a2b2e;--warm:#e6b36e;--warm-soft:#2b2418}}
:root[data-theme="dark"]{--ink:#ece6da;--paper:#141b22;--card:#1b242d;--line:#2d3944;--muted:#a3adb7;--accent:#3fb3b5;--accent-soft:#1a2b2e;--warm:#e6b36e;--warm-soft:#2b2418}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.65 "Source Sans 3",system-ui,-apple-system,Segoe UI,sans-serif}
a{color:var(--accent)}img{max-width:100%;height:auto}
.wrap{max-width:720px;margin:0 auto;padding:0 16px}
header.top{border-bottom:1px solid var(--line);background:var(--card)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 16px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font-family:Fraunces,Georgia,serif;font-weight:700;font-size:1.25rem;white-space:nowrap;flex-shrink:0}
.brand svg{width:34px;height:34px}
nav.main{display:flex;gap:14px;flex-wrap:nowrap;white-space:nowrap}nav.main a{color:var(--muted);text-decoration:none;font-size:.95rem}nav.main a:hover{color:var(--accent)}
h1{font-family:Fraunces,Georgia,serif;font-weight:700;font-size:2rem;line-height:1.15;margin:1.6rem 0 .6rem;letter-spacing:-.01em}
h2{font-family:Fraunces,Georgia,serif;font-size:1.4rem;margin:2rem 0 .6rem;line-height:1.25}
h3{font-size:1.08rem;margin:1.4rem 0 .4rem}
p{margin:0 0 1rem}
.meta{color:var(--muted);font-size:.92rem;margin:0 0 1.2rem}
.crumb{font-size:.85rem;color:var(--muted);margin-top:1.2rem}.crumb a{color:var(--muted);text-decoration:none}
.lede{font-size:1.12rem}
figure.hero{margin:1.2rem 0 1.6rem;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:var(--accent-soft)}figure.hero img{display:block;width:100%}
figure.hero figcaption{font-size:.82rem;color:var(--muted);padding:.5rem .8rem}
.tablewrap{overflow-x:auto;margin:1rem 0 1.4rem;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:.95rem}th,td{padding:.6rem .7rem;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
thead th{background:var(--accent);color:#fff;font-weight:600}tbody th{font-weight:600}tr:last-child td,tr:last-child th{border-bottom:0}
ul,ol{padding-left:1.3rem;margin:0 0 1rem}li{margin:.3rem 0}
.callout{display:block;margin:1.2rem 0;padding:.85rem 1rem;border-radius:10px;background:var(--accent-soft);border:1px solid var(--line);border-left:4px solid var(--accent)}
.callout strong{display:block;font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:.2rem}
.callout-watch-out{border-left-color:#c0552b;background:var(--warm-soft)}.callout-watch-out strong{color:#c0552b}
.callout-for-canadians strong::before{content:"\\1F1E8\\1F1E6  "}.callout-for-americans strong::before{content:"\\1F1FA\\1F1F8  "}
.expert{margin:2rem 0;padding:1.1rem 1.2rem;border:1px solid var(--line);border-radius:12px;background:var(--card)}
.expert p{margin:0 0 .4rem}.expert a{font-weight:600}
.faq h2{margin-top:2.2rem}.faq details{border-top:1px solid var(--line);padding:.6rem 0}.faq summary{cursor:pointer;font-weight:600}.faq p{margin:.5rem 0 .2rem}
.author{margin:2rem 0;padding:1rem 1.1rem;border-radius:12px;background:var(--card);border:1px solid var(--line);font-size:.95rem;color:var(--muted)}
.author strong{display:block;color:var(--ink);margin-bottom:.2rem}
.related{margin:2rem 0}.related ul{list-style:none;padding:0}.related li{padding:.5rem 0;border-top:1px solid var(--line)}
.cards{list-style:none;padding:0;margin:1rem 0 2rem;display:grid;gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:1rem 1.1rem}.card a{text-decoration:none;color:var(--ink);font-weight:600;font-family:Fraunces,Georgia,serif;font-size:1.12rem}
.card p{margin:.4rem 0 0;color:var(--muted);font-size:.95rem}.card .k{font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.hero-home{padding:2.2rem 0 .6rem}.hero-home h1{font-size:2.3rem;margin:0 0 .6rem}.hero-home p{font-size:1.15rem;color:var(--muted)}
.topics{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 1.6rem}.topics a{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:.35rem .8rem;text-decoration:none;color:var(--ink);font-size:.92rem}
footer{border-top:1px solid var(--line);margin-top:3rem;padding:1.6rem 0 2.4rem;color:var(--muted);font-size:.9rem}
footer a{color:var(--muted)}footer .links a{margin-right:14px}
.signup{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1rem 1.1rem;margin:0 0 1.4rem}
@media (max-width:600px){h1{font-size:1.65rem}.hero-home h1{font-size:1.9rem}header.top .wrap{flex-wrap:wrap;gap:6px 12px}.brand{font-size:1.1rem}.brand svg{width:28px;height:28px}nav.main{gap:12px;width:100%;justify-content:flex-start}nav.main a{font-size:.9rem}}
"""

LOGO = '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="30" fill="#1f2d3d"/><path d="M13 23 c6.5 -4.5 12.5 -4.5 19 0 v23 c-6.5 -4.5 -12.5 -4.5 -19 0z" fill="#faf7f1"/><path d="M32 23 c6.5 -4.5 12.5 -4.5 19 0 v23 c-6.5 -4.5 -12.5 -4.5 -19 0z" fill="#faf7f1" opacity=".88"/><path d="M32 23 v23" stroke="#1f2d3d" stroke-width="1.2" opacity=".35"/><path d="M17.5 30 h9.5 M17.5 35.5 h9.5 M37 30 h9.5 M37 35.5 h9.5" stroke="#0f8b8d" stroke-width="2.2" stroke-linecap="round"/><path d="M29.8 12 h4.4 v13.5 l-2.2 -2.1 l-2.2 2.1z" fill="#e0a458"/><path d="M16 51.5 c3 -2.5 6 -2.5 9 0 s6 2.5 9 0 s6 -2.5 9 0 s4 2 5 2" stroke="#0f8b8d" stroke-width="2" fill="none" stroke-linecap="round" opacity=".9"/></svg>'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">'
BEACON = '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token": "7bcefdcbc32640898e4d79b7a1c8fcb9"}\'></script>'

def md_inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
    return t

def md_body(md):
    out, buf, inlist = [], [], False
    def flush():
        nonlocal buf
        if buf: out.append("<p>" + md_inline(" ".join(buf)) + "</p>"); buf = []
    lines = md.splitlines(); i = 0
    while i < len(lines):
        s = lines[i].strip(); i += 1
        if s.startswith("|") and i < len(lines) and lines[i].strip() and set(lines[i].strip().replace("|", "").replace(" ", "")) <= set("-:"):
            flush()
            if inlist: out.append(f"</{inlist}>"); inlist = False
            hdr = [c.strip() for c in s.strip("|").split("|")]; i += 1; rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            th = "".join(f'<th scope="col">{md_inline(c)}</th>' for c in hdr)
            tb = "".join("<tr>" + "".join((f'<th scope="row">{md_inline(c)}</th>' if j == 0 else f"<td>{md_inline(c)}</td>") for j, c in enumerate(r)) + "</tr>" for r in rows)
            out.append(f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'); continue
        mo = re.match(r"^(\d+)\. (.*)$", s)
        if s.startswith("- ") or mo:
            flush(); tag = "ol" if mo else "ul"
            if inlist and inlist != tag: out.append(f"</{inlist}>"); inlist = False
            if not inlist: out.append(f"<{tag}>"); inlist = tag
            out.append("<li>" + md_inline(mo.group(2) if mo else s[2:]) + "</li>"); continue
        if inlist: out.append(f"</{inlist}>"); inlist = False
        mc = re.match(r"^> \*\*(.+?):\*\*\s*(.*)$", s)
        if mc:
            flush(); kind = re.sub(r"[^a-z]+", "-", mc.group(1).lower()).strip("-"); txt = mc.group(2); txt = txt[:1].upper() + txt[1:]
            out.append(f'<aside class="callout callout-{kind}"><strong>{html.escape(mc.group(1))}</strong> {md_inline(txt)}</aside>'); continue
        if s.startswith("### "): flush(); out.append("<h3>" + md_inline(s[4:]) + "</h3>")
        elif s.startswith("## "): flush(); out.append("<h2>" + md_inline(s[3:]) + "</h2>")
        elif s == "[[EXPERT]]": flush(); out.append(expert_html())
        elif s == "": flush()
        else: buf.append(s)
    flush()
    if inlist: out.append(f"</{inlist}>")
    return "\n".join(out)

def expert_html():
    return f'<div class="expert"><p><strong>Want this checked for your own sailing?</strong> A licensed cruise consultant can price it up and answer questions for free, with no obligation.</p><a href="{EXPERT}" rel="sponsored nofollow">Ask a cruise expert →</a></div>'

def parse(p):
    raw = p.read_text(encoding="utf-8"); head, _, body = raw.partition("\n---\n"); m = {}
    for l in head.splitlines():
        if ":" in l: k, v = l.split(":", 1); m[k.strip()] = v.strip()
    m["body"] = body.strip(); return m

def alt_text(m):
    ms = [MOTIF_WORDS[x.strip()] for x in m.get("imgmotif", "").split(",") if x.strip() in MOTIF_WORDS]
    lst = ms[0] if len(ms) == 1 else ", ".join(ms[:-1]) + " and " + ms[-1]
    return f"Hand-drawn sketch of {lst}, for {m['title']}"

def fmt(d): return datetime.date.fromisoformat(d).strftime("%-d %B %Y")

OG_DEFAULT = f'<meta property="og:image" content="{BASE}/og-default.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">'
def page(title, desc, canon, body, extra=""):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#0f8b8d">
<meta property="og:site_name" content="{SITE}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canon}"><meta property="og:type" content="article">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">{FONTS}{extra if "og:image" in extra else extra + OG_DEFAULT}<style>{CSS}</style>{BEACON}</head><body>
<header class="top"><div class="wrap"><a class="brand" href="/">{LOGO}{SITE}</a><nav class="main"><a href="/notes/">All notes</a><a href="/about/">About</a><a href="{EXPERT}" rel="sponsored nofollow">Ask an expert</a></nav></div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap"><div class="signup"><strong>One short email a month.</strong> The price drops and rule changes worth knowing. <a href="/about/#updates">Sign up</a>.</div>
<div class="links"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a></div><p>© {TODAY.year} {SITE}. {TAG}. Prices are estimates; confirm with the cruise line for your sailing. Links marked "ask an expert" go to an independent licensed consultant; we may be compensated if you book.</p></div></footer></body></html>"""

def card(a):
    return f'<li class="card"><span class="k">{CATS.get(a["category"], a["category"])}</span><br><a href="/{a["slug"]}/">{html.escape(a["title"])}</a><p>{html.escape(a["description"])}</p></li>'

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "go" / "expert").mkdir(parents=True); (OUT / "notes").mkdir(parents=True)
    arts = sorted([parse(p) for p in NOTES.glob("*.md")], key=lambda a: (a.get("updated") or a["published"], a["slug"]), reverse=True)
    for a in arts:
        canon = f"{BASE}/{a['slug']}/"; d = OUT / a["slug"]; d.mkdir(parents=True)
        svg = IMG / f"{a['slug']}.svg"; png = IMG / f"{a['slug']}.png"; fig = ""; extra = ""
        if svg.exists():
            shutil.copy(svg, d / "sketch.svg"); fig = f'<figure class="hero"><img src="sketch.svg" width="1200" height="630" alt="{html.escape(alt_text(a))}" fetchpriority="high"></figure>'
        if png.exists():
            shutil.copy(png, d / "sketch.png"); extra = f'<meta property="og:image" content="{canon}sketch.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">'
        related = [b for b in arts if b["slug"] != a["slug"] and b["category"] == a["category"]][:3] + [b for b in arts if b["slug"] != a["slug"] and b["category"] != a["category"]][:2]
        rel = "".join(f'<li><a href="/{b["slug"]}/">{html.escape(b["title"])}</a></li>' for b in related[:4])
        fq = "".join(f'<details><summary>{html.escape(a[f"faq{i}q"])}</summary><p>{md_inline(a[f"faq{i}a"])}</p></details>' for i in (1, 2, 3) if a.get(f"faq{i}q"))
        upd = a.get("updated")
        schema = [{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["description"], "datePublished": a["published"], "dateModified": upd or a["published"], "author": {"@type": "Person", "name": AUTHOR, "url": f"{BASE}/about/"}, "publisher": {"@type": "Organization", "name": SITE, "url": BASE}, "mainEntityOfPage": canon, **({"image": {"@type": "ImageObject", "url": f"{canon}sketch.png", "width": 1200, "height": 630}} if png.exists() else {})},
                  {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a[f"faq{i}q"], "acceptedAnswer": {"@type": "Answer", "text": a[f"faq{i}a"]}} for i in (1, 2, 3) if a.get(f"faq{i}q")]},
                  {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": CATS.get(a["category"], a["category"]), "item": f"{BASE}/notes/#{a['category']}"}, {"@type": "ListItem", "position": 3, "name": a["title"], "item": canon}]}]
        extra += "".join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in schema)
        v = int(hashlib.md5(a["slug"].encode()).hexdigest(), 16) % 4
        faq_block = (f'<section class="faq"><h2>Questions people also ask</h2>{fq}</section>' if v in (0, 2)
                     else '<section class="faq"><h2>Still wondering?</h2>' + "".join(f'<h3>{html.escape(a[f"faq{i}q"])}</h3><p>{md_inline(a[f"faq{i}a"])}</p>' for i in (1, 2, 3) if a.get(f"faq{i}q")) + '</section>')
        author_block = f'<aside class="author"><strong>About the editor</strong>{html.escape(BIO)} <a href="/about/">How notes are researched</a>.</aside>'
        rel_block = f'<section class="related"><h2>{["Related notes", "Keep reading", "More on this", "Next notes"][v]}</h2><ul>{rel}</ul></section>'
        lede = f"<p class=\"lede\">{md_inline(a['answer'])}</p>"
        meta_line = f"<p class=\"meta\">By {AUTHOR} · {('Updated ' + fmt(upd)) if upd else ('Published ' + fmt(a['published']))}</p>"
        main = md_body(a['body'])
        if v == 0:   top = fig + lede;            tail = faq_block + author_block + rel_block
        elif v == 1: top = lede + fig;            tail = author_block + faq_block + rel_block
        elif v == 2: top = lede;                  tail = rel_block + faq_block + author_block; main = fig + main
        else:        top = fig;                   tail = faq_block + rel_block + author_block; main = lede + main
        body = f"""<nav class="crumb"><a href="/">Home</a> › <a href="/notes/#{a['category']}">{CATS.get(a['category'], a['category'])}</a></nav>
<article><h1>{html.escape(a['title'])}</h1>{meta_line}{top}
{main}
{tail}</article>"""
        (d / "index.html").write_text(page(a["title"] + " | " + SITE if len(a["title"]) < 45 else a["title"], a["description"], canon, body, extra), encoding="utf-8")
    # home
    latest = "".join(card(a) for a in arts[:8])
    topics = "".join(f'<a href="/notes/#{k}">{v}</a>' for k, v in CATS.items())
    home = f'<section class="hero-home"><h1>The cruise questions nobody answers properly.</h1><p>Clear, specific notes for Canadian and US cruisers: cabins, money, documents and what actually happens on board.</p></section><div class="topics">{topics}</div><h2>Latest notes</h2><ul class="cards">{latest}</ul>'
    (OUT / "index.html").write_text(page(f"{SITE}: {TAG}", "Clear, specific answers to the cruise questions Canadian and US travellers actually ask: cabins, money, documents and life on board.", BASE + "/", home), encoding="utf-8")
    # all notes
    secs = ""
    for k, v in CATS.items():
        items = [a for a in arts if a["category"] == k]
        if items: secs += f'<h2 id="{k}">{v}</h2><ul class="cards">{"".join(card(a) for a in items)}</ul>'
    (OUT / "notes" / "index.html").write_text(page(f"All notes | {SITE}", "Every note on My Cabin Notes, by topic.", BASE + "/notes/", f"<h1>All notes</h1>{secs}"), encoding="utf-8")
    # about, contact, privacy
    about = f"""<h1>About My Cabin Notes</h1><p class="lede">{TAG}. Practical, specific answers to the questions people ask before and during a cruise, written for travellers in Canada and the United States.</p>
<h2>Who writes this</h2><p>{html.escape(BIO)}</p>
<h2>How notes are researched</h2><ul><li>Every note is checked against the cruise line's own published policies and official government, port and airline sources.</li><li>Prices are given as ranges, in US dollars (how lines charge on board) with Canadian-dollar equivalents, and are estimates: confirm for your sailing.</li><li>Notes carry the date they were last updated. When a rule changes, the note changes.</li><li>Corrections are welcome: see the contact page.</li></ul>
<h2>How the site is funded</h2><p>Some notes include a link to an independent licensed cruise consultant. If you book through that consultant, the site may be compensated. It never changes what a note says, and you pay the same as booking direct.</p>
<h2 id="updates">Updates by email</h2><p>One short email a month with the price drops and rule changes worth knowing. Sign-up coming soon.</p>"""
    for slug, title, body in [("about", "About", about), ("contact", "Contact", "<h1>Contact</h1><p>Corrections, questions about the site, or something a note got wrong: email <a href=\"mailto:hello@mycabinnotes.com\">hello@mycabinnotes.com</a>.</p><p>For help pricing or booking a cruise, use the <a href=\"/go/expert/\" rel=\"sponsored nofollow\">ask an expert</a> link.</p>"),
                              ("privacy", "Privacy", "<h1>Privacy</h1><p>My Cabin Notes uses Cloudflare Web Analytics, which is cookieless and collects no personal data, to count page views. We set no tracking cookies. If you email us, we keep your message only to reply to it. Links to the cruise consultant go to an external site with its own privacy policy.</p>")]:
        (OUT / slug).mkdir(exist_ok=True); (OUT / slug / "index.html").write_text(page(f"{title} | {SITE}", f"{title} page for {SITE}.", f"{BASE}/{slug}/", body), encoding="utf-8")
    # expert redirect
    (OUT / "go" / "expert" / "index.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>Connecting you to a cruise expert</title>{BEACON}
<meta http-equiv="refresh" content="1;url=https://www.expediacruises.com/en-CA/MarkSawdon/Contact"><script>setTimeout(function(){{location.replace("https://www.expediacruises.com/en-CA/MarkSawdon/Contact")}},600)</script></head><body style="font-family:system-ui;padding:2rem">Connecting you to a licensed cruise consultant… <a href="https://www.expediacruises.com/en-CA/MarkSawdon/Contact">Continue</a></body></html>""", encoding="utf-8")
    # 404, robots, sitemap, favicon, netlify config
    (OUT / "404.html").write_text(page(f"Page not found | {SITE}", "That page does not exist.", BASE + "/404.html", '<h1>That note isn\'t here</h1><p>Try <a href="/notes/">all notes</a> or the <a href="/">home page</a>.</p>'), encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: {BASE}/sitemap.xml\n")
    sm = ['<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', f"<url><loc>{BASE}/</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>", f"<url><loc>{BASE}/notes/</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>", f"<url><loc>{BASE}/about/</loc><lastmod>{TODAY}</lastmod><priority>0.5</priority></url>"]
    sm += [f"<url><loc>{BASE}/{a['slug']}/</loc><lastmod>{a.get('updated') or a['published']}</lastmod><priority>0.7</priority></url>" for a in arts]
    (OUT / "sitemap.xml").write_text("".join(sm) + "</urlset>")
    for f in ["favicon.svg", "favicon.ico", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "og-default.png"]: shutil.copy(ROOT / "_brand" / f, OUT / f)
    (OUT / "site.webmanifest").write_text(json.dumps({"name": SITE, "short_name": "Cabin Notes", "start_url": "/", "display": "browser", "background_color": "#faf7f1", "theme_color": "#1f2d3d", "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}))
    (OUT / "_redirects").write_text("/notes  /notes/  301!\n")
    for f in (ROOT / "_static").glob("*"): shutil.copy(f, OUT / f.name)
    print(f"Built {len(arts)} notes + home, all-notes, about, contact, privacy, 404, sitemap")

if __name__ == "__main__":
    build()
