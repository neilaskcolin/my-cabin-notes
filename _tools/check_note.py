#!/usr/bin/env python3
import re, sys, os, glob
N="/home/claude/mcn/_content/notes"; OLD="/home/claude/cqc/_content/articles"
MAP=[l.split("\t") for l in open("/home/claude/mcn/_tools/block1.tsv").read().splitlines()[1:] if l.strip()]
NEW={m[1]:m[0] for m in MAP}
MOTIFS=set("ship iceberg mountains whale sun palm suitcase passport plane money calendar map compass anchor lifering wifi phone cocktail wine food bed family couple group wheelchair medical umbrella snowflake camera binoculars bear train car document checklist clock gift bowtie nosmoke plug shirt bag ticket island lighthouse star".split())
BAN=["delve","in conclusion","whether you're","it's important to note","navigate the","embark on","look no further","game-changer","seamless","when i sailed","cruisequestionscanada"]
def words(b):
    b=re.sub(r"\]\([^)]*\)","]",b); b=re.sub(r"[#*>|\[\]_`-]"," ",b); return len(re.findall(r"[A-Za-z0-9$%'’.,]+",b))
def sh(t,n=8):
    w=re.findall(r"[a-z0-9']+",t.lower()); return {" ".join(w[i:i+n]) for i in range(len(w)-n+1)}
def check(slug):
    p=f"{N}/{slug}.md"; pr=[]
    if not os.path.exists(p): return slug,0,["file missing"]
    s=open(p,encoding="utf-8").read()
    if "\n---\n" not in s: return slug,0,["no --- separator"]
    fm,b=s.split("\n---\n",1)
    meta={k.strip():v.strip() for k,v in (l.split(":",1) for l in fm.splitlines() if ":" in l)}
    for k in ["title","slug","category","description","answer","faq1q","faq1a","faq2q","faq2a","faq3q","faq3a","imgmotif","published"]:
        if not meta.get(k): pr.append(f"missing {k}")
    if meta.get("slug")!=slug: pr.append("slug mismatch")
    if len(meta.get("title",""))>62: pr.append("title too long")
    d=len(meta.get("description",""))
    if d and not 120<=d<=160: pr.append(f"description {d} chars")
    if len(meta.get("answer","").split())>60: pr.append("answer too long")
    ms=[m.strip() for m in meta.get("imgmotif","").split(",") if m.strip()]
    if any(m not in MOTIFS for m in ms) or not 2<=len(ms)<=4: pr.append("bad imgmotif")
    w=words(b)
    if not 750<=w<=1250: pr.append(f"body words {w} (want 750-1200)")
    if b.count("[[EXPERT]]")!=1: pr.append("need exactly one [[EXPERT]]")
    for l in re.findall(r"\]\(/([^)]*)\)",b):
        if l.strip("/") not in NEW: pr.append(f"bad link /{l}")
    if re.search(r"(?m)^# ",b): pr.append("H1 in body")
    if len(re.findall(r"(?m)^## ",b))<5: pr.append("need 5+ H2s")
    comps=sum([bool(re.search(r"(?m)^\|",b)),bool(re.search(r"(?m)^\d+\. ",b)),bool(re.search(r"(?m)^- ",b)),bool(re.search(r"(?m)^> \*\*",b))])
    if comps<3: pr.append("use 3+ of table/numbered/bullets/callouts")
    low=s.lower()
    for x in BAN:
        if x in low: pr.append(f"banned '{x}'")
    old=NEW.get(slug)
    if old and os.path.exists(f"{OLD}/{old}.md"):
        o=open(f"{OLD}/{old}.md",encoding="utf-8").read()
        a,c=sh(b),sh(o.split("\n---\n",1)[1]); ov=len(a&c)/max(1,len(a))
        if ov>0.03: pr.append(f"too similar to old page ({ov:.0%} shared 8-word phrases)")
        if meta.get("title","").lower()==re.search(r"(?m)^title: (.*)$",o).group(1).lower(): pr.append("title same as old")
    return slug,w,pr
def structure_check():
    import collections
    sigs={}; heads={}; opens={}
    for f in glob.glob(f"{N}/*.md"):
        b=open(f,encoding="utf-8").read().split("\n---\n",1)[1]; slug=os.path.basename(f)[:-3]
        h2=tuple(re.findall(r"(?m)^## (.*)$",b)); heads[slug]=set(x.lower() for x in h2)
        sig=tuple(c for c in ["table" if re.search(r"(?m)^\|",b) else "","ol" if re.search(r"(?m)^\d+\. ",b) else "","ul" if re.search(r"(?m)^- ",b) else "","callout" if re.search(r"(?m)^> \*\*",b) else ""]); sigs[slug]=(len(h2),sig)
        opens[slug]=" ".join(b.split()[:6]).lower()
    probs=[]
    sl=sorted(heads)
    for i,a in enumerate(sl):
        for b2 in sl[i+1:]:
            shared=heads[a]&heads[b2]
            if len(shared)>=2: probs.append(f"{a} and {b2} share H2s: {sorted(shared)}")
            if opens[a]==opens[b2]: probs.append(f"{a} and {b2} open with the same words")
    cnt=collections.Counter(sigs.values())
    for k,n in cnt.items():
        if n>=4: probs.append(f"{n} pages share the exact shape {k}: vary section counts/components")
    return probs
args=sys.argv[1:]
if args==["--structure"]:
    pr=structure_check(); print("\n".join(pr) or "structure OK"); sys.exit(0)
if args==["--all"]: args=[os.path.basename(f)[:-3] for f in sorted(glob.glob(f"{N}/*.md"))]
ok=0
for a in args:
    s,w,pr=check(a); ok+=not pr
    print(("OK " if not pr else "FIX ")+f"{s} ({w} words)"+("" if not pr else ": "+"; ".join(pr)))
print(f"{ok}/{len(args)} pass")
