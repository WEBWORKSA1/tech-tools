#!/usr/bin/env python3
"""Build the Tech.Tools static site into the repository root.  Run: python3 scripts/build.py"""
import json, os, sys, datetime
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from layout import page, icon, esc, sponsor_card, lead_card, video, hp, SITE, BROKER_URL
from tools_data import CATS, TOOLS
from guides_data import GUIDES
from directory_data import DIRECTORY, DIR_CATS

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TODAY = datetime.date.today().isoformat()
BYID = {t["id"]: t for t in TOOLS}
CATBY = {c["id"]: c for c in CATS}
URLS = []  # for sitemap

def write(path, html, priority="0.6"):
    full = os.path.join(OUT, path, "index.html") if not path.endswith(".html") else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    if not path.endswith("404.html"):
        URLS.append((path, priority))

def depth(path):
    return "../" * len([p for p in path.strip("/").split("/") if p]) if path else ""

def P(path, **kw):
    kw.setdefault("cats", CATS)
    return page(path=path, root=depth(path), **kw)

def crumbs(root, items):
    parts = [f'<a href="{root}">Home</a>'] + [f'<a href="{root}{u}">{esc(n)}</a>' if u else esc(n) for n, u in items]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"

def crumb_schema(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    for i, (n, u) in enumerate(items, 2):
        lst.append({"@type": "ListItem", "position": i, "name": n, **({"item": f"{SITE}/{u}"} if u else {})})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}

def tool_card(t, root):
    c = CATBY[t["cat"]]
    return (f'<a class="card tool-card" href="{root}tools/{t["id"]}/" data-cat="{t["cat"]}"><span class="ic">{icon(c["icon"])}</span>'
            f'<span><h3>{esc(t["name"])}</h3><p>{t["short"]}</p></span></a>')

def guide_card(g, root):
    return (f'<a class="card" href="{root}guides/{g["slug"]}/"><span class="badge blue">{g["cat"]}</span> '
            f'<span class="muted" style="font-size:.82rem">· {g["minutes"]} min read</span><h3 style="margin-top:10px">{esc(g["title"])}</h3>'
            f'<p>{esc(g["desc"])}</p></a>')

def faq_html(faqs):
    return '<div class="faq">' + "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs) + "</div>"

def faq_schema(faqs):
    import re
    strip = lambda s: re.sub("<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}

def lead_form(form_id="lead", compact=False):
    """High-intent, 3-step qualification form."""
    services = ["Website / web app development", "Cloud, DevOps & hosting", "Cybersecurity review", "IT support & managed services",
                "AI automation & chatbots", "SaaS / software selection", "SEO & marketing technology", "Data, analytics & dashboards"]
    choices = "\n".join(f'<label class="choice"><input type="checkbox" name="services" value="{s}"> {s}</label>' for s in services)
    return f'''<form id="{form_id}" data-tt-form="Expert Help Lead" data-steps novalidate
  data-success="Request received! A specialist will email you within 1 business day with next steps. Check your spam folder just in case.">
  {hp()}<input type="hidden" name="lead_type" value="Expert help / tech audit">
  <div class="steps-bar" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="fstep on">
    <h3>1. What do you need help with?</h3>
    <div class="choice-grid">{choices}</div>
    <div class="field" style="margin-top:12px"><label for="{form_id}-goal">Main goal</label>
      <select id="{form_id}-goal" name="goal" required><option value="">Choose one…</option><option>Launch something new</option><option>Fix or speed up something existing</option><option>Cut software/IT costs</option><option>Improve security / compliance</option><option>Automate a manual process</option><option>Just exploring options</option></select></div>
    <button type="button" class="btn btn-primary btn-block" data-next>Continue →</button>
  </div>
  <div class="fstep">
    <h3>2. A few project details</h3>
    <div class="row"><div class="field"><label for="{form_id}-budget">Budget</label><select id="{form_id}-budget" name="budget" required><option value="">Select…</option><option>Under $1,000</option><option>$1,000 – $5,000</option><option>$5,000 – $25,000</option><option>$25,000 – $100,000</option><option>$100,000+</option><option>Not sure yet</option></select></div>
    <div class="field"><label for="{form_id}-time">Timeline</label><select id="{form_id}-time" name="timeline" required><option value="">Select…</option><option>ASAP</option><option>Within 1 month</option><option>1–3 months</option><option>3+ months</option></select></div></div>
    <div class="field"><label for="{form_id}-size">Company size</label><select id="{form_id}-size" name="company_size"><option>Just me</option><option>2–10</option><option>11–50</option><option>51–250</option><option>250+</option></select></div>
    <div class="field"><label for="{form_id}-desc">Describe the project</label><textarea id="{form_id}-desc" name="details" required minlength="10" placeholder="What are you trying to achieve? Any tools or platforms involved?"></textarea></div>
    <div class="row"><button type="button" class="btn btn-ghost" data-prev>← Back</button><button type="button" class="btn btn-primary" data-next>Continue →</button></div>
  </div>
  <div class="fstep">
    <h3>3. Where should we send your plan?</h3>
    <div class="row"><div class="field"><label for="{form_id}-name">Full name</label><input id="{form_id}-name" name="name" type="text" required autocomplete="name"></div>
    <div class="field"><label for="{form_id}-email">Work email</label><input id="{form_id}-email" name="email" type="email" required autocomplete="email"></div></div>
    <div class="row"><div class="field"><label for="{form_id}-co">Company / website</label><input id="{form_id}-co" name="company" type="text" autocomplete="organization"></div>
    <div class="field"><label for="{form_id}-phone">Phone (optional)</label><input id="{form_id}-phone" name="phone" type="tel" autocomplete="tel"></div></div>
    <div class="field"><label for="{form_id}-country">Country</label><input id="{form_id}-country" name="country" type="text" autocomplete="country-name"></div>
    <label class="check"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted about my request and accept the <a href="{{ROOT}}privacy/">Privacy Policy</a>.</label>
    <div class="row" style="margin-top:14px"><button type="button" class="btn btn-ghost" data-prev>← Back</button><button type="submit" class="btn btn-accent">Get my free plan →</button></div>
    <p class="form-note">No spam, no obligation. We never sell your details.</p>
  </div>
  <div class="form-status" role="status"></div>
</form>'''

def quick_lead(root):
    return f'''<form class="card" data-tt-form="Quick Lead" data-success="Thanks! We'll email you within 1 business day.">
  {hp()}<h3>Get a free tech stack audit</h3><p>Tell us what you're working on — we'll reply with a practical plan.</p>
  <div class="field"><label for="ql-name">Name</label><input id="ql-name" name="name" type="text" required></div>
  <div class="field"><label for="ql-email">Work email</label><input id="ql-email" name="email" type="email" required></div>
  <div class="field"><label for="ql-need">What do you need?</label><select id="ql-need" name="need" required><option value="">Choose…</option><option>Website or app built</option><option>Cloud / hosting help</option><option>Security review</option><option>IT support</option><option>AI automation</option><option>Pick the right software</option><option>Something else</option></select></div>
  <button class="btn btn-accent btn-block" type="submit">Get my free audit →</button>
  <p class="form-note">Free · No obligation · Reply in 1 business day</p><div class="form-status" role="status"></div></form>'''

# ============================================================ HOME
def build_home():
    root = ""
    popular = [t for t in TOOLS if t["popular"]]
    cats = "\n".join(f'''<a class="card cat-card" href="tools/#{c["id"]}"><span class="ic" style="width:42px;height:42px;border-radius:11px;display:grid;place-items:center;background:var(--primary-soft);color:var(--primary)">{icon(c["icon"])}</span>
      <h3>{c["name"]}</h3><p>{c["blurb"]}</p><span class="count">{sum(1 for t in TOOLS if t["cat"]==c["id"])} tools →</span></a>''' for c in CATS)
    vids = "\n".join(f'<div>{video(g["video"][0], g["video"][1])}<p style="margin-top:8px"><a href="guides/{g["slug"]}/"><b>{esc(g["title"].split(":")[0])}</b></a></p></div>' for g in GUIDES[:3])
    faqs = [("Are the tools really free?", "Yes. Every tool is free with no sign-up. The site is supported by advertising, sponsorships and voluntary donations."),
            ("Is my data uploaded?", "No. Nearly every tool runs entirely in your browser. The only exceptions are the IP and DNS lookups, which query public services directly from your browser — we don't store results."),
            ("Can I suggest a tool?", "Absolutely — use the contact form or submit it to the directory. Popular requests get built first."),
            ("Can you build something custom for my business?", "Yes. Our Get Expert Help service matches you with vetted developers, IT and security specialists. The first consultation is free.")]
    body = f'''
<section class="hero"><div class="container">
  <span class="eyebrow">{icon("shield",14)} 100% in-browser · No sign-up · Free forever</span>
  <h1>The fast, private toolbox for <em>everything tech</em>.</h1>
  <p class="lead">{len(TOOLS)} free utilities for developers, IT pros, marketers and makers — format JSON, look up DNS, generate passwords, compress images and more. Your data never leaves your device.</p>
  <form class="hero-search" id="hero-search" role="search"><input type="search" placeholder="What do you need? e.g. json, dns, password, qr…" aria-label="Search tools"><button class="btn btn-primary" type="submit">{icon("search",18)} Search</button></form>
  <div class="chips">{"\n".join(f'<a class="chip" href="tools/{t["id"]}/">{esc(t["name"].split(" (")[0])}</a>' for t in popular[:8])}</div>
  <div class="stats"><div class="stat"><b>{len(TOOLS)}</b><span>working tools</span></div><div class="stat"><b>{len(CATS)}</b><span>categories</span></div><div class="stat"><b>0</b><span>uploads required</span></div><div class="stat"><b>{len(GUIDES)}</b><span>in-depth guides</span></div></div>
</div></section>

<section class="block" style="padding-top:8px"><div class="container">
  <div class="section-head"><div><h2>Most popular tools</h2><p>The utilities people reach for every day.</p></div><a class="btn btn-ghost btn-sm" href="tools/">Browse all {len(TOOLS)} →</a></div>
  <div class="grid g3">{"\n".join(tool_card(t, root) for t in popular)}</div>
  <div id="recent-wrap" class="hidden" style="margin-top:28px"><h3>Recently used</h3><div class="chips" id="recent"></div></div>
</div></section>

<section class="block alt"><div class="container">
  <div class="section-head"><div><h2>Browse by category</h2><p>Organised the way you work.</p></div></div>
  <div class="grid g4">{cats}</div>
</div></section>

<section class="block"><div class="container">
  <div class="lead-band">
    <div><span class="eyebrow" style="background:rgba(251,191,36,.15);color:#fde68a">For businesses</span>
      <h2>Tools solve tasks. Experts solve projects.</h2>
      <p>When you need more than a utility — a new website, a cloud migration, a security review or an AI workflow — we'll match you with a vetted specialist and send a practical plan.</p>
      <ul><li>Free tech stack audit and recommendations</li><li>Vetted developers, IT, cloud and security pros</li><li>Clear scope and budget before any commitment</li><li>Reply within 1 business day</li></ul>
      <a class="btn btn-accent" href="get-expert-help/">Start your free audit →</a></div>
    {quick_lead(root)}
  </div>
</div></section>

<section class="block"><div class="container">
  <div class="section-head"><div><h2>Learn the fundamentals</h2><p>Plain-English guides written by practitioners, each paired with a hand-picked video.</p></div><a class="btn btn-ghost btn-sm" href="guides/">All guides →</a></div>
  <div class="grid g3">{"\n".join(guide_card(g, root) for g in GUIDES[:6])}</div>
</div></section>

<section class="block alt"><div class="container">
  <div class="section-head"><div><h2>Watch &amp; learn</h2><p>Curated videos from leading educators, embedded in privacy-enhanced mode.</p></div><a class="btn btn-ghost btn-sm" href="videos/">Video library →</a></div>
  <div class="grid g3">{vids}</div>
</div></section>

<section class="block"><div class="container"><div class="grid g3">
  <a class="card" href="directory/"><span class="ic" style="color:var(--primary)">{icon("grid",28)}</span><h3 style="margin-top:10px">Software directory</h3><p>{len(DIRECTORY)} hand-picked apps for building, shipping and securing — tagged free, freemium or paid.</p><span class="btn btn-ghost btn-sm">Explore the directory</span></a>
  <a class="card" href="contests/"><span class="ic" style="color:var(--accent)">{icon("trophy",28)}</span><h3 style="margin-top:10px">Build Challenge</h3><p>Build a useful browser tool, win prizes and get featured to thousands of visitors.</p><span class="btn btn-ghost btn-sm">See the challenge</span></a>
  <a class="card" href="careers/"><span class="ic" style="color:var(--ok)">{icon("users",28)}</span><h3 style="margin-top:10px">Join the talent network</h3><p>Developers, writers and video creators: get paid projects from Tech.Tools and our clients.</p><span class="btn btn-ghost btn-sm">Apply now</span></a>
</div></div></section>

<section class="block alt"><div class="container split">
  <div><span class="eyebrow">{icon("mega",14)} Advertise</span><h2>Reach developers, IT buyers and marketers.</h2><p class="muted">Sponsor a tool, feature your product in the directory, or take over a category. Native, clearly-labelled placements on high-intent pages.</p><a class="btn btn-primary" href="advertise/">View sponsorship packages</a> <a class="btn btn-ghost" href="partners/">Partner with us</a></div>
  <div><span class="eyebrow">{icon("heart",14)} Support</span><h2>Keep Tech.Tools free and independent.</h2><p class="muted">Donations fund servers, new tools, contest prizes and paying great contributors. Every bit helps.</p><a class="btn btn-accent" href="support/">Support the project</a></div>
</div></section>

<section class="block"><div class="container prose" style="margin:0 auto"><h2 class="center">Frequently asked questions</h2>{faq_html(faqs)}</div></section>
'''
    recent_js = '''<script>(function(){try{var r=JSON.parse(localStorage.getItem("tt-recent")||"[]");if(!r.length)return;var idx=(window.TT_INDEX||[]).filter(function(i){return i.c!=="Guide"});var h=r.map(function(id){var t=idx.filter(function(i){return i.u==="tools/"+id+"/"})[0];return t?'<a class="chip" href="'+t.u+'">'+t.t+"</a>":""}).join("");if(h){document.getElementById("recent").innerHTML=h;document.getElementById("recent-wrap").classList.remove("hidden")}}catch(e){}})();</script>'''
    schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": "Tech.Tools", "url": SITE + "/",
               "potentialAction": {"@type": "SearchAction", "target": SITE + "/tools/?q={search_term_string}", "query-input": "required name=search_term_string"}},
              {"@context": "https://schema.org", "@type": "Organization", "name": "Tech.Tools", "url": SITE + "/", "logo": SITE + "/assets/img/favicon.svg"},
              faq_schema(faqs)]
    write("", P("", title="Tech.Tools — Free Online Tech Tools for Developers, IT & Marketers",
                desc=f"{len(TOOLS)} free, private, in-browser tech tools: JSON formatter, DNS lookup, password generator, regex tester, image compressor and more. Plus guides, videos and expert help.",
                body=body, schema=schema, scripts=recent_js), "1.0")

# ============================================================ TOOLS INDEX + PAGES
def build_tools():
    root = "../"
    sections = ""
    for c in CATS:
        items = [t for t in TOOLS if t["cat"] == c["id"]]
        sections += f'<section id="{c["id"]}" class="mt"><h2 style="display:flex;gap:10px;align-items:center">{icon(c["icon"],24)} {c["name"]} <span class="muted" style="font-size:1rem;font-weight:500">({len(items)})</span></h2><p class="muted">{c["blurb"]}</p><div class="grid g3">{"\n".join(tool_card(t, root) for t in items)}</div></section>'
    filt = '<button class="on" data-f="all">All</button>' + "\n".join(f'<button data-f="{c["id"]}">{c["name"]}</button>' for c in CATS)
    body = f'''<div class="container page-head">{crumbs(root, [("Tools", "")])}<h1>All tech tools</h1><p class="lead">{len(TOOLS)} free utilities across {len(CATS)} categories. Everything runs in your browser — fast, private, no account needed.</p>
<input type="search" data-filter-input="toolgrid" placeholder="Filter tools…" aria-label="Filter tools" style="max-width:420px;margin:10px 0 14px">
<div class="filters" data-filter-group="toolgrid">{filt}</div></div>
<div class="container" id="toolgrid">{sections}</div>
<div class="container mt">{sponsor_card(root)}</div>
<script>(function(){{var q=new URLSearchParams(location.search).get("q");if(q){{var i=document.querySelector("[data-filter-input]");i.value=q;i.dispatchEvent(new Event("input"))}}}})();</script>'''
    # hide empty category sections when filtering
    body += '''<script>document.addEventListener("input",h);document.addEventListener("click",function(){setTimeout(h,0)});function h(){document.querySelectorAll("#toolgrid section").forEach(function(s){s.classList.toggle("hidden",!s.querySelector("[data-cat]:not(.hidden)"))})}</script>'''
    write("tools/", P("tools/", title="All Free Online Tech Tools", desc=f"Browse {len(TOOLS)} free online tools for developers, IT, security, SEO, text and design. No sign-up, runs in your browser.",
                      body=body, active="tools/", schema=crumb_schema([("Tools", "tools/")])), "0.9")

    for t in TOOLS:
        path = f"tools/{t['id']}/"; root = "../../"; c = CATBY[t["cat"]]
        rel = [BYID[x] for x in t["related"] if x in BYID] or [x for x in TOOLS if x["cat"] == t["cat"] and x["id"] != t["id"]][:4]
        guides = [g for g in GUIDES if t["id"] in g["tools"]]
        steps = "\n".join(f"<li>{s}</li>" for s in t["steps"])
        about = t["about"].replace('href="../../', f'href="{root}')
        guide_box = "\n".join(f'<a class="card" href="{root}guides/{g["slug"]}/" style="padding:14px"><span class="badge blue">Guide</span><h3 style="font-size:1rem;margin:8px 0 0">{esc(g["title"])}</h3></a>' for g in guides)
        body = f'''<div class="container page-head">{crumbs(root, [("Tools", "tools/"), (c["name"], f"tools/#{c['id']}"), (t["name"], "")])}
<h1>{esc(t["name"])}</h1><p class="lead">{t["short"]}</p>
<div class="trust"><span>Runs in your browser</span><span>No sign-up</span><span>Free forever</span></div></div>
<div class="container tool-layout">
  <div>
    <div class="workspace" data-tool="{t["js_id"]}"><noscript>This tool needs JavaScript enabled.</noscript><p class="muted">Loading tool…</p></div>
    <div class="toolbar" style="margin-top:10px"><button class="btn btn-ghost btn-sm" onclick="TT.copy(location.href)">Share this tool</button><a class="btn btn-ghost btn-sm" href="{root}contact/?subject={quote('Bug report: ' + t['name'])}">Report an issue</a></div>
    <article class="prose mt">
      <h2>How to use the {esc(t["name"])}</h2><ol>{steps}</ol>
      <h2>About this tool</h2>{about}
      <h2>Frequently asked questions</h2>{faq_html(t["faqs"])}
    </article>
    <div class="mt">{lead_card(root, "your business")}</div>
  </div>
  <aside class="side">
    {lead_card(root, "your team")}
    <div class="card"><h3>Related tools</h3><div style="display:flex;flex-direction:column;gap:8px">{"\n".join(f'<a href="{root}tools/{r["id"]}/">{esc(r["name"])} →</a>' for r in rel)}</div></div>
    {guide_box}
    {sponsor_card(root)}
  </aside>
</div>'''
        schema = [crumb_schema([("Tools", "tools/"), (t["name"], path)]),
                  {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": t["name"], "applicationCategory": "DeveloperApplication" if t["cat"] in ("developer", "network") else "UtilitiesApplication",
                   "operatingSystem": "Any (web browser)", "url": f"{SITE}/{path}", "description": t["desc"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
                  faq_schema(t["faqs"])]
        write(path, P(path, title=t["title"], desc=t["desc"], body=body, active="tools/", schema=schema,
                      scripts=f'<script src="{root}assets/js/tools.js"></script>'), "0.8")

# ============================================================ GUIDES + VIDEOS
def build_guides():
    root = "../"
    body = f'''<div class="container page-head">{crumbs(root, [("Guides", "")])}<h1>Guides</h1><p class="lead">Clear, practical explanations of the technology you use every day — each with a curated video and links to the matching tools.</p></div>
<div class="container"><div class="grid g3">{"\n".join(guide_card(g, root) for g in GUIDES)}</div><div class="mt">{lead_card(root, "your project")}</div></div>'''
    write("guides/", P("guides/", title="Tech Guides — JSON, DNS, Regex, Git, Security & More", desc="Practical, plain-English guides to JSON, regular expressions, Git, DNS, passwords, TLS, cron, Linux and subnetting.",
                       body=body, active="guides/", schema=crumb_schema([("Guides", "guides/")])), "0.8")
    for g in GUIDES:
        path = f"guides/{g['slug']}/"; root = "../../"
        b = g["body"].replace('href="../../', f'href="{root}')
        tools = "\n".join(tool_card(BYID[x], root) for x in g["tools"] if x in BYID)
        others = [o for o in GUIDES if o["slug"] != g["slug"]][:3]
        body = f'''<div class="container page-head">{crumbs(root, [("Guides", "guides/"), (g["title"].split(":")[0], "")])}
<span class="badge blue">{g["cat"]}</span> <span class="muted" style="font-size:.85rem">· {g["minutes"]} min read · Updated {TODAY}</span>
<h1 style="margin-top:12px">{esc(g["title"])}</h1><p class="lead">{esc(g["desc"])}</p></div>
<div class="container tool-layout"><article class="prose">
  {video(g["video"][0], g["video"][1])}<p class="form-note">Video: {esc(g["video"][1])}. Embedded from YouTube in privacy-enhanced mode; all rights belong to the creator.</p>
  {b}
  <h2>Try the tools</h2><div class="grid g2" style="max-width:none">{tools}</div>
  <div class="callout mt">Found an error or want a topic covered? <a href="{root}contact/">Tell us</a> — we review every message.</div>
</article>
<aside class="side">{lead_card(root, "your project")}<div class="card"><h3>More guides</h3><div style="display:flex;flex-direction:column;gap:8px">{"\n".join(f'<a href="{root}guides/{o["slug"]}/">{esc(o["title"].split(":")[0])} →</a>' for o in others)}</div></div>{sponsor_card(root)}</aside></div>'''
        schema = [crumb_schema([("Guides", "guides/"), (g["title"], path)]),
                  {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"], "datePublished": TODAY, "dateModified": TODAY,
                   "author": {"@type": "Organization", "name": "Tech.Tools Editorial"}, "publisher": {"@type": "Organization", "name": "Tech.Tools"}, "mainEntityOfPage": f"{SITE}/{path}"},
                  {"@context": "https://schema.org", "@type": "VideoObject", "name": g["video"][1], "description": f"Video lesson accompanying the guide: {g['title']}",
                   "thumbnailUrl": f"https://i.ytimg.com/vi/{g['video'][0]}/hqdefault.jpg", "uploadDate": "2020-01-01", "embedUrl": f"https://www.youtube-nocookie.com/embed/{g['video'][0]}"}]
        write(path, P(path, title=g["title"], desc=g["desc"], body=body, active="guides/", schema=schema, og_type="article"), "0.7")

    # videos
    root = "../"
    cards = "\n".join(f'<div class="card" style="padding:12px">{video(g["video"][0], g["video"][1])}<h3 style="font-size:1rem;margin:12px 0 4px">{esc(g["video"][1])}</h3><p style="margin:0;font-size:.88rem"><a href="{root}guides/{g["slug"]}/">Read the companion guide →</a></p></div>' for g in GUIDES)
    body = f'''<div class="container page-head">{crumbs(root, [("Videos", "")])}<h1>Video library</h1><p class="lead">Hand-picked lessons from respected educators on the fundamentals behind our tools. Videos load only when you press play (privacy-enhanced mode).</p></div>
<div class="container"><div class="grid g3">{cards}</div>
<div class="callout mt">Are you a creator? <a href="{root}partners/">Partner with us</a> to have your tutorials featured, or <a href="{root}advertise/">sponsor the library</a>.</div></div>'''
    write("videos/", P("videos/", title="Tech Video Library — Free Lessons on JSON, DNS, Git, Linux & Security", desc="Curated free video lessons on JSON, regex, Git, DNS, passwords, Base64, cron, Linux, TLS and IP subnetting.", body=body, active="videos/"), "0.6")

# ============================================================ DIRECTORY
def build_directory():
    root = "../"
    filt = '<button class="on" data-f="all">All</button>' + "\n".join(f'<button data-f="{k}">{v}</button>' for k, v in DIR_CATS)
    catname = dict(DIR_CATS)
    items = "\n".join(f'''<div class="card dir-item" data-cat="{d["cat"]}"><div class="meta"><span class="badge blue">{catname[d["cat"]]}</span><span class="badge {"green" if d["price"] in ("Free","Open source") else ""}">{d["price"]}</span></div>
<h3 style="margin:0">{esc(d["name"])}</h3><p style="margin:0">{esc(d["desc"])}</p><a class="go" href="{d["url"]}" target="_blank" rel="noopener nofollow">Visit site ↗</a></div>''' for d in DIRECTORY)
    featured = '''<div class="card dir-item" style="border:2px dashed var(--accent)"><div class="meta"><span class="badge">Featured slot</span></div><h3 style="margin:0">Your product here</h3><p style="margin:0">Pinned at the top of every directory view, with a logo and call-to-action.</p><a class="go" href="../advertise/">Get featured →</a></div>'''
    body = f'''<div class="container page-head">{crumbs(root, [("Directory", "")])}<h1>Software directory</h1>
<p class="lead">{len(DIRECTORY)} trusted apps and services for building, shipping, securing and growing — curated by the Tech.Tools team. We list tools on merit; sponsored placements are always labelled.</p>
<div class="toolbar"><a class="btn btn-primary btn-sm" href="submit/">+ Submit a tool</a><a class="btn btn-ghost btn-sm" href="../advertise/">Get featured</a></div>
<input type="search" data-filter-input="dirgrid" placeholder="Search the directory…" aria-label="Search directory" style="max-width:420px;margin:10px 0 14px">
<div class="filters" data-filter-group="dirgrid">{filt}</div></div>
<div class="container"><div class="grid g3" id="dirgrid">{featured}{items}</div>
<p class="form-note mt">Product names, logos and brands are property of their respective owners and are used for identification only. Listing does not imply endorsement by or affiliation with those companies. Links may be updated over time; <a href="../contact/">report a broken link</a>.</p>
<div class="mt">{lead_card(root, "choosing the right software")}</div></div>'''
    write("directory/", P("directory/", title="Software Directory — Best Developer, Cloud, Security & AI Tools", desc=f"Curated directory of {len(DIRECTORY)} trusted developer, cloud, design, productivity, security, AI, SEO and monitoring tools — free, freemium and paid.", body=body, active="directory/"), "0.8")

    root = "../../"
    cats_opt = "\n".join(f"<option>{v}</option>" for _, v in DIR_CATS)
    body = f'''<div class="container page-head">{crumbs(root, [("Directory", "directory/"), ("Submit a tool", "")])}<h1>Submit your tool</h1><p class="lead">Built something developers, IT teams or marketers will love? Submit it for free review — or choose a featured listing for priority placement.</p></div>
<div class="container split"><form class="card" data-tt-form="Directory Submission" data-success="Thanks! Your tool is in the review queue. We'll email you when it's live or if we have questions.">
{hp()}<div class="row"><div class="field"><label for="st-name">Tool name</label><input id="st-name" name="tool_name" required></div><div class="field"><label for="st-url">Website URL</label><input id="st-url" name="tool_url" type="url" required placeholder="https://"></div></div>
<div class="row"><div class="field"><label for="st-cat">Category</label><select id="st-cat" name="category">{cats_opt}</select></div><div class="field"><label for="st-price">Pricing</label><select id="st-price" name="pricing"><option>Free</option><option>Freemium</option><option>Paid</option><option>Open source</option></select></div></div>
<div class="field"><label for="st-desc">One-line description (max 140 chars)</label><input id="st-desc" name="description" maxlength="140" required></div>
<div class="field"><label for="st-why">Why should our audience care?</label><textarea id="st-why" name="pitch"></textarea></div>
<div class="field"><label>Listing type</label><div class="choice-grid"><label class="choice"><input type="radio" name="listing" value="Free review (queue)" checked> Free review</label><label class="choice"><input type="radio" name="listing" value="Featured listing (paid, priority)"> Featured (priority)</label></div></div>
<div class="row"><div class="field"><label for="st-you">Your name</label><input id="st-you" name="name" required></div><div class="field"><label for="st-em">Email</label><input id="st-em" name="email" type="email" required></div></div>
<label class="check"><input type="checkbox" required name="owner" value="yes"> I own or represent this product and have the right to submit it.</label>
<button class="btn btn-primary btn-block mt" type="submit">Submit for review</button><div class="form-status" role="status"></div></form>
<div><div class="card"><h3>Review criteria</h3><ul><li>Genuinely useful to developers, IT, makers or marketers</li><li>Working product with a clear website and privacy policy</li><li>No malware, scams, piracy or adult content</li><li>Honest pricing information</li></ul></div>
<div class="card mt"><h3>Want it faster?</h3><p>Featured listings skip the queue, get a highlighted card and a newsletter mention.</p><a class="btn btn-accent" href="{root}advertise/">See featured options</a></div></div></div>'''
    write("directory/submit/", P("directory/submit/", title="Submit a Tool to the Tech.Tools Directory", desc="Submit your software, SaaS or developer tool to the Tech.Tools directory for free review or a featured listing.", body=body, active="directory/"), "0.5")

# ============================================================ BUSINESS PAGES
def build_business():
    # ---------- Get expert help (lead gen) ----------
    root = "../"
    services = [("code", "Websites & web apps", "Marketing sites, SaaS products, e-commerce and internal tools."),
                ("globe", "Cloud & DevOps", "Hosting, migrations, CI/CD, cost optimisation and uptime."),
                ("shield", "Cybersecurity", "Security reviews, hardening, password & access policies."),
                ("users", "IT support", "Managed IT, device setup, email, backups and helpdesk."),
                ("rocket", "AI automation", "Chatbots, document workflows and process automation."),
                ("grid", "Software selection", "Pick the right SaaS without overpaying or locking in."),
                ("search", "SEO & martech", "Technical SEO, analytics, tracking and site speed."),
                ("calc", "Data & dashboards", "Reporting, spreadsheets to databases, BI dashboards.")]
    svc = "\n".join(f'<div class="card"><span style="color:var(--primary)">{icon(i,24)}</span><h3 style="margin-top:8px">{n}</h3><p style="margin:0">{d}</p></div>' for i, n, d in services)
    faqs = [("Is the audit really free?", "Yes. The initial review and recommendations are free with no obligation. If you choose to work with a specialist, you'll get a clear quote before anything starts."),
            ("Who are the specialists?", "Independent developers, IT, cloud and security professionals we vet for experience, communication and references. You'll see their background before agreeing to anything."),
            ("How fast will I hear back?", "Within one business day, usually sooner."),
            ("What does it cost after the audit?", "It depends on scope. Many tasks are fixed-price; ongoing support is usually monthly. You approve every cost up front."),
            ("Will you share my details?", "Only with the specialist you're matched with, for the purpose of your request. We never sell data.")]
    body = f'''<section class="hero" style="padding-bottom:30px"><div class="container split" style="align-items:center">
  <div>{crumbs(root, [("Get expert help", "")])}<span class="eyebrow">{icon("rocket",14)} Free tech stack audit</span>
  <h1>Get the right expert for your tech project — <em>in 24 hours</em>.</h1>
  <p class="lead">Tell us what you need. We review your situation, recommend the best approach and match you with a vetted specialist. Free, no obligation.</p>
  <div class="trust"><span>Free consultation</span><span>Vetted specialists</span><span>Quote before you commit</span><span>Data never sold</span></div>
  <ol style="margin-top:22px;color:var(--ink-2)"><li><b>Tell us</b> about your project (2 minutes)</li><li><b>Get a plan</b> with recommendations and budget range</li><li><b>Meet your match</b> — only proceed if it's a fit</li></ol></div>
  <div class="card" style="box-shadow:var(--shadow-lg)">{lead_form("eh").replace("{ROOT}", root)}</div>
</div></section>
<section class="block alt"><div class="container"><div class="section-head"><div><h2>What we can help with</h2><p>From a single fix to a full build.</p></div></div><div class="grid g4">{svc}</div></div></section>
<section class="block"><div class="container split"><div><h2>Why teams ask us first</h2>
<ul class="prose"><li><b>Independent advice.</b> We recommend what fits, not what pays the highest commission.</li><li><b>Practitioners, not salespeople.</b> Specialists who do the work scope the work.</li><li><b>Clear scope.</b> Fixed quotes where possible, milestones where not.</li><li><b>Small or large.</b> Solo founders to 250+ person companies.</li></ul></div>
<div><h2>FAQ</h2>{faq_html(faqs)}</div></div></section>
<section class="block alt"><div class="container center"><h2>Are you a specialist?</h2><p class="muted">Join our vetted network and receive qualified project requests.</p><a class="btn btn-primary" href="{root}careers/#talent">Apply to the network</a></div></section>'''
    write("get-expert-help/", P("get-expert-help/", title="Get Expert Help — Free Tech Stack Audit & Vetted Specialists", desc="Free tech stack audit and matching with vetted developers, cloud, IT, security and AI automation specialists. Reply within 1 business day.",
                                body=body, active="get-expert-help/", schema=[faq_schema(faqs), {"@context": "https://schema.org", "@type": "Service", "name": "Tech stack audit & specialist matching", "provider": {"@type": "Organization", "name": "Tech.Tools"}, "areaServed": "Worldwide", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Free initial audit"}}]), "0.9")

    # ---------- Advertise ----------
    tiers = [("Directory Featured", "$49", "/ month", ["Pinned featured card in the directory", "Highlighted design + logo", "Skip the review queue", "Dofollow link after review"], False),
             ("Tool Sponsor", "$299", "/ month", ["“Presented by” on one tool page", "Sidebar card on that tool", "Mention in the tool's how-to", "Monthly impressions report"], True),
             ("Category Takeover", "$799", "/ month", ["Sponsor every tool in one category", "Logo on the category section", "Featured directory listing included", "Newsletter mention"], False),
             ("Sponsored Guide", "$999", "one-time", ["Original long-form guide on your topic", "Your product as a worked example", "Clearly labelled “Sponsored”", "Permanent placement"], False)]
    tcards = "\n".join(f'''<div class="card tier{" featured" if f else ""}"><h3>{n}</h3><div class="price">{p} <small>{u}</small></div><ul>{"\n".join(f"<li>{x}</li>" for x in li)}</ul><a class="btn {"btn-primary" if f else "btn-ghost"} btn-block" href="#adform">Request this package</a></div>''' for n, p, u, li, f in tiers)
    body = f'''<div class="container page-head">{crumbs(root, [("Advertise", "")])}<span class="eyebrow">{icon("mega",14)} Advertise &amp; sponsor</span><h1>Put your product where tech decisions happen.</h1>
<p class="lead">Tech.Tools visitors arrive with a task to finish — formatting data, debugging DNS, securing accounts, choosing software. Native sponsorships reach them at the moment of need, alongside content they trust.</p></div>
<section class="container"><div class="grid g4">{tcards}</div><p class="form-note">Launch pricing in USD. Custom packages, newsletter sponsorships and contest sponsorships available. All sponsored placements are clearly labelled and must comply with our <a href="{root}terms/">terms</a> and Google publisher policies.</p></section>
<section class="block"><div class="container split"><div><h2>Audience</h2><ul class="prose"><li>Software developers and DevOps engineers</li><li>IT administrators and support teams</li><li>Security-conscious professionals</li><li>Marketers, SEOs and site owners</li><li>Founders and makers building online businesses</li></ul>
<h2>What we don't accept</h2><p class="muted">Malware, crypto scams, gambling, adult content, misleading claims, or anything that would put our readers at risk.</p>
<div class="card mt"><h3>Interested in acquiring or partnering on this domain?</h3><p>For acquisition, large sponsorships or strategic partnerships:</p><a class="btn btn-ghost" href="{BROKER_URL}" target="_blank" rel="noopener">Contact via web.works →</a></div></div>
<form id="adform" class="card" data-tt-form="Advertising Inquiry" data-success="Thanks! We'll send our media kit and availability within 1 business day.">{hp()}
<h3>Request the media kit</h3>
<div class="row"><div class="field"><label for="ad-name">Name</label><input id="ad-name" name="name" required></div><div class="field"><label for="ad-email">Work email</label><input id="ad-email" name="email" type="email" required></div></div>
<div class="row"><div class="field"><label for="ad-co">Company</label><input id="ad-co" name="company" required></div><div class="field"><label for="ad-url">Website</label><input id="ad-url" name="website" type="url" placeholder="https://"></div></div>
<div class="field"><label for="ad-pkg">Package</label><select id="ad-pkg" name="package">{"\n".join(f"<option>{t[0]}</option>" for t in tiers)}<option>Newsletter sponsorship</option><option>Contest sponsorship</option><option>Custom / not sure</option></select></div>
<div class="field"><label for="ad-bud">Monthly budget</label><select id="ad-bud" name="budget"><option>Under $250</option><option>$250 – $1,000</option><option>$1,000 – $5,000</option><option>$5,000+</option></select></div>
<div class="field"><label for="ad-msg">Goals &amp; timing</label><textarea id="ad-msg" name="message"></textarea></div>
<button class="btn btn-primary btn-block" type="submit">Send inquiry</button><div class="form-status" role="status"></div></form></div></section>'''
    write("advertise/", P("advertise/", title="Advertise on Tech.Tools — Sponsorships & Featured Listings", desc="Sponsor a tool, feature your product in the directory or take over a category. Native ads reaching developers, IT buyers and marketers.", body=body, active="advertise/"), "0.7")

    # ---------- Partners ----------
    body = f'''<div class="container page-head">{crumbs(root, [("Partnerships", "")])}<h1>Partner with Tech.Tools</h1><p class="lead">We work with SaaS companies, agencies, educators, creators and communities to build useful things together.</p></div>
<div class="container split"><div class="grid" style="gap:12px">
{"\n".join(f'<div class="card"><h3>{a}</h3><p style="margin:0">{b}</p></div>' for a, b in [("Integration partners", "Turn your API into a free tool on Tech.Tools with “Powered by” attribution."), ("Agency & referral partners", "Receive qualified leads from our Get Expert Help program in your specialty and region."), ("Content & creator partners", "Have your tutorials featured in our guides and video library; co-create courses."), ("Affiliate partners", "List your product with transparent affiliate disclosure where it genuinely helps readers."), ("Communities & education", "Free tools and workshops for bootcamps, universities, meetups and non-profits.")])}
</div><form class="card" data-tt-form="Partnership Inquiry" data-success="Thanks! Our partnerships team will reply within 2 business days.">{hp()}<h3>Propose a partnership</h3>
<div class="row"><div class="field"><label for="pa-name">Name</label><input id="pa-name" name="name" required></div><div class="field"><label for="pa-em">Email</label><input id="pa-em" name="email" type="email" required></div></div>
<div class="row"><div class="field"><label for="pa-org">Organisation</label><input id="pa-org" name="organisation" required></div><div class="field"><label for="pa-type">Partnership type</label><select id="pa-type" name="type"><option>Integration</option><option>Agency / referral</option><option>Content / creator</option><option>Affiliate</option><option>Community / education</option><option>Domain / acquisition</option><option>Other</option></select></div></div>
<div class="field"><label for="pa-msg">Your idea</label><textarea id="pa-msg" name="message" required></textarea></div>
<button class="btn btn-primary btn-block" type="submit">Send proposal</button><div class="form-status" role="status"></div></form></div>'''
    write("partners/", P("partners/", title="Partnerships", desc="Partner with Tech.Tools: integrations, agency referrals, creator collaborations, affiliate and education partnerships.", body=body), "0.5")

    # ---------- Support / donate ----------
    funds = [("Operations & hosting", "Servers, domains, APIs, monitoring and security.", 40), ("New tools & features", "Paying developers to build and maintain tools.", 30),
             ("Promotion & marketing", "Reaching people who need free, private tools.", 15), ("Hiring talent", "Writers, video creators and moderators.", 10), ("Contests & prizes", "Rewarding builders in our community challenges.", 5)]
    fcards = "\n".join(f'<div><div style="display:flex;justify-content:space-between"><b>{n}</b><span class="muted">{p}%</span></div><div class="progress"><span style="width:{p}%"></span></div><p class="form-note" style="margin-top:0">{d}</p></div>' for n, d, p in funds)
    body = f'''<div class="container page-head">{crumbs(root, [("Support Us", "")])}<span class="eyebrow">{icon("heart",14)} Support Tech.Tools</span><h1>Help keep {len(TOOLS)} tools free for everyone.</h1>
<p class="lead">Tech.Tools has no paywalls and no sign-ups. Ads cover part of the cost; supporters like you fund the rest — and decide how fast we grow.</p></div>
<div class="container split">
<form class="card" id="donate" data-tt-form="Donation Pledge" data-success="Thank you for your support! We'll email you a secure payment link and a receipt within 1 business day.">{hp()}
<h3>Make a contribution</h3>
<div class="choice-grid" style="margin-bottom:12px"><label class="choice"><input type="radio" name="frequency" value="One-time" checked> One-time</label><label class="choice"><input type="radio" name="frequency" value="Monthly"> Monthly</label></div>
<div class="amounts" data-target="dn-amt"><button type="button" data-v="5">$5</button><button type="button" data-v="10">$10</button><button type="button" class="on" data-v="25">$25</button><button type="button" data-v="50">$50</button><button type="button" data-v="100">$100</button></div>
<div class="field"><label for="dn-amt">Amount (USD)</label><input id="dn-amt" name="amount" type="number" min="1" value="25" required></div>
<div class="field"><label for="dn-fund">Direct my support to</label><select id="dn-fund" name="fund"><option>Where it's needed most</option>{"\n".join(f"<option>{f[0]}</option>" for f in funds)}</select></div>
<div class="row"><div class="field"><label for="dn-name">Name</label><input id="dn-name" name="name" required></div><div class="field"><label for="dn-em">Email</label><input id="dn-em" name="email" type="email" required></div></div>
<div class="field"><label for="dn-msg">Message (optional)</label><input id="dn-msg" name="message"></div>
<label class="check"><input type="checkbox" name="public_credit" value="yes"> List my name on the supporters wall</label>
<div id="pay-links" class="toolbar"></div>
<button class="btn btn-accent btn-block mt" type="submit">{icon("heart",18)} Pledge my support</button>
<p class="form-note">We'll send a secure payment link by email. Contributions support an independent publication and are not tax-deductible.</p><div class="form-status" role="status"></div></form>
<div><div class="card"><h3>Where your money goes</h3>{fcards}</div>
<div class="card mt"><h3>Other ways to help</h3><ul><li>Share a tool you love with your team</li><li>Whitelist Tech.Tools in your ad-blocker</li><li><a href="{root}directory/submit/">Suggest a tool</a> or <a href="{root}contact/">report a bug</a></li><li><a href="{root}careers/">Contribute</a> as a writer or developer</li><li><a href="{root}advertise/">Sponsor</a> through your company</li></ul></div>
<div class="card mt"><h3>Corporate sponsorship</h3><p>Support at $500+/month and get logo placement on this page and in our footer.</p><a class="btn btn-ghost" href="{root}advertise/">Become a sponsor</a></div></div></div>
<div class="container mt"><h2>Supporters wall</h2><p class="muted">Be the first name here. Thank you to everyone who keeps the lights on.</p></div>'''
    pay_js = f'''<script src="{root}assets/js/config.js"></script><script>(function(){{var c=window.TT_CONFIG||{{}},b=document.getElementById("pay-links"),h="";[["stripe","Pay by card (Stripe)"],["paypal","PayPal"],["kofi","Ko-fi"],["buymeacoffee","Buy Me a Coffee"],["github","GitHub Sponsors"]].forEach(function(p){{if(c[p[0]])h+='<a class="btn btn-primary btn-sm" target="_blank" rel="noopener" href="'+c[p[0]]+'">'+p[1]+"</a>"}});if(h)b.innerHTML='<p class="form-note" style="width:100%;margin:0">Pay instantly:</p>'+h}})();</script>'''
    write("support/", P("support/", title="Support Tech.Tools — Donate to Keep Tools Free", desc="Support Tech.Tools with a one-time or monthly contribution. Funds hosting, new tools, promotion, hiring talent and community contests.", body=body, active="support/", scripts=pay_js), "0.6")

    # ---------- Contests ----------
    rules = ["Open to individuals aged 18+ (or the age of majority in their jurisdiction) where not prohibited by law. Void where prohibited.",
             "No purchase, payment or donation is necessary to enter or win.",
             "One entry per person per challenge. Entries must be your original work and must not infringe third-party rights.",
             "Tools must run client-side in a browser, collect no personal data without disclosure, and contain no malware or tracking.",
             "Judging criteria: usefulness (40%), quality & accessibility (30%), originality (20%), documentation (10%).",
             "Winners are notified by email and must respond within 14 days. Prizes are non-transferable; taxes are the winner's responsibility.",
             "By entering, you grant Tech.Tools a non-exclusive licence to showcase your entry with attribution. You keep ownership.",
             "Tech.Tools may modify, extend or cancel a challenge if circumstances require; any change will be posted on this page."]
    body = f'''<div class="container page-head">{crumbs(root, [("Contests", "")])}<span class="eyebrow">{icon("trophy",14)} Community challenges</span><h1>The Tech.Tools Build Challenge</h1>
<p class="lead">Build a small, genuinely useful browser-based tool. The best entries get published on Tech.Tools with full credit, plus prizes from our sponsors and supporters.</p></div>
<div class="container split"><div>
<div class="grid g3">{"\n".join(f'<div class="card center"><div style="font-size:2rem">{m}</div><h3>{p}</h3><p style="margin:0;font-size:.9rem">{d}</p></div>' for m, p, d in [("🥇", "1st place", "Published tool + homepage feature + top sponsor prize"), ("🥈", "2nd place", "Published tool + newsletter feature + sponsor prize"), ("🥉", "3rd place", "Published tool + featured directory listing")])}</div>
<p class="form-note">Cash and product prizes are announced as sponsors join each round. <a href="{root}advertise/">Sponsor a prize</a> to put your brand in front of every entrant.</p>
<h2 class="mt">Current theme: “Tools for everyday IT”</h2><p>Think of a task a developer, sysadmin or support agent does every week that's still annoying. Make it one click. Examples: an SPF record builder, a log-line timestamp extractor, a Markdown table generator.</p>
<h2>Official rules</h2><ol class="prose">{"\n".join(f"<li>{r}</li>" for r in rules)}</ol></div>
<form class="card" data-tt-form="Contest Entry" data-success="Entry received! We'll confirm by email. Good luck!">{hp()}<h3>Submit your entry</h3>
<div class="row"><div class="field"><label for="ce-name">Full name</label><input id="ce-name" name="name" required></div><div class="field"><label for="ce-em">Email</label><input id="ce-em" name="email" type="email" required></div></div>
<div class="field"><label for="ce-title">Tool name</label><input id="ce-title" name="tool_name" required></div>
<div class="row"><div class="field"><label for="ce-demo">Live demo URL</label><input id="ce-demo" name="demo_url" type="url" required placeholder="https://"></div><div class="field"><label for="ce-src">Source code URL</label><input id="ce-src" name="source_url" type="url" placeholder="https://github.com/…"></div></div>
<div class="field"><label for="ce-desc">What problem does it solve?</label><textarea id="ce-desc" name="description" required></textarea></div>
<label class="check"><input type="checkbox" name="age_ok" value="yes" required> I am 18+ (or the age of majority where I live) and eligible to enter.</label>
<label class="check"><input type="checkbox" name="rules_ok" value="yes" required> I agree to the official rules and confirm this is my original work.</label>
<button class="btn btn-accent btn-block mt" type="submit">Submit entry</button><div class="form-status" role="status"></div></form></div>'''
    write("contests/", P("contests/", title="Build Challenge — Contests & Prizes", desc="Enter the Tech.Tools Build Challenge: create a useful browser-based tool, get published and win sponsor prizes. Free to enter.", body=body), "0.6")

    # ---------- Careers / talent ----------
    roles = [("Technical writer (freelance)", "Write clear guides on developer, IT and security topics. Paid per article."),
             ("JavaScript tool developer (freelance)", "Build and maintain fast, accessible client-side tools. Paid per tool."),
             ("Video creator / editor", "Produce short tutorials and tool walkthroughs for YouTube and social."),
             ("Partnerships & ad sales (commission)", "Bring sponsors and partners on board; generous commission."),
             ("Community moderator", "Help run contests and review directory submissions."),
             ("Specialist network", "Developers, cloud, IT and security pros who want qualified client projects.")]
    body = f'''<div class="container page-head">{crumbs(root, [("Careers & talent", "")])}<h1>Work with Tech.Tools</h1><p class="lead">We're a remote-first, independent publication. We hire talented contributors on a flexible basis and connect specialists with clients who need them.</p></div>
<div class="container split"><div><h2>Open roles</h2><div class="grid" style="gap:12px">{"\n".join(f'<div class="card"><h3>{a}</h3><p style="margin:0">{b}</p></div>' for a, b in roles)}</div>
<div class="card mt"><h3>Need to hire?</h3><p>Looking for a developer, IT or security specialist for your own project?</p><a class="btn btn-primary" href="{root}get-expert-help/">Get matched with talent →</a></div></div>
<form id="talent" class="card" data-tt-form="Talent Application" data-success="Application received! We review every application and reply within 5 business days.">{hp()}<h3>Apply</h3>
<div class="row"><div class="field"><label for="ta-name">Full name</label><input id="ta-name" name="name" required></div><div class="field"><label for="ta-em">Email</label><input id="ta-em" name="email" type="email" required></div></div>
<div class="field"><label for="ta-role">Role</label><select id="ta-role" name="role">{"\n".join(f"<option>{r[0]}</option>" for r in roles)}</select></div>
<div class="row"><div class="field"><label for="ta-port">Portfolio / LinkedIn / GitHub</label><input id="ta-port" name="portfolio" type="url" required placeholder="https://"></div><div class="field"><label for="ta-loc">Location / time zone</label><input id="ta-loc" name="location"></div></div>
<div class="row"><div class="field"><label for="ta-exp">Years of experience</label><select id="ta-exp" name="experience"><option>0–1</option><option>2–4</option><option>5–9</option><option>10+</option></select></div><div class="field"><label for="ta-rate">Expected rate (USD)</label><input id="ta-rate" name="rate" placeholder="e.g. $40/hr or $150/article"></div></div>
<div class="field"><label for="ta-why">Tell us about your best relevant work</label><textarea id="ta-why" name="pitch" required></textarea></div>
<button class="btn btn-primary btn-block" type="submit">Submit application</button><div class="form-status" role="status"></div></form></div>'''
    write("careers/", P("careers/", title="Careers & Talent Network", desc="Freelance roles at Tech.Tools for writers, JavaScript developers, video creators and partnerships, plus our vetted specialist network.", body=body), "0.5")

# ============================================================ COMPANY + LEGAL
def legal_page(path, title, desc, inner, active=""):
    root = depth(path)
    body = f'''<div class="container page-head">{crumbs(root, [(title, "")])}<h1>{title}</h1><p class="muted">Last updated: {TODAY}</p></div><div class="container"><article class="prose">{inner.replace("{ROOT}", root)}</article></div>'''
    write(path, P(path, title=title, desc=desc, body=body, active=active), "0.3")

def build_company():
    root = "../"
    body = f'''<div class="container page-head">{crumbs(root, [("About", "")])}<h1>About Tech.Tools</h1><p class="lead">Fast, private, genuinely useful tools — and the knowledge to use them well.</p></div>
<div class="container"><article class="prose">
<p>Tech.Tools is an independent online publication that builds free browser-based utilities for developers, IT professionals, marketers and makers, and publishes practical guides on the technology behind them.</p>
<h2>Our principles</h2><ul><li><b>Private by design.</b> Tools run in your browser. We don't want your data, so we don't collect it.</li><li><b>Free and fast.</b> No accounts, no paywalls, no artificial limits. Pages are lightweight static files.</li><li><b>Accurate.</b> Tools follow published standards (RFCs, WCAG, ECMA), and guides are reviewed for correctness and updated when things change.</li><li><b>Transparent.</b> Ads and sponsorships are clearly labelled and never change our tool results or editorial recommendations.</li></ul>
<h2>Editorial policy</h2><p>Guides are written and reviewed by practitioners. Embedded videos are selected from established educators for clarity and accuracy; their creators retain all rights. Directory listings are chosen on merit — paid placements are labelled “Featured” or “Sponsored”. We correct errors promptly; <a href="{root}contact/">report one here</a>.</p>
<h2>How we're funded</h2><p>Display advertising (Google AdSense), clearly-labelled sponsorships, our Get Expert Help referral service, and voluntary <a href="{root}support/">reader support</a>.</p>
<h2>Get in touch</h2><p>Use our <a href="{root}contact/">contact form</a>. For domain acquisition, sponsorship or partnership: <a href="{BROKER_URL}" target="_blank" rel="noopener">web.works/contact</a>.</p></article></div>'''
    write("about/", P("about/", title="About Tech.Tools", desc="Tech.Tools is an independent publication building free, private, in-browser tech tools and practical guides.", body=body,
                      schema={"@context": "https://schema.org", "@type": "AboutPage", "name": "About Tech.Tools", "url": SITE + "/about/"}), "0.5")

    body = f'''<div class="container page-head">{crumbs(root, [("Contact", "")])}<h1>Contact us</h1><p class="lead">Questions, bug reports, tool requests or feedback — we read everything and reply within 1–2 business days.</p></div>
<div class="container split"><form class="card" data-tt-form="Contact" data-success="Message sent — thank you! We'll reply within 1–2 business days.">{hp()}
<div class="row"><div class="field"><label for="ct-name">Name</label><input id="ct-name" name="name" required autocomplete="name"></div><div class="field"><label for="ct-em">Email</label><input id="ct-em" name="email" type="email" required autocomplete="email"></div></div>
<div class="field"><label for="ct-topic">Topic</label><select id="ct-topic" name="topic"><option>General question</option><option>Bug report</option><option>Tool request</option><option>Get expert help</option><option>Advertising / sponsorship</option><option>Partnership</option><option>Domain acquisition</option><option>Press</option><option>Privacy / legal request</option></select></div>
<div class="field"><label for="ct-sub">Subject</label><input id="ct-sub" name="subject" required></div>
<div class="field"><label for="ct-msg">Message</label><textarea id="ct-msg" name="message" required minlength="10"></textarea></div>
<button class="btn btn-primary btn-block" type="submit">Send message</button><div class="form-status" role="status"></div></form>
<div><div class="card"><h3>Prefer email?</h3><p>Click below to open your email app with our address pre-filled.</p><a class="btn btn-ghost" href="#" data-mail data-subject="Tech.Tools enquiry">{icon("mail",18)} Email Tech.Tools</a></div>
<div class="card mt"><h3>Domain, sponsorship &amp; partnership</h3><p>Interested in this website, the domain name, sponsorship, advertising or partnership?</p><a class="btn btn-accent" href="{BROKER_URL}" target="_blank" rel="noopener">Contact via web.works →</a></div>
<div class="card mt"><h3>Need a project done?</h3><p>Get a free tech stack audit and a vetted specialist.</p><a class="btn btn-primary" href="{root}get-expert-help/">Get expert help</a></div></div></div>
<script>(function(){{var s=new URLSearchParams(location.search).get("subject");if(s)document.getElementById("ct-sub").value=s}})();</script>'''
    write("contact/", P("contact/", title="Contact Tech.Tools", desc="Contact Tech.Tools for questions, bug reports, tool requests, advertising, partnerships or domain enquiries.", body=body,
                        schema={"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Tech.Tools", "url": SITE + "/contact/"}), "0.5")

    legal_page("privacy/", "Privacy Policy", "How Tech.Tools handles data, cookies, advertising and form submissions.", f'''
<p>This Privacy Policy explains what information Tech.Tools (“we”, “us”) collects when you use https://tech.tools (the “Site”), how we use it, and your choices.</p>
<h2>1. Data processed by our tools</h2><p>Almost all tools run entirely in your web browser. Text, files, images and passwords you enter are processed on your device and are <b>not</b> sent to our servers. Exceptions: the <i>What Is My IP</i> tool requests your IP and approximate location from ipify.org and ipapi.co, and the <i>DNS Lookup</i> tool sends the domain you enter to Google Public DNS (dns.google). These requests go directly from your browser to those providers under their own privacy policies. We do not receive or store the results.</p>
<h2>2. Information you send us</h2><p>When you submit a form (contact, expert help, newsletter, donations, directory, contest or job application), we receive the information you enter. Forms are delivered to our private inbox via the FormSubmit service. We use this information only to respond to your request, provide the service you asked for, and — for expert-help requests — share it with the specialist you're matched with. We never sell personal information.</p>
<h2>3. Cookies and local storage</h2><p>We use your browser's local storage for preferences such as dark mode, recently used tools and cookie choices. See our <a href="{{ROOT}}cookies/">Cookie Policy</a>.</p>
<h2>4. Advertising — Google AdSense</h2><p>We use Google AdSense to display ads. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visits to this and/or other sites on the Internet. You may opt out of personalised advertising by visiting <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. Learn how Google uses information from sites that use its services at <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">policies.google.com/technologies/partner-sites</a>. Visitors in the EEA, UK and Switzerland are shown a consent message where required.</p>
<h2>5. Embedded content</h2><p>Guides embed YouTube videos in privacy-enhanced mode (youtube-nocookie.com). The video player loads only when you click play; YouTube's privacy policy then applies. Fonts are served by Google Fonts and some libraries by cdnjs (Cloudflare).</p>
<h2>6. Hosting and logs</h2><p>The Site is static and hosted on GitHub Pages. GitHub may log visitor IP addresses for security purposes under its own privacy statement.</p>
<h2>7. Retention</h2><p>Form submissions are kept only as long as needed to handle your request and meet legal obligations, typically no longer than 24 months.</p>
<h2>8. Your rights</h2><p>Depending on where you live (e.g. GDPR, UK GDPR, CCPA/CPRA, PIPEDA), you may have rights to access, correct, delete or object to processing of your personal data. Contact us through the <a href="{{ROOT}}contact/">contact form</a> choosing “Privacy / legal request”. We respond within 30 days.</p>
<h2>9. Children</h2><p>The Site is not directed to children under 13 (16 in the EEA), and we do not knowingly collect their personal information.</p>
<h2>10. Changes</h2><p>We may update this policy; the “last updated” date above shows the latest revision.</p>''')

    legal_page("terms/", "Terms of Use", "Terms governing use of the Tech.Tools website, tools, content and services.", '''
<p>By accessing or using Tech.Tools (the “Site”), you agree to these Terms. If you do not agree, please do not use the Site.</p>
<h2>1. Use of tools</h2><p>Tools are provided free of charge for lawful personal and commercial use. You are responsible for verifying results before relying on them. You may not use the Site to break the law, attack systems you don't own or have permission to test, distribute malware, or infringe others' rights.</p>
<h2>2. No warranty</h2><p>The Site and all tools are provided “as is” and “as available”, without warranties of any kind, express or implied, including merchantability, fitness for a particular purpose and non-infringement. Results (for example password strength estimates, DNS answers or conversions) may be incomplete or inaccurate.</p>
<h2>3. Limitation of liability</h2><p>To the maximum extent permitted by law, Tech.Tools and its owners will not be liable for any indirect, incidental, special, consequential or punitive damages, or any loss of data, profits or revenue, arising from your use of the Site.</p>
<h2>4. Intellectual property</h2><p>Site design, code, text and original graphics are © Tech.Tools. You may link to any page and quote short excerpts with attribution. Third-party trademarks, videos and content belong to their owners. See our <a href="{ROOT}legal/">Trademark &amp; Copyright notice</a>.</p>
<h2>5. User submissions</h2><p>When you submit content (contest entries, directory listings, feedback), you confirm you have the right to do so and grant us a non-exclusive, worldwide, royalty-free licence to display it on the Site with attribution. You retain ownership.</p>
<h2>6. Expert help service</h2><p>Tech.Tools introduces you to independent specialists. Any engagement is a contract between you and the specialist. We are not party to it and are not responsible for their work, although we vet specialists and welcome feedback.</p>
<h2>7. Advertising and sponsorships</h2><p>Paid placements are labelled. Advertisers are responsible for their content. We may refuse or remove any ad or listing at our discretion.</p>
<h2>8. Donations</h2><p>Contributions are voluntary support for an independent publication, are generally non-refundable, and are not tax-deductible charitable donations.</p>
<h2>9. Contests</h2><p>Each challenge is governed by its official rules on the Contests page, which prevail over these Terms for that challenge.</p>
<h2>10. External links</h2><p>We are not responsible for the content or practices of third-party websites linked from the Site.</p>
<h2>11. Changes and governing law</h2><p>We may update these Terms at any time; continued use means acceptance. These Terms are governed by the laws applicable in the owner's place of business, without regard to conflict-of-law rules.</p>''')

    legal_page("cookies/", "Cookie Policy", "Which cookies and local storage Tech.Tools and its advertising partners use.", '''
<p>Cookies are small files stored by your browser. Local storage is a similar browser feature. Here's how Tech.Tools uses them.</p>
<table><tr><th>Name / type</th><th>Set by</th><th>Purpose</th><th>Duration</th></tr>
<tr><td>tt-theme (local storage)</td><td>Tech.Tools</td><td>Remembers light/dark mode</td><td>Until cleared</td></tr>
<tr><td>tt-recent (local storage)</td><td>Tech.Tools</td><td>Shows your recently used tools on this device</td><td>Until cleared</td></tr>
<tr><td>tt-cookie (local storage)</td><td>Tech.Tools</td><td>Remembers your cookie notice choice</td><td>Until cleared</td></tr>
<tr><td>Advertising cookies</td><td>Google and partners</td><td>Serve and measure ads, limit repetition, personalise where permitted</td><td>Varies, up to 13 months</td></tr>
<tr><td>YouTube cookies</td><td>Google</td><td>Only after you click play on an embedded video</td><td>Varies</td></tr></table>
<h2>Managing cookies</h2><p>You can block or delete cookies in your browser settings, and opt out of personalised ads at <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>. Blocking cookies does not stop the tools from working.</p>''')

    legal_page("disclaimer/", "Disclaimer", "Disclaimer for tools, guides, directory listings, affiliate links and advertising on Tech.Tools.", '''
<p><b>General information only.</b> Content and tools on Tech.Tools are provided for general informational and educational purposes. They are not professional, legal, financial or security advice. Always verify critical results and consult a qualified professional for your specific situation.</p>
<p><b>Security tools.</b> Password strength scores and crack-time figures are estimates based on common attack models. No tool can guarantee that a password or system is secure.</p>
<p><b>Third-party data.</b> IP geolocation and DNS answers come from third-party services and may be inaccurate or cached.</p>
<p><b>Directory and links.</b> Listing a product does not constitute an endorsement, and we are not responsible for third-party products, services or websites. Some links may be sponsored or affiliate links; these are disclosed where applicable and may earn us a commission at no extra cost to you.</p>
<p><b>Advertising.</b> Ads are served by Google AdSense and sponsors. We do not control the content of third-party ads; report inappropriate ads via the “AdChoices” link on the ad.</p>
<p><b>Videos.</b> Embedded videos are the property of their creators and are shown via YouTube's official embed player. Views expressed in them are the creators' own.</p>''')

    legal_page("legal/", "Trademark & Copyright Notice", "Trademark and copyright disclosure for Tech.Tools, including non-affiliation with similarly named companies.", f'''
<h2>Independence and non-affiliation</h2><p>Tech.Tools is an independent website operated under the domain name <b>tech.tools</b>. The name describes the site's subject matter — technology tools — and is used in a generic, descriptive sense. Tech.Tools is <b>not affiliated with, endorsed by, sponsored by or connected to</b> any company, product, store, brand or registered trademark named “TechTools”, “Tech Tools”, “Tech-Tools” or any similar mark, in any country. No such association should be inferred.</p>
<p>If you believe any content on this site infringes your trademark, please contact us via the <a href="{{ROOT}}contact/">contact form</a> (topic: “Privacy / legal request”) and we will review it promptly.</p>
<h2>Third-party trademarks</h2><p>Names such as GitHub, Google, YouTube, Cloudflare, Figma, Visual Studio Code, AWS and others mentioned on this site are trademarks or registered trademarks of their respective owners. They are used for identification and descriptive purposes only (nominative fair use) and do not imply endorsement.</p>
<h2>Copyright</h2><p>© {datetime.date.today().year} Tech.Tools. All rights reserved. The original text of guides and tool descriptions, the site design, logo, source code and graphics are owned by Tech.Tools and protected by copyright law. You may link to any page and quote brief excerpts with attribution and a link back. Republishing substantial portions without written permission is prohibited.</p>
<h2>Third-party content</h2><ul><li><b>Videos</b> are embedded via YouTube's official player; copyright remains with each creator.</li><li><b>Open-source libraries</b> loaded on some tools (js-yaml, qrcodejs) are used under their respective open-source licences (MIT).</li><li><b>Fonts</b> (Inter, Space Grotesk, JetBrains Mono) are served by Google Fonts under the SIL Open Font License.</li></ul>
<h2>Copyright complaints (DMCA)</h2><p>If you believe material on the Site infringes your copyright, send a notice through the <a href="{{ROOT}}contact/">contact form</a> including: identification of the work, the URL of the material, your contact details, a good-faith statement, a statement under penalty of perjury that you are authorised to act, and your signature. We will respond promptly and remove infringing material where appropriate.</p>''')

    legal_page("accessibility/", "Accessibility Statement", "Tech.Tools accessibility commitment and how to report barriers.", '''
<p>We want every tool to be usable by everyone. Tech.Tools aims to conform to the Web Content Accessibility Guidelines (WCAG) 2.2 level AA.</p>
<h2>What we do</h2><ul><li>Semantic HTML with labelled form fields and skip links</li><li>Keyboard-accessible controls with visible focus states (press Ctrl/⌘ + K to search)</li><li>Colour contrast checked with our own <a href="{ROOT}tools/contrast-checker/">contrast checker</a></li><li>Light and dark themes that respect your system preference</li><li>Responsive layouts that work at 320 px wide and 400% zoom</li></ul>
<h2>Known limitations</h2><p>Some visual tools (gradient and shadow generators) are inherently visual; their output is always provided as copyable text too. Third-party ads and embedded videos may not meet the same standard.</p>
<h2>Feedback</h2><p>Found a barrier? Tell us via the <a href="{ROOT}contact/">contact form</a> and we'll aim to fix it within 10 business days.</p>''')

    # HTML sitemap
    root = "../"
    groups = [("Tools", [(t["name"], f"tools/{t['id']}/") for t in TOOLS]), ("Guides", [(g["title"], f"guides/{g['slug']}/") for g in GUIDES]),
              ("Business", [("Get expert help", "get-expert-help/"), ("Advertise", "advertise/"), ("Partnerships", "partners/"), ("Support us", "support/"), ("Contests", "contests/"), ("Careers", "careers/"), ("Directory", "directory/"), ("Submit a tool", "directory/submit/"), ("Videos", "videos/")]),
              ("Company", [("About", "about/"), ("Contact", "contact/"), ("Privacy", "privacy/"), ("Terms", "terms/"), ("Cookies", "cookies/"), ("Disclaimer", "disclaimer/"), ("Trademark & Copyright", "legal/"), ("Accessibility", "accessibility/")])]
    body = f'<div class="container page-head">{crumbs(root, [("Sitemap", "")])}<h1>Sitemap</h1></div><div class="container grid g4">' + "\n".join(
        f'<div><h2 style="font-size:1.2rem">{n}</h2><ul>' + "\n".join(f'<li><a href="{root}{u}">{esc(t)}</a></li>' for t, u in items) + "</ul></div>" for n, items in groups) + "</div>"
    write("sitemap/", P("sitemap/", title="Sitemap", desc="Every page on Tech.Tools: tools, guides, business and company pages.", body=body), "0.3")

    # 404 — base tag computed so relative links work on both github.io/tech-tools/ and the custom domain
    body = f'''<section class="hero"><div class="container center"><h1>404 — tool not found</h1><p class="lead" style="margin:0 auto">That page doesn't exist (yet). Try searching, or head back to all tools.</p>
<div class="toolbar" style="justify-content:center;margin-top:20px"><a class="btn btn-primary" href="tools/">Browse all tools</a><button class="btn btn-ghost" data-search-open>Search</button><a class="btn btn-ghost" href="contact/">Request this tool</a></div></div></section>'''
    html = page(path="404.html", title="Page not found", desc="The page you requested could not be found.", body=body, root="", cats=CATS, noindex=True)
    html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<script>document.write(\'<base href="\'+(location.hostname.slice(-10)==="github.io"?"/"+location.pathname.split("/")[1]+"/":"/")+\'">\')</script>', 1)
    write("404.html", html)

# ============================================================ STATIC EXTRAS
def build_extras():
    os.makedirs(os.path.join(OUT, "assets/img"), exist_ok=True)
    idx = [{"t": t["name"], "u": f"tools/{t['id']}/", "c": CATBY[t["cat"]]["name"], "k": t["short"] + " " + t["id"].replace("-", " "), "p": t["popular"]} for t in TOOLS]
    idx += [{"t": g["title"].split(":")[0], "u": f"guides/{g['slug']}/", "c": "Guide", "k": g["desc"], "p": False} for g in GUIDES]
    idx += [{"t": n, "u": u, "c": "Page", "k": k, "p": False} for n, u, k in [("Get expert help", "get-expert-help/", "hire consultant audit developer agency"), ("Advertise", "advertise/", "sponsor ads media kit"), ("Support us", "support/", "donate donation contribute"), ("Software directory", "directory/", "apps saas software list"), ("Contests", "contests/", "prize challenge win"), ("Careers", "careers/", "jobs hiring talent work"), ("Contact", "contact/", "email message help")]]
    with open(os.path.join(OUT, "assets/js/search-index.js"), "w") as f:
        f.write("window.TT_INDEX=" + json.dumps(idx, ensure_ascii=False, indent=0) + ";\n")

    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u, p in URLS:
            f.write(f"  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /scripts/\nDisallow: /docs/\n\nSitemap: {SITE}/sitemap.xml\n")
    with open(os.path.join(OUT, "ads.txt"), "w") as f:
        f.write("google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
    with open(os.path.join(OUT, "manifest.webmanifest"), "w") as f:
        json.dump({"name": "Tech.Tools", "short_name": "Tech.Tools", "start_url": "./", "display": "standalone", "background_color": "#0c1222", "theme_color": "#0c1222",
                   "icons": [{"src": "assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, f, indent=1)
    with open(os.path.join(OUT, "assets/img/favicon.svg"), "w") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0c1222"/><g fill="none" stroke="#fbbf24" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" transform="translate(8 8) scale(2)"><path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8-1.3-1.3a4 4 0 0 0-5-5"/><path d="M3 21l6-6"/></g></svg>')
    cfg = os.path.join(OUT, "assets/js/config.js")
    if not os.path.exists(cfg):
        with open(cfg, "w") as f:
            f.write("""/* Payment links for the Support page. Paste your hosted payment URLs (never an email address) and the buttons appear automatically.
   e.g. stripe: "https://buy.stripe.com/xxxx", kofi: "https://ko-fi.com/yourname" */
window.TT_CONFIG = { stripe: "", paypal: "", kofi: "", buymeacoffee: "", github: "" };
""")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    build_og()

def build_og():
    """1200x630 social share image (needs Pillow; skipped silently if unavailable)."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    W, H = 1200, 630
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):  # diagonal-ish gradient
        t = y / H; d.line([(0, y), (W, y)], fill=(int(12 + 0 * t), int(18 + 50 * t), int(34 + 82 * t)))
    for x in range(0, W, 48): d.line([(x, 0), (x, H)], fill=(30, 45, 75))
    for y in range(0, H, 48): d.line([(0, y), (W, y)], fill=(30, 45, 75))
    def font(sz, bold=True):
        for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
            if os.path.exists(p): return ImageFont.truetype(p, sz)
        return ImageFont.load_default()
    f1 = font(110); x = 90
    for part, col in [("Tech", (255, 255, 255)), (".", (251, 191, 36)), ("Tools", (255, 255, 255))]:
        d.text((x, 190), part, font=f1, fill=col); x += d.textlength(part, font=f1)
    d.text((92, 345), f"{len(TOOLS)} free, private, in-browser tech tools", font=font(40, False), fill=(207, 224, 247))
    d.text((92, 420), "JSON · DNS · Regex · Passwords · QR · Images · SEO", font=font(30, False), fill=(125, 211, 252))
    img.save(os.path.join(OUT, "assets/img/og.png"), optimize=True)

if __name__ == "__main__":
    build_home(); build_tools(); build_guides(); build_directory(); build_business(); build_company(); build_extras()
    print(f"Built {len(URLS)} indexed pages + 404 into {OUT}")
