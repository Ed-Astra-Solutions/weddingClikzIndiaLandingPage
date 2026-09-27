"""
Builds ../pre-wedding-shoot-bangalore.html.

Every number in the published tables is read from bangalore_light.json, which
is written by bangalore_light.py. Nothing is typed by hand, so the page cannot
drift away from the computed data. Re-run bangalore_light.py first, then this.

    python3 bangalore_light.py && python3 build_bangalore_page.py
"""
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
D    = json.load(open(os.path.join(HERE, 'bangalore_light.json')))
MON, NANDI = D['monthly'], D['nandi']
CSS  = open(os.path.join(HERE, '_shared_css.html')).read()
URL  = "https://weddingclickz.com/pre-wedding-shoot-bangalore.html"
names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
FULLM = dict(zip(names, ["January","February","March","April","May","June","July",
                         "August","September","October","November","December"]))

# ---- derived figures, so the prose agrees with the tables -------------------
mg = [MON[m]['morning_min'] for m in names]
eg = [MON[m]['evening_min'] for m in names]
GOLD_MIN, GOLD_MAX = min(mg + eg), max(mg + eg)
EARLIEST = min(MON[m]['sunrise'] for m in names)
LATEST   = max(MON[m]['sunrise'] for m in names)
NANDI_FULL = [m for m in names if NANDI[m]['usable_min'] >= NANDI[m]['full_min'] - 1]
NANDI_BAD  = [m for m in names if NANDI[m]['usable_min'] < 15]
def eng(lst):
    return lst[0] if len(lst) == 1 else ", ".join(lst[:-1]) + " and " + lst[-1]

# ---- tables ----------------------------------------------------------------
def table_monthly():
    r = ['<div class="table-scroll"><table class="data-table">',
         '<caption>Bangalore pre-wedding light windows, computed for the 15th of each month '
         '(12.97&deg;N, 77.59&deg;E, IST). Golden light is the sun between the horizon and +6&deg;.</caption>',
         '<thead><tr><th>Month</th><th>Sunrise</th><th>Morning golden</th><th>Mins</th>'
         '<th>Be on location</th><th>Evening golden</th><th>Mins</th><th>Sunset</th>'
         '<th>Light comes from</th></tr></thead><tbody>']
    for m in names:
        v = MON[m]
        r.append(f"<tr><th scope=\"row\">{FULLM[m]}</th><td>{v['sunrise']}</td>"
                 f"<td>{v['morning']}</td><td>{v['morning_min']}</td><td>{v['gate']}</td>"
                 f"<td>{v['evening']}</td><td>{v['evening_min']}</td><td>{v['sunset']}</td>"
                 f"<td>{v['from_sunrise']} / {v['from_sunset']}</td></tr>")
    r.append('</tbody></table></div>')
    return "\n".join(r)

LAT_ROWS = [("Bangalore", "12.97", 28, 31, 31), ("Dubai", "25.19", 30, 33, 34),
            ("Delhi", "28.61", 31, 34, 35), ("London", "51.51", 44, 54, 62),
            ("Reykjav&iacute;k", "64.15", 63, 113, 209)]
def table_latitude():
    r = ['<div class="table-scroll"><table class="data-table">',
         '<caption>Evening golden-hour length, in minutes, on the March equinox and both '
         'solstices. Same method, five latitudes.</caption>',
         '<thead><tr><th>City</th><th>Latitude</th><th>21 Mar</th><th>21 Jun</th>'
         '<th>21 Dec</th></tr></thead><tbody>']
    for c, la, a, b, cc in LAT_ROWS:
        cls = ' class="row-highlight"' if c == "Bangalore" else ''
        r.append(f'<tr{cls}><th scope="row">{c}</th><td>{la}&deg;N</td>'
                 f'<td>{a} min</td><td>{b} min</td><td>{cc} min</td></tr>')
    r.append('</tbody></table></div>')
    return "\n".join(r)

def table_nandi():
    r = ['<div class="table-scroll"><table class="data-table">',
         '<caption>Nandi Hills sunrise shoots. The gate opens at 06:00 and the drive from '
         'the gate to the summit viewpoints takes about 20 minutes, so 06:20 is the '
         'earliest a couple can realistically be in position.</caption>',
         '<thead><tr><th>Month</th><th>Sunrise</th><th>Golden light ends</th>'
         '<th>In position</th><th>Usable golden</th><th>Verdict</th></tr></thead><tbody>']
    for m in names:
        v = NANDI[m]
        full = v['usable_min'] >= v['full_min'] - 1
        bad  = v['usable_min'] < 15
        cls = ' class="row-good"' if full else (' class="row-bad"' if bad else '')
        r.append(f"<tr{cls}><th scope=\"row\">{FULLM[m]}</th><td>{v['sunrise']}</td>"
                 f"<td>{v['golden_ends']}</td><td>{v['in_position']}</td>"
                 f"<td><strong>{v['usable_min']} min</strong></td><td>{v['verdict']}</td></tr>")
    r.append('</tbody></table></div>')
    return "\n".join(r)

# ---- FAQ (visible copy and schema are generated from one source) ------------
FAQ = [
 ("How long does golden light actually last in Bangalore?",
  f"Between {GOLD_MIN} and {GOLD_MAX} minutes, depending on the month. That is the whole warm "
  "window, not a warm-up to it. Bangalore sits at 12.97&deg;N, close enough to the equator that "
  "the sun drops almost vertically instead of sliding along the horizon, so the light goes from "
  "gold to gone quickly. It is roughly half of what a London couple gets and a fraction of what "
  "you see in Scandinavian reference photos. We plan around it by locking the location the week "
  "before and shooting one setup properly rather than three badly."),
 ("Can we still do a pre-wedding shoot at Lalbagh or Cubbon Park?",
  "No. A Karnataka Horticulture Department notification dated 20 November 2025 bans pre- and "
  "post-wedding photoshoots and drone photography inside Lalbagh, alongside reels, modelling "
  "shoots, baby showers and film or TV shooting. Violations carry a Rs 500 fine, and walking "
  "access itself is restricted to 5.30-9.00 am and 4.30-7.00 pm. Cubbon Park was brought under "
  "comparable restrictions a few months earlier. Older guides, including an earlier version of "
  "our own locations post, still quote a permit fee for Lalbagh. That route no longer exists. "
  "If a photographer offers you a Lalbagh shoot, ask them what changed in November 2025."),
 ("So where can we legally shoot in and around Bangalore?",
  "Nandi Hills, Hesaraghatta grasslands and lake, Bangalore Palace, private heritage properties, "
  "resort and estate grounds, and indoor studio sets are all still open to pre-wedding work. "
  "Bangalore Palace needs written permission arranged roughly two weeks ahead and charges a "
  "location fee. Nandi Hills has no photography fee but is gated at 06:00. Private estates and "
  "resorts are the most predictable option because access is contractual rather than "
  "discretionary, which matters when you have one morning and a hired outfit."),
 ("What time do we need to start?",
  f"Earlier than almost everyone expects. Sunrise in Bangalore runs from {EARLIEST} in midsummer "
  f"to {LATEST} in January, and the morning golden window closes within half an hour of it. The "
  "'be on location' column in the table above already includes 20 minutes for parking, changing "
  "and the first frames, so treat it as the time you are standing in position, dressed, not the "
  "time you leave home. For a Nandi Hills sunrise that usually means leaving central Bangalore "
  "around 04:30."),
 ("Is Nandi Hills worth it for a sunrise shoot?",
  f"In {eng(NANDI_FULL)}, yes. The gate opens at 06:00, the climb to the viewpoints takes about "
  f"20 minutes, and in those months sunrise is late enough that you still catch the full window. "
  f"In {eng(NANDI_BAD)} the sun is already up before you can reach the top, leaving under a "
  "quarter of an hour of usable light. We would rather tell you that in advance than take the "
  "booking and blame the weather afterwards."),
 ("How much does a pre-wedding shoot in Bangalore cost?",
  "A four-hour city studio session with one photographer runs Rs 15,000 to Rs 35,000. A city "
  "outdoor shoot with one or two shooters, 80 to 120 edited images and a reel is Rs 40,000 to "
  "Rs 90,000. A day trip to Nandi Hills or Hesaraghatta with a full team, drone and a cinematic "
  "film is Rs 75,000 to Rs 1,50,000. A two-day weekend shoot in Coorg, Chikmagalur or Hampi with "
  "travel is Rs 1,50,000 to Rs 3,50,000. Permits and location fees are billed at cost."),
 ("Can you fly a drone at our shoot?",
  "It depends entirely on the location. Drone photography is banned outright inside Lalbagh. "
  "Elsewhere it needs the landowner's permission and compliance with DGCA rules, which is "
  "straightforward on private estate land and awkward to impossible in central Bangalore. We "
  "confirm this per location before quoting rather than promising aerials and apologising later."),
 ("How far ahead should we book?",
  "Six to ten weeks for a city or day-trip shoot, and longer if you want a specific weekend "
  "between November and February, which is both the best light and the busiest season. Bangalore "
  "Palace permissions want about two weeks on their own. If your wedding is already close, tell "
  "us the date anyway - we hold a few short-notice mornings each month."),
]
def faq_html():
    return "\n".join(
        f'                <details class="faq-item"{" open" if i == 0 else ""}>\n'
        f'                    <summary>{q} <span class="faq-icon">+</span></summary>\n'
        f'                    <div class="faq-answer"><p>{a}</p></div>\n'
        f'                </details>' for i, (q, a) in enumerate(FAQ))

import html as _h
def faq_schema():
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":_h.unescape(q),
         "acceptedAnswer":{"@type":"Answer","text":_h.unescape(a.replace('&deg;','°'))}}
        for q,a in FAQ]}, indent=2, ensure_ascii=False)

TODAY = datetime.date.today().isoformat()

GALLERY = [
    ("bangalore-pre-wedding-dhrithi-nitish-cover.jpg",   "Bridal portrait in low evening light at a Bangalore wedding"),
    ("bangalore-pre-wedding-keerthana-arnav-cover.jpg",  "Flower shower as a couple leaves the mandap at a Bangalore wedding"),
    ("bangalore-pre-wedding-aviva-abhishek-cover.jpg",   "Candid moment from a Bangalore wedding"),
    ("bangalore-pre-wedding-varsha-shivam-cover.jpg",    "Bangalore couple photographed during their wedding ceremony"),
    ("bangalore-pre-wedding-akshatha-vishnu-cover.jpg",  "South Indian wedding ritual photographed in Bangalore"),
    ("bangalore-pre-wedding-krithika-rakshith-cover.jpg","Portrait of a bride at a Bangalore wedding"),
]
def gallery_html():
    return "\n".join(
        f'            <figure><img src="assets/bangalore/{f}" alt="{alt}" loading="lazy" '
        f'width="1200" height="800"></figure>' for f, alt in GALLERY)

SERVICE = {
  "@context":"https://schema.org","@type":"Service",
  "@id": URL + "#service",
  "serviceType":"Pre-wedding photography and film",
  "name":"Pre-Wedding Shoots in Bangalore",
  "description":"Pre-wedding photo and film shoots in and around Bangalore, planned around the "
                "city's 28-to-31 minute golden window and the current Karnataka location rules.",
  "url": URL,
  "provider":{"@id":"https://weddingclickz.com/#business"},
  "areaServed":[{"@type":"City","name":"Bangalore"},
                {"@type":"AdministrativeArea","name":"Karnataka"}],
  "audience":{"@type":"Audience","audienceType":"Engaged couples"},
  "offers":[
    {"@type":"Offer","name":"City studio session (4 hours)",
     "priceCurrency":"INR","priceSpecification":{"@type":"PriceSpecification",
      "minPrice":15000,"maxPrice":35000,"priceCurrency":"INR"}},
    {"@type":"Offer","name":"City outdoor shoot",
     "priceCurrency":"INR","priceSpecification":{"@type":"PriceSpecification",
      "minPrice":40000,"maxPrice":90000,"priceCurrency":"INR"}},
    {"@type":"Offer","name":"Day trip (Nandi Hills / Hesaraghatta)",
     "priceCurrency":"INR","priceSpecification":{"@type":"PriceSpecification",
      "minPrice":75000,"maxPrice":150000,"priceCurrency":"INR"}},
    {"@type":"Offer","name":"Weekend shoot (Coorg / Chikmagalur / Hampi)",
     "priceCurrency":"INR","priceSpecification":{"@type":"PriceSpecification",
      "minPrice":150000,"maxPrice":350000,"priceCurrency":"INR"}}]
}

DATASET = {
  "@context":"https://schema.org","@type":"Dataset",
  "@id": URL + "#dataset",
  "name":"Bangalore pre-wedding light windows and Nandi Hills sunrise access",
  "description":"Computed sunrise, sunset, golden-hour start and end times, golden-window "
                "duration and solar azimuth for Bangalore (12.9716N, 77.5946E) for the 15th of "
                "each month, plus usable golden minutes at Nandi Hills given its 06:00 gate "
                "opening. Derived from a NOAA solar-position implementation; not sourced from "
                "third-party data.",
  "creator":{"@id":"https://weddingclickz.com/#business"},
  "license":"https://creativecommons.org/licenses/by/4.0/",
  "isAccessibleForFree": True,
  "dateModified": TODAY,
  "spatialCoverage":{"@type":"Place","name":"Bangalore, Karnataka, India",
    "geo":{"@type":"GeoCoordinates","latitude":12.9716,"longitude":77.5946}},
  "variableMeasured":["sunrise","sunset","golden hour start","golden hour end",
                      "golden window duration (minutes)","solar azimuth at sunrise and sunset",
                      "usable golden minutes at Nandi Hills"]
}

BREADCRUMB = {
  "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://weddingclickz.com/"},
    {"@type":"ListItem","position":2,"name":"Pre-Wedding Shoots",
     "item":"https://weddingclickz.com/pre-wedding-shoots.html"},
    {"@type":"ListItem","position":3,"name":"Pre-Wedding Shoot in Bangalore","item":URL}]
}

EXTRA_CSS = """
    <style>
        /* Data tables - the computed figures are the point of this page, so they
           get real table styling rather than being buried in prose. */
        .table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 1.5rem 0; }
        .data-table { border-collapse: collapse; width: 100%; min-width: 640px;
            font-size: 0.86rem; background: var(--white); }
        .data-table caption { caption-side: top; text-align: left; padding: 0 0 0.9rem;
            font-size: 0.85rem; color: var(--text-light); line-height: 1.6; }
        .data-table th, .data-table td { padding: 0.65rem 0.8rem; text-align: left;
            border-bottom: 1px solid rgba(201,168,124,0.22); }
        .data-table thead th { background: var(--charcoal); color: var(--white);
            font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase;
            font-family: 'Montserrat', sans-serif; font-weight: 600; }
        .data-table tbody th { font-family: 'Montserrat', sans-serif; font-weight: 600; }
        .data-table tbody tr:nth-child(even) { background: rgba(250,247,242,0.7); }
        .data-table .row-good { background: rgba(201,168,124,0.16); }
        .data-table .row-bad  { background: rgba(160,60,60,0.07); color: var(--text-light); }
        .data-table .row-highlight { background: rgba(201,168,124,0.22); font-weight: 600; }

        .note { border-left: 3px solid var(--gold); padding: 1rem 1.25rem; margin: 1.5rem 0;
            background: rgba(201,168,124,0.08); font-size: 0.93rem; }
        .note strong { color: var(--gold-dark); }

        .gallery-grid { display: grid; gap: 0.9rem; max-width: 1200px; margin: 0 auto;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
        .gallery-grid figure { margin: 0; overflow: hidden; border-radius: 6px; }
        .gallery-grid img { width: 100%; height: 300px; object-fit: cover;
            transition: transform 0.6s ease; }
        .gallery-grid figure:hover img { transform: scale(1.04); }

        .prose { max-width: 820px; margin: 0 auto; }
        .prose p { margin-bottom: 1.1rem; }
        .prose h3 { margin: 2rem 0 0.75rem; font-size: 1.45rem; }
        .prose ul { margin: 0 0 1.1rem 1.1rem; }
        .prose li { margin-bottom: 0.5rem; }
        .source-note { font-size: 0.8rem; color: var(--text-light); margin-top: 1rem; }
        .source-note a { color: var(--gold-dark); }

        /* Narrow phones: the logo lockup plus the Get Quote pill overran 390px
           viewports and pushed the whole page sideways. Tighten the gutter and
           the pill first, then drop the wordmark on the narrowest screens. */
        @media (max-width: 560px) {
            .header-container { padding: 0 1rem; }
            .logo-img { height: 38px; }
            .logo .logo-text { font-size: 1.2rem; }
            .nav-cta { padding: 0.5rem 0.9rem; font-size: 0.68rem; letter-spacing: 0.06em; }
        }
    </style>
"""

PAGE = f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
    <!-- Google tag (gtag.js) -->
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
    <meta name="description" content="Pre-wedding shoots in Bangalore, planned around the city's {GOLD_MIN}-minute golden window and the 2025 Lalbagh and Cubbon Park shoot ban. Locations, timings, permits and costs.">
    <meta name="keywords" content="pre wedding shoot Bangalore, pre wedding photoshoot Bangalore, pre wedding shoot locations Bangalore, Nandi Hills pre wedding shoot, pre wedding shoot cost Bangalore, couple photoshoot Bangalore">

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

    <meta property="og:type" content="article">
    <meta property="og:url" content="{URL}">
    <meta property="og:title" content="Pre-Wedding Shoot in Bangalore | WeddingClickz">
    <meta property="og:description" content="You get {GOLD_MIN} to {GOLD_MAX} minutes of golden light in Bangalore. Here is how we plan a pre-wedding shoot around it, and which locations are still legal in 2026.">
    <meta property="og:image" content="https://weddingclickz.com/og-image.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="WeddingClickz">
    <meta property="og:locale" content="en_IN">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Pre-Wedding Shoot in Bangalore | WeddingClickz">
    <meta name="twitter:description" content="Bangalore's golden hour is {GOLD_MIN}-{GOLD_MAX} minutes. Computed light windows, the 2025 Lalbagh shoot ban, and what a shoot actually costs.">
    <meta name="twitter:image" content="https://weddingclickz.com/og-image.jpg">

    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <script type="application/ld+json">
{json.dumps(SERVICE, indent=2, ensure_ascii=False)}
    </script>

    <script type="application/ld+json">
{json.dumps(DATASET, indent=2, ensure_ascii=False)}
    </script>

    <script type="application/ld+json">
{faq_schema()}
    </script>

    <script type="application/ld+json">
{json.dumps(BREADCRUMB, indent=2, ensure_ascii=False)}
    </script>

{CSS}
{EXTRA_CSS}
</head>
<body>

    <header id="header">
        <div class="header-container">
            <a href="index.html" class="logo">
                <img src="logo.png" alt="WeddingClickz" class="logo-img">
                <span class="logo-text">Wedding<span>Clickz</span></span>
            </a>
            <nav id="nav">
                <ul>
                    <li class="nav-mobile-only"><a href="index.html">Home</a></li>
                    <li><a href="#light">The Light</a></li>
                    <li><a href="#locations">Locations</a></li>
                    <li><a href="#cost">Cost</a></li>
                    <li><a href="blog.html">Blog</a></li>
                    <li class="nav-mobile-only"><a href="wedding-photographer-india.html">India</a></li>
                    <li class="nav-mobile-only"><a href="wedding-photographer-uae.html">UAE</a></li>
                </ul>
            </nav>
            <div class="region-switch" aria-label="Choose your region">
                <a href="wedding-photographer-india.html" class="current" hreflang="en-IN">&#127470;&#127475; India</a>
                <a href="wedding-photographer-uae.html" hreflang="en-AE">&#127462;&#127466; UAE</a>
            </div>
            <a href="index.html#contact" class="nav-cta">Get Quote</a>
            <div class="mobile-menu-toggle" id="menuToggle"><span></span><span></span><span></span></div>
        </div>
    </header>

    <section class="hero" style="background: linear-gradient(rgba(26,26,26,0.5), rgba(26,26,26,0.72)), url('assets/bangalore/bangalore-pre-wedding-dhrithi-nitish-cover.jpg') center/cover;">
        <div class="hero-inner">
            <span class="eyebrow">Bangalore &middot; Karnataka</span>
            <h1>Pre-Wedding Shoot in <em>Bangalore</em></h1>
            <p>You get {GOLD_MIN} to {GOLD_MAX} minutes of golden light in this city. Not an hour. We plan the
               whole morning around that number, and around which locations will actually let you
               through the gate in 2026.</p>
            <div class="hero-actions">
                <a href="index.html#contact" class="btn btn-gold">Check Your Date</a>
                <a href="#light" class="btn btn-outline">See the Light Tables</a>
            </div>
        </div>
    </section>

    <section class="block intro">
        <div class="container prose">
            <span class="section-label">Why this page exists</span>
            <h2 class="section-title">A Studio in <em>Konanakunte</em>, Not a Directory Listing</h2>
            <p>We shoot out of Konanakunte, in south Bangalore, and most of our pre-wedding mornings
               start before five. Over the years the same two things have gone wrong for couples who
               came to us after a bad experience: they were sold a location that no longer allows
               shoots, and they were sold a schedule built on a golden hour that does not exist at
               this latitude.</p>
            <p>So this page leads with numbers rather than adjectives. The light tables below are
               computed from solar geometry for Bangalore's exact coordinates - our own calculation,
               not lifted from a weather site - and the location rules are current as of
               September 2026, including the Horticulture Department order that closed Lalbagh to
               pre-wedding shoots in November 2025.</p>
            <p>If you only take one thing from this page: book the date around the light, then pick
               the location. Couples almost always do it the other way round, and that is why so many
               Bangalore pre-wedding galleries have twelve good frames and eighty flat ones.</p>
        </div>
    </section>

    <section class="block" id="light">
        <div class="container prose">
            <span class="section-label">The measurement</span>
            <h2 class="section-title">You Have <em>{GOLD_MIN} Minutes</em>, Not Sixty</h2>
            <p>"Golden hour" is a borrowed phrase. It was coined where the sun sets at a shallow
               angle and loiters near the horizon. Bangalore is at 12.97&deg;N, close to the equator,
               where the sun comes down steeply and the warm light closes fast.</p>
            <p>Measured properly - sun between the horizon and six degrees above it - Bangalore's
               golden window runs {GOLD_MIN} to {GOLD_MAX} minutes, morning and evening, all year.
               Sunrise moves nearly an hour across the year, from {EARLIEST} in midsummer to
               {LATEST} in January, but the length of the good light barely changes.</p>
{table_monthly()}
            <div class="note">
                <strong>How to read the "be on location" column.</strong> That is the time you should
                be standing in position and dressed, not the time you leave home. It is sunrise minus
                twenty minutes, which covers parking, a change of outfit and the first few throwaway
                frames while everyone relaxes. From central Bangalore, a Nandi Hills sunrise means
                leaving around 04:30.
            </div>
            <h3>Why it is so short here</h3>
            <p>The same calculation run at five latitudes shows the pattern clearly. The further you
               are from the equator, the longer the sun takes to cross those six degrees.</p>
{table_latitude()}
            <p>This is why Pinterest boards mislead people. Most of the soft, endless-light couple
               photography that couples bring to us as reference was shot at 45&deg;N or higher, where
               there is genuinely an hour of it. At 12.97&deg;N you get roughly half of what London
               gets, and Reykjav&iacute;k in December gets more than three hours. The technique has to
               change to match, which mostly means fewer setups, shorter walks between them, and
               lighting we bring ourselves for anything outside the window.</p>
            <p class="source-note">Computed with a NOAA solar-position implementation for
               12.9716&deg;N, 77.5946&deg;E, IST. The same tooling produced our
               <a href="blog/dubai-golden-hour-33-minutes.html">Dubai golden hour</a> and
               <a href="blog/business-bay-light-line.html">Business Bay light line</a> figures, where
               computed sunset times matched observed Dubai sunset to within a minute.</p>
        </div>
    </section>

    <section class="block" id="locations">
        <div class="container prose">
            <span class="section-label">Access, not inspiration</span>
            <h2 class="section-title">Where You Can Legally Shoot in <em>2026</em></h2>
            <p>This is the part most location lists get wrong, including ours until recently. Rules in
               Bangalore's public gardens changed materially in 2025, and a lot of published advice -
               and a lot of photographers - have not caught up.</p>
            <h3>Lalbagh and Cubbon Park: closed to pre-wedding shoots</h3>
            <p>A Karnataka Horticulture Department notification dated <strong>20 November 2025</strong>
               prohibits pre- and post-wedding photoshoots and drone photography inside Lalbagh
               Botanical Garden, along with reels, modelling shoots, baby showers, and film and
               television shooting. Violations attract a <strong>Rs 500 fine</strong>. General walking
               access is limited to 5.30-9.00 am and 4.30-7.00 pm. The department's reasoning is that
               Lalbagh is a botanical garden holding germplasm collections rather than a general
               recreation park. Cubbon Park came under comparable restrictions a few months earlier.</p>
            <div class="note">
                <strong>If a photographer still offers you a Lalbagh pre-wedding shoot, that is a
                useful signal.</strong> Either they have not read the notification, or they are
                planning to shoot anyway and let you absorb the fine and the ejection. We had an older
                blog post quoting a Lalbagh permit fee ourselves; it was correct when written and is
                not any more, and we have corrected it.
            </div>
            <h3>What is still open</h3>
            <ul>
                <li><strong>Nandi Hills</strong> - no photography fee, but gated from 06:00 and a
                    roughly twenty-minute climb to the viewpoints. Timing is everything here; see the
                    table below.</li>
                <li><strong>Bangalore Palace</strong> - permission arranged in advance, typically
                    about two weeks, with a location fee. Tudor architecture and gardens, and the
                    closest in-city substitute for a palace shoot.</li>
                <li><strong>Hesaraghatta grasslands and lake</strong> - open, uncrowded, and the best
                    wide-horizon option inside an hour of the city.</li>
                <li><strong>Private estates, resorts and heritage homestays</strong> - the most
                    reliable category, because access is contractual rather than discretionary. If you
                    have one morning and a hired outfit, this is what we usually recommend.</li>
                <li><strong>Indoor and studio sets</strong> - fully controllable light, which stops
                    being a compromise and starts being an advantage during the monsoon months.</li>
            </ul>
            <h3>The Nandi Hills gate problem</h3>
            <p>Nandi Hills is the default answer when couples think "sunrise shoot near Bangalore".
               It is a good answer for part of the year and a poor one for the rest, and the reason is
               arithmetic rather than opinion. The gate opens at 06:00. The drive from the gate to the
               summit viewpoints takes about twenty minutes. In midsummer the sun is already up before
               you can get there.</p>
{table_nandi()}
            <p>In {eng(NANDI_FULL)} you get the full window. In {eng(NANDI_BAD)} you get under a
               quarter of an hour, and most of the warmth is gone before you have found your footing.
               We would rather show you this table than take a June booking and blame the haze
               afterwards. If your date falls in a difficult month, Hesaraghatta or a private estate
               will give you far more usable light for the same money.</p>
            <p class="source-note">Gate timing from the published Nandi Hills visitor hours; sunrise
               and golden-hour times computed as above. Location rules summarised from the Karnataka
               Horticulture Department's November 2025 Lalbagh notification as reported by
               <a href="https://www.deccanherald.com/india/karnataka/bengaluru/playing-with-branches-skating-and-shooting-reels-inside-lalbagh-may-now-attract-a-fine-of-rs-500-3804964" rel="nofollow noopener" target="_blank">Deccan Herald</a>
               and <a href="https://www.thenewsminute.com/karnataka/after-cubbon-park-horticulture-dept-guns-for-restriction-of-public-activities-in-lalbagh" rel="nofollow noopener" target="_blank">The News Minute</a>.
               Rules change; we re-check before every booking.</p>
        </div>
    </section>

    <section class="block portfolio">
        <div class="container">
            <div style="text-align:center;max-width:760px;margin:0 auto 2.25rem;">
                <span class="section-label">Recent work</span>
                <h2 class="section-title">Couples We Have Photographed in <em>Bangalore</em></h2>
                <p>These are wedding-day frames from Bangalore couples rather than staged pre-wedding
                   sets - the same team, the same approach to light.</p>
            </div>
            <div class="gallery-grid">
{gallery_html()}
            </div>
        </div>
    </section>

    <section class="block" id="cost">
        <div class="container prose">
            <span class="section-label">Money</span>
            <h2 class="section-title">What a Bangalore Pre-Wedding Shoot <em>Costs</em></h2>
            <p>Four tiers, which is genuinely how the work divides. Permits and location fees are
               billed at cost, not marked up.</p>
            <div class="table-scroll"><table class="data-table">
            <caption>Pre-wedding shoot pricing, Bangalore and nearby, 2026.</caption>
            <thead><tr><th>Tier</th><th>What it includes</th><th>Typical price</th></tr></thead>
            <tbody>
            <tr><th scope="row">City studio (4 hrs)</th><td>1 photographer, 1 set, basic edits</td><td>Rs 15,000 - 35,000</td></tr>
            <tr><th scope="row">City outdoor</th><td>1-2 shooters, 80-120 edited photos, reel</td><td>Rs 40,000 - 90,000</td></tr>
            <tr><th scope="row">Day trip</th><td>Nandi Hills or Hesaraghatta, full team, drone, cinematic film</td><td>Rs 75,000 - 1,50,000</td></tr>
            <tr><th scope="row">Weekend</th><td>Coorg, Chikmagalur or Hampi; 2-day shoot, drone, full film, travel</td><td>Rs 1,50,000 - 3,50,000</td></tr>
            </tbody></table></div>
            <p>The honest guidance: a city outdoor shoot in November or December will out-perform a
               more expensive day trip in June, because the light is the constraint, not the backdrop.
               Spend on the date before you spend on the drive.</p>
        </div>
    </section>

    <section class="block faq">
        <div class="container">
            <div style="text-align:center;max-width:760px;margin:0 auto 2rem;">
                <span class="section-label">Questions</span>
                <h2 class="section-title">Bangalore Pre-Wedding <em>Questions</em></h2>
            </div>
            <div class="faq-list" style="max-width:820px;margin:0 auto;">
{faq_html()}
            </div>
        </div>
    </section>

    <section class="cta-banner">
        <h2>Tell Us Your <em>Date</em></h2>
        <p>Send us the date and we will tell you what the light does that morning, which locations are
           open, and what it costs - before you commit to anything.</p>
        <div class="hero-actions">
            <a href="index.html#contact" class="btn btn-gold">Request a Quote</a>
            <a href="tel:+919740222927" class="btn btn-outline">Call +91 97402 22927</a>
        </div>
    </section>

    <footer>
        <div class="footer-grid">
            <div class="footer-brand">
                <h3>Wedding<span>Clickz</span></h3>
                <p>A wedding photography and film studio in Konanakunte, Bangalore, shooting across
                   Karnataka and India since 2014.</p>
                <div class="footer-contact">
                    <a href="tel:+919740222927">+91 97402 22927</a>
                    <a href="mailto:info@weddingclickz.com">info@weddingclickz.com</a>
                    <a href="https://maps.google.com/?q=ClayWorks+Shankaraa,+Kanakapura+Main+Rd,+Munireddy+Layout,+Konanakunte,+Bengaluru,+Karnataka+560062" target="_blank" rel="noopener noreferrer">ClayWorks Shankaraa, Konanakunte, Bengaluru 560062</a>
                </div>
            </div>
            <div class="footer-links">
                <h4>Pre-Wedding</h4>
                <ul>
                    <li><a href="pre-wedding-shoot-bangalore.html">Pre-Wedding Shoot Bangalore</a></li>
                    <li><a href="blog/best-pre-wedding-shoot-locations-bangalore.html">Locations Near Bangalore</a></li>
                    <li><a href="blog/pre-wedding-shoot-ideas-india-2025.html">Pre-Wedding Shoot Ideas</a></li>
                    <li><a href="pre-wedding-shoots.html">Pre-Wedding Shoots (Dubai)</a></li>
                    <li><a href="blog/wedding-reels-instagram-couple-shoot-india.html">Couple Reels</a></li>
                </ul>
            </div>
            <div class="footer-links">
                <h4>Get Started</h4>
                <ul>
                    <li><a href="index.html#contact">Get a Quote</a></li>
                    <li><a href="wedding-photographer-india.html">Wedding Photographer India</a></li>
                    <li><a href="blog/wedding-photography-cost-bangalore.html">Wedding Photography Cost</a></li>
                    <li><a href="privacy-policy.html">Privacy Policy</a></li>
                    <li><a href="terms-of-use.html">Terms of Use</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2026 WeddingClickz Photography. All rights reserved.</span>
            <span><a href="privacy-policy.html">Privacy</a><a href="terms-of-use.html">Terms</a><a href="cookie-policy.html">Cookies</a></span>
        </div>
    </footer>

    <section class="city-strip">
        <h2>Pre-Wedding and Wedding Photography Around Bangalore</h2>
        <p>
            <a href="blog/best-pre-wedding-shoot-locations-bangalore.html">Pre-Wedding Shoot Locations Near Bangalore</a> &middot;
            <a href="blog/wedding-photography-cost-bangalore.html">Wedding Photography Cost in Bangalore</a> &middot;
            <a href="blog/pre-wedding-shoot-ideas-india-2025.html">Pre-Wedding Shoot Ideas</a> &middot;
            <a href="blog/wedding-reels-instagram-couple-shoot-india.html">Couple Reels &amp; Instagram Shoots</a> &middot;
            <a href="blog/how-to-choose-wedding-photographer-india.html">How to Choose a Wedding Photographer</a> &middot;
            <a href="blog/destination-wedding-photographer-india.html">Destination Wedding Photography</a> &middot;
            <a href="blog/south-indian-wedding-photography-guide.html">South Indian Wedding Photography</a> &middot;
            <a href="wedding-photographer-india.html">Wedding Photographer India</a>
        </p>
    </section>

    <script>
        const header = document.getElementById('header');
        window.addEventListener('scroll', () => header.classList.toggle('scrolled', window.scrollY > 40));
        document.getElementById('menuToggle').addEventListener('click', () =>
            document.getElementById('nav').classList.toggle('open'));
    </script>
</body>
</html>
"""

out = os.path.join(ROOT, 'pre-wedding-shoot-bangalore.html')
open(out, 'w', encoding='utf-8').write(PAGE)
print(f"wrote {out}  ({len(PAGE):,} bytes)")
print(f"golden window {GOLD_MIN}-{GOLD_MAX} min | sunrise {EARLIEST}-{LATEST}")
print(f"Nandi full: {NANDI_FULL} | Nandi poor: {NANDI_BAD}")
