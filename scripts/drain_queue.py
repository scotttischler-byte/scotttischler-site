#!/usr/bin/env python3
"""Take the 2 oldest articles from content_queue/, stamp them with today's date,
and write articles_today.py for publish_articles.py to build. Consumed queue files
move to content_queue/_published/. No API, no key — pure file operations."""
import os, json, glob, datetime, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "content_queue")
DONE = os.path.join(QUEUE, "_published")
os.makedirs(DONE, exist_ok=True)

MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
def pretty(iso):
    y,m,d = [int(x) for x in iso.split("-")]
    return f"{MONTHS[m-1]} {d}, {y}"

today = datetime.date.today().isoformat()
files = sorted(f for f in glob.glob(os.path.join(QUEUE, "*.json")))

if not files:
    print("QUEUE EMPTY — nothing to publish. Refill content_queue/ with article JSON files.")
    # write an empty ARTICLES so publish_articles has nothing to do
    open(os.path.join(ROOT, "articles_today.py"), "w").write("ARTICLES = []\n")
    sys.exit(0)

take = files[:2]
articles = []
for f in take:
    a = json.load(open(f))
    a["date"] = today
    a["pretty"] = pretty(today)
    a.setdefault("read", "8 min read")
    a["faq"] = [tuple(x) for x in a.get("faq", [])]
    articles.append(a)

# write articles_today.py
with open(os.path.join(ROOT, "articles_today.py"), "w", encoding="utf-8") as out:
    out.write("# -*- coding: utf-8 -*-\n")
    out.write("ARTICLES = " + repr(articles) + "\n")

for f in take:
    shutil.move(f, os.path.join(DONE, os.path.basename(f)))

remaining = len(files) - len(take)
print(f"Staged {len(articles)} article(s) for {today}. Queue remaining: {remaining}")
if remaining <= 4:
    print(f"::warning::Content queue low ({remaining} left). Refill content_queue/ soon.")
