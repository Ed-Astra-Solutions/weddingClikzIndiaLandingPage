# Business Bay solar tooling

Generates the computed data published in the Light Line blog series.
All figures in those four posts come from here — nothing is sourced from
third-party sites, so the tables are original and safe to publish as our own.

- `solar.py`   — NOAA solar-position implementation. Sunrise/sunset, golden
                 and blue hour windows, sunset azimuth, shadow multipliers,
                 and the "light line" (lowest sunlit height behind a blocker).
- `almanac.py` — Builds the published tables. Run `python3 almanac.py`.

Coordinates default to the Dubai studio: 25.1855 N, 55.2625 E, UTC+4
(5th Floor, Bay Square, Business Bay).

## Published in

- /blog/business-bay-light-line.html            (all five tables)
- /blog/business-bay-rooftop-photography-floors.html
- /blog/business-bay-canal-golden-hour.html
- /blog/dubai-golden-hour-33-minutes.html       (latitude comparison)

## Verification

Computed sunset times match observed Dubai sunset to within a minute
(Dec ~17:32, Jun ~19:10), which is the check that validated the model.

If you change any number here, update the matching table in the posts —
the almanac post is marked up as schema.org/Dataset and is intended to be
citable, so accuracy is the whole point.
