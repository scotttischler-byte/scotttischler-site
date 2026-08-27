#!/usr/bin/env python3
import os, json, html as ihtml
ROOT=os.path.dirname(os.path.abspath(__file__))
data=json.load(open(os.path.join(ROOT,"_catalog.json")))
CAT=data["catalog"]; LIVE=set(data["live"])
SITE="https://scotttischler.com"
PORTRAIT=open(os.path.join(ROOT,"portrait_b64.txt")).read().strip()
MONTHS=["January","February","March","April","May","June","July","August","September","October","November","December"]
def pd(iso):
    y,m,d=[int(x) for x in iso.split("-")]; return f"{MONTHS[m-1]} {d}, {y}"

# excerpts for live pieces (pulled from sources)
EXCERPTS={
 "what-is-answer-engine-optimization":"Search stopped being a list of links and became a set of answers. AEO decides whether the answer names your brand.",
 "aeo-vs-seo":"The blue link is being replaced by the synthesized answer. What changes when the buyer never sees your ranking — and a 90-day plan.",
 "how-ai-decides-which-businesses-to-recommend":"When an AI names one business and ignores its competitors, that choice isn't random. Here's what actually drives it.",
 "entity-authority":"Search became about entities — the people, companies, and places AI recognizes as real and trustworthy. How to become one.",
 "zero-click-era":"The search box is being replaced by an answer that rarely sends anyone to your site. How to win when the click is gone.",
 "get-cited-by-chatgpt-claude-perplexity":"The buyers you want are asking AI, not Google — and it names only a handful of sources. Here's how to become one of them.",
}
COMING={
 "structured-data-knowledge-graphs":"Turn your business into clean, machine-readable facts with schema.org and knowledge-graph signals.",
 "local-business-aeo":"How local and service businesses become the AI's neighborhood recommendation.",
 "measuring-ai-referred-traffic":"The metrics and methods for tracking traffic and leads that originate inside AI answers.",
 "the-epistemic-shift":"The research note: how discovery moved from ten blue links to generative-AI recommendations.",
 "aeo-for-service-businesses":"An Answer Engine Optimization playbook tailored to service-based businesses.",
 "google-ai-overviews-playbook":"A practical, step-by-step approach to earning visibility in Google's AI Overviews.",
 "reviews-reputation-ai-trust":"How reviews, sentiment, and reputation feed the trust signals AI weighs when it recommends.",
 "content-architecture-answer-engines":"Structuring content so answer engines can find, lift, and cite it cleanly.",
 "personal-brand-ai-will-recommend":"How founders and executives build a personal entity that AI systems recognize and cite.",
 "seo-agency-to-aeo-practice":"A repositioning guide for agencies moving from ranking services to Answer Engine Optimization.",
 "franchising-category-defining-business":"What it takes to franchise and scale a category-defining service business.",
 "founders-guide-category-creation":"The founder's playbook for defining and owning a new market category.",
 "future-of-search-2026-2030":"Where AI-driven search is heading over the next five years — and how to prepare.",
 "lessons-20-years-martech":"Two decades in marketing technology, distilled into what actually builds durable authority.",
}
# pull excerpts straight from source files for any live article
import glob as _glob
SRC_EXCERPT={}
for _p in _glob.glob(os.path.join(ROOT,"articles_src","*.txt")):
    _raw=open(_p,encoding="utf-8").read()
    _m={}
    for _line in _raw[:_raw.index("\nBODY:")].splitlines():
        if ":" in _line:
            _k,_v=_line.split(":",1); _m[_k.strip().lower()]=_v.strip()
    if _m.get("slug"): SRC_EXCERPT[_m["slug"]]=_m.get("excerpt","")

def excerpt(slug):
    return SRC_EXCERPT.get(slug) or EXCERPTS.get(slug) or COMING.get(slug,"")

cats = sorted({c for _,_,c,_ in CAT})
chips = '<button class="chip active" data-f="all">All</button>'+"".join(
    f'<button class="chip" data-f="{ihtml.escape(c)}">{ihtml.escape(c)}</button>' for c in cats)

cards=[]
for slug,title,cat,date in CAT:
    live = slug in LIVE
    body=f"""<span class="tag">{ihtml.escape(cat)}</span>
      <h2>{ihtml.escape(title)}</h2>
      <p>{ihtml.escape(excerpt(slug))}</p>
      <div class="meta">{pd(date)}</div>"""
    if live:
        card=f'''<a class="card" data-cat="{ihtml.escape(cat)}" href="{slug}.html">
      {body}
      <div class="links"><span class="read">Read article →</span><span class="pdf" onclick="event.preventDefault();event.stopPropagation();window.location.href='pdf/{slug}.pdf'">⤓ PDF</span></div>
    </a>'''
    else:
        card=f'''<div class="card soon" data-cat="{ihtml.escape(cat)}">
      {body}
      <div class="links"><span class="cs">Coming soon</span></div>
    </div>'''
    cards.append(card)
cards_html="\n".join(cards)

CSS="""
:root{--bg:#0a0b0e;--bg2:#0e1014;--panel:#14171e;--ink:#f3f5f9;--soft:#c4cad6;--mute:#838b9b;--line:rgba(190,205,230,.10);--line2:rgba(190,205,230,.16);--accent:#4f8cff;--accent2:#86b3ff;--sans:'Inter',system-ui,sans-serif;--serif:'Fraunces',Georgia,serif;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.nav{position:sticky;top:0;z-index:50;background:rgba(10,11,14,.82);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.nav .in{max-width:1180px;margin:0 auto;padding:0 26px;height:66px;display:flex;align-items:center;justify-content:space-between}
.brand{font-family:var(--serif);font-size:20px}.brand span{color:var(--accent)}
.nav a.back{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--soft)}.nav a.back:hover{color:var(--accent2)}
.wrap{max-width:1180px;margin:0 auto;padding:0 26px}
.head{padding:78px 0 30px;text-align:center;position:relative;overflow:hidden}
.head::before{content:'';position:absolute;inset:0;background:radial-gradient(700px 320px at 50% -10%,rgba(79,140,255,.18),transparent 60%);pointer-events:none}
.eyebrow{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:var(--accent2);font-weight:600}
.head h1{font-family:var(--serif);font-weight:400;font-size:clamp(34px,5vw,56px);line-height:1.05;margin:16px 0 16px;letter-spacing:-.015em}
.head p{color:var(--soft);font-size:18px;max-width:40em;margin:0 auto}
.chips{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:34px 0 44px}
.chip{border:1px solid var(--line2);background:var(--panel);color:var(--soft);border-radius:999px;padding:9px 16px;font-size:13px;cursor:pointer;transition:.2s}
.chip:hover{border-color:var(--accent);color:var(--accent2)}
.chip.active{background:linear-gradient(135deg,var(--accent2),var(--accent));color:#08122a;border-color:transparent;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;padding-bottom:80px}
.card{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:16px;background:var(--panel);padding:26px;transition:transform .3s,border-color .3s;min-height:240px}
.card:hover{transform:translateY(-4px);border-color:rgba(79,140,255,.4)}
.card .tag{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent2);font-weight:600}
.card h2{font-family:var(--serif);font-weight:500;font-size:20px;line-height:1.22;margin:12px 0 10px}
.card p{color:var(--soft);font-size:14px;flex:1}
.card .meta{color:var(--mute);font-size:12.5px;margin-top:14px}
.card .links{display:flex;justify-content:space-between;align-items:center;margin-top:16px;padding-top:14px;border-top:1px solid var(--line)}
.card .read{color:var(--accent2);font-size:13px;font-weight:600;letter-spacing:.04em}
.card .pdf{color:var(--soft);font-size:12.5px;border:1px solid var(--line2);border-radius:999px;padding:5px 12px;cursor:pointer;transition:.2s}
.card .pdf:hover{border-color:var(--accent);color:var(--accent2)}
.card.soon{opacity:.6}.card.soon:hover{transform:none;border-color:var(--line)}
.card .cs{color:var(--mute);font-size:12.5px;letter-spacing:.08em;text-transform:uppercase}
footer{border-top:1px solid var(--line);padding:34px 0;color:var(--mute);font-size:13px}
footer .in{max-width:1180px;margin:0 auto;padding:0 26px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
footer a{color:var(--soft)}
@media(max-width:900px){.grid{grid-template-columns:1fr}}
"""

HTML=f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>The AEO Library — Insights by Scott Tischler</title>
<meta name="description" content="Expert guides on Answer Engine Optimization, AI search, and entity authority by Scott Tischler, Founder & Chairman of AIrecommend.ai.">
<link rel="canonical" href="{SITE}/articles/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="alternate" type="application/rss+xml" title="Scott Tischler — The AEO Library" href="{SITE}/feed.xml">
<meta property="og:title" content="The AEO Library — Insights by Scott Tischler">
<meta property="og:description" content="Expert articles on AI search and Answer Engine Optimization. Free to read and download as PDFs.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230a0b0e'/%3E%3Ctext x='32' y='44' font-family='Georgia,serif' font-size='38' fill='%234f8cff' text-anchor='middle'%3ES%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="nav"><div class="in"><a href="../index.html" class="brand">Scott <span>Tischler</span></a><a href="../index.html" class="back">← Back to site</a></div></div>
<div class="head"><div class="wrap">
<span class="eyebrow">The AEO Library</span>
<h1>Insights on AI Search &amp; Answer Engine Optimization</h1>
<p>Practitioner-grade guides on becoming the business AI recommends. Free to read, free to download, written to help you build real authority. New articles added regularly on the way to 200+.</p>
</div></div>
<div class="wrap">
<div class="chips">{chips}</div>
<div class="grid" id="grid">
{cards_html}
</div>
</div>
<footer><div class="in"><div>© 2026 Scott Tischler. All rights reserved.</div><div><a href="../index.html">Home</a> · <a href="/privacy.html">Privacy</a> · <a href="https://airecommend.ai" target="_blank" rel="noopener">AIrecommend.ai</a> · <a href="mailto:scott@airecommend.ai">Contact</a></div></div></footer>
<script defer src="/track.js"></script>
<script>
const chips=document.querySelectorAll('.chip'),cards=document.querySelectorAll('.card');
chips.forEach(c=>c.addEventListener('click',()=>{{
  chips.forEach(x=>x.classList.remove('active'));c.classList.add('active');
  const f=c.dataset.f;
  cards.forEach(card=>{{card.style.display=(f==='all'||card.dataset.cat===f)?'':'none';}});
}}));
</script>
</body></html>"""
open(os.path.join(ROOT,"articles","index.html"),"w",encoding="utf-8").write(HTML)

# sitemap
urls=[f"{SITE}/",f"{SITE}/articles/"]
for slug,_,_,_ in CAT:
    if slug in LIVE: urls.append(f"{SITE}/articles/{slug}.html")
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls: sm+=f"  <url><loc>{u}</loc></url>\n"
sm+="</urlset>\n"
open(os.path.join(ROOT,"sitemap.xml"),"w").write(sm)
print("hub + sitemap built;", len(LIVE),"live,",len(CAT)-len(LIVE),"coming soon")
