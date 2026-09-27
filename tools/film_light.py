"""
Cinematic light budget for UAE wedding films.

Same NOAA solar-position core as solar.py / almanac.py, but parameterised by
location so the numbers can be computed for Dubai and Abu Dhabi (and any
reference latitude) instead of only Business Bay.

What it answers, for a wedding film crew:
  - when does the usable evening light start and end
  - how many minutes of golden light and of blue light exist on that date
  - how that budget compares with a higher-latitude city

Run: python3 film_light.py
Nothing here is sourced from a third party; it is all computed.
"""
import math, datetime, json

def solar(dt_utc, lat, lon):
    """NOAA solar position. Returns (elevation_deg, azimuth_deg from N, CW)."""
    jd = dt_utc.toordinal() + 1721424.5 + (dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600)/24
    t = (jd - 2451545.0)/36525
    L0 = (280.46646 + t*(36000.76983 + t*0.0003032)) % 360
    M  = 357.52911 + t*(35999.05029 - 0.0001537*t)
    e  = 0.016708634 - t*(0.000042037 + 0.0000001267*t)
    Mr = math.radians(M)
    C  = (math.sin(Mr)*(1.914602 - t*(0.004817+0.000014*t))
          + math.sin(2*Mr)*(0.019993-0.000101*t) + math.sin(3*Mr)*0.000289)
    true_long = L0 + C
    omega = 125.04 - 1934.136*t
    app_long = true_long - 0.00569 - 0.00478*math.sin(math.radians(omega))
    eps0 = 23 + (26 + (21.448 - t*(46.815 + t*(0.00059 - t*0.001813)))/60)/60
    eps  = eps0 + 0.00256*math.cos(math.radians(omega))
    decl = math.degrees(math.asin(math.sin(math.radians(eps))*math.sin(math.radians(app_long))))
    y = math.tan(math.radians(eps/2))**2
    L0r = math.radians(L0)
    eot = 4*math.degrees(y*math.sin(2*L0r) - 2*e*math.sin(Mr)
                         + 4*e*y*math.sin(Mr)*math.cos(2*L0r)
                         - 0.5*y*y*math.sin(4*L0r) - 1.25*e*e*math.sin(2*Mr))
    mins = dt_utc.hour*60 + dt_utc.minute + dt_utc.second/60
    tst = (mins + eot + 4*lon) % 1440
    ha = tst/4 - 180
    lr, dr, hr = map(math.radians, (lat, decl, ha))
    z = math.acos(min(1, max(-1, math.sin(lr)*math.sin(dr) + math.cos(lr)*math.cos(dr)*math.cos(hr))))
    elev = 90 - math.degrees(z)
    az = math.degrees(math.acos(min(1, max(-1,
         (math.sin(lr)*math.cos(z) - math.sin(dr))/(math.cos(lr)*math.sin(z))))))
    az = (az + 180) % 360 if ha > 0 else (540 - az) % 360
    return elev, az

def find(date, target_elev, rising, lat, lon, tz):
    """Local clock time (minutes past midnight) when the sun crosses target_elev."""
    lo, hi = (0, 12*60) if rising else (12*60, 24*60)
    for _ in range(60):
        mid = (lo+hi)/2
        utc = datetime.datetime.combine(date, datetime.time()) + datetime.timedelta(minutes=mid-tz*60)
        e, _ = solar(utc, lat, lon)
        if (e < target_elev) == rising: lo = mid
        else: hi = mid
    return (lo+hi)/2

def hm(m):
    t = int(round(m)); return f"{t//60:02d}:{t%60:02d}"

# Golden hour is taken as sun altitude +6deg -> 0deg (the standard warm-light
# window); civil-twilight blue light runs 0deg -> -6deg.
SITES = {
    "Dubai (Business Bay)":   (25.1855, 55.2625, 4.0),
    "Abu Dhabi (Corniche)":   (24.4539, 54.3773, 4.0),
    "Delhi (reference)":      (28.6139, 77.2090, 5.5),
    "London (reference)":     (51.5072, -0.1276, 1.0),
}
names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

def budget(lat, lon, tz, d):
    ss  = find(d, -0.833, False, lat, lon, tz)   # sunset (refraction-corrected)
    g_s = find(d,  6.0,   False, lat, lon, tz)   # golden hour starts
    b_e = find(d, -6.0,   False, lat, lon, tz)   # civil twilight ends
    az  = solar(datetime.datetime.combine(d, datetime.time())
                + datetime.timedelta(minutes=ss-tz*60), lat, lon)[1]
    return dict(sunset=hm(ss), golden=f"{hm(g_s)}-{hm(ss)}", golden_min=round(ss-g_s),
                blue=f"{hm(ss)}-{hm(b_e)}", blue_min=round(b_e-ss),
                total_min=round(b_e-g_s), az=round(az, 1))

out = {}
for site, (lat, lon, tz) in SITES.items():
    print(f"\n=== EVENING LIGHT BUDGET - {site} ===")
    print(f"{'MO':<5}{'SUNSET':>8}{'GOLDEN WINDOW':>16}{'GOLD':>6}{'BLUE WINDOW':>14}{'BLUE':>6}{'TOTAL':>7}{'SUN AZ':>8}")
    rows = {}
    for mo in range(1, 13):
        b = budget(lat, lon, tz, datetime.date(2026, mo, 15))
        rows[names[mo-1]] = b
        print(f"{names[mo-1]:<5}{b['sunset']:>8}{b['golden']:>16}{str(b['golden_min'])+'m':>6}"
              f"{b['blue']:>14}{str(b['blue_min'])+'m':>6}{str(b['total_min'])+'m':>7}{str(b['az'])+'d':>8}")
    g = [r['golden_min'] for r in rows.values()]
    t = [r['total_min'] for r in rows.values()]
    print(f"  golden hour: min {min(g)}m / max {max(g)}m / spread {max(g)-min(g)}m"
          f"   |  total usable: {min(t)}-{max(t)}m")
    out[site] = rows

# Solstice-day extremes, the two dates a crew plans the hardest around.
print("\n=== SOLSTICE COMPARISON (21 Jun / 21 Dec) ===")
print(f"{'SITE':<24}{'21 JUN GOLD':>13}{'21 DEC GOLD':>13}{'21 JUN TOTAL':>14}{'21 DEC TOTAL':>14}")
for site, (lat, lon, tz) in SITES.items():
    j = budget(lat, lon, tz, datetime.date(2026, 6, 21))
    dc = budget(lat, lon, tz, datetime.date(2026, 12, 21))
    print(f"{site:<24}{str(j['golden_min'])+'m':>13}{str(dc['golden_min'])+'m':>13}"
          f"{str(j['total_min'])+'m':>14}{str(dc['total_min'])+'m':>14}")

json.dump(out, open('film_light.json', 'w'), indent=1)
print("\nwrote film_light.json")
