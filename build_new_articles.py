#!/usr/bin/env python3
"""Generate new article HTML (web + print) matching the existing scotttischler.com template."""
import os, json, html as ihtml

ROOT = os.path.dirname(os.path.abspath(__file__))
PORTRAIT = open(os.path.join(ROOT, "portrait_small_b64.txt")).read().strip()
SITE = "https://scotttischler.com"

def seo_title(t):
    suffix = " | Scott Tischler"
    if len(t) + len(suffix) <= 60: return t + suffix
    if len(t) <= 60: return t
    cut = t[:60]
    if " " in cut: cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,:;—-")

def esc(s):  # attribute-safe
    return ihtml.escape(s, quote=True)

def web_html(a):
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q,ans in a["faq"]]}
    art_ld = {"@context":"https://schema.org","@type":"Article","headline":a["title"],
        "description":a["desc"],"datePublished":a["date"],"dateModified":a["date"],
        "author":{"@type":"Person","name":"Scott Tischler","url":SITE+"/","jobTitle":"Founder & Chairman, AIrecommend.ai"},
        "publisher":{"@type":"Organization","name":"Scott Tischler / AIrecommend.ai"},
        "mainEntityOfPage":f"{SITE}/articles/{a['slug']}.html","articleSection":a["cat"]}
    tk = "".join(f"<li>{t}</li>" for t in a["takeaways"])
    fq = "".join(f'<div class="item"><div class="q">{ihtml.escape(q)}</div><div class="a">{ans}</div></div>' for q,ans in a["faq"])
    return f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(seo_title(a["title"]))}</title>
<meta name="description" content="{esc(a["desc"])}">
<meta name="author" content="Scott Tischler">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="{SITE}/articles/{a['slug']}.html">
<link rel="alternate" type="application/rss+xml" title="Scott Tischler — The AEO Library" href="{SITE}/feed.xml">
<meta property="og:type" content="article"><meta property="og:title" content="{esc(a["title"])}">
<meta property="og:description" content="{esc(a["desc"])}"><meta property="article:published_time" content="{a['date']}">
<meta property="article:author" content="Scott Tischler">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230a0b0e'/%3E%3Ctext x='32' y='44' font-family='Georgia,serif' font-size='38' fill='%234f8cff' text-anchor='middle'%3ES%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(art_ld)}</script>
<script type="application/ld+json">{json.dumps(faq_ld)}</script>
<style>
:root{{--bg:#0a0b0e;--bg2:#0e1014;--panel:#14171e;--ink:#f3f5f9;--soft:#c4cad6;--mute:#838b9b;--line:rgba(190,205,230,.10);--line2:rgba(190,205,230,.16);--accent:#4f8cff;--accent2:#86b3ff;--gold:#c9a24b;--sans:'Inter',system-ui,sans-serif;--serif:'Fraunces',Georgia,serif;}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
.nav{{position:sticky;top:0;z-index:50;background:rgba(10,11,14,.82);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}}
.nav .in{{max-width:1180px;margin:0 auto;padding:0 26px;height:66px;display:flex;align-items:center;justify-content:space-between}}
.brand{{font-family:var(--serif);font-size:20px}}.brand span{{color:var(--accent)}}
.nav a.back{{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--soft)}}
.nav a.back:hover{{color:var(--accent2)}}
.wrap{{max-width:760px;margin:0 auto;padding:0 26px}}
.hero{{padding:70px 0 34px;border-bottom:1px solid var(--line)}}
.cat{{display:inline-block;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent2);font-weight:600;margin-bottom:18px}}
h1.title{{font-family:var(--serif);font-weight:400;font-size:clamp(30px,5vw,50px);line-height:1.08;letter-spacing:-.015em;margin-bottom:22px}}
.byline{{display:flex;align-items:center;gap:14px;margin-top:24px}}
.byline img{{width:52px;height:52px;border-radius:50%;object-fit:cover;object-position:50% 20%;border:1px solid var(--line2)}}
.byline .who{{font-size:15px;font-weight:600}}
.byline .who small{{display:block;color:var(--mute);font-weight:400;font-size:13px;margin-top:2px}}
.actions{{display:flex;gap:12px;margin-top:26px;flex-wrap:wrap}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border-radius:999px;font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;transition:.2s;cursor:pointer;border:0}}
.btn.solid{{background:linear-gradient(135deg,var(--accent2),var(--accent));color:#08122a}}
.btn.solid:hover{{transform:translateY(-2px)}}
.btn.ghost{{border:1px solid var(--line2);color:var(--ink)}}
.btn.ghost:hover{{border-color:var(--accent);color:var(--accent2)}}
article{{padding:44px 0 20px;font-size:17.5px}}
article h2{{font-family:var(--serif);font-weight:500;font-size:28px;margin:44px 0 14px;line-height:1.2}}
article h3{{font-family:var(--serif);font-weight:500;font-size:21px;margin:32px 0 10px}}
article p{{margin:0 0 20px;color:#dfe3ea}}
article ul,article ol{{margin:0 0 22px 22px}}article li{{margin:0 0 10px;color:#dfe3ea}}
article strong{{color:#fff}}
article a{{color:var(--accent2);border-bottom:1px solid rgba(134,179,255,.3)}}
article code{{background:#1b1f28;padding:2px 6px;border-radius:5px;font-size:.9em;color:#cfe0ff}}
article table{{width:100%;border-collapse:collapse;margin:0 0 26px;font-size:15px}}
article th,article td{{border:1px solid var(--line2);padding:10px 12px;text-align:left;color:#dfe3ea}}
article th{{background:#12151c;color:#fff;font-weight:600}}
article em{{color:#eef2f8}}
.takeaways{{background:linear-gradient(140deg,rgba(79,140,255,.12),transparent);border:1px solid var(--line2);border-radius:16px;padding:28px 30px;margin:36px 0}}
.takeaways h3{{font-family:var(--serif);font-size:20px;margin-bottom:14px;color:#fff}}
.takeaways ul{{list-style:none;margin:0}}
.takeaways li{{position:relative;padding:8px 0 8px 26px;color:#dfe3ea;font-size:15.5px}}
.takeaways li::before{{content:'✦';position:absolute;left:0;color:var(--accent2)}}
.faq{{margin:40px 0}}
.faq h2{{font-family:var(--serif);font-weight:500;font-size:26px;margin-bottom:18px}}
.faq .item{{border-bottom:1px solid var(--line);padding:18px 0}}
.faq .q{{font-family:var(--serif);font-size:18px;color:#fff;margin-bottom:8px}}
.faq .a{{color:var(--soft);font-size:15.5px}}
.cta{{margin:40px 0 10px;background:var(--panel);border:1px solid var(--line2);border-radius:18px;padding:34px;text-align:center}}
.cta h3{{font-family:var(--serif);font-size:24px;margin-bottom:10px}}
.cta p{{color:var(--soft);margin-bottom:20px}}
.authorbox{{display:flex;gap:18px;align-items:flex-start;margin:36px 0;padding:26px;border:1px solid var(--line);border-radius:16px;background:var(--bg2)}}
.authorbox img{{width:70px;height:70px;border-radius:50%;object-fit:cover;object-position:50% 20%;flex-shrink:0;border:1px solid var(--line2)}}
.authorbox h3{{font-family:var(--serif);font-size:19px;margin-bottom:6px}}
.authorbox p{{color:var(--soft);font-size:14.5px}}
footer{{border-top:1px solid var(--line);margin-top:40px;padding:36px 0;color:var(--mute);font-size:13px}}
footer .in{{max-width:760px;margin:0 auto;padding:0 26px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}}
footer a{{color:var(--soft)}}
@media(max-width:600px){{article{{font-size:16.5px}}}}
</style></head><body>
<div class="nav"><div class="in"><a href="../index.html" class="brand">Scott <span>Tischler</span></a><a href="index.html" class="back">← All Articles</a></div></div>
<div class="hero"><div class="wrap">
<span class="cat">{ihtml.escape(a["cat"])}</span>
<h1 class="title">{ihtml.escape(a["title"])}</h1>
<div class="byline"><img src="data:image/jpeg;base64,{PORTRAIT}" alt="Scott Tischler"><div class="who">Scott Tischler<small>Founder &amp; Chairman, AIrecommend.ai · {a["pretty"]} · {a["read"]}</small></div></div>
<div class="actions"><a class="btn solid" href="pdf/{a['slug']}.pdf" download>⤓ Download PDF</a><a class="btn ghost" href="https://airecommend.ai" target="_blank" rel="noopener">Visit AIrecommend.ai</a></div>
</div></div>
<div class="wrap"><article>
{a["body"]}
<div class="takeaways"><h3>Key takeaways</h3><ul>{tk}</ul></div>
<div class="faq"><h2>Frequently asked questions</h2>{fq}</div>
<div class="authorbox"><img src="data:image/jpeg;base64,{PORTRAIT}" alt="Scott Tischler"><div><h3>About the author</h3><p>Scott Tischler is the Founder &amp; Chairman of AIrecommend.ai and a practitioner-authority on AI search and Answer Engine Optimization. With 20+ years in marketing technology — including American Express, MetLife, and UBS — and executive and professional study at Wharton, Harvard, and Oxford, he helps businesses become the ones AI recommends.</p></div></div>
<div class="cta"><h3>Want to be the business AI recommends?</h3><p>See how AIrecommend.ai builds the entity authority answer engines reward.</p><a class="btn solid" href="https://airecommend.ai" target="_blank" rel="noopener">Explore AIrecommend.ai</a></div>
</article></div>
<footer><div class="in"><div>© 2026 Scott Tischler. All rights reserved.</div><div><a href="../index.html">Home</a> · <a href="index.html">Articles</a> · <a href="/privacy.html">Privacy</a> · <a href="mailto:scott@airecommend.ai">Contact</a></div></div></footer>
<script defer src="/track.js"></script>
</body></html>'''

def print_html(a):
    tk = "".join(f"<li>{t}</li>" for t in a["takeaways"])
    fq = "".join(f'<div class="q">{ihtml.escape(q)}</div><div class="a">{ans}</div>' for q,ans in a["faq"])
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
@page{{size:Letter;margin:20mm 18mm 22mm;}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Helvetica,Arial,sans-serif;color:#1a1f2b;line-height:1.62;font-size:11.2pt}}
.cover{{border-bottom:3px solid #4f8cff;padding-bottom:16px;margin-bottom:22px}}
.brandrow{{display:flex;align-items:center;gap:14px;margin-bottom:20px}}
.brandrow img{{width:64px;height:64px;border-radius:50%;object-fit:cover;object-position:50% 20%}}
.brandrow .n{{font-size:17pt;color:#0a0b0e}}
.brandrow .n small{{display:block;font-size:9pt;color:#4f8cff;font-weight:600;letter-spacing:.04em;margin-top:2px}}
.cat{{font-size:8.5pt;letter-spacing:.16em;text-transform:uppercase;color:#4f8cff;font-weight:700}}
h1{{font-weight:500;font-size:24pt;line-height:1.12;margin:8px 0 10px;color:#0a0b0e}}
.meta{{font-size:9.5pt;color:#6b7280}}
h2{{font-weight:600;font-size:15pt;margin:20px 0 8px;color:#0a0b0e}}
h3{{font-weight:600;font-size:12.5pt;margin:15px 0 6px;color:#12151c}}
p{{margin:0 0 11px}}
ul,ol{{margin:0 0 12px 18px}}li{{margin:0 0 6px}}
strong{{color:#0a0b0e}}
a{{color:#2f6fe0;text-decoration:none}}
table{{width:100%;border-collapse:collapse;margin:0 0 14px;font-size:9.5pt}}
th,td{{border:1px solid #d5dbe6;padding:6px 8px;text-align:left}}
th{{background:#eef3fc;font-weight:700}}
code{{background:#eef1f6;padding:1px 4px;border-radius:4px;font-size:.9em}}
.takeaways{{background:#f3f7ff;border:1px solid #cbd9f5;border-radius:10px;padding:16px 18px;margin:18px 0}}
.takeaways h3{{margin-top:0;color:#1a3a7a}}
.takeaways ul{{list-style:none;margin:0}}
.takeaways li{{padding:5px 0 5px 18px;position:relative;font-size:10.2pt}}
.takeaways li::before{{content:'✦';position:absolute;left:0;color:#4f8cff}}
.faq{{margin-top:18px}}
.faq .q{{font-weight:600;font-size:11pt;color:#0a0b0e;margin-top:12px}}
.faq .a{{font-size:10.2pt;color:#333}}
.footer{{margin-top:22px;padding-top:12px;border-top:1px solid #d5dbe6;font-size:8.6pt;color:#6b7280;display:flex;justify-content:space-between}}
.author{{margin-top:18px;padding:14px 16px;background:#f7f9fc;border:1px solid #e2e8f2;border-radius:10px;font-size:9.6pt;color:#333}}
.author b{{color:#0a0b0e}}
</style></head><body>
<div class="cover">
<div class="brandrow"><img src="data:image/jpeg;base64,{PORTRAIT}" alt="Scott Tischler"><div class="n">Scott Tischler<small>FOUNDER &amp; CHAIRMAN · AIRECOMMEND.AI</small></div></div>
<div class="cat">{ihtml.escape(a["cat"])}</div>
<h1>{ihtml.escape(a["title"])}</h1>
<div class="meta">By Scott Tischler · {a["pretty"]} · {a["read"]}</div>
</div>
{a["body"]}
<div class="takeaways"><h3>Key takeaways</h3><ul>{tk}</ul></div>
<div class="faq"><h2>Frequently asked questions</h2>{fq}</div>
<div class="author"><b>About the author.</b> Scott Tischler is the Founder &amp; Chairman of AIrecommend.ai and a practitioner-authority on AI search and Answer Engine Optimization. With 20+ years in marketing technology — including American Express, MetLife, and UBS — and executive and professional study at Wharton, Harvard, and Oxford, he helps businesses become the ones AI recommends.</div>
<div class="footer"><span>© 2026 Scott Tischler · scotttischler.com</span><span>scott@airecommend.ai · AIrecommend.ai</span></div>
</body></html>'''

def build(articles):
    os.makedirs(os.path.join(ROOT,"articles","pdf"), exist_ok=True)
    for a in articles:
        open(os.path.join(ROOT,"articles",a["slug"]+".html"),"w").write(web_html(a))
        open(os.path.join(ROOT,"articles","pdf",a["slug"]+".print.html"),"w").write(print_html(a))
        print("wrote", a["slug"])

if __name__ == "__main__":
    from articles_today import ARTICLES
    build(ARTICLES)
