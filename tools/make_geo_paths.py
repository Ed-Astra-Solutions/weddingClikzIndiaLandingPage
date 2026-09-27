"""
Moves the India and UAE landing pages to real URL paths:

    weddingclickz.com/in/   <- wedding-photographer-india.html
    weddingclickz.com/ae/   <- wedding-photographer-uae.html

The site is on GitHub Pages, which cannot do server-side redirects or rewrites,
so each path has to be a real directory holding an index.html. The old .html
URLs are kept as stubs that canonicalise to the new path and bounce the visitor,
so nothing that already links to them breaks.

Run: python3 make_geo_paths.py
"""
import os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = 'https://weddingclickz.com'

MOVES = [
    ('wedding-photographer-india.html', 'in',  'en-IN', 'India'),
    ('wedding-photographer-uae.html',   'ae',  'en-AE', 'UAE'),
]
# every self/sibling reference that must now point at a path
LINK_MAP = {
    'wedding-photographer-india.html': '/in/',
    'wedding-photographer-uae.html':   '/ae/',
}

HREFLANG = (
    f'    <link rel="alternate" hreflang="en-in" href="{SITE}/in/">\n'
    f'    <link rel="alternate" hreflang="en-ae" href="{SITE}/ae/">\n'
    f'    <link rel="alternate" hreflang="en-bh" href="{SITE}/ae/">\n'
    f'    <link rel="alternate" hreflang="x-default" href="{SITE}/">\n'
)

def rootify(s):
    """Relative refs break one level down, so make them root-relative."""
    def fix(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r'https?:|//|#|mailto:|tel:|data:|/', val):
            return m.group(0)
        for old, new in LINK_MAP.items():
            if val == old:
                return f'{attr}="{new}"'
            if val.startswith(old + '#'):
                return f'{attr}="{new}{val[len(old):]}"'
        return f'{attr}="/{val}"'
    s = re.sub(r'\b(href|src)="([^"]+)"', fix, s)
    # background images inside style attributes
    s = re.sub(r"url\('(?!https?:|/|data:)([^']+)'\)", lambda m: f"url('/{m.group(1)}')", s)
    return s

for src, path, lang, label in MOVES:
    s = open(os.path.join(ROOT, src), encoding='utf-8').read()
    s = rootify(s)

    new_url = f'{SITE}/{path}/'
    s = re.sub(r'<link rel="canonical" href="[^"]*">',
               f'<link rel="canonical" href="{new_url}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">',
               f'<meta property="og:url" content="{new_url}">', s, count=1)
    # replace the whole hreflang cluster with the path-based one
    s = re.sub(r'([ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*)+',
               HREFLANG, s, count=1)

    outdir = os.path.join(ROOT, path)
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, 'index.html'), 'w', encoding='utf-8').write(s)
    print(f'wrote {path}/index.html  ({len(s):,} bytes)')

    # old URL becomes a canonicalising stub
    stub = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<title>WeddingClickz {label} — moved to /{path}/</title>
<link rel="canonical" href="{new_url}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={new_url}">
<script>location.replace("{new_url}");</script>
</head>
<body>
<p>This page now lives at <a href="{new_url}">{new_url}</a>.</p>
</body>
</html>
"""
    open(os.path.join(ROOT, src), 'w', encoding='utf-8').write(stub)
    print(f'  {src} -> stub redirecting to /{path}/')
