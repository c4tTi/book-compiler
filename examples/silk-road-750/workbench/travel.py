"""Journey-time estimator for a Chang'an -> Samarkand journey c. 750.

Rerun with your own numbers:  python3 travel.py
Every input is listed at the top with its source. Distances are ROUGH modern
estimates along the historical line of the route (not sourced; refine with
OWTRAD [@owtrad] or CHGIS [@chgis] before relying on them).
"""

# --- inputs -----------------------------------------------------------------
KM_PER_LI = 0.54  # Tang li c. 530-560 m; conventional approximation (verify)

# Official Tang daily travel allowances, attributed to the Tang Liudian
# [@tangliudian] via [@chiculture-posts; @wotc-driving] (search snippets):
OFFICIAL_LI_PER_DAY = {"horse": 70, "foot or donkey": 50, "cart": 30}
# Loaded camel caravan, popular estimate 15-25 miles/day [@fad-caravans] (weak source)
CARAVAN_KM_PER_DAY = {"caravan (slow)": 24, "caravan (fast)": 32}
# Rest / waiting days: market days, pass checks (guosuo) [@hansen2005],
# waiting for weather at passes. Assumption: 1 rest day in 4 marching days.
REST_FACTOR = 1.25

# Stages (from, to, km). Northern Tianshan route via Turfan, Kucha, Bedel
# pass to Suyab, then west through Talas and Chach. ESTIMATES.
STAGES = [
    ("Chang'an", "Liangzhou (Wuwei)", 900),
    ("Liangzhou", "Shazhou (Dunhuang)", 750),
    ("Dunhuang", "Yizhou (Hami)", 400),
    ("Yizhou", "Xizhou (Gaochang/Turfan)", 400),
    ("Xizhou", "Yanqi (Karashahr)", 300),
    ("Yanqi", "Qiuci (Kucha), seat of Anxi", 300),
    ("Kucha", "Aksu", 250),
    ("Aksu", "Suyab (Ak-Beshim) via Bedel pass", 400),
    ("Suyab", "Talas (Taraz)", 280),
    ("Talas", "Chach (Tashkent)", 300),
    ("Chach", "Samarkand", 300),
]
# ----------------------------------------------------------------------------

def days(km, km_per_day, rest=REST_FACTOR):
    return km / km_per_day * rest

def main():
    total = sum(s[2] for s in STAGES)
    modes = {m: li * KM_PER_LI for m, li in OFFICIAL_LI_PER_DAY.items()}
    modes.update(CARAVAN_KM_PER_DAY)
    print(f"Total route (estimate): {total:,} km\n")
    header = f"{'Stage':48s}" + "".join(f"{m[:14]:>16s}" for m in modes)
    print("Days per stage incl. rest factor", REST_FACTOR)
    print(header)
    cum = {m: 0.0 for m in modes}
    for a, b, km in STAGES:
        row = f"{(a + ' -> ' + b)[:44]:44s}{km:4d}"
        for m, v in modes.items():
            d = days(km, v)
            cum[m] += d
            row += f"{d:16.0f}"
        print(row)
    print("-" * len(header))
    print(f"{'TOTAL days':48s}" + "".join(f"{cum[m]:16.0f}" for m in modes))
    print(f"{'TOTAL months (30 d)':48s}" + "".join(f"{cum[m]/30:16.1f}" for m in modes))
    print("\nSensitivity: caravan (slow) total days if distances are off by +/-20% and rest factor 1.0-1.6")
    base = CARAVAN_KM_PER_DAY["caravan (slow)"]
    for dist_mult in (0.8, 1.0, 1.2):
        cells = []
        for rest in (1.0, 1.25, 1.6):
            cells.append(f"rest {rest}: {total*dist_mult/base*rest:5.0f} d")
        print(f"  distance x{dist_mult}:  " + "   ".join(cells))

if __name__ == "__main__":
    main()
