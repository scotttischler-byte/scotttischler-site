/* ============================================================
   scotttischler.com — consent + tracking loader
   ------------------------------------------------------------
   Privacy-first: NOTHING loads until the visitor accepts.
   Fill in the IDs below and analytics/pixels turn on automatically.
   Leave an ID blank to keep that tool off.
   ============================================================ */
(function () {
  var CONFIG = {
    ga4:        "",   // Google Analytics 4, e.g. "G-XXXXXXXXXX"
    metaPixel:  "",   // Meta (Facebook) Pixel ID, e.g. "123456789012345"
    googleAds:  "",   // Google Ads / gtag conversion ID, e.g. "AW-XXXXXXXXX"
    visitorSrc: ""    // Visitor-ID tool script URL (e.g. RB2B / Vector / Leadfeeder)
  };

  var KEY = "st_consent_v1";
  var choice = null;
  try { choice = localStorage.getItem(KEY); } catch (e) {}

  function loadScript(src, attrs) {
    var s = document.createElement("script");
    s.async = true; s.src = src;
    if (attrs) Object.keys(attrs).forEach(function (k) { s.setAttribute(k, attrs[k]); });
    document.head.appendChild(s);
    return s;
  }

  function enableTracking() {
    // Google Analytics 4 / Google Ads (gtag)
    var gaId = CONFIG.ga4 || CONFIG.googleAds;
    if (gaId) {
      loadScript("https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(gaId));
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      if (CONFIG.ga4) window.gtag("config", CONFIG.ga4, { anonymize_ip: true });
      if (CONFIG.googleAds) window.gtag("config", CONFIG.googleAds);
    }
    // Meta (Facebook) Pixel
    if (CONFIG.metaPixel) {
      !function (f, b, e, v, n, t, s) {
        if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
        if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = [];
        t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
      }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
      window.fbq("init", CONFIG.metaPixel);
      window.fbq("track", "PageView");
    }
    // Anonymous visitor-identification tool (B2B)
    if (CONFIG.visitorSrc) loadScript(CONFIG.visitorSrc);
  }

  function setChoice(val) {
    try { localStorage.setItem(KEY, val); } catch (e) {}
    var b = document.getElementById("st-consent");
    if (b) b.parentNode.removeChild(b);
    if (val === "accepted") enableTracking();
  }

  function banner() {
    var wrap = document.createElement("div");
    wrap.id = "st-consent";
    wrap.setAttribute("role", "dialog");
    wrap.setAttribute("aria-label", "Cookie consent");
    wrap.innerHTML =
      '<div class="st-c-inner">' +
        '<p>This site uses cookies and similar tools for analytics and to improve your experience. ' +
        'See our <a href="/privacy.html">Privacy Policy</a>.</p>' +
        '<div class="st-c-btns">' +
          '<button type="button" class="st-c-decline">Decline</button>' +
          '<button type="button" class="st-c-accept">Accept</button>' +
        '</div>' +
      '</div>';
    var css = document.createElement("style");
    css.textContent =
      '#st-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;background:#12151c;border:1px solid rgba(190,205,230,.18);' +
      'border-radius:14px;box-shadow:0 20px 60px rgba(0,0,0,.5);max-width:640px;margin:0 auto;font-family:Inter,system-ui,sans-serif}' +
      '#st-consent .st-c-inner{display:flex;gap:16px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:16px 18px}' +
      '#st-consent p{color:#c4cad6;font-size:13.5px;line-height:1.5;margin:0;flex:1;min-width:220px}' +
      '#st-consent a{color:#86b3ff}' +
      '#st-consent .st-c-btns{display:flex;gap:10px}' +
      '#st-consent button{border-radius:999px;padding:10px 18px;font-size:13px;font-weight:600;cursor:pointer;border:1px solid rgba(190,205,230,.22);background:transparent;color:#f3f5f9}' +
      '#st-consent .st-c-accept{background:linear-gradient(135deg,#86b3ff,#4f8cff);color:#08122a;border-color:transparent}';
    document.head.appendChild(css);
    document.body.appendChild(wrap);
    wrap.querySelector(".st-c-accept").addEventListener("click", function () { setChoice("accepted"); });
    wrap.querySelector(".st-c-decline").addEventListener("click", function () { setChoice("declined"); });
  }

  function start() {
    if (choice === "accepted") { enableTracking(); return; }
    if (choice === "declined") { return; }
    banner();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
