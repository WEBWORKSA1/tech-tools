"""Original long-form guides. Video IDs verified via YouTube oEmbed on 2026-10-16."""

GUIDES = [
dict(slug="json-explained", title="JSON Explained: A Practical Guide for Developers and Analysts",
 desc="What JSON is, its six data types, common syntax errors, JSON vs XML vs YAML, and how to read, validate and transform JSON quickly.",
 cat="Developer", minutes=8, video=("iiADhChRriM", "Learn JSON in 10 Minutes — Web Dev Simplified"),
 tools=["json-formatter", "yaml-json", "json-to-csv"],
 body="""
<p>If you have ever opened an API response, a <code>package.json</code> file or an exported settings file, you've met JSON. JavaScript Object Notation was popularised by Douglas Crockford in the early 2000s as a lighter alternative to XML, and it has since become the lingua franca of web data. It is human-readable, maps naturally onto the data structures of almost every programming language, and is simple enough that its full grammar fits on a single page.</p>
<h2>The six building blocks</h2>
<p>Every JSON document is built from just six kinds of value:</p>
<table><tr><th>Type</th><th>Example</th><th>Notes</th></tr>
<tr><td>Object</td><td><code>{"name": "Ada"}</code></td><td>Unordered key/value pairs; keys must be double-quoted strings</td></tr>
<tr><td>Array</td><td><code>[1, 2, 3]</code></td><td>Ordered list of any values</td></tr>
<tr><td>String</td><td><code>"hello"</code></td><td>Double quotes only; escape with backslash</td></tr>
<tr><td>Number</td><td><code>42</code>, <code>-3.14</code>, <code>1e6</code></td><td>No leading zeros, no NaN or Infinity</td></tr>
<tr><td>Boolean</td><td><code>true</code> / <code>false</code></td><td>Lowercase</td></tr>
<tr><td>Null</td><td><code>null</code></td><td>Represents “no value”</td></tr></table>
<p>Objects and arrays can nest to any depth, which is how JSON represents complex records such as an order with a customer, a list of line items and a shipping address.</p>
<h2>The five mistakes that break JSON</h2>
<ol><li><b>Trailing commas</b> — <code>[1, 2, 3,]</code> is valid JavaScript but invalid JSON.</li>
<li><b>Single quotes</b> — <code>{'a': 1}</code> must be <code>{"a": 1}</code>.</li>
<li><b>Unquoted keys</b> — <code>{a: 1}</code> is a JavaScript object literal, not JSON.</li>
<li><b>Comments</b> — JSON has no comment syntax. Tools that allow them (like VS Code settings) use a variant called JSONC.</li>
<li><b>Big numbers</b> — integers beyond 2<sup>53</sup> lose precision in JavaScript. APIs often send IDs as strings for this reason.</li></ol>
<p>Our <a href="../../tools/json-formatter/">JSON formatter</a> reports each of these with the exact line and column.</p>
<h2>JSON vs XML vs YAML</h2>
<p><b>XML</b> is more verbose but supports attributes, namespaces and schemas, so it persists in enterprise systems, office documents and RSS. <b>YAML</b> is a superset of JSON designed for humans to write: no braces, indentation-based, with comments — which is why Kubernetes and CI pipelines use it. <b>JSON</b> sits in the middle: strict enough for machines, readable enough for people, and supported natively by every browser. A good rule: exchange data in JSON, write configuration in YAML, and only choose XML when a standard demands it.</p>
<h2>Working with JSON day to day</h2>
<p>A few habits make JSON much easier to live with:</p>
<ul><li><b>Pretty-print before reading.</b> Minified responses hide structure; formatting reveals it instantly.</li>
<li><b>Sort keys before diffing.</b> Two objects with identical data but different key order look completely different in a text diff.</li>
<li><b>Use JSON Lines for logs.</b> One JSON object per line (<code>.jsonl</code>) streams and greps far better than one giant array.</li>
<li><b>Validate at the boundary.</b> Parse and validate incoming JSON against a schema (JSON Schema, Zod, Pydantic) before it reaches business logic.</li>
<li><b>Convert for non-developers.</b> Stakeholders live in spreadsheets — convert arrays of objects to CSV with our <a href="../../tools/json-to-csv/">JSON to CSV converter</a>.</li></ul>
<h2>Security notes</h2>
<p>Never use <code>eval()</code> to parse JSON — use <code>JSON.parse</code>, which can't execute code. Be careful about pasting API responses into online tools that upload them: responses often contain access tokens, emails and personal data. Everything on Tech.Tools runs locally in your browser for exactly this reason.</p>
"""),

dict(slug="regular-expressions-for-beginners", title="Regular Expressions for Beginners: Patterns You'll Actually Use",
 desc="Learn regex from scratch: character classes, quantifiers, anchors, groups and lookarounds, with ten copy-ready patterns and common pitfalls.",
 cat="Developer", minutes=10, video=("rhzKDrUiJVk", "Learn Regular Expressions In 20 Minutes — Web Dev Simplified"),
 tools=["regex-tester", "text-cleaner"],
 body="""
<p>Regular expressions (regex) describe patterns in text. With one line you can validate a postcode, pull every order number out of a log file or reformat a thousand dates. The syntax looks cryptic at first, but around a dozen symbols cover 90% of real-world use. Open our <a href="../../tools/regex-tester/">regex tester</a> in another tab and try each example as you read.</p>
<h2>Literal characters and the special ones</h2>
<p>Most characters match themselves: the pattern <code>cat</code> finds “cat”. Twelve characters have special meaning and must be escaped with a backslash to match literally: <code>. ^ $ * + ? ( ) [ ] { } | \\</code>. So to match “3.14” you write <code>3\\.14</code>.</p>
<h2>Character classes</h2>
<table><tr><th>Pattern</th><th>Matches</th></tr>
<tr><td><code>.</code></td><td>Any character except newline</td></tr>
<tr><td><code>\\d</code> / <code>\\D</code></td><td>A digit / a non-digit</td></tr>
<tr><td><code>\\w</code> / <code>\\W</code></td><td>Word character [A-Za-z0-9_] / anything else</td></tr>
<tr><td><code>\\s</code> / <code>\\S</code></td><td>Whitespace / non-whitespace</td></tr>
<tr><td><code>[aeiou]</code></td><td>Any one listed character</td></tr>
<tr><td><code>[^0-9]</code></td><td>Any character <em>not</em> in the range</td></tr></table>
<h2>Quantifiers: how many?</h2>
<p><code>*</code> means zero or more, <code>+</code> one or more, <code>?</code> zero or one, and <code>{2,4}</code> between two and four. Quantifiers are <b>greedy</b> by default — they grab as much as possible. Add <code>?</code> to make them lazy: in <code>&lt;b&gt;bold&lt;/b&gt;</code>, the pattern <code>&lt;.+&gt;</code> matches the whole string while <code>&lt;.+?&gt;</code> matches just <code>&lt;b&gt;</code>.</p>
<h2>Anchors and boundaries</h2>
<p><code>^</code> anchors to the start and <code>$</code> to the end (of the string, or of each line with the <code>m</code> flag). <code>\\b</code> marks a word boundary, so <code>\\bcat\\b</code> matches “cat” but not “category”. Anchors are essential for validation — without them, <code>\\d{5}</code> happily “validates” <code>abc123456xyz</code>.</p>
<h2>Groups, alternation and backreferences</h2>
<p>Parentheses group parts of a pattern and capture what they match: <code>(\\d{4})-(\\d{2})-(\\d{2})</code> captures year, month and day. Reference them in replacements as <code>$1</code>, <code>$2</code>… — so replacing with <code>$3/$2/$1</code> converts ISO dates to day/month/year. Name groups for readability: <code>(?&lt;year&gt;\\d{4})</code>. The pipe <code>|</code> means “or”: <code>(jpg|png|webp)$</code>.</p>
<h2>Lookarounds</h2>
<p>Lookaheads <code>(?=...)</code> and lookbehinds <code>(?&lt;=...)</code> assert that something comes next (or before) without consuming it. The classic use is password rules: <code>^(?=.*\\d)(?=.*[A-Z]).{12,}$</code> requires a digit, an uppercase letter and 12+ characters.</p>
<h2>Ten patterns worth bookmarking</h2>
<pre><code>Email (pragmatic):   ^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$
URL:                 https?://[^\\s/$.?#].[^\\s]*
IPv4:                \\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b
ISO date:            \\d{4}-\\d{2}-\\d{2}
Time 24h:            ^([01]\\d|2[0-3]):[0-5]\\d$
Hex colour:          #(?:[0-9a-fA-F]{3}){1,2}\\b
UUID:                [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}
Duplicate words:     \\b(\\w+)\\s+\\1\\b
Trailing spaces:     [ \\t]+$
US ZIP:              ^\\d{5}(-\\d{4})?$</code></pre>
<h2>Pitfalls</h2>
<ul><li><b>Catastrophic backtracking.</b> Nested quantifiers like <code>(a+)+$</code> can take exponential time on certain inputs — a real denial-of-service risk on servers.</li>
<li><b>Over-validating emails.</b> The full email grammar is enormous; a simple pattern plus a confirmation email is better than a 6,000-character regex.</li>
<li><b>Parsing HTML.</b> Regex can't reliably parse nested markup — use a DOM parser.</li></ul>
"""),

dict(slug="git-and-github-basics", title="Git & GitHub Basics: The Commands That Matter",
 desc="A practical introduction to Git and GitHub: commits, branches, merging, remotes, pull requests and the ten commands that cover daily work.",
 cat="Developer", minutes=9, video=("RGOj5yH7evk", "Git and GitHub for Beginners — Crash Course (freeCodeCamp.org)"),
 tools=["diff-checker", "timestamp-converter"],
 body="""
<p>Git is a distributed version-control system created by Linus Torvalds in 2005 to manage Linux kernel development. It records snapshots of your project so you can see what changed, when and why, undo mistakes, and work in parallel with others without overwriting each other's work. GitHub is a hosting service built around Git that adds collaboration: pull requests, code review, issues, Actions for CI/CD, and free static hosting with GitHub Pages.</p>
<h2>Core concepts in plain English</h2>
<ul><li><b>Repository</b> — a project folder plus its full history (stored in a hidden <code>.git</code> directory).</li>
<li><b>Commit</b> — a saved snapshot with a message, author and timestamp. Each commit has a unique SHA-1 (or SHA-256) hash ID.</li>
<li><b>Staging area</b> — the waiting room where you choose exactly which changes go into the next commit.</li>
<li><b>Branch</b> — a movable pointer to a line of commits, letting you develop a feature in isolation.</li>
<li><b>Remote</b> — a copy of the repository elsewhere, typically on GitHub, named <code>origin</code>.</li></ul>
<h2>The ten commands you'll use daily</h2>
<pre><code>git clone &lt;url&gt;            # copy a remote repo to your machine
git status                  # what's changed and what's staged
git add &lt;file&gt;   / git add -p  # stage changes (-p = choose hunks)
git commit -m "message"     # record a snapshot
git log --oneline --graph   # compact history
git switch -c feature-x     # create and move to a new branch
git pull                    # fetch + merge remote changes
git push -u origin feature-x # publish your branch
git diff                    # unstaged changes
git restore &lt;file&gt;          # discard local changes to a file</code></pre>
<h2>A healthy workflow</h2>
<ol><li>Pull the latest <code>main</code>.</li><li>Create a short-lived branch for one change.</li><li>Commit small, logical steps with messages that explain <em>why</em>.</li><li>Push and open a pull request; let CI run tests.</li><li>Request review, address feedback, then merge (squash merges keep history tidy).</li><li>Delete the branch.</li></ol>
<h2>Writing good commit messages</h2>
<p>Use the imperative mood (“Add password strength meter”, not “Added…”), keep the subject under about 50 characters, and use the body to explain context. Future you — and anyone running <code>git blame</code> — will be grateful.</p>
<h2>Undoing things safely</h2>
<table><tr><th>Situation</th><th>Command</th></tr>
<tr><td>Fix the last commit message</td><td><code>git commit --amend</code></td></tr>
<tr><td>Unstage a file</td><td><code>git restore --staged file</code></td></tr>
<tr><td>Undo a pushed commit</td><td><code>git revert &lt;sha&gt;</code> (creates an inverse commit)</td></tr>
<tr><td>Recover “lost” work</td><td><code>git reflog</code></td></tr></table>
<p>Avoid <code>git push --force</code> on shared branches; if you must, use <code>--force-with-lease</code>, which refuses to overwrite commits you haven't seen.</p>
<h2>Never commit secrets</h2>
<p>API keys pushed to a public repository are typically found by automated scanners within minutes. Add <code>.env</code> to <code>.gitignore</code>, use your platform's secret store, and if a secret leaks, rotate it immediately — deleting the commit isn't enough because history and forks persist.</p>
"""),

dict(slug="how-dns-works", title="How DNS Works: From Typing a URL to Loading a Page",
 desc="A clear walkthrough of the Domain Name System: resolvers, root and TLD servers, record types, TTL and caching, plus how to debug DNS problems.",
 cat="Network & IT", minutes=8, video=("mpQZVYPuDGU", "How a DNS Server (Domain Name System) works — PowerCert Animated Videos"),
 tools=["dns-lookup", "what-is-my-ip"],
 body="""
<p>Computers talk to each other using IP addresses, but humans remember names. The Domain Name System (DNS) is the internet's distributed phone book that translates <code>tech.tools</code> into an address like <code>203.0.113.10</code>. It's queried before almost every connection your devices make, usually in a few milliseconds — and when it breaks, it looks like “the internet is down”.</p>
<h2>The journey of a lookup</h2>
<ol><li><b>Local caches.</b> Your browser and operating system first check whether they resolved the name recently.</li>
<li><b>Recursive resolver.</b> If not, the query goes to a resolver — usually your ISP's, or a public one like 1.1.1.1, 8.8.8.8 or 9.9.9.9.</li>
<li><b>Root servers.</b> The resolver asks a root server, which replies with the servers responsible for the top-level domain (<code>.tools</code>, <code>.com</code>…).</li>
<li><b>TLD servers.</b> These point to the domain's <b>authoritative name servers</b> (the NS records set at your registrar).</li>
<li><b>Authoritative server.</b> Returns the actual record — an A record with an IPv4 address, for example.</li>
<li><b>Caching.</b> The resolver caches the answer for its TTL and hands it back to you.</li></ol>
<h2>Record types you need to know</h2>
<table><tr><th>Type</th><th>What it does</th><th>Example value</th></tr>
<tr><td>A</td><td>Maps a name to an IPv4 address</td><td>185.199.108.153</td></tr>
<tr><td>AAAA</td><td>Maps a name to an IPv6 address</td><td>2606:50c0:8000::153</td></tr>
<tr><td>CNAME</td><td>Alias to another hostname</td><td>www → username.github.io</td></tr>
<tr><td>MX</td><td>Mail servers with priorities</td><td>10 mx1.mailhost.com</td></tr>
<tr><td>TXT</td><td>Free text: SPF, DKIM, DMARC, verification</td><td>v=spf1 include:_spf.google.com ~all</td></tr>
<tr><td>NS</td><td>Delegates a zone to name servers</td><td>ns1.provider.net</td></tr>
<tr><td>CAA</td><td>Restricts which CAs may issue certificates</td><td>0 issue "letsencrypt.org"</td></tr></table>
<h2>TTL and “propagation”</h2>
<p>Each record carries a time-to-live in seconds. Resolvers worldwide may serve the cached old value until it expires — that's what people mean by “waiting for DNS to propagate”. The professional trick: lower the TTL to 300 seconds a day before a migration, make the change, then raise it again afterwards.</p>
<h2>Debugging checklist</h2>
<ul><li>Check the record with our <a href="../../tools/dns-lookup/">DNS lookup tool</a> or <code>dig example.com A</code>.</li>
<li>Confirm the domain's NS records point to the provider where you're editing records — editing the wrong zone is the most common mistake.</li>
<li>A CNAME can't coexist with other records at the same name, and can't sit at the zone apex (use ALIAS/ANAME or A records there).</li>
<li>For email issues, verify MX, SPF (TXT), DKIM (TXT on a selector) and DMARC (TXT on <code>_dmarc</code>).</li>
<li>Still stuck? Flush your local cache (<code>ipconfig /flushdns</code> on Windows).</li></ul>
<h2>DNS privacy and security</h2>
<p>Traditional DNS travels unencrypted, so networks can see and tamper with lookups. DNS-over-HTTPS (DoH) and DNS-over-TLS encrypt queries; DNSSEC adds signatures so answers can't be forged. Modern browsers can enable DoH in their settings.</p>
"""),

dict(slug="password-security-guide", title="Password Security in 2026: What Actually Protects Your Accounts",
 desc="Why length beats complexity, how attackers crack passwords, password managers, passphrases, passkeys and two-factor authentication explained.",
 cat="Security", minutes=8, video=("3NjQ9b3pgIg", "How to Choose a Password — Computerphile"),
 tools=["password-generator", "password-strength", "hash-generator"],
 body="""
<p>Stolen and reused credentials remain one of the most common ways attackers break into accounts. The good news: a handful of habits defeat the vast majority of attacks, and none of them require being a security expert.</p>
<h2>How passwords actually get cracked</h2>
<ul><li><b>Credential stuffing.</b> Attackers take email/password pairs leaked from one site and try them on hundreds of others. If you reuse passwords, one breach unlocks everything.</li>
<li><b>Dictionary and rule attacks.</b> Cracking tools try leaked passwords, dictionary words and predictable mutations — “Summer2026!”, “P@ssw0rd” — first. Human “cleverness” is very predictable.</li>
<li><b>Brute force.</b> Trying every combination. Modern GPUs test billions of guesses per second against fast hashes, so short passwords fall quickly.</li>
<li><b>Phishing.</b> No password strength helps if you type it into a fake login page.</li></ul>
<h2>Length beats complexity</h2>
<p>Every extra character multiplies the work for an attacker. An 8-character password using all character types has about 52 bits of entropy; a 16-character lowercase-only password has about 75 bits — vastly stronger and easier to type. Current NIST guidance (SP 800-63B) reflects this: favour length, drop arbitrary composition rules and forced periodic changes, and screen against known-breached passwords.</p>
<h2>Use a password manager</h2>
<p>The single highest-impact step is a password manager: it generates a unique random password for every site, fills it only on the genuine domain (a strong anti-phishing defence) and syncs across devices. You then remember just one strong master passphrase. Our <a href="../../tools/password-generator/">password generator</a> can create both.</p>
<h2>Passphrases for the things you type</h2>
<p>For your master password and device logins, use five or more <em>randomly chosen</em> words — like <code>orbit-walnut-plasma-heron-tundra</code>. Chosen randomly (not a quote or lyric), that's roughly 65+ bits of entropy and far easier to remember than <code>xK#9qL!2</code>.</p>
<h2>Turn on two-factor authentication</h2>
<p>2FA means a stolen password alone isn't enough. From strongest to weakest:</p>
<ol><li><b>Passkeys / hardware security keys</b> (FIDO2/WebAuthn) — phishing-resistant by design.</li>
<li><b>Authenticator apps</b> (TOTP codes).</li>
<li><b>SMS codes</b> — better than nothing, but vulnerable to SIM-swap attacks.</li></ol>
<h2>Passkeys: the post-password future</h2>
<p>Passkeys replace passwords with a cryptographic key pair stored on your device or in your password manager. The site only ever sees a public key, so there's nothing reusable to steal in a breach and nothing to type into a phishing page. Major platforms support them; enable them wherever offered.</p>
<h2>For developers: storing passwords</h2>
<p>Never store plain text or fast hashes (MD5, SHA-256) of passwords. Use a slow, salted, memory-hard algorithm — Argon2id first, then scrypt or bcrypt — and check new passwords against breach corpora. Rate-limit login attempts and offer passkeys.</p>
<div class="callout"><b>Quick checklist:</b> password manager ✔ unique password everywhere ✔ 2FA on email, banking and work accounts ✔ passkeys where available ✔ breach alerts enabled ✔.</div>
"""),

dict(slug="base64-explained", title="Base64 Explained: What It Is, How It Works and When to Use It",
 desc="How Base64 encoding works bit by bit, why it adds 33% overhead, URL-safe Base64, data URIs, and the security myths to avoid.",
 cat="Developer", minutes=6, video=("8qkxeZmKmOY", "What is Base64?"),
 tools=["base64", "image-to-base64", "jwt-decoder"],
 body="""
<p>Base64 is everywhere once you start looking: email attachments, JSON Web Tokens, data URIs in CSS, basic-auth headers and API payloads carrying files. It solves one problem — moving binary data through channels designed for text — and it's worth understanding precisely so you use it correctly.</p>
<h2>How it works</h2>
<p>Base64 reads input in groups of 3 bytes (24 bits) and splits them into four 6-bit chunks. Each 6-bit value (0–63) maps to one character from a 64-character alphabet: <code>A–Z</code>, <code>a–z</code>, <code>0–9</code>, <code>+</code> and <code>/</code>. When the input length isn't a multiple of three, the output is padded with <code>=</code>.</p>
<pre><code>Text:      M        a        n
ASCII:     77       97       110
Bits:      01001101 01100001 01101110
6-bit:     010011 010110 000101 101110
Index:     19     22     5      46
Base64:    T      W      F      u        → "TWFu"</code></pre>
<p>Because 3 bytes become 4 characters, encoded data is about <b>33% larger</b> than the original — the price of text-safety.</p>
<h2>Variants</h2>
<ul><li><b>Standard (RFC 4648 §4)</b> — uses <code>+</code> and <code>/</code>, padded with <code>=</code>.</li>
<li><b>URL-safe (RFC 4648 §5)</b> — swaps in <code>-</code> and <code>_</code> so the result survives URLs and filenames; padding is often omitted. JWTs use this.</li>
<li><b>MIME</b> — standard alphabet, wrapped at 76 characters per line for email.</li></ul>
<h2>Good uses</h2>
<ul><li>Embedding small images or fonts directly in CSS/HTML as data URIs.</li>
<li>Sending binary files inside JSON APIs.</li>
<li>Encoding binary keys or certificates (PEM files are Base64 between header lines).</li></ul>
<h2>Bad uses and myths</h2>
<ul><li><b>“It's encrypted.”</b> No — Base64 is reversible by anyone. Basic-auth credentials in Base64 are effectively plain text, which is why they must only travel over HTTPS.</li>
<li><b>Large files in JSON.</b> The 33% overhead plus parsing cost adds up; use multipart uploads or pre-signed URLs for anything big.</li>
<li><b>Big data URIs.</b> They can't be cached separately and bloat HTML; keep them to tiny assets.</li></ul>
<h2>Unicode gotcha</h2>
<p>JavaScript's <code>btoa()</code> only accepts Latin-1 characters and throws on emoji or most non-European text. Encode to UTF-8 bytes first — our <a href="../../tools/base64/">Base64 tool</a> does this automatically.</p>
"""),

dict(slug="cron-jobs-explained", title="Cron Jobs Explained: Scheduling Tasks Like a Pro",
 desc="Understand crontab syntax, special strings, environment pitfalls, logging, time zones and modern alternatives to cron.",
 cat="Developer", minutes=7, video=("QZJ1drMQz1A", "Linux/Mac Tutorial: Cron Jobs — How to Schedule Commands with crontab (Corey Schafer)"),
 tools=["cron-explainer", "timestamp-converter"],
 body="""
<p>Cron has scheduled recurring work on Unix systems since the 1970s, and its syntax lives on in Kubernetes CronJobs, GitHub Actions schedules, cloud schedulers and countless job queues. Learn it once and you'll use it everywhere.</p>
<h2>Crontab syntax</h2>
<pre><code>┌───────── minute (0–59)
│ ┌─────── hour (0–23)
│ │ ┌───── day of month (1–31)
│ │ │ ┌─── month (1–12 or JAN–DEC)
│ │ │ │ ┌─ day of week (0–7 or SUN–SAT; 0 and 7 = Sunday)
│ │ │ │ │
* * * * *  command-to-run</code></pre>
<p>Edit your user's schedule with <code>crontab -e</code> and list it with <code>crontab -l</code>.</p>
<h2>Patterns you'll reuse</h2>
<table><tr><th>Expression</th><th>Runs</th></tr>
<tr><td><code>*/5 * * * *</code></td><td>Every 5 minutes</td></tr>
<tr><td><code>0 * * * *</code></td><td>Every hour, on the hour</td></tr>
<tr><td><code>30 2 * * *</code></td><td>Daily at 02:30</td></tr>
<tr><td><code>0 9 * * 1-5</code></td><td>Weekdays at 09:00</td></tr>
<tr><td><code>0 0 1 * *</code></td><td>Midnight on the 1st of each month</td></tr>
<tr><td><code>@reboot</code></td><td>Once at startup</td></tr></table>
<p>Paste any expression into the <a href="../../tools/cron-explainer/">cron explainer</a> to see it in plain English with the next run times.</p>
<h2>The pitfalls that bite everyone</h2>
<ul><li><b>Minimal environment.</b> Cron runs with a tiny <code>PATH</code> and none of your shell profile. Use absolute paths (<code>/usr/bin/python3</code>) or set <code>PATH</code> at the top of the crontab.</li>
<li><b>Silent failures.</b> Output is mailed locally or discarded. Redirect it: <code>... &gt;&gt; /var/log/backup.log 2&gt;&amp;1</code>.</li>
<li><b>Percent signs.</b> In crontab, <code>%</code> means newline — escape it as <code>\\%</code> (common with <code>date +%F</code>).</li>
<li><b>Overlapping runs.</b> If a job takes longer than its interval, copies pile up. Wrap it with <code>flock -n /tmp/job.lock</code>.</li>
<li><b>Day-of-month OR day-of-week.</b> When both are restricted, cron fires if <em>either</em> matches — not both.</li>
<li><b>Time zones and DST.</b> Jobs at 02:00–03:00 local time may skip or double-run on daylight-saving changes. Schedule critical jobs in UTC.</li></ul>
<h2>Monitoring</h2>
<p>A cron job that silently stops is worse than one that fails loudly. Have each job ping a heartbeat monitor on success; if the ping doesn't arrive on schedule, you get an alert.</p>
<h2>Beyond cron</h2>
<p>On modern Linux, <b>systemd timers</b> add logging, dependencies and catch-up for missed runs. In the cloud, Kubernetes CronJobs, AWS EventBridge Scheduler and GitHub Actions <code>schedule:</code> all accept cron syntax — though cloud schedulers usually evaluate it in UTC.</p>
"""),

dict(slug="linux-command-line-basics", title="Linux Command Line Basics: 30 Commands to Get Productive",
 desc="Navigate files, inspect logs, manage processes and permissions, and chain commands with pipes — a practical Linux terminal primer.",
 cat="Network & IT", minutes=10, video=("sWbUDq4S6Y8", "Introduction to Linux – Full Course for Beginners (freeCodeCamp.org)"),
 tools=["cron-explainer", "cidr-calculator", "hash-generator"],
 body="""
<p>Most of the internet runs on Linux: web servers, containers, cloud VMs, routers and Android phones. Even on macOS or Windows (via WSL), the same shell skills apply. You don't need to memorise hundreds of commands — around thirty cover almost everything a developer or IT pro does daily.</p>
<h2>Navigating the filesystem</h2>
<pre><code>pwd                 # where am I?
ls -lah             # list files, long format, human sizes, hidden files
cd /var/log         # change directory (cd ~ = home, cd - = previous)
mkdir -p a/b/c      # create nested directories
cp -r src dest      # copy (recursive for folders)
mv old new          # move or rename
rm -r folder        # delete — there is no recycle bin!
find . -name "*.log" -mtime -1   # files changed in last day</code></pre>
<h2>Reading and searching files</h2>
<pre><code>cat file            # print a file
less file           # page through (q to quit, / to search)
head -n 20 file     # first 20 lines
tail -f app.log     # follow a log live
grep -rin "error" . # recursive, case-insensitive search with line numbers
wc -l file          # count lines</code></pre>
<h2>Pipes and redirection: the superpower</h2>
<p>The pipe <code>|</code> sends one command's output into the next, letting small tools combine into powerful one-liners:</p>
<pre><code># top 10 IP addresses hitting a web server
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head
# save output, append, or discard errors
cmd &gt; out.txt     cmd &gt;&gt; out.txt     cmd 2&gt;/dev/null</code></pre>
<h2>Permissions</h2>
<p><code>ls -l</code> shows permissions like <code>-rwxr-x---</code>: read/write/execute for the owner, group and others. Change them with <code>chmod</code> (<code>chmod 755 script.sh</code> or <code>chmod +x script.sh</code>) and ownership with <code>chown user:group file</code>. Each octal digit is a sum: read 4 + write 2 + execute 1 — convert with our <a href="../../tools/number-base/">number base converter</a>.</p>
<h2>Processes and system health</h2>
<pre><code>top / htop          # live process view
ps aux | grep nginx # find a process
kill PID            # politely stop (kill -9 only as a last resort)
df -h               # disk space per filesystem
du -sh *            # size of each item here
free -h             # memory usage
systemctl status nginx   # service status (systemd)
journalctl -u nginx -f   # follow a service's logs</code></pre>
<h2>Networking</h2>
<pre><code>ip a                # your interfaces and IPs
ping -c 4 host      # reachability
curl -I https://example.com   # fetch headers only
dig example.com MX  # DNS lookup
ss -tulpn           # listening ports
ssh user@server     # remote login (use keys, not passwords)</code></pre>
<h2>Habits of efficient users</h2>
<ul><li>Press <b>Tab</b> to autocomplete and <b>Ctrl+R</b> to search history.</li>
<li>Read the manual: <code>man grep</code> or <code>grep --help</code>.</li>
<li>Use <code>sudo</code> only when needed, and double-check any <code>rm -rf</code>.</li>
<li>Automate repeat tasks with a shell script and schedule it with cron.</li></ul>
"""),

dict(slug="how-https-tls-works", title="How HTTPS and TLS Work: The Padlock, Explained",
 desc="What happens in a TLS handshake, how certificates and certificate authorities create trust, TLS 1.3 improvements and common HTTPS errors.",
 cat="Security", minutes=8, video=("0TLDTodL7Lc", "Transport Layer Security (TLS) — Computerphile"),
 tools=["dns-lookup", "http-status-codes", "hash-generator"],
 body="""
<p>The padlock in your browser means your connection uses HTTPS — HTTP carried inside TLS (Transport Layer Security). TLS gives three guarantees: <b>confidentiality</b> (eavesdroppers can't read the traffic), <b>integrity</b> (nobody can alter it in transit) and <b>authentication</b> (you're talking to the real owner of the domain). It does <em>not</em> mean the site itself is trustworthy — phishing sites get certificates too.</p>
<h2>The handshake in TLS 1.3</h2>
<ol><li><b>ClientHello.</b> Your browser sends supported cipher suites and a key share for an ephemeral Diffie-Hellman exchange.</li>
<li><b>ServerHello.</b> The server picks parameters and sends its own key share. Both sides can now derive shared session keys — without ever sending them over the wire.</li>
<li><b>Certificate and proof.</b> The server sends its certificate chain and signs the handshake with its private key, proving it controls the certificate.</li>
<li><b>Finished.</b> Both sides confirm the handshake wasn't tampered with, then encrypted application data flows.</li></ol>
<p>TLS 1.3 (RFC 8446) completes this in one round trip, removes obsolete algorithms, and makes forward secrecy mandatory: even if the server's private key leaks later, past sessions stay secret.</p>
<h2>Certificates and the chain of trust</h2>
<p>A certificate binds a domain name to a public key, signed by a Certificate Authority (CA). Your operating system or browser ships with a list of trusted root CAs; the server presents its own certificate plus intermediate certificates linking back to one of those roots. Free, automated CAs such as Let's Encrypt made HTTPS the default across the web. You can restrict which CAs may issue for your domain with a CAA record — check it with our <a href="../../tools/dns-lookup/">DNS lookup</a>.</p>
<h2>Common errors and what they mean</h2>
<table><tr><th>Error</th><th>Likely cause</th></tr>
<tr><td>Certificate expired</td><td>Renewal failed — automate it</td></tr>
<tr><td>Name mismatch</td><td>Certificate doesn't cover this hostname (e.g. missing www)</td></tr>
<tr><td>Untrusted issuer</td><td>Self-signed cert or missing intermediate</td></tr>
<tr><td>Mixed content</td><td>HTTPS page loading HTTP scripts or images</td></tr>
<tr><td>Clock errors</td><td>Device date/time is wrong</td></tr></table>
<h2>Hardening checklist for site owners</h2>
<ul><li>Redirect all HTTP to HTTPS with a 301.</li>
<li>Enable HSTS so browsers refuse plain HTTP in future.</li>
<li>Support TLS 1.2 and 1.3 only; disable older versions.</li>
<li>Automate certificate renewal and monitor expiry.</li>
<li>Fix mixed content — browsers increasingly block it outright.</li></ul>
"""),

dict(slug="ip-addresses-and-subnetting", title="IP Addresses and Subnetting Made Simple",
 desc="Understand IPv4 and IPv6, public vs private addresses, CIDR notation, subnet masks and how to size a subnet — with worked examples.",
 cat="Network & IT", minutes=9, video=("5WfiTHiU4x8", "What is an IP Address? // You SUCK at Subnetting // EP 1 (NetworkChuck)"),
 tools=["cidr-calculator", "what-is-my-ip", "number-base"],
 body="""
<p>Every device on a network needs an address. Understanding how those addresses are structured — and how networks are carved into subnets — is foundational for anyone working in IT, DevOps or cloud infrastructure.</p>
<h2>IPv4 in one paragraph</h2>
<p>An IPv4 address is 32 bits, written as four decimal octets: <code>192.168.1.10</code>. That allows about 4.3 billion addresses — far too few for today's internet, which is why we rely on NAT (many private devices sharing one public address) and are steadily adopting IPv6.</p>
<h2>Public vs private</h2>
<p>RFC 1918 reserves three ranges for private networks that are never routed on the public internet:</p>
<table><tr><th>Range</th><th>CIDR</th><th>Typical use</th></tr>
<tr><td>10.0.0.0 – 10.255.255.255</td><td>10.0.0.0/8</td><td>Enterprises, cloud VPCs</td></tr>
<tr><td>172.16.0.0 – 172.31.255.255</td><td>172.16.0.0/12</td><td>Docker, mid-size networks</td></tr>
<tr><td>192.168.0.0 – 192.168.255.255</td><td>192.168.0.0/16</td><td>Home and small-office routers</td></tr></table>
<p>Your router translates between these and the public address you can see with our <a href="../../tools/what-is-my-ip/">What Is My IP</a> tool.</p>
<h2>CIDR and subnet masks</h2>
<p>CIDR notation <code>192.168.1.0/24</code> says the first 24 bits identify the network and the remaining 8 bits identify hosts. The equivalent subnet mask is <code>255.255.255.0</code> — 24 ones followed by 8 zeros in binary. Hosts per subnet = 2<sup>(32 − prefix)</sup>, minus 2 reserved addresses (network and broadcast).</p>
<table><tr><th>Prefix</th><th>Mask</th><th>Usable hosts</th></tr>
<tr><td>/30</td><td>255.255.255.252</td><td>2</td></tr><tr><td>/28</td><td>255.255.255.240</td><td>14</td></tr>
<tr><td>/26</td><td>255.255.255.192</td><td>62</td></tr><tr><td>/24</td><td>255.255.255.0</td><td>254</td></tr>
<tr><td>/22</td><td>255.255.252.0</td><td>1,022</td></tr><tr><td>/16</td><td>255.255.0.0</td><td>65,534</td></tr></table>
<h2>Worked example</h2>
<p>You need four subnets of at least 50 hosts from <code>10.20.0.0/24</code>. 50 hosts needs 6 host bits (64 addresses, 62 usable), so each subnet is a /26: <code>10.20.0.0/26</code>, <code>.64/26</code>, <code>.128/26</code> and <code>.192/26</code>. Verify each in the <a href="../../tools/cidr-calculator/">subnet calculator</a>.</p>
<h2>Cloud planning tips</h2>
<ul><li>Pick a large, unusual private block for each VPC (e.g. 10.42.0.0/16) so future VPN or peering connections don't overlap.</li>
<li>Cloud providers reserve extra addresses per subnet — AWS reserves 5 — so size generously.</li>
<li>Kubernetes needs separate ranges for nodes, pods and services; pods consume addresses fast.</li></ul>
<h2>IPv6 essentials</h2>
<p>IPv6 addresses are 128 bits written in hex groups: <code>2001:db8:85a3::8a2e:370:7334</code> (<code>::</code> compresses consecutive zero groups). The standard subnet for a LAN is a /64 — 18 quintillion addresses — so the scarcity mindset of IPv4 simply doesn't apply.</p>
"""),
]
