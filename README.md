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

The published static build only: `index.html`, one file, no dependencies, no
build step, no tracking. It is generated from the full application with

    python build_share.py docs

The application's server half — the model calls, billing, accounts — is not
here. This is the half that runs in a browser and needs nothing.

## Publishing an update

Rebuild, copy the one file over, commit, push:

    python build_share.py docs
    cp docs/index.html ../style-engine-site/index.html

GitHub Pages serves the repository root of the `main` branch. The file sits at
the root rather than in `/docs` for a boring but real reason: root is the
default in the Pages settings, so publishing needs no second dropdown and there
is one less thing to set wrong.
