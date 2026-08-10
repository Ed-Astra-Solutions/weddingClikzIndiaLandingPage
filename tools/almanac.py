import math, datetime, json
LAT, LON, TZ = 25.1855, 55.2625, 4.0
exec(open('solar.py').read().split('print(')[0].split('# ──')[0].replace('LAT, LON, TZ = 25.1857, 55.2769, 4.0','pass'))

M={}
for mo in range(1,13):
    d=datetime.date(2026,mo,15)
    sr=find(d,-0.833,True); ss=find(d,-0.833,False)
    g_start=find(d,6,False); g_end=ss
    blue=find(d,-6,False); night=find(d,-12,False)
    m_g_end=find(d,6,True); m_blue=find(d,-6,True)
    az_ss=solar(datetime.datetime.combine(d,datetime.time())+datetime.timedelta(minutes=ss-TZ*60))[1]
    az_sr=solar(datetime.datetime.combine(d,datetime.time())+datetime.timedelta(minutes=sr-TZ*60))[1]
    noon=(sr+ss)/2; noon_e=solar(datetime.datetime.combine(d,datetime.time())+datetime.timedelta(minutes=noon-TZ*60))[0]
    M[mo]=dict(sr=hm(sr),ss=hm(ss),gm=f"{hm(sr)}–{hm(m_g_end)}",ge=f"{hm(g_start)}–{hm(ss)}",
        blue=f"{hm(ss)}–{hm(blue)}",night=hm(night),azss=round(az_ss,1),azsr=round(az_sr,1),
        noon=hm(noon),noone=round(noon_e,1),daylen=hm(ss-sr))
names="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
print("=== TABLE 1: BUSINESS BAY SOLAR ALMANAC (15th of month) ===")
print(f"{'MO':4}{'SUNRISE':>8}{'SUNSET':>8}{'DAY':>7}{'MORN GOLDEN':>15}{'EVE GOLDEN':>15}{'BLUE HOUR':>15}{'SUNSET AZ':>10}{'NOON ALT':>9}")
for mo in range(1,13):
    v=M[mo]; print(f"{names[mo-1]:4}{v['sr']:>8}{v['ss']:>8}{v['daylen']:>7}{v['gm']:>15}{v['ge']:>15}{v['blue']:>15}{str(v['azss'])+'d':>10}{str(v['noone'])+'d':>9}")

print("\n=== TABLE 2: SHADOW MULTIPLIER vs SUN ALTITUDE ===")
print(f"{'ALT':>5}{'SHADOW x HEIGHT':>18}{'300m TOWER CASTS':>19}")
for e in (60,45,30,20,15,10,6,4,2,1):
    r=1/math.tan(math.radians(e)); print(f"{e:>4}d{r:>17.2f}x{r*300:>17.0f}m")

print("\n=== TABLE 3: THE LIGHT LINE — lowest sunlit height (m) / floor ===")
cases=[("Low-rise neighbour",120),("Mid tower",180),("Tall tower",240),("Super-tall",300)]
gaps=[40,80,150,300]
for name,Hb in cases:
    print(f"\n  Blocking tower {Hb}m ({name})")
    print(f"  {'GAP':>6}" + "".join(f"{str(e)+'d':>12}" for e in (20,15,10,6,3)))
    for D in gaps:
        cells=[]
        for e in (20,15,10,6,3):
            h=max(0,Hb-D*math.tan(math.radians(e)))
            cells.append(f"{h:.0f}m/F{h/3.2:.0f}" if h>0 else "lit/F0")
        print(f"  {D:>5}m" + "".join(f"{c:>12}" for c in cells))

print("\n=== TABLE 4: HOW FAST THE LIGHT LINE CLIMBS (last 40 min of light) ===")
for mo,lbl in ((1,'Jan'),(6,'Jun')):
    d=datetime.date(2026,mo,15); ss=find(d,-0.833,False)
    print(f"\n  {lbl}: minutes before sunset → sun altitude → lit line on a 240m tower @100m gap")
    for off in (40,30,20,10,5,0):
        t=ss-off; e=solar(datetime.datetime.combine(d,datetime.time())+datetime.timedelta(minutes=t-TZ*60))[0]
        h=max(0,240-100*math.tan(math.radians(e)))
        print(f"    T-{off:>2}min  {hm(t)}  alt {e:>4.1f}d   lit above {h:>5.0f}m  (floor {h/3.2:.0f}+)")

print("\n=== TABLE 5: SUNSET AZIMUTH BY MONTH (compass bearing of the sun at sunset) ===")
for mo in range(1,13):
    az=M[mo]['azss']; comp='WSW' if az<255 else 'W' if az<285 else 'WNW'
    print(f"  {names[mo-1]}  {az}d  {comp}")
print(f"\n  Annual swing: {min(M[m]['azss'] for m in M)}d (Dec) to {max(M[m]['azss'] for m in M)}d (Jun) = {max(M[m]['azss'] for m in M)-min(M[m]['azss'] for m in M):.1f}d of arc")
json.dump(M,open('almanac.json','w'),indent=1)
