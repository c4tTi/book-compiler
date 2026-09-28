#!/usr/bin/env python3
"""Rough payback / cost-per-stored-kWh model for a Swiss home battery.

Edit the SCENARIOS or pass your own numbers:
    python3 battery_payback.py --capex 7500 --usable 10 --cycles 250 --buy 0.30 --sell 0.07

All prices in CHF. Assumptions and their sources are in 01-is-it-worth-it.md.
The model is deliberately simple (no discounting by default, flat prices);
use it to see which inputs matter, not as a quote.
"""
import argparse


def model(capex, usable, cycles, buy, sell, rte=0.90, fade=0.025, life=15,
          subsidy=0.0, tax_rate=0.0, discount=0.0):
    """Return a dict of results.

    capex     installed price incl. VAT (CHF)
    usable    usable capacity (kWh)
    cycles    full-equivalent cycles per year actually used (CH: ~200-280)
    buy       marginal grid price you avoid (CHF/kWh, volumetric energy+grid+levies)
    sell      feed-in price you give up (CHF/kWh, incl. HKN)
    rte       round-trip efficiency (AC, incl. conversion; HTW SPI 89-97 %)
    fade      capacity loss per year (field data: 2-3 %-points/yr)
    life      years of use counted
    subsidy   one-off subsidy (CHF)
    tax_rate  marginal income-tax rate if deductible as energy-saving investment
    discount  real discount rate
    """
    net = capex - subsidy
    net -= net * tax_rate
    yearly, total_kwh, cum, payback = [], 0.0, 0.0, None
    for y in range(1, life + 1):
        cap = usable * max(0.0, 1 - fade * (y - 1))
        delivered = cap * cycles * rte          # kWh delivered to the house
        charged = cap * cycles                  # kWh of PV no longer fed in
        saving = delivered * buy - charged * sell
        disc = (1 + discount) ** y
        cum += saving / disc
        total_kwh += delivered
        yearly.append(saving)
        if payback is None and cum >= net:
            payback = y
    return {
        "net_invest": net,
        "saving_y1": yearly[0],
        "saving_total": sum(yearly),
        "npv": cum - net,
        "cost_per_stored_kwh": net / total_kwh if total_kwh else float("nan"),
        "payback_years": payback,
    }


SCENARIOS = [
    # name, capex, usable, cycles, buy, sell, subsidy, tax_rate
    ("Base: 10 kWh, CHF 7500, 250 cyc, 27.7/7 Rp", 7500, 10, 250, 0.277, 0.07, 0, 0.0),
    ("Base + tax deduction (25 %)", 7500, 10, 250, 0.277, 0.07, 0, 0.25),
    ("Base + Stadt ZH subsidy + tax", 7500, 10, 250, 0.277, 0.07, 2000, 0.25),
    ("Cheap: 10 kWh, CHF 5000 (~500/kWh)", 5000, 10, 250, 0.277, 0.07, 0, 0.0),
    ("Expensive: 10 kWh, CHF 10000", 10000, 10, 250, 0.277, 0.07, 0, 0.0),
    ("High tariff 35 Rp, sell 6 Rp", 7500, 10, 250, 0.35, 0.06, 0, 0.0),
    ("Low tariff 22 Rp, sell 9 Rp", 7500, 10, 250, 0.22, 0.09, 0, 0.0),
    ("Oversized: 15 kWh, CHF 8800, 180 cyc", 8800, 15, 180, 0.277, 0.07, 0, 0.0),
    ("Heat pump/EV house: 10 kWh, 300 cyc", 7500, 10, 300, 0.277, 0.07, 0, 0.0),
    ("Low use: 10 kWh, 180 cyc", 7500, 10, 180, 0.277, 0.07, 0, 0.0),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--capex", type=float)
    ap.add_argument("--usable", type=float, default=10)
    ap.add_argument("--cycles", type=float, default=250)
    ap.add_argument("--buy", type=float, default=0.277)
    ap.add_argument("--sell", type=float, default=0.07)
    ap.add_argument("--rte", type=float, default=0.90)
    ap.add_argument("--fade", type=float, default=0.025)
    ap.add_argument("--life", type=int, default=15)
    ap.add_argument("--subsidy", type=float, default=0)
    ap.add_argument("--tax-rate", type=float, default=0)
    ap.add_argument("--discount", type=float, default=0)
    a = ap.parse_args()
    rows = []
    if a.capex:
        rows.append(("Your numbers", model(a.capex, a.usable, a.cycles, a.buy, a.sell, a.rte, a.fade,
                                           a.life, a.subsidy, a.tax_rate, a.discount)))
    else:
        for name, capex, usable, cycles, buy, sell, sub, tax in SCENARIOS:
            rows.append((name, model(capex, usable, cycles, buy, sell, a.rte, a.fade, a.life, sub, tax, a.discount)))
    print(f"| Scenario | Net invest CHF | Saving yr 1 CHF | Saving {a.life} y CHF | NPV CHF | Cost/stored kWh Rp | Payback (y) |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for name, r in rows:
        pb = r["payback_years"] if r["payback_years"] else f">{a.life}"
        print(f"| {name} | {r['net_invest']:,.0f} | {r['saving_y1']:,.0f} | {r['saving_total']:,.0f} | "
              f"{r['npv']:,.0f} | {100*r['cost_per_stored_kwh']:.1f} | {pb} |")
    print(f"\nAssumptions: RTE {a.rte:.0%}, fade {a.fade:.1%}/yr, life {a.life} y, discount {a.discount:.0%}.")


if __name__ == "__main__":
    main()
