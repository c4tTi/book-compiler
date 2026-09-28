# Mokuhanga (Japanese Woodblock Printing): workshop compendium

A cited research compendium and teaching workbench for running a **weekend workshop on mokuhanga**: history, techniques, materials, tools, suppliers, safety, and how others teach it.

## What's here

| Path | Contents |
|---|---|
| `compendium/00-overview.md` | One-page map of the field, best sources by type, coverage table. **Start here** |
| `compendium/01-…09-*.md` | Chapters: history, people, materials, tools, technique, suppliers, safety, teaching, contemporary practice |
| `compendium/90-glossary.md` | ~45 Japanese terms with kanji |
| `compendium/99-bibliography.md` | Generated bibliography (189 sources) |
| `workbench/syllabus.md` | Draft two-day timetable, outcomes, prep checklist, risks and fallbacks |
| `workbench/reading-list.md` | Core / recommended / take-home / advanced |
| `workbench/supply-budget.md` + `budget.py` | Class budget computed from prices seen on supplier sites (edit and re-run) |
| `sources.jsonl` | Source registry: type, lens, field, language, reliability 1–5, status |
| `00-scope.md` | Scope, facets, fields, lenses, coverage notes, full search log |
| `library/` | Empty. Put your own PDFs/notes in `library/raw/` (git-ignored) |

## How it was compiled

- **Date:** 28 September 2026. **Scope defaults** (the user was unavailable): adult beginners, 8–12 participants, English-language focus with Japanese sources where possible, suppliers in US/UK/Japan. Western woodcut and linocut, art-market valuation and connoisseurship were excluded.
- **Method:** 51 web searches by facet, field and lens (including Japanese-language queries); 66 page fetches (about 17 blocked or unparseable) plus 11 OpenAlex abstract look-ups and local PDF text extraction; 11 catalogue runs through `compiler.py discover` (Open Library, Crossref, Europe PMC, Internet Archive, Hacker News, Stack Exchange); abstracts via Europe PMC and OpenAlex; `compiler.py verify` on the unverified sources.
- **Confidence flags in chapters:** ✅ well established · ⚠️ contested or weak · 🔎 verify before relying on it.
- **Status honesty:** `seen` = read this session (often a fetch summary or an abstract only, as noted); `confirmed` = existence checked (catalogue, DOI, the page's own title); `unverified` = second-hand only.

## Coverage and gaps

- **189 sources**: 59 read (31%), 129 confirmed, 1 unverified (Phillips 1926). 17 source types; all 10 lenses; 9 fields; 6 languages (en 171, ja 13, es 2, fr/pt/tr 1 each).
- **Thin:** the *critical* lens (no organized critique of Western mokuhanga found); community forums (Reddit/Facebook unreadable); art-education research (one 2026 paper + conference papers); Japanese books (catalogue records only).
- **Verify before teaching or publishing:**
  - Damp-pack timing and pigment:nori ratios are practitioner rules of thumb, not read in a source this session. Check them in Vollmer or McKenna and test your paper.
  - Supplier prices (seen 28 Sep 2026) change.
  - The name of the last professional hon-baren maker (sources differ: Gosho vs Goto).
  - The UNESCO washi listing (the page shows a 2025 extension to the 2014 inscription).
  - The year of the first International Mokuhanga Conference.
- Several sites blocked the fetcher (British Museum blog, Met, Smithsonian, Jackson's, Wiley, Nature). Their content is marked `confirmed` from search results, or read through a PDF download or an abstract API.

## How to extend

- "Go deeper on X" (e.g. bokashi, washi, sharpening): add sources with `compiler.py add`, update the chapter, re-run `bib` and `check`.
- **Add your own material:** drop PDFs into `library/raw/`, then `compiler.py ingest projects/mokuhanga` and `compiler.py search projects/mokuhanga "<term>"`.
- **Re-price:** edit `workbench/budget.py` (participants, prices) and run `python3 budget.py > supply-budget.md`.
- Helper: `python3 <skill>/scripts/compiler.py stats|check|bib projects/mokuhanga`.
