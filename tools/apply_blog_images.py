"""
Applies blog_image_plan.json to the blog posts.

Per post:
  - swaps the .post-cover image (India posts only, where the old cover was a
    UAE photograph standing in for India)
  - points og:image, twitter:image and the Article schema "image" at that real
    cover instead of the generic og-image.jpg
  - inserts one or two <figure> blocks spread through the body, matching the
    markup already used by the six hand-illustrated posts

Run: python3 apply_blog_images.py [--dry]
"""
import json, os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PLAN = json.load(open(os.path.join(HERE, 'blog_image_plan.json')))
DIMS = json.load(open(os.path.join(HERE, '_dims.json')))
DRY  = '--dry' in sys.argv
SITE = 'https://weddingclickz.com/'

FIG = ('<figure style="margin:2.2rem 0;">'
       '<img src="/{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" '
       'style="width:100%;max-height:600px;object-fit:cover;border-radius:8px;">'
       '<figcaption style="font-size:.8rem;opacity:.6;text-align:center;margin-top:.55rem;">'
       '{alt}</figcaption></figure>')

def dims(src):
    return DIMS.get(src, [1200, 800])

changed = cov_n = fig_n = 0
for post, spec in sorted(PLAN.items()):
    path = os.path.join(ROOT, 'blog', post)
    s = orig = open(path, encoding='utf-8').read()

    # ---- cover ----
    if spec['cover']:
        src, alt = spec['cover']['src'], spec['cover']['alt']
        w, h = dims(src)
        m = re.search(r'(<div class="post-cover">\s*<img)([^>]*)(>)', s, re.S)
        if m:
            new_img = (f'{m.group(1)} src="/{src}" alt="{alt}" '
                       f'width="{w}" height="{h}" fetchpriority="high"{m.group(3)}')
            s = s[:m.start()] + new_img + s[m.end():]
            cov_n += 1
        abs_url = SITE + src
        s = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
                   lambda mm: mm.group(1) + abs_url + mm.group(2), s, count=1)
        s = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")',
                   lambda mm: mm.group(1) + abs_url + mm.group(2), s, count=1)
        s = re.sub(r'("image"\s*:\s*")[^"]*(")',
                   lambda mm: mm.group(1) + abs_url + mm.group(2), s, count=1)

    # ---- inline figures, spread through the body ----
    if spec['inline']:
        am = re.search(r'(<article class="post-content">)(.*?)(</article>)', s, re.S)
        if am:
            head, body, tail = am.group(1), am.group(2), am.group(3)
            # candidate insertion points: just before an <h2>
            pts = [m.start() for m in re.finditer(r'<h2', body)]
            figs = [FIG.format(src=i['src'], alt=i['alt'],
                               w=dims(i['src'])[0], h=dims(i['src'])[1])
                    for i in spec['inline']]
            if len(pts) >= 2:
                # spread: roughly one third and two thirds through the headings
                idx = sorted({max(1, len(pts)//3), max(2, (2*len(pts))//3)})
                idx = [i for i in idx if i < len(pts)][:len(figs)]
            else:
                idx = []
            if idx:
                for off, (i, fig) in enumerate(zip(idx, figs)):
                    at = pts[i] + sum(len(f) for f in figs[:off])
                    body = body[:at] + fig + '\n\n' + body[at:]
            else:   # short post with few headings: append before the end
                body = body + '\n' + '\n'.join(figs)
            fig_n += len(figs)
            s = s[:am.start()] + head + body + tail + s[am.end():]

    if s != orig:
        changed += 1
        if not DRY:
            shutil.copy(path, path + '.bak')
            open(path, 'w', encoding='utf-8').write(s)

print(f"{'DRY RUN: ' if DRY else ''}{changed} posts changed | {cov_n} covers | {fig_n} figures")
