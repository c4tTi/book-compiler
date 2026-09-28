# 5. Equipment, bees and costs

## 5.1 Hive systems used in Switzerland

| System | How it works | Fit for balcony/roof | Notes |
|---|---|---|---|
| **Schweizerkasten** (Swiss box, Bürki-Jeker type) | Rear-access boxes, traditionally stacked inside a **bee house** (8–20 colonies) | ✗ Poor: built for bee houses, not for outdoor stands | 50–80% of Swiss colonies [@wikiimkereich; @hlsbienen]; heavier and pricier, and you must pull every comb in front to reach the back [@bienenlandmagazin] |
| **Dadant Blatt magazine** | Top-access boxes; large brood box + shallower honey supers | ✓ Good: standard outdoor magazine | Widespread from Romandie across CH [@bienenlandmagazin]; many Swiss colony sellers sell on Dadant frames [@apimat] |
| **Swiss-frame magazine** | Top-access magazine using Swiss frames | ✓ | Swiss frames' short lugs and nailing are not ideal for magazines [@bienenlandmagazin] |
| **Zander / Deutsch Normal / Mini-Plus / half-size Dadant** | German magazine sizes; Mini-Plus is very small | ✓ compact, but ⚠️ less common in CH | A German blog recommends compact hives for balconies [@bienenquellebalkon] 🔎 |
| **BienenBox / single-box and "natural" hives** (Warré, top-bar, Klotzbeute) | Natural comb, less intervention, smaller harvest | ✓ (BienenBox used in the Stadtbienen course) | FreeTheBees argues housing should follow the bees' needs, not keeper comfort [@freethebees; @stadtbienenkurs] |

**Recommendation for a Zurich beginner:** use the **hive system your course and club use** (often Dadant Blatt magazine in current Swiss courses 🔎: confirm with your course). You will buy colonies, frames and help locally, and mixing frame sizes is a classic beginner's mistake (inference from the sources above) ⚠️. The Swiss textbook covers all mainstream systems [@bienenbuch].

## 5.2 What you need (first colony)

The Zürcher Bienenfreunde list [@zbfwerden]:
- **Personal gear** (bee suit or jacket with veil, gloves): CHF 80–150.
- **Hive-care tools** (smoker, hive tool, bee brush, feeder, Varroa diagnostic tray, etc.): ~CHF 200.
- **New hive with accessories** (floor with Varroa screen, brood box, honey super(s), queen excluder, lid, frames, foundation): ~CHF 500.
- **A colony**: ~CHF 150.

⚠️ The club states the total as CHF 430–650, but the items above add up to **CHF 930–1000**. Budget with the item list.

Also plan for: a **water drinker**, **Varroa medicines** and dispensers (formic acid: Liebig or Nassenheider dispensers are BGD-recommended; oxalic acid for winter) [@merkblaetterverz], **sugar/feed**, protective goggles and acid gloves, a lockable box for medicines, and a hive scale or strap to secure the hive against wind (roof).

**Extraction equipment** (extractor, uncapping tools, strainers, jars) is usually **borrowed or rented from the club**. The Zürcher Bienenfreunde teaching apiary has an extraction room [@zbfkurse] 🔎 (ask about rental).

## 5.3 Where to buy

- **Bienen Meier AG** (Künten AG), the largest Swiss beekeeping supplier, online shop [@bienenmeier].
- **BienenSchweiz marketplace** for colonies, queens and used equipment [@bsmarktplatz]. ⚠️ Buy **used equipment** only from known, healthy apiaries (foulbrood spores survive on wood and wax; small-hive-beetle risk from imports) [@blvbeutenkaefer; @bsfaulbrut].
- **The Swiss textbook** (*Das Schweizerische Bienenbuch*, 5 vols.) from the BienenSchweiz shop; it is included in the club course fee [@bienenbuch; @zbfkurse].

## 5.4 Getting bees

- **Summer young colony (Jungvolk)** on 6 Dadant frames: from end of June, e.g. CHF 250. **Overwintered young colony**: from April, e.g. CHF 350. Queens: CHF 50 (F1) to CHF 80 (A-station mated) [@apimat] (prices seen 2026-09-28; out of stock at the time).
- Marketplace ads list young colonies from **CHF 85–250** [@bsmarktplatz].
- **Race:** most Swiss colonies are **Carnica** or **Buckfast**. The native **dark bee (Apis mellifera mellifera)** is protected in Glarus and Melchtal and is bred by mellifera.ch [@mellifera]. Zurich city is not a protected area 🔎. For a balcony, **gentleness and low swarming tendency** matter more than race. Ask the club for calm local stock.
- **Health check:** buy from a registered Swiss beekeeper outside restricted zones [@vetazhseuchen]. Ask about the Varroa treatment history.
- **Timing:** the realistic moment for a beginner is **after year 1 of the course**. The club course lets you "build your own apiary in year 2 with the club's support" [@zbfkurse].

## 5.5 Costs (from `workbench/model.py`)

Computed with the item list above, course prices and colony prices (all sources in the script):

| Scenario | Start-up (CHF) | Running (CHF/yr, from yr 2) |
|---|---|---|
| 1 colony, club Grundkurs, colony CHF 150–350 | 1,915–2,115 | ~200 |
| 2 colonies, club Grundkurs | 2,565–2,965 | ~270 |
| 1 colony, Stadtbienen course (EUR 560) | 1,490–1,690 | ~200 |
| First 3 years total, 1 / 2 colonies (club course) | 2,415 / 3,305 | — |

Running costs = Bienen-Zeitung CHF 80 + club CHF 50 [@zbfkurse] + per-colony medicines and sugar (**assumptions**, not sourced: CHF 30 + CHF 40). Honey income is excluded (the Swiss average yield is ~11 kg/colony [@wikiimkereich], and selling brings food-law duties, chapter 8).

**Time:** rule of thumb **~10 h per colony per year**. Beginners should plan **about 1 hour per colony per week in spring and summer**, with inspections every 7–9 days in swarm season, and much less in winter 🔎 (German club sources) [@aumeierzeit]. Add course time: 18 half-days over two years [@bsimkerwerden].

## Purpose note

- **Essential:** 5.1 recommendation (match your course), 5.2 checklist, 5.4 timing.
- **Decision-relevant:** 5.5 budget. Run `python3 workbench/model.py` with your own quotes.
- **Optional:** alternative/natural hive systems, unless the ecological course appeals to you.
