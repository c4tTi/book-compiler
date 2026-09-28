# Open questions: what would change the decision, and how to find out

| # | Question | Why it matters | How to find out |
|---|---|---|---|
| 1 | What is our all-in tariff (Rp/kWh) for 2026/2027? | Sets the value of every stored kWh (ch. 01) | Latest bill, or strompreis.elcom.admin.ch for your municipality [@elcom-strompreise] |
| 2 | What does our utility pay for feed-in (incl. HKN), per quarter? | The other half of the spread | Utility website / contract. The BFE reference price is the floor logic [@bfe2026refprice] |
| 3 | How big is our PV (kWp), how old and which brand/model of inverter? | Decides AC vs DC, compatible brands, whether to swap the inverter now (ch. 04-05) | Inverter label / installation documents |
| 4 | How much do we use between sunset and sunrise on summer days? | The most a battery can shift per day, so it caps useful size (ch. 03) | 15-min smart-meter data from utility portal |
| 5 | Heat pump? EV now or within 2-3 years? | Raises consumption; an EV may replace a battery (ch. 06) | Household plans |
| 6 | Which subsidies apply at our address, and must we apply before ordering? | Can cut CHF 1,000-3,000 (ch. 02) | energiefranken.ch; commune; utility [@energiefranken] |
| 7 | Is a battery tax-deductible in our canton for an existing building? | Worth ~25-30 % of cost (ch. 02) | Cantonal tax office. Sources disagree [@zh-steuer-energiespar; @solarguide-steuer] |
| 8 | Do we want backup power? Which circuits? | Rules out simple AC retrofits (ch. 07) | Family decision |
| 9 | Single-phase unbalance limit and connection rules of our utility | Affects product choice (Powerwall 3 vs 3P etc.) | Utility's technical connection conditions (TAB/WV) |
| 10 | Does our utility offer a dynamic tariff? | Adds value if the EMS can use it (ch. 09) | Utility; EKZ/Groupe E examples [@ekz2025dyn; @groupee-vario] |

## Checklist for comparing installer quotes

- Usable (not nominal) kWh; price per usable kWh incl. VAT, installation, EMS, metering.
- HTW SPI or at least standby consumption; AC or DC coupling; single or three phase.
- Warranty: years, retained capacity %, throughput cap, who pays labour, registration needs [@memodo-htw2026].
- Backup: none / socket / whole house; transfer time; black-start.
- EMS openness (Modbus/SunSpec, Solar Manager "active control") [@solarmanager-dyn].
- Placement per VKF rules (not in escape routes) [@heureka-aufstellen]; notification to utility; safety certificate.
- Simulated self-consumption and autarky **with and without** battery for your load profile.
