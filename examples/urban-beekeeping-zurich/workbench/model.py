#!/usr/bin/env python3
"""Start-up and running cost model for a small Zurich balcony/roof apiary.

Run:  python3 workbench/model.py
Edit the INPUTS block with your own quotes. Every input names its source ([@id] in
sources.jsonl) or says ASSUMPTION. Prices seen 2026-09-28; they change.
"""

# ---------------------------------------------------------------- INPUTS (CHF)
INPUTS = {
    # Training
    "course_grundkurs_2yr": 950,      # [@zbfkurse] Zürcher Bienenfreunde, incl. Bienenbuch + folder; BienenSchweiz range 950-1250 [@bsimkerwerden]
    "course_wabe3": 950,              # [@wabe3] 10 x 4 h
    "course_stadtbienen_eur": 560,    # [@stadtbienenkurs] EUR, 1 year
    # One-off equipment per beekeeper (Zürcher Bienenfreunde item list [@zbfwerden])
    "personal_gear_low": 80, "personal_gear_high": 150,   # suit/veil, gloves
    "hive_care_tools": 200,           # smoker, hive tool, brush, feeder, varroa tray etc.
    # Per colony
    "hive_with_accessories": 500,     # [@zbfwerden] new hive incl. accessories
    "colony_low": 150,                # [@zbfwerden]; marketplace Jungvölker CHF 85-250 [@bsmarktplatz]
    "colony_high": 350,               # [@apimat] overwintered Jungvolk CHF 350 (summer Jungvolk CHF 250)
    "varroa_meds_per_colony_yr": 30,  # ASSUMPTION: formic + oxalic acid products per colony/year; get a quote
    "sugar_per_colony_yr": 40,        # ASSUMPTION: ~15-20 kg winter feed; price not sourced
    # Annual memberships
    "bienenzeitung_yr": 80,           # [@zbfkurse] 1st year free, then CHF 80 (gives subsidiary liability cover [@haftpflicht])
    "club_membership_yr": 50,         # [@zbfkurse] 1st year free, then CHF 50
    # Honey (optional upside)
    "honey_kg_per_colony": 11,        # [@wikiimkereich] Swiss average ~11 kg/colony; urban yields vary widely
    "honey_value_per_kg": 0,          # set e.g. 30 if you sell; 0 = you keep/give it away. Selling triggers LGV Art. 20 notification [@lmrhonig2022]
}


def startup(colonies, course, colony_price):
    i = INPUTS
    gear = (i["personal_gear_low"] + i["personal_gear_high"]) / 2 + i["hive_care_tools"]
    per_colony = i["hive_with_accessories"] + colony_price
    return course + gear + colonies * per_colony


def running(colonies):
    i = INPUTS
    return (i["bienenzeitung_yr"] + i["club_membership_yr"]
            + colonies * (i["varroa_meds_per_colony_yr"] + i["sugar_per_colony_yr"]))


def honey_income(colonies):
    i = INPUTS
    return colonies * i["honey_kg_per_colony"] * i["honey_value_per_kg"]


if __name__ == "__main__":
    i = INPUTS
    courses = {"Grundkurs (club, 2 yrs)": i["course_grundkurs_2yr"],
               "Wabe3 (10 sessions)": i["course_wabe3"],
               "Stadtbienen (EUR 560 ~ CHF 525)": 525}
    print("Base case: 1 colony, club Grundkurs, colony CHF 250")
    b = startup(1, i["course_grundkurs_2yr"], 250)
    print(f"  start-up total      CHF {b:,.0f}")
    print(f"  running per year    CHF {running(1):,.0f}  (from year 2)")
    print()
    print("Sensitivity (start-up CHF | running CHF/yr)")
    print(f"{'course':34s} {'colonies':>8s} {'colony CHF':>10s} {'start-up':>9s} {'running':>8s}")
    for cname, cprice in courses.items():
        for n in (1, 2):
            for cp in (i["colony_low"], i["colony_high"]):
                print(f"{cname:34s} {n:8d} {cp:10d} {startup(n, cprice, cp):9,.0f} {running(n):8,.0f}")
    print()
    print("Cost over first 3 years (1 vs 2 colonies, club course, colony CHF 250):")
    for n in (1, 2):
        total = startup(n, i["course_grundkurs_2yr"], 250) + 2 * running(n)
        print(f"  {n} colony/ies: CHF {total:,.0f}  (honey income counted: CHF {3*honey_income(n):,.0f})")
    print()
    print("Note: Zürcher Bienenfreunde quote a total of CHF 430-650, but their own item list"
          " sums to CHF 930-1000 per first colony + gear; this model uses the item list.")


# ---------------------------------------------------------------- OPTIONS MATRIX
# Scores 1 (poor) - 5 (good). Weights sum to 1. Evidence per cell is in options-matrix.md.
# Change weights/scores to your own situation and rerun.
WEIGHTS = {"legal_simplicity": 0.20, "neighbour_risk": 0.20, "bee_welfare_site": 0.15,
           "practicality": 0.15, "learning_value": 0.15, "biodiversity": 0.15}
OPTIONS = {
    #                      legal neighb  site  pract learn  biod
    "A Balcony hive":      (3,    2,     3,    2,    5,     2),
    "B Roof hive":         (2,    4,     2,    2,    5,     2),
    "C Off-site (club/garden)": (4, 4,   4,    3,    5,     2),
    "D Course + sponsorship, no own bees": (5, 5, 5, 5, 3,  3),
    "E Wild-bee balcony only": (5,  5,     5,    5,    2,     4),
}


def matrix():
    keys = list(WEIGHTS)
    print("Weighted options matrix (higher = better)")
    for name, scores in sorted(OPTIONS.items(), key=lambda kv: -sum(WEIGHTS[k]*s for k, s in zip(keys, kv[1]))):
        total = sum(WEIGHTS[k] * s for k, s in zip(keys, scores))
        print(f"  {name:40s} {total:.2f}")
    print("  Sensitivity: weight learning_value 0.35 (others scaled down):")
    w2 = {k: (0.35 if k == "learning_value" else v * 0.65 / 0.85) for k, v in WEIGHTS.items()}
    for name, scores in OPTIONS.items():
        print(f"    {name:38s} {sum(w2[k]*s for k, s in zip(keys, scores)):.2f}")


if __name__ == "__main__":
    print()
    matrix()
