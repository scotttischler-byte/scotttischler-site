#!/usr/bin/env python3
"""Daily article source for the AEO engine.

Order of preference:
1. If content_queue/*.json has entries, use up to 2 of them (free, no API).
2. Otherwise call the Anthropic API to generate 2 fresh AEO articles,
   de-duplicated against everything already published.

Writes articles_today.py for publish_articles.py to build.
Requires ANTHROPIC_API_KEY in the environment ONLY when the queue is empty.
"""
import os, json, glob, datetime, shutil, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "content_queue")
DONE = os.path.join(QUEUE, "_published")
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def pretty(iso):
    y,m,d = [int(x) for x in iso.split("-")]
    return f"{MONTHS[m-1]} {d}, {y}"

def write_today(articles):
    for a in articles:
        a["faq"] = [tuple(x) for x in a.get("faq", [])]
    with open(os.path.join(ROOT, "articles_today.py"), "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("ARTICLES = " + repr(articles) + "\n")

def from_queue(today):
    files = sorted(glob.glob(os.path.join(QUEUE, "*.json")))
    if not files:
        return None
    os.makedirs(DONE, exist_ok=True)
    take = files[:2]
    arts = []
    for fp in take:
        a = json.load(open(fp))
        a["date"] = today; a["pretty"] = pretty(today); a.setdefault("read","8 min read")
        arts.append(a)
    for fp in take:
        shutil.move(fp, os.path.join(DONE, os.path.basename(fp)))
    print(f"Using {len(arts)} article(s) from queue; {len(files)-len(take)} left.")
    return arts

CANDIDATE_MODELS = [
    os.environ.get("MODEL",""),
    "claude-sonnet-4-5", "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-20250514", "claude-3-7-sonnet-latest",
    "claude-3-5-sonnet-latest", "claude-3-5-sonnet-20241022",
]

PROMPT = """You are Scott Tischler, Founder & Chairman of AIrecommend.ai and a practitioner-authority on Answer Engine Optimization (AEO), AI search, and generative-engine optimization (GEO). Write {n} NEW long-form articles for scotttischler.com.

Voice: first person, direct, practitioner, evidence-based, with honest hedging on opinions ("my read, not a guarantee"). Never fabricate statistics; you may reference AIrecommend.ai's "State of AI Search 2026" research only qualitatively. Do not claim any credential except that he is Founder & Chairman of AIrecommend.ai.

Topic lane: AI visibility / AEO / GEO / how ChatGPT, Gemini, Perplexity and Google's AI answers pick who to cite and recommend. Each article must be DISTINCT and must NOT duplicate any of these already-published slugs/titles:
{existing}

Return ONLY a JSON array of {n} objects, no prose, no markdown fences. Each object:
{{
 "slug": "kebab-case-unique",
 "cat": "one of: Measurement, Strategy, Playbook, How AI Works, Entity Authority, Technical, AI & Search",
 "title": "compelling specific title",
 "desc": "<=160 char meta description",
 "read": "e.g. 8 min read",
 "body": "the article as HTML using <h2>/<h3>/<p>/<ul>/<ol>/<strong>/<em>, ~1500-2000 words, opening with a direct answer, NO <h1>",
 "takeaways": ["5-6 concise takeaway strings"],
 "faq": [["question","self-contained answer"], ["q","a"], ["q","a"]]
}}
"""

def from_api(today, n=2):
    import anthropic
    cat = json.load(open(os.path.join(ROOT, "_catalog.json")))
    existing = "; ".join(sorted(c[0] for c in cat["catalog"]))[:6000]
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    prompt = PROMPT.format(n=n, existing=existing)
    last_err = None
    for model in [m for m in CANDIDATE_MODELS if m]:
        try:
            msg = client.messages.create(model=model, max_tokens=8000,
                                         messages=[{"role":"user","content":prompt}])
            text = "".join(b.text for b in msg.content if getattr(b,"type","")=="text").strip()
            text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
            arts = json.loads(text)
            slugs = {c[0] for c in cat["catalog"]}
            arts = [a for a in arts if a.get("slug") and a["slug"] not in slugs][:n]
            for a in arts:
                a["date"]=today; a["pretty"]=pretty(today); a.setdefault("read","8 min read")
            if arts:
                print(f"Generated {len(arts)} article(s) via {model}.")
                return arts
        except Exception as e:
            last_err = f"{model}: {e}"
            print("model attempt failed:", last_err)
            continue
    raise SystemExit("Generation failed for all candidate models. Last error: " + str(last_err))

if __name__ == "__main__":
    today = datetime.date.today().isoformat()
    arts = from_queue(today)
    if not arts:
        arts = from_api(today, n=2)
    write_today(arts)
    print("Wrote articles_today.py with", len(arts), "article(s).")
