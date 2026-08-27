#!/usr/bin/env python3
import os, re, glob, html as ihtml, json, datetime
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "articles_src")
OUT = os.path.join(ROOT, "articles")
PDFDIR = os.path.join(OUT, "pdf")
os.makedirs(PDFDIR, exist_ok=True)

PORTRAIT = open(os.path.join(ROOT, "portrait_small_b64.txt")).read().strip()
SITE = "https://scotttischler.com"

MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
def pretty_date(iso):
    y,m,d = [int(x) for x in iso.split("-")]
    return f"{MONTHS[m-1]} {d}, {y}"

def seo_title(t):
    """<title> tag <= 60 chars (Google truncation). On-page H1 stays full."""
    t = t.strip(); suffix = " | Scott Tischler"
    if len(t) + len(suffix) <= 60: return t + suffix
    if len(t) <= 60: return t
    cut = t[:60]
    if " " in cut: cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,:;—-")

def seo_desc(d):
    """Meta description <= 160 chars, trimmed at a word boundary."""
    d = d.strip()
    if len(d) <= 160: return d
    cut = d[:160]
    if " " in cut: cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,:;—-")

# ---- full 20-topic catalog for the hub (live ones have a matching src file) ----
CATALOG = [
    ("ai-recommendation-study-2026","The AI Recommendation Study: What AI Actually Recommends (2026 Pilot)","Original Research","2026-07-30"),
    ("what-is-answer-engine-optimization","What Is Answer Engine Optimization (AEO)? The Definitive 2026 Guide","AEO Fundamentals","2026-07-28"),
    ("aeo-vs-seo","AEO vs. SEO: Why Ranking #1 No Longer Wins","Strategy","2026-07-28"),
    ("how-ai-decides-which-businesses-to-recommend","How AI Systems Actually Decide Which Businesses to Recommend","How AI Works","2026-07-28"),
    ("entity-authority","Entity Authority: The New Currency of Online Trust","Entity Authority","2026-07-28"),
    ("zero-click-era","The Zero-Click Era: How to Win When Nobody Clicks Through","Strategy","2026-07-28"),
    ("get-cited-by-chatgpt-claude-perplexity","How to Get Your Business Cited by ChatGPT, Claude, and Perplexity","Playbook","2026-07-28"),
    ("i-asked-chatgpt-to-recommend-a-business","I Asked ChatGPT to Recommend a Business in My Town — Here's What Actually Decided the Winner","AI & Search","2026-07-28"),
    ("competitor-recommended-by-ai","Your Competitor Is Being Recommended by AI Right Now — and You Have No Idea","AI & Search","2026-07-28"),
    ("businesses-ai-will-kill-first","The Businesses AI Will Quietly Kill First — and How to Survive the Shift","Business","2026-07-28"),
    ("category-creation","Category Creation: How to Build a Company Nobody Can Compete With","Business","2026-07-28"),
    ("franchising-misunderstood-wealth","Why Franchising Is the Most Misunderstood Path to Wealth in America","Franchise","2026-07-28"),
    ("before-you-buy-a-franchise","Before You Buy a Franchise: 7 Questions That Separate Winners From Cautionary Tales","Franchise","2026-07-28"),
    ("lab-grown-vs-natural-diamonds","Lab-Grown vs. Natural Diamonds: What Most Jewelers Won't Tell You","Jewelry","2026-07-28"),
    ("custom-engagement-ring-cost","The Real Cost of a Custom Engagement Ring — Broken Down by Someone Who Builds Them","Jewelry","2026-07-28"),
    ("discipline-over-motivation-training-after-40","Discipline Over Motivation: An Operator's Guide to Training After 40","Fitness","2026-07-28"),
    ("vertical-leap-title-lessons","What Winning a National Vertical-Leap Title Taught Me About Everything Else","Fitness","2026-07-28"),
    ("reviews-not-getting-recommended-by-ai","Why Your 5-Star Reviews Aren't Getting You Recommended by AI","AI & Search","2026-07-28"),
    ("ai-is-rewriting-your-brand","AI Is Rewriting Your Brand Right Now — Here's How to Take Back Control","AI & Search","2026-07-28"),
    ("zero-dollar-marketing-channel-2027","The $0 Marketing Channel Everyone Will Be Fighting Over by 2027","Business","2026-07-28"),
    ("moats-in-the-age-of-ai","Moats in the Age of AI: What Actually Protects a Business Now","Business","2026-07-28"),
    ("single-vs-multi-unit-franchise-math","Single-Unit vs. Multi-Unit: The Franchise Math That Builds Real Wealth","Franchise","2026-07-28"),
    ("semi-absentee-franchise-myth","The Semi-Absentee Franchise Myth — and How to Actually Get There","Franchise","2026-07-28"),
    ("buy-engagement-ring-without-getting-played","How to Buy an Engagement Ring Without Getting Played: A Jeweler's Field Guide","Jewelry","2026-07-28"),
    ("lost-art-of-plique-a-jour","The Lost Art of Plique-à-Jour — and Why Handmade Jewelry Still Wins","Jewelry","2026-07-28"),
    ("minimum-effective-dose-busy-founders","The Minimum Effective Dose: How Busy Founders Actually Stay in Shape","Fitness","2026-07-28"),
    ("strength-longevity-investment","Strength Is Your Best Longevity Investment — The Training Case for Your Next 30 Years","Fitness","2026-07-28"),
    ("structured-data-knowledge-graphs","Structured Data & Knowledge Graphs: Making Your Business Machine-Readable","Technical","2026-07-28"),
    ("local-business-aeo","Local Business AEO: Becoming the AI's Neighborhood Recommendation","Local","2026-07-28"),
    ("measuring-ai-referred-traffic","Measuring AI-Referred Traffic and Leads","Measurement","2026-07-28"),
    ("the-epistemic-shift","The Epistemic Shift: From Ten Blue Links to AI Recommendations","Research","2026-06-15"),
    ("aeo-for-service-businesses","Answer Engine Optimization for Service Businesses","Industry","2026-07-28"),
    ("google-ai-overviews-playbook","Google AI Overviews: A Practical Optimization Playbook","Playbook","2026-07-28"),
    ("reviews-reputation-ai-trust","Reviews, Reputation, and How AI Weighs Trust","Trust","2026-07-28"),
    ("content-architecture-answer-engines","Content Architecture for Answer Engines","Content","2026-07-28"),
    ("personal-brand-ai-will-recommend","Building a Personal Brand AI Will Recommend","Personal Brand","2026-07-28"),
    ("seo-agency-to-aeo-practice","From SEO Agency to AEO Practice: Repositioning for the AI Era","Agencies","2026-07-28"),
    ("franchising-category-defining-business","Franchising a Category-Defining Service Business","Franchise","2026-07-28"),
    ("founders-guide-category-creation","The Founder's Guide to Category Creation","Founders","2026-07-28"),
    ("future-of-search-2026-2030","The Future of Search, 2026–2030: Predictions for Business Owners","Trends","2026-07-28"),
    ("lessons-20-years-martech","Lessons from 20 Years in MarTech: What Actually Builds Authority","Experience","2026-07-28"),
    ("chatgpt-shopping-ai-product-recommendations","How to Get Your Products Recommended in ChatGPT Shopping and AI Assistants","AI & Search","2026-07-28"),
    ("death-of-the-homepage","The Death of the Homepage: Where Your Website Traffic Is Really Going","Business","2026-07-28"),
    ("recession-proof-franchises","Recession-Resistant Franchises: What the Data Actually Supports","Franchise","2026-07-28"),
    ("moissanite-vs-diamond","Moissanite vs. Diamond: An Honest Breakdown from a Jeweler","Jewelry","2026-07-28"),
    ("three-lifts-after-40","The Three Lifts That Matter Most After 40","Fitness","2026-07-28"),
    ("prompts-customers-type-about-your-industry","The Exact Prompts Your Customers Are Typing Into AI About Your Industry","Playbook","2026-07-28"),
    ("house-hacking-first-property","House Hacking: How to Buy Your First Property and Let It Pay for Itself","Real Estate","2026-07-28"),
    ("creative-financing-explained","Creative Financing Explained: Seller Financing, Subject-To, and Lease Options","Real Estate","2026-07-28"),
    ("reading-a-market-top","How to Read a Market Top: What Selling Before 2008 Taught Me","Real Estate","2026-07-28"),
    ("rent-by-the-room-coliving","The Rent-by-the-Room Playbook: Co-Living Before It Was a Trend","Real Estate","2026-07-28"),
    ("buying-commercial-warehouse","Buying Your First Commercial Property: Lessons From a 48,000 SqFt Warehouse","Real Estate","2026-07-28"),
    ("brrrr-method-honest","The BRRRR Method, Honestly: Where It Works and Where People Get Hurt","Real Estate","2026-07-28"),
    ("real-estate-in-age-of-ai","Real Estate Investing in the Age of AI: How Deals, Agents, and Buyers Are Changing","Real Estate","2026-07-28"),
    ("franchise-financing-options","How to Finance a Franchise: SBA Loans, ROBS, and Creative Options","Franchise","2026-07-28"),
    ("ai-agents-book-and-buy","When AI Agents Start Booking and Buying: Preparing Your Business for Agentic Commerce","AI & Search","2026-07-28"),
    ("wikipedia-wikidata-authority","Wikipedia, Wikidata, and Why They Decide What AI Believes About You","Entity Authority","2026-07-28"),
    ("aeo-myths-costing-visibility","5 AEO Myths That Are Quietly Costing You AI Visibility","Strategy","2026-07-28"),
    ("perplexity-vs-chatgpt-vs-google-ai","Perplexity vs. ChatGPT vs. Google AI: Where Your Customers Actually Ask","AI & Search","2026-07-28"),
    ("pricing-power-ai-era","Pricing Power in the AI Era: Why Being the Recommendation Lets You Charge More","Business","2026-07-28"),
    ("reputation-compounding-ai-era","Why Reputation Is the Only Asset That Compounds in the AI Era","Business","2026-07-28"),
    ("small-business-ai-playbook-2026","The Small Business AI Playbook for 2026","Business","2026-07-28"),
    ("first-90-days-franchise-owner","The First 90 Days as a Franchise Owner: A Survival Guide","Franchise","2026-07-28"),
    ("diamond-4cs-decoded","The 4Cs Decoded: Which Actually Matter Most When You Buy a Diamond","Jewelry","2026-07-28"),
    ("does-fine-jewelry-hold-value","Does Fine Jewelry Hold Value? An Honest Look at Jewelry as an Asset","Jewelry","2026-07-28"),
    ("training-around-injuries-after-40","Training Around Injuries After 40: How to Keep Progressing Without Breaking Down","Fitness","2026-07-28"),
    ("nutrition-for-busy-professionals","The No-Nonsense Nutrition Guide for Busy Professionals","Fitness","2026-07-28"),
    ("first-rental-property-analysis","How to Analyze Your First Rental Property in 15 Minutes","Real Estate","2026-07-28"),
    ("subject-to-deals-explained","Subject-To Deals Explained: The Creative Finance Strategy Most Investors Fear","Real Estate","2026-07-28"),
    ("self-storage-investing","Self-Storage Investing: The Boring Asset That Quietly Builds Wealth","Real Estate","2026-07-28"),
    ("raising-private-money","Raising Private Money: How to Fund Real Estate Deals Without a Bank","Real Estate","2026-07-28"),
    ("tax-strategies-real-estate-investors","The Tax Advantages That Make Real Estate Different From Every Other Investment","Real Estate","2026-07-28"),
    ("answer-engine-audit-diy","How to Audit Your Business's AI Visibility in One Afternoon","Playbook","2026-07-28"),
    ("schema-markup-that-matters","The Schema Markup That Actually Moves AI Visibility","Technical","2026-07-28"),
    ("ai-recommendation-b2b","How B2B Buyers Now Use AI to Build Their Shortlist","AI & Search","2026-07-28"),
    ("first-mover-advantage-aeo","The AEO First-Mover Advantage Won't Last — Here's the Window","Strategy","2026-07-28"),
    ("llms-txt-explained","What Is llms.txt? The New Standard for Talking to AI Crawlers","Technical","2026-07-28"),
    ("personal-brand-founder-moat","Your Personal Brand Is the Founder Moat AI Can't Copy","Business","2026-07-28"),
    ("referrals-in-the-ai-era","Word of Mouth at Machine Scale: Referrals in the AI Era","Business","2026-07-28"),
    ("build-authority-from-zero","How to Build Authority From Zero in a Crowded Market","Business","2026-07-28"),
    ("franchise-vs-startup","Franchise vs. Startup: The Honest Trade-offs Nobody Explains","Franchise","2026-07-28"),
    ("reading-franchise-disclosure-document","How to Read a Franchise Disclosure Document Like a Pro","Franchise","2026-07-28"),
    ("custom-jewelry-process","From Idea to Heirloom: How a Custom Jewelry Piece Is Actually Made","Jewelry","2026-07-28"),
    ("caring-for-fine-jewelry","How to Care for Fine Jewelry So It Lasts Generations","Jewelry","2026-07-28"),
    ("building-muscle-after-40-science","Building Muscle After 40: What the Science Actually Says","Fitness","2026-07-28"),
    ("recovery-is-the-real-performance-enhancer","Recovery Is the Real Performance Enhancer: Sleep, Stress, and Training","Fitness","2026-07-28"),
    ("staying-consistent-for-decades","How to Stay Consistent for Decades, Not Weeks","Fitness","2026-07-28"),
    ("agentic-commerce-guide","Agentic Commerce Is Here: How to Get Your Business Bought by AI Agents","AI & Search","2026-07-30"),
    ("mcp-explained-for-business","What Is MCP (Model Context Protocol)? AI Agents' Plumbing, Explained for Business Owners","AI & Search","2026-07-30"),
    ("ai-agents-changing-buying","How AI Agents Are Quietly Taking Over the Buying Decision","AI & Search","2026-07-30"),
    ("geo-vs-aeo-vs-seo-2026","GEO vs. AEO vs. SEO in 2026: The Only Framework You Need","Strategy","2026-07-30"),
    ("two-channel-search-google-and-ai","The Two-Channel Reality: Winning Google and AI Search at the Same Time","Strategy","2026-07-30"),
    ("vertical-ai-agents-industry","Why Vertical AI Agents Will Beat General AI in Your Industry","Business","2026-07-30"),
    ("small-language-models-advantage","Small Language Models: The Cheaper AI Advantage Most Businesses Are Missing","Business","2026-07-30"),
    ("ai-governance-for-businesses","AI Governance for Normal Businesses: What the EU AI Act and Agent Risks Actually Mean for You","Business","2026-07-30"),
    ("get-recommended-by-ai-agents","How to Make Sure AI Agents Recommend and Choose Your Business","Playbook","2026-07-30"),
    ("state-of-ai-search-2026","The State of AI Search in 2026: The Numbers Every Business Owner Should Know","Research","2026-07-30"),
]

def parse(path):
    raw = open(path, encoding="utf-8").read()
    meta = {}
    body_idx = raw.index("\nBODY:")
    head = raw[:body_idx]
    for line in head.splitlines():
        if ":" in line:
            k,v = line.split(":",1)
            meta[k.strip().lower()] = v.strip()
    rest = raw[body_idx+len("\nBODY:"):]
    # split TAKEAWAYS and FAQ
    tk_idx = rest.index("\nTAKEAWAYS:")
    body_md = rest[:tk_idx].strip()
    after = rest[tk_idx+len("\nTAKEAWAYS:"):]
    faq_idx = after.index("\nFAQ:")
    tk_md = after[:faq_idx].strip()
    faq_raw = after[faq_idx+len("\nFAQ:"):].strip()
    takeaways = [l[1:].strip() for l in tk_md.splitlines() if l.strip().startswith("-")]
    faqs = []
    q=a=None
    for line in faq_raw.splitlines():
        if line.startswith("Q:"):
            if q and a: faqs.append((q,a))
            q = line[2:].strip(); a=None
        elif line.startswith("A:"):
            a = line[2:].strip()
        elif line.strip() and a is not None:
            a += " "+line.strip()
    if q and a: faqs.append((q,a))
    meta["body_html"] = markdown.markdown(body_md, extensions=["extra","sane_lists"])
    meta["takeaways"] = takeaways
    meta["faqs"] = faqs
    return meta

def read_time_words(meta):
    return meta.get("read","")

# ------------------------- WEB ARTICLE TEMPLATE -------------------------
WEB_CSS = """
:root{--bg:#0a0b0e;--bg2:#0e1014;--panel:#14171e;--ink:#f3f5f9;--soft:#c4cad6;--mute:#838b9b;--line:rgba(190,205,230,.10);--line2:rgba(190,205,230,.16);--accent:#4f8cff;--accent2:#86b3ff;--gold:#c9a24b;--sans:'Inter',system-ui,sans-serif;--serif:'Fraunces',Georgia,serif;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.nav{position:sticky;top:0;z-index:50;background:rgba(10,11,14,.82);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.nav .in{max-width:1180px;margin:0 auto;padding:0 26px;height:66px;display:flex;align-items:center;justify-content:space-between}
.brand{font-family:var(--serif);font-size:20px}.brand span{color:var(--accent)}
.nav a.back{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--soft)}
.nav a.back:hover{color:var(--accent2)}
.wrap{max-width:760px;margin:0 auto;padding:0 26px}
.hero{padding:70px 0 34px;border-bottom:1px solid var(--line)}
.cat{display:inline-block;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent2);font-weight:600;margin-bottom:18px}
h1.title{font-family:var(--serif);font-weight:400;font-size:clamp(30px,5vw,50px);line-height:1.08;letter-spacing:-.015em;margin-bottom:22px}
.byline{display:flex;align-items:center;gap:14px;margin-top:24px}
.byline img{width:52px;height:52px;border-radius:50%;object-fit:cover;object-position:50% 20%;border:1px solid var(--line2)}
.byline .who{font-size:15px;font-weight:600}
.byline .who small{display:block;color:var(--mute);font-weight:400;font-size:13px;margin-top:2px}
.actions{display:flex;gap:12px;margin-top:26px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border-radius:999px;font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;transition:.2s;cursor:pointer;border:0}
.btn.solid{background:linear-gradient(135deg,var(--accent2),var(--accent));color:#08122a}
.btn.solid:hover{transform:translateY(-2px)}
.btn.ghost{border:1px solid var(--line2);color:var(--ink)}
.btn.ghost:hover{border-color:var(--accent);color:var(--accent2)}
article{padding:44px 0 20px;font-size:17.5px}
article h2{font-family:var(--serif);font-weight:500;font-size:28px;margin:44px 0 14px;line-height:1.2}
article h3{font-family:var(--serif);font-weight:500;font-size:21px;margin:32px 0 10px}
article p{margin:0 0 20px;color:#dfe3ea}
article ul,article ol{margin:0 0 22px 22px}article li{margin:0 0 10px;color:#dfe3ea}
article strong{color:#fff}
article a{color:var(--accent2);border-bottom:1px solid rgba(134,179,255,.3)}
article code{background:#1b1f28;padding:2px 6px;border-radius:5px;font-size:.9em;color:#cfe0ff}
article table{width:100%;border-collapse:collapse;margin:0 0 26px;font-size:15px}
article th,article td{border:1px solid var(--line2);padding:10px 12px;text-align:left;color:#dfe3ea}
article th{background:#12151c;color:#fff;font-weight:600}
article em{color:#eef2f8}
.takeaways{background:linear-gradient(140deg,rgba(79,140,255,.12),transparent);border:1px solid var(--line2);border-radius:16px;padding:28px 30px;margin:36px 0}
.takeaways h3{font-family:var(--serif);font-size:20px;margin-bottom:14px;color:#fff}
.takeaways ul{list-style:none;margin:0}
.takeaways li{position:relative;padding:8px 0 8px 26px;color:#dfe3ea;font-size:15.5px}
.takeaways li::before{content:'✦';position:absolute;left:0;color:var(--accent2)}
.faq{margin:40px 0}
.faq h2{font-family:var(--serif);font-weight:500;font-size:26px;margin-bottom:18px}
.faq .item{border-bottom:1px solid var(--line);padding:18px 0}
.faq .q{font-family:var(--serif);font-size:18px;color:#fff;margin-bottom:8px}
.faq .a{color:var(--soft);font-size:15.5px}
.cta{margin:40px 0 10px;background:var(--panel);border:1px solid var(--line2);border-radius:18px;padding:34px;text-align:center}
.cta h3{font-family:var(--serif);font-size:24px;margin-bottom:10px}
.cta p{color:var(--soft);margin-bottom:20px}
.authorbox{display:flex;gap:18px;align-items:flex-start;margin:36px 0;padding:26px;border:1px solid var(--line);border-radius:16px;background:var(--bg2)}
.authorbox img{width:70px;height:70px;border-radius:50%;object-fit:cover;object-position:50% 20%;flex-shrink:0;border:1px solid var(--line2)}
.authorbox h3{font-family:var(--serif);font-size:19px;margin-bottom:6px}
.authorbox p{color:var(--soft);font-size:14.5px}
footer{border-top:1px solid var(--line);margin-top:40px;padding:36px 0;color:var(--mute);font-size:13px}
footer .in{max-width:760px;margin:0 auto;padding:0 26px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
footer a{color:var(--soft)}
@media(max-width:600px){article{font-size:16.5px}}
"""

def web_article(slug, meta, prev_next):
    date_iso = meta["date"]; date_h = pretty_date(date_iso)
    title_tag = ihtml.escape(seo_title(meta['title'])); desc_tag = ihtml.escape(seo_desc(meta['meta']))
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in meta["faqs"]]}
    art_ld = {"@context":"https://schema.org","@type":"Article","headline":meta["title"],
        "description":meta["meta"],"datePublished":date_iso,"dateModified":date_iso,
        "author":{"@type":"Person","name":"Scott Tischler","url":SITE+"/","jobTitle":"Founder & Chairman, AIrecommend.ai"},
        "publisher":{"@type":"Organization","name":"Scott Tischler / AIrecommend.ai"},
        "mainEntityOfPage":f"{SITE}/articles/{slug}.html","articleSection":meta["category"]}
    faqs_html = "".join(f'<div class="item"><div class="q">{ihtml.escape(q)}</div><div class="a">{a}</div></div>' for q,a in meta["faqs"])
    tk_html = "".join(f"<li>{t}</li>" for t in meta["takeaways"])
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title_tag}</title>
<meta name="description" content="{desc_tag}">
<meta name="author" content="Scott Tischler">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="{SITE}/articles/{slug}.html">
<link rel="alternate" type="application/rss+xml" title="Scott Tischler — The AEO Library" href="{SITE}/feed.xml">
<meta property="og:type" content="article"><meta property="og:title" content="{ihtml.escape(meta['title'])}">
<meta property="og:description" content="{desc_tag}"><meta property="article:published_time" content="{date_iso}">
<meta property="article:author" content="Scott Tischler">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230a0b0e'/%3E%3Ctext x='32' y='44' font-family='Georgia,serif' font-size='38' fill='%234f8cff' text-anchor='middle'%3ES%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(art_ld)}</script>
<script type="application/ld+json">{json.dumps(faq_ld)}</script>
<style>{WEB_CSS}</style></head><body>
<div class="nav"><div class="in"><a href="../index.html" class="brand">Scott <span>Tischler</span></a><a href="index.html" class="back">← All Articles</a></div></div>
<div class="hero"><div class="wrap">
<span class="cat">{ihtml.escape(meta['category'])}</span>
<h1 class="title">{ihtml.escape(meta['title'])}</h1>
<div class="byline"><img src="{PORTRAIT}" alt="Scott Tischler"><div class="who">Scott Tischler<small>Founder &amp; Chairman, AIrecommend.ai · {date_h} · {meta.get('read','')}</small></div></div>
<div class="actions"><a class="btn solid" href="pdf/{slug}.pdf" download>⤓ Download PDF</a><a class="btn ghost" href="https://airecommend.ai" target="_blank" rel="noopener">Visit AIrecommend.ai</a></div>
</div></div>
<div class="wrap"><article>{meta['body_html']}
<div class="takeaways"><h3>Key takeaways</h3><ul>{tk_html}</ul></div>
<div class="faq"><h2>Frequently asked questions</h2>{faqs_html}</div>
<div class="authorbox"><img src="{PORTRAIT}" alt="Scott Tischler"><div><h3>About the author</h3><p>Scott Tischler is the Founder &amp; Chairman of AIrecommend.ai and a practitioner-authority on AI search and Answer Engine Optimization. With 20+ years in marketing technology — including American Express, MetLife, and UBS — and executive study at Wharton, Harvard, Yale, and Oxford, he helps businesses become the ones AI recommends.</p></div></div>
<div class="cta"><h3>Want to be the business AI recommends?</h3><p>See how AIrecommend.ai builds the entity authority answer engines reward.</p><a class="btn solid" href="https://airecommend.ai" target="_blank" rel="noopener">Explore AIrecommend.ai</a></div>
</article></div>
<footer><div class="in"><div>© {date_iso[:4]} Scott Tischler. All rights reserved.</div><div><a href="../index.html">Home</a> · <a href="index.html">Articles</a> · <a href="/privacy.html">Privacy</a> · <a href="mailto:scott@airecommend.ai">Contact</a></div></div></footer>
<script defer src="/track.js"></script>
</body></html>"""

# ------------------------- PRINT / PDF TEMPLATE -------------------------
PRINT_CSS = """
@page{size:Letter;margin:20mm 18mm 22mm;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Helvetica,Helvetica,Arial,sans-serif;color:#1a1f2b;line-height:1.62;font-size:11.2pt}
.cover{border-bottom:3px solid #4f8cff;padding-bottom:16px;margin-bottom:22px}
.brandrow{display:flex;align-items:center;gap:14px;margin-bottom:20px}
.brandrow img{width:64px;height:64px;border-radius:50%;object-fit:cover;object-position:50% 20%}
.brandrow .n{font-family:Helvetica,Helvetica,Arial,sans-serif;font-size:17pt;color:#0a0b0e}
.brandrow .n small{display:block;font-family:Helvetica,Arial,sans-serif;font-size:9pt;color:#4f8cff;font-weight:600;letter-spacing:.04em;margin-top:2px}
.cat{font-size:8.5pt;letter-spacing:.16em;text-transform:uppercase;color:#4f8cff;font-weight:700}
h1{font-family:Helvetica,Helvetica,Arial,sans-serif;font-weight:500;font-size:24pt;line-height:1.12;margin:8px 0 10px;color:#0a0b0e}
.meta{font-size:9.5pt;color:#6b7280}
h2{font-family:Helvetica,Helvetica,Arial,sans-serif;font-weight:600;font-size:15pt;margin:20px 0 8px;color:#0a0b0e}
h3{font-family:Helvetica,Helvetica,Arial,sans-serif;font-weight:600;font-size:12.5pt;margin:15px 0 6px;color:#12151c}
p{margin:0 0 11px}
ul,ol{margin:0 0 12px 18px}li{margin:0 0 6px}
strong{color:#0a0b0e}
a{color:#2f6fe0;text-decoration:none}
table{width:100%;border-collapse:collapse;margin:0 0 14px;font-size:9.5pt}
th,td{border:1px solid #d5dbe6;padding:6px 8px;text-align:left}
th{background:#eef3fc;font-weight:700}
code{background:#eef1f6;padding:1px 4px;border-radius:4px;font-size:.9em}
.takeaways{background:#f3f7ff;border:1px solid #cbd9f5;border-radius:10px;padding:16px 18px;margin:18px 0}
.takeaways h3{margin-top:0;color:#1a3a7a}
.takeaways ul{list-style:none;margin:0}
.takeaways li{padding:5px 0 5px 18px;position:relative;font-size:10.2pt}
.takeaways li::before{content:'\2022';position:absolute;left:0;color:#4f8cff}
.faq{margin-top:18px}
.faq .q{font-family:Helvetica,Helvetica,Arial,sans-serif;font-weight:600;font-size:11pt;color:#0a0b0e;margin-top:12px}
.faq .a{font-size:10.2pt;color:#333}
.footer{margin-top:22px;padding-top:12px;border-top:1px solid #d5dbe6;font-size:8.6pt;color:#6b7280;display:flex;justify-content:space-between}
.author{margin-top:18px;padding:14px 16px;background:#f7f9fc;border:1px solid #e2e8f2;border-radius:10px;font-size:9.6pt;color:#333}
.author b{color:#0a0b0e}
"""

def print_article(slug, meta):
    date_h = pretty_date(meta["date"])
    faqs_html = "".join(f'<div class="q">{ihtml.escape(q)}</div><div class="a">{re.sub("<[^>]+>","",a)}</div>' for q,a in meta["faqs"])
    tk_html = "".join(f"<li>{ihtml.escape(t)}</li>" for t in meta["takeaways"])
    body = meta["body_html"]
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>{PRINT_CSS}</style></head><body>
<div class="cover">
<div class="brandrow"><img src="{PORTRAIT}" alt="Scott Tischler"><div class="n">Scott Tischler<small>FOUNDER &amp; CHAIRMAN · AIRECOMMEND.AI</small></div></div>
<div class="cat">{ihtml.escape(meta['category'])}</div>
<h1>{ihtml.escape(meta['title'])}</h1>
<div class="meta">By Scott Tischler · {date_h} · {meta.get('read','')}</div>
</div>
{body}
<div class="takeaways"><h3>Key takeaways</h3><ul>{tk_html}</ul></div>
<div class="faq"><h2>Frequently asked questions</h2>{faqs_html}</div>
<div class="author"><b>About the author.</b> Scott Tischler is the Founder &amp; Chairman of AIrecommend.ai and a practitioner-authority on AI search and Answer Engine Optimization. With 20+ years in marketing technology — including American Express, MetLife, and UBS — and executive study at Wharton, Harvard, Yale, and Oxford, he helps businesses become the ones AI recommends.</div>
<div class="footer"><span>© {meta['date'][:4]} Scott Tischler · scotttischler.com</span><span>scott@airecommend.ai · AIrecommend.ai</span></div>
</body></html>"""

# ------------------------- BUILD -------------------------
built = {}
for path in sorted(glob.glob(os.path.join(SRC,"*.txt"))):
    meta = parse(path)
    slug = meta["slug"]
    built[slug] = meta
    open(os.path.join(OUT, slug+".html"),"w",encoding="utf-8").write(web_article(slug, meta, None))
    open(os.path.join(PDFDIR, slug+".print.html"),"w",encoding="utf-8").write(print_article(slug, meta))
    print("built", slug)

# save catalog + which are live for hub build
live = set(built.keys())
json.dump({"catalog":CATALOG,"live":list(live)}, open(os.path.join(ROOT,"_catalog.json"),"w"))
print("LIVE:", len(live), "of", len(CATALOG))
