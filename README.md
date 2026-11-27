# PXE Boot site (draft)

Static one-page site for [pxe-boot.com](https://pxe-boot.com/). Plain HTML, CSS, and a small script. No build step.

The brand name is **PXE Boot**. `pxe-boot.com` is only the web address.

Example characters live at `examples.html`, with one page per character in `models/`. Pictures and character bibles are in `images/models/<name>/`. Regenerate the pages from those bibles with `python3 tools/build_model_pages.py`.

Preview locally:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000

GitHub Pages publishes the `main` branch only, from `.github/workflows/pages.yml`. This repo does not deploy pull-request previews. Do not merge until the custom domain is ready (see below).

## Brand

Header lockup is the Keyhole P horizontal mark for a dark background (`brand/lockup-horizontal-dark.svg`). Viewports under 960px use `brand/lockup-horizontal-small-dark.svg`, because the full lockup's minimum size is 48px tall and the small lockup is the 24–47px version. Keep at least that size, and keep clear space around the mark.

Icons at the site root: `favicon.ico`, `favicon.svg` (follows light and dark browser theme), `favicon-16.png`, `favicon-32.png`, `favicon-48.png`, `apple-touch-icon.png`, `icon-512.png`. Social image: `og-image.png` (1200×630).

Colors in `styles.css`: primary teal `#0f766e`, glow teal `#5eead4`, ink `#0f172a`, light `#f8fafc`, slate `#475569`, accent `#0d9488` for buttons and links.

The page still sends `noindex, nofollow`. Remove that meta tag before a public launch.

## Ordering

The $49 Character Identity Pack is two Gumroad products. There is no Stripe checkout.

| What | Link |
|---|---|
| $20 deposit (every Order button) | https://pxeboot.gumroad.com/l/dojdxr |
| $29 balance | https://pxeboot.gumroad.com/l/ytuicr |
| Storefront | https://pxeboot.gumroad.com |

$49 = $20 deposit + $29 balance. That split is written on the page.

## Waitlist (Formspree)

The form posts to https://formspree.io/f/mjywzjlw with `Accept: application/json`. It does not store addresses in this repo. The email field is `name="email"`, and an empty `_gotcha` field is included as a spam honeypot.

A successful signup hides the form and shows "You're on the list." A failed request asks the visitor to try again.

## Custom domain

`CNAME` contains `pxe-boot.com`. Merging this file makes GitHub Pages redirect `https://gmn9569.github.io/pxe-boot-site-v2/` to `https://pxe-boot.com/`. That host will not resolve until DNS for pxe-boot.com points at GitHub Pages. Do not merge until Gary approves that DNS change. This repo does not change DNS or registrar settings.
