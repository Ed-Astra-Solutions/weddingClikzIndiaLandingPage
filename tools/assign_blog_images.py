"""
Assigns real photographs to every blog post: a cover for the listing card and
one or two inline images inside the post.

Rules that matter:
  - India-focused posts get images from the region=IN archive (blog/images/india),
    which is the only verified-India material we hold. assets/gallery came from
    region=UAE, so it must never caption an India post.
  - Alt text may only claim a location the archive metadata actually records
    (Bangalore, Goa, Dubai, Abu Dhabi). Posts about Udaipur, Kerala or Jaipur get
    truthful generic alt text instead of a fabricated location claim.
  - Every post gets distinct images; nothing is reused across posts.

Run: python3 assign_blog_images.py   (writes blog_image_plan.json)
"""
import json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IND  = os.path.join(ROOT, 'blog/images/india')

man    = {m['file']: m for m in json.load(open(os.path.join(IND, '_manifest.json')))}
orient = json.load(open(os.path.join(IND, '_orient.json')))

# Dubai/Abu Dhabi shots inside the India archive belong to the UAE pool.
ind_land = [f for f in orient['landscape'] if man[f]['place'] in ('Bangalore', 'Goa')]
ind_port = [f for f in orient['portrait']  if man[f]['place'] in ('Bangalore', 'Goa')]

# blog/images holds the purpose-shot UAE set; assets/gallery is also region=UAE
# material, and widening the pool with it keeps every UAE post's images distinct.
# Files named after an article rather than its content ("how-to-choose-...")
# cannot yield honest alt text, so they stay out of the pool.
TOPIC_NAMED = ('how-to-choose-',)
UAE_POOL = ([('blog/images/' + os.path.basename(p))
             for p in sorted(glob.glob(os.path.join(ROOT, 'blog/images/*.jpg')))] +
            [('assets/gallery/' + os.path.basename(p))
             for p in sorted(glob.glob(os.path.join(ROOT, 'assets/gallery/*.jpg')))])
UAE_POOL = [r for r in UAE_POOL if not os.path.basename(r).startswith(TOPIC_NAMED)]

# Posts set in the UAE, including Indian weddings held in Dubai.
UAE_POSTS = {
 'business-bay-canal-golden-hour.html','business-bay-light-line.html',
 'business-bay-rooftop-photography-floors.html','candid-vs-traditional-wedding-photography.html',
 'dubai-golden-hour-33-minutes.html','dubai-wedding-photographer-guide.html',
 'how-to-choose-wedding-photographer-uae.html','pre-wedding-shoot-locations-abu-dhabi.html',
 'pre-wedding-shoot-locations-dubai.html','wedding-photographer-abu-dhabi.html',
 'wedding-photography-bahrain.html','indian-wedding-photographer-dubai-abu-dhabi.html',
 'indian-wedding-photographers-dubai.html',
}

# What each post is about, for alt text that describes the picture honestly.
SUBJECT = {
 'best-pre-wedding-shoot-locations-bangalore.html': 'a couple before their wedding',
 'candid-vs-traditional-wedding-photography-india.html': 'a candid, unposed wedding moment',
 'destination-wedding-photographer-india.html': 'a destination wedding celebration',
 'destination-wedding-photography-india-guide.html': 'a destination wedding celebration',
 'drone-wedding-photography-india-2025.html': 'a wedding celebration',
 'drone-wedding-photography-india.html': 'a wedding celebration',
 'how-to-choose-wedding-photographer-india.html': 'a wedding ceremony',
 'kerala-wedding-photography-guide.html': 'a South Indian wedding ritual',
 'marwari-wedding-photography-guide.html': 'a traditional Indian wedding ritual',
 'pre-wedding-shoot-ideas-india-2025.html': 'a couple portrait',
 'south-indian-wedding-photography-guide.html': 'a South Indian wedding ceremony',
 'south-indian-wedding-photography.html': 'a South Indian wedding ceremony',
 'udaipur-destination-wedding-photographer.html': 'a destination wedding celebration',
 'wedding-cinematography-india-highlight-film-guide.html': 'a wedding celebration',
 'wedding-photography-checklist-india.html': 'a wedding day moment',
 'wedding-photography-cost-bangalore.html': 'a wedding ceremony',
 'wedding-photography-cost-india-2025.html': 'a wedding ceremony',
 'wedding-photography-shot-list-india.html': 'a wedding day moment',
 'wedding-photography-trends-india-2025-2026.html': 'a wedding celebration',
 'wedding-reels-instagram-couple-shoot-india.html': 'a couple portrait',
}

# Three phrasings so a post never repeats the same alt string, which is both an
# accessibility problem and a duplicate-content smell.
FRAMES = [
    "{S} photographed in {pl} by WeddingClickz",
    "{S} during a {pl} wedding, shot by the WeddingClickz team",
    "WeddingClickz coverage of {s} at a {pl} wedding",
]
def alt_for(post, f, slot=0):
    subj = SUBJECT.get(post, 'a wedding')
    pl = man[f]['place']            # only Bangalore and Goa are verified here
    return FRAMES[slot % len(FRAMES)].format(
        S=subj[0].upper() + subj[1:], s=subj, pl=pl)

def existing_inline(post):
    """How many images the post body already has. Posts that are already
    illustrated are left untouched."""
    s = open(os.path.join(ROOT, 'blog', post), encoding='utf-8').read()
    m = re.search(r'<article class="post-content">(.*?)</article>', s, re.S)
    return len(re.findall(r'<img', m.group(1))) if m else 0

posts = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, 'blog/*.html')))
ALREADY = {p for p in posts if existing_inline(p) > 0}
india_posts = [p for p in posts if p not in UAE_POSTS]

plan, li, pi = {}, 0, 0
for p in india_posts:
    cover  = ind_land[li % len(ind_land)]; li += 1
    if p in ALREADY:
        inline = []
    else:
        inline = [ind_land[li % len(ind_land)], ind_port[pi % len(ind_port)]]
        li += 1; pi += 1
    plan[p] = {
        'pool': 'india',
        'cover': {'src': f'blog/images/india/{cover}', 'alt': alt_for(p, cover, 0)},
        'inline': [{'src': f'blog/images/india/{f}', 'alt': alt_for(p, f, k + 1)}
                   for k, f in enumerate(inline)],
    }

# UAE posts keep their existing covers; they only need inline images.
# Match UAE posts to UAE images by place keyword, so a Dubai post does not get
# an Abu Dhabi photograph. Falls back to the general pool once a bucket is spent.
PLACE_KEYS = {
    'business-bay': ['dubai'], 'dubai': ['dubai'],
    'abu-dhabi':    ['abu-dhabi'], 'bahrain': ['bahrain'],
    'uae':          ['uae'],
}
UAE_LABEL = {'dubai': 'Dubai', 'abu-dhabi': 'Abu Dhabi',
             'bahrain': 'Bahrain', 'uae': 'the UAE'}

PLACE_CAPS = {'dubai': 'Dubai', 'abu': 'Abu', 'dhabi': 'Dhabi', 'uae': 'UAE',
              'bahrain': 'Bahrain', 'gcc': 'GCC', 'nikah': 'Nikah',
              'indian': 'Indian', 'muslim': 'Muslim', 'christian': 'Christian',
              'sikh': 'Sikh', 'hindu': 'Hindu', 'anand': 'Anand', 'karaj': 'Karaj'}

def describe(rel):
    """Turn a descriptive filename into a sentence. Accurate by construction,
    because the filename is what the image actually shows."""
    base = os.path.splitext(os.path.basename(rel))[0]
    base = re.sub(r'[-_]+', ' ', base)
    base = re.sub(r'\b\d+\b', '', base).strip()
    words = [PLACE_CAPS.get(w.lower(), w) for w in base.split()]
    txt = ' '.join(words).strip()
    return txt[0].upper() + txt[1:] if txt else 'Wedding photography'

used = set()
def pick_uae(post, n):
    keys = next((v for k, v in PLACE_KEYS.items() if k in post), ['uae'])
    out = []
    for kw in keys + ['']:
        for rel in UAE_POOL:
            if len(out) == n: break
            if rel in used or rel in out: continue
            if kw and kw not in os.path.basename(rel): continue
            out.append(rel)
        if len(out) == n: break
    used.update(out)
    return out

def place_of(post):
    for k, v in PLACE_KEYS.items():
        if k in post: return UAE_LABEL[v[0]]
    return 'the UAE'

for p in sorted(UAE_POSTS):
    if p in ALREADY:
        plan[p] = {'pool': 'uae', 'cover': None, 'inline': []}
        continue
    picks = pick_uae(p, 2)
    plan[p] = {'pool': 'uae', 'cover': None, 'inline': [
        {'src': rel, 'alt': f'{describe(rel)} by WeddingClickz'} for rel in picks]}

json.dump(plan, open(os.path.join(HERE, 'blog_image_plan.json'), 'w'), indent=1)
ni = sum(len(v['inline']) for v in plan.values())
nc = sum(1 for v in plan.values() if v['cover'])
print(f"planned {len(plan)} posts | {nc} cover swaps | {ni} inline images added")
print(f"left alone (already illustrated): {len(ALREADY)} -> {sorted(ALREADY)}")
allf = [i['src'] for v in plan.values() for i in v['inline']] + \
       [v['cover']['src'] for v in plan.values() if v['cover']]
print(f"images referenced {len(allf)}, distinct {len(set(allf))}")
