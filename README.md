# Style Engine

**See how you actually write.**

Drop in your schoolwork and it measures your writing back to you — sentence
rhythm, the phrases you lean on, how you open an argument, the typos that are
really just your hands moving too fast.

Nothing is generated. Nothing is sent anywhere. The page you are served is a
single HTML file and the measuring happens in your own browser, so your writing
never leaves the tab.

**Try it: https://lpbrochu03-cmd.github.io/style-engine/**

---

## What it does

- **The Mirror** — profiles a document you drop in and reports your measured
  patterns back to you. Free, always.
- **Draft Feedback** — scores a draft against a rubric. It never writes the
  essay for you; that is a deliberate limit, not a missing feature.
- **Assignments** — a checklist that lives in your browser.

## What this repo is

Two pages and the pictures between them:

    index.html      the landing page — hand-written, no dependencies, no
                    analytics, nothing fetched from anyone else
    404.html        hand-written
    app/index.html  the app itself, generated from the full application
    pricing/        what things cost, generated from store.json
    privacy/        generated from the app's PRIVACY.md
    terms/          generated from the app's TERMS.md
    assets/fonts/   the two typefaces, served from here rather than a CDN
    assets/         the poster stills and the film

The three generated pages are built by `python build_pages.py`. Privacy and
Terms are not written here — they are written once as markdown in the app's
repo and rendered from it, because two copies of a promise about someone's
writing is one copy too many. The day they disagree, one of them is a lie.

## The look

The palette, the two typefaces, the type scale and the motion vocabulary are
one file — `../style-engine/theme.css` — and `build_pages.py` inlines it into
every page here. It used to be written out four separate times, in this repo
and in the app's, and had already drifted: this repo's copy had lost the light
theme and four of the five palettes.

`theme.css` contains nothing but custom properties, `@font-face` and
`@keyframes`. That restraint is load-bearing: the same file is inlined into the
app, and the app's buttons are 2px-radius instrument controls where the site's
are pills. A single `.btn` rule in there would restyle all forty-nine of them.
Rules that *apply* those values live in `theme-site.css`, which only this repo's
pages take.

To change a colour or a duration everywhere: edit `theme.css`, then run
`python build_pages.py` here and `python sync_theme.py` in the app repo.

**No third-party requests is still the decision.** The two typefaces are served
from `assets/fonts/` on this origin — 69 KB, latin subset — rather than from a
font CDN. The page's whole claim is that nothing is sent anywhere, and a page
that loads a font from a third party tells every visitor's browser to announce
itself to that third party first. Self-hosting keeps the claim true. Both faces
also carry a full system fallback, so the app still renders correctly when it
is opened as a standalone file with no `assets/` beside it.

The application's server half — the model calls, billing, accounts — is not
here. This is the half that runs in a browser and needs nothing.

## Publishing an update

Rebuild the app half, copy the one file over, commit, push. From the app repo:

    python sync_theme.py                 # only if theme.css changed
    python build_share.py docs
    cp docs/index.html ../style-engine-site/app/index.html

Then from here:

    python build_pages.py                # generated pages + the theme block

The landing page and 404 are edited directly and are not generated — but the
block between their `@theme:start` / `@theme:end` markers is, so run
`build_pages.py` after touching `theme.css` or the two will disagree.

Pages deploys from `.github/workflows/pages.yml` on every push to `main`, so
the branch and folder dropdowns in the Pages settings screen do not need to be
set at all.
