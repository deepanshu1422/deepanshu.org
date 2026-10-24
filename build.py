#!/usr/bin/env python3
# Builds index.html + /<slug>/ redirect pages from resources.json.
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "resources.json")))

CARD = '''      <a class="card" href="/{slug}/">
        <div class="row"><span class="tag">{tag}</span><span class="kw">Comment “{kw}”</span></div>
        <h2>{title}</h2>
        <p>{desc}</p>
        <span class="go">deepanshu.org/{slug} →</span>
      </a>'''

REDIRECT = '''<!doctype html>
<html><head><meta charset="utf-8"><title>{title} — deepanshu.org</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<script>location.replace("{url}")</script>
</head><body style="font-family:system-ui;padding:24px">Redirecting to <a href="{url}">{title}</a>…</body></html>
'''

esc = lambda r: {k: html.escape(v) for k, v in r.items()}
cards = "\n".join(CARD.format(**esc(r)) for r in R)
tpl = open(os.path.join(HERE, "index.tpl.html")).read()
open(os.path.join(HERE, "index.html"), "w").write(tpl.replace("{{CARDS}}", cards))
for r in R:
    os.makedirs(os.path.join(HERE, r["slug"]), exist_ok=True)
    open(os.path.join(HERE, r["slug"], "index.html"), "w").write(REDIRECT.format(**esc(r)))
print(f"built {len(R)} resources")
