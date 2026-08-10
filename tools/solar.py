import math, datetime
LAT, LON, TZ = 25.1857, 55.2769, 4.0   # Business Bay, Dubai

def solar(dt_utc):
    """NOAA solar position. Returns (elevation_deg, azimuth_deg from North CW)."""
    jd = dt_utc.toordinal() + 1721424.5 + (dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600)/24
    t = (jd - 2451545.0)/36525
    L0 = (280.46646 + t*(36000.76983 + t*0.0003032)) % 360
    M  = 357.52911 + t*(35999.05029 - 0.0001537*t)
    e  = 0.016708634 - t*(0.000042037 + 0.0000001267*t)
    Mr = math.radians(M)
    C  = math.sin(Mr)*(1.914602 - t*(0.004817+0.000014*t)) + math.sin(2*Mr)*(0.019993-0.000101*t) + math.sin(3*Mr)*0.000289
    true_long = L0 + C
    omega = 125.04 - 1934.136*t
    app_long = true_long - 0.00569 - 0.00478*math.sin(math.radians(omega))
    eps0 = 23 + (26 + (21.448 - t*(46.815 + t*(0.00059 - t*0.001813)))/60)/60
    eps  = eps0 + 0.00256*math.cos(math.radians(omega))
    decl = math.degrees(math.asin(math.sin(math.radians(eps))*math.sin(math.radians(app_long))))
    y = math.tan(math.radians(eps/2))**2
    L0r = math.radians(L0)
    eot = 4*math.degrees(y*math.sin(2*L0r) - 2*e*math.sin(Mr) + 4*e*y*math.sin(Mr)*math.cos(2*L0r)
                         - 0.5*y*y*math.sin(4*L0r) - 1.25*e*e*math.sin(2*Mr))
    mins = dt_utc.hour*60 + dt_utc.minute + dt_utc.second/60
    tst = (mins + eot + 4*LON) % 1440
    ha = tst/4 - 180
    lr, dr, hr = map(math.radians, (LAT, decl, ha))
    z = math.acos(min(1,max(-1,math.sin(lr)*math.sin(dr) + math.cos(lr)*math.cos(dr)*math.cos(hr))))
    elev = 90 - math.degrees(z)
    az = math.degrees(math.acos(min(1,max(-1,(math.sin(lr)*math.cos(z) - math.sin(dr))/(math.cos(lr)*math.sin(z))))))
    az = (az + 180) % 360 if ha > 0 else (540 - az) % 360
    return elev, az

def find(date, target_elev, rising):
    """Local time (minutes) when sun crosses target elevation."""
    lo, hi = (0, 12*60) if rising else (12*60, 24*60)
    for _ in range(60):
        mid = (lo+hi)/2
        utc = datetime.datetime.combine(date, datetime.time()) + datetime.timedelta(minutes=mid-TZ*60)
        e,_ = solar(utc)
        if (e < target_elev) == rising: lo = mid
        else: hi = mid
    return (lo+hi)/2

def hm(m): return f"{int(m)//60:02d}:{int(round(m))%60:02d}"

print(f"{'MONTH':4} {'SUNRISE':>7} {'SUNSET':>7} {'GOLDEN HOUR (6°→0°)':>21} {'BLUE HR END':>11} {'SUNSET AZ':>9} {'NOON ELEV':>9} {'SHADOW@6°':>9}")
rows=[]
for mo in range(1,13):
    d = datetime.date(2026, mo, 15)
    sr, ss = find(d,-0.833,True), find(d,-0.833,False)
    g6 = find(d, 6, False); b6 = find(d, -6, False)
    _, az = solar(datetime.datetime.combine(d, datetime.time()) + datetime.timedelta(minutes=ss-TZ*60))
    noon_e,_ = solar(datetime.datetime.combine(d, datetime.time()) + datetime.timedelta(minutes=(sr+ss)/2-TZ*60))
    ratio = 1/math.tan(math.radians(6))
    rows.append((d.strftime('%b'),hm(sr),hm(ss),f"{hm(g6)}–{hm(ss)}",hm(b6),f"{az:.1f}°",f"{noon_e:.1f}°",f"{ratio:.1f}x"))
    print(f"{rows[-1][0]:4} {rows[-1][1]:>7} {rows[-1][2]:>7} {rows[-1][3]:>21} {rows[-1][4]:>11} {rows[-1][5]:>9} {rows[-1][6]:>9} {rows[-1][7]:>9}")
print()
print("Sunset azimuth range across year:", f"{min(float(r[5][:-1]) for r in rows):.1f}° – {max(float(r[5][:-1]) for r in rows):.1f}°")

# ── Which dates does the setting sun align with the Business Bay grid axis? ──
# Sheikh Zayed Rd / Business Bay tower grid runs ~056°/236°; canal axis ~ 240-250°
def sunset_az(d):
    ss = find(d, -0.833, False)
    _, az = solar(datetime.datetime.combine(d, datetime.time()) + datetime.timedelta(minutes=ss-TZ*60))
    return az, ss

print("\n=== SUNSET AZIMUTH BY DATE (alignment windows) ===")
targets = {236.0:"SZR / tower-grid axis", 240.0:"Marasi Dr canal axis", 245.0:"canal bend / Bay Ave"}
for tgt,label in targets.items():
    hits=[]
    prev=None
    for n in range(365):
        d = datetime.date(2026,1,1)+datetime.timedelta(days=n)
        az,ss = sunset_az(d)
        if prev is not None and (prev-tgt)*(az-tgt) <= 0:
            hits.append((d.strftime('%d %b'), hm(ss), f"{az:.1f}"))
        prev = az
    print(f"  {tgt:.0f}° ({label}): " + " | ".join(f"{h[0]} @ {h[1]}" for h in hits))

print("\n=== ANNUAL SUNSET AZIMUTH EXTREMES ===")
best=(999,None); worst=(0,None)
for n in range(365):
    d=datetime.date(2026,1,1)+datetime.timedelta(days=n)
    az,_=sunset_az(d)
    if az<best[0]: best=(az,d)
    if az>worst[0]: worst=(az,d)
print(f"  southernmost sunset {best[0]:.1f}° on {best[1]:%d %b} | northernmost {worst[0]:.1f}° on {worst[1]:%d %b}")

# ── The light line: at what height is a facade still lit, behind a blocking tower ──
print("\n=== SUNLIT-HEIGHT LINE (metres above ground) vs solar elevation ===")
print(f"{'BLOCKER':>8} {'GAP':>5} " + "".join(f"{e:>7}°" for e in (20,15,10,6,3,1)))
for Hb,D in ((150,60),(150,120),(200,80),(250,100),(300,150),(300,300)):
    line=[max(0, Hb - D*math.tan(math.radians(e))) for e in (20,15,10,6,3,1)]
    print(f"{Hb:>6}m {D:>4}m " + "".join(f"{v:>8.0f}" for v in line))
print("\n  (~3.2 m per residential floor → divide by 3.2 for the lit-floor number)")
