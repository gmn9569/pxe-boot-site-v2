# pxe-boot-site (DRAFT)

Static one-page landing page for pxe-boot.com. Plain HTML/CSS + a tiny JS file, no build step.
Deploy later by pointing Cloudflare Pages or GitHub Pages at the repo root.

- `index.html`: page markup (includes `noindex` while in draft; remove before launch)
- `styles.css`, `script.js`, `favicon.svg` (placeholder)
- Waitlist form is a **placeholder**: not wired to any service.
- Preview locally: `python3 -m http.server` then open http://localhost:8000
