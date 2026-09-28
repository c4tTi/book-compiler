# 01 · Is a home battery worth it? (economics)

## 1.1 The one mechanism that pays for a battery

A battery earns money one way for a Swiss household: every kWh of midday solar
it stores and releases in the evening is a kWh you **don't buy** (at the retail
price) instead of one you **sell** (at the feed-in price). The value of each
stored kWh is therefore roughly *retail price x efficiency minus feed-in price*.

- Retail: the 2026 median household tariff is **27.7 Rp/kWh** (H4 profile,
  4,500 kWh/yr): about 10.75 Rp grid, 12.11 Rp energy, 2.3 Rp federal
  surcharges, plus local levies. It varies a lot by municipality, from under
  10 to over 36 Rp in Romandie alone [@elcom2026prices; @rts2026batt; @solarpanelswiss2026]. ✅
- Feed-in: since 1 January 2026 the fallback feed-in price is the BFE's quarterly
  PV reference market price, with a legal floor of **6 Rp/kWh** for plants up to
  30 kW, plus up to ~3 Rp for guarantees of origin (HKN) at many utilities
  [@swissolar2026neu; @ekz2025rueck]. The official reference price was
  **10.27 Rp in Q1 2026 but only 3.90 Rp in Q2** (April: 2.3 Rp) [@bfe2026refprice]. In the
  quarters when you have most surplus, you will usually get the 6 Rp floor
  (plus HKN, if your utility pays it). ✅

So each shifted kWh is worth roughly **17-22 Rp** at median tariffs, less in
cheap municipalities, more in expensive ones.

## 1.2 What a battery costs in 2026

| Source | Price quoted | Notes |
|---|---|---|
| Swissolar Batteriemonitor 2026 | ~CHF 8,800 for 15 kWh installed (≈ CHF 586/kWh), −25 % vs 2024 | member survey, industry view [@swissolar2026bm] |
| Swissolar report 2025 | ~CHF 800/kWh average (Dec 2024); installers say 300-600 CHF/kWh would be "economic" | [@swissolar2025batt] |
| RTS / Romandie installers | 10 kWh CHF 6,000-9,500; "halved from 1,000 to 500 CHF/kWh" | [@rts2026batt; @solarpanelswiss2026] |
| Lead-gen sites | Powerwall 3 ~CHF 12,000; BYD 10 kWh ~9,000; Huawei 10 kWh ~8,500 | indicative only [@solarbatt-ch-vergleich] |
| EnergieSchweiz story (current) | 12 kWp + 15 kWh ≈ CHF 8,000 installed | [@energieschweiz-batt] |
| EnergieSchweiz FAQ (2020 data) | CHF 1,140-1,480/kWh | outdated, still on the website [@energieschweiz-solarbatt] |

⚠️ Will prices keep falling? Swissolar reports −25 % in one year [@swissolar2026bm]; an expert quoted by EnergieSchweiz says the market is stabilising and waiting won't pay [@energieschweiz-batt]. Older Swiss and German cost-effectiveness studies show how fast these conclusions date [@vonsien2019cost; @nyholm2016sweden].

Rule of thumb for a 10 kWh retrofit quote in 2026: **CHF 6,000-9,000 installed**;
backup capability adds ~CHF 1,000-2,500 [@beobachter2023; @energieschweiz-solarbatt]. Fixed costs
(planning, installation, admin) are ~40 % of the price, so small batteries
are expensive per kWh [@lenews2026]. ⚠️ prices fall fast; get 2-3 quotes.

## 1.3 The numbers for a typical 4-person house

The workbench model (`workbench/battery_payback.py`) uses: 10 kWh usable, 250
full cycles per year (realistic in Switzerland: many summer cycles, few in
winter), 90 % round-trip efficiency, 2.5 %-points capacity loss per year
(field data: 2-3 %/yr [@figgener2024multiyear]), 27.7 Rp avoided, 7 Rp feed-in lost.

| Scenario | Net cost CHF | Saving yr 1 | Payback |
|---|---:|---:|---|
| CHF 7,500, no subsidy | 7,500 | ~450 | >15 y (≈ break-even at 20 y) |
| + tax deduction at 25 % marginal rate | 5,625 | ~450 | ~16 y |
| + Stadt Zürich subsidy (CHF 2,000) + tax | 4,125 | ~450 | ~11 y |
| Cheap: CHF 5,000 | 5,000 | ~450 | ~14 y |
| High tariff 35 Rp / feed-in 6 Rp | 7,500 | ~640 | ~15 y |
| Low tariff 22 Rp / feed-in 9 Rp | 7,500 | ~270 | never |
| Oversized 15 kWh (fewer cycles) | 8,800 | ~480 | never |

The **cost per stored kWh** is 15-37 Rp across these cases, around 27 Rp
in the base case. That is at or above the ~20 Rp a stored kWh is worth.
Swissolar's own example gets **14.5 Rp per stored kWh** (10 kWh, CHF 7,700, 6,000 cycles,
90 % DoD) [@swissolar2025batt]. The difference is that Swissolar assumes every one of the 6,000 cycles is
used. In Switzerland you use perhaps 200-280 a year, so over 15-20 years a battery rarely
reaches its cycle rating. ⚠️ This utilisation assumption decides the answer. Check it with your own
load data (ch. 03).

## 1.4 What the sources conclude, by lens

- **Official/federal:** EnergieSchweiz: "nur selten rentabel". It is
  most favourable with large PV, high consumption (heat pump, EV) and the
  investment would need to roughly halve [@energieschweiz-solarbatt]. The 2020 federal
  market study found batteries "not economic today" and noted buyers are
  driven by other motives [@perchnielsen2020].
- **Scholarly:** ETH Zurich modelling found that at ~1,000 €/kWh almost no Swiss household profits from adding
  a battery, but at 250 €/kWh nearly all do. Profitability is best with high demand and high
  irradiation [@han2022techno]. Prices in 2026 are between those two points, and so is the answer. ⚠️
- **Industry:** Swissolar 2026: batteries are now "in many cases already
  profitable" thanks to falling prices, lower feed-in and dynamic tariffs
  [@swissolar2026bm]. Installer blogs say similar things, but they are selling batteries [@ecoen-speicher; @energyunlimited2026; @trisol2026].
- **Critical/popular:** Beobachter says batteries "practically never pay for themselves" (2023). Le
  News (Aug 2026) says the maths "still doesn't add up", with payback "well over a decade"
  [@beobachter2023; @lenews2026]. Stiftung Warentest (DE, 2026) finds 4-10 year paybacks in Germany,
  where retail prices are higher [@stiftungwarentest2026]. A homeowner quoted by HEV Schweiz
  calculated a 60-year payback [@hev2025speichern].
- **System view:** A BFE-commissioned study (ZHAW/HSLU/Consentec) finds home
  batteries privately rational but systemically inefficient. They save grid fees that other customers then pay
  [@energeiaplus2026speicher; @schlecht2025speicherbedarf]. 🔎 This creates a policy risk: grid tariffs
  could move toward fixed or power-based charges, which would cut a battery's savings.

## 1.5 Why people buy anyway

Swiss buyers name self-consumption / autarky first, then reaction to low
feed-in, then profitability. "Supporting renewables" and grid-friendly
operation rank low [@swissolar2025batt; @swissolar2026bm]. Backup power and interest in the
technology are further motives. It is legitimate to buy a battery for independence or
backup, as long as you know you are paying for it.

## Purpose note

- **Essential:** §1.1 (value per stored kWh), §1.3 (your payback depends on price, tariff spread and cycles), the
  subsidy/tax effect.
- **Decision rule of thumb:** a battery roughly pays off within its lifetime only if
  (a) the installed price is ≤ ~CHF 600/kWh after subsidies and tax, (b) your
  tariff spread is ≥ ~20 Rp, and (c) it is sized so it cycles on most days.
  Otherwise, treat it as a comfort/backup purchase.
- **Optional:** the system-level debate (§1.4, last bullet), unless you care about grid policy risk.
