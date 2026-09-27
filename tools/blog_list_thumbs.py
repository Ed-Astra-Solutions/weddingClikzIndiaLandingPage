"""
Gives every card on blog.html a thumbnail, using that post's own cover image so
the listing and the article always agree.

Run: python3 blog_list_thumbs.py
"""
import re, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BLOG = os.path.join(ROOT, 'blog.html')
DIMS = json.load(open(os.path.join(HERE, '_dims.json')))

def cover_of(href):
    post = os.path.join(ROOT, href.lstrip('/'))
    if not os.path.exists(post):
        return None
    s = open(post, encoding='utf-8').read()
    m = re.search(r'<div class="post-cover">\s*<img[^>]*?src="([^"]+)"[^>]*?alt="([^"]*)"', s, re.S)
    return (m.group(1), m.group(2)) if m else None

s = open(BLOG, encoding='utf-8').read()

# 1. thumbnail markup inside each card
def card(m):
    open_tag, href, inner = m.group(1), m.group(2), m.group(3)
    if 'fg-thumb' in inner:
        return m.group(0)
    cv = cover_of(href)
    if not cv:
        return m.group(0)
    src, alt = cv
    w, h = DIMS.get(src.lstrip('/'), [1200, 800])
    thumb = (f'\n                    <img class="fg-thumb" src="{src}" alt="{alt}" '
             f'width="{w}" height="{h}" loading="lazy" decoding="async">')
    return open_tag + thumb + inner + '</a>'

s, n = re.subn(r'(<a class="fg-card" href="([^"]+)">)(.*?)</a>', card, s, flags=re.S)

# 2. styling for the thumbnail, appended to the page's own stylesheet
css = """
        /* Listing thumbnails: each card shows its post's real cover image. */
        .fg-card { padding: 0; overflow: hidden; display: flex; flex-direction: column; }
        .fg-thumb {
            width: 100%; height: 190px; object-fit: cover; display: block;
            border-bottom: 1px solid var(--border-subtle);
            transition: transform 0.5s ease;
        }
        .fg-card > .fg-cat { margin-top: 1.25rem; }
        .fg-card > .fg-cat, .fg-card > h3, .fg-card > p { padding-inline: 1.5rem; }
        .fg-card > p { padding-bottom: 1.5rem; }
        .fg-card:hover .fg-thumb { transform: scale(1.05); }
        @media (max-width: 700px) { .fg-thumb { height: 200px; } }
"""
marker = '.fg-card p {'
i = s.index(marker)
end = s.index('}', i) + 1
s = s[:end] + '\n' + css + s[end:]

open(BLOG, 'w', encoding='utf-8').write(s)
print(f"added thumbnails to {n} cards")
missing = [h for h in re.findall(r'<a class="fg-card" href="([^"]+)"', s) if not cover_of(h)]
print("cards without a resolvable cover:", missing or "none")
