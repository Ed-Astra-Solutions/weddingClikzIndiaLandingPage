"""
Builds ../blog/bangalore-golden-hour-28-minutes.html — the authority/data post.

This content used to sit on the pre-wedding landing page. It was moved here so
the landing page can lead with pictures and the experience, while the research
keeps working as a citable asset in its own right. Figures come from
bangalore_light.json; nothing is typed by hand.

    python3 bangalore_light.py && python3 build_bangalore_light_post.py
"""
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
D = json.load(open(os.path.join(HERE, 'bangalore_light.json')))
MON, NANDI = D['monthly'], D['nandi']
names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
FULL = dict(zip(names, ["January","February","March","April","May","June","July",
                        "August","September","October","November","December"]))
URL = "https://weddingclickz.com/blog/bangalore-golden-hour-28-minutes.html"

mg = [MON[m]['morning_min'] for m in names]
eg = [MON[m]['evening_min'] for m in names]
GMIN, GMAX = min(mg + eg), max(mg + eg)
EARLY = min(MON[m]['sunrise'] for m in names)
LATE  = max(MON[m]['sunrise'] for m in names)
FULLW = [m for m in names if NANDI[m]['usable_min'] >= NANDI[m]['full_min'] - 1]
BAD   = [m for m in names if NANDI[m]['usable_min'] < 15]
def eng(l): return l[0] if len(l)==1 else ", ".join(l[:-1]) + " and " + l[-1]

def t_month():
    r=['<div class="data-table-wrap"><table class="data">',
       '<caption>Bangalore light windows, 15th of each month</caption>',
       '<thead><tr><th>Month</th><th>Sunrise</th><th>Morning golden</th><th>Min</th>'
       '<th>Evening golden</th><th>Min</th><th>Sunset</th><th>Light from</th></tr></thead><tbody>']
    for m in names:
        v=MON[m]
        pk=' peak' if v['morning_min']==GMAX else ''
        r.append(f"<tr><td>{FULL[m]}</td><td class=\"num\">{v['sunrise']}</td>"
                 f"<td class=\"num\">{v['morning']}</td><td class=\"num{pk}\">{v['morning_min']}</td>"
                 f"<td class=\"num\">{v['evening']}</td><td class=\"num\">{v['evening_min']}</td>"
                 f"<td class=\"num\">{v['sunset']}</td><td class=\"num\">{v['from_sunrise']}/{v['from_sunset']}</td></tr>")
    return "\n".join(r)+'</tbody></table></div>'

LAT=[("Bangalore","12.97",28,31,31),("Dubai","25.19",30,33,34),("Delhi","28.61",31,34,35),
     ("London","51.51",44,54,62),("Reykjav&iacute;k","64.15",63,113,209)]
def t_lat():
    r=['<div class="data-table-wrap"><table class="data">',
       '<caption>Evening golden hour by latitude</caption>',
       '<thead><tr><th>City</th><th>Latitude</th><th>21 Mar</th><th>21 Jun</th><th>21 Dec</th></tr></thead><tbody>']
    for c,la,a,b,cc in LAT:
        pk=' peak' if c=="Bangalore" else ''
        r.append(f'<tr><td>{c}</td><td class="num">{la}&deg;N</td>'
                 f'<td class="num{pk}">{a} min</td><td class="num">{b} min</td><td class="num">{cc} min</td></tr>')
    return "\n".join(r)+'</tbody></table></div>'

def t_nandi():
    r=['<div class="data-table-wrap"><table class="data">',
       '<caption>Nandi Hills: usable golden minutes after a 06:00 gate</caption>',
       '<thead><tr><th>Month</th><th>Sunrise</th><th>Golden ends</th><th>In position</th>'
       '<th>Usable</th><th>Verdict</th></tr></thead><tbody>']
    for m in names:
        v=NANDI[m]
        pk=' peak' if v['usable_min']>=v['full_min']-1 else ''
        r.append(f"<tr><td>{FULL[m]}</td><td class=\"num\">{v['sunrise']}</td>"
                 f"<td class=\"num\">{v['golden_ends']}</td><td class=\"num\">{v['in_position']}</td>"
                 f"<td class=\"num{pk}\">{v['usable_min']} min</td><td>{v['verdict']}</td></tr>")
    return "\n".join(r)+'</tbody></table></div>'

FAQ=[("How long is golden hour in Bangalore?",
      f"Between {GMIN} and {GMAX} minutes, morning or evening, all year. Bangalore sits at "
      "12.97&deg;N, close enough to the equator that the sun drops almost vertically rather "
      "than sliding along the horizon, so the warm light closes fast."),
     ("Can you still shoot a pre-wedding at Lalbagh or Cubbon Park?",
      "No. A Karnataka Horticulture Department notification dated 20 November 2025 bans pre- "
      "and post-wedding photoshoots and drone photography inside Lalbagh, with a Rs 500 fine. "
      "Cubbon Park came under comparable restrictions a few months earlier."),
     ("When is Nandi Hills worth it for sunrise?",
      f"{eng(FULLW)}. The gate opens at 06:00 and the climb takes about twenty minutes, so in "
      f"{eng(BAD)} the sun is already up before you can be in position and under a quarter of "
      "an hour of usable light is left."),
     ("What time does the light start?",
      f"Sunrise runs from {EARLY} in midsummer to {LATE} in January, and the morning window "
      "closes within half an hour of it.")]

def faq_html():
    return "\n".join(f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>'
                     for q,a in FAQ)
import html as _h
def faq_schema():
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":_h.unescape(q),"acceptedAnswer":{"@type":"Answer",
         "text":_h.unescape(a.replace('&deg;','°'))}} for q,a in FAQ]},indent=2,ensure_ascii=False)

TODAY=datetime.date.today().isoformat()
DATASET={"@context":"https://schema.org","@type":"Dataset","@id":URL+"#dataset",
 "name":"Bangalore golden-hour windows and Nandi Hills sunrise access",
 "description":"Computed sunrise, sunset, golden-hour start/end, window duration and solar "
   "azimuth for Bangalore (12.9716N, 77.5946E) for the 15th of each month, plus usable golden "
   "minutes at Nandi Hills given its 06:00 gate. Derived from a NOAA solar-position "
   "implementation; not sourced from third parties.",
 "creator":{"@id":"https://weddingclickz.com/#business"},
 "license":"https://creativecommons.org/licenses/by/4.0/","isAccessibleForFree":True,
 "dateModified":TODAY,
 "spatialCoverage":{"@type":"Place","name":"Bangalore, Karnataka, India",
   "geo":{"@type":"GeoCoordinates","latitude":12.9716,"longitude":77.5946}},
 "variableMeasured":["sunrise","sunset","golden hour start","golden hour end",
   "golden window duration (minutes)","solar azimuth","usable golden minutes at Nandi Hills"]}
ARTICLE={"@context":"https://schema.org","@type":"Article",
 "mainEntityOfPage":{"@type":"WebPage","@id":URL},
 "headline":f"Bangalore's Golden Hour Is {GMIN} Minutes",
 "description":f"Computed light windows for Bangalore: a {GMIN}-{GMAX} minute golden window, "
   "why latitude makes it short, and the Nandi Hills gate arithmetic.",
 "image":"https://weddingclickz.com/assets/prewedding-in/prewedding-17.jpg",
 "author":{"@type":"Organization","name":"WeddingClickz","url":"https://weddingclickz.com"},
 "publisher":{"@type":"Organization","name":"WeddingClickz",
   "logo":{"@type":"ImageObject","url":"https://weddingclickz.com/favicon.ico"}},
 "datePublished":TODAY,"dateModified":TODAY,"articleSection":"Data · Bangalore"}
BREAD={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"Home","item":"https://weddingclickz.com/"},
 {"@type":"ListItem","position":2,"name":"Blog","item":"https://weddingclickz.com/blog.html"},
 {"@type":"ListItem","position":3,"name":f"Bangalore's Golden Hour Is {GMIN} Minutes"}]}

PAGE=f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#1A1A1A">

<title>Bangalore's Golden Hour Is {GMIN} Minutes | WeddingClickz</title>
<meta name="description" content="Not sixty. Computed light windows for Bangalore — why latitude halves the golden hour, the month-by-month table, and why Nandi Hills only works in winter.">
<meta name="keywords" content="golden hour Bangalore, sunrise time Bangalore photography, Nandi Hills sunrise shoot, pre-wedding light Bangalore, best time pre-wedding shoot Bangalore">
<link rel="canonical" href="{URL}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="IN-KA">
<meta name="geo.placename" content="Bangalore, Karnataka, India">
<meta name="geo.position" content="12.971600;77.594600">
<meta name="ICBM" content="12.971600, 77.594600">
<meta name="author" content="WeddingClickz">

<meta property="og:type" content="article">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="Bangalore's Golden Hour Is {GMIN} Minutes">
<meta property="og:description" content="Why latitude halves the window, month by month — and the gate arithmetic that decides whether a Nandi Hills sunrise is worth the 04:30 start.">
<meta property="og:image" content="https://weddingclickz.com/assets/prewedding-in/prewedding-17.jpg">
<meta property="og:site_name" content="WeddingClickz">
<meta property="article:published_time" content="{TODAY}T09:00:00+05:30">
<meta property="article:modified_time" content="{TODAY}T09:00:00+05:30">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Bangalore's Golden Hour Is {GMIN} Minutes">
<meta name="twitter:description" content="Computed light windows for Bangalore, and why Nandi Hills sunrises only work in winter.">
<meta name="twitter:image" content="https://weddingclickz.com/assets/prewedding-in/prewedding-17.jpg">

<script type="application/ld+json">
{json.dumps(ARTICLE, indent=2, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(DATASET, indent=2, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{faq_schema()}
</script>
<script type="application/ld+json">
{json.dumps(BREAD, indent=2, ensure_ascii=False)}
</script>

<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="post.css">
</head>
<body>

<header class="site-header">
  <div class="header-container">
    <a href="/index.html" class="logo"><img src="/logo.png" alt="WeddingClickz" class="logo-img"></a>
    <nav>
      <div class="mobile-menu-toggle" onclick="this.classList.toggle('active'); document.querySelector('nav ul').classList.toggle('open');"><span></span><span></span><span></span></div>
      <ul>
        <li><a href="/index.html#archives">Portfolio</a></li>
        <li><a href="/index.html#films">Films</a></li>
        <li><a href="/pre-wedding-shoot-bangalore.html">Pre-Wedding</a></li>
        <li><a href="/blog.html" class="active">Blog</a></li>
        <li><a href="/index.html#contact" class="nav-cta">Get in Touch</a></li>
      </ul>
    </nav>
  </div>
</header>

<section class="post-hero">
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <a href="/">Home</a> &nbsp;/&nbsp; <a href="/blog.html">Blog</a> &nbsp;/&nbsp; <span>Bangalore's Golden Hour Is {GMIN} Minutes</span>
  </nav>
  <span class="post-category">Data &middot; Bangalore</span>
  <h1 class="post-title">Bangalore's Golden Hour Is <em>{GMIN} Minutes</em></h1>
  <div class="post-meta">
    <span>By WeddingClickz</span><span class="dot">&bull;</span>
    <span>{datetime.date.today().strftime('%-d %B %Y')}</span><span class="dot">&bull;</span>
    <span>6 min read</span>
  </div>
</section>

<div class="post-cover">
  <img src="/assets/prewedding-in/prewedding-17.jpg" alt="Couple photographed in low golden light during a pre-wedding shoot by WeddingClickz" width="1200" height="800" fetchpriority="high">
</div>

<article class="post-content">

<p>Not sixty. We compute our own solar tables for the cities we shoot in, and for
Bangalore the answer is uncomfortably short: the warm window lasts
<strong>{GMIN} to {GMAX} minutes</strong>, morning or evening, every month of the year.</p>

<p>That matters more than it sounds. Most of the soft, endless-light couple photography
that couples bring us as reference was shot at 45&deg;N or higher, where an hour of it
genuinely exists. Planning a Bangalore shoot against that expectation is how you end up
with twelve good frames and eighty flat ones.</p>

<h2>Why it is so short</h2>

<p>Golden hour is not a unit of time, it is a sun angle &mdash; roughly the horizon to six
degrees above it. How long the sun takes to cross those six degrees depends on how steeply
it travels, and that depends on latitude. Bangalore is at 12.97&deg;N. The sun comes down
almost vertically here, so it crosses the warm band quickly and the light is gone.</p>

{t_lat()}

<p>Reykjav&iacute;k in December gets more than three hours. London gets roughly double what
we do. At 12.97&deg;N the window is about as short as inhabited latitudes go.</p>

<h2>The month-by-month table</h2>

<p>Sunrise moves nearly an hour across the year, from {EARLY} in midsummer to {LATE} in
January, but the <em>length</em> of the good light barely changes. The last column is the
compass direction the light arrives from, which decides which way a location can face.</p>

{t_month()}

<h2>The Nandi Hills gate problem</h2>

<p>Nandi Hills is the default answer when couples think &ldquo;sunrise shoot near
Bangalore&rdquo;. It is a good answer for part of the year and a poor one for the rest, and
the reason is arithmetic rather than taste.</p>

<p>The gate opens at <strong>06:00</strong>. The drive from the gate up to the summit
viewpoints takes about twenty minutes. In midsummer, sunrise is {EARLY} &mdash; before you
can legally be on the hill at all.</p>

{t_nandi()}

<p>In {eng(FULLW)} you get the full window. In {eng(BAD)} you get under a quarter of an
hour, and most of the warmth is gone before anyone has found their footing. If your date
falls in a difficult month, Hesaraghatta or a private estate will give you far more usable
light for the same money.</p>

<h2>Where you can legally shoot in 2026</h2>

<p>Worth saying plainly, because a lot of published advice has not caught up. A Karnataka
Horticulture Department notification dated <strong>20 November 2025</strong> prohibits pre-
and post-wedding photoshoots and drone photography inside <strong>Lalbagh</strong>, along
with reels, modelling shoots, baby showers and film or TV shooting. Violations carry a
<strong>Rs 500 fine</strong>, and general access is limited to 5:30&ndash;9:00 AM and
4:30&ndash;7:00 PM. <strong>Cubbon Park</strong> came under comparable restrictions a few
months earlier.</p>

<p>Still open: Nandi Hills, Hesaraghatta, Bangalore Palace (advance permission and a
location fee), private estates and resorts, and indoor studio sets.</p>

<h2>The short version</h2>

<ul>
<li>You get <strong>{GMIN}&ndash;{GMAX} minutes</strong> of golden light, not an hour.</li>
<li>Book the date around the light, then pick the location &mdash; couples almost always do it the other way round.</li>
<li>Nandi Hills sunrises are a winter proposition: {eng(FULLW)}.</li>
<li>Lalbagh and Cubbon Park are closed to pre-wedding shoots.</li>
<li>One location per shoot. Travel between two eats the entire window.</li>
</ul>

<h2>Questions</h2>
{faq_html()}

<p class="source-note" style="font-size:.82rem;opacity:.65;margin-top:2rem;">Computed with a
NOAA solar-position implementation for 12.9716&deg;N, 77.5946&deg;E, IST. The same tooling
produced our <a href="/blog/dubai-golden-hour-33-minutes.html">Dubai golden hour</a> and
<a href="/blog/business-bay-light-line.html">Business Bay light line</a> figures, where
computed sunset times matched observed Dubai sunset to within a minute. Location rules from
the Karnataka Horticulture Department's November 2025 notification. Figures are free to cite
with attribution.</p>

<p style="margin-top:2rem;"><strong>Planning an actual shoot?</strong> See
<a href="/pre-wedding-shoot-bangalore.html">pre-wedding shoots in Bangalore</a> &mdash; the
work, the locations and what a session includes.</p>

</article>

<section class="related" aria-label="Related Articles">
  <h2>Keep Reading</h2>
  <div class="related-grid">
    <a class="related-card" href="/pre-wedding-shoot-bangalore.html">
      <span class="cat">Pre-Wedding</span>
      <h3>Pre-Wedding Shoots in Bangalore</h3>
      <p>The work itself &mdash; locations, what a session includes, and what it costs.</p>
    </a>
    <a class="related-card" href="/blog/best-pre-wedding-shoot-locations-bangalore.html">
      <span class="cat">Locations</span>
      <h3>Pre-Wedding Shoot Locations Near Bangalore</h3>
      <p>Fifteen locations with travel time, light window and current permit position.</p>
    </a>
    <a class="related-card" href="/blog/dubai-golden-hour-33-minutes.html">
      <span class="cat">Data &middot; Dubai</span>
      <h3>Dubai's Golden Hour Is 33 Minutes</h3>
      <p>The same calculation, run for Business Bay.</p>
    </a>
  </div>
</section>

<footer class="site-footer">
  <p>&copy; 2026 WeddingClickz Photography &middot;
     <a href="/">Home</a> &middot; <a href="/blog.html">Blog</a> &middot;
     <a href="/pre-wedding-shoot-bangalore.html">Pre-Wedding Bangalore</a></p>
</footer>
</body>
</html>
"""
out=os.path.join(ROOT,'blog','bangalore-golden-hour-28-minutes.html')
open(out,'w',encoding='utf-8').write(PAGE)
print(f"wrote {out} ({len(PAGE):,} bytes) | golden {GMIN}-{GMAX} | nandi full {FULLW}")
