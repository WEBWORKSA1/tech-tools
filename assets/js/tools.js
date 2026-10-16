/* Tech.Tools — tool runtime. Every tool runs 100% in the browser unless noted (IP & DNS lookups query public APIs). */
(function () {
  "use strict";
  var E = TT.esc;
  function el(root, s) { return root.querySelector(s); }
  function on(n, ev, fn) { n.addEventListener(ev, fn); }
  function btn(id, label, cls) { return '<button type="button" class="btn ' + (cls || "btn-ghost") + ' btn-sm" id="' + id + '">' + label + "</button>"; }
  function copyBtn(id) { return btn(id, "Copy"); }
  function bindCopy(root, id, getter) { on(el(root, "#" + id), "click", function () { TT.copy(getter()); }); }
  function utf8ToB64(s) { return btoa(unescape(encodeURIComponent(s))); }
  function b64ToUtf8(s) { return decodeURIComponent(escape(atob(s))); }
  function pad(n, w) { n = String(n); while (n.length < (w || 2)) n = "0" + n; return n; }
  function rnd(n) { var a = new Uint32Array(n); crypto.getRandomValues(a); return a; }

  /* --- compact MD5 (RFC 1321) --- */
  function md5(str) {
    function rl(x, c) { return (x << c) | (x >>> (32 - c)); }
    function add(x, y) { var l = (x & 0xffff) + (y & 0xffff); return (((x >> 16) + (y >> 16) + (l >> 16)) << 16) | (l & 0xffff); }
    var bytes = new TextEncoder().encode(str), n = bytes.length, words = [];
    for (var i = 0; i < n; i++) words[i >> 2] |= bytes[i] << ((i % 4) * 8);
    words[n >> 2] |= 0x80 << ((n % 4) * 8);
    var nw = (((n + 8) >> 6) + 1) * 16; for (i = 0; i < nw; i++) words[i] = words[i] | 0;
    words[nw - 2] = n * 8;
    var S = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21], K = [];
    for (i = 0; i < 64; i++) K[i] = Math.floor(Math.abs(Math.sin(i + 1)) * 4294967296) | 0;
    var a0 = 0x67452301, b0 = 0xefcdab89 | 0, c0 = 0x98badcfe | 0, d0 = 0x10325476;
    for (var o = 0; o < nw; o += 16) {
      var A = a0, B = b0, C = c0, D = d0;
      for (i = 0; i < 64; i++) {
        var F, g, r = i >> 4;
        if (r === 0) { F = (B & C) | (~B & D); g = i; }
        else if (r === 1) { F = (D & B) | (~D & C); g = (5 * i + 1) % 16; }
        else if (r === 2) { F = B ^ C ^ D; g = (3 * i + 5) % 16; }
        else { F = C ^ (B | ~D); g = (7 * i) % 16; }
        var tmp = D; D = C; C = B;
        B = add(B, rl(add(add(A, F), add(K[i], words[o + g])), S[r * 4 + (i % 4)]));
        A = tmp;
      }
      a0 = add(a0, A); b0 = add(b0, B); c0 = add(c0, C); d0 = add(d0, D);
    }
    return [a0, b0, c0, d0].map(function (v) { var s = ""; for (var j = 0; j < 4; j++) s += pad(((v >>> (j * 8)) & 255).toString(16)); return s; }).join("");
  }
  window.TT_md5 = md5;

  var T = {};

  /* ===================== DEVELOPER ===================== */
  T["json-formatter"] = function (r) {
    r.innerHTML = '<label for="jin">Paste JSON</label><textarea id="jin" spellcheck="false" placeholder=\'{"name":"Tech.Tools","free":true}\'></textarea>' +
      '<div class="toolbar"><label style="margin:0;align-self:center">Indent</label><select id="jind" style="width:auto"><option value="2">2 spaces</option><option value="4">4 spaces</option><option value="tab">Tab</option></select>' +
      btn("jfmt", "Format / Beautify", "btn-primary") + btn("jmin", "Minify") + btn("jsort", "Sort keys") + btn("jsample", "Sample") + copyBtn("jcopy") + btn("jdl", "Download") + "</div>" +
      '<div id="jstat" class="form-note" aria-live="polite"></div><pre class="out" id="jout"></pre>';
    var inp = el(r, "#jin"), out = el(r, "#jout"), st = el(r, "#jstat");
    function sortKeys(v) { if (Array.isArray(v)) return v.map(sortKeys); if (v && typeof v === "object") { var o = {}; Object.keys(v).sort().forEach(function (k) { o[k] = sortKeys(v[k]); }); return o; } return v; }
    function run(mode) {
      var txt = inp.value.trim(); if (!txt) { st.textContent = "Paste some JSON first."; return; }
      try {
        var v = JSON.parse(txt); if (mode === "sort") v = sortKeys(v);
        var ind = el(r, "#jind").value; ind = ind === "tab" ? "\t" : +ind;
        out.textContent = mode === "min" ? JSON.stringify(v) : JSON.stringify(v, null, ind);
        st.innerHTML = '<span class="pill-ok">✓ Valid JSON</span> · ' + out.textContent.length.toLocaleString() + " chars";
      } catch (e) {
        var m = /line \d+/.test(e.message) ? null : /position (\d+)/.exec(e.message), extra = "";
        if (m) { var p = +m[1], pre = txt.slice(0, p), line = pre.split("\n").length, col = p - pre.lastIndexOf("\n"); extra = " (line " + line + ", column " + col + ")"; }
        st.innerHTML = '<span class="pill-bad">✗ Invalid JSON</span> — ' + E(e.message) + extra; out.textContent = "";
      }
    }
    on(el(r, "#jfmt"), "click", function () { run("fmt"); }); on(el(r, "#jmin"), "click", function () { run("min"); }); on(el(r, "#jsort"), "click", function () { run("sort"); });
    on(el(r, "#jsample"), "click", function () { inp.value = '{"site":"Tech.Tools","tools":38,"private":true,"categories":["developer","network","security"],"owner":{"type":"independent","since":2026}}'; run("fmt"); });
    bindCopy(r, "jcopy", function () { return out.textContent; });
    on(el(r, "#jdl"), "click", function () { TT.download("formatted.json", out.textContent || inp.value, "application/json"); });
  };

  T["base64"] = function (r) {
    r.innerHTML = '<label for="bin">Input</label><textarea id="bin" placeholder="Text or Base64…"></textarea>' +
      '<div class="toolbar">' + btn("benc", "Encode →", "btn-primary") + btn("bdec", "← Decode") + '<label class="check" style="margin:0;align-self:center"><input type="checkbox" id="burl"> URL-safe</label>' + copyBtn("bcopy") + "</div>" +
      '<label for="bfile">…or encode a file</label><input type="file" id="bfile"><div id="bstat" class="form-note"></div><pre class="out" id="bout"></pre>';
    var i = el(r, "#bin"), o = el(r, "#bout"), s = el(r, "#bstat");
    on(el(r, "#benc"), "click", function () { var v = utf8ToB64(i.value); if (el(r, "#burl").checked) v = v.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); o.textContent = v; s.textContent = "Encoded " + i.value.length + " chars → " + v.length; });
    on(el(r, "#bdec"), "click", function () { try { var v = i.value.trim().replace(/-/g, "+").replace(/_/g, "/"); while (v.length % 4) v += "="; o.textContent = b64ToUtf8(v); s.textContent = "Decoded OK"; } catch (e) { s.innerHTML = '<span class="pill-bad">Not valid Base64 (or not UTF-8 text)</span>'; } });
    on(el(r, "#bfile"), "change", function (e) { var f = e.target.files[0]; if (!f) return; var fr = new FileReader(); fr.onload = function () { o.textContent = fr.result; s.textContent = f.name + " · " + (f.size / 1024).toFixed(1) + " KB → data URI"; }; fr.readAsDataURL(f); });
    bindCopy(r, "bcopy", function () { return o.textContent; });
  };

  T["url-encoder"] = function (r) {
    r.innerHTML = '<label for="uin">Input</label><textarea id="uin" placeholder="https://example.com/search?q=tech tools&lang=en"></textarea>' +
      '<div class="toolbar">' + btn("uenc", "Encode component", "btn-primary") + btn("uencu", "Encode full URL") + btn("udec", "Decode") + btn("uparse", "Parse URL") + copyBtn("ucopy") + "</div><pre class=\"out\" id=\"uout\"></pre>";
    var i = el(r, "#uin"), o = el(r, "#uout");
    on(el(r, "#uenc"), "click", function () { o.textContent = encodeURIComponent(i.value); });
    on(el(r, "#uencu"), "click", function () { o.textContent = encodeURI(i.value); });
    on(el(r, "#udec"), "click", function () { try { o.textContent = decodeURIComponent(i.value.replace(/\+/g, " ")); } catch (e) { o.textContent = "Malformed percent-encoding: " + e.message; } });
    on(el(r, "#uparse"), "click", function () { try { var u = new URL(i.value.trim()); var lines = ["protocol: " + u.protocol, "host: " + u.host, "pathname: " + u.pathname, "hash: " + u.hash, "query params:"]; u.searchParams.forEach(function (v, k) { lines.push("  " + k + " = " + v); }); o.textContent = lines.join("\n"); } catch (e) { o.textContent = "Not a valid absolute URL."; } });
    bindCopy(r, "ucopy", function () { return o.textContent; });
  };

  T["jwt-decoder"] = function (r) {
    r.innerHTML = '<label for="jwin">JWT</label><textarea id="jwin" placeholder="eyJhbGciOi…"></textarea><div class="toolbar">' + btn("jwdec", "Decode", "btn-primary") + btn("jwsample", "Sample") + '</div><div id="jwmeta" class="form-note"></div><div class="grid g2"><div><label>Header</label><pre class="out" id="jwh"></pre></div><div><label>Payload</label><pre class="out" id="jwp"></pre></div></div><p class="form-note">Signature is not verified — decoding happens locally and your token never leaves this page.</p>';
    function part(s) { s = s.replace(/-/g, "+").replace(/_/g, "/"); while (s.length % 4) s += "="; return JSON.parse(b64ToUtf8(s)); }
    function dec() {
      var t = el(r, "#jwin").value.trim(), m = el(r, "#jwmeta"); var p = t.split(".");
      if (p.length < 2) { m.innerHTML = '<span class="pill-bad">A JWT has 3 dot-separated parts.</span>'; return; }
      try {
        var h = part(p[0]), pl = part(p[1]); el(r, "#jwh").textContent = JSON.stringify(h, null, 2); el(r, "#jwp").textContent = JSON.stringify(pl, null, 2);
        var info = ["alg: " + (h.alg || "?")]; var now = Date.now() / 1000;
        if (pl.iat) info.push("issued " + new Date(pl.iat * 1000).toLocaleString());
        if (pl.exp) info.push((pl.exp < now ? '<span class="pill-bad">expired</span> ' : '<span class="pill-ok">valid until</span> ') + new Date(pl.exp * 1000).toLocaleString());
        m.innerHTML = info.join(" · ");
      } catch (e) { m.innerHTML = '<span class="pill-bad">Could not decode: ' + E(e.message) + "</span>"; }
    }
    on(el(r, "#jwdec"), "click", dec);
    on(el(r, "#jwsample"), "click", function () { var h = utf8ToB64('{"alg":"HS256","typ":"JWT"}').replace(/=+$/, ""), p = utf8ToB64(JSON.stringify({ sub: "1234567890", name: "Ada Lovelace", iat: Math.floor(Date.now() / 1000), exp: Math.floor(Date.now() / 1000) + 3600 })).replace(/=+$/, ""); el(r, "#jwin").value = h + "." + p + ".signature"; dec(); });
  };

  T["uuid-generator"] = function (r) {
    r.innerHTML = '<div class="row" style="display:grid;grid-template-columns:1fr 1fr;gap:12px"><div><label for="uv">Version</label><select id="uv"><option value="4">v4 (random)</option><option value="7">v7 (time-ordered)</option></select></div><div><label for="un">How many</label><input id="un" type="number" min="1" max="1000" value="5"></div></div>' +
      '<div class="toolbar"><label class="check" style="margin:0"><input type="checkbox" id="uup"> Uppercase</label><label class="check" style="margin:0"><input type="checkbox" id="unh"> No hyphens</label></div><div class="toolbar">' + btn("ugen", "Generate", "btn-primary") + copyBtn("ucp") + btn("udl", "Download .txt") + '</div><pre class="out" id="uo"></pre>';
    function hex(b) { return Array.prototype.map.call(b, function (x) { return pad(x.toString(16)); }).join(""); }
    function v4() { return crypto.randomUUID ? crypto.randomUUID() : fmt((function () { var b = crypto.getRandomValues(new Uint8Array(16)); b[6] = (b[6] & 15) | 64; b[8] = (b[8] & 63) | 128; return hex(b); })()); }
    function v7() { var b = crypto.getRandomValues(new Uint8Array(16)), ts = Date.now(); for (var i = 5; i >= 0; i--) { b[i] = ts % 256; ts = Math.floor(ts / 256); } b[6] = (b[6] & 15) | 112; b[8] = (b[8] & 63) | 128; return fmt(hex(b)); }
    function fmt(h) { return h.slice(0, 8) + "-" + h.slice(8, 12) + "-" + h.slice(12, 16) + "-" + h.slice(16, 20) + "-" + h.slice(20); }
    function gen() { var n = Math.min(1000, Math.max(1, +el(r, "#un").value || 1)), out = []; for (var i = 0; i < n; i++) { var u = el(r, "#uv").value === "7" ? v7() : v4(); if (el(r, "#unh").checked) u = u.replace(/-/g, ""); if (el(r, "#uup").checked) u = u.toUpperCase(); out.push(u); } el(r, "#uo").textContent = out.join("\n"); }
    on(el(r, "#ugen"), "click", gen); bindCopy(r, "ucp", function () { return el(r, "#uo").textContent; });
    on(el(r, "#udl"), "click", function () { TT.download("uuids.txt", el(r, "#uo").textContent); }); gen();
  };

  T["hash-generator"] = function (r) {
    r.innerHTML = '<label for="hin">Text to hash</label><textarea id="hin" placeholder="Type or paste text — hashes update live"></textarea><label class="check"><input type="checkbox" id="hup"> Uppercase output</label><dl class="kv" id="hout" style="margin-top:14px"></dl>';
    var algs = ["MD5", "SHA-1", "SHA-256", "SHA-384", "SHA-512"];
    function hx(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (b) { return pad(b.toString(16)); }).join(""); }
    function upd() {
      var t = el(r, "#hin").value, up = el(r, "#hup").checked, enc = new TextEncoder().encode(t);
      Promise.all(algs.map(function (a) { return a === "MD5" ? Promise.resolve(md5(t)) : crypto.subtle.digest(a, enc).then(hx); })).then(function (res) {
        el(r, "#hout").innerHTML = res.map(function (h, i) { h = up ? h.toUpperCase() : h; return "<dt>" + algs[i] + '</dt><dd><a href="#" data-h="' + h + '" title="Click to copy">' + h + "</a></dd>"; }).join("");
      });
    }
    on(el(r, "#hin"), "input", upd); on(el(r, "#hup"), "change", upd);
    on(el(r, "#hout"), "click", function (e) { var h = e.target.getAttribute("data-h"); if (h) { e.preventDefault(); TT.copy(h); } });
    if (!window.crypto || !crypto.subtle) el(r, "#hout").innerHTML = "<dd>SHA hashing needs HTTPS.</dd>"; else upd();
  };

  T["regex-tester"] = function (r) {
    r.innerHTML = '<div style="display:grid;grid-template-columns:1fr 120px;gap:12px"><div><label for="rx">Pattern</label><input id="rx" type="text" class="mono" value="\\b[\\w.+-]+@[\\w-]+\\.[\\w.]+\\b"></div><div><label for="rf">Flags</label><input id="rf" type="text" class="mono" value="g"></div></div>' +
      '<label for="rt" style="margin-top:12px">Test string</label><textarea id="rt">Contact sales@example.com or support@test.io — not a real@ address.</textarea>' +
      '<label for="rr">Replace with (optional)</label><input id="rr" type="text" class="mono" placeholder="$1, $&lt;name&gt;…"><div id="rs" class="form-note"></div><label>Matches</label><div class="out" id="rh"></div><label style="margin-top:12px">Groups / replace result</label><pre class="out" id="rg"></pre>';
    function upd() {
      var re, st = el(r, "#rs"), txt = el(r, "#rt").value, flags = el(r, "#rf").value;
      try { re = new RegExp(el(r, "#rx").value, flags.indexOf("g") > -1 ? flags : flags + "g"); } catch (e) { st.innerHTML = '<span class="pill-bad">' + E(e.message) + "</span>"; return; }
      var html = "", last = 0, groups = [], m, n = 0;
      while ((m = re.exec(txt)) && n < 5000) { n++; html += E(txt.slice(last, m.index)) + '<mark style="background:#fde68a;color:#111;border-radius:3px">' + E(m[0]) + "</mark>"; last = m.index + m[0].length; groups.push("#" + n + " @" + m.index + ": " + JSON.stringify(m.slice(1)) + (m.groups ? " " + JSON.stringify(m.groups) : "")); if (m[0] === "") re.lastIndex++; }
      el(r, "#rh").innerHTML = html + E(txt.slice(last));
      st.innerHTML = n ? '<span class="pill-ok">' + n + " match" + (n > 1 ? "es" : "") + "</span>" : "No matches";
      var rep = el(r, "#rr").value; el(r, "#rg").textContent = rep ? txt.replace(new RegExp(re.source, flags), rep) : groups.join("\n");
    }
    ["#rx", "#rf", "#rt", "#rr"].forEach(function (s) { on(el(r, s), "input", upd); }); upd();
  };

  T["timestamp-converter"] = function (r) {
    r.innerHTML = '<div class="card" style="margin-bottom:14px"><span class="muted">Current Unix time</span><div class="result-big mono" id="tnow"></div></div>' +
      '<div class="grid g2"><div><label for="tts">Unix timestamp (s or ms)</label><input id="tts" type="text" class="mono" placeholder="1760572800"><div class="toolbar">' + btn("t2d", "→ Date", "btn-primary") + '</div><dl class="kv" id="tdo"></dl></div>' +
      '<div><label for="tdt">Date &amp; time (local)</label><input id="tdt" type="datetime-local" step="1"><div class="toolbar">' + btn("d2t", "→ Timestamp", "btn-primary") + '</div><dl class="kv" id="tto"></dl></div></div>';
    setInterval(function () { el(r, "#tnow").textContent = Math.floor(Date.now() / 1000); }, 500); el(r, "#tnow").textContent = Math.floor(Date.now() / 1000);
    function rel(ms) { var d = (ms - Date.now()) / 1000, a = Math.abs(d), u = [[31536000, "year"], [2592000, "month"], [86400, "day"], [3600, "hour"], [60, "minute"], [1, "second"]]; for (var i = 0; i < u.length; i++) if (a >= u[i][0] || i === u.length - 1) { var v = Math.round(a / u[i][0]); return d < 0 ? v + " " + u[i][1] + (v !== 1 ? "s" : "") + " ago" : "in " + v + " " + u[i][1] + (v !== 1 ? "s" : ""); } }
    on(el(r, "#t2d"), "click", function () { var v = el(r, "#tts").value.trim(); if (!/^-?\d+$/.test(v)) { el(r, "#tdo").innerHTML = "<dd>Enter digits only.</dd>"; return; } var ms = v.length > 11 ? +v : +v * 1000, d = new Date(ms); el(r, "#tdo").innerHTML = "<dt>UTC</dt><dd>" + d.toUTCString() + "</dd><dt>Local</dt><dd>" + d.toLocaleString() + "</dd><dt>ISO 8601</dt><dd>" + d.toISOString() + "</dd><dt>Relative</dt><dd>" + rel(ms) + "</dd>"; });
    on(el(r, "#d2t"), "click", function () { var v = el(r, "#tdt").value; if (!v) return; var d = new Date(v); el(r, "#tto").innerHTML = "<dt>Seconds</dt><dd>" + Math.floor(d / 1000) + "</dd><dt>Milliseconds</dt><dd>" + d.getTime() + "</dd><dt>ISO 8601</dt><dd>" + d.toISOString() + "</dd>"; });
  };

  T["cron-explainer"] = function (r) {
    r.innerHTML = '<label for="cx">Cron expression (5 fields)</label><input id="cx" type="text" class="mono" value="*/15 9-17 * * 1-5" style="font-size:1.2rem"><div class="chips" style="margin:10px 0">' +
      ["* * * * *", "0 * * * *", "0 0 * * *", "0 9 * * 1-5", "*/5 * * * *", "0 0 1 * *", "30 2 * * 0"].map(function (c) { return '<button type="button" class="chip" data-c="' + c + '">' + c + "</button>"; }).join("") +
      '</div><div class="callout" id="cdesc"></div><label>Next 8 run times (your local time)</label><pre class="out" id="cnext"></pre>';
    var names = ["minute", "hour", "day-of-month", "month", "day-of-week"], ranges = [[0, 59], [0, 23], [1, 31], [1, 12], [0, 7]];
    var MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], DOW = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
    function parseField(f, i) {
      var set = {}, lo = ranges[i][0], hi = ranges[i][1];
      f = f.toUpperCase(); MON.forEach(function (m, k) { if (i === 3) f = f.replace(m, k + 1); }); DOW.forEach(function (d, k) { if (i === 4) f = f.replace(d, k); });
      f.split(",").forEach(function (part) {
        var m = /^(\*|\d+(?:-\d+)?)(?:\/(\d+))?$/.exec(part); if (!m) throw new Error("Bad " + names[i] + ' field "' + part + '"');
        var a = lo, b = hi, st = m[2] ? +m[2] : 1;
        if (m[1] !== "*") { var ab = m[1].split("-"); a = +ab[0]; b = ab[1] !== undefined ? +ab[1] : (m[2] ? hi : a); }
        if (a < lo || b > hi || a > b) throw new Error(names[i] + " out of range " + lo + "–" + hi);
        for (var x = a; x <= b; x += st) set[i === 4 && x === 7 ? 0 : x] = 1;
      });
      return set;
    }
    function describe(p) {
      function f(v, unit, plural) { if (v === "*") return "every " + unit; if (/^\*\/\d+$/.test(v)) return "every " + v.slice(2) + " " + plural; return plural + " " + v; }
      var d = [p[0] === "0" && p[1] !== "*" ? "At minute 0" : p[0] === "*" ? "Every minute" : /^\*\//.test(p[0]) ? "Every " + p[0].slice(2) + " minutes" : "At minute " + p[0]];
      if (p[1] !== "*") d.push(/^\*\//.test(p[1]) ? "every " + p[1].slice(2) + " hours" : "during hour(s) " + p[1]);
      if (p[2] !== "*") d.push("on day-of-month " + p[2]); if (p[3] !== "*") d.push("in month " + p[3]);
      if (p[4] !== "*") d.push("on weekday(s) " + p[4] + " (0 = Sunday)"); return d.join(", ") + ".";
    }
    function upd() {
      var parts = el(r, "#cx").value.trim().split(/\s+/);
      try {
        if (parts.length !== 5) throw new Error("Expected 5 fields, got " + parts.length);
        var s = parts.map(parseField); el(r, "#cdesc").textContent = describe(parts);
        var d = new Date(); d.setSeconds(0, 0); d.setMinutes(d.getMinutes() + 1); var res = [], guard = 0;
        var domStar = parts[2] === "*", dowStar = parts[4] === "*";
        while (res.length < 8 && guard++ < 600000) {
          var dayOk = domStar && dowStar ? true : domStar ? s[4][d.getDay()] : dowStar ? s[2][d.getDate()] : (s[2][d.getDate()] || s[4][d.getDay()]);
          if (s[3][d.getMonth() + 1] && dayOk && s[1][d.getHours()] && s[0][d.getMinutes()]) res.push(d.toLocaleString(undefined, { weekday: "short", year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }));
          d.setMinutes(d.getMinutes() + 1);
        }
        el(r, "#cnext").textContent = res.join("\n") || "No run in the next year.";
      } catch (e) { el(r, "#cdesc").innerHTML = '<span class="pill-bad">' + E(e.message) + "</span>"; el(r, "#cnext").textContent = ""; }
    }
    on(el(r, "#cx"), "input", upd); r.querySelectorAll("[data-c]").forEach(function (c) { on(c, "click", function () { el(r, "#cx").value = c.getAttribute("data-c"); upd(); }); }); upd();
  };

  T["diff-checker"] = function (r) {
    r.innerHTML = '<div class="grid g2"><div><label for="da">Original</label><textarea id="da">The quick brown fox\njumps over the lazy dog.\nTech tools save time.</textarea></div><div><label for="db">Changed</label><textarea id="db">The quick red fox\njumps over the lazy dog.\nGood tech tools save hours.</textarea></div></div>' +
      '<div class="toolbar">' + btn("dgo", "Compare lines", "btn-primary") + btn("dw", "Compare words") + '</div><div id="dst" class="form-note"></div><div class="out" id="dout" style="background:var(--surface-2);color:var(--ink);border:1px solid var(--line)"></div>';
    function lcs(a, b) {
      var n = a.length, m = b.length; if (n * m > 4e6) return null; var dp = []; for (var i = 0; i <= n; i++) dp.push(new Uint32Array(m + 1));
      for (i = n - 1; i >= 0; i--) for (var j = m - 1; j >= 0; j--) dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
      var out = []; i = 0; j = 0; while (i < n && j < m) { if (a[i] === b[j]) { out.push([0, a[i]]); i++; j++; } else if (dp[i + 1][j] >= dp[i][j + 1]) out.push([-1, a[i++]]); else out.push([1, b[j++]]); }
      while (i < n) out.push([-1, a[i++]]); while (j < m) out.push([1, b[j++]]); return out;
    }
    function run(words) {
      var A = el(r, "#da").value, B = el(r, "#db").value, sp = words ? /(\s+)/ : /\n/;
      var res = lcs(A.split(sp), B.split(sp)); if (!res) { el(r, "#dst").textContent = "Input too large for in-browser diff."; return; }
      var add = 0, del = 0;
      el(r, "#dout").innerHTML = res.map(function (x) { var t = E(x[1]); if (x[0] === 1) { add++; return '<span class="diff-add">' + (words ? t : "+ " + t) + "</span>"; } if (x[0] === -1) { del++; return '<span class="diff-del">' + (words ? t : "- " + t) + "</span>"; } return words ? t : "  " + t; }).join(words ? "" : "\n");
      el(r, "#dst").innerHTML = '<span class="pill-ok">+' + add + '</span> · <span class="pill-bad">−' + del + "</span> " + (words ? "words" : "lines");
    }
    on(el(r, "#dgo"), "click", function () { run(false); }); on(el(r, "#dw"), "click", function () { run(true); }); run(false);
  };

  T["html-entities"] = function (r) {
    r.innerHTML = '<label for="hein">Input</label><textarea id="hein">&lt;a href="/tools?a=1&b=2"&gt;Café &amp; “quotes”&lt;/a&gt;</textarea><div class="toolbar">' + btn("heenc", "Encode", "btn-primary") + btn("heall", "Encode non-ASCII too") + btn("hedec", "Decode") + copyBtn("hecp") + '</div><pre class="out" id="heout"></pre>';
    var i = el(r, "#hein"), o = el(r, "#heout");
    on(el(r, "#heenc"), "click", function () { o.textContent = E(i.value); });
    on(el(r, "#heall"), "click", function () { o.textContent = E(i.value).replace(/[^\x00-\x7f]/g, function (c) { return "&#" + c.codePointAt(0) + ";"; }); });
    on(el(r, "#hedec"), "click", function () { var t = document.createElement("textarea"); t.innerHTML = i.value; o.textContent = t.value; });
    bindCopy(r, "hecp", function () { return o.textContent; });
  };

  T["case-converter"] = function (r) {
    var cases = { "UPPER CASE": function (s) { return s.toUpperCase(); }, "lower case": function (s) { return s.toLowerCase(); }, "Title Case": function (s) { return s.toLowerCase().replace(/\b\w/g, function (c) { return c.toUpperCase(); }); }, "Sentence case": function (s) { return s.toLowerCase().replace(/(^\s*\w|[.!?]\s+\w)/g, function (c) { return c.toUpperCase(); }); },
      camelCase: function (s) { var w = words(s); return w.map(function (x, i) { return i ? cap(x) : x; }).join(""); }, PascalCase: function (s) { return words(s).map(cap).join(""); }, snake_case: function (s) { return words(s).join("_"); }, "kebab-case": function (s) { return words(s).join("-"); }, CONSTANT_CASE: function (s) { return words(s).join("_").toUpperCase(); }, "dot.case": function (s) { return words(s).join("."); } };
    function words(s) { return s.replace(/([a-z0-9])([A-Z])/g, "$1 $2").toLowerCase().split(/[^a-z0-9]+/).filter(Boolean); }
    function cap(x) { return x.charAt(0).toUpperCase() + x.slice(1); }
    r.innerHTML = '<label for="ccin">Text</label><textarea id="ccin" style="min-height:120px">tech tools make developerLife easier</textarea><div class="toolbar">' + Object.keys(cases).map(function (k, n) { return '<button type="button" class="btn btn-ghost btn-sm" data-k="' + n + '">' + k + "</button>"; }).join("") + "</div>" + '<pre class="out" id="ccout"></pre><div class="toolbar">' + copyBtn("cccp") + "</div>";
    var keys = Object.keys(cases);
    r.querySelectorAll("[data-k]").forEach(function (b) { on(b, "click", function () { el(r, "#ccout").textContent = cases[keys[+b.getAttribute("data-k")]](el(r, "#ccin").value); }); });
    bindCopy(r, "cccp", function () { return el(r, "#ccout").textContent; });
  };

  T["number-base"] = function (r) {
    var bases = [["Decimal", 10], ["Hexadecimal", 16], ["Binary", 2], ["Octal", 8], ["Base 36", 36]];
    r.innerHTML = '<p class="form-note">Type in any field — the others update instantly. Uses BigInt, so huge numbers work.</p>' + bases.map(function (b) { return '<div class="field"><label for="nb' + b[1] + '">' + b[0] + " (base " + b[1] + ')</label><input id="nb' + b[1] + '" type="text" class="mono" data-b="' + b[1] + '"></div>'; }).join("") + '<div id="nbs" class="form-note"></div>';
    function toBig(s, b) { s = s.trim().toLowerCase().replace(/^0[xbo]/, ""); if (!s) return null; var neg = s[0] === "-"; if (neg) s = s.slice(1); var v = 0n, B = BigInt(b); for (var i = 0; i < s.length; i++) { var d = parseInt(s[i], 36); if (isNaN(d) || d >= b) throw new Error('"' + s[i] + '" is not a base-' + b + " digit"); v = v * B + BigInt(d); } return neg ? -v : v; }
    r.querySelectorAll("[data-b]").forEach(function (inp) {
      on(inp, "input", function () { try { var v = toBig(inp.value, +inp.getAttribute("data-b")); el(r, "#nbs").textContent = ""; r.querySelectorAll("[data-b]").forEach(function (o) { if (o !== inp) o.value = v === null ? "" : v.toString(+o.getAttribute("data-b")); }); } catch (e) { el(r, "#nbs").innerHTML = '<span class="pill-bad">' + E(e.message) + "</span>"; } });
    });
    el(r, "#nb10").value = "255"; el(r, "#nb10").dispatchEvent(new Event("input"));
  };

  T["yaml-json"] = function (r) {
    r.innerHTML = '<div class="grid g2"><div><label for="yin">YAML</label><textarea id="yin" spellcheck="false">site: Tech.Tools\nfree: true\ncategories:\n  - developer\n  - network\nowner:\n  type: independent</textarea></div><div><label for="jyin">JSON</label><textarea id="jyin" spellcheck="false"></textarea></div></div><div class="toolbar">' + btn("y2j", "YAML → JSON", "btn-primary") + btn("j2y", "JSON → YAML") + '</div><div id="yst" class="form-note"></div>';
    function need(cb) { if (window.jsyaml) return cb(); var s = document.createElement("script"); s.src = "https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js"; s.onload = cb; s.onerror = function () { el(r, "#yst").textContent = "Could not load YAML parser — check your connection."; }; document.head.appendChild(s); }
    on(el(r, "#y2j"), "click", function () { need(function () { try { el(r, "#jyin").value = JSON.stringify(jsyaml.load(el(r, "#yin").value), null, 2); el(r, "#yst").innerHTML = '<span class="pill-ok">Converted</span>'; } catch (e) { el(r, "#yst").innerHTML = '<span class="pill-bad">' + E(e.message) + "</span>"; } }); });
    on(el(r, "#j2y"), "click", function () { need(function () { try { el(r, "#yin").value = jsyaml.dump(JSON.parse(el(r, "#jyin").value)); el(r, "#yst").innerHTML = '<span class="pill-ok">Converted</span>'; } catch (e) { el(r, "#yst").innerHTML = '<span class="pill-bad">' + E(e.message) + "</span>"; } }); });
  };

  T["json-to-csv"] = function (r) {
    r.innerHTML = '<label for="jcin">JSON array of objects — or CSV</label><textarea id="jcin" spellcheck="false">[{"tool":"JSON Formatter","category":"Developer","free":true},{"tool":"DNS Lookup","category":"Network","free":true}]</textarea><div class="toolbar">' + btn("j2c", "JSON → CSV", "btn-primary") + btn("c2j", "CSV → JSON") + copyBtn("jccp") + btn("jcdl", "Download") + '</div><div id="jcs" class="form-note"></div><pre class="out" id="jcout"></pre>';
    function cell(v) { if (v === null || v === undefined) return ""; if (typeof v === "object") v = JSON.stringify(v); v = String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
    function parseCSV(t) { var rows = [], row = [], f = "", q = false; for (var i = 0; i < t.length; i++) { var c = t[i]; if (q) { if (c === '"' && t[i + 1] === '"') { f += '"'; i++; } else if (c === '"') q = false; else f += c; } else if (c === '"') q = true; else if (c === ",") { row.push(f); f = ""; } else if (c === "\n" || c === "\r") { if (c === "\r" && t[i + 1] === "\n") i++; row.push(f); rows.push(row); row = []; f = ""; } else f += c; } if (f || row.length) { row.push(f); rows.push(row); } return rows; }
    on(el(r, "#j2c"), "click", function () { try { var a = JSON.parse(el(r, "#jcin").value); if (!Array.isArray(a)) a = [a]; var keys = []; a.forEach(function (o) { Object.keys(o).forEach(function (k) { if (keys.indexOf(k) < 0) keys.push(k); }); }); el(r, "#jcout").textContent = [keys.map(cell).join(",")].concat(a.map(function (o) { return keys.map(function (k) { return cell(o[k]); }).join(","); })).join("\n"); el(r, "#jcs").textContent = a.length + " rows × " + keys.length + " columns"; } catch (e) { el(r, "#jcs").innerHTML = '<span class="pill-bad">' + E(e.message) + "</span>"; } });
    on(el(r, "#c2j"), "click", function () { var rows = parseCSV(el(r, "#jcin").value.trim()); if (rows.length < 2) { el(r, "#jcs").textContent = "Need a header row plus data."; return; } var h = rows[0]; el(r, "#jcout").textContent = JSON.stringify(rows.slice(1).map(function (rw) { var o = {}; h.forEach(function (k, i) { o[k] = rw[i] === undefined ? "" : rw[i]; }); return o; }), null, 2); el(r, "#jcs").textContent = (rows.length - 1) + " records"; });
    bindCopy(r, "jccp", function () { return el(r, "#jcout").textContent; });
    on(el(r, "#jcdl"), "click", function () { var t = el(r, "#jcout").textContent; TT.download(t.trim()[0] === "[" ? "data.json" : "data.csv", t); });
  };

  /* ===================== SECURITY ===================== */
  T["password-generator"] = function (r) {
    r.innerHTML = '<div class="out" id="pgo" style="font-size:1.25rem;min-height:auto;text-align:center"></div><div class="meter" style="margin:10px 0"><span id="pgm"></span></div><div id="pgs" class="form-note"></div>' +
      '<div class="range-row"><label for="pgl" style="margin:0">Length <b id="pglv">20</b></label><input type="range" id="pgl" min="6" max="128" value="20"></div>' +
      '<div class="toolbar"><label class="check"><input type="checkbox" id="pgu" checked> A–Z</label><label class="check"><input type="checkbox" id="pgd" checked> a–z</label><label class="check"><input type="checkbox" id="pgn" checked> 0–9</label><label class="check"><input type="checkbox" id="pgy" checked> !@#$</label><label class="check"><input type="checkbox" id="pgx"> Exclude look-alikes (Il1O0)</label></div>' +
      '<div class="toolbar">' + btn("pgg", "Generate", "btn-primary") + copyBtn("pgc") + btn("pgp", "Passphrase") + "</div>";
    var WORDS = "acid,agent,alpha,amber,anchor,apple,arrow,atlas,azure,badge,bamboo,banjo,beacon,berry,bison,blaze,bloom,bolt,brave,breeze,brick,bronze,cable,cactus,canyon,cargo,cedar,chalk,cider,cliff,cobalt,comet,coral,cosmic,crane,crisp,cyber,delta,denim,dingo,drift,eagle,echo,ember,epoch,fable,falcon,fern,fiber,flint,forge,fossil,frost,galaxy,garnet,gecko,glacier,granite,gravity,harbor,hazel,helix,heron,indigo,iron,ivory,jade,jaguar,jungle,karma,kayak,kernel,koala,lagoon,laser,lemon,lotus,lunar,magnet,mango,maple,marble,meadow,meteor,mint,mosaic,nebula,neon,nickel,nova,oasis,ocean,onyx,orbit,otter,oxygen,panda,pepper,photon,pixel,plasma,pluto,polar,prism,pulse,quartz,quasar,radar,raven,reef,rocket,ruby,saffron,sage,salmon,sapphire,shadow,sierra,signal,silver,solar,sonic,spark,sphinx,spruce,stone,summit,tango,thunder,tiger,topaz,tundra,turbo,ultra,umber,vapor,velvet,vertex,violet,vortex,walnut,willow,wizard,xenon,yeti,zebra,zenith,zinc".split(",");
    function pick(n) { return rnd(1)[0] % n; }
    function score(pw, pool) { var bits = Math.round(pw.length * Math.log2(pool || 1)); var pct = Math.min(100, bits / 1.28), col = bits < 50 ? "var(--bad)" : bits < 80 ? "var(--accent)" : "var(--ok)"; el(r, "#pgm").style.width = pct + "%"; el(r, "#pgm").style.background = col; el(r, "#pgs").textContent = "≈ " + bits + " bits of entropy — " + (bits < 50 ? "weak" : bits < 80 ? "good" : "excellent"); }
    function gen() {
      var sets = [], L = +el(r, "#pgl").value; el(r, "#pglv").textContent = L;
      if (el(r, "#pgu").checked) sets.push("ABCDEFGHIJKLMNOPQRSTUVWXYZ"); if (el(r, "#pgd").checked) sets.push("abcdefghijklmnopqrstuvwxyz"); if (el(r, "#pgn").checked) sets.push("0123456789"); if (el(r, "#pgy").checked) sets.push("!@#$%^&*()-_=+[]{};:,.?/");
      if (!sets.length) { el(r, "#pgo").textContent = "Pick at least one character set"; return; }
      if (el(r, "#pgx").checked) sets = sets.map(function (s) { return s.replace(/[Il1O0o]/g, ""); });
      var all = sets.join(""), pw = sets.map(function (s) { return s[pick(s.length)]; });
      while (pw.length < L) pw.push(all[pick(all.length)]);
      for (var i = pw.length - 1; i > 0; i--) { var j = pick(i + 1), t = pw[i]; pw[i] = pw[j]; pw[j] = t; }
      el(r, "#pgo").textContent = pw.join("").slice(0, L); score(el(r, "#pgo").textContent, all.length);
    }
    on(el(r, "#pgg"), "click", gen); on(el(r, "#pgl"), "input", gen); r.querySelectorAll("input[type=checkbox]").forEach(function (c) { on(c, "change", gen); });
    on(el(r, "#pgp"), "click", function () { var w = []; for (var i = 0; i < 5; i++) w.push(WORDS[pick(WORDS.length)]); var p = w.join("-") + "-" + pick(100); el(r, "#pgo").textContent = p; var bits = Math.round(5 * Math.log2(WORDS.length) + Math.log2(100)); el(r, "#pgm").style.width = Math.min(100, bits / 1.28) + "%"; el(r, "#pgm").style.background = "var(--accent)"; el(r, "#pgs").textContent = "≈ " + bits + " bits — memorable 5-word passphrase"; });
    bindCopy(r, "pgc", function () { return el(r, "#pgo").textContent; }); gen();
  };

  T["password-strength"] = function (r) {
    r.innerHTML = '<label for="psin">Password (checked locally — never sent anywhere)</label><input id="psin" type="password" autocomplete="off" placeholder="Type a password"><label class="check" style="margin-top:8px"><input type="checkbox" id="psshow"> Show</label><div class="meter" style="margin:14px 0"><span id="psm"></span></div><div class="result-big" id="psv">—</div><dl class="kv" id="psk"></dl><ul id="pstips" style="margin-top:12px"></ul>';
    var COMMON = ["password", "123456", "qwerty", "letmein", "admin", "welcome", "iloveyou", "monkey", "dragon", "football", "abc123", "111111", "sunshine", "master", "login", "princess", "passw0rd", "starwars", "trustno1", "baseball"];
    function fmtT(s) { if (s < 1) return "instantly"; var u = [[3.15e9 * 1e6, "million+ years"], [3.15e7, "years"], [86400, "days"], [3600, "hours"], [60, "minutes"], [1, "seconds"]]; for (var i = 0; i < u.length; i++) if (s >= u[i][0]) return (i === 0 ? "" : Math.round(s / u[i][0]).toLocaleString() + " ") + u[i][1]; }
    function upd() {
      var p = el(r, "#psin").value, pool = 0, tips = [];
      if (/[a-z]/.test(p)) pool += 26; else tips.push("Add lowercase letters");
      if (/[A-Z]/.test(p)) pool += 26; else tips.push("Add uppercase letters");
      if (/\d/.test(p)) pool += 10; else tips.push("Add numbers");
      if (/[^A-Za-z0-9]/.test(p)) pool += 33; else tips.push("Add symbols");
      if (p.length < 14) tips.push("Use 14+ characters — length beats complexity");
      var bits = p.length * Math.log2(pool || 1), low = p.toLowerCase();
      if (COMMON.some(function (c) { return low.indexOf(c) > -1; })) { bits = Math.min(bits, 12); tips.unshift("Contains a very common password pattern"); }
      if (/(.)\1{2,}/.test(p)) { bits -= 8; tips.push("Avoid repeated characters"); }
      if (/(0123|1234|2345|3456|4567|5678|6789|abcd|qwer|asdf)/i.test(p)) { bits -= 10; tips.push("Avoid keyboard or number sequences"); }
      bits = Math.max(0, Math.round(bits));
      var lvl = bits < 28 ? ["Very weak", "var(--bad)"] : bits < 45 ? ["Weak", "var(--bad)"] : bits < 60 ? ["Fair", "var(--accent)"] : bits < 80 ? ["Strong", "var(--ok)"] : ["Very strong", "var(--ok)"];
      el(r, "#psm").style.width = Math.min(100, bits / 1.2) + "%"; el(r, "#psm").style.background = lvl[1]; el(r, "#psv").textContent = p ? lvl[0] : "—"; el(r, "#psv").style.color = lvl[1];
      var secs = Math.pow(2, bits) / 1e10;
      el(r, "#psk").innerHTML = p ? "<dt>Length</dt><dd>" + p.length + "</dd><dt>Entropy</dt><dd>≈ " + bits + " bits</dd><dt>Offline crack time*</dt><dd>" + fmtT(secs / 2) + "</dd>" : "";
      el(r, "#pstips").innerHTML = p ? tips.map(function (t) { return "<li>" + t + "</li>"; }).join("") + '<li class="muted" style="list-style:none;font-size:.82rem">*Estimate assumes 10 billion guesses/second against a fast hash.</li>' : "";
    }
    on(el(r, "#psin"), "input", upd); on(el(r, "#psshow"), "change", function () { el(r, "#psin").type = this.checked ? "text" : "password"; });
  };

  T["qr-generator"] = function (r) {
    r.innerHTML = '<div class="grid g2"><div><label for="qrin">Text or URL</label><textarea id="qrin" style="min-height:110px">https://tech.tools</textarea><div class="row" style="display:grid;grid-template-columns:1fr 1fr;gap:12px"><div><label for="qrs">Size</label><select id="qrs"><option>256</option><option selected>320</option><option>512</option><option>1024</option></select></div><div><label for="qre">Error correction</label><select id="qre"><option value="L">Low</option><option value="M" selected>Medium</option><option value="Q">Quartile</option><option value="H">High</option></select></div></div>' +
      '<div class="row" style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px"><div><label for="qrf">Foreground</label><input type="color" id="qrf" value="#0c1222"></div><div><label for="qrb">Background</label><input type="color" id="qrb" value="#ffffff"></div></div><div class="toolbar">' + btn("qrg", "Generate", "btn-primary") + btn("qrd", "Download PNG") + '</div></div><div class="center"><div id="qrbox" style="display:inline-block;padding:14px;background:#fff;border-radius:12px;border:1px solid var(--line)"></div><p class="form-note" id="qrst"></p></div></div>';
    function need(cb) { if (window.QRCode) return cb(); var s = document.createElement("script"); s.src = "https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"; s.onload = cb; s.onerror = function () { el(r, "#qrst").textContent = "Could not load QR library."; }; document.head.appendChild(s); }
    function gen() { need(function () { var b = el(r, "#qrbox"); b.innerHTML = ""; var sz = +el(r, "#qrs").value; try { new QRCode(b, { text: el(r, "#qrin").value || " ", width: sz, height: sz, colorDark: el(r, "#qrf").value, colorLight: el(r, "#qrb").value, correctLevel: QRCode.CorrectLevel[el(r, "#qre").value] }); el(r, "#qrst").textContent = "Scan to test before printing."; b.querySelectorAll("img,canvas").forEach(function (x) { x.style.maxWidth = "100%"; x.style.height = "auto"; }); } catch (e) { el(r, "#qrst").textContent = "Text too long for a QR code at this error-correction level."; } }); }
    on(el(r, "#qrg"), "click", gen);
    on(el(r, "#qrd"), "click", function () { var c = el(r, "#qrbox canvas"); if (!c) return; var a = document.createElement("a"); a.href = c.toDataURL("image/png"); a.download = "qr-code.png"; a.click(); });
    gen();
  };

  /* ===================== NETWORK ===================== */
  T["what-is-my-ip"] = function (r) {
    r.innerHTML = '<div class="card center"><span class="muted">Your public IP address</span><div class="result-big mono" id="ipv">Looking up…</div><div class="toolbar" style="justify-content:center">' + copyBtn("ipc") + '</div></div><dl class="kv" id="ipk" style="margin-top:16px"></dl><p class="form-note">Lookup uses the public ipify and ipapi.co services from your browser. We don\'t store it.</p>';
    fetch("https://api.ipify.org?format=json").then(function (x) { return x.json(); }).then(function (j) {
      el(r, "#ipv").textContent = j.ip;
      return fetch("https://ipapi.co/" + j.ip + "/json/").then(function (x) { return x.json(); }).then(function (g) {
        if (g.error) return;
        var rows = [["Version", j.ip.indexOf(":") > -1 ? "IPv6" : "IPv4"], ["City", g.city], ["Region", g.region], ["Country", g.country_name], ["Postal", g.postal], ["Time zone", g.timezone], ["ISP / Org", g.org], ["ASN", g.asn]];
        el(r, "#ipk").innerHTML = rows.filter(function (x) { return x[1]; }).map(function (x) { return "<dt>" + x[0] + "</dt><dd>" + E(x[1]) + "</dd>"; }).join("");
      });
    }).catch(function () { el(r, "#ipv").textContent = "Unavailable"; el(r, "#ipk").innerHTML = "<dd>An ad-blocker or network policy blocked the lookup.</dd>"; });
    bindCopy(r, "ipc", function () { return el(r, "#ipv").textContent; });
  };

  T["dns-lookup"] = function (r) {
    r.innerHTML = '<div style="display:grid;grid-template-columns:1fr 140px auto;gap:10px;align-items:end"><div><label for="dnd">Domain</label><input id="dnd" type="text" value="example.com" autocapitalize="off"></div><div><label for="dnt">Record</label><select id="dnt">' + ["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SOA", "CAA", "SRV", "PTR"].map(function (t) { return "<option>" + t + "</option>"; }).join("") + '</select></div><div>' + btn("dng", "Lookup", "btn-primary") + '</div></div><div class="toolbar">' + btn("dnall", "Check all common records") + '</div><div id="dns" class="form-note"></div><div id="dno"></div><p class="form-note">Queries Google Public DNS over HTTPS (dns.google) directly from your browser.</p>';
    var TYPES = { 1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR", 15: "MX", 16: "TXT", 28: "AAAA", 33: "SRV", 257: "CAA" };
    function q(name, type) { return fetch("https://dns.google/resolve?name=" + encodeURIComponent(name) + "&type=" + type).then(function (x) { return x.json(); }); }
    function table(type, j) { var a = j.Answer || []; if (!a.length) return "<h3>" + type + '</h3><p class="muted">No ' + type + " records" + (j.Status === 3 ? " (domain does not exist)" : "") + ".</p>"; return "<h3>" + type + '</h3><div class="prose" style="max-width:none"><table><tr><th>Name</th><th>Type</th><th>TTL</th><th>Data</th></tr>' + a.map(function (x) { return "<tr><td>" + E(x.name) + "</td><td>" + (TYPES[x.type] || x.type) + "</td><td>" + x.TTL + "</td><td class=\"mono\" style=\"word-break:break-all\">" + E(x.data) + "</td></tr>"; }).join("") + "</table></div>"; }
    function clean() { return el(r, "#dnd").value.trim().replace(/^https?:\/\//, "").replace(/\/.*$/, ""); }
    on(el(r, "#dng"), "click", function () { var d = clean(), t = el(r, "#dnt").value; el(r, "#dns").textContent = "Querying…"; q(d, t).then(function (j) { el(r, "#dns").textContent = ""; el(r, "#dno").innerHTML = table(t, j); }).catch(function () { el(r, "#dns").textContent = "Lookup failed — network blocked?"; }); });
    on(el(r, "#dnall"), "click", function () { var d = clean(), ts = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "CAA"]; el(r, "#dns").textContent = "Querying " + ts.length + " record types…"; Promise.all(ts.map(function (t) { return q(d, t).catch(function () { return {}; }); })).then(function (res) { el(r, "#dns").textContent = ""; el(r, "#dno").innerHTML = res.map(function (j, i) { return table(ts[i], j); }).join(""); }); });
    on(el(r, "#dnd"), "keydown", function (e) { if (e.key === "Enter") el(r, "#dng").click(); });
  };

  T["cidr-calculator"] = function (r) {
    r.innerHTML = '<label for="cin">IPv4 address / CIDR</label><input id="cin" type="text" class="mono" value="192.168.1.10/24" style="font-size:1.15rem"><div id="cst" class="form-note"></div><dl class="kv" id="cout" style="margin-top:12px"></dl><details style="margin-top:16px"><summary>CIDR cheat sheet</summary><div class="prose" style="max-width:none"><table id="ccheat"></table></div></details>';
    function ip2n(s) { var p = s.split("."); if (p.length !== 4 || p.some(function (x) { return !/^\d{1,3}$/.test(x) || +x > 255; })) throw new Error("Invalid IPv4 address"); return ((+p[0] << 24) >>> 0) + (+p[1] << 16) + (+p[2] << 8) + +p[3]; }
    function n2ip(n) { return [n >>> 24, (n >>> 16) & 255, (n >>> 8) & 255, n & 255].join("."); }
    function bin(n) { return [24, 16, 8, 0].map(function (s) { return pad(((n >>> s) & 255).toString(2), 8); }).join("."); }
    function upd() {
      try {
        var v = el(r, "#cin").value.trim().split("/"), ip = ip2n(v[0]), pre = v[1] === undefined ? 32 : +v[1]; if (!(pre >= 0 && pre <= 32)) throw new Error("Prefix must be 0–32");
        var mask = pre === 0 ? 0 : (0xffffffff << (32 - pre)) >>> 0, net = (ip & mask) >>> 0, bc = (net | (~mask >>> 0)) >>> 0, total = Math.pow(2, 32 - pre);
        var hosts = pre >= 31 ? total : total - 2, first = pre >= 31 ? net : net + 1, last = pre >= 31 ? bc : bc - 1, a = ip >>> 24;
        var cls = a < 128 ? "A" : a < 192 ? "B" : a < 224 ? "C" : a < 240 ? "D (multicast)" : "E", priv = (a === 10) || (a === 172 && ((ip >>> 16) & 255) >= 16 && ((ip >>> 16) & 255) <= 31) || (a === 192 && ((ip >>> 16) & 255) === 168);
        el(r, "#cst").textContent = "";
        el(r, "#cout").innerHTML = [["Network", n2ip(net) + "/" + pre], ["Subnet mask", n2ip(mask)], ["Wildcard", n2ip(~mask >>> 0)], ["Broadcast", n2ip(bc)], ["First host", n2ip(first)], ["Last host", n2ip(last)], ["Usable hosts", hosts.toLocaleString()], ["Total addresses", total.toLocaleString()], ["Class", cls], ["Scope", priv ? "Private (RFC 1918)" : a === 127 ? "Loopback" : "Public"], ["Binary mask", bin(mask)]].map(function (x) { return "<dt>" + x[0] + "</dt><dd>" + x[1] + "</dd>"; }).join("");
      } catch (e) { el(r, "#cst").innerHTML = '<span class="pill-bad">' + E(e.message) + "</span>"; }
    }
    on(el(r, "#cin"), "input", upd); upd();
    var rows = "<tr><th>CIDR</th><th>Mask</th><th>Usable hosts</th></tr>"; for (var p = 32; p >= 8; p--) { var m = p === 0 ? 0 : (0xffffffff << (32 - p)) >>> 0, t = Math.pow(2, 32 - p); rows += "<tr><td>/" + p + "</td><td>" + n2ip(m) + "</td><td>" + (p >= 31 ? t : t - 2).toLocaleString() + "</td></tr>"; }
    el(r, "#ccheat").innerHTML = rows;
  };

  T["browser-info"] = function (r) {
    r.innerHTML = '<label for="uain">User-Agent string</label><textarea id="uain" style="min-height:80px" class="mono"></textarea><div class="toolbar">' + btn("uap", "Parse", "btn-primary") + btn("uame", "Use my browser") + '</div><div class="grid g2"><div><h3>Parsed</h3><dl class="kv" id="uaout"></dl></div><div><h3>Your device</h3><dl class="kv" id="uadev"></dl></div></div>';
    function parse(ua) {
      var b = "Unknown", v = "", os = "Unknown", dev = /Mobi|Android|iPhone/i.test(ua) ? "Mobile" : /iPad|Tablet/i.test(ua) ? "Tablet" : "Desktop", m;
      if ((m = /Edg\/([\d.]+)/.exec(ua))) { b = "Microsoft Edge"; v = m[1]; } else if ((m = /OPR\/([\d.]+)/.exec(ua))) { b = "Opera"; v = m[1]; } else if ((m = /SamsungBrowser\/([\d.]+)/.exec(ua))) { b = "Samsung Internet"; v = m[1]; } else if ((m = /Firefox\/([\d.]+)/.exec(ua))) { b = "Firefox"; v = m[1]; } else if ((m = /Chrome\/([\d.]+)/.exec(ua))) { b = "Chrome"; v = m[1]; } else if ((m = /Version\/([\d.]+).*Safari/.exec(ua))) { b = "Safari"; v = m[1]; }
      if ((m = /Windows NT ([\d.]+)/.exec(ua))) os = "Windows " + ({ "10.0": "10/11", "6.3": "8.1", "6.1": "7" }[m[1]] || m[1]); else if ((m = /Android ([\d.]+)/.exec(ua))) os = "Android " + m[1]; else if ((m = /(iPhone|iPad).*OS ([\d_]+)/.exec(ua))) os = "iOS " + m[2].replace(/_/g, "."); else if ((m = /Mac OS X ([\d_]+)/.exec(ua))) os = "macOS " + m[1].replace(/_/g, "."); else if (/CrOS/.test(ua)) os = "ChromeOS"; else if (/Linux/.test(ua)) os = "Linux";
      var bot = /bot|crawl|spider|slurp/i.test(ua);
      return [["Browser", b + (v ? " " + v : "")], ["Engine", /Gecko\/\d/.test(ua) && /Firefox/.test(ua) ? "Gecko" : /AppleWebKit/.test(ua) ? (/Chrome|Edg|OPR/.test(ua) ? "Blink" : "WebKit") : "Unknown"], ["OS", os], ["Device", dev], ["Bot", bot ? "Yes" : "No"]];
    }
    function show() { el(r, "#uaout").innerHTML = parse(el(r, "#uain").value).map(function (x) { return "<dt>" + x[0] + "</dt><dd>" + E(x[1]) + "</dd>"; }).join(""); }
    el(r, "#uain").value = navigator.userAgent; show();
    on(el(r, "#uap"), "click", show); on(el(r, "#uame"), "click", function () { el(r, "#uain").value = navigator.userAgent; show(); });
    var d = [["Screen", screen.width + " × " + screen.height], ["Viewport", innerWidth + " × " + innerHeight], ["Pixel ratio", devicePixelRatio], ["Color depth", screen.colorDepth + "-bit"], ["Language", navigator.language], ["Time zone", Intl.DateTimeFormat().resolvedOptions().timeZone], ["CPU threads", navigator.hardwareConcurrency || "?"], ["Cookies", navigator.cookieEnabled ? "Enabled" : "Disabled"], ["Online", navigator.onLine ? "Yes" : "No"], ["Dark mode", matchMedia("(prefers-color-scheme: dark)").matches ? "Yes" : "No"], ["Touch", "ontouchstart" in window ? "Yes" : "No"]];
    el(r, "#uadev").innerHTML = d.map(function (x) { return "<dt>" + x[0] + "</dt><dd>" + E(x[1]) + "</dd>"; }).join("");
  };

  T["http-status-codes"] = function (r) {
    var C = [[100, "Continue", "Server received headers; client should send the body."], [101, "Switching Protocols", "Upgrading, e.g. to WebSocket."], [200, "OK", "Request succeeded."], [201, "Created", "A new resource was created (typical for POST)."], [202, "Accepted", "Accepted for processing, not completed yet."], [204, "No Content", "Success with no response body."], [206, "Partial Content", "Range request served (video streaming, resumable downloads)."], [301, "Moved Permanently", "Permanent redirect — passes SEO signals to the new URL."], [302, "Found", "Temporary redirect."], [304, "Not Modified", "Cached copy is still valid."], [307, "Temporary Redirect", "Temporary redirect that keeps the HTTP method."], [308, "Permanent Redirect", "Permanent redirect that keeps the HTTP method."], [400, "Bad Request", "Malformed syntax or invalid parameters."], [401, "Unauthorized", "Authentication required or failed."], [403, "Forbidden", "Authenticated but not allowed."], [404, "Not Found", "Resource does not exist."], [405, "Method Not Allowed", "HTTP verb not supported on this endpoint."], [408, "Request Timeout", "Client took too long to send the request."], [409, "Conflict", "Request conflicts with current state (e.g. version clash)."], [410, "Gone", "Removed permanently — tells search engines to drop it."], [413, "Content Too Large", "Payload exceeds server limits."], [415, "Unsupported Media Type", "Wrong Content-Type."], [418, "I'm a teapot", "April Fools' RFC 2324 joke, still widely recognised."], [422, "Unprocessable Content", "Well-formed but semantically invalid (validation errors)."], [429, "Too Many Requests", "Rate limit hit — check Retry-After."], [500, "Internal Server Error", "Generic server-side failure."], [501, "Not Implemented", "Server doesn't support the functionality."], [502, "Bad Gateway", "Upstream server returned an invalid response."], [503, "Service Unavailable", "Overloaded or down for maintenance."], [504, "Gateway Timeout", "Upstream server didn't respond in time."]];
    r.innerHTML = '<input type="search" id="hsq" placeholder="Search code or phrase, e.g. 404 or redirect"><div class="filters" style="margin-top:12px">' + ["all", "1", "2", "3", "4", "5"].map(function (f) { return '<button type="button" data-hf="' + f + '"' + (f === "all" ? ' class="on"' : "") + ">" + (f === "all" ? "All" : f + "xx") + "</button>"; }).join("") + '</div><div class="prose" style="max-width:none"><table><thead><tr><th>Code</th><th>Name</th><th>Meaning</th></tr></thead><tbody id="hsb"></tbody></table></div>';
    var cur = "all";
    function draw() { var q = el(r, "#hsq").value.toLowerCase(); el(r, "#hsb").innerHTML = C.filter(function (c) { return (cur === "all" || String(c[0])[0] === cur) && (!q || (c.join(" ").toLowerCase().indexOf(q) > -1)); }).map(function (c) { var col = c[0] < 300 ? "var(--ok)" : c[0] < 400 ? "var(--primary)" : c[0] < 500 ? "var(--warn)" : "var(--bad)"; return '<tr><td class="mono" style="color:' + col + ';font-weight:700">' + c[0] + "</td><td>" + c[1] + "</td><td>" + c[2] + "</td></tr>"; }).join(""); }
    on(el(r, "#hsq"), "input", draw); r.querySelectorAll("[data-hf]").forEach(function (b) { on(b, "click", function () { r.querySelectorAll("[data-hf]").forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on"); cur = b.getAttribute("data-hf"); draw(); }); }); draw();
  };

  /* ===================== WEB & SEO ===================== */
  T["meta-tag-generator"] = function (r) {
    r.innerHTML = '<div class="field"><label for="mtt">Page title <span class="muted" id="mttc"></span></label><input id="mtt" type="text" value="Free Online Developer Tools"></div><div class="field"><label for="mtd">Meta description <span class="muted" id="mtdc"></span></label><textarea id="mtd" style="min-height:80px">Format JSON, decode JWTs, look up DNS and more — free, fast, private tools that run in your browser.</textarea></div>' +
      '<div class="row" style="display:grid;grid-template-columns:1fr 1fr;gap:12px"><div class="field"><label for="mtu">Canonical URL</label><input id="mtu" type="url" value="https://example.com/"></div><div class="field"><label for="mti">Social image URL</label><input id="mti" type="url" placeholder="https://example.com/og.png"></div></div><label class="check"><input type="checkbox" id="mtn"> noindex (hide from search)</label>' +
      '<h3 style="margin-top:16px">Google preview</h3><div class="card" id="mtprev" style="font-family:arial,sans-serif"></div><h3 style="margin-top:16px">Code</h3><pre class="out" id="mto"></pre><div class="toolbar">' + copyBtn("mtc") + "</div>";
    function upd() {
      var t = el(r, "#mtt").value, d = el(r, "#mtd").value, u = el(r, "#mtu").value, im = el(r, "#mti").value;
      el(r, "#mttc").textContent = "(" + t.length + "/60)"; el(r, "#mttc").style.color = t.length > 60 ? "var(--bad)" : ""; el(r, "#mtdc").textContent = "(" + d.length + "/160)"; el(r, "#mtdc").style.color = d.length > 160 ? "var(--bad)" : "";
      el(r, "#mtprev").innerHTML = '<div style="color:var(--muted);font-size:.82rem">' + E(u) + '</div><div style="color:#1a0dab;font-size:1.2rem">' + E(t.length > 60 ? t.slice(0, 57) + "…" : t) + '</div><div style="font-size:.9rem;color:var(--ink-2)">' + E(d.length > 160 ? d.slice(0, 157) + "…" : d) + "</div>";
      var c = ['<title>' + E(t) + "</title>", '<meta name="description" content="' + E(d) + '">', '<link rel="canonical" href="' + E(u) + '">', el(r, "#mtn").checked ? '<meta name="robots" content="noindex,follow">' : '<meta name="robots" content="index,follow">', '<meta name="viewport" content="width=device-width, initial-scale=1">', "", "<!-- Open Graph -->", '<meta property="og:type" content="website">', '<meta property="og:title" content="' + E(t) + '">', '<meta property="og:description" content="' + E(d) + '">', '<meta property="og:url" content="' + E(u) + '">'];
      if (im) c.push('<meta property="og:image" content="' + E(im) + '">');
      c.push("", "<!-- Twitter / X -->", '<meta name="twitter:card" content="' + (im ? "summary_large_image" : "summary") + '">', '<meta name="twitter:title" content="' + E(t) + '">', '<meta name="twitter:description" content="' + E(d) + '">');
      if (im) c.push('<meta name="twitter:image" content="' + E(im) + '">');
      el(r, "#mto").textContent = c.join("\n");
    }
    r.querySelectorAll("input,textarea").forEach(function (i) { on(i, "input", upd); on(i, "change", upd); }); bindCopy(r, "mtc", function () { return el(r, "#mto").textContent; }); upd();
  };

  T["robots-txt-generator"] = function (r) {
    r.innerHTML = '<div class="field"><label for="rbd">Default for all bots</label><select id="rbd"><option value="allow">Allow everything</option><option value="disallow">Block everything</option></select></div><div class="field"><label for="rbx">Disallow paths (one per line)</label><textarea id="rbx" style="min-height:90px">/admin/\n/cart/\n/search?</textarea></div>' +
      '<div class="field"><label>Block AI training crawlers</label><div class="choice-grid">' + ["GPTBot", "Google-Extended", "CCBot", "ClaudeBot", "PerplexityBot", "Bytespider"].map(function (b) { return '<label class="choice"><input type="checkbox" value="' + b + '" data-bot> ' + b + "</label>"; }).join("") + '</div></div><div class="field"><label for="rbs">Sitemap URL</label><input id="rbs" type="url" value="https://example.com/sitemap.xml"></div><div class="field"><label for="rbc">Crawl-delay (seconds, optional)</label><input id="rbc" type="number" min="0" placeholder="(Google ignores this)"></div><pre class="out" id="rbo"></pre><div class="toolbar">' + copyBtn("rbcp") + btn("rbdl", "Download robots.txt") + "</div>";
    function upd() {
      var o = ["User-agent: *"]; if (el(r, "#rbd").value === "disallow") o.push("Disallow: /"); else { var p = el(r, "#rbx").value.split("\n").map(function (s) { return s.trim(); }).filter(Boolean); if (p.length) p.forEach(function (x) { o.push("Disallow: " + x); }); else o.push("Allow: /"); }
      if (el(r, "#rbc").value) o.push("Crawl-delay: " + el(r, "#rbc").value);
      r.querySelectorAll("[data-bot]:checked").forEach(function (b) { o.push("", "User-agent: " + b.value, "Disallow: /"); });
      if (el(r, "#rbs").value) o.push("", "Sitemap: " + el(r, "#rbs").value);
      el(r, "#rbo").textContent = o.join("\n");
    }
    r.querySelectorAll("input,textarea,select").forEach(function (i) { on(i, "input", upd); on(i, "change", upd); }); bindCopy(r, "rbcp", function () { return el(r, "#rbo").textContent; }); on(el(r, "#rbdl"), "click", function () { TT.download("robots.txt", el(r, "#rbo").textContent); }); upd();
  };

  T["utm-builder"] = function (r) {
    var f = [["utu", "Website URL *", "https://example.com/pricing"], ["uts", "utm_source *", "newsletter"], ["utm", "utm_medium *", "email"], ["utc", "utm_campaign *", "fall_launch"], ["utt", "utm_term", ""], ["utn", "utm_content", ""]];
    r.innerHTML = '<div class="grid g2">' + f.map(function (x) { return '<div class="field"><label for="' + x[0] + '">' + x[1] + '</label><input id="' + x[0] + '" type="text" value="' + x[2] + '"></div>'; }).join("") + '</div><label class="check"><input type="checkbox" id="utl" checked> Force lowercase &amp; replace spaces with _</label><label style="margin-top:14px">Campaign URL</label><div class="out" id="uto"></div><div class="toolbar">' + copyBtn("utcp") + "</div>";
    function upd() {
      var norm = el(r, "#utl").checked, base = el(r, "#utu").value.trim(); if (!base) { el(r, "#uto").textContent = ""; return; }
      try { var u = new URL(base); [["uts", "utm_source"], ["utm", "utm_medium"], ["utc", "utm_campaign"], ["utt", "utm_term"], ["utn", "utm_content"]].forEach(function (p) { var v = el(r, "#" + p[0]).value.trim(); if (norm) v = v.toLowerCase().replace(/\s+/g, "_"); if (v) u.searchParams.set(p[1], v); else u.searchParams.delete(p[1]); }); el(r, "#uto").textContent = u.toString(); } catch (e) { el(r, "#uto").textContent = "Enter a full URL including https://"; }
    }
    r.querySelectorAll("input").forEach(function (i) { on(i, "input", upd); on(i, "change", upd); }); bindCopy(r, "utcp", function () { return el(r, "#uto").textContent; }); upd();
  };

  /* ===================== TEXT ===================== */
  T["word-counter"] = function (r) {
    r.innerHTML = '<textarea id="wcin" style="min-height:240px;font-family:var(--font)" placeholder="Start typing or paste your text…"></textarea><div class="grid g4" style="margin-top:14px" id="wcs"></div><h3 style="margin-top:18px">Top keywords</h3><div class="chips" id="wck"></div>';
    var STOP = "the,a,an,and,or,but,of,to,in,on,for,with,is,are,was,were,be,it,this,that,as,at,by,from,you,your,we,our,i,not,can,will,if,so,do,has,have,they,their,its,than,then,into,about,more".split(",");
    function upd() {
      var t = el(r, "#wcin").value, w = t.match(/[\p{L}\p{N}'’-]+/gu) || [], sents = t.split(/[.!?]+(\s|$)/).filter(function (s) { return s && s.trim(); }).length, paras = t.split(/\n\s*\n/).filter(function (s) { return s.trim(); }).length;
      var stats = [["Words", w.length], ["Characters", t.length], ["No spaces", t.replace(/\s/g, "").length], ["Sentences", sents], ["Paragraphs", paras], ["Reading time", Math.max(w.length ? 1 : 0, Math.round(w.length / 238)) + " min"], ["Speaking time", Math.round(w.length / 150) + " min"], ["Avg word", w.length ? (w.join("").length / w.length).toFixed(1) + " ch" : "0"]];
      el(r, "#wcs").innerHTML = stats.map(function (s) { return '<div class="card" style="padding:14px"><div class="muted" style="font-size:.82rem">' + s[0] + '</div><div style="font-family:var(--display);font-size:1.5rem;font-weight:700">' + s[1] + "</div></div>"; }).join("");
      var f = {}; w.forEach(function (x) { x = x.toLowerCase(); if (x.length > 2 && STOP.indexOf(x) < 0) f[x] = (f[x] || 0) + 1; });
      el(r, "#wck").innerHTML = Object.keys(f).sort(function (a, b) { return f[b] - f[a]; }).slice(0, 12).map(function (k) { return '<span class="chip">' + E(k) + " · " + f[k] + " (" + (100 * f[k] / w.length).toFixed(1) + "%)</span>"; }).join("") || '<span class="muted">—</span>';
    }
    on(el(r, "#wcin"), "input", upd); upd();
  };

  T["lorem-ipsum"] = function (r) {
    var L = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum".split(" ");
    r.innerHTML = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px"><div><label for="lin">Amount</label><input id="lin" type="number" value="3" min="1" max="100"></div><div><label for="lu">Unit</label><select id="lu"><option value="p">Paragraphs</option><option value="s">Sentences</option><option value="w">Words</option></select></div></div><div class="toolbar"><label class="check"><input type="checkbox" id="lst" checked> Start with “Lorem ipsum…”</label><label class="check"><input type="checkbox" id="lh"> Wrap in &lt;p&gt; tags</label></div><div class="toolbar">' + btn("lg", "Generate", "btn-primary") + copyBtn("lc") + '</div><pre class="out" id="lo" style="font-family:var(--font)"></pre>';
    function w(n) { var o = []; for (var i = 0; i < n; i++) o.push(L[rnd(1)[0] % L.length]); return o; }
    function sent() { var s = w(8 + (rnd(1)[0] % 10)).join(" "); return s.charAt(0).toUpperCase() + s.slice(1) + "."; }
    function para() { var o = []; for (var i = 0, n = 4 + (rnd(1)[0] % 4); i < n; i++) o.push(sent()); return o.join(" "); }
    function gen() {
      var n = Math.min(100, Math.max(1, +el(r, "#lin").value || 1)), u = el(r, "#lu").value, out;
      if (u === "w") out = [w(n).join(" ")]; else if (u === "s") { out = []; for (var i = 0; i < n; i++) out.push(sent()); out = [out.join(" ")]; } else { out = []; for (i = 0; i < n; i++) out.push(para()); }
      if (el(r, "#lst").checked) out[0] = "Lorem ipsum dolor sit amet, " + out[0].charAt(0).toLowerCase() + out[0].slice(1);
      el(r, "#lo").textContent = el(r, "#lh").checked ? out.map(function (p) { return "<p>" + p + "</p>"; }).join("\n") : out.join("\n\n");
    }
    on(el(r, "#lg"), "click", gen); bindCopy(r, "lc", function () { return el(r, "#lo").textContent; }); gen();
  };

  T["text-cleaner"] = function (r) {
    var ops = { "Trim each line": function (t) { return t.split("\n").map(function (l) { return l.trim(); }).join("\n"); }, "Remove extra spaces": function (t) { return t.replace(/[ \t]+/g, " "); }, "Remove empty lines": function (t) { return t.split("\n").filter(function (l) { return l.trim(); }).join("\n"); }, "Remove duplicate lines": function (t) { var s = {}; return t.split("\n").filter(function (l) { if (s[l]) return false; s[l] = 1; return true; }).join("\n"); }, "Sort A→Z": function (t) { return t.split("\n").sort(function (a, b) { return a.localeCompare(b); }).join("\n"); }, "Sort Z→A": function (t) { return t.split("\n").sort(function (a, b) { return b.localeCompare(a); }).join("\n"); }, "Reverse lines": function (t) { return t.split("\n").reverse().join("\n"); }, "Join lines": function (t) { return t.split("\n").join(" "); }, "Strip HTML tags": function (t) { var d = document.createElement("div"); d.innerHTML = t; return d.textContent; }, "Smart → straight quotes": function (t) { return t.replace(/[“”]/g, '"').replace(/[‘’]/g, "'"); }, "Number lines": function (t) { return t.split("\n").map(function (l, i) { return (i + 1) + ". " + l; }).join("\n"); }, "Shuffle lines": function (t) { var a = t.split("\n"); for (var i = a.length - 1; i > 0; i--) { var j = rnd(1)[0] % (i + 1), x = a[i]; a[i] = a[j]; a[j] = x; } return a.join("\n"); } };
    var keys = Object.keys(ops);
    r.innerHTML = '<textarea id="tcin" style="font-family:var(--font)">  banana\napple   pie\n\napple   pie\n  cherry  </textarea><div class="toolbar">' + keys.map(function (k, i) { return '<button type="button" class="btn btn-ghost btn-sm" data-o="' + i + '">' + k + "</button>"; }).join("") + '</div><div class="toolbar">' + btn("tcu", "Undo") + copyBtn("tcc") + '</div><div id="tcs" class="form-note"></div>';
    var hist = [];
    r.querySelectorAll("[data-o]").forEach(function (b) { on(b, "click", function () { var t = el(r, "#tcin"); hist.push(t.value); t.value = ops[keys[+b.getAttribute("data-o")]](t.value); el(r, "#tcs").textContent = keys[+b.getAttribute("data-o")] + " applied · " + t.value.split("\n").length + " lines"; }); });
    on(el(r, "#tcu"), "click", function () { if (hist.length) el(r, "#tcin").value = hist.pop(); }); bindCopy(r, "tcc", function () { return el(r, "#tcin").value; });
  };

  /* ===================== DESIGN ===================== */
  function hexToRgb(h) { h = h.replace("#", ""); if (h.length === 3) h = h.split("").map(function (c) { return c + c; }).join(""); if (!/^[0-9a-f]{6}$/i.test(h)) return null; var n = parseInt(h, 16); return [n >> 16, (n >> 8) & 255, n & 255]; }
  function rgbToHex(c) { return "#" + c.map(function (x) { return pad(Math.round(x).toString(16)); }).join(""); }
  function rgbToHsl(c) { var r = c[0] / 255, g = c[1] / 255, b = c[2] / 255, mx = Math.max(r, g, b), mn = Math.min(r, g, b), h, s, l = (mx + mn) / 2; if (mx === mn) h = s = 0; else { var d = mx - mn; s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn); h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h /= 6; } return [Math.round(h * 360), Math.round(s * 100), Math.round(l * 100)]; }
  function hslToRgb(h, s, l) { s /= 100; l /= 100; var k = function (n) { return (n + h / 30) % 12; }, a = s * Math.min(l, 1 - l), f = function (n) { return l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1))); }; return [255 * f(0), 255 * f(8), 255 * f(4)]; }
  function lum(c) { var a = c.map(function (v) { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }); return .2126 * a[0] + .7152 * a[1] + .0722 * a[2]; }

  T["color-converter"] = function (r) {
    r.innerHTML = '<div style="display:grid;grid-template-columns:120px 1fr;gap:16px;align-items:start"><div><div class="swatch" id="ccsw"></div><input type="color" id="ccpick" value="#0284c7" style="width:100%;margin-top:8px;height:40px"></div><div><div class="field"><label for="cchex">HEX</label><input id="cchex" class="mono" type="text"></div><div class="field"><label for="ccrgb">RGB</label><input id="ccrgb" class="mono" type="text"></div><div class="field"><label for="cchsl">HSL</label><input id="cchsl" class="mono" type="text"></div></div></div><h3>Tints &amp; shades</h3><div id="ccsh" style="display:grid;grid-template-columns:repeat(9,1fr);gap:4px"></div><p class="form-note">Click any swatch to copy its HEX.</p>';
    function set(rgb, src) {
      var hex = rgbToHex(rgb), hsl = rgbToHsl(rgb); el(r, "#ccsw").style.background = hex;
      if (src !== "hex") el(r, "#cchex").value = hex; if (src !== "rgb") el(r, "#ccrgb").value = "rgb(" + rgb.map(Math.round).join(", ") + ")"; if (src !== "hsl") el(r, "#cchsl").value = "hsl(" + hsl[0] + ", " + hsl[1] + "%, " + hsl[2] + "%)"; if (src !== "pick") el(r, "#ccpick").value = hex;
      var out = ""; [95, 85, 72, 60, hsl[2], 40, 30, 20, 10].forEach(function (L) { var h = rgbToHex(hslToRgb(hsl[0], hsl[1], L)); out += '<button type="button" title="' + h + '" data-hex="' + h + '" style="height:46px;border:1px solid var(--line);border-radius:8px;background:' + h + ';cursor:pointer"></button>'; });
      el(r, "#ccsh").innerHTML = out;
    }
    on(el(r, "#cchex"), "input", function () { var c = hexToRgb(this.value.trim()); if (c) set(c, "hex"); });
    on(el(r, "#ccrgb"), "input", function () { var m = this.value.match(/\d+(\.\d+)?/g); if (m && m.length >= 3 && m.slice(0, 3).every(function (x) { return +x <= 255; })) set(m.slice(0, 3).map(Number), "rgb"); });
    on(el(r, "#cchsl"), "input", function () { var m = this.value.match(/\d+(\.\d+)?/g); if (m && m.length >= 3) set(hslToRgb(+m[0], +m[1], +m[2]), "hsl"); });
    on(el(r, "#ccpick"), "input", function () { set(hexToRgb(this.value), "pick"); });
    on(el(r, "#ccsh"), "click", function (e) { var h = e.target.getAttribute("data-hex"); if (h) TT.copy(h); });
    set(hexToRgb("#0284c7"));
  };

  T["contrast-checker"] = function (r) {
    r.innerHTML = '<div class="grid g2"><div><label for="ctf">Text color</label><div style="display:flex;gap:8px"><input type="color" id="ctfp" value="#0c1222"><input id="ctf" class="mono" type="text" value="#0c1222"></div></div><div><label for="ctb">Background</label><div style="display:flex;gap:8px"><input type="color" id="ctbp" value="#fde68a"><input id="ctb" class="mono" type="text" value="#fde68a"></div></div></div><div id="ctprev" class="card" style="margin-top:14px"><p style="font-size:1.6rem;font-weight:700;margin:0">Large heading text</p><p style="margin:.3em 0 0">Normal body text — the quick brown fox jumps over the lazy dog.</p></div><div class="result-big center" id="ctr" style="margin-top:14px"></div><div class="grid g4" id="ctg" style="margin-top:10px"></div><div class="toolbar">' + btn("ctsw", "Swap colors") + "</div>";
    function upd() {
      var f = hexToRgb(el(r, "#ctf").value.trim()), b = hexToRgb(el(r, "#ctb").value.trim()); if (!f || !b) return;
      var L1 = lum(f), L2 = lum(b), ratio = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
      el(r, "#ctprev").style.color = rgbToHex(f); el(r, "#ctprev").style.background = rgbToHex(b); el(r, "#ctr").textContent = ratio.toFixed(2) + " : 1";
      el(r, "#ctg").innerHTML = [["AA normal", 4.5], ["AA large", 3], ["AAA normal", 7], ["AAA large", 4.5]].map(function (x) { var ok = ratio >= x[1]; return '<div class="card center" style="padding:12px"><div class="muted" style="font-size:.82rem">' + x[0] + " (≥" + x[1] + ')</div><div class="' + (ok ? "pill-ok" : "pill-bad") + '">' + (ok ? "Pass" : "Fail") + "</div></div>"; }).join("");
    }
    [["#ctf", "#ctfp"], ["#ctb", "#ctbp"]].forEach(function (p) { on(el(r, p[0]), "input", function () { if (hexToRgb(this.value)) el(r, p[1]).value = rgbToHex(hexToRgb(this.value)); upd(); }); on(el(r, p[1]), "input", function () { el(r, p[0]).value = this.value; upd(); }); });
    on(el(r, "#ctsw"), "click", function () { var a = el(r, "#ctf").value; el(r, "#ctf").value = el(r, "#ctb").value; el(r, "#ctb").value = a; el(r, "#ctfp").value = rgbToHex(hexToRgb(el(r, "#ctf").value)); el(r, "#ctbp").value = rgbToHex(hexToRgb(el(r, "#ctb").value)); upd(); }); upd();
  };

  T["css-gradient-generator"] = function (r) {
    r.innerHTML = '<div class="swatch" id="gprev" style="height:180px"></div><div class="grid g3" style="margin-top:14px"><div><label for="gt">Type</label><select id="gt"><option value="linear">Linear</option><option value="radial">Radial</option><option value="conic">Conic</option></select></div><div><label for="ga">Angle <b id="gav">135</b>°</label><input type="range" id="ga" min="0" max="360" value="135"></div><div><label>Stops</label><div style="display:flex;gap:6px"><input type="color" id="g1" value="#0284c7"><input type="color" id="g2" value="#7c3aed"><input type="color" id="g3" value="#f59e0b"></div><label class="check"><input type="checkbox" id="g3on" checked> Use 3rd stop</label></div></div><div class="toolbar">' + btn("grnd", "Random", "btn-primary") + copyBtn("gcp") + '</div><pre class="out" id="gout"></pre>';
    function css() { var t = el(r, "#gt").value, a = el(r, "#ga").value, s = [el(r, "#g1").value, el(r, "#g2").value]; if (el(r, "#g3on").checked) s.push(el(r, "#g3").value); el(r, "#gav").textContent = a; return t === "linear" ? "linear-gradient(" + a + "deg, " + s.join(", ") + ")" : t === "radial" ? "radial-gradient(circle, " + s.join(", ") + ")" : "conic-gradient(from " + a + "deg, " + s.join(", ") + (s.length ? ", " + s[0] : "") + ")"; }
    function upd() { var c = css(); el(r, "#gprev").style.background = c; el(r, "#gout").textContent = "background: " + el(r, "#g1").value + ";\nbackground: " + c + ";"; }
    r.querySelectorAll("input,select").forEach(function (i) { on(i, "input", upd); on(i, "change", upd); });
    on(el(r, "#grnd"), "click", function () { ["#g1", "#g2", "#g3"].forEach(function (s) { el(r, s).value = rgbToHex(hslToRgb(rnd(1)[0] % 360, 60 + rnd(1)[0] % 35, 45 + rnd(1)[0] % 20)); }); el(r, "#ga").value = rnd(1)[0] % 360; upd(); });
    bindCopy(r, "gcp", function () { return el(r, "#gout").textContent; }); upd();
  };

  T["box-shadow-generator"] = function (r) {
    var S = [["bx", "Offset X", -50, 50, 0], ["by", "Offset Y", -50, 50, 12], ["bb", "Blur", 0, 100, 30], ["bs", "Spread", -30, 30, -6], ["bo", "Opacity %", 0, 100, 25]];
    r.innerHTML = '<div style="display:grid;place-items:center;height:220px;background:var(--bg-2);border-radius:14px"><div id="bsprev" style="width:150px;height:110px;background:var(--surface);border-radius:16px"></div></div><div class="grid g2" style="margin-top:14px">' + S.map(function (s) { return '<div><label for="' + s[0] + '">' + s[1] + ' <b id="' + s[0] + 'v">' + s[4] + '</b></label><input type="range" id="' + s[0] + '" min="' + s[2] + '" max="' + s[3] + '" value="' + s[4] + '"></div>'; }).join("") + '<div><label for="bcol">Shadow color</label><input type="color" id="bcol" value="#0c1222"> <label class="check" style="display:inline-flex"><input type="checkbox" id="bin"> Inset</label></div></div><pre class="out" id="bout"></pre><div class="toolbar">' + copyBtn("bcp") + "</div>";
    function upd() { var v = {}; S.forEach(function (s) { v[s[0]] = el(r, "#" + s[0]).value; el(r, "#" + s[0] + "v").textContent = v[s[0]]; }); var c = hexToRgb(el(r, "#bcol").value), val = (el(r, "#bin").checked ? "inset " : "") + v.bx + "px " + v.by + "px " + v.bb + "px " + v.bs + "px rgba(" + c.join(", ") + ", " + (v.bo / 100) + ")"; el(r, "#bsprev").style.boxShadow = val; el(r, "#bout").textContent = "box-shadow: " + val + ";"; }
    r.querySelectorAll("input").forEach(function (i) { on(i, "input", upd); on(i, "change", upd); }); bindCopy(r, "bcp", function () { return el(r, "#bout").textContent; }); upd();
  };

  T["image-compressor"] = function (r) {
    r.innerHTML = '<label for="icf">Choose images (JPG, PNG, WebP) — processed on your device</label><input type="file" id="icf" accept="image/*" multiple><div class="grid g3" style="margin-top:12px"><div><label for="icfmt">Output format</label><select id="icfmt"><option value="image/webp">WebP</option><option value="image/jpeg">JPEG</option><option value="image/png">PNG (lossless)</option></select></div><div><label for="icq">Quality <b id="icqv">75</b>%</label><input type="range" id="icq" min="10" max="100" value="75"></div><div><label for="icw">Max width (px)</label><input id="icw" type="number" placeholder="original" min="16"></div></div><div class="toolbar">' + btn("icgo", "Compress", "btn-primary") + '</div><div id="icout" class="grid g2"></div>';
    on(el(r, "#icq"), "input", function () { el(r, "#icqv").textContent = this.value; });
    on(el(r, "#icgo"), "click", function () {
      var files = el(r, "#icf").files, out = el(r, "#icout"); out.innerHTML = ""; if (!files.length) { out.innerHTML = '<p class="muted">Pick at least one image.</p>'; return; }
      Array.prototype.forEach.call(files, function (f) {
        var img = new Image(), url = URL.createObjectURL(f);
        img.onload = function () {
          var mw = +el(r, "#icw").value || img.naturalWidth, sc = Math.min(1, mw / img.naturalWidth), c = document.createElement("canvas"); c.width = Math.round(img.naturalWidth * sc); c.height = Math.round(img.naturalHeight * sc);
          var fmt = el(r, "#icfmt").value, ctx = c.getContext("2d"); if (fmt === "image/jpeg") { ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, c.width, c.height); } ctx.drawImage(img, 0, 0, c.width, c.height);
          c.toBlob(function (b) {
            var save = 100 - (100 * b.size / f.size), ext = fmt.split("/")[1].replace("jpeg", "jpg"), card = document.createElement("div"); card.className = "card";
            var o = URL.createObjectURL(b); card.innerHTML = '<img src="' + o + '" alt="" style="border-radius:8px;max-height:180px;object-fit:contain;width:100%;background:var(--bg-2)"><p style="margin:.6em 0"><b>' + E(f.name) + "</b><br>" + (f.size / 1024).toFixed(1) + " KB → " + (b.size / 1024).toFixed(1) + ' KB <span class="' + (save > 0 ? "pill-ok" : "pill-bad") + '">' + (save > 0 ? "−" : "+") + Math.abs(save).toFixed(0) + "%</span><br>" + c.width + "×" + c.height + '</p><a class="btn btn-primary btn-sm" download="' + E(f.name.replace(/\.\w+$/, "")) + "-min." + ext + '" href="' + o + '">Download</a>';
            out.appendChild(card); URL.revokeObjectURL(url);
          }, fmt, +el(r, "#icq").value / 100);
        };
        img.src = url;
      });
    });
  };

  T["image-to-base64"] = function (r) {
    r.innerHTML = '<label for="i64f">Choose an image</label><input type="file" id="i64f" accept="image/*"><div id="i64p" style="margin:12px 0"></div><div class="toolbar">' + btn("i64d", "Copy data URI", "btn-primary") + btn("i64c", "Copy CSS") + btn("i64h", "Copy &lt;img&gt;") + '</div><div id="i64s" class="form-note"></div><pre class="out" id="i64o" style="max-height:220px"></pre>';
    var uri = "";
    on(el(r, "#i64f"), "change", function (e) { var f = e.target.files[0]; if (!f) return; var fr = new FileReader(); fr.onload = function () { uri = fr.result; el(r, "#i64p").innerHTML = '<img src="' + uri + '" alt="preview" style="max-height:160px;border-radius:8px;border:1px solid var(--line)">'; el(r, "#i64o").textContent = uri; el(r, "#i64s").textContent = f.name + " · original " + (f.size / 1024).toFixed(1) + " KB → Base64 " + (uri.length / 1024).toFixed(1) + " KB (+" + Math.round(100 * (uri.length / f.size - 1)) + "%)"; }; fr.readAsDataURL(f); });
    on(el(r, "#i64d"), "click", function () { if (uri) TT.copy(uri); }); on(el(r, "#i64c"), "click", function () { if (uri) TT.copy("background-image: url(\"" + uri + "\");"); }); on(el(r, "#i64h"), "click", function () { if (uri) TT.copy('<img src="' + uri + '" alt="">'); });
  };

  /* ===================== CALCULATORS ===================== */
  T["data-size-converter"] = function (r) {
    var U = [["B", 1], ["KB", 1e3], ["MB", 1e6], ["GB", 1e9], ["TB", 1e12], ["PB", 1e15], ["KiB", 1024], ["MiB", Math.pow(1024, 2)], ["GiB", Math.pow(1024, 3)], ["TiB", Math.pow(1024, 4)], ["bit", 1 / 8], ["Mbit", 1e6 / 8], ["Gbit", 1e9 / 8]];
    r.innerHTML = '<div style="display:grid;grid-template-columns:1fr 140px;gap:12px"><div><label for="dsv">Value</label><input id="dsv" type="number" value="1" step="any"></div><div><label for="dsu">Unit</label><select id="dsu">' + U.map(function (u) { return "<option" + (u[0] === "GB" ? " selected" : "") + ">" + u[0] + "</option>"; }).join("") + '</select></div></div><div class="grid g3" id="dso" style="margin-top:14px"></div><p class="form-note">KB/MB/GB are decimal (SI, powers of 1000). KiB/MiB/GiB are binary (IEC, powers of 1024) — that\'s why a “1 TB” drive shows ~931 GiB.</p>';
    function upd() { var v = +el(r, "#dsv").value, f = U.filter(function (u) { return u[0] === el(r, "#dsu").value; })[0][1], bytes = v * f; el(r, "#dso").innerHTML = U.map(function (u) { var x = bytes / u[1]; return '<div class="card" style="padding:12px"><div class="muted" style="font-size:.8rem">' + u[0] + '</div><div class="mono" style="font-weight:600;word-break:break-all">' + (Math.abs(x) >= 1e15 || (x !== 0 && Math.abs(x) < 1e-6) ? x.toExponential(4) : +x.toPrecision(10)).toLocaleString(undefined, { maximumFractionDigits: 6 }) + "</div></div>"; }).join(""); }
    on(el(r, "#dsv"), "input", upd); on(el(r, "#dsu"), "change", upd); upd();
  };

  T["download-time-calculator"] = function (r) {
    r.innerHTML = '<div class="grid g2"><div><label for="dtz">File size</label><div style="display:flex;gap:8px"><input id="dtz" type="number" value="4.7" step="any"><select id="dtzu" style="width:110px"><option value="1e6">MB</option><option value="1e9" selected>GB</option><option value="1e12">TB</option></select></div></div><div><label for="dts">Connection speed</label><div style="display:flex;gap:8px"><input id="dts" type="number" value="100" step="any"><select id="dtsu" style="width:110px"><option value="1e6" selected>Mbps</option><option value="1e9">Gbps</option><option value="1e3">Kbps</option></select></div></div></div><label for="dto" style="margin-top:12px">Protocol overhead <b id="dtov">10</b>%</label><input type="range" id="dto" min="0" max="30" value="10" style="width:100%"><div class="card center" style="margin-top:14px"><span class="muted">Estimated time</span><div class="result-big" id="dtr"></div><div class="muted" id="dtr2"></div></div>';
    function fmt(s) { var h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = Math.round(s % 60); return (h ? h + "h " : "") + (h || m ? m + "m " : "") + x + "s"; }
    function upd() { var bits = +el(r, "#dtz").value * +el(r, "#dtzu").value * 8, bps = +el(r, "#dts").value * +el(r, "#dtsu").value * (1 - el(r, "#dto").value / 100); el(r, "#dtov").textContent = el(r, "#dto").value; if (!bps) return; var s = bits / bps; el(r, "#dtr").textContent = fmt(s); el(r, "#dtr2").textContent = "Effective throughput " + (bps / 8e6).toFixed(2) + " MB/s"; }
    r.querySelectorAll("input,select").forEach(function (i) { on(i, "input", upd); on(i, "change", upd); }); upd();
  };

  T["aspect-ratio-calculator"] = function (r) {
    r.innerHTML = '<div class="grid g2"><div><label for="arw">Width</label><input id="arw" type="number" value="1920"></div><div><label for="arh">Height</label><input id="arh" type="number" value="1080"></div></div><div class="card center" style="margin-top:12px"><span class="muted">Aspect ratio</span><div class="result-big" id="arr"></div></div><h3 style="margin-top:16px">Resize keeping ratio</h3><div class="grid g2"><div><label for="arnw">New width</label><input id="arnw" type="number" placeholder="e.g. 1280"></div><div><label for="arnh">New height</label><input id="arnh" type="number" placeholder="auto"></div></div><div class="chips" style="margin-top:14px">' + ["16:9", "4:3", "1:1", "21:9", "9:16", "3:2", "4:5"].map(function (x) { return '<button type="button" class="chip" data-ar="' + x + '">' + x + "</button>"; }).join("") + "</div>";
    function g(a, b) { return b ? g(b, a % b) : a; }
    function upd() { var w = +el(r, "#arw").value, h = +el(r, "#arh").value; if (w > 0 && h > 0) { var d = g(w, h); el(r, "#arr").textContent = w / d + ":" + h / d + "  (" + (w / h).toFixed(4) + ")"; } }
    on(el(r, "#arw"), "input", upd); on(el(r, "#arh"), "input", upd);
    on(el(r, "#arnw"), "input", function () { var w = +el(r, "#arw").value, h = +el(r, "#arh").value; el(r, "#arnh").value = this.value ? Math.round(this.value * h / w) : ""; });
    on(el(r, "#arnh"), "input", function () { var w = +el(r, "#arw").value, h = +el(r, "#arh").value; el(r, "#arnw").value = this.value ? Math.round(this.value * w / h) : ""; });
    r.querySelectorAll("[data-ar]").forEach(function (b) { on(b, "click", function () { var p = b.getAttribute("data-ar").split(":"); el(r, "#arh").value = Math.round(el(r, "#arw").value * p[1] / p[0]); upd(); }); }); upd();
  };

  /* ---------- boot ---------- */
  document.querySelectorAll("[data-tool]").forEach(function (n) {
    var id = n.getAttribute("data-tool");
    if (T[id]) { try { T[id](n); } catch (e) { n.innerHTML = '<p class="pill-bad">This tool failed to load: ' + E(e.message) + "</p>"; } }
    try { var rec = JSON.parse(localStorage.getItem("tt-recent") || "[]").filter(function (x) { return x !== id; }); rec.unshift(id); localStorage.setItem("tt-recent", JSON.stringify(rec.slice(0, 8))); } catch (e) {}
  });
  window.TT_TOOLS = T;
})();
