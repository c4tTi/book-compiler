#!/usr/bin/env python3
"""Weighted options matrix. Edit WEIGHTS (must sum to 100) and SCORES (1-5), then run."""
WEIGHTS = {  # criterion: weight
    "Financial return": 30,
    "Self-sufficiency / independence": 15,
    "Backup in outages": 10,
    "Future-proof (tariffs, EV, EMS)": 15,
    "Fit with existing PV / simplicity": 10,
    "Environmental benefit": 10,
    "Risk (price drop, tech, warranty)": 10,
}
OPTIONS = {  # option: scores in WEIGHTS order
    "A. No battery: load shifting + heat-pump boiler / EV on surplus": [5, 2, 1, 4, 5, 4, 5],
    "B. Small AC-coupled LFP, 5-8 kWh usable, no backup": [3, 3, 2, 3, 4, 2, 3],
    "C. Hybrid inverter swap + 8-12 kWh LFP with backup": [2, 4, 5, 4, 2, 2, 3],
    "D. All-in-one whole-house (e.g. Powerwall 3P), 13.5 kWh": [2, 4, 5, 3, 3, 2, 2],
    "E. Wait 1-2 years (prices -25%/yr, V2H ~2028)": [4, 1, 1, 5, 5, 3, 4],
}
assert sum(WEIGHTS.values()) == 100
crit = list(WEIGHTS)
print("| Option | " + " | ".join(f"{c} ({WEIGHTS[c]})" for c in crit) + " | **Weighted (max 5)** |")
print("|---|" + "---:|" * (len(crit) + 1))
res = []
for o, s in OPTIONS.items():
    w = sum(WEIGHTS[c] * v for c, v in zip(crit, s)) / 100
    res.append((w, o))
    print(f"| {o} | " + " | ".join(str(v) for v in s) + f" | **{w:.2f}** |")
print()
for w, o in sorted(res, reverse=True):
    print(f"- {w:.2f}  {o}")
