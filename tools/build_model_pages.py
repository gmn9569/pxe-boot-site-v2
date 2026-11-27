#!/usr/bin/env python3
"""Turn images/models/<name>/bible.md into static example pages.

Run from the repo root: python3 tools/build_model_pages.py
The site has no client-side markdown step. This writes examples.html and
models/<name>.html, then the pages are served as plain HTML.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "images" / "models"
ORDER = ["isa", "bea", "hex", "mochi", "rook", "tala"]
NAMES = {
    "isa": "Isa",
    "bea": "Bea",
    "hex": "Hex",
    "mochi": "Mochi",
    "rook": "Rook",
    "tala": "Tala",
}
SHOTS = [
    ("banner_1500x500.jpg", "Banner", "banner", True),
    ("avatar_1024.jpg", "Avatar", "avatar portrait", False),
    ("cover.jpg", "Cover", "cover", False),
    ("thumbnail_1280x720.jpg", "Thumbnail", "thumbnail", False),
]
LIKENESS = {
    "likeness_turtleneck.jpg": (
        "Likeness · black turtleneck",
        "Isa likeness, fitted black turtleneck on a studio background",
    ),
    "likeness_blouse.jpg": (
        "Likeness · ivory blouse",
        "Isa likeness, ivory blouse in a daylight interior",
    ),
    "likeness_blazer.jpg": (
        "Likeness · black blazer",
        "Isa likeness, black blazer in an evening interior",
    ),
}


def jpeg_size(path):
    data = path.read_bytes()
    if data[:2] != b"\xff\xd8":
        raise SystemExit(f"Not a JPEG: {path}")
    i = 2
    while i < len(data) - 8:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = int.from_bytes(data[i + 5 : i + 7], "big"), int.from_bytes(data[i + 7 : i + 9], "big")
            return width, height
        if marker in (0xD8, 0xD9):
            i += 2
            continue
        seg = int.from_bytes(data[i + 2 : i + 4], "big")
        i += 2 + seg
    raise SystemExit(f"No size in {path}")


def inline(text):
    escaped = html.escape(text.strip())
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def paragraph(block):
    parts = []
    lines = block.split("\n")
    for index, line in enumerate(lines):
        hard = line.endswith("  ")
        parts.append(inline(line))
        if index < len(lines) - 1:
            parts.append("<br>" if hard else " ")
    return "<p>" + "".join(parts) + "</p>"


def is_table_sep(line):
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def markdown_to_html(source):
    blocks = re.split(r"\n\s*\n", source.strip())
    out = []
    for block in blocks:
        lines = block.split("\n")
        if len(lines) == 1 and lines[0].startswith("#"):
            level = len(lines[0]) - len(lines[0].lstrip("#"))
            text = lines[0][level:].strip()
            # Keep a single page h1 (the character name). Bible headings start at h2.
            tag = "h2" if level <= 1 else "h3"
            out.append(f"<{tag}>{inline(text)}</{tag}>")
            continue
        if all(line.startswith("- ") for line in lines):
            items = "".join(f"<li>{inline(line[2:])}</li>" for line in lines)
            out.append(f"<ul>{items}</ul>")
            continue
        if "|" in block and any(is_table_sep(line) for line in lines):
            rows = []
            for line in lines:
                if is_table_sep(line):
                    continue
                cells = [inline(cell) for cell in line.strip().strip("|").split("|")]
                rows.append(cells)
            head, body = rows[0], rows[1:]
            thead = "<tr>" + "".join(f"<th>{cell}</th>" for cell in head) + "</tr>"
            tbody = "".join(
                "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in body
            )
            out.append(f'<div class="bible-table"><table><thead>{thead}</thead><tbody>{tbody}</tbody></table></div>')
            continue
        out.append(paragraph(block))
    return "\n".join(out)


def concept_paragraph(source):
    match = re.search(r"^## Concept\s*\n+(.+?)(?:\n\s*\n|\n## )", source, re.M | re.S)
    if not match:
        raise SystemExit("Missing concept section")
    text = " ".join(line.strip() for line in match.group(1).strip().splitlines())
    return text


def first_sentence(text):
    match = re.match(r"(.+?\.)\s", text + " ")
    return match.group(1) if match else text


def chrome(title, description, canonical, depth, current, body):
    prefix = "../" if depth else ""
    home = f"{prefix}index.html"

    def href(page):
        return f"{prefix}{page}" if page else home

    nav = [
        ("How it works", f"{home}#how", False),
        ("Our promise", f"{home}#promise", False),
        ("Who it's for", f"{home}#who", False),
        ("Examples", href("examples.html"), current == "examples"),
        ("The pack", f"{home}#order", False),
    ]
    items = []
    for label, url, here in nav:
        current_attr = ' aria-current="page"' if here else ""
        items.append(f'<li><a href="{url}"{current_attr}>{label}</a></li>')
    items.append(
        '<li><a class="btn small" href="https://pxeboot.gumroad.com/l/dojdxr">Order</a></li>'
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="robots" content="noindex, nofollow">
  <link rel="canonical" href="{html.escape(canonical)}">
  <meta name="theme-color" content="#0f172a">
  <link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{prefix}favicon.ico" sizes="any">
  <link rel="icon" href="{prefix}favicon-16.png" type="image/png" sizes="16x16">
  <link rel="icon" href="{prefix}favicon-32.png" type="image/png" sizes="32x32">
  <link rel="icon" href="{prefix}favicon-48.png" type="image/png" sizes="48x48">
  <link rel="icon" href="{prefix}icon-512.png" type="image/png" sizes="512x512">
  <link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
  <link rel="stylesheet" href="{prefix}styles.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="top">
    <div class="wrap nav">
      <a class="brand" href="{home}">
        <picture>
          <source media="(max-width: 959px)" srcset="{prefix}brand/lockup-horizontal-small-dark.svg">
          <img src="{prefix}brand/lockup-horizontal-dark.svg" width="300" height="72" alt="PXE Boot">
        </picture>
      </a>
      <nav aria-label="Primary">
        <ul>
          {''.join(items)}
        </ul>
      </nav>
    </div>
  </header>
  <main id="main" class="page">
    {body}
  </main>
  <footer class="foot">
    <div class="wrap">
      <p>&copy; <span id="year">2026</span> PXE Boot. You learn it, you own it.</p>
      <p class="small"><a href="https://pxe-boot.com/">pxe-boot.com</a> · <a href="https://pxeboot.gumroad.com">Store</a></p>
    </div>
  </footer>
  <script src="{prefix}script.js" defer></script>
</body>
</html>
"""


def shot_html(href, src, width, height, alt, label, size_label, wide):
    wide_class = " shot-wide" if wide else ""
    return f"""<a class="shot{wide_class}" href="{href}">
      <img src="{src}" width="{width}" height="{height}" alt="{html.escape(alt)}">
      <span class="shot-label">{html.escape(label)} <span>{size_label}</span></span>
    </a>"""


def build_model(slug):
    folder = MODELS / slug
    bible_path = folder / "bible.md"
    source = bible_path.read_text(encoding="utf-8")
    name = NAMES[slug]
    concept = concept_paragraph(source)
    summary = first_sentence(concept)
    asset = f"../images/models/{slug}"
    shots = []
    for filename, label, role, wide in SHOTS:
        path = folder / filename
        width, height = jpeg_size(path)
        alt = f"{name}, a PXE Boot AI character, {role}"
        if slug == "isa" and filename == "avatar_1024.jpg":
            alt = "Isa, a PXE Boot AI character, avatar portrait in a red leather jacket"
        shots.append(
            shot_html(
                f"{asset}/{filename}",
                f"{asset}/{filename}",
                width,
                height,
                alt,
                label,
                f"{width}×{height}",
                wide,
            )
        )
    likeness_files = sorted(folder.glob("likeness_*.jpg"))
    likeness = ""
    if likeness_files:
        cards = []
        for path in likeness_files:
            label, alt = LIKENESS.get(
                path.name,
                (path.stem.replace("_", " ").title(), f"{name} likeness"),
            )
            width, height = jpeg_size(path)
            cards.append(
                shot_html(
                    f"{asset}/{path.name}",
                    f"{asset}/{path.name}",
                    width,
                    height,
                    alt,
                    label,
                    f"{width}×{height}",
                    False,
                )
            )
        likeness = f"""<h2>Likeness set</h2>
    <p class="lead">Same face, different clothes and light. Each picture opens full size.</p>
    <div class="shot-grid">{''.join(cards)}</div>"""
    body = f"""<div class="wrap">
      <p class="crumb"><a href="../examples.html">Examples</a> <span aria-hidden="true">/</span> {html.escape(name)}</p>
      <p class="eyebrow on-light">Character Identity Pack example</p>
      <h1>{html.escape(name)}</h1>
      <p class="lead">{html.escape(concept)}</p>
      <div class="shot-grid" aria-label="{html.escape(name)} pack pictures">
        {''.join(shots)}
      </div>
      {likeness}
      <div class="bible">
        {markdown_to_html(source)}
      </div>
      <p class="bible-download"><a href="{asset}/bible.md" download>Download the character bible (Markdown)</a></p>
      <div class="cta-row model-cta">
        <a class="btn" href="https://pxeboot.gumroad.com/l/dojdxr">Order — pay the $20 deposit</a>
      </div>
      <p class="order-secondary"><a href="https://pxeboot.gumroad.com/l/ytuicr">Already paid the deposit? Pay the balance</a></p>
    </div>"""
    page = chrome(
        f"{name} | PXE Boot",
        summary,
        f"https://pxe-boot.com/models/{slug}.html",
        1,
        None,
        body,
    )
    out = ROOT / "models" / f"{slug}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return {"slug": slug, "name": name, "summary": summary}


def build_index(cards):
    items = []
    for card in cards:
        slug, name, summary = card["slug"], card["name"], card["summary"]
        thumb = MODELS / slug / "thumbnail_1280x720.jpg"
        width, height = jpeg_size(thumb)
        items.append(
            f"""<a class="card example-card-link" href="models/{slug}.html">
          <img src="images/models/{slug}/thumbnail_1280x720.jpg" width="{width}" height="{height}" alt="{html.escape(name)}, a PXE Boot AI character, thumbnail">
          <h2>{html.escape(name)}</h2>
          <p>{html.escape(summary)}</p>
        </a>"""
        )
    body = f"""<div class="wrap">
      <p class="eyebrow on-light">Sample lineup</p>
      <h1>Example characters</h1>
      <p class="lead">Fictional adult characters used as safe-for-work samples of an avatar, a banner, a thumbnail, and a cover. Isa is first. None of them are real people.</p>
      <div class="example-index">
        {''.join(items)}
      </div>
      <div class="cta-row model-cta">
        <a class="btn" href="https://pxeboot.gumroad.com/l/dojdxr">Order — pay the $20 deposit</a>
      </div>
    </div>"""
    page = chrome(
        "Example characters | PXE Boot",
        "Sample PXE Boot characters: Isa, Bea, Hex, Mochi, Rook, and Tala. Fictional, safe for work, and not based on real people.",
        "https://pxe-boot.com/examples.html",
        0,
        "examples",
        body,
    )
    (ROOT / "examples.html").write_text(page, encoding="utf-8")


def main():
    missing = [slug for slug in ORDER if not (MODELS / slug / "bible.md").is_file()]
    if missing:
        raise SystemExit(f"Missing model folders: {', '.join(missing)}")
    cards = [build_model(slug) for slug in ORDER]
    build_index(cards)
    print(f"Wrote examples.html and {len(cards)} model pages.")


if __name__ == "__main__":
    main()
