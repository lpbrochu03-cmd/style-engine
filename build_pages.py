"""Render the plain-text pages of the site: privacy, terms, and what things cost.

    python build_pages.py

Privacy and Terms are not written here. They are written once, as markdown, in
the app's own repo, and this turns those files into pages. Two copies of a
promise about what happens to someone's writing is one copy too many: the day
they disagree, the page is a lie and nobody notices. Same for the prices, which
come out of store.json — the file that is already the whole catalogue.

The look is the landing page's, cut down to what a page of text needs.
"""
import html
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, os.pardir, "style-engine")

# ---------------------------------------------------------------------------
# A very small markdown reader. It handles exactly what PRIVACY.md and TERMS.md
# use -- headings, paragraphs, bullets, bold, italics, code and links -- and
# nothing else. A general parser would be a dependency and a liability for four
# constructs.
# ---------------------------------------------------------------------------

def inline(text):
    out = html.escape(text)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def markdown(src):
    lines = src.split("\n")
    html_parts = []
    para = []
    bullets = []

    def flush_para():
        if para:
            html_parts.append("<p>" + inline(" ".join(para).strip()) + "</p>")
            para.clear()

    def flush_bullets():
        if bullets:
            items = "".join("<li>" + inline(b) + "</li>" for b in bullets)
            html_parts.append("<ul>" + items + "</ul>")
            bullets.clear()

    for raw in lines:
        line = raw.rstrip()

        if not line.strip():
            flush_para()
            flush_bullets()
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_para()
            flush_bullets()
            level = len(m.group(1))
            # The document's own H1 becomes the page title, set by the template,
            # so it is not repeated in the body.
            if level == 1:
                continue
            html_parts.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue

        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            flush_para()
            bullets.append(m.group(1))
            continue

        flush_bullets()
        para.append(line.strip())

    flush_para()
    flush_bullets()
    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# The look. Inlined rather than linked: these pages are small enough that a
# second request for the stylesheet would cost more than the bytes it saves,
# and every page on this site is meant to stand up on its own.
#
# The palette, faces, motion vocabulary and shared controls are NOT written
# here any more. They live in the app repo's theme.css and are read in, the
# same one-directional way this file already reads PRIVACY.md, TERMS.md and
# store.json. Before that, the colours were written out four separate times —
# here, in index.html, in 404.html and in the app — and had already drifted:
# this file's copy had lost the light half and four of the five palettes.
# ---------------------------------------------------------------------------

# Two files, because the app takes the first and not the second. theme.css is
# nothing but custom properties, @font-face and @keyframes, so it is safe to
# inline anywhere; theme-site.css applies them, and its `.btn` would otherwise
# turn all forty-nine of the app's instrument buttons into the site's pills.
THEME = os.path.join(APP, "theme.css")
THEME_SITE = os.path.join(APP, "theme-site.css")


def _read(path):
    if not os.path.exists(path):
        sys.exit(f"missing {path} — is the app repo beside this one?")
    return open(path, encoding="utf-8").read()


def theme_css(assets):
    """The full stylesheet every site page starts with, with its one
    build-time hole filled.

    `assets` is the path from the page being written back to /assets. It cannot
    be baked in because the pages sit at different depths: the landing page and
    404 are at the root, everything generated here is one folder down. Getting
    it wrong costs the fonts silently — the page still renders, in the fallback
    stack, looking almost right.
    """
    return (_read(THEME) + _read(THEME_SITE)).replace("__ASSETS__", assets)


# What is left here is only what a page of text and a price list need. Anything
# another page also uses belongs in theme.css instead.
PAGE_CSS = """
.bar{position:sticky;top:0;z-index:5;
  background:color-mix(in srgb, var(--ground) 82%, transparent);
  backdrop-filter:blur(12px) saturate(1.1);
  border-bottom:1px solid var(--line);
  transition:border-color var(--dur-2) var(--ease-out)}
.bar-in{max-width:760px;margin:0 auto;padding:14px var(--gutter);
  display:flex;align-items:center;justify-content:space-between;gap:16px}
.home{font-family:var(--mono);font-size:var(--t-xs);letter-spacing:var(--track-mono);
  text-transform:uppercase;color:var(--ink-2);text-decoration:none;
  display:inline-flex;align-items:center;gap:.6em;
  transition:color var(--dur-2) var(--ease-out)}
.home:hover{color:var(--accent)}
/* The arrow leads the eye back the way the link goes. Transform only, so it
   cannot nudge the text beside it. */
.home svg{width:1em;height:1em;transition:transform var(--dur-2) var(--ease-out)}
.home:hover svg{transform:translateX(-3px)}
.bar-right{display:flex;align-items:center;gap:16px}
.bar-shop{font:600 var(--t-sm)/1 var(--sans);color:var(--ink-2);text-decoration:none;
  display:inline-flex;align-items:center;min-height:34px;padding:0 4px;
  transition:color var(--dur-2) var(--ease-out)}
.bar-shop:hover{color:var(--accent)}
/* Geometry only — the fill, hover, press and glow come from theme.css so this
   button behaves identically to the one on the landing page. */
.bar-try{font-size:var(--t-sm);padding:9px 16px;white-space:nowrap}

main{max-width:760px;margin:0 auto;
  padding:clamp(48px,10vw,96px) var(--gutter) clamp(60px,12vw,120px)}
.eyebrow{font-family:var(--mono);font-size:var(--t-micro);letter-spacing:.18em;
  text-transform:uppercase;color:var(--accent);margin:0 0 1.3em;
  display:flex;align-items:center;gap:.75em}
.eyebrow::before{content:"";width:clamp(18px,6vw,34px);height:2px;background:var(--amber);flex:none}
h1{font-weight:700;font-size:clamp(2.3rem,8vw,3.6rem);line-height:1;margin:0 0 .5em}
.stamp{font-family:var(--mono);font-size:var(--t-xs);color:var(--ink-3);margin:0 0 2.6em;
  padding-bottom:1.6em;border-bottom:1px solid var(--line)}
h2{font-weight:600;font-size:var(--t-2xl);line-height:1.18;margin:2.5em 0 .7em}
h2:first-of-type{margin-top:0}
h3{font-weight:600;font-size:1.1rem;margin:2em 0 .5em}
p{margin:0 0 1.15em}
strong{color:var(--ink);font-weight:650}
em{color:var(--ink-2)}
code{font-family:var(--mono);font-size:.9em;background:var(--surface);
  border:1px solid var(--line);border-radius:var(--radius-sm);padding:.12em .42em}
ul{margin:0 0 1.3em;padding-left:1.15em}
li{margin-bottom:.5em}
li::marker{color:var(--accent)}
/* Body links get the shared treatment; scoped to main so the nav and footer,
   which have their own, are left alone. */
main a{color:var(--accent);text-decoration:none;
  border-bottom:1px solid color-mix(in srgb, var(--accent) 35%, transparent);
  transition:border-color var(--dur-2) var(--ease-out)}
main a:hover{border-bottom-color:currentColor}

/* Prices. A row per thing, the number set in the mono face because it is a
   figure to compare, not a sentence to read. */
.rows{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.row{border-bottom:1px solid var(--line);padding:clamp(20px,4.6vw,30px) 0;
  display:grid;gap:.35em .9em;grid-template-columns:1fr auto}
.row h2{grid-area:1/1/2/2;margin:0;font-size:var(--t-xl)}
.row .price{grid-area:1/2/2/3;font-family:var(--mono);font-size:clamp(1rem,3.6vw,1.15rem);
  color:var(--ink);white-space:nowrap;align-self:baseline}
.row .price small{color:var(--ink-3);font-size:.76em}
/* The picture sits between the price and the description: it is the fastest
   answer to "what is this", and a screenshot below the copy is a screenshot
   nobody scrolls to. Width and height are on the tag so the row does not
   jump when it loads. */
.row .shot{grid-area:2/1/3/3;display:block;margin:.2em 0 .95em;max-width:560px;
  border:1px solid var(--line);border-radius:var(--radius-sm);overflow:hidden;line-height:0;
  border-bottom:1px solid var(--line);
  transition:border-color var(--dur-2) var(--ease-out),
             box-shadow var(--dur-3) var(--ease-out),
             transform var(--dur-3) var(--ease-out)}
.row .shot img{display:block;width:100%;height:auto;max-height:290px;
  object-fit:cover;object-position:top left;
  transition:transform var(--dur-4) var(--ease-out)}
/* The row lifts and the picture inside it pushes very slightly past its frame:
   two speeds on one gesture, which is what stops it reading as a flat swap. */
.row .shot:hover{border-color:var(--ink-3);box-shadow:var(--elev-2);transform:translateY(-2px)}
.row .shot:hover img{transform:scale(1.02)}
.row p{grid-area:3/1/4/3;margin:0;color:var(--ink-2);font-size:.97rem}
.row .flag{grid-area:4/1/5/3;font-family:var(--mono);font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--amber);margin-top:.5em;
  display:inline-flex;align-items:center;gap:.55em}
/* A dot before the state, because "not yet" and "buy by hand" differ only by
   colour otherwise, and colour alone is not a distinction everyone can see. */
.row .flag::before{content:"";width:5px;height:5px;border-radius:50%;
  background:currentColor;flex:none;box-shadow:0 0 8px currentColor}
/* Amber is the shop's "not yet". Something you can actually buy has to look
   different from something you can't, or the two read as one state. */
.row .flag.open{color:var(--accent)}
.pay-handle{font-family:var(--mono);color:var(--accent);word-break:break-all}
.pay-steps{margin:.9em 0 0;padding-left:1.2em;color:var(--ink-2)}
.pay-steps li{margin:.35em 0}

.note{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:clamp(18px,4vw,26px);margin:0 0 2.4em;box-shadow:var(--elev-1)}
.note p:last-child{margin-bottom:0}

footer{border-top:1px solid var(--line);padding:clamp(34px,7vw,56px) var(--gutter);
  color:var(--ink-3);font-size:var(--t-sm)}
.foot-in{max-width:760px;margin:0 auto;display:flex;flex-wrap:wrap;gap:10px 26px;
  justify-content:space-between}
footer a{color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--line);
  display:inline-flex;align-items:center;min-height:26px;
  transition:color var(--dur-2) var(--ease-out),border-color var(--dur-2) var(--ease-out)}
footer a:hover{color:var(--accent);border-bottom-color:currentColor}
.foot-nav{display:flex;gap:14px 22px;flex-wrap:wrap;align-items:center}

/* These pages are text, so the entrance is the page arriving rather than each
   paragraph doing something on scroll. One gesture, once. */
main>*{animation:se-rise var(--dur-4) var(--ease-out) both}
main>*:nth-child(1){animation-delay:.02s}
main>*:nth-child(2){animation-delay:.06s}
main>*:nth-child(3){animation-delay:.10s}
main>*:nth-child(n+4){animation-delay:.14s}
"""

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M19 12H6M11 6l-6 6 6 6"/></svg>')

SITE = "https://lpbrochu03-cmd.github.io/style-engine"

ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'"
        "%3E%3Crect width='32' height='32' fill='%23080a05'/%3E%3Cpath d='M3 20 L8 20 L10 9 "
        "L13 25 L16 14 L19 22 L22 17 L25 20 L29 20' fill='none' stroke='%237fd39f' "
        "stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")


def page(slug, title, eyebrow, stamp, body, description):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)} — Style Engine</title>
<meta name="description" content="{html.escape(description)}">
<meta property="og:title" content="{html.escape(title)} — Style Engine">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/{slug}/">
<!-- 1200x630, drawn by ../style-engine/ads/cards.html. The poster it replaced
     was 9:16, so every scraper cropped it to a blank band. -->
<meta property="og:image" content="{SITE}/assets/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="See how you actually write — a bar chart of six sentence lengths, average 11.5 words.">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{ICON}">
<!-- Set before the stylesheet so the reveal rules only ever apply where there
     is a script alive to undo them. -->
<script>document.documentElement.className+=' js'</script>
<style>{theme_css("../assets")}{PAGE_CSS}</style>
</head>
<body>

<div class="bar">
  <div class="bar-in">
    <a class="home" href="../">{ARROW} Style Engine</a>
    <span class="bar-right">
      <a class="bar-shop" href="../pricing/">Shop</a>
      <a class="bar-try" href="../app/">Measure my writing</a>
    </span>
  </div>
</div>

<main>
  <p class="eyebrow">{html.escape(eyebrow)}</p>
  <h1>{html.escape(title)}</h1>
  <p class="stamp">{stamp}</p>
  {body}
</main>

<footer>
  <div class="foot-in">
    <span>Style Engine</span>
    <nav class="foot-nav">
      <a href="../">Home</a>
      <a href="../pricing/">Shop</a>
      <a href="../privacy/">Privacy</a>
      <a href="../terms/">Terms</a>
    </nav>
  </div>
</footer>
</body>
</html>
"""


def write(slug, text):
    out_dir = os.path.join(HERE, slug)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "index.html")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"  {slug}/index.html  ({len(text)/1000:.1f} KB)")


def stamp_from(md):
    m = re.search(r"^\*Last updated:\s*(.+?)\*$", md, re.M)
    return f"Last updated {html.escape(m.group(1))}" if m else ""


def build_doc(slug, source, eyebrow, description):
    src_path = os.path.join(APP, source)
    if not os.path.exists(src_path):
        sys.exit(f"missing {src_path} — is the app repo beside this one?")
    md = open(src_path, encoding="utf-8").read()
    title = re.search(r"^#\s+(.*)$", md, re.M).group(1)
    stamp = stamp_from(md)
    # The date is lifted out into the header under the title, so the line it
    # came from is dropped rather than printed a second line below itself.
    body = markdown(re.sub(r"^\*Last updated:.*?\*$\n?", "", md, flags=re.M))
    write(slug, page(slug, title, eyebrow, stamp, body, description))


def money(cents, currency):
    sym = "$" if currency == "usd" else ""
    return f"{sym}{cents/100:,.2f}".rstrip("0").rstrip(".") if cents % 100 else f"{sym}{cents//100}"


def copy_shop_pictures(wanted):
    """Bring the shelf's pictures over from the app repo into assets/shop/.

    Copied rather than linked, because this repo is what gets served and the
    app repo is not published. Only the files the page actually references are
    copied: the folder next door is a working directory, and a build step that
    hoovers up whatever is in it publishes drafts.
    """
    if not wanted:
        return []
    src = os.path.join(APP, "shop")
    dst = os.path.join(HERE, "assets", "shop")
    os.makedirs(dst, exist_ok=True)
    copied = []
    for name in sorted(wanted):
        found = os.path.join(src, name)
        if not os.path.isfile(found):
            # Loud, because the alternative is a broken frame on the public
            # page and a build that said "done."
            print(f"  MISSING picture: shop/{name} — the row will have no image")
            continue
        shutil.copyfile(found, os.path.join(dst, name))
        copied.append(name)
    return copied


def build_pricing():
    data = json.load(open(os.path.join(APP, "store.json"), encoding="utf-8"))
    # Selling by hand needs somewhere to send the money. Absent from store.json,
    # this whole path stays off and the page reads exactly as it did before —
    # which is the correct state until an adult's account exists to name here.
    pay = data.get("pay") or None
    shown = [p for p in data["products"]
             if p.get("shelf") == "main" and p.get("status") != "hidden"]
    have = set(copy_shop_pictures({p["image"] for p in shown if p.get("image")}))
    rows = []
    # The back room is reached by typing its name into the app. Listing its
    # shelf on a public price page would be publishing the secret — `shown` is
    # filtered on the way in, above.
    for p in shown:
        price = money(p["price"], p.get("currency", "usd"))
        unit = " <small>/ month</small>" if "subscription" in p.get("tags", []) else " <small>once</small>"
        # Three states, not two. "manual" is the one that matters before there
        # is a processor: the price is real, the thing exists, and it is bought
        # by paying a person and being sent a key by hand.
        if p.get("status") == "live":
            flag = ""
        elif p.get("status") == "manual" and pay:
            flag = '<div class="flag open">Buy by hand &mdash; see above</div>'
        else:
            flag = '<div class="flag">Not buyable yet</div>'

        # Only if the file actually came across. A row with no picture is the
        # design, not a fallback; a row with a picture that 404s is neither.
        shot = ""
        if p.get("image") in have:
            alt = html.escape(f'{p["name"]}, as it looks when you open it')
            # `../` because this page is written to pricing/index.html, so a bare
            # "assets/..." asks for pricing/assets/... and gets the 404 page.
            # The same climb the nav links in this file already make.
            shot = (f'<a class="shot" href="../assets/shop/{p["image"]}">'
                    f'<img src="../assets/shop/{p["image"]}" alt="{alt}" '
                    f'loading="lazy" decoding="async" width="1200" height="750"></a>')

        rows.append(
            '<li class="row">'
            f'<h2>{html.escape(p["name"])}</h2>'
            f'<div class="price">{price}{unit}</div>'
            f'{shot}'
            f'<p>{html.escape(p.get("blurb", ""))}</p>'
            f'{flag}'
            '</li>'
        )

    # Stated plainly at the top rather than discovered at a checkout that does
    # not work. Nothing here takes money yet and the page should say so first.
    buyable = [p for p in shown if p.get("status") in ("live", "manual")]
    if pay and buyable:
        # No checkout, no processor, no monthly server bill: someone pays a
        # person and a key is issued by hand with backend/issue_key.py. It is
        # how the first few sales happen anyway, so the page may as well say it
        # instead of pretending the shop is shut.
        handle = html.escape(pay.get("handle", ""))
        service = html.escape(pay.get("service", "Venmo"))
        contact = html.escape(pay.get("email", ""))
        turnaround = html.escape(pay.get("turnaround", "within a day"))
        steps = [f'<li>Send the price below to <span class="pay-handle">{handle}</span> '
                 f'on {service}.</li>',
                 '<li>Put the name of the thing you are buying in the note.</li>']
        if contact:
            steps.append(f'<li>Email <span class="pay-handle">{contact}</span> from the '
                         'address you want the key sent to.</li>')
        parts = ['<div class="note">',
                 '<p><strong>Buying works, but it is done by hand.</strong> There is no '
                 'checkout on this page yet &mdash; you pay a person, and a key comes '
                 f'back to you {turnaround}.</p>',
                 '<ol class="pay-steps">', "".join(steps), '</ol>']
        if pay.get("note"):
            parts.append(f'<p>{html.escape(pay["note"])}</p>')
        parts.append('<p>The Style Mirror is free, works now, and stays free.</p></div>')
        note = "".join(parts)
    else:
        note = (
            '<div class="note">'
            '<p><strong>Nothing on this page can be bought today.</strong> Payments '
            'need an account owned by an adult, and that is not set up yet. The '
            'prices are real and they are what these will cost.</p>'
            '<p>The Style Mirror is free, works now, and stays free.</p>'
            '</div>'
        )

    body = note + '<ul class="rows">' + "".join(rows) + "</ul>"
    write("pricing", page(
        "pricing", "The shop", "Everything for sale",
        "Prices are real; the checkout is not open yet.",
        body,
        "What Style Engine Pro and the other things cost. The Style Mirror is free."))


# ---------------------------------------------------------------------------
# The two hand-written pages.
#
# index.html and 404.html are edited by hand and always will be — they are the
# argument, not a rendering of something else. But they need the same palette,
# faces and motion as everything else, and copying it in is how it drifted the
# first time. So they carry a pair of markers, and this rewrites what is
# between them. Everything outside the markers is left exactly as written.
# ---------------------------------------------------------------------------

START = "/* @theme:start — generated by build_pages.py; edit theme.css instead */"
END = "/* @theme:end */"


def sync_theme(name, assets):
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        print(f"  {name}: not here, skipped")
        return
    src = open(path, encoding="utf-8").read()
    a, b = src.find(START), src.find(END)
    if a == -1 or b == -1:
        # Loud rather than silent: a page that quietly stops being themed looks
        # almost right, which is the hardest kind of wrong to notice.
        print(f"  {name}: NO THEME MARKERS — not themed. Add {START} / {END}")
        return
    block = START + "\n" + theme_css(assets) + "\n" + END
    out = src[:a] + block + src[b + len(END):]
    if out == src:
        print(f"  {name}  (already current)")
        return
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"  {name}  ({len(out)/1000:.1f} KB)")


if __name__ == "__main__":
    print("generated pages:")
    build_doc("privacy", "PRIVACY.md", "The short version: almost nothing",
              "What Style Engine keeps, what it sends elsewhere, and how to get rid of it.")
    build_doc("terms", "TERMS.md", "Plain terms",
              "What Style Engine is, what it will not do, and the rules for using it.")
    build_pricing()
    print("hand-written pages, theme block:")
    sync_theme("index.html", "assets")
    sync_theme("404.html", "assets")
    print("done.")
