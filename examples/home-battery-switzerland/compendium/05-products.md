# 05 · Which one? Products on the Swiss market

## 5.1 Who sells what in Switzerland

Swissolar's 2025 member survey: **BYD and Huawei** lead by a wide margin. **Fronius** gained
strongly, and **Sigenergy** rose fast. Varta, E3/DC and Sonnen (DE) remain relevant. Swiss
maker **Modual** (AC-coupled, second-life EV cells) is in the top 10 [@swissolar2026bm; @srf2025batt; @modual].
Tesla Powerwall 3 and Enphase are also offered [@solarbatt-ch-vergleich]. The market is Chinese-dominated. The phase-out of
Chinese export VAT rebates may raise prices [@swissolar2026bm]. ⚠️

## 5.2 The main options for a retrofit

| System | Coupling / what it needs | Usable kWh | Independent efficiency data | Notes |
|---|---|---|---|---|
| **BYD Battery-Box Premium HVS/HVM** | DC to a compatible hybrid inverter (Fronius, SMA, Kostal, GoodWe, Sungrow...) | HVS 5.1-12.8; HVM 8.3-22.1 per tower | Kostal G3 + BYD HVS 12.8: SPI 95.1 % (DC), 94.3 % (AC); HTW 2026 test winner 10 kW AC class | Widest inverter compatibility; LFP; 10 y / 80 % with throughput cap [@byd-hvs-datasheet; @memodo-htw2026; @kostal2026htw] |
| **Huawei LUNA2000 S1** | Needs Huawei SUN2000 hybrid inverter | 6.9-20.7 per stack | not in HTW 2026 | Very common in CH; works well if you already have Huawei [@huawei-luna-specs; @swissolar2026bm] |
| **Fronius GEN24 Plus + Reserva** | Hybrid inverter (replaces yours) | 9.5 / 12.6 tested; other sizes 🔎 | SPI 95.3 % class A | Austrian; strong service network in CH [@fronius2026htw; @memodo-htw2026] |
| **SMA Sunny Boy Smart Energy + Home Storage** | Hybrid | 6.5 tested; other sizes 🔎 | 5 kW class: SPI 92.8 % (class A for size) | [@memodo-htw2026; @sma-hs-garantie] |
| **Sungrow SH + SBR** | Sungrow hybrid only | ~9.6 and up 🔎 | not in HTW 2026 | Cheaper; 10 y / 80 % (13,000 cycles claimed by third party) [@sungrow-sbr; @sungrow-vs-byd] |
| **Tesla Powerwall 3 / 3P** | All-in-one (inverter + battery) or AC-coupled to existing PV | 13.5 (+ expansions) | solar→battery→home 89 % (datasheet) | Whole-home backup with Gateway; single-phase version runs into CH unbalance rules, so use 3P; internet needed for warranty [@tesla-pw3-datasheet; @tesla-pw3p-datasheet] |
| **Fox ESS, RCT Power, SAX Power** | Hybrid / AC | various | SPI 97.0 %, 96.4 %, AC 5 kW winner | Test leaders, thinner Swiss installer base 🔎 [@htw2026inspektion; @memodo-htw2026] |
| **Modual (CH)** | AC-coupled, second-life cells | modular | none found | Local maker, ad claims < CHF 250/kWh 🔎 [@modual] |

## 5.3 How to choose (in this order)

1. **What inverter do you have, and how old is it?** This decides AC vs DC and
   limits your brand choice (Huawei → LUNA; Fronius GEN24 → Reserva or BYD; SMA → SMA
   or BYD; old string inverter → AC-coupled battery or replace with a hybrid) [@sungrow-vs-byd; @acspeicher-pvorg].
2. **Do you want full-house backup?** Then choose hybrid/all-in-one with backup switch (ch. 07).
3. **Efficiency and standby:** prefer SPI class A/B and low standby [@htw2026inspektion].
4. **Warranty terms:** retained capacity, throughput cap, labour costs [@memodo-htw2026].
5. **Installer and service quality in your region.** This matters more than the brand for a
   15-year device. Get 2-3 quotes with the same kWh and ask for SPI and warranty sheets.
6. **EMS compatibility** (Solar Manager or the inverter maker's EMS) if you want dynamic
   tariffs or heat pump/EV control [@solarmanager-dyn].

## 5.4 What the testers say

Stiftung Warentest (2026) relies on HTW's data and puts detailed results behind a paywall. Its
public text stresses that installation costs have not fallen as much as module prices [@stiftungwarentest2026].
No Swiss consumer magazine (K-Tipp, Kassensturz) test of home batteries was found. 🔎

## Purpose note

- **Essential:** §5.3 step 1. Your existing inverter narrows the choice more than anything else.
- **Shortlist to ask installers for (if you buy):** BYD HVS (if your inverter is compatible) ·
  your inverter maker's own battery · a Fronius/SMA/Kostal hybrid + battery if replacing an old
  inverter · Powerwall 3P only if whole-house backup is a priority.
