/* NBA Hardwood Dog Tags — site behavior. No trackers, no cookies, no third-party scripts. */
const FALLBACK_EMAIL = "scott.tischler@gmail.com"; // reservations open the visitor's own email app until a form endpoint exists
const FORM_ENDPOINT = ""; // optional: a Cloudflare Worker URL that accepts JSON reservations
const KICKSTARTER_URL = ""; // paste the live campaign link here when published

(function () {
  const nav = document.querySelector(".nav");
  const onScroll = () => nav && nav.classList.toggle("solid", window.scrollY > 40);
  onScroll(); window.addEventListener("scroll", onScroll, { passive: true });
  const burger = document.querySelector(".burger"), links = document.querySelector(".links");
  if (burger && links) {
    burger.addEventListener("click", () => { const o = links.classList.toggle("open"); burger.setAttribute("aria-expanded", o); document.body.style.overflow = o ? "hidden" : ""; });
    links.addEventListener("click", (e) => { if (e.target.tagName === "A") { links.classList.remove("open"); document.body.style.overflow = ""; } });
  }
  const items = document.querySelectorAll(".rv");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    items.forEach((el) => io.observe(el));
  } else items.forEach((el) => el.classList.add("in"));

  // team grid: conference filter, finish, search
  const grid = document.getElementById("teamGrid");
  if (grid) {
    let conf = "all", fin = "gold", q = "";
    const cards = [...grid.querySelectorAll(".tcard")];
    const draw = () => cards.forEach((c) => {
      const ok = (conf === "all" || c.dataset.conf === conf) && (!q || c.dataset.name.includes(q));
      c.classList.toggle("hide", !ok);
      const img = c.querySelector("img"); const want = c.dataset.img + "-" + fin + ".jpg";
      if (!img.getAttribute("src").endsWith(want)) img.src = "img/renders/" + want;
      c.href = "preorder.html?team=" + c.dataset.slug + "&finish=" + fin;
      c.querySelector("span").textContent = fin === "gold" ? "24K Gold" : fin[0].toUpperCase() + fin.slice(1);
    });
    const seg = (id, key, cb) => { const el = document.getElementById(id); if (!el) return; el.addEventListener("click", (e) => { const c = e.target.closest(".chip"); if (!c) return; el.querySelectorAll(".chip").forEach((x) => x.classList.remove("on")); c.classList.add("on"); cb(c.dataset[key]); draw(); }); };
    seg("confSeg", "f", (v) => (conf = v)); seg("finSeg", "fin", (v) => (fin = v));
    const s = document.getElementById("q"); if (s) s.addEventListener("input", () => { q = s.value.trim().toLowerCase(); draw(); });
    draw();
  }

  // lightbox (gallery)
  const lb = document.querySelector(".lb");
  if (lb) {
    const li = lb.querySelector("img"), lc = lb.querySelector("p"), close = () => lb.classList.remove("on");
    document.querySelectorAll(".mosaic figure").forEach((f) => f.addEventListener("click", () => { const i = f.querySelector("img"); li.src = i.dataset.full || i.src; li.alt = i.alt; lc.textContent = i.alt; lb.classList.add("on"); }));
    lb.addEventListener("click", close); document.addEventListener("keydown", (e) => e.key === "Escape" && close());
  }

  // reservation form
  const f = document.getElementById("reserve");
  if (f) {
    const T = window.TEAMS, FIN = { silver: "Silver", black: "Black", gold: "24K Gold" };
    const sel = document.getElementById("team"), fsel = document.getElementById("finish");
    sel.innerHTML = T.map((t) => `<option value="${t[1]}">${t[0]}</option>`).join("");
    const p = new URLSearchParams(location.search); // team + finish only; no personal data is ever put in a URL
    if (p.get("team") && T.some((t) => t[1] === p.get("team"))) sel.value = p.get("team");
    if (FIN[p.get("finish")]) fsel.value = p.get("finish");
    let qty = 1; const cart = [];
    const img = document.getElementById("rimg"), qn = document.getElementById("qty"), list = document.getElementById("cart"), tot = document.getElementById("tot");
    const render = () => {
      const t = T.find((x) => x[1] === sel.value); img.src = "img/renders/" + t[1] + "-" + fsel.value + ".jpg"; img.alt = t[0] + " — " + FIN[fsel.value] + " (concept render)"; qn.textContent = qty;
      list.innerHTML = cart.map((c, i) => `<li><span>${c.q} × ${c.team} — ${c.fin}</span><button type="button" data-i="${i}" aria-label="Remove">✕</button></li>`).join("");
      tot.textContent = cart.reduce((a, c) => a + c.q, 0);
    };
    sel.onchange = fsel.onchange = render;
    document.getElementById("minus").onclick = () => { qty = Math.max(1, qty - 1); render(); };
    document.getElementById("plus").onclick = () => { qty = Math.min(20, qty + 1); render(); };
    document.getElementById("add").onclick = () => { const t = T.find((x) => x[1] === sel.value), k = t[1] + fsel.value, h = cart.find((c) => c.k === k); if (h) h.q += qty; else cart.push({ k, team: t[0], fin: FIN[fsel.value], q: qty }); qty = 1; render(); };
    list.addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) { cart.splice(+b.dataset.i, 1); render(); } });
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!cart.length) { const t = T.find((x) => x[1] === sel.value); cart.push({ k: t[1] + fsel.value, team: t[0], fin: FIN[fsel.value], q: qty }); render(); }
      const d = new FormData(f), lines = cart.map((c) => `${c.q} x ${c.team} — ${c.fin}`).join("\n");
      const body = `Name: ${d.get("first")} ${d.get("last")}\nEmail: ${d.get("email")}\nMobile: ${d.get("phone") || "-"}\n\nReservation (no payment taken):\n${lines}`;
      const ok = document.getElementById("sent");
      if (FORM_ENDPOINT) { try { await fetch(FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ first: d.get("first"), last: d.get("last"), email: d.get("email"), phone: d.get("phone"), cart }) }); ok.hidden = false; return; } catch (_) {} }
      window.location.href = `mailto:${FALLBACK_EMAIL}?subject=${encodeURIComponent("NBA Hardwood Dog Tags reservation")}&body=${encodeURIComponent(body)}`;
      ok.hidden = false;
    });
    render();
  }

  // contact form
  const cf = document.getElementById("contactform");
  if (cf) cf.addEventListener("submit", (e) => { e.preventDefault(); const d = new FormData(cf); window.location.href = `mailto:${FALLBACK_EMAIL}?subject=${encodeURIComponent("NBA Hardwood Dog Tags — " + (d.get("topic") || "inquiry"))}&body=${encodeURIComponent(`Name: ${d.get("name")}\nEmail: ${d.get("email")}\n\n${d.get("message") || ""}`)}`; document.getElementById("sent").hidden = false; });

  // film: play when visible; sound on request
  document.querySelectorAll(".phone").forEach((box) => {
    const v = box.querySelector("video"), b = box.querySelector(".snd");
    if (b) b.addEventListener("click", () => { const on = v.muted; v.muted = !on; b.textContent = on ? "Sound on" : "Sound off"; b.setAttribute("aria-pressed", on); if (on) { v.currentTime = 0; v.play().catch(() => {}); } });
    if ("IntersectionObserver" in window) new IntersectionObserver((es) => es.forEach((e) => (e.isIntersecting ? v.play().catch(() => {}) : v.pause())), { threshold: 0.4 }).observe(box);
  });
})();
