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

    index.html      the landing page — hand-written, no dependencies, no fonts
                    fetched, no analytics
    app/index.html  the app itself, generated from the full application
    assets/         the poster stills and the film

No web fonts is a decision rather than an omission. The page's whole claim is
that nothing is sent anywhere, and a page that loads a font from a third party
tells every visitor's browser to announce itself to that third party first.

The application's server half — the model calls, billing, accounts — is not
here. This is the half that runs in a browser and needs nothing.

## Publishing an update

Rebuild the app half, copy the one file over, commit, push:

    python build_share.py docs
    cp docs/index.html ../style-engine-site/app/index.html

The landing page is edited directly; it is not generated from anything.

Pages deploys from `.github/workflows/pages.yml` on every push to `main`, so
the branch and folder dropdowns in the Pages settings screen do not need to be
set at all.
