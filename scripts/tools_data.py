"""Tool catalogue + original SEO content for each tool page."""

CATS = [
    {"id": "developer", "name": "Developer", "icon": "code", "blurb": "Format, encode, decode, convert and debug — the daily toolkit for engineers."},
    {"id": "security", "name": "Security", "icon": "shield", "blurb": "Generate and audit passwords, hashes and QR codes without uploading a byte."},
    {"id": "network", "name": "Network & IT", "icon": "globe", "blurb": "IP, DNS, subnets, user agents and HTTP — diagnostics for sysadmins and support teams."},
    {"id": "seo", "name": "Web & SEO", "icon": "search", "blurb": "Meta tags, robots.txt and campaign links for marketers and site owners."},
    {"id": "text", "name": "Text & Writing", "icon": "text", "blurb": "Count, clean, sort and generate text for docs, posts and data entry."},
    {"id": "design", "name": "Design & Images", "icon": "palette", "blurb": "Colors, contrast, gradients, shadows and on-device image compression."},
    {"id": "calculators", "name": "Calculators", "icon": "calc", "blurb": "Data sizes, download times and aspect ratios worked out instantly."},
]

def T(id, name, cat, short, title, desc, about, steps, faqs, popular=False, related=None):
    return dict(id=id, name=name, cat=cat, short=short, title=title, desc=desc, about=about,
                steps=steps, faqs=faqs, popular=popular, related=related or [])

TOOLS = [
# ---------------- DEVELOPER ----------------
T("json-formatter", "JSON Formatter & Validator", "developer",
  "Beautify, minify, sort and validate JSON with exact error positions.",
  "JSON Formatter & Validator — Beautify, Minify, Sort Keys",
  "Free online JSON formatter and validator. Beautify or minify JSON, sort keys, and find syntax errors by line and column. Runs entirely in your browser.",
  """<p>JSON (JavaScript Object Notation) is the default data format of the modern web: REST APIs return it, configuration files are written in it, and logs are increasingly structured as it. Because machines usually emit JSON on a single line, it is almost unreadable to humans. A formatter re-indents the data so you can see the hierarchy of objects and arrays at a glance.</p>
<p>This tool parses your input with the browser's native <code>JSON.parse</code>, which follows the ECMA-404 / RFC 8259 grammar strictly. That means it will flag the mistakes that most often break production systems: trailing commas, single-quoted strings, unquoted keys, comments and stray control characters. When parsing fails we translate the engine's character offset into a line and column so you can jump straight to the problem.</p>
<h3>Format vs. minify vs. sort</h3>
<ul><li><b>Format</b> adds indentation (2 spaces, 4 spaces or tabs) for reading and code review.</li>
<li><b>Minify</b> strips all optional whitespace — useful before embedding JSON in a URL, a header or a fixture where size matters.</li>
<li><b>Sort keys</b> orders object keys alphabetically at every level, which makes two JSON documents far easier to diff.</li></ul>
<div class="callout">Privacy: your JSON never leaves this page. That matters when you are pasting API responses that contain tokens, emails or customer data.</div>""",
  ["Paste JSON into the input box (or click <b>Sample</b>).", "Choose an indent size.", "Click <b>Format</b>, <b>Minify</b> or <b>Sort keys</b>.", "If the JSON is invalid, read the error line/column and fix it.", "Copy the result or download it as a .json file."],
  [("Why does my JSON say 'Unexpected token'?", "Usually a trailing comma after the last item, a single-quoted string, or a comment. Strict JSON allows none of these."),
   ("Is there a size limit?", "No server limit — the practical limit is your device's memory. Multi-megabyte files format in well under a second on a modern laptop."),
   ("Does formatting change my data?", "No. Formatting only changes whitespace. Sorting keys changes key order, which JSON treats as insignificant."),
   ("Can it validate JSON Schema?", "This tool validates syntax only. Schema validation checks structure against rules and is on our roadmap.")],
  popular=True, related=["yaml-json", "json-to-csv", "diff-checker", "jwt-decoder"]),

T("base64", "Base64 Encode / Decode", "developer",
  "Encode text or files to Base64 and decode back — UTF-8 and URL-safe.",
  "Base64 Encoder & Decoder — Text, Files, URL-Safe",
  "Encode or decode Base64 online with full UTF-8 support, URL-safe mode and file-to-data-URI conversion. Private, in-browser and free.",
  """<p>Base64 turns arbitrary bytes into a 64-character alphabet (A–Z, a–z, 0–9, + and /) so binary data can travel through systems that only handle text: email bodies, JSON payloads, HTML attributes and HTTP headers. Every 3 bytes of input become 4 characters of output, so encoded data is roughly 33% larger.</p>
<p>A common bug is encoding non-English text with the browser's raw <code>btoa()</code>, which throws on characters like “é” or “日本”. This tool converts text to UTF-8 bytes first, so emoji and accented characters round-trip correctly.</p>
<h3>Standard vs. URL-safe Base64</h3>
<p>The <code>+</code> and <code>/</code> characters have special meanings in URLs, so RFC 4648 defines a URL-safe variant that uses <code>-</code> and <code>_</code> and usually drops the <code>=</code> padding. JWTs use this variant. Tick <b>URL-safe</b> when encoding for query strings or tokens; the decoder accepts both forms automatically.</p>
<div class="callout">Base64 is an encoding, not encryption. Anyone can decode it — never use it to hide passwords or secrets.</div>""",
  ["Type or paste text into the input.", "Click <b>Encode</b> (tick URL-safe if needed) or <b>Decode</b>.", "To embed a file, choose it under “encode a file” to get a data URI.", "Copy the output."],
  [("Why is my decoded text garbled?", "The original bytes may not have been UTF-8 text — for example an image or a compressed file. Decode it as a file instead."),
   ("What is the '=' at the end?", "Padding that makes the length a multiple of 4. It can be safely removed in URL-safe contexts."),
   ("Is Base64 secure?", "No. It offers zero confidentiality. Use proper encryption for secrets.")],
  popular=True, related=["image-to-base64", "url-encoder", "jwt-decoder", "hash-generator"]),

T("url-encoder", "URL Encode / Decode & Parser", "developer",
  "Percent-encode strings, decode URLs and break a URL into its parts.",
  "URL Encoder, Decoder & Parser — Percent-Encoding Tool",
  "Encode and decode URLs and query strings (percent-encoding), and parse any URL into protocol, host, path and parameters. Free and private.",
  """<p>URLs may only contain a limited set of ASCII characters. Everything else — spaces, ampersands inside values, non-Latin text — must be <em>percent-encoded</em> as <code>%</code> followed by two hex digits (a space becomes <code>%20</code>). Getting this wrong is behind countless broken links, failed API calls and analytics parameters that silently truncate.</p>
<h3>Component vs. full URL encoding</h3>
<p><b>Encode component</b> (<code>encodeURIComponent</code>) escapes everything that has meaning in a URL, including <code>/ ? &amp; =</code>. Use it for a single query value. <b>Encode full URL</b> (<code>encodeURI</code>) leaves the structural characters intact and only escapes what is illegal — use it on a complete address that already has the right shape.</p>
<p>The <b>Parse URL</b> button splits an address into protocol, host, path, hash and each query parameter, decoded — a fast way to audit tracking links or debug redirects.</p>""",
  ["Paste a URL or text.", "Choose Encode component, Encode full URL, Decode or Parse.", "Copy the result."],
  [("Should spaces be %20 or +?", "In paths use %20. In HTML form submissions (application/x-www-form-urlencoded) spaces become +. Our decoder handles both."),
   ("Why is my URL double-encoded (%2520)?", "It was encoded twice — %25 is the encoding of %. Decode once to fix it."),
   ("Is the URL sent anywhere?", "No, parsing uses your browser's built-in URL API.")],
  related=["utm-builder", "base64", "html-entities"]),

T("jwt-decoder", "JWT Decoder", "developer",
  "Inspect JSON Web Token header and payload, with expiry check.",
  "JWT Decoder — Decode JSON Web Tokens Online (Private)",
  "Decode a JSON Web Token's header and payload, check iat and exp claims, and see the algorithm — entirely in your browser. Tokens are never uploaded.",
  """<p>A JSON Web Token (JWT, RFC 7519) is three Base64URL-encoded parts joined by dots: a <b>header</b> naming the signing algorithm, a <b>payload</b> of claims (who the user is, when the token expires), and a <b>signature</b>. Because the first two parts are only encoded, anyone holding a token can read them — which is exactly why this decoder is useful for debugging authentication.</p>
<h3>Claims you'll see most</h3>
<table><tr><th>Claim</th><th>Meaning</th></tr><tr><td><code>sub</code></td><td>Subject — usually the user ID</td></tr><tr><td><code>iat</code></td><td>Issued-at time (Unix seconds)</td></tr><tr><td><code>exp</code></td><td>Expiry time — we flag expired tokens</td></tr><tr><td><code>aud</code> / <code>iss</code></td><td>Intended audience and issuer</td></tr></table>
<div class="callout">Security note: never paste production tokens into tools that send them to a server. This decoder runs locally. It does not verify signatures — verification requires the secret or public key and must happen on your backend.</div>""",
  ["Paste a token (starts with <code>eyJ</code>).", "Click <b>Decode</b>.", "Review header, payload and the expiry status."],
  [("Can you verify the signature?", "Not here — verification needs your secret or public key, which should never be pasted into a website."),
   ("Why is my token 'expired'?", "Its exp claim is earlier than your device clock. Check clock skew if it just expired."),
   ("Is a JWT encrypted?", "Standard signed JWTs (JWS) are not encrypted. Encrypted JWTs (JWE) have five parts and can't be decoded without a key.")],
  popular=True, related=["base64", "timestamp-converter", "hash-generator"]),

T("uuid-generator", "UUID / GUID Generator", "developer",
  "Bulk-generate v4 random or v7 time-ordered UUIDs.",
  "UUID Generator — Bulk v4 & v7 UUIDs / GUIDs",
  "Generate up to 1,000 cryptographically random UUID v4 or time-ordered UUID v7 identifiers. Uppercase and no-hyphen options, copy or download.",
  """<p>A UUID (Universally Unique Identifier, also called a GUID) is a 128-bit value written as 32 hex digits in five groups, e.g. <code>3f2b8c1e-7a4d-4e9b-9c2a-1d5e6f7a8b9c</code>. Systems use them as database keys and request IDs because they can be generated anywhere without coordination and practically never collide.</p>
<h3>v4 or v7?</h3>
<p><b>Version 4</b> is 122 bits of randomness — the classic choice. <b>Version 7</b> (RFC 9562, 2024) puts a millisecond Unix timestamp in the first 48 bits, so IDs sort by creation time. That keeps B-tree database indexes compact and inserts fast, which is why many teams now default to v7 for primary keys.</p>
<p>All values here come from <code>crypto.getRandomValues</code>, the browser's cryptographically secure generator — not <code>Math.random</code>.</p>""",
  ["Pick v4 or v7 and a quantity.", "Toggle uppercase or no-hyphen formatting.", "Click <b>Generate</b>, then copy or download."],
  [("Can two UUIDs collide?", "For v4 you'd need to generate about 2.7 quintillion to have a 50% chance of one duplicate."),
   ("Is GUID the same as UUID?", "Yes — GUID is Microsoft's name for the same standard."),
   ("Which version for database keys?", "v7, if your stack supports it, because it is time-sortable.")],
  related=["password-generator", "hash-generator", "timestamp-converter"]),

T("hash-generator", "Hash Generator (MD5, SHA-256…)", "developer",
  "Live MD5, SHA-1, SHA-256, SHA-384 and SHA-512 hashes of any text.",
  "Hash Generator — MD5, SHA-1, SHA-256, SHA-512 Online",
  "Compute MD5, SHA-1, SHA-256, SHA-384 and SHA-512 hashes of text instantly in your browser using the Web Crypto API. Click any hash to copy.",
  """<p>A cryptographic hash function maps any input to a fixed-length fingerprint. Change a single character and the hash changes completely; the same input always produces the same output. Developers use hashes to verify downloads, deduplicate files, build cache keys and sign API requests.</p>
<h3>Which algorithm?</h3>
<ul><li><b>SHA-256</b> — today's default for integrity checks, Git's next object format and most signing schemes.</li>
<li><b>SHA-512 / SHA-384</b> — longer output; often faster than SHA-256 on 64-bit CPUs.</li>
<li><b>SHA-1 and MD5</b> — broken for security (practical collisions exist). Still fine for non-adversarial checksums and legacy compatibility.</li></ul>
<div class="callout">Don't store passwords as plain SHA or MD5 hashes. Use a slow password-hashing function such as Argon2id, bcrypt or scrypt.</div>""",
  ["Type or paste text.", "Hashes update as you type.", "Click any hash to copy it."],
  [("Can a hash be reversed?", "Not mathematically, but short or common inputs can be found with lookup tables — which is why passwords need salts and slow hashes."),
   ("Why does my hash differ from another tool?", "Check for trailing newlines or spaces, and encoding. We hash the UTF-8 bytes exactly as typed."),
   ("Can I hash files?", "File hashing is on the roadmap; for now use the command line: <code>sha256sum file</code>.")],
  related=["password-generator", "base64", "uuid-generator"]),

T("regex-tester", "Regex Tester", "developer",
  "Test JavaScript regular expressions with live highlighting and groups.",
  "Regex Tester — Live JavaScript Regular Expression Debugger",
  "Test and debug regular expressions with live match highlighting, capture groups, named groups and replace preview. JavaScript flavor, runs locally.",
  """<p>Regular expressions are a compact language for describing text patterns — validating emails, extracting IDs from logs, or rewriting thousands of lines at once. They're also notoriously easy to get subtly wrong, so testing against real samples before shipping is essential.</p>
<p>This tester uses your browser's native JavaScript regex engine, so behaviour matches Node.js and front-end code exactly. Matches are highlighted live; the panel below lists each match with its index and capture groups, or shows the full result of a replacement.</p>
<h3>Flags cheat sheet</h3>
<table><tr><th>Flag</th><th>Effect</th></tr><tr><td>g</td><td>Find all matches (always on here)</td></tr><tr><td>i</td><td>Case-insensitive</td></tr><tr><td>m</td><td>^ and $ match at each line</td></tr><tr><td>s</td><td>. also matches newlines</td></tr><tr><td>u</td><td>Unicode mode (\\p{L} etc.)</td></tr></table>
<p>New to regex? Read our <a href="../../guides/regular-expressions-for-beginners/">beginner's guide to regular expressions</a>.</p>""",
  ["Enter a pattern and flags.", "Paste test text — matches highlight instantly.", "Optionally enter a replacement using $1 or $&lt;name&gt;."],
  [("Which regex flavor is this?", "ECMAScript (JavaScript). Most syntax is shared with PCRE, Python and Java, but lookbehind and named-group syntax can differ slightly."),
   ("Why does my pattern hang?", "Nested quantifiers like (a+)+ can cause catastrophic backtracking. Simplify the pattern."),
   ("How do I match a literal dot?", "Escape it: \\.")],
  popular=True, related=["text-cleaner", "diff-checker", "case-converter"]),

T("timestamp-converter", "Unix Timestamp Converter", "developer",
  "Convert epoch seconds/milliseconds to dates and back.",
  "Unix Timestamp Converter — Epoch to Date & Date to Epoch",
  "Convert Unix epoch timestamps (seconds or milliseconds) to UTC, local and ISO 8601 dates, and convert dates back to timestamps. Live current epoch clock.",
  """<p>A Unix timestamp counts seconds since 00:00:00 UTC on 1 January 1970 (the “epoch”). Databases, logs, JWTs and APIs store time this way because it is time-zone-free and easy to compare. JavaScript and many analytics tools use <em>milliseconds</em> instead — 13 digits rather than 10. This converter detects which you pasted automatically.</p>
<h3>Why ISO 8601?</h3>
<p>The <code>2026-10-16T08:00:00.000Z</code> format is unambiguous, sorts correctly as text, and is what JSON APIs should exchange. The trailing <code>Z</code> means UTC.</p>
<p>Note on 2038: systems that store timestamps as signed 32-bit integers overflow on 19 January 2038. Modern 64-bit systems are unaffected, but embedded devices and old databases may not be.</p>""",
  ["Paste a timestamp and click <b>→ Date</b>.", "Or pick a date and time and click <b>→ Timestamp</b>.", "Copy any value from the results."],
  [("Seconds or milliseconds?", "10 digits ≈ seconds, 13 digits ≈ milliseconds. We detect it for you."),
   ("Why is my converted time off by hours?", "You're comparing UTC with local time. Both are shown."),
   ("What about leap seconds?", "Unix time ignores leap seconds, as do almost all systems.")],
  related=["cron-explainer", "jwt-decoder", "uuid-generator"]),

T("cron-explainer", "Cron Expression Explainer", "developer",
  "Translate cron schedules to plain English and preview next runs.",
  "Cron Expression Explainer & Next Run Calculator",
  "Paste a 5-field cron expression to get a plain-English explanation and the next 8 run times in your local time zone. Supports ranges, steps, lists and names.",
  """<p>Cron is the Unix scheduler behind backups, reports, cache warmers and countless CI jobs. Its five fields — <b>minute, hour, day of month, month, day of week</b> — are compact but easy to misread. One wrong asterisk can turn a nightly job into one that fires every minute.</p>
<table><tr><th>Syntax</th><th>Meaning</th><th>Example</th></tr><tr><td><code>*</code></td><td>every value</td><td><code>* * * * *</code> every minute</td></tr><tr><td><code>*/n</code></td><td>every n</td><td><code>*/15 * * * *</code> every 15 min</td></tr><tr><td><code>a-b</code></td><td>range</td><td><code>0 9-17 * * *</code> hourly 9–17</td></tr><tr><td><code>a,b</code></td><td>list</td><td><code>0 0 1,15 * *</code> 1st &amp; 15th</td></tr></table>
<p>One classic gotcha: if <b>both</b> day-of-month and day-of-week are restricted, cron runs when <em>either</em> matches. Our next-run preview follows that rule. Learn more in our <a href="../../guides/cron-jobs-explained/">cron jobs guide</a>.</p>""",
  ["Type a cron expression or click an example chip.", "Read the explanation.", "Check the next run times before deploying."],
  [("Does it support seconds?", "Standard cron has 5 fields. Quartz and some cloud schedulers add seconds or years — strip those first."),
   ("Is 0 or 7 Sunday?", "Both mean Sunday."),
   ("Which time zone does cron use?", "The server's local zone unless configured (e.g. CRON_TZ). Our preview uses your browser's zone.")],
  related=["timestamp-converter", "regex-tester"]),

T("diff-checker", "Text Diff Checker", "developer",
  "Compare two texts line-by-line or word-by-word.",
  "Diff Checker — Compare Two Texts Online (Line & Word Diff)",
  "Find the differences between two blocks of text or code, line by line or word by word, with added and removed counts. Private, in-browser diff.",
  """<p>A diff shows exactly what changed between two versions of a document: config files before and after a deploy, contract drafts, API responses or translated copy. This checker uses a longest-common-subsequence algorithm — the same idea behind <code>git diff</code> — to keep matching content aligned and highlight only real changes.</p>
<p><b>Line mode</b> is best for code and configuration. <b>Word mode</b> is better for prose, where a single edited word would otherwise mark a whole paragraph as changed.</p>
<div class="callout">Tip: to compare two JSON documents reliably, run both through the <a href="../json-formatter/">JSON formatter</a> with <b>Sort keys</b> first so ordering differences disappear.</div>""",
  ["Paste the original on the left and the changed text on the right.", "Choose line or word comparison.", "Green = added, red = removed."],
  [("Is there a size limit?", "Very large inputs (millions of comparisons) are refused to keep your browser responsive."),
   ("Does it ignore whitespace?", "Not yet — use the Text Cleaner to trim lines first."),
   ("Is my text uploaded?", "No.")],
  related=["json-formatter", "text-cleaner", "word-counter"]),

T("html-entities", "HTML Entity Encoder / Decoder", "developer",
  "Escape &lt; &gt; &amp; and quotes, or decode entities back to text.",
  "HTML Entity Encoder & Decoder — Escape HTML Online",
  "Encode special characters as HTML entities to prevent broken markup and XSS, or decode entities back into readable text. Free and private.",
  """<p>Characters like <code>&lt;</code>, <code>&gt;</code> and <code>&amp;</code> have special meaning in HTML. To show them literally — in a code sample, a tooltip or user-generated content — they must be written as entities such as <code>&amp;lt;</code>. Failing to escape user input is the root cause of cross-site scripting (XSS), one of the most common web vulnerabilities.</p>
<p><b>Encode</b> escapes the five critical characters. <b>Encode non-ASCII too</b> additionally converts characters like “é” or “—” into numeric entities, useful for systems that mangle UTF-8. <b>Decode</b> turns entities back into plain text.</p>""",
  ["Paste text or HTML.", "Click Encode, Encode non-ASCII or Decode.", "Copy the output."],
  [("Is escaping enough to stop XSS?", "It's essential for HTML text content, but attributes, URLs and JavaScript contexts need context-specific encoding. Use your framework's templating."),
   ("What's the difference between &amp;amp;nbsp; and a space?", "&amp;nbsp; is a non-breaking space that prevents line wraps.")],
  related=["url-encoder", "base64", "text-cleaner"]),

T("case-converter", "Case Converter", "developer",
  "camelCase, snake_case, kebab-case, Title Case and more.",
  "Case Converter — camelCase, snake_case, kebab-case, Title Case",
  "Convert text between UPPER, lower, Title, Sentence, camelCase, PascalCase, snake_case, kebab-case, CONSTANT_CASE and dot.case instantly.",
  """<p>Every language and tool has its naming convention: JavaScript variables are <code>camelCase</code>, classes are <code>PascalCase</code>, Python and SQL columns prefer <code>snake_case</code>, URLs and CSS classes use <code>kebab-case</code>, and environment variables are <code>CONSTANT_CASE</code>. Converting by hand is slow and error-prone, especially across dozens of field names.</p>
<p>The converter splits input on spaces, punctuation and existing camel humps, so <code>userIDValue</code>, <code>user_id_value</code> and “User ID value” all normalise cleanly. Paste a list — one item per line — to convert many identifiers at once.</p>""",
  ["Paste text.", "Click the target case.", "Copy the output."],
  [("Does Title Case follow AP or Chicago rules?", "It capitalises every word. For editorial headlines, review small words like “of” and “and” manually."),
   ("Can I convert many lines?", "Yes, each line is converted; separators between lines are preserved for simple cases.")],
  related=["text-cleaner", "word-counter", "lorem-ipsum"]),

T("number-base", "Number Base Converter", "developer",
  "Decimal ⇄ hex ⇄ binary ⇄ octal with big-number support.",
  "Number Base Converter — Binary, Hex, Decimal, Octal",
  "Convert numbers between decimal, hexadecimal, binary, octal and base 36 in real time. Uses BigInt so arbitrarily large integers stay exact.",
  """<p>Computers think in binary, engineers read memory and colours in hexadecimal, Unix permissions are octal, and humans count in decimal. This converter keeps all of them in sync as you type, using JavaScript's <code>BigInt</code> so even 256-bit values (like cryptographic keys) convert without losing precision.</p>
<h3>Quick reference</h3>
<table><tr><th>Decimal</th><th>Hex</th><th>Binary</th></tr><tr><td>10</td><td>A</td><td>1010</td></tr><tr><td>255</td><td>FF</td><td>1111 1111</td></tr><tr><td>4096</td><td>1000</td><td>1 0000 0000 0000</td></tr></table>
<p>Prefixes such as <code>0x</code>, <code>0b</code> and <code>0o</code> are accepted and ignored.</p>""",
  ["Type into any base field.", "All other fields update instantly.", "Copy whichever representation you need."],
  [("Does it support fractions?", "Integers only — fractional base conversion is lossy and rarely needed."),
   ("Negative numbers?", "Yes, with a leading minus sign (not two's complement).")],
  related=["color-converter", "cidr-calculator", "data-size-converter"]),

T("yaml-json", "YAML ⇄ JSON Converter", "developer",
  "Convert Kubernetes/CI YAML to JSON and back.",
  "YAML to JSON Converter (and JSON to YAML)",
  "Convert YAML to JSON and JSON to YAML online with clear error messages. Ideal for Kubernetes manifests, GitHub Actions, Docker Compose and OpenAPI files.",
  """<p>YAML dominates infrastructure: Kubernetes manifests, GitHub Actions workflows, Docker Compose and OpenAPI specs are all YAML. But many APIs and programming tools want JSON. Because YAML is a superset of JSON, conversion is lossless for normal data — but YAML's indentation rules make subtle mistakes common.</p>
<p>This converter uses the widely adopted open-source js-yaml parser (loaded from cdnjs on first use) and reports the exact line of any indentation or syntax error.</p>
<div class="callout">YAML gotcha: unquoted <code>no</code>, <code>yes</code>, <code>on</code> and <code>off</code> may be parsed as booleans by older YAML 1.1 parsers (“the Norway problem”). Quote country codes and flags to be safe.</div>""",
  ["Paste YAML on the left (or JSON on the right).", "Click the conversion direction.", "Copy the result."],
  [("Are comments preserved?", "No — JSON has no comments, so they are dropped when converting from YAML."),
   ("Multi-document YAML (---)?", "Only the first document is converted.")],
  related=["json-formatter", "json-to-csv"]),

T("json-to-csv", "JSON ⇄ CSV Converter", "developer",
  "Turn JSON arrays into spreadsheets and CSV into JSON.",
  "JSON to CSV Converter (and CSV to JSON) — Free Online",
  "Convert a JSON array of objects into CSV for Excel or Google Sheets, or parse CSV with quoted fields back into JSON. Downloads included.",
  """<p>APIs speak JSON; finance, sales and operations teams live in spreadsheets. This converter bridges the two. It collects every key across all objects to build the header row, so records with missing fields still line up, and it escapes commas, quotes and line breaks according to RFC 4180 so Excel and Google Sheets open the file cleanly.</p>
<p>Going the other way, the CSV parser handles quoted fields containing commas and doubled quotes, then maps each row to an object keyed by the header.</p>""",
  ["Paste a JSON array (or CSV with a header row).", "Click JSON → CSV or CSV → JSON.", "Copy or download the result."],
  [("What about nested objects?", "Nested values are written as JSON strings inside the cell."),
   ("Excel shows weird characters?", "Import via Data → From Text/CSV and choose UTF-8.")],
  related=["json-formatter", "yaml-json", "text-cleaner"]),

# ---------------- SECURITY ----------------
T("password-generator", "Strong Password Generator", "security",
  "Cryptographically random passwords and memorable passphrases.",
  "Strong Password Generator — Random Passwords & Passphrases",
  "Generate strong random passwords (6–128 characters) or memorable passphrases with entropy scoring. Uses your browser's secure random generator; nothing is stored.",
  """<p>Most account takeovers start with reused or guessable passwords. The fix is simple: a unique, random password for every account, kept in a password manager. This generator uses <code>crypto.getRandomValues</code> — a cryptographically secure source — and guarantees at least one character from every set you select.</p>
<h3>How strong is strong enough?</h3>
<p>Strength is measured in bits of <b>entropy</b>: length × log₂(pool size). A 20-character password from all four sets has about 130 bits — far beyond any brute-force attack. For things you must type or remember, a <b>passphrase</b> of five random words is easier on humans and still strong.</p>
<table><tr><th>Entropy</th><th>Verdict</th></tr><tr><td>&lt; 50 bits</td><td>Weak — crackable offline</td></tr><tr><td>50–80</td><td>Good for most accounts</td></tr><tr><td>80+</td><td>Excellent</td></tr></table>
<p>Read our <a href="../../guides/password-security-guide/">password security guide</a> for the full picture.</p>""",
  ["Set the length with the slider.", "Choose character sets.", "Click <b>Generate</b> or <b>Passphrase</b>, then copy."],
  [("Are generated passwords saved?", "No. They exist only in this page until you close it."),
   ("Why exclude look-alike characters?", "Removing I, l, 1, O and 0 helps when a password must be read aloud or typed from paper."),
   ("Passphrase or password?", "Random passwords for a password manager; passphrases for your master password and device logins.")],
  popular=True, related=["password-strength", "hash-generator", "uuid-generator"]),

T("password-strength", "Password Strength Checker", "security",
  "Estimate entropy and crack time with actionable tips.",
  "Password Strength Checker — Entropy & Crack-Time Estimate",
  "Check how strong a password is with an entropy score, estimated offline crack time and specific improvement tips. Checked locally, never transmitted.",
  """<p>Password meters on sign-up forms often reward the wrong things — a capital letter and an exclamation mark turn “Password1!” green. Real attackers use dictionaries, leaked-password lists and keyboard patterns first. This checker estimates entropy, then penalises common passwords, repeated characters and sequences like “1234” or “qwer” to give a more honest verdict.</p>
<p>The crack-time figure assumes an attacker with a fast GPU rig making ten billion guesses per second against a fast hash — a realistic worst case after a data breach. Slow password hashes (bcrypt, Argon2) make real-world attacks thousands of times harder, but you can't know which one a website uses.</p>
<div class="callout">Your typing is evaluated in JavaScript on this page. Nothing is logged or sent — verify by opening your browser's network tab.</div>""",
  ["Type a password.", "Read the strength rating and crack-time estimate.", "Follow the tips, or generate a new one."],
  [("Is it safe to type my real password?", "It never leaves your device, but best practice is to test a similar pattern rather than your actual password."),
   ("Why is length more important than symbols?", "Each extra character multiplies the search space; symbols only enlarge it modestly.")],
  related=["password-generator", "hash-generator"]),

T("qr-code-generator", "QR Code Generator", "security",
  "Custom-colour QR codes for URLs, Wi-Fi and text — PNG download.",
  "Free QR Code Generator — Custom Colours, PNG Download, No Sign-Up",
  "Create QR codes for links, text and contact details with custom colours, size and error correction. Download PNG. No sign-up, no expiry, no tracking redirects.",
  """<p>Many “free” QR generators route your code through their own short link so they can track scans — and later disable it unless you pay. Codes generated here encode your content <em>directly</em>, so they work forever and nobody sits in the middle.</p>
<h3>Choosing error correction</h3>
<p>QR codes contain redundancy that lets them scan even when partly damaged or covered. <b>Low</b> (7%) gives the smallest, simplest pattern; <b>High</b> (30%) survives scratches or a logo placed in the centre. For print, choose Medium or higher and test with several phones.</p>
<p>Keep strong contrast — dark foreground on light background. Inverted or low-contrast codes fail on many scanners.</p>""",
  ["Enter a URL or text.", "Choose size, error correction and colours.", "Click <b>Generate</b>, scan to test, then download PNG."],
  [("Do these QR codes expire?", "Never — the data is encoded directly with no redirect."),
   ("Can I track scans?", "Not with a static code. Add UTM parameters with our <a href=\"../utm-builder/\">UTM builder</a> and measure in your analytics."),
   ("How much text fits?", "Up to ~2,900 characters at Low error correction, fewer at higher levels.")],
  popular=True, related=["utm-builder", "url-encoder", "image-compressor"]),

# ---------------- NETWORK ----------------
T("what-is-my-ip", "What Is My IP Address", "network",
  "See your public IP, ISP, location and time zone.",
  "What Is My IP Address? — Public IPv4/IPv6, ISP & Location",
  "Instantly see your public IP address (IPv4 or IPv6), approximate location, ISP/organisation, ASN and time zone. Free IP lookup.",
  """<p>Your <b>public IP address</b> is how the rest of the internet sees your connection. It's different from the private address (like 192.168.x.x) that your router gives your laptop. Support teams ask for it when whitelisting access, game servers use it for matchmaking, and it's the first thing to check when a VPN seems not to be working.</p>
<p>The location shown is derived from IP registration databases and is usually accurate to the city or region — not your street. ISPs also rotate addresses, so your IP may change after a router restart.</p>
<h3>IPv4 vs IPv6</h3>
<p>IPv4 addresses (e.g. 203.0.113.7) are running out; IPv6 (e.g. 2001:db8::1) has a practically unlimited supply. If you see an IPv6 address, your ISP supports the modern protocol.</p>""",
  ["Open the page — your IP appears automatically.", "Click <b>Copy</b> to share it with support."],
  [("Can someone find my home from my IP?", "Only an approximate area. Your ISP holds the exact customer mapping and releases it only under legal process."),
   ("Why does it show a different city?", "IP geolocation is approximate and may show your ISP's hub location."),
   ("How do I hide my IP?", "Use a reputable VPN or Tor; your traffic then appears to come from their servers.")],
  popular=True, related=["dns-lookup", "cidr-calculator", "browser-info"]),

T("dns-lookup", "DNS Lookup", "network",
  "Query A, AAAA, MX, TXT, NS, CNAME, CAA and more records.",
  "DNS Lookup — Check A, MX, TXT, NS, CNAME & CAA Records",
  "Look up DNS records for any domain via DNS-over-HTTPS: A, AAAA, CNAME, MX, TXT, NS, SOA, CAA, SRV and PTR. Check email (SPF/DMARC) and propagation.",
  """<p>The Domain Name System translates names like <code>example.com</code> into IP addresses and holds the records that route email and prove domain ownership. When a site won't load after a migration, email bounces, or a verification TXT record “isn't found”, a DNS lookup is the first diagnostic step.</p>
<table><tr><th>Record</th><th>Purpose</th></tr><tr><td>A / AAAA</td><td>IPv4 / IPv6 address of the host</td></tr><tr><td>CNAME</td><td>Alias pointing to another name</td></tr><tr><td>MX</td><td>Mail servers, with priority</td></tr><tr><td>TXT</td><td>SPF, DKIM, DMARC, site verification</td></tr><tr><td>NS</td><td>Authoritative name servers</td></tr><tr><td>CAA</td><td>Which CAs may issue TLS certificates</td></tr></table>
<p>Queries go directly from your browser to Google Public DNS over HTTPS. Results reflect what that resolver currently caches, so recently changed records may take up to the old TTL to update. See our <a href="../../guides/how-dns-works/">How DNS works guide</a>.</p>""",
  ["Enter a domain (no https://).", "Pick a record type and click <b>Lookup</b>, or check all common records.", "Compare TTLs and values with your DNS provider."],
  [("Why don't I see my new record?", "Resolvers cache records for the TTL period. Wait, or lower the TTL before future changes."),
   ("How do I check SPF or DMARC?", "Look up TXT on the domain for SPF, and TXT on _dmarc.yourdomain.com for DMARC."),
   ("What does NXDOMAIN mean?", "The domain doesn't exist in DNS — check spelling or registration.")],
  popular=True, related=["what-is-my-ip", "cidr-calculator", "http-status-codes"]),

T("cidr-calculator", "Subnet / CIDR Calculator", "network",
  "Network, broadcast, host range and mask for any IPv4 CIDR.",
  "Subnet Calculator — IPv4 CIDR, Netmask, Host Range",
  "Calculate network address, broadcast, usable host range, subnet mask, wildcard mask and host count for any IPv4 CIDR. Includes a /8–/32 cheat sheet.",
  """<p>CIDR notation (<code>192.168.1.0/24</code>) describes a block of IP addresses: the number after the slash is how many leading bits identify the network. The remaining bits identify hosts. Cloud VPCs, firewall rules, Kubernetes pod ranges and office networks are all planned in CIDR blocks.</p>
<p>Two addresses in each normal subnet are reserved — the network address and the broadcast address — so a /24 has 256 addresses but 254 usable hosts. Point-to-point /31 links and single-host /32 routes are special cases, handled correctly here.</p>
<p>The private ranges defined in RFC 1918 — 10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16 — are flagged automatically. Our <a href="../../guides/ip-addresses-and-subnetting/">subnetting guide</a> walks through the maths.</p>""",
  ["Enter an IPv4 address with prefix, e.g. 10.0.0.5/20.", "Read network, mask, broadcast and host range.", "Open the cheat sheet for quick sizing."],
  [("How many hosts in a /26?", "64 addresses, 62 usable."),
   ("What's a wildcard mask?", "The inverse of the subnet mask, used in Cisco ACLs and OSPF."),
   ("IPv6 support?", "Coming soon — IPv6 subnets are usually /64.")],
  related=["what-is-my-ip", "dns-lookup", "number-base"]),

T("browser-info", "User-Agent Parser & Browser Info", "network",
  "Parse any user-agent and see your screen, viewport and device details.",
  "User Agent Parser — What's My Browser, OS & Screen Size",
  "Parse any User-Agent string into browser, engine, OS and device type, and see your own screen resolution, viewport, pixel ratio, language and time zone.",
  """<p>Every browser sends a <b>User-Agent</b> string identifying itself. Support teams ask customers for it, QA teams reproduce bugs with it, and analytics tools segment traffic by it. Unfortunately the format is a historical mess — nearly every browser claims to be “Mozilla/5.0” and Chrome also claims to be Safari — so parsing by eye is unreliable.</p>
<p>This tool decodes the string into browser, version, rendering engine, operating system and device type, and flags common crawlers. The “Your device” panel adds details a screenshot can't show: viewport size, device pixel ratio, colour depth, time zone and dark-mode preference — everything a front-end developer needs to reproduce a layout bug.</p>""",
  ["Your own browser is parsed automatically.", "Paste any other UA string and click <b>Parse</b>.", "Copy the details into your bug report."],
  [("Is the user-agent reliable?", "It can be spoofed and is being reduced by browsers (UA reduction). Use feature detection for logic, UA only for diagnostics."),
   ("Why does Windows 11 show as 10/11?", "Windows 11 still reports 'Windows NT 10.0' in the UA string.")],
  related=["what-is-my-ip", "aspect-ratio-calculator"]),

T("http-status-codes", "HTTP Status Codes Reference", "network",
  "Searchable list of 1xx–5xx codes with plain-English meanings.",
  "HTTP Status Codes — Complete Searchable Reference (1xx–5xx)",
  "Searchable reference of HTTP status codes from 100 to 504 with plain-English explanations — redirects, client errors, server errors and SEO implications.",
  """<p>Every HTTP response starts with a three-digit status code. The first digit tells you the class: <b>2xx</b> success, <b>3xx</b> redirect, <b>4xx</b> the client did something wrong, <b>5xx</b> the server failed. Knowing the difference between, say, 401 and 403, or 301 and 302, saves hours of debugging and protects your search rankings.</p>
<h3>SEO-critical codes</h3>
<ul><li><b>301/308</b> — permanent moves; search engines transfer ranking signals.</li><li><b>302/307</b> — temporary; the original URL stays indexed.</li><li><b>404 vs 410</b> — 410 tells crawlers to drop a page faster.</li><li><b>503</b> — with Retry-After, the right way to signal maintenance without losing rankings.</li></ul>""",
  ["Search by number or keyword.", "Filter by class with the chips.", "Read the meaning and fix accordingly."],
  [("401 vs 403?", "401: you're not authenticated. 403: you are, but you're not allowed."),
   ("Should a missing page return 200?", "No — a 'soft 404' confuses search engines. Return a real 404 status.")],
  related=["dns-lookup", "url-encoder", "robots-txt-generator"]),

# ---------------- WEB & SEO ----------------
T("meta-tag-generator", "Meta Tag Generator", "seo",
  "SEO title, description, canonical, Open Graph and Twitter tags.",
  "Meta Tag Generator — SEO, Open Graph & Twitter Card Tags",
  "Generate SEO meta tags, canonical, Open Graph and Twitter/X card markup with a live Google search preview and length counters.",
  """<p>The title tag and meta description are what searchers see in Google results, and Open Graph tags control how your link looks when shared on LinkedIn, Facebook, Slack or WhatsApp. A compelling, correctly sized snippet can lift click-through rate significantly without changing your ranking.</p>
<ul><li><b>Title</b>: aim for ≤ 60 characters; put the primary keyword early.</li><li><b>Description</b>: ≤ 160 characters; write it like ad copy with a reason to click.</li><li><b>Canonical</b>: tells search engines which URL is the original when duplicates exist (tracking parameters, HTTP/HTTPS, trailing slashes).</li><li><b>og:image</b>: 1200×630 px works across most platforms.</li></ul>""",
  ["Fill in title, description and URL.", "Check the live preview and character counters.", "Copy the generated tags into your page's &lt;head&gt;."],
  [("Does Google always use my description?", "Not always — it rewrites snippets to match the query, but a good description is used more often."),
   ("Do meta keywords matter?", "No. Google has ignored the keywords meta tag for over a decade.")],
  related=["robots-txt-generator", "utm-builder", "word-counter"]),

T("robots-txt-generator", "Robots.txt Generator", "seo",
  "Build robots.txt with sitemap and AI-crawler blocking.",
  "Robots.txt Generator — With AI Crawler Blocking & Sitemap",
  "Create a valid robots.txt file: allow or block crawlers, disallow paths, block AI training bots like GPTBot and CCBot, and declare your sitemap.",
  """<p><code>robots.txt</code> sits at the root of your domain and tells well-behaved crawlers which paths they may fetch. It's used to keep admin areas, cart pages and internal search results out of crawl budgets, and — increasingly — to opt out of AI model training crawlers.</p>
<div class="callout">robots.txt is a request, not a lock. It does not hide pages from people or stop malicious bots. Never rely on it to protect private data; use authentication.</div>
<p>Also note: blocking a page in robots.txt doesn't remove it from Google if other sites link to it. To de-index a page, allow crawling and add a <code>noindex</code> meta tag instead — you can generate one with our <a href="../meta-tag-generator/">meta tag generator</a>.</p>""",
  ["Choose the default policy.", "List paths to disallow.", "Optionally block AI crawlers and add your sitemap URL.", "Download and upload to your site root."],
  [("Where does robots.txt go?", "At https://yourdomain.com/robots.txt — subfolders are ignored."),
   ("Does blocking GPTBot affect Google rankings?", "No. Google-Extended controls AI training only; Googlebot still indexes you.")],
  related=["meta-tag-generator", "http-status-codes", "utm-builder"]),

T("utm-builder", "UTM Campaign URL Builder", "seo",
  "Tag links with utm_source, medium and campaign for analytics.",
  "UTM Builder — Campaign URL Generator for Google Analytics",
  "Build UTM-tagged campaign URLs for Google Analytics and other tools with consistent lowercase naming. Copy-ready links for email, social and ads.",
  """<p>UTM parameters tell your analytics where a visitor came from. Without them, traffic from newsletters, social posts and partner links lands in “direct” or “referral” buckets and you can't tell which campaign actually worked.</p>
<table><tr><th>Parameter</th><th>Use for</th><th>Example</th></tr><tr><td>utm_source</td><td>Who sent the traffic</td><td>newsletter, linkedin</td></tr><tr><td>utm_medium</td><td>Channel type</td><td>email, social, cpc</td></tr><tr><td>utm_campaign</td><td>The initiative</td><td>fall_launch</td></tr><tr><td>utm_content</td><td>Which link/creative</td><td>header_button</td></tr></table>
<p>Consistency matters more than cleverness: analytics treats “Email” and “email” as different mediums. The lowercase option enforces one convention.</p>""",
  ["Enter your landing page URL.", "Fill source, medium and campaign.", "Copy the generated URL."],
  [("Should I use UTMs on internal links?", "No — that overwrites the visitor's original source and corrupts your data."),
   ("Are UTMs case-sensitive?", "Yes, in most analytics tools. Stick to lowercase.")],
  related=["qr-code-generator", "url-encoder", "meta-tag-generator"]),

# ---------------- TEXT ----------------
T("word-counter", "Word & Character Counter", "text",
  "Words, characters, sentences, reading time and keyword density.",
  "Word Counter — Characters, Sentences, Reading Time & Keyword Density",
  "Count words, characters (with and without spaces), sentences and paragraphs, estimate reading and speaking time, and see keyword density as you type.",
  """<p>Character and word limits are everywhere: meta descriptions, tweets, college essays, ad copy, app-store listings and LinkedIn headlines. This counter updates live as you type and adds the metrics writers actually need — reading time (at 238 words per minute, the average for adult non-fiction readers), speaking time for presentations (150 wpm) and the most frequent keywords.</p>
<p>Keyword density helps you spot accidental over-repetition. Modern SEO doesn't reward stuffing a keyword; if one term dominates the list, vary your wording.</p>""",
  ["Paste or type your text.", "Read the live statistics.", "Check top keywords for repetition."],
  [("Does it count hyphenated words as one?", "Yes, “state-of-the-art” is one word."),
   ("Is my text saved?", "No, it stays on your device.")],
  popular=True, related=["text-cleaner", "case-converter", "meta-tag-generator"]),

T("lorem-ipsum", "Lorem Ipsum Generator", "text",
  "Placeholder paragraphs, sentences or words — optional &lt;p&gt; tags.",
  "Lorem Ipsum Generator — Paragraphs, Sentences or Words",
  "Generate lorem ipsum placeholder text by paragraphs, sentences or words, optionally wrapped in HTML paragraph tags, for mockups and prototypes.",
  """<p>Lorem ipsum is scrambled Latin derived from Cicero's <em>De finibus bonorum et malorum</em> (45 BC). Designers have used it since the 1500s because it has a natural distribution of word lengths without distracting readers with meaning — so reviewers focus on layout, not copy.</p>
<p>Use it during wireframing, but swap in real content before launch: placeholder text left on a live site looks unprofessional, hurts SEO, and is a common reason ad networks reject a site as “low-value content”.</p>""",
  ["Choose amount and unit.", "Toggle the classic opening and HTML tags.", "Generate and copy."],
  [("Is lorem ipsum real Latin?", "Partly — it's altered and truncated Latin, so it doesn't read as sentences."),
   ("Can I use it commercially?", "Yes, it's public domain.")],
  related=["word-counter", "case-converter", "text-cleaner"]),

T("text-cleaner", "Text Cleaner & Line Tools", "text",
  "Trim, dedupe, sort, shuffle, number and strip HTML from text.",
  "Text Cleaner — Remove Duplicates, Sort Lines, Trim Spaces, Strip HTML",
  "Clean up text in one click: trim lines, remove extra spaces, empty or duplicate lines, sort A–Z, reverse, shuffle, number lines and strip HTML tags. Undo included.",
  """<p>Copy-pasting from PDFs, spreadsheets and web pages leaves debris: double spaces, blank lines, smart quotes that break code, and HTML tags. This toolkit chains small, predictable operations — apply as many as you need, in any order, with unlimited undo.</p>
<p>Common recipes: <b>email lists</b> — trim, remove empty lines, remove duplicates, sort. <b>Keyword lists</b> — remove duplicates, sort. <b>Code snippets</b> — smart → straight quotes. <b>Giveaway draws</b> — shuffle lines and pick the top entry.</p>""",
  ["Paste your text.", "Click operations in the order you need.", "Use Undo if needed, then copy."],
  [("Is duplicate removal case-sensitive?", "Yes — 'Apple' and 'apple' are kept. Convert case first with the Case Converter if needed."),
   ("Is shuffle truly random?", "It uses a cryptographically secure Fisher–Yates shuffle.")],
  related=["case-converter", "word-counter", "diff-checker"]),

# ---------------- DESIGN ----------------
T("color-converter", "Color Converter & Shades", "design",
  "HEX ⇄ RGB ⇄ HSL with a 9-step tint and shade palette.",
  "Color Converter — HEX to RGB to HSL + Tints & Shades",
  "Convert colours between HEX, RGB and HSL instantly, pick from a colour wheel, and generate a nine-step tint and shade palette for your design system.",
  """<p>Designers think in HSL (hue, saturation, lightness), browsers accept everything, and brand guides list HEX codes. Converting between them by hand is tedious. Type into any field and the others update; the swatch row generates lighter tints and darker shades of the same hue — a quick start for a design-system colour scale.</p>
<p>Why HSL? Adjusting lightness while keeping hue and saturation fixed produces visually coherent variations, which is how most modern UI palettes (like 50–900 scales) are built.</p>""",
  ["Enter a HEX, RGB or HSL value — or use the picker.", "Click any tint or shade to copy its HEX."],
  [("Does it support transparency?", "Alpha support (RGBA/HSLA) is on the roadmap."),
   ("Why do my colours look different in print?", "Screens use RGB light; printers use CMYK ink. Ask your printer for a proof.")],
  related=["contrast-checker", "css-gradient-generator", "box-shadow-generator"]),

T("contrast-checker", "Color Contrast Checker (WCAG)", "design",
  "Check text/background contrast against WCAG AA and AAA.",
  "Color Contrast Checker — WCAG 2.2 AA & AAA",
  "Check the contrast ratio between text and background colours against WCAG 2.2 AA and AAA for normal and large text, with a live preview.",
  """<p>About one in twelve men has some form of colour-vision deficiency, and low-contrast text is hard for everyone to read on a phone in sunlight. The Web Content Accessibility Guidelines (WCAG) define minimum contrast ratios, and many organisations are legally required to meet AA.</p>
<table><tr><th>Level</th><th>Normal text</th><th>Large text (18pt / 14pt bold)</th></tr><tr><td>AA</td><td>4.5 : 1</td><td>3 : 1</td></tr><tr><td>AAA</td><td>7 : 1</td><td>4.5 : 1</td></tr></table>
<p>The ratio is computed from relative luminance exactly as specified in WCAG 2.x.</p>""",
  ["Pick text and background colours.", "Read the ratio and pass/fail grid.", "Adjust until AA passes at minimum."],
  [("Does contrast apply to icons?", "Yes — WCAG 1.4.11 requires 3:1 for meaningful graphics and UI components."),
   ("Is 4.5:1 enough?", "It's the legal baseline in many places; aim higher for body text.")],
  related=["color-converter", "css-gradient-generator"]),

T("css-gradient-generator", "CSS Gradient Generator", "design",
  "Linear, radial and conic gradients with copy-ready CSS.",
  "CSS Gradient Generator — Linear, Radial & Conic",
  "Design linear, radial and conic CSS gradients with up to three colour stops and any angle. Random inspiration button and copy-ready CSS with fallback.",
  """<p>Gradients add depth to hero sections, buttons and cards without shipping a single image byte. CSS supports three kinds: <b>linear</b> (along an angle), <b>radial</b> (from a centre point) and <b>conic</b> (sweeping around a centre — great for pie charts and colour wheels).</p>
<p>The generated code includes a solid-colour fallback line first, a good habit for email clients and very old browsers that ignore gradients.</p>""",
  ["Choose a type and angle.", "Pick colour stops (or hit Random).", "Copy the CSS."],
  [("Can I animate gradients?", "Animate background-position on an oversized gradient, or use @property for smooth colour transitions."),
   ("Why is my gradient banding?", "Very subtle gradients over large areas can band on 8-bit screens; add more stops or slight noise.")],
  related=["color-converter", "box-shadow-generator", "contrast-checker"]),

T("box-shadow-generator", "CSS Box Shadow Generator", "design",
  "Visually tune offset, blur, spread, opacity and inset shadows.",
  "CSS Box Shadow Generator — Visual Editor",
  "Create CSS box-shadow values visually: offset, blur, spread, colour, opacity and inset, with a live preview and one-click copy.",
  """<p>Shadows communicate elevation — what's clickable, what floats above the page. Good UI shadows are usually soft and subtle: a larger blur, slight negative spread and low opacity look far more natural than a hard black offset.</p>
<p>Pro tip: layer two shadows — a tight, darker one for contact and a large, faint one for ambient light — separated by a comma in the same <code>box-shadow</code> declaration.</p>""",
  ["Drag the sliders.", "Pick a colour and toggle inset.", "Copy the CSS."],
  [("box-shadow vs drop-shadow?", "box-shadow follows the element's box; filter: drop-shadow follows the actual shape of transparent images."),
   ("Do shadows hurt performance?", "Large animated shadows can; animate opacity of a pseudo-element instead.")],
  related=["css-gradient-generator", "color-converter"]),

T("image-compressor", "Image Compressor & Resizer", "design",
  "Compress and resize JPG/PNG/WebP on your device — batch.",
  "Image Compressor — Compress & Resize JPG, PNG, WebP (No Upload)",
  "Compress and resize images in your browser — convert to WebP, JPEG or PNG with adjustable quality and max width. Batch processing, no uploads, no watermarks.",
  """<p>Images are usually the heaviest part of a web page, and page speed affects both search rankings and conversions. Most online compressors upload your photos to their servers. This one does everything on your device with the HTML canvas, so it's instant, private and works with confidential images.</p>
<h3>Which format?</h3>
<ul><li><b>WebP</b> — typically 25–35% smaller than JPEG at similar quality; supported by all modern browsers.</li><li><b>JPEG</b> — universal; best for photos when compatibility matters.</li><li><b>PNG</b> — lossless; use for screenshots, logos and transparency.</li></ul>
<p>Resizing matters more than quality: a 4000-px phone photo displayed at 1200 px wastes over 90% of its pixels.</p>""",
  ["Choose one or more images.", "Pick output format, quality and optional max width.", "Click <b>Compress</b> and download each result."],
  [("Are my images uploaded?", "No — processing happens in your browser."),
   ("Is EXIF data removed?", "Yes, re-encoding through canvas strips metadata such as GPS location."),
   ("Why did PNG get bigger?", "PNG is lossless; converting a photo to PNG often increases size. Use WebP or JPEG for photos.")],
  popular=True, related=["image-to-base64", "aspect-ratio-calculator", "qr-code-generator"]),

T("image-to-base64", "Image to Base64", "design",
  "Convert images to data URIs for CSS, HTML and email.",
  "Image to Base64 Converter — Data URI for CSS & HTML",
  "Convert an image to a Base64 data URI and copy it as raw text, a CSS background or an HTML img tag. Size overhead shown. Runs locally.",
  """<p>A data URI embeds an image directly inside HTML or CSS, saving an extra HTTP request. It's handy for tiny icons, email signatures and single-file prototypes. The trade-off: Base64 adds about 33% to file size and embedded images can't be cached separately, so keep it for assets under a few kilobytes.</p>""",
  ["Choose an image.", "Copy as a data URI, a CSS rule or an &lt;img&gt; tag."],
  [("Is there a size limit?", "No hard limit, but large data URIs bloat your HTML and slow rendering."),
   ("Do email clients support data URIs?", "Many block them; hosted images are more reliable in email.")],
  related=["base64", "image-compressor"]),

# ---------------- CALCULATORS ----------------
T("data-size-converter", "Data Size Converter", "calculators",
  "Bytes, KB, MB, GB, TB and KiB/MiB/GiB, plus bits.",
  "Data Size Converter — MB, GB, TB, GiB, Bits & Bytes",
  "Convert data sizes between bytes, KB, MB, GB, TB, PB, binary KiB/MiB/GiB/TiB and bits. Explains why a 1 TB drive shows 931 GB.",
  """<p>Storage vendors use decimal units (1 GB = 1,000,000,000 bytes) while operating systems often display binary units (1 GiB = 1,073,741,824 bytes) but label them “GB”. That's why a new “1 TB” drive appears as about 931 GB in Windows. Network speeds add a third twist: they're measured in <b>bits</b> per second, and there are 8 bits in a byte.</p>
<p>This converter shows every common unit at once so you can sanity-check cloud bills, backup plans and bandwidth quotas.</p>""",
  ["Enter a value and unit.", "Read every equivalent unit in the grid."],
  [("Is 1 KB 1000 or 1024 bytes?", "Officially 1000 (SI). 1024 bytes is 1 KiB (IEC). Many tools still blur them."),
   ("Mbps vs MB/s?", "Divide Mbps by 8 for MB/s: 100 Mbps ≈ 12.5 MB/s.")],
  related=["download-time-calculator", "number-base"]),

T("download-time-calculator", "Download Time Calculator", "calculators",
  "How long will a file take at your connection speed?",
  "Download Time Calculator — File Size × Internet Speed",
  "Estimate how long a download or upload will take from file size and connection speed, including realistic protocol overhead.",
  """<p>Will a 50 GB game finish overnight? How long will a 2 TB backup take to upload? Divide the size in bits by the speed in bits per second — then add overhead. TCP/IP headers, encryption and Wi-Fi inefficiency typically consume 5–15% of advertised bandwidth, which is why the overhead slider defaults to 10%.</p>""",
  ["Enter file size and connection speed.", "Adjust overhead to taste.", "Read the estimated time."],
  [("Why is my real download slower?", "The server, Wi-Fi signal, congestion and VPNs all cap throughput below your plan speed."),
   ("Upload vs download?", "Many plans are asymmetric — enter your upload speed for uploads.")],
  related=["data-size-converter", "what-is-my-ip"]),

T("aspect-ratio-calculator", "Aspect Ratio Calculator", "calculators",
  "Find ratios and resize dimensions for video and images.",
  "Aspect Ratio Calculator — 16:9, 4:3, 9:16 Resizer",
  "Calculate the aspect ratio of any width and height and resize while preserving proportions. Presets for 16:9, 4:3, 1:1, 21:9, 9:16 and more.",
  """<p>Aspect ratio is width divided by height. Getting it right avoids stretched thumbnails and black bars: YouTube and most monitors use 16:9, Instagram feed posts favour 4:5 or 1:1, Reels/TikTok/Shorts use 9:16, and ultrawide monitors are 21:9.</p>
<p>Enter the original dimensions, then type a new width or height and the other value is calculated to preserve proportions — handy for responsive images, video exports and CSS <code>aspect-ratio</code> values.</p>""",
  ["Enter original width and height.", "Type a new width or height to resize.", "Or click a preset ratio."],
  [("What's the YouTube thumbnail size?", "1280×720 (16:9)."),
   ("Can CSS keep ratios?", "Yes: <code>aspect-ratio: 16 / 9;</code> on the element.")],
  related=["image-compressor", "browser-info"]),
]

# map the QR id used in tools.js
for t in TOOLS:
    if t["id"] == "qr-code-generator":
        t["js_id"] = "qr-generator"
    else:
        t["js_id"] = t["id"]
