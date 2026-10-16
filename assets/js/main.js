/* Tech.Tools — site runtime (no dependencies) */
(function () {
  "use strict";
  var ROOT = document.documentElement.getAttribute("data-root") || "";

  /* ---------- helpers ---------- */
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  var toastEl;
  window.TT = window.TT || {};
  TT.toast = function (msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove("show"); }, 1800);
  };
  TT.copy = function (text) {
    var done = function () { TT.toast("Copied to clipboard"); };
    if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(text).then(done, fallback); } else { fallback(); }
    function fallback() { var t = document.createElement("textarea"); t.value = text; t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); try { document.execCommand("copy"); done(); } catch (e) { TT.toast("Copy failed"); } t.remove(); }
  };
  TT.download = function (name, text, type) {
    var b = new Blob([text], { type: type || "text/plain" }); var a = document.createElement("a");
    a.href = URL.createObjectURL(b); a.download = name; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  };
  TT.esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };

  /* ---------- private contact route (never rendered in markup) ---------- */
  var _r = ["moc.liamg", "1askrowbew"];
  function route() { return _r[1].split("").reverse().join("") + "@" + _r[0].split("").reverse().join(""); }
  $$("[data-mail]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var subj = a.getAttribute("data-subject") || "Tech.Tools enquiry";
      window.location.href = "mai" + "lto:" + route() + "?subject=" + encodeURIComponent(subj);
    });
  });

  /* ---------- theme ---------- */
  var saved = store("tt-theme"); if (saved) document.documentElement.setAttribute("data-theme", saved);
  $$("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var cur = document.documentElement.getAttribute("data-theme");
      if (!cur) cur = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      var next = cur === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next); store("tt-theme", next);
    });
  });

  /* ---------- mobile nav ---------- */
  var mb = $(".menu-btn"), nl = $(".nav-links");
  if (mb && nl) mb.addEventListener("click", function () { var o = nl.classList.toggle("open"); mb.setAttribute("aria-expanded", o ? "true" : "false"); });

  /* ---------- quick search (Ctrl/Cmd+K) ---------- */
  var modal = $(".search-modal"), sInput = modal && $("input", modal), sRes = modal && $(".search-results", modal), sel = 0;
  function openSearch(q) { if (!modal) return; modal.classList.add("open"); sInput.value = q || ""; render(sInput.value); setTimeout(function () { sInput.focus(); }, 10); }
  function closeSearch() { if (modal) modal.classList.remove("open"); }
  function score(item, q) {
    var t = (item.t + " " + item.k + " " + item.c).toLowerCase(), s = 0;
    q.split(/\s+/).forEach(function (w) { if (!w) return; if (item.t.toLowerCase().indexOf(w) === 0) s += 5; if (item.t.toLowerCase().indexOf(w) > -1) s += 3; else if (t.indexOf(w) > -1) s += 1; else s -= 10; });
    return s;
  }
  function render(q) {
    var idx = window.TT_INDEX || []; q = (q || "").trim().toLowerCase();
    var list = q ? idx.map(function (i) { return { i: i, s: score(i, q) }; }).filter(function (x) { return x.s > 0; }).sort(function (a, b) { return b.s - a.s; }).map(function (x) { return x.i; }) : idx.filter(function (i) { return i.p; });
    list = list.slice(0, 12); sel = 0;
    sRes.innerHTML = list.length ? list.map(function (i, n) { return '<a href="' + ROOT + i.u + '"' + (n === 0 ? ' class="sel"' : "") + "><span>" + TT.esc(i.t) + "</span><small>" + TT.esc(i.c) + "</small></a>"; }).join("") : '<p class="muted" style="padding:12px">No match. Try “json”, “dns”, “password”…</p>';
  }
  if (modal) {
    sInput.addEventListener("input", function () { render(sInput.value); });
    sInput.addEventListener("keydown", function (e) {
      var links = $$("a", sRes); if (!links.length) return;
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); links[sel].classList.remove("sel"); sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + links.length) % links.length; links[sel].classList.add("sel"); links[sel].scrollIntoView({ block: "nearest" }); }
      if (e.key === "Enter") { e.preventDefault(); links[sel].click(); }
    });
    modal.addEventListener("click", function (e) { if (e.target === modal) closeSearch(); });
  }
  $$("[data-search-open]").forEach(function (b) { b.addEventListener("click", function () { openSearch(); }); });
  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); openSearch(); }
    if (e.key === "Escape") closeSearch();
  });
  var heroForm = $("#hero-search");
  if (heroForm) heroForm.addEventListener("submit", function (e) { e.preventDefault(); openSearch($("input", heroForm).value); });

  /* ---------- forms → private inbox via FormSubmit AJAX ---------- */
  $$("form[data-tt-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = $(".form-status", form) || (function () { var d = document.createElement("div"); d.className = "form-status"; form.appendChild(d); return d; })();
      if (form.querySelector("[name=_honey]") && form.querySelector("[name=_honey]").value) return;
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = {}; new FormData(form).forEach(function (v, k) { if (k === "_honey") return; data[k] = data[k] ? data[k] + ", " + v : v; });
      data._subject = "[Tech.Tools] " + (form.getAttribute("data-tt-form") || "Form") + " — " + (data.name || data.email || "new submission");
      data._template = "table"; data.page = location.href;
      var btn = $("button[type=submit]", form); if (btn) { btn.disabled = true; btn._t = btn.textContent; btn.textContent = "Sending…"; }
      fetch("https://formsubmit.co/ajax/" + route(), { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || j.success === "false") throw new Error("x"); }); })
        .then(function () {
          status.className = "form-status ok"; status.textContent = form.getAttribute("data-success") || "Thanks — we received your submission and will reply within 1 business day.";
          form.reset(); $$(".fstep", form).forEach(function (s, i) { s.classList.toggle("on", i === 0); }); stepBar(form, 0);
          if (typeof gtag === "function") gtag("event", "generate_lead", { form: form.getAttribute("data-tt-form") });
        })
        .catch(function () {
          status.className = "form-status err"; status.innerHTML = 'Could not send right now. <a href="#" data-mail-fallback>Email us instead</a>.';
          var f = $("[data-mail-fallback]", status); if (f) f.addEventListener("click", function (ev) { ev.preventDefault(); location.href = "mai" + "lto:" + route() + "?subject=" + encodeURIComponent(data._subject) + "&body=" + encodeURIComponent(Object.keys(data).filter(function (k) { return k[0] !== "_"; }).map(function (k) { return k + ": " + data[k]; }).join("\n")); });
        })
        .then(function () { if (btn) { btn.disabled = false; btn.textContent = btn._t; } });
    });
  });

  /* ---------- multi-step forms ---------- */
  function stepBar(form, n) { $$(".steps-bar span", form).forEach(function (s, i) { s.classList.toggle("on", i <= n); }); }
  $$("form[data-steps]").forEach(function (form) {
    var steps = $$(".fstep", form), cur = 0;
    function go(n) { steps[cur].classList.remove("on"); cur = n; steps[cur].classList.add("on"); stepBar(form, cur); var f = $("input,select,textarea", steps[cur]); if (f) f.focus({ preventScroll: true }); }
    $$("[data-next]", form).forEach(function (b) {
      b.addEventListener("click", function () {
        var bad = $$("input,select,textarea", steps[cur]).filter(function (f) { return !f.checkValidity(); });
        if (bad.length) { bad[0].reportValidity(); return; }
        if (cur < steps.length - 1) go(cur + 1);
      });
    });
    $$("[data-prev]", form).forEach(function (b) { b.addEventListener("click", function () { if (cur > 0) go(cur - 1); }); });
    stepBar(form, 0);
  });

  /* ---------- donation amount picker ---------- */
  $$(".amounts").forEach(function (g) {
    var target = document.getElementById(g.getAttribute("data-target"));
    $$("button", g).forEach(function (b) {
      b.addEventListener("click", function () { $$("button", g).forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on"); if (target) target.value = b.getAttribute("data-v"); });
    });
  });

  /* ---------- lite YouTube embeds (privacy-enhanced, loads on click) ---------- */
  $$(".video-lite").forEach(function (b) {
    var id = b.getAttribute("data-id");
    b.style.backgroundImage = "url(https://i.ytimg.com/vi/" + id + "/hqdefault.jpg)";
    b.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      f.title = b.getAttribute("aria-label") || "YouTube video"; f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"; f.allowFullscreen = true;
      b.replaceWith(f);
    });
  });

  /* ---------- directory / tools filters ---------- */
  $$("[data-filter-group]").forEach(function (g) {
    var scope = document.getElementById(g.getAttribute("data-filter-group")), q = document.querySelector('[data-filter-input="' + g.getAttribute("data-filter-group") + '"]'), active = "all";
    function apply() {
      var term = q ? q.value.trim().toLowerCase() : "";
      $$("[data-cat]", scope).forEach(function (el) {
        var okCat = active === "all" || el.getAttribute("data-cat") === active;
        var okQ = !term || el.textContent.toLowerCase().indexOf(term) > -1;
        el.classList.toggle("hidden", !(okCat && okQ));
      });
    }
    $$("button", g).forEach(function (b) { b.addEventListener("click", function () { $$("button", g).forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on"); active = b.getAttribute("data-f"); apply(); }); });
    if (q) q.addEventListener("input", apply);
  });

  /* ---------- sticky lead CTA after scroll ---------- */
  var sc = $(".sticky-cta");
  if (sc && !store("tt-cta-hide")) {
    window.addEventListener("scroll", function () { sc.classList.toggle("show", window.scrollY > 900); }, { passive: true });
    var x = $("[data-cta-close]", sc); if (x) x.addEventListener("click", function () { sc.remove(); store("tt-cta-hide", "1"); });
  }

  /* ---------- cookie notice ---------- */
  var ck = $(".cookie");
  if (ck && !store("tt-cookie")) {
    ck.classList.add("show");
    $$("[data-cookie]", ck).forEach(function (b) { b.addEventListener("click", function () { store("tt-cookie", b.getAttribute("data-cookie")); ck.classList.remove("show"); }); });
  }

  /* ---------- year ---------- */
  $$("[data-year]").forEach(function (e) { e.textContent = new Date().getFullYear(); });
})();
