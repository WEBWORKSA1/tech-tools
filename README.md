# Tech.Tools

Free, private, in-browser tech tools for developers, IT pros, marketers and makers — plus guides, a video library, a curated software directory and a "Get Expert Help" service.

**Live:** https://tech.tools (GitHub Pages)

## What's inside
- 38 working client-side tools (`/tools/`), each with how-to, explainer and FAQ
- 10 long-form guides with embedded videos (`/guides/`, `/videos/`)
- Software directory + submission flow (`/directory/`)
- Lead generation (`/get-expert-help/`), advertising (`/advertise/`), partnerships, donations (`/support/`), contests, careers
- Full legal set: privacy, terms, cookies, disclaimer, accessibility, trademark & copyright
- `sitemap.xml`, `robots.txt`, `ads.txt`, structured data on every page

## Editing
All pages are generated. Edit the data/templates in `scripts/` and run:

```bash
python3 scripts/build.py
```

- Tools content: `scripts/tools_data.py` · tool logic: `assets/js/tools.js`
- Guides: `scripts/guides_data.py` · Directory: `scripts/directory_data.py`
- Shell/header/footer: `scripts/layout.py` · Styles: `assets/css/style.css`
- Donation payment buttons: paste hosted payment links into `assets/js/config.js`

## Hosting (GitHub Pages, free)
The built site is committed at the repository root, so GitHub Pages serves it straight from `main` — no Actions needed.

One-time setup: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `(root)` → Save.** The site appears at `https://webworksa1.github.io/tech-tools/`.

Custom domain: under Settings → Pages enter `tech.tools` (GitHub adds a `CNAME` file), point DNS A records for the apex to 185.199.108.153, 185.199.109.153, 185.199.110.153 and 185.199.111.153, add a `www` CNAME to `webworksa1.github.io`, then tick **Enforce HTTPS**.

After editing anything in `scripts/` or `assets/`, run `python3 scripts/build.py` and commit the regenerated files.

## Strategy
See `docs/BUILD-PROMPT.md` (business case + phase-wise build prompt) and `docs/RESEARCH.md` (competitive research).

## Legal
© Tech.Tools. All rights reserved. Not affiliated with any company named "TechTools", "Tech Tools" or similar. Third-party trademarks belong to their owners. See `/legal/`.
