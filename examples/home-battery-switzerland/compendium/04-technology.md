# 04 · Technology choices that matter

## 4.1 Chemistry: LFP by default

- **LFP (lithium iron phosphate)** dominates home storage. It is cheaper, has longer cycle life and is
  much harder to ignite than NMC [@swissolar2025batt; @heureka-aufstellen]. ✅
- **NMC** (older LG RESU, some German systems) has higher energy density but higher fire risk
  and faster ageing at high state of charge and heat. Swiss fire rules treat it more strictly (ch. 08)
  [@heureka-aufstellen; @pvmag2022lg].
- Salt (sodium-nickel) and sodium-ion batteries exist but are niche for homes [@swissolar2026bm; @energieschweiz-solarbatt].

## 4.2 Retrofit: AC- or DC-coupled?

You already have PV, so this is the key design question.

| | AC-coupled battery (own battery inverter) | DC-coupled / hybrid inverter |
|---|---|---|
| Works with existing inverter? | Yes, any brand/age | Only if your inverter is a hybrid with a battery input, or you replace it |
| Efficiency | Extra conversion, ~4-8 % more loss | Best (HTW: DC Kostal+BYD 95.1 % vs AC 94.3 % SPI) |
| Cost | Lower if inverter is fine | Cheaper overall if the old inverter is near end-of-life anyway |
| Backup | Often only a single emergency socket | Full-house backup easier |

Sources: [@acspeicher-pvorg; @ac-dc-pvforum; @memodo-htw2026; @swissolar-netzausfall]. ✅ For a retrofit
onto a healthy inverter, AC coupling is the default. If your inverter is 8-12+ years old,
consider replacing it with a hybrid now and buying the battery with it.

## 4.3 Efficiency: look up the SPI, not just the round-trip figure

HTW Berlin's annual **Stromspeicher-Inspektion** rates whole systems with the
System Performance Index (SPI). 2026 range: **97.0 % (Fox ESS) down to 89.3 % (class G)**.
Standby draw ranges from 4 to 64 W, and a 64 W standby alone wastes ~560 kWh/yr. The difference between the best and worst
system is ~€200/yr [@htw2026inspektion; @memodo-htw2026]. The method has been refined since
2018 [@htw2018inspektion]. The full 2026 study PDF has per-system details [@htw2026pdf]. ⚠️ Only manufacturers who volunteer are tested. BYD and Huawei, the two biggest
Swiss brands, do not appear as stand-alone systems every year.

## 4.4 Ageing and warranties

- Field data from 21 German home storage systems over up to 8 years: **~2-3 %-points of
  capacity lost per year** [@figgener2024multiyear; @figgener2024briefing]. ✅ Plan on ~70-80 % after 10 years.
- Warranties are typically 10 years / 80 % remaining capacity. Some offer only 60 % (Tesla's retained-capacity figure was not confirmed in this session 🔎), and
  most cap energy throughput. Some cover only a replacement unit, not labour. Tesla
  requires a permanent internet connection for the full warranty [@memodo-htw2026; @tesla-pw3-datasheet; @byd-hvs-datasheet].
  HTW recommends checking six points: duration, registration, retained capacity, throughput cap,
  cost coverage and claim process [@memodo-htw2026].
- Expect 10-20 years of life [@energieschweiz-solarbatt]. ⚠️ Forum reports say adding modules is often only allowed within ~12 months of commissioning (cell-batch matching) [@pvforum-ch-ekz]. Buy the capacity you need at the start
  or pick a modular system that promises expansion.

## 4.5 Swiss grid connection details

- Switzerland limits single-phase unbalance to ~3.6-3.7 kVA. A single-phase battery
  inverter above that needs approval or a 3-phase alternative (e.g. Powerwall 3P for DACH).
  🔎 Check your utility's technical connection rules (TAB/WV) [@tesla-pw3p-datasheet].
- An EMS is needed for dynamic tariffs and for the Stadt Zürich subsidy. Solar Manager (Swiss) is
  the most-used third-party EMS [@swissolar2026bm; @solarmanager-dyn].

## Purpose note

- **Essential:** LFP, AC vs DC decision, SPI/standby, warranty fine print.
- **Optional:** chemistry alternatives.
