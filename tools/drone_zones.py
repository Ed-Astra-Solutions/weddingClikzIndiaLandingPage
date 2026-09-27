"""
How far each UAE wedding location sits from the nearest airport/airfield.

Why this exists: GCAA rules bar recreational/unapproved drone flight within
5 km of a UAE airport's outer fence, heliports, helicopter landing sites and
airfields. That single rule decides whether aerial footage is even legally
possible at a given venue, and no one publishes it per wedding location.

METHOD + HONEST LIMITS
  - Distances are great-circle (haversine) from the venue to the airport
    REFERENCE POINT (ARP), not to the airport's outer fence. A fence sits
    1-3 km outside the ARP, so the true clearance is SMALLER than the number
    printed here. Anything under ~8 km should be treated as "assume you are
    inside the zone until DCAA/GCAA says otherwise".
  - Helipads are not included: Dubai has many rooftop helipads (including on
    Burj Al Arab and several Marina/Downtown towers) that are not published
    as a clean dataset. They only ever shrink the legal envelope further.
  - This is a planning aid for shot-listing, not an airspace authorisation.
    The authority of record is DCAA (Dubai) / GCAA (federal).

Run: python3 drone_zones.py
"""
import math

R_KM = 6371.0088          # IUGG mean Earth radius
LIMIT_KM = 5.0            # GCAA exclusion radius, measured from the outer fence
CAUTION_KM = 8.0          # ARP-based buffer that absorbs fence offset

def haversine(a, b):
    (la1, lo1), (la2, lo2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2)
    dp = p2 - p1
    dl = math.radians(lo2 - lo1)
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R_KM*math.asin(math.sqrt(h))

# Airport / airfield reference points
AIRFIELDS = {
    "DXB Dubai Intl":            (25.2532, 55.3657),
    "DWC Al Maktoum Intl":       (24.8964, 55.1614),
    "SHJ Sharjah Intl":          (25.3286, 55.5172),
    "AUH Abu Dhabi Intl":        (24.4330, 54.6511),
    "Al Bateen Executive":       (24.4283, 54.4581),
    "RKT Ras Al Khaimah Intl":   (25.6135, 55.9388),
    "Al Ain Intl":               (24.2617, 55.6092),
    "Fujairah Intl":             (25.1122, 56.3240),
}

# Wedding / pre-wedding locations couples actually ask for
VENUES = [
    ("Business Bay (our studio)",        25.1855, 55.2625),
    ("Downtown / Burj Khalifa",          25.1972, 55.2744),
    ("Al Seef, Dubai Creek",             25.2631, 55.2972),
    ("Madinat Jumeirah",                 25.1336, 55.1853),
    ("Palm Jumeirah / Atlantis",         25.1304, 55.1171),
    ("Dubai Marina / JBR",               25.0805, 55.1403),
    ("Expo City Dubai",                  24.9605, 55.1500),
    ("Bab Al Shams desert resort",       24.8083, 55.2372),
    ("Al Qudra Lakes",                   24.8100, 55.3400),
    ("Hatta",                            24.8000, 56.1170),
    ("Emirates Palace, Abu Dhabi",       24.4614, 54.3172),
    ("Saadiyat Island, Abu Dhabi",       24.5430, 54.4297),
    ("Abu Dhabi Corniche",               24.4744, 54.3391),
    ("Qasr Al Sarab, Liwa",              23.0470, 53.7780),
    ("Waldorf Astoria, Ras Al Khaimah",  25.7100, 55.7700),
]

print(f"{'LOCATION':<34}{'NEAREST AIRFIELD':<26}{'ARP DIST':>9}   VERDICT")
print("-"*95)
rows = []
for name, lat, lon in VENUES:
    near, dist = min(((k, haversine((lat, lon), v)) for k, v in AIRFIELDS.items()),
                     key=lambda t: t[1])
    if dist <= LIMIT_KM:
        verdict = "INSIDE 5 km - no drone without DCAA/GCAA approval"
    elif dist <= CAUTION_KM:
        verdict = "MARGINAL - fence offset may put you inside; verify"
    else:
        verdict = "outside 5 km - still needs registration + approval"
    rows.append((name, near, dist, verdict))
    print(f"{name:<34}{near:<26}{dist:>7.1f}km   {verdict}")

print("\nSummary")
ins = [r for r in rows if r[2] <= LIMIT_KM]
marg = [r for r in rows if LIMIT_KM < r[2] <= CAUTION_KM]
out = [r for r in rows if r[2] > CAUTION_KM]
print(f"  inside 5 km of an airfield ARP : {len(ins)}/{len(rows)}")
print(f"  marginal (5-8 km)              : {len(marg)}/{len(rows)}")
print(f"  clear of the 8 km buffer        : {len(out)}/{len(rows)}")
print("\n  clear: " + ", ".join(r[0] for r in out))
