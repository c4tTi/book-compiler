# Home battery for a Swiss PV house: overview

*Compiled 28 Sep 2026 for a 4-person household with existing solar panels. Rules and prices
as of autumn 2026. 105 sources; see `99-bibliography.md`.*

## The field on one page

A home battery shifts midday solar into the evening. Its whole financial case is the gap
between what you pay for grid power (Swiss median **27.7 Rp/kWh** in 2026) and what you
get for exporting (since 2026 usually the **6 Rp floor** + up to ~3 Rp HKN in summer). Each
stored kWh is worth ~17-22 Rp [@elcom2026prices; @bfe2026refprice; @swissolar2026neu].
Installed prices fell to roughly **CHF 590-800 per kWh** (15 kWh for ~CHF 8,800 in 2025)
[@swissolar2026bm; @swissolar2025batt]. At realistic Swiss use (~250 cycles/yr), a 10 kWh battery at
CHF 7,500 saves ~CHF 450/yr, so payback is ~15-20 years, which is about the battery's life. With a subsidy,
tax deduction or a price under ~CHF 600/kWh, payback falls to 11-14 years (ch. 01, workbench model).

About half of new Swiss PV systems now get a battery [@swissolar2025batt; @rts2026batt]. Buyers mainly want
independence. Profit comes second [@swissolar2026bm]. Voices split along lenses: **industry**
(Swissolar, installers) says batteries are now often profitable, while **official and critical** voices (EnergieSchweiz,
Beobachter, Le News, a BFE system study) say rarely, or only in the right setup
[@energieschweiz-solarbatt; @beobachter2023; @lenews2026; @energeiaplus2026speicher]. **Scholarly** modelling (ETH) says it
depends on price. In 2026 we are near the break-even zone [@han2022techno].

**Main open questions:** will grid tariffs move from per-kWh to power/fixed charges, which would
hurt batteries, or toward dynamic pricing, which would help? Will V2H make stationary batteries redundant by ~2028?

## Bottom line for this household (confidence: medium)

1. **Cheap measures first:** load shifting, heat-pump boiler or boiler on surplus, EV charging on
   surplus (ch. 06).
2. **Buy a battery if** at least two of these apply: (a) your tariff is ≥ ~27 Rp and feed-in ≤ ~8 Rp;
   (b) you have or will get a heat pump or EV that is *not* already soaking up surplus; (c) you get a
   subsidy (e.g. SH, TG, NE, City of Zurich) and/or tax deduction; (d) backup power or independence has real value
   to you. Otherwise wait 1-2 years, since prices are falling ~25 %/yr [@swissolar2026bm].
3. **If you buy:** LFP, **5-8 kWh usable** (8-12 with heat pump/EV), matched to your inverter
   (AC-coupled if your inverter is healthy), SPI class A/B, good warranty, open EMS
   (ch. 03-05, 09). Get 2-3 quotes and apply for subsidies *before* ordering.

## Best sources by type

| Type | Pick | Why |
|---|---|---|
| Swiss market report | Swissolar *Batteriemonitor Schweiz 2026* [@swissolar2026bm]; *Batteriespeicher mit PV 2025* [@swissolar2025batt] | Current Swiss prices, brands, sizing rules (industry view) |
| Official data | BFE reference market prices [@bfe2026refprice]; ElCom 2026 tariffs [@elcom2026prices; @elcom-strompreise] | The two numbers that decide payback |
| Official guidance | EnergieSchweiz FAQ on solar batteries [@energieschweiz-solarbatt]; federal market study 2020 [@perchnielsen2020] | Neutral, sceptical baseline |
| Independent test | HTW Berlin *Stromspeicher-Inspektion 2026* [@htw2026inspektion] | Only lab-based efficiency comparison of whole systems |
| Paper | Han, Garrison & Hug 2022 (ETH) [@han2022techno]; Figgener et al. 2024 field ageing [@figgener2024multiyear] | Swiss profitability model; real-world degradation |
| Critical / system view | BFE storage study summary [@energeiaplus2026speicher]; Forrester et al. 2022 [@forrester2022grid] | Why home batteries may be less useful to the grid than claimed |
| Journalism | Beobachter [@beobachter2023]; Le News [@lenews2026]; RTS (FR) [@rts2026batt] | Consumer-side scepticism; Romandie subsidies |
| Book | Bucher, *Photovoltaikanlagen* (BFH, 2nd ed. 2025) [@bucher2021pv] | Swiss standard textbook incl. storage sizing |
| Handbook | *Solarstrom-Eigenverbrauch optimieren* [@eigenverbrauch-handbuch] | Order of self-consumption measures, 4-person example |
| Video | Akkudoktor on home storage economics [@akkudoktor2026] | Popular, numerate, critical (German context) |
| Course | Swissolar course *Batteriespeicher für PV-Anlagen* [@swissolar-kurs-batt] | Professional-level sizing and economics |
| Tools | EnergieSchweiz Solarrechner [@energieschweiz-solarrechner]; HTW Unabhängigkeitsrechner [@htw-unabh]; energiefranken.ch [@energiefranken] | Sizing and subsidy lookup |
| Community | Photovoltaikforum, Swiss subforum [@pvforum-ch-ekz]; Akkudoktor forum [@akkudoktor-forum] | Owner experience (not fetchable here) |
| Safety | Heureka (BE) summary of VKF rules [@heureka-aufstellen]; VKF FAQ [@vkf-faq-lfp] | Where you may place it |
| Audio/podcast | none found for Swiss home batteries | gap |

## Coverage

| Lens | Coverage | Notes |
|---|---|---|
| industry | strong (labelled) | Swissolar, utilities, installers, datasheets. Bias toward "buy". |
| official | strong | BFE, ElCom, EnergieSchweiz, VKF, tax offices, City of Zurich |
| scholarly | good | ETH, HTW, RWTH, LBNL, LCA papers |
| data | good | BFE prices, ElCom tariffs, calculators |
| popular | good | SRF, RTS, NZZ, Beobachter, Le News, Akkudoktor |
| critical | good | consumer press, BFE system study, recalls |
| practitioner | good | Swissolar handbooks/courses, Bucher, HEV, cantonal advice |
| cultural | thin | 3 FR + 2 IT sources; Romandie/Ticino subsidy details thin |
| community | thin | forums block fetching; Reddit unreachable |
| historical | thin (by design) | KEV history; topic is ~10 years old |

Fields: energy economics and electrical engineering dominate. Fire safety, tax law, LCA, power systems,
building services and mobility are each covered by 2-5 sources. Electrochemistry is covered only through field-ageing data.

**Gaps to close before acting:** your own tariff and feed-in terms; your canton's tax treatment;
current subsidy for your postcode; the exact Swiss single-phase unbalance rule of your utility;
installer quotes. See `workbench/open-questions.md`.
