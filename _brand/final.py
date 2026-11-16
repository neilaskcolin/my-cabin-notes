NAVY="#1f2d3d"; TEAL="#0f8b8d"; WARM="#e0a458"; CREAM="#faf7f1"
def mark(bg=True, size=64):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{size}" height="{size}">
{'<circle cx="32" cy="32" r="30" fill="'+NAVY+'"/>' if bg else ''}
<path d="M13 23 c6.5 -4.5 12.5 -4.5 19 0 v23 c-6.5 -4.5 -12.5 -4.5 -19 0z" fill="{CREAM}"/>
<path d="M32 23 c6.5 -4.5 12.5 -4.5 19 0 v23 c-6.5 -4.5 -12.5 -4.5 -19 0z" fill="{CREAM}" opacity=".88"/>
<path d="M32 23 v23" stroke="{NAVY}" stroke-width="1.2" opacity=".35"/>
<path d="M17.5 30 h9.5 M17.5 35.5 h9.5 M37 30 h9.5 M37 35.5 h9.5" stroke="{TEAL}" stroke-width="2.2" stroke-linecap="round"/>
<path d="M29.8 12 h4.4 v13.5 l-2.2 -2.1 l-2.2 2.1z" fill="{WARM}"/>
<path d="M16 51.5 c3 -2.5 6 -2.5 9 0 s6 2.5 9 0 s6 -2.5 9 0 s4 2 5 2" stroke="{TEAL}" stroke-width="2" fill="none" stroke-linecap="round" opacity=".9"/>
</svg>'''
import pathlib
pathlib.Path("logo.svg").write_text(mark())
pathlib.Path("favicon.svg").write_text(mark())
pathlib.Path("mark-nobg.svg").write_text(mark(False))
og=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
<rect width="1200" height="630" fill="{CREAM}"/>
<path d="M0 560 c100 -40 200 -40 300 0 s200 40 300 0 s200 -40 300 0 s200 40 300 0 v70 h-1200z" fill="{TEAL}" opacity=".18"/>
<g transform="translate(120 175) scale(4.4)">{mark().split('>',1)[1].rsplit('</svg>',1)[0]}</g>
<text x="440" y="300" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="92" fill="{NAVY}">My Cabin Notes</text>
<text x="444" y="370" font-family="Helvetica, Arial, sans-serif" font-size="38" fill="{TEAL}">Real answers for cruisers</text>
</svg>'''
pathlib.Path("og-default.svg").write_text(og)
