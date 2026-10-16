"""Shared page shell for Tech.Tools static build."""
import json, html

SITE = "https://tech.tools"
BRAND = "Tech.Tools"
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
BROKER_URL = "https://web.works/contact"

ICONS = {
  "code": '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
  "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
  "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 4 10 15 15 0 0 1-4 10 15 15 0 0 1-4-10 15 15 0 0 1 4-10z"/>',
  "text": '<path d="M4 7V4h16v3M9 20h6M12 4v16"/>',
  "palette": '<circle cx="13.5" cy="6.5" r="1.5"/><circle cx="17.5" cy="10.5" r="1.5"/><circle cx="8.5" cy="7.5" r="1.5"/><circle cx="6.5" cy="12.5" r="1.5"/><path d="M12 2a10 10 0 0 0 0 20c1 0 2-.8 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.3 0-1.1.9-2 2-2h2.4A5.6 5.6 0 0 0 22 10c0-4.4-4.5-8-10-8z"/>',
  "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/>',
  "calc": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/>',
  "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
  "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
  "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V2H6.5A2.5 2.5 0 0 0 4 4.5v15z"/><path d="M20 17v5H6.5a2.5 2.5 0 0 1 0-5"/>',
  "play": '<circle cx="12" cy="12" r="10"/><path d="m10 8 6 4-6 4z"/>',
  "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="M12 15l-3-3a22 22 0 0 1 2-4A13 13 0 0 1 22 2c0 2.7-.8 7.5-6 11a22 22 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
  "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
  "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6M18 9h1.5a2.5 2.5 0 0 0 0-5H18M4 22h16M10 14.7V17c0 .6-.5 1-1 1.2C7.9 18.8 7 20.2 7 22M14 14.7V17c0 .6.5 1 1 1.2 1.2.6 2 2 2 3.8M18 2H6v7a6 6 0 0 0 12 0V2z"/>',
  "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
  "mega": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
  "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
}

def icon(name, size=20):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

NAV = [
    ("tools/", "Tools"),
    ("directory/", "Directory"),
    ("guides/", "Guides"),
    ("videos/", "Videos"),
    ("advertise/", "Advertise"),
    ("support/", "Support"),
]

def esc(s):
    return html.escape(s, quote=True)

def header(root, active):
    links = "".join(
        f'<li><a href="{root}{href}"{" aria-current=\"page\"" if active == href else ""}>{label}</a></li>'
        for href, label in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="topbar" role="note"><a href="{BROKER_URL}" target="_blank" rel="noopener">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership</a></div>
<header class="site-header">
  <nav class="container nav" aria-label="Primary">
    <a class="logo" href="{root}" aria-label="{BRAND} home"><span class="logo-mark">{logo_svg()}</span><span>Tech<span class="dot">.</span>Tools</span></a>
    <ul class="nav-links">{links}<li><a href="{root}get-expert-help/"{" aria-current=\"page\"" if active == "get-expert-help/" else ""}>Get Expert Help</a></li></ul>
    <div class="nav-actions">
      <button class="search-trigger" data-search-open aria-label="Search tools">{icon("search",16)}<span>Search tools…</span><kbd>Ctrl K</kbd></button>
      <button class="icon-btn" data-theme-toggle aria-label="Toggle dark mode">{icon("sun",18)}</button>
      <a class="btn btn-primary btn-cta" href="{root}get-expert-help/">Free Tech Audit</a>
      <button class="icon-btn menu-btn" aria-label="Open menu" aria-expanded="false">{icon("menu",18)}</button>
    </div>
  </nav>
</header>'''

def logo_svg():
    return ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" stroke-width="2.4" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 '
            '8-8-1.3-1.3a4 4 0 0 0-5-5"/><path d="M3 21l6-6"/></svg>')

def footer(root, cats):
    catlinks = "".join(f'<li><a href="{root}tools/#{c["id"]}">{c["name"]}</a></li>' for c in cats[:6])
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div>
        <a class="logo" href="{root}"><span class="logo-mark">{logo_svg()}</span><span>Tech<span class="dot">.</span>Tools</span></a>
        <p class="muted" style="margin-top:12px">Free, fast, privacy-first tech utilities that run in your browser — plus guides, videos and a curated directory of the software that powers modern teams.</p>
        <form class="newsletter" data-tt-form="Newsletter" data-success="You're on the list. Watch your inbox for the next Tech.Tools digest.">
          <input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
          <input type="hidden" name="form" value="newsletter">
          <label class="hp" for="nl-email">Email</label>
          <input id="nl-email" type="email" name="email" placeholder="you@company.com" required aria-label="Email address">
          <button class="btn btn-primary btn-sm" type="submit">Subscribe</button>
          <div class="form-status" role="status"></div>
        </form>
      </div>
      <div><h4>Tools</h4><ul>{catlinks}<li><a href="{root}tools/">All tools →</a></li></ul></div>
      <div><h4>Resources</h4><ul>
        <li><a href="{root}guides/">Guides</a></li><li><a href="{root}videos/">Video library</a></li>
        <li><a href="{root}directory/">Software directory</a></li><li><a href="{root}directory/submit/">Submit a tool</a></li>
        <li><a href="{root}contests/">Contests &amp; prizes</a></li><li><a href="{root}sitemap/">Sitemap</a></li></ul></div>
      <div><h4>Business</h4><ul>
        <li><a href="{root}get-expert-help/">Get expert help</a></li><li><a href="{root}advertise/">Advertise &amp; sponsor</a></li>
        <li><a href="{root}partners/">Partnerships</a></li><li><a href="{root}careers/">Careers &amp; talent</a></li>
        <li><a href="{root}support/">Support / donate</a></li><li><a href="{BROKER_URL}" target="_blank" rel="noopener">Acquire this domain</a></li></ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="{root}about/">About</a></li><li><a href="{root}contact/">Contact</a></li>
        <li><a href="{root}privacy/">Privacy Policy</a></li><li><a href="{root}terms/">Terms of Use</a></li>
        <li><a href="{root}cookies/">Cookie Policy</a></li><li><a href="{root}disclaimer/">Disclaimer</a></li>
        <li><a href="{root}legal/">Trademark &amp; Copyright</a></li><li><a href="{root}accessibility/">Accessibility</a></li></ul></div>
    </div>
    <div class="foot-bottom">
      <span>© <span data-year>2026</span> {BRAND}. Original content and code © {BRAND}. All rights reserved.</span>
      <span>{BRAND} is an independent publication and is not affiliated with any company named “TechTools”, “Tech Tools” or similar. Third-party names and logos are trademarks of their respective owners. <a href="{root}legal/">Full disclosure</a>.</span>
    </div>
  </div>
</footer>
<div class="search-modal" role="dialog" aria-modal="true" aria-label="Search">
  <div class="search-box"><input type="search" placeholder="Search tools and guides…" aria-label="Search"><div class="search-results"></div></div>
</div>
<div class="cookie" role="dialog" aria-label="Cookie notice">
  <strong>Cookies &amp; ads</strong>
  <p style="margin:.4em 0 0">We use cookies for essential features, analytics and to serve ads (Google AdSense), which keep every tool free. See our <a href="{root}cookies/">Cookie Policy</a> and <a href="{root}privacy/">Privacy Policy</a>.</p>
  <div class="btns"><button class="btn btn-primary btn-sm" data-cookie="all">Accept</button><button class="btn btn-ghost btn-sm" data-cookie="essential">Essential only</button></div>
</div>
<div class="sticky-cta"><a class="btn btn-accent" href="{root}get-expert-help/">{icon("rocket",18)} Get a free tech stack audit</a> <button class="icon-btn" data-cta-close aria-label="Dismiss" style="display:inline-grid;vertical-align:middle;width:32px;height:32px">×</button></div>'''

def page(*, path, title, desc, body, root, cats, active="", schema=None, extra_head="", scripts="", og_type="website", noindex=False):
    canonical = f"{SITE}/{path}"
    full_title = title if BRAND in title else f"{title} | {BRAND}"
    ld = ""
    if schema:
        for s in (schema if isinstance(schema, list) else [schema]):
            ld += f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f'''<!doctype html>
<html lang="en" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
{ADSENSE}
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0c1222">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{root}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
{ld}{extra_head}
</head>
<body>
{header(root, active)}
<main id="main">
{body}
</main>
{footer(root, cats)}
<script src="{root}assets/js/search-index.js"></script>
<script src="{root}assets/js/main.js"></script>
{scripts}
</body>
</html>
'''

def sponsor_card(root):
    return f'''<aside class="sponsor-card"><small>Sponsored slot available</small>
<strong>Put your product in front of developers &amp; IT buyers</strong>
<p class="muted" style="font-size:.88rem;margin:.4em 0 .8em">Native placements on high-intent tool pages.</p>
<a class="btn btn-ghost btn-sm" href="{root}advertise/">See sponsorship options</a></aside>'''

def lead_card(root, context="your stack"):
    return f'''<aside class="card" style="border-color:var(--primary)">
<span class="badge blue">Free · 24h reply</span>
<h3 style="margin-top:10px">Need this done for {esc(context)}?</h3>
<p>Get matched with a vetted developer, IT or SaaS specialist. Free consultation, no obligation.</p>
<a class="btn btn-primary btn-block" href="{root}get-expert-help/">Get expert help →</a></aside>'''

def video(vid, title):
    return f'<div class="video"><button class="video-lite" data-id="{vid}" aria-label="Play video: {esc(title)}"></button></div>'

def hp():
    return '<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">'
