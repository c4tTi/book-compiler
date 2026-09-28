# Scope: Home battery storage for a Swiss PV household

- **Request:** we're thinking about adding a home battery to our solar panels (Switzerland, 4 person house). compile the resources so we can decide if its worth it and which one
- **Purpose:** decision: (1) is a battery worth it for us, (2) if yes, which size and product. Workbench = options matrix + payback model + open questions.
- **Audience:** the household (non-specialists, homeowners), so plain language, CHF figures, Swiss rules as of autumn 2026.
- **Depth:** decision-grade; enough to brief an installer and judge quotes. Not an engineering design.
- **Languages / regions:** Switzerland (DE main; FR, IT sources for Romandie/Ticino); German HTW Berlin test data because no Swiss lab test exists; a few international papers.
- **Defaults assumed (user was away, no questions asked):** existing PV of unknown size (typical Swiss EFH 8-12 kWp), house not yet known to have heat pump / EV (both scenarios covered), canton unknown (Zurich used as worked example for subsidies/tax), retrofit onto existing inverter (so AC- vs DC-coupling matters).
- **Out of scope:** off-grid systems, balcony/plug-in batteries, commercial storage, DIY battery building, seasonal storage.
- **Started:** 2026-09-28

This file is a working document: edit or rewrite any part of it freely.

## Facets

| Facet | Key questions | Chapter | Status |
|---|---|---|---|
| economics | Does it pay? Payback, cost per stored kWh, what drives it | 01 | done |
| swiss-rules | Feed-in 2026, minimum compensation, tariffs, subsidies, tax, LEG/vZEV | 02 | done |
| sizing | How many kWh for a 4-person house, with/without heat pump/EV | 03 | done |
| technology | LFP vs NMC, AC vs DC coupling, efficiency (SPI), degradation, warranties | 04 | done |
| products | Which brands in CH, test results, shortlist | 05 | done |
| alternatives | Cheaper ways to raise self-consumption; EV/V2H; thermal storage; LEG | 06 | done |
| backup | Emergency/backup power: what it takes and costs | 07 | done |
| safety | Fire rules (VKF), placement, recalls, installation | 08 | done |
| grid-flex | Dynamic tariffs, grid-serving operation, system view, future-proofing | 09 | done |
| environment | Embodied CO2, recycling, second-life | 10 | done |

## Fields

- energy economics (tariffs, payback, LCOE)
- electrical engineering / power electronics (inverters, coupling, efficiency)
- electrochemistry (cell chemistry, ageing)
- power systems / grid engineering (system value, flexibility)
- energy law & policy (StromVG/EnG 2026, subsidies)
- tax law (cantonal deductions)
- fire safety (VKF rules)
- building services (heat pumps, boilers, EMS)
- environmental science / LCA
- consumer protection
- mobility (bidirectional charging)

## Lenses

| Lens | What it means | Where to look for this topic | Covered |
|---|---|---|---|
| scholarly | academic research, reviews, university presses | ETH (Han et al.), HTW Berlin, RWTH field data, LBNL, LCA journals | yes |
| practitioner | people who do it: experts, teachers, professionals, makers | Swissolar courses/handbooks, Bucher textbook, cantonal energy advice (heureka), HEV | yes |
| historical | primary sources, archives, historical scholarship, classic texts | KEV history 2009-2014, HTW 2013/2018 classics, 2018 EnergieSchweiz guide | thin (topic is young; history matters only for why self-consumption rules exist) |
| cultural | regional, non-English, indigenous or tradition-specific perspectives | Romandie (RTS, installers), Ticino (IT), Swiss makers | yes (FR/IT thin) |
| critical | skeptics, critics, debunkers, ethical and safety critiques | Beobachter, Le News, Warentest, BFE system study, Akkudoktor, recalls | yes |
| official | government, regulators, standards bodies, professional associations | BFE, ElCom, EnergieSchweiz, VKF, cantonal tax offices, Stadt Zürich | yes |
| industry | companies, market reports, trade press, product documentation | Swissolar reports, utilities (EKZ, Groupe E), datasheets, installers | yes (over-represented, labelled) |
| community | forums, lived experience, user reviews, grassroots groups | Photovoltaikforum (CH subforum), Akkudoktor forum, VESE, HN, Stack Exchange | thin (forums block fetching; Reddit not reachable) |
| popular | journalism, popular books, podcasts, documentaries, influencers | SRF, RTS, NZZ, Beobachter, Akkudoktor video | yes; no Swiss podcast found |
| data | datasets, statistics, tools, calculators, software | BFE reference prices, ElCom tariffs, Solarrechner, HTW calculator, sonnendach | yes |

## Known gaps / notes for check warnings

- Only 2 decades of sources (2000s via one 2007 paper): home batteries only became a consumer product ~2013, and 2026 rules changed the economics, so recency is deliberate.
- Community lens thin: Photovoltaikforum and Reddit block fetching; entries are title-confirmed only.
- No podcast or audio found that addresses Swiss home batteries specifically.
- Tax deductibility of batteries is inconsistent between sources (see ch. 02); verify with your cantonal tax office.

## Search log

| Query / place searched | New sources | Notes |
|---|---|---|
| Batteriespeicher Einfamilienhaus Schweiz lohnt sich 2026 Rückliefertarif | 6 |  |
| Stromgesetz 2026 Mindestvergütung / EnergieSchweiz Faktenblatt / HTW Inspektion 2026 | 10 |  |
| Swiss PV battery profitability paper; ElCom 2026; Förderung Kanton; Kassensturz/Warentest | 9 |  |
| FR: batterie domestique Suisse rentable; VKF Brandschutz; dynamische Tarife; HTW Rechner | 12 |  |
| Notstrom; LFP vs NMC; bidirektional; Hersteller CH; AC vs DC | 7 |  |
| discover crossref/papers/hn/stackexchange/books (6 runs) | 13 | Europe PMC very noisy for this engineering topic; Open Library DE returned 0; Nature/Elsevier/SSRN 403 -> Crossref API abstracts |
| Referenzmarktpreis BFE; Steuerabzug; Akkudoktor; reddit (no results); Beobachter/K-Tipp; Ökobilanz; Ticino IT | 20 | Reddit not reachable via search; NZZ 402; BFE PDFs saved as binary -> extracted with pypdf |
| Products: Powerwall 3, BYD, Huawei, Sungrow/SMA/Fronius, Solar Manager; 3-phase unbalance CH | 10 | tesla.com 403; datasheets via energylibrary PDF |
| Thermal storage alternative; Swissolar course; Solarrechner; pvforum CH thread; Eigenverbrauch Handbuch | 9 |  |
| Recalls LG/Senec; podcasts (none found); HTW Inspektion history; Batteriemonitor 2026; BFE storage study; KEV history | 12 | No Swiss podcast episode on home batteries found |
