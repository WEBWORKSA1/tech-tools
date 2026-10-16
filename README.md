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

## Hosting
GitHub Pages → Settings → Pages → Deploy from branch `main`, folder `/ (root)`. For the custom domain add `tech.tools` under Custom domain and point DNS A records to 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153.

## Strategy
See `docs/BUILD-PROMPT.md` (business case + phase-wise build prompt) and `docs/RESEARCH.md` (competitive research).

## Legal
© Tech.Tools. All rights reserved. Not affiliated with any company named "TechTools", "Tech Tools" or similar. Third-party trademarks belong to their owners. See `/legal/`.
