import json, re, html

NEW = [
  {"slug":"share-of-model","cat":"Measurement",
   "title":"Share of Model: The AI-Visibility Metric That Replaces Keyword Rankings",
   "card":"Keyword rank tells you nothing about whether AI recommends you. Share of Model does — the percentage of AI answers that actually name your brand. How to define, measure, and move it.",
   "feeddesc":"Keyword rank measures position on a page of links. Share of Model measures how often AI answers name you — and it's now the metric that matters. How to define, measure, and move it.",
   "date":"2026-08-27","pretty":"August 27, 2026","rfc":"Wed, 27 Aug 2026 09:00:00 +0000"},
  {"slug":"prompt-market-fit","cat":"Strategy",
   "title":"Prompt-Market Fit: How to Find the AI Questions Actually Worth Winning",
   "card":"Not every AI question is worth winning. Prompt-market fit is the overlap of real buyer intent, commercial value, and a realistic chance of being named. The method for finding it.",
   "feeddesc":"Most AEO effort is wasted chasing impressive prompts no buyer types. Prompt-market fit finds the questions that map to real intent and that you can actually win. The method.",
   "date":"2026-08-27","pretty":"August 27, 2026","rfc":"Wed, 27 Aug 2026 09:00:00 +0000"},
]

# ---- 1. HUB (articles/index.html) ----
hub = open("articles/index.html").read()
cards = ""
for a in NEW:
    cards += (f'<a class="card" data-cat="{html.escape(a["cat"])}" href="{a["slug"]}.html">\n'
              f'      <span class="tag">{html.escape(a["cat"])}</span>\n'
              f'      <h2>{html.escape(a["title"])}</h2>\n'
              f'      <p>{html.escape(a["card"])}</p>\n'
              f'      <div class="meta">{a["pretty"]}</div>\n'
              f'      <div class="links"><span class="read">Read article →</span><span class="pdf" onclick="event.preventDefault();event.stopPropagation();window.location.href=\'pdf/{a["slug"]}.pdf\'">⤓ PDF</span></div>\n'
              f'    </a>\n')
anchor = '<div class="grid" id="grid">\n'
assert anchor in hub, "grid anchor not found"
hub = hub.replace(anchor, anchor + cards, 1)
open("articles/index.html","w").write(hub)
print("hub: inserted", len(NEW), "cards")

# ---- 2. SITEMAP ----
sm = open("sitemap.xml").read()
blocks = ""
for a in NEW:
    blocks += (f'  <url>\n    <loc>https://scotttischler.com/articles/{a["slug"]}.html</loc>\n'
               f'    <lastmod>{a["date"]}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
    blocks += (f'  <url>\n    <loc>https://scotttischler.com/articles/pdf/{a["slug"]}.pdf</loc>\n'
               f'    <lastmod>{a["date"]}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.5</priority>\n  </url>\n')
# insert right after the /articles/ hub url block (before first real article)
marker = '<loc>https://scotttischler.com/articles/</loc>'
idx = sm.find(marker)
close = sm.find('</url>', idx) + len('</url>') + 1
sm = sm[:close] + "\n" + blocks + sm[close:]
open("sitemap.xml","w").write(sm)
print("sitemap: total <loc> now", sm.count("<loc>"))

# ---- 3. FEED ----
fd = open("feed.xml").read()
items = ""
for a in NEW:
    items += (f'    <item>\n      <title>{html.escape(a["title"])}</title>\n'
              f'      <link>https://scotttischler.com/articles/{a["slug"]}.html</link>\n'
              f'      <guid>https://scotttischler.com/articles/{a["slug"]}.html</guid>\n'
              f'      <category>{html.escape(a["cat"])}</category>\n'
              f'      <dc:creator>Scott Tischler</dc:creator>\n'
              f'      <pubDate>{a["rfc"]}</pubDate>\n'
              f'      <description>{html.escape(a["feeddesc"])}</description>\n    </item>\n')
fidx = fd.find('<item>')
istart = fd.rfind('\n', 0, fidx) + 1
fd = fd[:istart] + items + fd[istart:]
open("feed.xml","w").write(fd)
print("feed: items now", fd.count("<item>"))

# ---- 4. CATALOG ----
cat = json.load(open("_catalog.json"))
for a in reversed(NEW):
    entry = [a["slug"], a["title"], a["cat"], a["date"]]
    cat["catalog"] = [c for c in cat["catalog"] if c[0]!=a["slug"]]
    cat["catalog"].insert(0, entry)
    if a["slug"] not in cat["live"]:
        cat["live"].insert(0, a["slug"])
json.dump(cat, open("_catalog.json","w"), indent=0)
print("catalog: entries", len(cat["catalog"]), "live", len(cat["live"]))
