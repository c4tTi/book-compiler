# Options matrix: battery yes/no, and which

Scores 1-5 (5 = best) are judgments based on the cited chapters. Weights reflect a
**money-first** household (default). Recompute with your own weights:
`python3 options_matrix.py` (edit WEIGHTS/OPTIONS at the top). Payback figures come from
`python3 battery_payback.py` (edit or pass `--capex --usable --cycles --buy --sell`).

## Evidence per criterion

| Criterion | Key evidence |
|---|---|
| Financial return | Each stored kWh is worth ~17-22 Rp at median tariffs. Cost per stored kWh is ~27 Rp at CHF 750/kWh and 250 cycles/yr, ~18 Rp at CHF 500/kWh. Payback 11 to >20 y (ch. 01) [@elcom2026prices; @bfe2026refprice; @swissolar2026bm; @han2022techno] |
| Self-sufficiency | A battery raises self-consumption from ~30-60 % to up to 70-80 %. It adds nothing in winter [@beobachter2023; @perchnielsen2020; @eigenverbrauch-handbuch] |
| Backup | Needs a backup-capable hybrid/all-in-one and a transfer switch. An AC retrofit usually gives at most one socket [@swissolar-netzausfall] |
| Future-proof | Dynamic tariffs (EKZ, Groupe E) need an EMS. V2H interoperability expected ~2028. Tariff-structure risk [@ekz2025dyn; @energieschweiz-bidi; @energeiaplus2026speicher] |
| Fit / simplicity | AC coupling works with any inverter; DC needs a hybrid or inverter replacement [@acspeicher-pvorg; @sungrow-vs-byd] |
| Environmental | Low-carbon Swiss grid means little CO2 saved by shifting. Embodied impact is dominated by cell production [@treeze2018lca; @energeiaplus2026speicher] |
| Risk | Prices fell ~25 % in a year. 2-3 %/yr capacity fade. Warranty fine print varies [@swissolar2026bm; @figgener2024multiyear; @memodo-htw2026] |

## Matrix (money-first weights)

| Option | Financial return (30) | Self-sufficiency / independence (15) | Backup in outages (10) | Future-proof (tariffs, EV, EMS) (15) | Fit with existing PV / simplicity (10) | Environmental benefit (10) | Risk (price drop, tech, warranty) (10) | **Weighted (max 5)** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A. No battery: load shifting + heat-pump boiler / EV on surplus | 5 | 2 | 1 | 4 | 5 | 4 | 5 | **3.90** |
| B. Small AC-coupled LFP, 5-8 kWh usable, no backup | 3 | 3 | 2 | 3 | 4 | 2 | 3 | **2.90** |
| C. Hybrid inverter swap + 8-12 kWh LFP with backup | 2 | 4 | 5 | 4 | 2 | 2 | 3 | **3.00** |
| D. All-in-one whole-house (e.g. Powerwall 3P), 13.5 kWh | 2 | 4 | 5 | 3 | 3 | 2 | 2 | **2.85** |
| E. Wait 1-2 years (prices -25%/yr, V2H ~2028) | 4 | 1 | 1 | 5 | 5 | 3 | 4 | **3.40** |

- 3.90  A. No battery: load shifting + heat-pump boiler / EV on surplus
- 3.40  E. Wait 1-2 years (prices -25%/yr, V2H ~2028)
- 3.00  C. Hybrid inverter swap + 8-12 kWh LFP with backup
- 2.90  B. Small AC-coupled LFP, 5-8 kWh usable, no backup
- 2.85  D. All-in-one whole-house (e.g. Powerwall 3P), 13.5 kWh

**Sensitivity:** with **independence/backup-first** weights (financial 15, independence 25,
backup 20, future-proof 15, fit 10, environment 5, risk 10), the order flips:
C 3.50 · D 3.35 · A 3.25 · B 2.85 · E 2.85.

## Payback model output (base assumptions, 15-year life)

| Scenario | Net invest CHF | Saving yr 1 CHF | Saving 15 y CHF | NPV CHF | Cost/stored kWh Rp | Payback (y) |
|---|---:|---:|---:|---:|---:|---:|
| Base: 10 kWh, CHF 7500, 250 cyc, 27.7/7 Rp | 7,500 | 448 | 5,547 | -1,953 | 26.9 | >15 |
| Base + tax deduction (25 %) | 5,625 | 448 | 5,547 | -78 | 20.2 | >15 |
| Base + Stadt ZH subsidy + tax | 4,125 | 448 | 5,547 | 1,422 | 14.8 | 11 |
| Cheap: 10 kWh, CHF 5000 (~500/kWh) | 5,000 | 448 | 5,547 | 547 | 18.0 | 14 |
| Expensive: 10 kWh, CHF 10000 | 10,000 | 448 | 5,547 | -4,453 | 35.9 | >15 |
| High tariff 35 Rp, sell 6 Rp | 7,500 | 638 | 7,889 | 389 | 26.9 | 15 |
| Low tariff 22 Rp, sell 9 Rp | 7,500 | 270 | 3,341 | -4,159 | 26.9 | >15 |
| Oversized: 15 kWh, CHF 8800, 180 cyc | 8,800 | 484 | 5,991 | -2,809 | 29.3 | >15 |
| Heat pump/EV house: 10 kWh, 300 cyc | 7,500 | 538 | 6,657 | -843 | 22.4 | >15 |
| Low use: 10 kWh, 180 cyc | 7,500 | 323 | 3,994 | -3,506 | 37.4 | >15 |

Assumptions: RTE 90%, fade 2.5%/yr, life 15 y, discount 0%.

With a 20-year life (LFP at ~250 cycles/yr may last that long), the base case is at break-even and the
tax/subsidy cases pay back in 11-16 years (`--life 20`).

## Recommendation (confidence: medium)

- **Do A regardless.** Load shifting, heat-pump boiler or boiler on surplus, and EV charging on surplus are the
  cheapest self-consumption gains, and they shrink the battery you would need.
- **If money is the main criterion:** don't buy yet unless you can get ≤ ~CHF 600/kWh installed
  after subsidy and tax, with a tariff spread ≥ 20 Rp. Otherwise re-quote in 12-18 months (**E**). ⚠️ Counterpoint: an expert quoted by EnergieSchweiz expects prices to stabilise and advises against waiting [@energieschweiz-batt], so waiting is a bet, not a sure gain.
- **If independence/backup matters:** choose **C** (hybrid inverter + 8-12 kWh LFP with backup),
  especially if your inverter is > 8-10 years old. Choose **B** (small AC-coupled) if your inverter is
  young and backup is not needed.
- Confidence is medium because the answer hinges on inputs we don't have yet: your tariff, feed-in
  terms, canton, inverter model/age, and 15-min load data (see `open-questions.md`).
