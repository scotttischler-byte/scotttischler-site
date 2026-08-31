#!/usr/bin/env python3
"""Submit the 2 most recently published article URLs + the sitemap to IndexNow
(notifies Bing, Yandex, and the IndexNow network). Runs on the GitHub runner,
which has outbound internet."""
import os, json, glob, urllib.request, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://scotttischler.com"

# find the IndexNow key file (32 hex chars .txt at repo root)
keyfiles = [os.path.basename(f) for f in glob.glob(os.path.join(ROOT, "*.txt"))
            if re.fullmatch(r"[0-9a-f]{32}\.txt", os.path.basename(f))]
if not keyfiles:
    print("No IndexNow key file found; skipping.")
    raise SystemExit(0)
key = keyfiles[0][:-4]

cat = json.load(open(os.path.join(ROOT, "_catalog.json")))
newest = [c[0] for c in cat["catalog"][:2]]
urls = [f"{SITE}/articles/{s}.html" for s in newest] + [f"{SITE}/sitemap.xml"]

payload = json.dumps({
    "host": "scotttischler.com",
    "key": key,
    "keyLocation": f"{SITE}/{key}.txt",
    "urlList": urls,
}).encode()

req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=payload,
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        print("IndexNow:", r.status, "->", urls)
except Exception as e:
    print("IndexNow ping failed:", e)
