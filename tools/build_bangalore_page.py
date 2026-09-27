"""
Builds ../pre-wedding-shoot-bangalore.html.

This page sells the shoot: pictures first, then what the day feels like and what
you walk away with. The computed light research that used to lead this page now
lives at /blog/bangalore-golden-hour-28-minutes.html and is linked from a short
planning note, so it keeps earning links without dominating a page whose job is
to show couples the work.

Image rule: only frames that actually read as India are used here. The
region=IN pre-wedding set also contains overseas shoots (Bali), which are
excluded by hand in INDIA_SAFE below. Captions never claim a location, because
the pre-wedding API records none.

    python3 bangalore_light.py && python3 build_bangalore_page.py
"""
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
D    = json.load(open(os.path.join(HERE, 'bangalore_light.json')))
MON  = D['monthly']
CSS  = open(os.path.join(HERE, '_shared_css.html')).read()
URL  = "https://weddingclickz.com/pre-wedding-shoot-bangalore.html"
names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

GMIN = min([MON[m]['morning_min'] for m in names] + [MON[m]['evening_min'] for m in names])
GMAX = max([MON[m]['morning_min'] for m in names] + [MON[m]['evening_min'] for m in names])

# 03/04/05/15/16 are overseas shoots in the same feed - never used on this page.
INDIA_SAFE = [1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21]
def img(n): return f"assets/prewedding-in/prewedding-{n:02d}.jpg"

# Descriptions of what is visibly in each frame. No location claims.
CAPTION = {
 1:  "Hands and a turn, caught mid-movement",
 2:  "Quiet moment under trees",
 6:  "A heritage courtyard, and room to move in it",
 7:  "Late-afternoon light through a colonnade",
 8:  "Dust, a bike and a long lens",
 9:  "The same session, backlit",
 10: "Last light through the canopy",
 11: "Close, unposed, shallow focus",
 12: "Estate country, an easy drive from the city",
 13: "Shade, greenery and a clean wall",
 14: "Sitting, talking, barely aware of the camera",
 17: "Open field, low sun, nothing else in frame",
 18: "Silhouette against a breaking sky",
 19: "Foliage as a frame",
 20: "Green steps, shot from distance",
 21: "Balloons, and a couple not taking it too seriously",
}

HERO = 17
GALLERY = [8, 12, 18, 6, 17, 10, 13, 2, 20, 9, 11, 21, 7, 19, 14, 1]

def gallery_html():
    out = []
    for i, n in enumerate(GALLERY):
        tall = ' tall' if i % 5 in (0, 3) else ''
        out.append(
            f'        <figure class="shot{tall}" data-i="{i}">'
            f'<img src="{img(n)}" alt="Pre-wedding couple shoot by WeddingClickz — {CAPTION[n].lower()}" '
            f'loading="lazy" decoding="async">'
            f'<figcaption>{CAPTION[n]}</figcaption></figure>')
    return "\n".join(out)

STEPS = [
 ("One call, before anything is booked",
  "We ask what you actually like &mdash; and what you hate. Most couples know the second "
  "better than the first, and it is more useful. Out of that we suggest two or three "
  "locations rather than fifteen, and tell you which months suit them.",
  13),
 ("A morning, not a marathon",
  "One location per shoot. Four to five hours, starting early. You change once or twice, we "
  "walk, we talk, and the camera mostly stays out of your way. The pictures people keep are "
  "almost never the ones where someone was being told how to stand.",
  14),
 ("We handle the access",
  "Permits, location fees, estate permissions, the 04:30 alarm and the flask of coffee. You "
  "turn up dressed. Rules in Bangalore's public gardens changed in 2025 and we track them, "
  "so nobody gets turned away at a gate on the morning.",
  6),
 ("Edited, not filtered",
  "A teaser within a week while you still want to send it to everyone. The full set in three "
  "to four weeks, colour-graded by hand. No presets sprayed over everything, no watermark "
  "across your own faces.",
  10),
]
def steps_html():
    return "\n".join(
        f'''            <article class="step">
                <div class="step-img"><img src="{img(n)}" alt="Pre-wedding couple shoot by WeddingClickz" loading="lazy" decoding="async"></div>
                <div class="step-copy"><span class="step-n">{i:02d}</span><h3>{t}</h3><p>{b}</p></div>
            </article>''' for i, (t, b, n) in enumerate(STEPS, 1))

GET = [
 ("80&ndash;120", "edited photographs", "the full set, hand colour-graded"),
 ("1 teaser", "within 7 days", "a short reel, ready to post"),
 ("4&ndash;5 hrs", "on location", "one location, unhurried"),
 ("Full rights", "to your own pictures", "print them, post them, no watermark"),
]
def get_html():
    return "\n".join(
        f'                <div class="get-card"><strong>{a}</strong><span>{b}</span><em>{c}</em></div>'
        for a, b, c in GET)

PRICE = [
 ("City studio", "4 hours, one photographer, one set", "Rs 15,000 &ndash; 35,000"),
 ("City outdoor", "1&ndash;2 shooters, 80&ndash;120 edits, reel", "Rs 40,000 &ndash; 90,000"),
 ("Day trip", "Nandi Hills or Hesaraghatta, full team, drone, film", "Rs 75,000 &ndash; 1,50,000"),
 ("Weekend away", "Coorg, Chikmagalur or Hampi &mdash; 2 days, travel included", "Rs 1,50,000 &ndash; 3,50,000"),
]
def price_html():
    return "\n".join(
        f'<tr><th scope="row">{a}</th><td>{b}</td><td class="price">{c}</td></tr>'
        for a, b, c in PRICE)

FAQ = [
 ("How long does it take, start to finish?",
  "Four to five hours on the day, one location. A teaser reel lands within seven days and the "
  "full edited set in three to four weeks."),
 ("Do we have to be good in front of a camera?",
  "No, and almost nobody is. The first half hour is deliberately throwaway &mdash; that is "
  "when people stop performing. Everything worth keeping comes after."),
 ("Where can we shoot?",
  "Nandi Hills, Hesaraghatta, Bangalore Palace, private estates and resorts, coffee country in "
  "Coorg or Chikmagalur, and indoor sets. Lalbagh and Cubbon Park are closed to pre-wedding "
  "shoots since a November 2025 Horticulture Department order, so anyone still offering you "
  "those has not read it."),
 ("What does it cost?",
  "Rs 15,000&ndash;35,000 for a studio session, Rs 40,000&ndash;90,000 for a city outdoor "
  "shoot, Rs 75,000&ndash;1,50,000 for a day trip with a film crew, and "
  "Rs 1,50,000&ndash;3,50,000 for a weekend away. Permits and location fees are billed at cost."),
 ("When should we book?",
  "Six to ten weeks out, and longer for a weekend between November and February &mdash; that is "
  "both the best light and the busiest season. If your wedding is already close, ask anyway; we "
  "keep a few short-notice mornings each month."),
 ("What is the best time of year?",
  f"November to February, comfortably. The golden window here is only {GMIN}&ndash;{GMAX} "
  "minutes long whatever the month, but winter gives you a late enough sunrise to actually reach "
  "a location before it opens. We wrote up the numbers if you like that sort of thing."),
]
def faq_html():
    return "\n".join(
        f'''                <details class="faq-item"{" open" if i == 0 else ""}>
                    <summary>{q} <span class="faq-icon">+</span></summary>
                    <div class="faq-answer"><p>{a}</p></div>
                </details>''' for i, (q, a) in enumerate(FAQ))

import html as _h
def faq_schema():
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": _h.unescape(q),
         "acceptedAnswer": {"@type": "Answer", "text": _h.unescape(a)}} for q, a in FAQ]},
        indent=2, ensure_ascii=False)

SERVICE = {
 "@context": "https://schema.org", "@type": "Service", "@id": URL + "#service",
 "serviceType": "Pre-wedding photography and film",
 "name": "Pre-Wedding Shoots in Bangalore",
 "description": "Pre-wedding photo and film shoots in and around Bangalore — one location, "
                "four to five hours, 80–120 edited photographs and a teaser reel within a week.",
 "url": URL, "provider": {"@id": "https://weddingclickz.com/#business"},
 "areaServed": [{"@type": "City", "name": "Bangalore"},
                {"@type": "AdministrativeArea", "name": "Karnataka"}],
 "audience": {"@type": "Audience", "audienceType": "Engaged couples"},
 "offers": [
   {"@type": "Offer", "name": "City studio session (4 hours)", "priceCurrency": "INR",
    "priceSpecification": {"@type": "PriceSpecification", "minPrice": 15000, "maxPrice": 35000, "priceCurrency": "INR"}},
   {"@type": "Offer", "name": "City outdoor shoot", "priceCurrency": "INR",
    "priceSpecification": {"@type": "PriceSpecification", "minPrice": 40000, "maxPrice": 90000, "priceCurrency": "INR"}},
   {"@type": "Offer", "name": "Day trip (Nandi Hills / Hesaraghatta)", "priceCurrency": "INR",
    "priceSpecification": {"@type": "PriceSpecification", "minPrice": 75000, "maxPrice": 150000, "priceCurrency": "INR"}},
   {"@type": "Offer", "name": "Weekend shoot (Coorg / Chikmagalur / Hampi)", "priceCurrency": "INR",
    "priceSpecification": {"@type": "PriceSpecification", "minPrice": 150000, "maxPrice": 350000, "priceCurrency": "INR"}}]}
BREAD = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
 {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://weddingclickz.com/"},
 {"@type": "ListItem", "position": 2, "name": "Pre-Wedding Shoots", "item": "https://weddingclickz.com/pre-wedding-shoots.html"},
 {"@type": "ListItem", "position": 3, "name": "Pre-Wedding Shoot in Bangalore", "item": URL}]}
GALLERY_LD = {"@context": "https://schema.org", "@type": "ImageGallery", "@id": URL + "#gallery",
 "name": "Pre-wedding shoots by WeddingClickz",
 "associatedMedia": [{"@type": "ImageObject",
   "contentUrl": f"https://weddingclickz.com/{img(n)}",
   "caption": CAPTION[n],
   "creator": {"@id": "https://weddingclickz.com/#business"},
   "copyrightHolder": {"@id": "https://weddingclickz.com/#business"}} for n in GALLERY]}

EXTRA_CSS = """
    <style>
        /* This page leads with pictures, so the gallery gets the real estate and
           the prose is kept deliberately short. */
        .lede { max-width: 680px; margin: 0 auto; text-align: center; }
        .lede p { font-size: 1.02rem; color: var(--text-light); }

        /* Masonry-ish grid: a few frames run tall so the wall is not a rigid table. */
        .gallery-wall {
            column-count: 4; column-gap: 10px; max-width: 1500px;
            margin: 0 auto; padding: 0 10px;
        }
        .gallery-wall .shot {
            break-inside: avoid; margin: 0 0 10px; position: relative;
            overflow: hidden; border-radius: 4px; cursor: zoom-in; background: #1a1a1a;
        }
        .gallery-wall .shot img {
            width: 100%; display: block; transition: transform .7s cubic-bezier(.2,.7,.3,1);
        }
        .gallery-wall .shot:hover img { transform: scale(1.045); }
        .gallery-wall figcaption {
            position: absolute; left: 0; right: 0; bottom: 0; padding: 1.6rem .9rem .8rem;
            font-size: .76rem; letter-spacing: .02em; color: #fff;
            background: linear-gradient(transparent, rgba(0,0,0,.72));
            opacity: 0; transform: translateY(6px); transition: all .35s ease;
        }
        .gallery-wall .shot:hover figcaption { opacity: 1; transform: none; }
        @media (max-width: 1100px) { .gallery-wall { column-count: 3; } }
        @media (max-width: 760px)  { .gallery-wall { column-count: 2; } }
        @media (max-width: 460px)  { .gallery-wall { column-count: 1; } }

        /* Alternating image/text steps for the experience section. */
        .steps-flow { max-width: 1120px; margin: 0 auto; display: grid; gap: 2.75rem; }
        .step { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; align-items: center; }
        .step:nth-child(even) .step-img { order: 2; }
        .step-img { overflow: hidden; border-radius: 6px; aspect-ratio: 4/3; }
        .step-img img { width: 100%; height: 100%; object-fit: cover; display: block; }
        .step-n {
            display: block; font-family: 'Cormorant Garamond', serif; font-size: 2.4rem;
            color: var(--gold); line-height: 1; margin-bottom: .5rem;
        }
        .step-copy { text-align: left; }
        .step-copy h3 { font-size: 1.6rem; margin-bottom: .7rem; }
        .step-copy p { color: var(--text-light); font-size: .96rem; }
        @media (max-width: 820px) {
            .step { grid-template-columns: 1fr; gap: 1.25rem; }
            .step:nth-child(even) .step-img { order: 0; }
        }

        /* What you walk away with. */
        .get-grid {
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;
            max-width: 1120px; margin: 0 auto;
        }
        .get-card {
            border: 1px solid rgba(201,168,124,.28); border-radius: 6px;
            padding: 1.6rem 1.2rem; text-align: center; background: var(--white);
        }
        .get-card strong {
            display: block; font-family: 'Cormorant Garamond', serif; font-size: 2rem;
            color: var(--gold-dark); line-height: 1.1;
        }
        .get-card span { display: block; font-size: .9rem; margin: .35rem 0 .5rem; font-weight: 500; }
        .get-card em { font-size: .8rem; color: var(--text-light); font-style: normal; }
        @media (max-width: 860px) { .get-grid { grid-template-columns: repeat(2, 1fr); } }

        /* Pricing */
        .price-table { width: 100%; border-collapse: collapse; max-width: 900px; margin: 0 auto; }
        .price-table th, .price-table td { padding: 1rem .9rem; text-align: left;
            border-bottom: 1px solid rgba(201,168,124,.22); font-size: .92rem; }
        .price-table tbody th { font-weight: 600; white-space: nowrap; }
        .price-table td.price { text-align: right; white-space: nowrap; color: var(--gold-dark); font-weight: 600; }
        @media (max-width: 620px) {
            .price-table thead { display: none; }
            .price-table tr { display: block; padding: .6rem 0; border-bottom: 1px solid rgba(201,168,124,.22); }
            .price-table th, .price-table td { display: block; border: 0; padding: .18rem 0; }
            .price-table td.price { text-align: left; }
        }

        /* Small planning note that points at the research post. */
        .note-strip {
            max-width: 820px; margin: 0 auto; border-left: 3px solid var(--gold);
            background: rgba(201,168,124,.08); padding: 1.15rem 1.35rem; font-size: .93rem;
        }
        .note-strip a { color: var(--gold-dark); font-weight: 600; }

        /* Lightbox */
        .lb { position: fixed; inset: 0; background: rgba(12,12,12,.96); z-index: 4000;
              display: none; align-items: center; justify-content: center; }
        .lb.open { display: flex; }
        .lb img { max-width: 92vw; max-height: 86vh; object-fit: contain; }
        .lb button { position: absolute; background: none; border: 0; color: #fff;
              font-size: 2rem; cursor: pointer; padding: .5rem 1rem; line-height: 1; }
        .lb .lb-x { top: 1rem; right: 1.2rem; }
        .lb .lb-p { left: .5rem; top: 50%; transform: translateY(-50%); }
        .lb .lb-n { right: .5rem; top: 50%; transform: translateY(-50%); }
        .lb .lb-cap { position: absolute; bottom: 1.1rem; left: 0; right: 0; text-align: center;
              color: rgba(255,255,255,.75); font-size: .82rem; }

        @media (max-width: 560px) {
            .header-container { padding: 0 1rem; }
            .logo-img { height: 38px; }
            .logo .logo-text { font-size: 1.2rem; }
            .nav-cta { padding: .5rem .9rem; font-size: .68rem; letter-spacing: .06em; }
        }
    </style>
"""

PAGE = f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-J09CVYG8EV"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-J09CVYG8EV');
    </script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="theme-color" content="#2C2C2C">

    <title>Pre-Wedding Shoot in Bangalore | WeddingClickz</title>
    <meta name="description" content="Pre-wedding shoots in and around Bangalore — see the work, then the details. One location, four to five hours, 80–120 edited photographs and a teaser within a week.">
    <meta name="keywords" content="pre wedding shoot Bangalore, pre wedding photoshoot Bangalore, couple photoshoot Bangalore, pre wedding shoot locations Bangalore, pre wedding shoot cost Bangalore, Nandi Hills pre wedding shoot">

    <link rel="canonical" href="{URL}">
    <link rel="alternate" hreflang="en-in" href="{URL}">
    <link rel="alternate" hreflang="x-default" href="{URL}">

    <meta name="language" content="English">
    <meta name="geo.region" content="IN-KA">
    <meta name="geo.placename" content="Bangalore, Karnataka, India">
    <meta name="geo.position" content="12.971600;77.594600">
    <meta name="ICBM" content="12.971600, 77.594600">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
    <meta name="author" content="WeddingClickz">

    <meta property="og:type" content="website">
    <meta property="og:url" content="{URL}">
    <meta property="og:title" content="Pre-Wedding Shoot in Bangalore | WeddingClickz">
    <meta property="og:description" content="One location, one morning, and pictures that look like the two of you. See the work.">
    <meta property="og:image" content="https://weddingclickz.com/{img(HERO)}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="800">
    <meta property="og:site_name" content="WeddingClickz">
    <meta property="og:locale" content="en_IN">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Pre-Wedding Shoot in Bangalore | WeddingClickz">
    <meta name="twitter:description" content="One location, one morning, and pictures that look like the two of you.">
    <meta name="twitter:image" content="https://weddingclickz.com/{img(HERO)}">

    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <script type="application/ld+json">
{json.dumps(SERVICE, indent=2, ensure_ascii=False)}
    </script>
    <script type="application/ld+json">
{json.dumps(GALLERY_LD, indent=2, ensure_ascii=False)}
    </script>
    <script type="application/ld+json">
{faq_schema()}
    </script>
    <script type="application/ld+json">
{json.dumps(BREAD, indent=2, ensure_ascii=False)}
    </script>

{CSS}
{EXTRA_CSS}
</head>
<body>

    <header id="header">
        <div class="header-container">
            <a href="/index.html" class="logo">
                <img src="/logo.png" alt="WeddingClickz" class="logo-img">
                <span class="logo-text">Wedding<span>Clickz</span></span>
            </a>
            <nav id="nav">
                <ul>
                    <li class="nav-mobile-only"><a href="/index.html">Home</a></li>
                    <li><a href="#work">The Work</a></li>
                    <li><a href="#how">How It Goes</a></li>
                    <li><a href="#cost">Cost</a></li>
                    <li><a href="/blog.html">Blog</a></li>
                    <li class="nav-mobile-only"><a href="/in/">India</a></li>
                    <li class="nav-mobile-only"><a href="/ae/">UAE</a></li>
                </ul>
            </nav>
            <div class="region-switch" aria-label="Choose your region">
                <a href="/in/" class="current" hreflang="en-IN">&#127470;&#127475; India</a>
                <a href="/ae/" hreflang="en-AE">&#127462;&#127466; UAE</a>
            </div>
            <a href="/index.html#contact" class="nav-cta">Check Your Date</a>
            <div class="mobile-menu-toggle" id="menuToggle"><span></span><span></span><span></span></div>
        </div>
    </header>

    <section class="hero" style="background: linear-gradient(rgba(20,20,20,.35), rgba(20,20,20,.62)), url('/{img(HERO)}') center/cover;">
        <div class="hero-inner">
            <span class="eyebrow">Bangalore &middot; Karnataka</span>
            <h1>Pre-Wedding Shoots in <em>Bangalore</em></h1>
            <p>One location. One morning. Pictures that look like the two of you rather than
               two people being told where to stand.</p>
            <div class="hero-actions">
                <a href="#work" class="btn btn-gold">See the Work</a>
                <a href="/index.html#contact" class="btn btn-outline">Check Your Date</a>
            </div>
        </div>
    </section>

    <section class="block" id="work" style="padding-bottom:3rem;">
        <div class="container">
            <div class="section-header lede" style="margin-bottom:2.5rem;">
                <span class="section-label">Recent work</span>
                <h2 class="section-title">The <em>Pictures</em></h2>
                <p>Estates, dust roads, courtyards and open fields &mdash; shot the way the
                   morning actually went.</p>
            </div>
        </div>
        <div class="gallery-wall" id="wall">
{gallery_html()}
        </div>
    </section>

    <section class="block" id="how" style="background:var(--white);">
        <div class="container">
            <div class="section-header lede" style="margin-bottom:3rem;">
                <span class="section-label">The experience</span>
                <h2 class="section-title">How the Morning <em>Actually Goes</em></h2>
            </div>
            <div class="steps-flow">
{steps_html()}
            </div>
        </div>
    </section>

    <section class="block">
        <div class="container">
            <div class="section-header lede" style="margin-bottom:2.5rem;">
                <span class="section-label">What you walk away with</span>
                <h2 class="section-title">What You <em>Get</em></h2>
            </div>
            <div class="get-grid">
{get_html()}
            </div>
            <div class="note-strip" style="margin-top:2.5rem;">
                <strong>One planning note.</strong> Golden light in Bangalore lasts about
                {GMIN}&ndash;{GMAX} minutes &mdash; not an hour &mdash; so we build the morning
                around it and shoot one location properly instead of three badly. If you want
                the arithmetic, we published
                <a href="/blog/bangalore-golden-hour-28-minutes.html">the full light tables</a>,
                including why a Nandi Hills sunrise only works between December and March.
            </div>
        </div>
    </section>

    <section class="block" id="cost" style="background:var(--white);">
        <div class="container">
            <div class="section-header lede" style="margin-bottom:2.5rem;">
                <span class="section-label">Cost</span>
                <h2 class="section-title">What It <em>Costs</em></h2>
                <p>Permits and location fees are billed at cost, never marked up.</p>
            </div>
            <table class="price-table">
                <thead><tr><th>Shoot</th><th>What it includes</th><th class="price">Typical</th></tr></thead>
                <tbody>
{price_html()}
                </tbody>
            </table>
        </div>
    </section>

    <section class="block faq">
        <div class="container">
            <div class="section-header lede" style="margin-bottom:2rem;">
                <span class="section-label">Questions</span>
                <h2 class="section-title">Before You <em>Ask</em></h2>
            </div>
            <div class="faq-list" style="max-width:820px;margin:0 auto;">
{faq_html()}
            </div>
        </div>
    </section>

    <section class="cta-banner">
        <h2>Tell Us Your <em>Date</em></h2>
        <p>Send the date and we will come back with the locations that suit it and what it costs.</p>
        <div class="hero-actions">
            <a href="/index.html#contact" class="btn btn-gold">Check Your Date</a>
            <a href="tel:+919740222927" class="btn btn-outline">Call +91 97402 22927</a>
        </div>
    </section>

    <div class="lb" id="lb" aria-hidden="true">
        <button class="lb-x" aria-label="Close">&times;</button>
        <button class="lb-p" aria-label="Previous">&#8249;</button>
        <img id="lbImg" src="" alt="">
        <button class="lb-n" aria-label="Next">&#8250;</button>
        <div class="lb-cap" id="lbCap"></div>
    </div>

    <footer>
        <div class="footer-grid">
            <div class="footer-brand">
                <h3>Wedding<span>Clickz</span></h3>
                <p>A wedding photography and film studio in Konanakunte, Bangalore, shooting
                   across Karnataka and India since 2014.</p>
                <div class="footer-contact">
                    <a href="tel:+919740222927">+91 97402 22927</a>
                    <a href="mailto:info@weddingclickz.com">info@weddingclickz.com</a>
                    <a href="https://maps.google.com/?q=ClayWorks+Shankaraa,+Kanakapura+Main+Rd,+Munireddy+Layout,+Konanakunte,+Bengaluru,+Karnataka+560062" target="_blank" rel="noopener noreferrer">ClayWorks Shankaraa, Konanakunte, Bengaluru 560062</a>
                </div>
            </div>
            <div class="footer-links">
                <h4>Pre-Wedding</h4>
                <ul>
                    <li><a href="/pre-wedding-shoot-bangalore.html">Pre-Wedding Bangalore</a></li>
                    <li><a href="/blog/best-pre-wedding-shoot-locations-bangalore.html">Locations Near Bangalore</a></li>
                    <li><a href="/blog/bangalore-golden-hour-28-minutes.html">Bangalore Light Tables</a></li>
                    <li><a href="/blog/pre-wedding-shoot-ideas-india-2025.html">Pre-Wedding Ideas</a></li>
                    <li><a href="/pre-wedding-shoots.html">Pre-Wedding Shoots (Dubai)</a></li>
                </ul>
            </div>
            <div class="footer-links">
                <h4>Get Started</h4>
                <ul>
                    <li><a href="/index.html#contact">Get a Quote</a></li>
                    <li><a href="/in/">Wedding Photographer India</a></li>
                    <li><a href="/blog/wedding-photography-cost-bangalore.html">Wedding Photography Cost</a></li>
                    <li><a href="/privacy-policy.html">Privacy Policy</a></li>
                    <li><a href="/terms-of-use.html">Terms of Use</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2026 WeddingClickz Photography. All rights reserved.</span>
            <span><a href="/privacy-policy.html">Privacy</a><a href="/terms-of-use.html">Terms</a><a href="/cookie-policy.html">Cookies</a></span>
        </div>
    </footer>

    <section class="city-strip">
        <h2>Pre-Wedding and Wedding Photography Around Bangalore</h2>
        <p>
            <a href="/blog/best-pre-wedding-shoot-locations-bangalore.html">Pre-Wedding Shoot Locations Near Bangalore</a> &middot;
            <a href="/blog/bangalore-golden-hour-28-minutes.html">Bangalore's Golden Hour Is {GMIN} Minutes</a> &middot;
            <a href="/blog/wedding-photography-cost-bangalore.html">Wedding Photography Cost in Bangalore</a> &middot;
            <a href="/blog/pre-wedding-shoot-ideas-india-2025.html">Pre-Wedding Shoot Ideas</a> &middot;
            <a href="/blog/wedding-reels-instagram-couple-shoot-india.html">Couple Reels</a> &middot;
            <a href="/blog/south-indian-wedding-photography-guide.html">South Indian Wedding Photography</a> &middot;
            <a href="/in/">Wedding Photographer India</a>
        </p>
    </section>

    <script>
        const header = document.getElementById('header');
        window.addEventListener('scroll', () => header.classList.toggle('scrolled', window.scrollY > 40));
        document.getElementById('menuToggle').addEventListener('click', () =>
            document.getElementById('nav').classList.toggle('open'));

        // Gallery lightbox
        (function () {{
            const shots = Array.from(document.querySelectorAll('#wall .shot'));
            const lb = document.getElementById('lb');
            const im = document.getElementById('lbImg');
            const cap = document.getElementById('lbCap');
            let i = 0;
            function show(n) {{
                i = (n + shots.length) % shots.length;
                const img = shots[i].querySelector('img');
                im.src = img.src; im.alt = img.alt;
                cap.textContent = shots[i].querySelector('figcaption').textContent;
            }}
            function open(n) {{ show(n); lb.classList.add('open'); lb.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden'; }}
            function close() {{ lb.classList.remove('open'); lb.setAttribute('aria-hidden','true'); document.body.style.overflow=''; }}
            shots.forEach((s, n) => s.addEventListener('click', () => open(n)));
            lb.querySelector('.lb-x').addEventListener('click', close);
            lb.querySelector('.lb-p').addEventListener('click', e => {{ e.stopPropagation(); show(i-1); }});
            lb.querySelector('.lb-n').addEventListener('click', e => {{ e.stopPropagation(); show(i+1); }});
            lb.addEventListener('click', e => {{ if (e.target === lb) close(); }});
            document.addEventListener('keydown', e => {{
                if (!lb.classList.contains('open')) return;
                if (e.key === 'Escape') close();
                if (e.key === 'ArrowLeft') show(i-1);
                if (e.key === 'ArrowRight') show(i+1);
            }});
        }})();
    </script>
</body>
</html>
"""

out = os.path.join(ROOT, 'pre-wedding-shoot-bangalore.html')
open(out, 'w', encoding='utf-8').write(PAGE)
import re
words = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', PAGE, flags=re.S)).split())
print(f"wrote {out} ({len(PAGE):,} bytes) | gallery {len(GALLERY)} images | visible words ~{words}")
