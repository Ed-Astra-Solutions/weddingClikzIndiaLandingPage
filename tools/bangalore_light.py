"""
Pre-wedding shoot light planner for Bangalore.

Same NOAA solar core as solar.py / almanac.py / film_light.py, re-pointed at
Bangalore (12.97 N) and asked the questions a couple planning a pre-wedding
shoot actually has:

  - what time does usable light start, and when must we be at the gate
  - how many minutes of golden light do we really get
  - which compass direction is the light coming from that month
  - how does Bangalore compare with places that get a long, lazy golden hour

The latitude point is the headline: Bangalore sits at 12.97 N, closer to the
equator than Dubai (25.19 N), so the sun sets more steeply and the golden
window is SHORTER than most couples (and most photographers' Pinterest
references, which are shot in Europe or North America) assume.

Run: python3 bangalore_light.py
Everything here is computed, not sourced.
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

def compass(az):
    pts = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return pts[int((az % 360)/22.5 + 0.5) % 16]

BLR = (12.9716, 77.5946, 5.5)          # Bangalore
names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

print("=== TABLE 1: BANGALORE PRE-WEDDING LIGHT WINDOWS (15th of each month) ===")
print("Morning golden = sunrise to sun at +6deg.  Evening golden = +6deg to sunset.")
print(f"\n{'MO':<5}{'SUNRISE':>8}{'MORNING GOLDEN':>17}{'MIN':>5}{'GATE':>7}"
      f"{'EVENING GOLDEN':>17}{'MIN':>5}{'SUNSET':>8}{'LIGHT FROM':>12}")
lat, lon, tz = BLR
data = {}
for mo in range(1, 13):
    d = datetime.date(2026, mo, 15)
    sr  = find(d, -0.833, True,  lat, lon, tz)
    ss  = find(d, -0.833, False, lat, lon, tz)
    mge = find(d, 6.0,   True,  lat, lon, tz)     # morning golden ends
    egs = find(d, 6.0,   False, lat, lon, tz)     # evening golden starts
    az_sr = solar(datetime.datetime.combine(d, datetime.time())
                  + datetime.timedelta(minutes=sr-tz*60), lat, lon)[1]
    az_ss = solar(datetime.datetime.combine(d, datetime.time())
                  + datetime.timedelta(minutes=ss-tz*60), lat, lon)[1]
    gate = sr - 20                                  # be on location 20 min early
    data[names[mo-1]] = dict(sunrise=hm(sr), sunset=hm(ss),
        morning=f"{hm(sr)}-{hm(mge)}", morning_min=round(mge-sr), gate=hm(gate),
        evening=f"{hm(egs)}-{hm(ss)}", evening_min=round(ss-egs),
        az_sunrise=round(az_sr,1), az_sunset=round(az_ss,1),
        from_sunrise=compass(az_sr), from_sunset=compass(az_ss))
    v = data[names[mo-1]]
    print(f"{names[mo-1]:<5}{v['sunrise']:>8}{v['morning']:>17}{str(v['morning_min'])+'m':>5}"
          f"{v['gate']:>7}{v['evening']:>17}{str(v['evening_min'])+'m':>5}{v['sunset']:>8}"
          f"{v['from_sunrise']+'/'+v['from_sunset']:>12}")

mg = [v['morning_min'] for v in data.values()]
eg = [v['evening_min'] for v in data.values()]
print(f"\n  morning golden: {min(mg)}-{max(mg)} min   evening golden: {min(eg)}-{max(eg)} min")
print(f"  earliest sunrise {min(v['sunrise'] for v in data.values())}"
      f"   latest sunrise {max(v['sunrise'] for v in data.values())}")

print("\n=== TABLE 2: WHY BANGALORE'S GOLDEN HOUR IS SHORT (latitude effect) ===")
print("Evening golden-hour length on the equinox and both solstices.\n")
CITIES = {
    "Bangalore":  (12.9716, 77.5946, 5.5),
    "Dubai":      (25.1855, 55.2625, 4.0),
    "Delhi":      (28.6139, 77.2090, 5.5),
    "London":     (51.5072, -0.1276, 1.0),
    "Reykjavik":  (64.1466, -21.9426, 0.0),
}
DATES = [("21 Mar", datetime.date(2026,3,21)),
         ("21 Jun", datetime.date(2026,6,21)),
         ("21 Dec", datetime.date(2026,12,21))]
print(f"{'CITY':<12}{'LAT':>7}" + "".join(f"{lbl:>10}" for lbl,_ in DATES))
for city,(la,lo,tz_) in CITIES.items():
    cells=[]
    for _,d in DATES:
        ss=find(d,-0.833,False,la,lo,tz_); gs=find(d,6.0,False,la,lo,tz_)
        cells.append(f"{round(ss-gs)}m")
    print(f"{city:<12}{str(la)+'d':>7}" + "".join(f"{c:>10}" for c in cells))
print("\n  The sun's path is steeper near the equator, so the warm window closes faster.")
print("  A Bangalore couple gets roughly half the golden light a London couple does.")

json.dump(data, open('bangalore_light.json','w'), indent=1)
print("\nwrote bangalore_light.json")

# ---------------------------------------------------------------------------
# TABLE 3: the Nandi Hills gate problem.
#
# Nandi Hills is THE sunrise pre-wedding location near Bangalore, but the gate
# opens at 06:00 and the climb from the gate to the summit viewpoints takes
# about 20 minutes by car. In summer, Bangalore's sunrise is EARLIER than the
# gate opens, so the warm light is already spent by the time a couple is in
# position. Combining the computed sunrise with the published gate time shows
# exactly which months work and which do not.
# ---------------------------------------------------------------------------
GATE_OPEN  = 6*60        # 06:00, published Nandi Hills opening time
CLIMB_MIN  = 20          # gate to summit viewpoint, by car

print("\n=== TABLE 3: NANDI HILLS SUNRISE SHOOT - USABLE GOLDEN MINUTES ===")
print(f"Gate opens {hm(GATE_OPEN)}; allow {CLIMB_MIN} min gate-to-summit, so earliest")
print(f"in-position time is {hm(GATE_OPEN+CLIMB_MIN)}.\n")
print(f"{'MO':<5}{'SUNRISE':>8}{'GOLDEN ENDS':>13}{'IN POSITION':>13}{'USABLE':>8}   VERDICT")
nandi = {}
for mo in range(1, 13):
    d = datetime.date(2026, mo, 15)
    sr  = find(d, -0.833, True, lat, lon, tz)
    mge = find(d, 6.0,    True, lat, lon, tz)
    in_pos  = max(GATE_OPEN + CLIMB_MIN, sr)      # cannot shoot before light or before access
    usable  = max(0, mge - in_pos)
    full    = mge - sr
    if usable >= full - 1:      verdict = "full window - best months"
    elif usable >= 15:          verdict = "workable, arrive at opening"
    elif usable > 0:            verdict = "marginal - most of the light is gone"
    else:                       verdict = "no golden light left"
    nandi[names[mo-1]] = dict(sunrise=hm(sr), golden_ends=hm(mge),
                              in_position=hm(in_pos), usable_min=round(usable),
                              full_min=round(full), verdict=verdict)
    print(f"{names[mo-1]:<5}{hm(sr):>8}{hm(mge):>13}{hm(in_pos):>13}"
          f"{str(round(usable))+'m':>8}   {verdict}")

best = [m for m,v in nandi.items() if v['usable_min'] >= v['full_min']-1]
worst= [m for m,v in nandi.items() if v['usable_min'] < 15]
print(f"\n  full golden window available : {', '.join(best)}")
print(f"  compromised (<15 min usable)  : {', '.join(worst)}")
print("  Sunrise shoots at Nandi Hills are a winter proposition, not a summer one.")

json.dump(dict(monthly=data, nandi=nandi), open('bangalore_light.json','w'), indent=1)
print("\nrewrote bangalore_light.json (monthly + nandi)")
