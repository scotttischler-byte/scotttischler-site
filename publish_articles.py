#!/usr/bin/env python3
"""Reusable publisher: reads ARTICLES from articles_today.py, writes web+print HTML,
generates PDFs, and updates hub, sitemap, feed, and catalog. One command for the daily run.

Each ARTICLES entry needs: slug, cat, title, desc, date (YYYY-MM-DD), pretty, read, body,
takeaways (list[str]), faq (list[(q,a)]). Optional: card (hub blurb), feeddesc (rss blurb) —
default to desc. Run:  python3 publish_articles.py   then deploy the folder.
"""
import os, json, html as ihtml, subprocess, sys
from build_new_articles import web_html, print_html, ROOT

MONTHS_RFC = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

def rfc822(date_iso):
    import datetime
    y,m,d = [int(x) for x in date_iso.split("-")]
    dt = datetime.date(y,m,d)
    days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    mons=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    return f"{days[dt.weekday()]}, {d:02d} {mons[m-1]} {y} 09:00:00 +0000"

def publish(articles):
    os.makedirs(os.path.join(ROOT,"articles","pdf"), exist_ok=True)
    # 1. write HTML + print HTML
    for a in articles:
        open(os.path.join(ROOT,"articles",a["slug"]+".html"),"w").write(web_html(a))
        open(os.path.join(ROOT,"articles","pdf",a["slug"]+".print.html"),"w").write(print_html(a))
        print("wrote", a["slug"])
    # 2. PDFs (only the new print.html files)
    try:
        import asyncio
        from playwright.async_api import async_playwright
        async def gen():
            async with async_playwright() as p:
                b=await p.chromium.launch(); pg=await b.new_page()
                for a in articles:
                    f=os.path.join(ROOT,"articles","pdf",a["slug"]+".print.html")
                    await pg.goto("file://"+f); await pg.wait_for_timeout(400)
                    await pg.pdf(path=os.path.join(ROOT,"articles","pdf",a["slug"]+".pdf"),
                                 format="Letter",print_background=True,margin={"top":"0","bottom":"0","left":"0","right":"0"})
                    print("pdf", a["slug"])
                await b.close()
        asyncio.run(gen())
    except Exception as e:
        print("PDF generation skipped:", e)
    # 3. HUB
    hub=open(os.path.join(ROOT,"articles","index.html")).read()
    cards=""
    for a in articles:
        blurb=a.get("card", a["desc"])
        cards+=(f'<a class="card" data-cat="{ihtml.escape(a["cat"])}" href="{a["slug"]}.html">\n'
                f'      <span class="tag">{ihtml.escape(a["cat"])}</span>\n'
                f'      <h2>{ihtml.escape(a["title"])}</h2>\n'
                f'      <p>{ihtml.escape(blurb)}</p>\n'
                f'      <div class="meta">{a["pretty"]}</div>\n'
                f'      <div class="links"><span class="read">Read article →</span><span class="pdf" onclick="event.preventDefault();event.stopPropagation();window.location.href=\'pdf/{a["slug"]}.pdf\'">⤓ PDF</span></div>\n'
                f'    </a>\n')
    anchor='<div class="grid" id="grid">\n'
    hub=hub.replace(anchor, anchor+cards, 1)
    open(os.path.join(ROOT,"articles","index.html"),"w").write(hub)
    print("hub cards inserted")
    # 4. SITEMAP
    sm=open(os.path.join(ROOT,"sitemap.xml")).read()
    blocks=""
    for a in articles:
        blocks+=(f'  <url>\n    <loc>https://scotttischler.com/articles/{a["slug"]}.html</loc>\n'
                 f'    <lastmod>{a["date"]}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
        blocks+=(f'  <url>\n    <loc>https://scotttischler.com/articles/pdf/{a["slug"]}.pdf</loc>\n'
                 f'    <lastmod>{a["date"]}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.5</priority>\n  </url>\n')
    marker='<loc>https://scotttischler.com/articles/</loc>'
    idx=sm.find(marker); close=sm.find('</url>', idx)+len('</url>')+1
    sm=sm[:close]+"\n"+blocks+sm[close:]
    open(os.path.join(ROOT,"sitemap.xml"),"w").write(sm)
    print("sitemap updated:", sm.count("<loc>"), "urls")
    # 5. FEED
    fd=open(os.path.join(ROOT,"feed.xml")).read()
    items=""
    for a in articles:
        items+=(f'    <item>\n      <title>{ihtml.escape(a["title"])}</title>\n'
                f'      <link>https://scotttischler.com/articles/{a["slug"]}.html</link>\n'
                f'      <guid>https://scotttischler.com/articles/{a["slug"]}.html</guid>\n'
                f'      <category>{ihtml.escape(a["cat"])}</category>\n'
                f'      <dc:creator>Scott Tischler</dc:creator>\n'
                f'      <pubDate>{rfc822(a["date"])}</pubDate>\n'
                f'      <description>{ihtml.escape(a.get("feeddesc", a["desc"]))}</description>\n    </item>\n')
    fidx=fd.find('<item>'); istart=fd.rfind('\n',0,fidx)+1
    fd=fd[:istart]+items+fd[istart:]
    open(os.path.join(ROOT,"feed.xml"),"w").write(fd)
    print("feed updated:", fd.count("<item>"), "items")
    # 6. CATALOG
    cat=json.load(open(os.path.join(ROOT,"_catalog.json")))
    for a in reversed(articles):
        cat["catalog"]=[c for c in cat["catalog"] if c[0]!=a["slug"]]
        cat["catalog"].insert(0,[a["slug"],a["title"],a["cat"],a["date"]])
        if a["slug"] not in cat["live"]: cat["live"].insert(0,a["slug"])
    json.dump(cat, open(os.path.join(ROOT,"_catalog.json"),"w"), indent=0)
    print("catalog:", len(cat["catalog"]), "entries")
    # 7. IndexNow URL list for the caller to ping
    urls=[f"https://scotttischler.com/articles/{a['slug']}.html" for a in articles]
    urls.append("https://scotttischler.com/sitemap.xml")
    print("INDEXNOW_URLS="+json.dumps(urls))
    return urls

if __name__=="__main__":
    sys.path.insert(0, ROOT)
    from articles_today import ARTICLES
    publish(ARTICLES)
