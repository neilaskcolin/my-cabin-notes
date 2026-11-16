NAVY="#1f2d3d"; TEAL="#0f8b8d"; WARM="#e0a458"; CREAM="#faf7f1"
# Option A: luggage tag with three note lines and a wave
A=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<path d="M14 10 h30 a4 4 0 0 1 4 4 v30 l-8 10 h-26 a4 4 0 0 1 -4 -4 v-36 a4 4 0 0 1 4 -4z" fill="{NAVY}"/>
<path d="M40 44 v6 a4 4 0 0 0 4 -4 h-4z" fill="{TEAL}"/>
<circle cx="22" cy="18" r="3" fill="{CREAM}"/><circle cx="22" cy="18" r="1.4" fill="{NAVY}"/>
<path d="M18 28 h22 M18 35 h22" stroke="{CREAM}" stroke-width="2.6" stroke-linecap="round"/>
<path d="M18 42 c3 -3 6 -3 9 0 s6 3 9 0" stroke="{TEAL}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
</svg>'''
# Option B: porthole notebook, teal ring, folded corner
B=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect x="10" y="8" width="44" height="48" rx="6" fill="{NAVY}"/>
<rect x="10" y="8" width="8" height="48" rx="3" fill="{TEAL}"/>
<circle cx="37" cy="30" r="11" fill="{CREAM}"/>
<circle cx="37" cy="30" r="11" fill="none" stroke="{WARM}" stroke-width="2.5"/>
<path d="M27 32 c3 -3 6 -3 9 0 s6 3 9 0 M27 36.5 c3 -3 6 -3 9 0 s6 3 9 0" stroke="{TEAL}" stroke-width="2.2" fill="none" stroke-linecap="round"/>
<circle cx="35" cy="24" r="2.2" fill="{WARM}"/>
<path d="M26 48 h22" stroke="{CREAM}" stroke-width="2.4" stroke-linecap="round" opacity=".7"/>
</svg>'''
# Option C: monogram "M" as waves inside a rounded square, pencil-stroke feel
C=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect x="6" y="6" width="52" height="52" rx="14" fill="{NAVY}"/>
<path d="M16 42 v-18 l8 10 l8 -10 v18" stroke="{CREAM}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M36 36 c3 -3 6 -3 9 0 s6 3 9 0" stroke="{TEAL}" stroke-width="3.5" fill="none" stroke-linecap="round" transform="translate(-4 7)"/>
<circle cx="47" cy="22" r="3.5" fill="{WARM}"/>
</svg>'''
# Option D: open notebook pages as a wave, bookmark ribbon
D=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<circle cx="32" cy="32" r="28" fill="{NAVY}"/>
<path d="M14 24 c6 -4 12 -4 18 0 v22 c-6 -4 -12 -4 -18 0z" fill="{CREAM}"/>
<path d="M32 24 c6 -4 12 -4 18 0 v22 c-6 -4 -12 -4 -18 0z" fill="{CREAM}" opacity=".85"/>
<path d="M18 31 h10 M18 36 h10 M36 31 h10 M36 36 h10" stroke="{TEAL}" stroke-width="2" stroke-linecap="round"/>
<path d="M30 14 h4 v12 l-2 -2 l-2 2z" fill="{WARM}"/>
</svg>'''
import pathlib
for n,s in zip("ABCD",[A,B,C,D]): pathlib.Path(f"mark{n}.svg").write_text(s)
html=f'''<html><body style="margin:0;background:#faf7f1;font-family:Georgia,serif;padding:40px">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:40px">
{''.join(f"""<div style="background:#fff;border:1px solid #e5e1d8;border-radius:16px;padding:32px">
<div style="font:14px system-ui;color:#0f8b8d;letter-spacing:.1em">OPTION {n}</div>
<div style="display:flex;align-items:center;gap:16px;margin:20px 0"><img src="mark{n}.svg" width="56"><span style="font-size:34px;font-weight:700;color:#1f2d3d">My Cabin Notes</span></div>
<div style="display:flex;gap:16px;align-items:center"><img src="mark{n}.svg" width="16"><img src="mark{n}.svg" width="32"><img src="mark{n}.svg" width="96">
<div style="background:#1f2d3d;padding:14px;border-radius:12px;display:flex;align-items:center;gap:10px"><img src="mark{n}.svg" width="32"><span style="color:#faf7f1;font-size:20px;font-weight:700">My Cabin Notes</span></div></div></div>""" for n in "ABCD")}
</div></body></html>'''
pathlib.Path("sheet.html").write_text(html)
