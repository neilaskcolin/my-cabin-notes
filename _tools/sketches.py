#!/usr/bin/env python3
"""Sketch illustrations for every article.
Reads imgmotif / imgalt from front matter, composes a hand-drawn style SVG (1200x630)
into _content/img/<slug>.svg and renders a PNG (for og:image) with Playwright.
Usage: python3 sketches.py [--png] [slug ...]
"""
import re, sys, glob, os, hashlib, math

ROOT = "/home/claude/mcn"
ART = f"{ROOT}/_content/notes"
OUT = f"{ROOT}/_content/img"
ACCENTS = [("#0f8b8d", "#eef6f4"), ("#1f2d3d", "#eef0f3"), ("#e0a458", "#fbf3e6"), ("#5b7b8f", "#eef2f5")]
INK = "#1f2d3d"

# Each motif is drawn in a 100x100 box. {a} = accent colour, {s} = soft fill, {w} = white.
M = {
"ship": '<path d="M8 62h84l-10 18H20z" fill="{a}"/><path d="M22 62V48h56v14" fill="{w}"/><path d="M30 48V38h38v10" fill="{s}"/><rect x="44" y="26" width="9" height="12" fill="{a}"/><circle cx="32" cy="55" r="2.2"/><circle cx="42" cy="55" r="2.2"/><circle cx="52" cy="55" r="2.2"/><circle cx="62" cy="55" r="2.2"/><circle cx="72" cy="55" r="2.2"/><path d="M4 86c8-4 14 4 22 0s14 4 22 0 14 4 22 0 14 4 26 0" fill="none"/>',
"iceberg": '<path d="M20 70l14-30 10 8 12-22 10 20 8-6 10 30z" fill="{w}"/><path d="M44 48l6 22M66 46l-4 24" fill="none"/><path d="M14 70h74" fill="none"/><path d="M26 70l8 16h34l10-16" fill="{s}" stroke-dasharray="4 4"/>',
"mountains": '<path d="M6 80l26-44 14 20 16-30 32 54z" fill="{s}"/><path d="M26 46l6-10 6 10-6-3zM56 36l6-10 7 12-7-3z" fill="{w}"/><path d="M6 80h88" fill="none"/>',
"whale": '<path d="M12 60c4-16 30-22 50-16 12 4 18 10 24 4l6-8-2 14c-4 10-14 16-30 18-24 3-46-2-48-12z" fill="{a}"/><path d="M14 62c20 8 46 8 66 0" fill="none" stroke="{w}"/><circle cx="26" cy="54" r="2" fill="{w}" stroke="none"/><path d="M40 40c-2-8 2-14 0-20M40 30c-6-4-10-2-12 0M40 30c6-4 10-2 12 0" fill="none"/><path d="M4 80c10-4 16 4 26 0s16 4 26 0 16 4 26 0" fill="none"/>',
"sun": '<circle cx="50" cy="50" r="18" fill="{a}"/><path d="M50 18v-10M50 92v-10M18 50H8M92 50H82M27 27l-7-7M80 80l-7-7M73 27l7-7M20 80l7-7" fill="none"/>',
"palm": '<path d="M50 92c-2-24 0-44 6-60" fill="none" stroke-width="5"/><path d="M56 32c-14-10-30-8-40 2 14-2 26 0 40-2zM56 32c10-14 26-16 36-8-12 0-24 2-36 8zM56 32c-4-14 0-24 10-28-2 10-6 18-10 28zM56 32c14 0 26 8 30 20-10-8-20-14-30-20z" fill="{a}"/><path d="M30 92h44" fill="none"/>',
"suitcase": '<rect x="18" y="34" width="64" height="48" rx="6" fill="{a}"/><path d="M38 34v-10h24v10" fill="none"/><path d="M34 34v48M66 34v48" fill="none" stroke="{w}"/><circle cx="28" cy="86" r="3"/><circle cx="72" cy="86" r="3"/>',
"passport": '<rect x="26" y="14" width="48" height="70" rx="5" fill="{a}"/><circle cx="50" cy="44" r="12" fill="none" stroke="{w}"/><path d="M38 44h24M50 32c-6 6-6 18 0 24M50 32c6 6 6 18 0 24" fill="none" stroke="{w}"/><path d="M36 68h28" fill="none" stroke="{w}"/><path d="M50 22l2 3h-4z" fill="{w}" stroke="none"/>',
"plane": '<path d="M8 54l84-16-6 10-30 8-10 22h-8l4-18-20 4-6 6H10l4-10z" fill="{w}"/><path d="M60 46l-14-16h-8l8 20" fill="{a}"/>',
"money": '<rect x="10" y="30" width="62" height="36" rx="4" fill="{s}"/><circle cx="41" cy="48" r="10" fill="{w}"/><text x="41" y="54.5" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="17" fill="#23313f" stroke="none">$</text><circle cx="74" cy="70" r="14" fill="{a}"/><circle cx="74" cy="70" r="9" fill="none" stroke="{w}"/><circle cx="58" cy="80" r="10" fill="{a}"/>',
"calendar": '<rect x="16" y="20" width="68" height="64" rx="6" fill="{w}"/><path d="M16 36h68" fill="none"/><rect x="16" y="20" width="68" height="16" rx="6" fill="{a}"/><path d="M32 14v12M68 14v12" fill="none"/><path d="M28 48h8M46 48h8M64 48h8M28 62h8M46 62h8M28 74h8" fill="none"/><circle cx="68" cy="66" r="8" fill="{a}" stroke="none"/>',
"map": '<path d="M10 24l26-8 28 8 26-8v60l-26 8-28-8-26 8z" fill="{s}"/><path d="M36 16v60M64 24v60" fill="none"/><path d="M20 60c10-10 20 6 30-6s20-2 30-14" fill="none" stroke="{a}" stroke-dasharray="4 4"/><path d="M78 30c-6 0-9 5-9 9 0 7 9 15 9 15s9-8 9-15c0-4-3-9-9-9z" fill="{a}"/>',
"compass": '<circle cx="50" cy="50" r="34" fill="{w}"/><circle cx="50" cy="50" r="27" fill="none"/><path d="M50 26l7 24-7 24-7-24z" fill="{a}"/><path d="M50 26l7 24H43z" fill="#c0392b"/><path d="M50 12v6M50 82v6M12 50h6M82 50h6" fill="none"/>',
"anchor": '<circle cx="50" cy="18" r="7" fill="none"/><path d="M50 25v60M34 38h32M18 62c4 18 18 24 32 24s28-6 32-24" fill="none" stroke-width="5"/><path d="M12 64l8-6 4 10zM88 64l-8-6-4 10z" fill="{a}"/>',
"lifering": '<circle cx="50" cy="50" r="34" fill="{w}"/><circle cx="50" cy="50" r="15" fill="{s}"/><path d="M26 26l12 12M74 26L62 38M26 74l12-12M74 74L62 62" fill="none" stroke="{a}" stroke-width="12"/><circle cx="50" cy="50" r="34" fill="none"/><circle cx="50" cy="50" r="15" fill="none"/>',
"wifi": '<path d="M14 42c20-20 52-20 72 0M24 54c14-14 38-14 52 0M34 66c8-8 24-8 32 0" fill="none" stroke="{a}" stroke-width="6"/><circle cx="50" cy="78" r="5" fill="{a}"/>',
"phone": '<rect x="30" y="12" width="40" height="76" rx="7" fill="{w}"/><rect x="35" y="22" width="30" height="52" rx="2" fill="{s}"/><path d="M45 82h10" fill="none"/><path d="M40 40h20M40 50h14M40 60h18" fill="none" stroke="{a}"/>',
"cocktail": '<path d="M22 22h56L52 52v26M38 82h28" fill="none"/><path d="M28 28h44L52 48z" fill="{a}"/><circle cx="70" cy="22" r="8" fill="#f4c542"/><path d="M60 14l-14 22" fill="none"/>',
"wine": '<path d="M34 14h24c2 18 0 30-12 34-12-4-14-16-12-34z" fill="{w}"/><path d="M35 28h22c0 8-3 16-11 18-8-2-11-10-11-18z" fill="{a}" stroke="none"/><path d="M46 48v26M34 82h24" fill="none"/><rect x="66" y="30" width="16" height="52" rx="4" fill="{a}"/><path d="M70 18h8v12h-8z" fill="{a}"/>',
"food": '<ellipse cx="50" cy="60" rx="36" ry="14" fill="{w}"/><ellipse cx="50" cy="56" rx="24" ry="8" fill="{a}"/><path d="M14 30v24M10 30v10c0 4 8 4 8 0V30M86 30c-6 4-6 16 0 18v12" fill="none"/>',
"bed": '<path d="M10 70V36M90 70V52H10" fill="none"/><rect x="10" y="52" width="80" height="12" fill="{a}"/><rect x="16" y="42" width="22" height="10" rx="4" fill="{w}"/><path d="M10 70h80M14 70v8M86 70v8" fill="none"/><rect x="64" y="20" width="22" height="16" rx="2" fill="{s}"/><path d="M64 28c6-4 14-4 22 0" fill="none"/>',
"family": '<circle cx="30" cy="30" r="9" fill="{s}"/><path d="M18 76V52c0-8 6-12 12-12s12 4 12 12v24" fill="{a}"/><circle cx="62" cy="34" r="8" fill="{s}"/><path d="M52 76V54c0-7 5-10 10-10s10 3 10 10v22" fill="{a}"/><circle cx="84" cy="52" r="6" fill="{s}"/><path d="M77 76V66c0-5 3-7 7-7s7 2 7 7v10" fill="{w}"/>',
"couple": '<circle cx="36" cy="30" r="9" fill="{s}"/><path d="M24 80V54c0-8 6-12 12-12s12 4 12 12v26" fill="{a}"/><circle cx="64" cy="30" r="9" fill="{s}"/><path d="M52 80l4-26c1-8 4-12 8-12s7 4 8 12l4 26z" fill="{w}"/><path d="M44 60h12" fill="none"/><path d="M50 18c-3-4-8-1-6 3l6 5 6-5c2-4-3-7-6-3z" fill="#c0392b" stroke="none"/>',
"group": '<circle cx="22" cy="36" r="7" fill="{s}"/><circle cx="42" cy="30" r="7" fill="{s}"/><circle cx="62" cy="30" r="7" fill="{s}"/><circle cx="80" cy="36" r="7" fill="{s}"/><path d="M12 76V56c0-6 4-10 10-10s10 4 10 10M32 76V50c0-6 4-10 10-10s10 4 10 10v26M52 76V50c0-6 4-10 10-10s10 4 10 10M70 76V56c0-6 4-10 10-10s10 4 10 10v20" fill="{a}"/>',
"wheelchair": '<circle cx="44" cy="20" r="7" fill="{s}"/><path d="M44 28v26h22l8 18" fill="none" stroke-width="5"/><path d="M44 40h18" fill="none" stroke-width="5"/><circle cx="42" cy="66" r="18" fill="none" stroke="{a}" stroke-width="5"/>',
"medical": '<rect x="18" y="26" width="64" height="52" rx="8" fill="{w}"/><path d="M38 26v-8h24v8" fill="none"/><path d="M44 40h12v10h10v12H56v10H44V62H34V50h10z" fill="#c0392b"/>',
"umbrella": '<path d="M12 50c4-22 22-34 38-34s34 12 38 34c-6-4-12-4-18 0-6-4-14-4-20 0-6-4-14-4-20 0-6-4-12-4-18 0z" fill="{a}"/><path d="M50 16v62c0 8 12 8 12 0" fill="none"/><path d="M24 70l-4 8M36 76l-4 8M74 72l-4 8" fill="none" stroke="{a}"/>',
"snowflake": '<path d="M50 12v76M17 31l66 38M17 69l66-38" fill="none" stroke="{a}" stroke-width="4"/><path d="M42 18l8 8 8-8M42 82l8-8 8 8M18 42l11 4-3 11M82 58l-11-4 3-11M18 58l11-4-3-11M82 42l-11 4 3 11" fill="none"/>',
"camera": '<rect x="12" y="32" width="76" height="48" rx="8" fill="{a}"/><path d="M34 32l6-10h20l6 10" fill="{s}"/><circle cx="50" cy="56" r="16" fill="{w}"/><circle cx="50" cy="56" r="9" fill="{s}"/><rect x="72" y="38" width="8" height="5" fill="{w}" stroke="none"/>',
"binoculars": '<circle cx="30" cy="62" r="16" fill="{a}"/><circle cx="70" cy="62" r="16" fill="{a}"/><circle cx="30" cy="62" r="8" fill="{w}"/><circle cx="70" cy="62" r="8" fill="{w}"/><path d="M22 48l6-24h12l4 24M78 48l-6-24H60l-4 24M44 46h12" fill="{s}"/>',
"bear": '<path d="M14 74c0-18 10-30 30-30h16c14 0 24 8 26 20l4 2-2 8H72v6h-8v-6H34v6h-8v-6z" fill="#7a5230"/><circle cx="80" cy="52" r="3" fill="{w}" stroke="none"/><circle cx="70" cy="42" r="5" fill="#7a5230"/><path d="M4 84c10-4 18 4 28 0s18 4 28 0 18 4 36 0" fill="none" stroke="{a}"/>',
"train": '<rect x="18" y="20" width="64" height="54" rx="10" fill="{a}"/><rect x="26" y="28" width="20" height="16" rx="2" fill="{w}"/><rect x="54" y="28" width="20" height="16" rx="2" fill="{w}"/><circle cx="32" cy="62" r="4" fill="{w}"/><circle cx="68" cy="62" r="4" fill="{w}"/><path d="M28 74l-8 14M72 74l8 14M10 88h80" fill="none"/>',
"car": '<path d="M10 66V54l10-4 10-14h38l12 14 10 4v12z" fill="{a}"/><path d="M34 40h14v12H28zM54 40h12l8 12H54z" fill="{w}"/><circle cx="28" cy="68" r="8" fill="{w}"/><circle cx="74" cy="68" r="8" fill="{w}"/>',
"document": '<path d="M24 10h38l16 16v64H24z" fill="{w}"/><path d="M62 10v16h16" fill="{s}"/><path d="M32 40h36M32 50h36M32 60h28M32 70h32" fill="none"/><circle cx="66" cy="76" r="9" fill="{a}"/>',
"checklist": '<rect x="20" y="12" width="60" height="78" rx="6" fill="{w}"/><rect x="36" y="6" width="28" height="12" rx="4" fill="{a}"/><path d="M30 34l4 4 8-8M30 54l4 4 8-8M30 74l4 4 8-8" fill="none" stroke="{a}" stroke-width="4"/><path d="M50 36h22M50 56h22M50 76h18" fill="none"/>',
"clock": '<circle cx="50" cy="50" r="34" fill="{w}"/><path d="M50 26v24l16 10" fill="none" stroke="{a}" stroke-width="5"/><path d="M50 18v5M50 77v5M18 50h5M77 50h5" fill="none"/>',
"gift": '<rect x="16" y="40" width="68" height="44" fill="{a}"/><rect x="12" y="30" width="76" height="12" fill="{s}"/><path d="M50 30v54" fill="none" stroke="{w}" stroke-width="6"/><path d="M50 30c-10-16-26-10-18 0M50 30c10-16 26-10 18 0" fill="none"/>',
"bowtie": '<path d="M50 50L16 30v40zM50 50l34-20v40z" fill="{a}"/><rect x="42" y="42" width="16" height="16" rx="3" fill="{s}"/>',
"nosmoke": '<rect x="18" y="44" width="56" height="12" fill="{w}"/><rect x="74" y="44" width="10" height="12" fill="{a}"/><path d="M80 38c0-8-6-8-6-16" fill="none"/><circle cx="50" cy="50" r="38" fill="none" stroke="#c0392b" stroke-width="7"/><path d="M23 23l54 54" fill="none" stroke="#c0392b" stroke-width="7"/>',
"plug": '<path d="M34 12v18M66 12v18" fill="none" stroke-width="5"/><path d="M24 30h52v18c0 14-12 22-26 22S24 62 24 48z" fill="{a}"/><path d="M50 70v18" fill="none" stroke-width="5"/>',
"shirt": '<path d="M34 14l-22 14 8 16 10-6v48h40V38l10 6 8-16-22-14c-4 8-24 8-32 0z" fill="{a}"/><path d="M38 14c4 8 20 8 24 0" fill="none"/>',
"bag": '<path d="M22 34h56l-6 54H28z" fill="{a}"/><path d="M38 34c0-22 24-22 24 0" fill="none"/><path d="M36 52h28" fill="none" stroke="{w}"/>',
"ticket": '<path d="M12 30h76v12a8 8 0 000 16v12H12V58a8 8 0 000-16z" fill="{a}"/><path d="M66 30v40" fill="none" stroke="{w}" stroke-dasharray="4 4"/><path d="M24 44h30M24 54h22" fill="none" stroke="{w}"/>',
"island": '<path d="M14 76c10-12 62-12 72 0z" fill="#f2d49b"/><path d="M50 72c0-18 2-30 8-40" fill="none" stroke-width="4"/><path d="M58 32c-10-8-22-6-28 2 10-2 18 0 28-2zM58 32c8-10 20-10 26-4-8 0-18 0-26 4zM58 32c10 2 18 8 20 16-6-6-14-10-20-16z" fill="{a}"/><path d="M4 84c10-4 18 4 28 0s18 4 28 0 18 4 36 0" fill="none"/>',
"lighthouse": '<path d="M40 86l4-56h12l4 56z" fill="{w}"/><path d="M42 58h16M41 72h18" fill="none" stroke="#c0392b" stroke-width="6"/><rect x="40" y="18" width="20" height="12" fill="{a}"/><path d="M38 18l12-8 12 8z" fill="#c0392b"/><path d="M62 22l26-8M62 26l26 8" fill="none" stroke="#f4c542" stroke-width="3"/><path d="M28 86h44" fill="none"/>',
"star": '<path d="M50 10l11 25 27 2-21 17 7 27-24-15-24 15 7-27-21-17 27-2z" fill="{a}"/>',
}

def fm(slug):
    s = open(f"{ART}/{slug}.md", encoding="utf-8").read().split("\n---\n", 1)[0]
    return {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in s.splitlines() if ":" in l)}

def h(slug, salt=""):
    return int(hashlib.md5((salt + slug).encode()).hexdigest(), 16)

FALLBACK = {"alaska": "ship,mountains,whale", "deals": "money,ticket,ship", "first-time": "ship,checklist,suitcase",
            "fly-cruise": "plane,ship,suitcase", "groups": "group,ship,calendar", "couples-50": "couple,ship,wine"}

WATER = {"ship":86,"whale":80,"iceberg":70,"island":78,"lighthouse":86,"mountains":80}
SEA = set(WATER)
def motif(name, x, y, sc, a, soft, rot=0, hy=None):
    if hy is not None and name in SEA: y = hy - WATER[name] * sc
    body = M[name].replace("{a}", a).replace("{s}", soft).replace("{w}", "#ffffff")
    return (f'<g transform="translate({x} {y}) rotate({rot} {50*sc} {50*sc}) scale({sc})" fill="none" stroke="{INK}" '
            f'stroke-width="{2.6/ sc * 2.2:.2f}" stroke-linecap="round" stroke-linejoin="round" filter="url(#rough)">{body}</g>')

def compose(slug):
    m = fm(slug)
    names = [x.strip() for x in (m.get("imgmotif") or FALLBACK.get(m.get("category"), "ship,compass")).split(",") if x.strip() in M][:4]
    if not names: names = ["ship", "compass"]
    a, soft = ACCENTS[h(slug, "a") % len(ACCENTS)]
    lay = h(slug, "l") % 3
    seed = h(slug, "s") % 97
    W, H = 1200, 630
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{(m.get("imgalt") or m.get("title","")).replace(chr(34),"")}">',
             f'<defs><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="{seed}"/><feDisplacementMap in="SourceGraphic" scale="3.2"/></filter>'
             f'<pattern id="paper" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M0 24L24 0" stroke="{a}" stroke-opacity=".06"/></pattern></defs>',
             f'<rect width="{W}" height="{H}" fill="{soft}"/><rect width="{W}" height="{H}" fill="url(#paper)"/>']
    # horizon and waves
    hy = 470 + (h(slug, "y") % 40)
    parts.append(f'<g fill="none" stroke="{a}" stroke-opacity=".35" stroke-width="3" stroke-linecap="round" filter="url(#rough)">'
                 + "".join(f'<path d="M{-40+i*7} {hy+k*34} ' + " ".join(f"q 30 {-10 if j%2 else 10} 60 0" for j in range(22)) + '"/>' for k, i in [(0,0),(1,3),(2,1)]) + '</g>')
    # sun or moon accent and clouds/birds
    sx = [980, 160, 600][lay]
    parts.append(f'<circle cx="{sx}" cy="110" r="46" fill="#f4c542" fill-opacity=".55" filter="url(#rough)"/>')
    for i in range(3):
        bx = 300 + (h(slug, f"b{i}") % 600); by = 70 + (h(slug, f"c{i}") % 90)
        parts.append(f'<path d="M{bx} {by} q 10 -10 20 0 q 10 -10 20 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    # layout positions: (x, y, scale)
    main = [(90, 120, 3.8), (720, 120, 3.8), (420, 110, 3.9)][lay]
    small = [[(560, 230, 2.2), (820, 170, 2.0), (1000, 320, 1.6)],
             [(80, 230, 2.2), (340, 170, 2.0), (520, 330, 1.6)],
             [(80, 250, 2.0), (880, 220, 2.2), (1040, 70, 1.4)]][lay]
    rot = (h(slug, "r") % 9) - 4
    parts.append(motif(names[0], *main, a, soft, rot if names[0] not in SEA else 0, hy=hy+6))
    for i, nm in enumerate(names[1:]):
        x, y, sc = small[i]
        parts.append(motif(nm, x, y, sc, a, soft, 0 if nm in SEA else ((h(slug, f"r{i}") % 13) - 6), hy=hy+6))
    # sketch frame
    parts.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="22" fill="none" stroke="{INK}" stroke-opacity=".25" stroke-width="3" filter="url(#rough)"/>')
    parts.append('</svg>')
    return "\n".join(parts)

def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    slugs = args or [os.path.basename(f)[:-3] for f in sorted(glob.glob(f"{ART}/*.md"))]
    os.makedirs(OUT, exist_ok=True)
    for s in slugs:
        open(f"{OUT}/{s}.svg", "w", encoding="utf-8").write(compose(s))
    print(f"svg: {len(slugs)}")
    if "--png" in sys.argv:
        from playwright.sync_api import sync_playwright
        exe = "/opt/pw-browsers/chromium" if os.path.isfile("/opt/pw-browsers/chromium") else None
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
            pg = b.new_page(viewport={"width": 1200, "height": 630})
            for s in slugs:
                pg.goto(f"file://{OUT}/{s}.svg"); pg.screenshot(path=f"{OUT}/{s}.png")
            b.close()
        print(f"png: {len(slugs)}")

if __name__ == "__main__":
    main()
