# 03 · Sizing for a 4-person house

## 3.1 How much electricity does a 4-person house use?

- Without heat pump or EV: ~4,000-4,500 kWh/yr for a single-family house (EKZ:
  4,050 kWh; ElCom's H4 reference 4,500 kWh). The efficient-to-generous range is 2,000-8,000
  [@ekz-4pers; @elcom2026prices].
- A heat pump adds ~3,000-6,000 kWh/yr, mostly in winter when PV is weak. An EV adds
  ~2,000-3,000 kWh per 15,000 km, and it charges when parked [@ekz-4pers].

## 3.2 Rules of thumb (they agree more than they differ)

| Rule | 4,500 kWh house | 9,000 kWh (HP) | Source |
|---|---|---|---|
| Usable kWh ≈ annual demand / 1,000 | 4.5 kWh | 9 kWh | [@swissolar2025batt] |
| or ≈ 1-2 h of PV peak / annual PV yield / 1,000 | 8-10 kWh for 10 kWp | same | [@swissolar2025batt] |
| Take the **smaller** of the two, max 1.5 kWh per kWp | 4.5-6 kWh | ~9 kWh | [@swissolar2025batt; @stadtzh2026] |
| HTW Berlin: max 1.5 kWh usable per 1,000 kWh/yr | ≤ 6.8 kWh | ≤ 13.5 kWh | [@htw-unabh; @weniger2013dim] |
| EnergieSchweiz: ~1 kWh per kWp (up to 1.5) | 8-12 kWh for 8-12 kWp | – | [@energieschweiz-batt] |
| Swiss self-consumption handbook: 4,500 kWh, 3-6 kWp → 4-6 kWh; self-consumption 30 → up to 70 % | 4-6 kWh | – | [@eigenverbrauch-handbuch] |

✅ For a typical 4-person house without heat pump/EV, **5-8 kWh usable** is the sweet spot. With a heat pump and/or EV,
**8-12 kWh**. Swiss average installed size is larger (13.5 kWh in 2023; 15 kWh is Swissolar's
2025 "typical" system) [@swissolar2025batt; @swissolar2026bm]. Installers often upsize, and every kWh beyond what you cycle
daily lowers the return (ch. 01, "oversized" scenario).

## 3.3 Diminishing returns

A measured Swiss household (4,773 kWh, 5.8 kWp) shows self-sufficiency rising steeply up to
~15 kWh and then flattening. Storing across seasons would take ~300 kWh, and full autarky 1,291 kWh
(about 8 tonnes) [@perchnielsen2020]. Winter self-sufficiency is not achievable with a
home battery. Forum users with 30 kWp and 75-130 kWh still struggle in November [@pvforum-ch-ekz].
Batteries are day-night storage only [@swissolar2025batt; @srf2026bm]. ✅

Typical self-consumption shares: 15-30 % without measures; 40-60 % with heat pump + smart
control; up to 70-80 % with a battery [@beobachter2023; @ekz2025rueck; @eigenverbrauch-handbuch]. ⚠️ Autarky
(share of *demand* covered) is lower than self-consumption (share of *production* used). Installers
sometimes blur the two.

## 3.4 Tools to size with your own data

1. **Your smart-meter 15-minute data** (ask your utility or read it from the meter
   portal). This is the best input.
2. **EnergieSchweiz/Swissolar Solarrechner**: address-based, battery option,
   auto-sizes [@energieschweiz-solarrechner; @sonnendach].
3. **HTW Berlin Unabhängigkeitsrechner**: fast autarky curves. German weather,
   but the shape transfers [@htw-unabh].
4. Independent Swiss calculators (e.g. Eigenwatt). Methods unchecked [@eigenwatt].
5. For unusual profiles, run a time-step simulation (installer or textbook methods
   [@bucher2021pv; @quaschning2016understanding; @quaschning2011regen]).

## Purpose note

- **Essential:** the 5-8 kWh vs 8-12 kWh guidance and "don't oversize".
- **Next step:** download a year of your 15-min data, and check how many kWh you
  use between sunset and sunrise on a typical summer day. That is the most a battery can shift per day.
