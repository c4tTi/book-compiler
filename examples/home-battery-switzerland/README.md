# Home battery for a Swiss PV household: decision compendium

This folder helps you decide **whether** to add a battery to existing solar panels (4-person house,
Switzerland) and **which one**. It was compiled on 28 Sep 2026, and rules and prices are as of autumn 2026.

## What's here

| Path | Contents |
|---|---|
| `compendium/00-overview.md` | One-page answer, best sources, coverage. **Start here.** |
| `compendium/01-is-it-worth-it.md` | Economics: value per stored kWh, 2026 prices, payback, what each lens concludes |
| `compendium/02-swiss-rules-2026.md` | Feed-in 2026 (6 Rp floor, BFE reference prices), dynamic tariffs, LEG/vZEV, subsidies, tax |
| `compendium/03-sizing.md` | How many kWh for a 4-person house; tools |
| `compendium/04-technology.md` | LFP vs NMC, AC vs DC retrofit, HTW efficiency (SPI), ageing, warranties, Swiss grid rules |
| `compendium/05-products.md` | Brands on the Swiss market, test data, how to choose |
| `compendium/06-alternatives.md` | Load shifting, heat storage, EV/V2H, sharing with neighbours |
| `compendium/07-backup-power.md` | Emergency socket vs whole-house backup |
| `compendium/08-safety-installation.md` | VKF fire rules, recalls, installation checklist |
| `compendium/09-grid-and-dynamic-tariffs.md` | Dynamic tariffs, system critique, future-proofing |
| `compendium/10-environment.md` | Embodied CO2, recycling |
| `compendium/90-glossary.md`, `99-bibliography.md` | Terms; all 105 sources with status |
| `workbench/options-matrix.md` | Weighted options A-E with evidence, sensitivity and recommendation |
| `workbench/open-questions.md` | The 10 facts about *your* house that would change the answer, and a quote checklist |
| `workbench/battery_payback.py` | Payback / cost-per-stored-kWh model. Run with your own numbers |
| `workbench/options_matrix.py` | Recomputes the matrix with your own weights |
| `sources.jsonl`, `00-scope.md` | Source registry and scope/search log |

Examples:
```bash
python3 workbench/battery_payback.py                      # scenario table
python3 workbench/battery_payback.py --capex 8200 --usable 10 --cycles 240 --buy 0.31 --sell 0.075 --subsidy 1000 --tax-rate 0.25 --life 20
python3 workbench/options_matrix.py
```

## How it was compiled

- Scope: decision purpose. Facets: economics, Swiss rules, sizing, technology, products, alternatives,
  backup, safety, grid/dynamic tariffs, environment. Defaults (no questions asked): existing PV of
  unknown size, canton unknown (Zurich used as the worked example), heat pump/EV status unknown (both covered).
- Web search in DE/FR/IT/EN by facet, then catalogue searches (Crossref, Europe PMC, Open Library, Hacker News,
  Stack Exchange) via the topic-compiler helper, then a fields/lens sweep (tax, fire safety, LCA, critical
  press, community), then snowballing from the Swissolar reports and the federal market study.
- Key PDFs (Swissolar 2025 and 2026 reports, federal market study 2020, BFE reference prices, treeze LCA,
  Powerwall datasheet, self-consumption handbook) were downloaded and read in full text.

## Coverage and gaps

105 sources: 33 read, 69 confirmed, 3 unverified. 12 source types, 10/10 lenses, 12 fields, 4 languages
(DE 81, EN 19, FR 3, IT 2). Thin areas: community voices (forums block automated reading),
Romandie/Ticino detail, no Swiss podcast found, no Swiss consumer test of home batteries. Verify before acting:
cantonal tax deductibility of batteries, your utility's single-phase rules, current subsidy at your postcode, and
the treeze CO2 figure.

## How to extend

Ask for things like "add my smart-meter CSV and size the battery", "compare these three installer quotes",
"go deeper on V2H", or "update for 2027 tariffs". Put your own files (quotes, bills, load data) in `library/raw/`
(git-ignored) and run `python3 <skill>/scripts/compiler.py ingest <project>`.
