/* Diamond Locs — site behavior. No trackers, no cookies, no third-party scripts. */

// Where inquiries are sent. CHANGE THIS to the business inbox before launch.
const CONTACT_EMAIL = "hello@diamondlocs.com";

(function () {
  const nav = document.querySelector(".nav");
  const onScroll = () => nav && nav.classList.toggle("solid", window.scrollY > 40);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // mobile menu
  const burger = document.querySelector(".burger");
  const links = document.querySelector(".links");
  if (burger && links) {
    burger.addEventListener("click", () => {
      const open = links.classList.toggle("open");
      burger.setAttribute("aria-expanded", open);
      document.body.style.overflow = open ? "hidden" : "";
    });
    links.addEventListener("click", (e) => {
      if (e.target.tagName === "A") {
        links.classList.remove("open");
        document.body.style.overflow = "";
      }
    });
  }

  // scroll reveal
  const items = document.querySelectorAll(".rv");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }),
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
    items.forEach((el) => io.observe(el));
  } else items.forEach((el) => el.classList.add("in"));

  // collection filter
  const fbtns = document.querySelectorAll(".filters button");
  const pieces = document.querySelectorAll(".piece");
  fbtns.forEach((b) =>
    b.addEventListener("click", () => {
      fbtns.forEach((x) => x.classList.remove("on"));
      b.classList.add("on");
      const f = b.dataset.f;
      pieces.forEach((p) => p.classList.toggle("hide", f !== "all" && p.dataset.c !== f));
    })
  );

  // lightbox
  const lb = document.querySelector(".lb");
  if (lb) {
    const lbimg = lb.querySelector("img");
    const lbcap = lb.querySelector("p");
    const close = () => lb.classList.remove("on");
    pieces.forEach((p) =>
      p.addEventListener("click", () => {
        const img = p.querySelector("img");
        lbimg.src = img.src;
        lbimg.alt = img.alt;
        lbcap.textContent = p.querySelector("h3").textContent;
        lb.classList.add("on");
      })
    );
    lb.addEventListener("click", close);
    document.addEventListener("keydown", (e) => e.key === "Escape" && close());
  }

  // inquiry form -> opens the visitor's own email app (nothing is stored on a server)
  const form = document.querySelector("#inquiry");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const d = new FormData(form);
      const subject = `Inquiry — ${d.get("interest") || "Diamond Locs"}`;
      const body =
        `Name: ${d.get("name")}\nEmail: ${d.get("email")}\nPhone: ${d.get("phone") || "-"}\n` +
        `Interest: ${d.get("interest")}\nBirth month / stone: ${d.get("stone") || "-"}\n\n${d.get("message") || ""}`;
      window.location.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      const ok = document.querySelector("#sent");
      if (ok) ok.hidden = false;
    });
  }
})();
