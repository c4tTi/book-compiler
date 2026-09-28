# Silk Road c. 750: research compendium for a historical novel

Research base for a novel set on the route between Tang China and Samarkand around 750 AD. Compiled 2026-09-28 with the topic-compiler skill.

## What's here

| Path | Contents |
|---|---|
| `compendium/00-overview.md` | One-page map of the field, best sources by type, coverage and gaps. **Start here.** |
| `compendium/01`–`11` | Chapters: history, route/travel/maps, trade & money, daily life, religion, languages & names, peoples, war, primary sources, art & archaeology, writing the period. Each ends with a keep/optional/cut note for the novel |
| `compendium/90-glossary.md` | Terms (guosuo, sabao, hufu, jiedushi…) |
| `compendium/99-bibliography.md` | All 145 sources, generated from the registry, with reliability and read status |
| `workbench/keep-cut-log.md` | Topic-by-topic keep/brief/cut table for you to decide |
| `workbench/voice-and-positions.md` | Your positions on the historical debates, plus a "rules of the world" quick sheet |
| `workbench/book-outline.md` | A four-part scaffold (749–757) pointing into the compendium, and POV ideas |
| `workbench/travel.py` | Journey-time calculator (Chang'an → Samarkand). Edit the inputs and run `python3 travel.py` |
| `sources.jsonl` | The source registry (one JSON record per source) |
| `00-scope.md` | Scope, facets, fields, lenses, diversity exceptions and the full search log |
| `library/` | Put your own PDFs/EPUBs in `library/raw/` (git-ignored) |

## How it was compiled

- **Scope defaults** (the user was unavailable): purpose = writing a historical novel; window 700–790 centred on 747–757; northern route via Turfan and Kucha, with the southern route and Samarkand/Bukhara; English-first but with Chinese, French, Russian, Japanese and Persian material flagged.
- **Strategy:** 11 facets × 11 fields × 10 lenses. About 80 web searches by facet, field and lens (including queries in Chinese, Russian and French); catalogue runs on Crossref, Open Library, Internet Archive and History Stack Exchange (OpenAlex was rate-limited all session); snowballing from Wikipedia references and the Hansen/Skaff papers.
- **Reading:** 30 sources read in whole or in part, including the two Hansen papers on Turfan trade and money, Skaff's Sogdian diaspora paper, Rong Xinjiang's lecture on Sogdian colonies, and SPP 306 on Sogdian religion (all as PDFs); Wikipedia hub articles; and abstracts. 112 more are confirmed (catalogue or own page checked); 3 are unverified.
- **Blocked:** Encyclopaedia Iranica, UNESCO WHC, chiculture.org.hk and emco.hcommons.org returned 403, and the Wayback Machine was unreachable, so some key Iranica articles are confirmed but unread.

## Coverage and gaps

See `00-overview.md` → Coverage. Main gaps:
- food and medicine (thin);
- Uzbek/Tajik scholarship;
- Arabic geographers on Transoxiana routes;
- a scholarly figure for caravan speed;
- the Tang Liudian travel rates, which are secondary-reported only;
- the stage distances in `travel.py`, which are estimates.

## How to extend

- "Go deeper on X" (e.g. Samarkand in 750, Tang food, the Tibetan side): add sources with `compiler.py add`, update the chapter, then run `compiler.py bib` and `compiler.py check`.
- "Add my PDFs": put them in `library/raw/`, then run `compiler.py ingest` and `compiler.py search <term>`.
- Verify the ⚠️/🔎 items before publication; start with the Iranica articles and Heng's ward figures.
