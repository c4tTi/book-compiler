# Urban beekeeping in Zurich (balcony/roof): compendium

A cited, structured guide for starting to keep honeybees on a balcony or roof in the city of Zurich: rules, site, equipment, bee health, courses, clubs, costs and alternatives. Compiled 2026-09-28.

## What's here

| Path | Contents |
|---|---|
| `compendium/00-overview.md` | **Start here.** Short answer, map of the field, best sources, coverage and gaps |
| `compendium/01–10-*.md` | Chapters: rules · urban ecology · site check · safety/neighbours/insurance · equipment & costs · bee year · bee health · honey & food law · courses/clubs/contacts · alternatives |
| `compendium/90-glossary.md` | German–English beekeeping terms |
| `compendium/99-bibliography.md` | All sources with type, reliability and status (generated) |
| `workbench/site-check.md` | Checklist for your balcony/roof |
| `workbench/options-matrix.md` | Balcony vs roof vs off-site vs no-own-bees, with a recommendation |
| `workbench/model.py` | Runnable cost model + weighted options matrix (`python3 workbench/model.py`) |
| `workbench/learning-path.md` | Stages and dated first steps from Oct 2026 |
| `workbench/open-questions.md` | What to ask your landlord, the city, the Veterinäramt, your insurer |
| `00-scope.md` | Scope, facets, fields, lenses, search log |
| `sources.jsonl` | Source registry (one JSON object per source) |
| `library/` | Empty; put your own PDFs in `library/raw/` (git-ignored) |

## How it was compiled

- **Scope:** city/canton of Zurich and Swiss federal law; beginner hobbyist; English output from mainly German sources. Defaults (user away): honeybees as the main topic, wild-bee alternatives included, user assumed to be a tenant.
- **Strategy:** web searches by facet (rules, city policy, site, health, courses, clubs, honey, equipment); catalogue searches with the topic-compiler helper (Europe PMC, Crossref, OpenAlex, Open Library, Internet Archive; Stack Exchange/HN gave nothing); a sweep for thin lenses (critical, cultural/French, historical, community, data); PDFs of official information sheets read in full with the helper's `pdf` command; abstracts read via `abstract --mark-read`.
- **Counts:** 102 sources; 62 read (web page, PDF text or abstract), 39 confirmed (exists, not read), 1 unverified. Languages: German 79, English 21, French 2. All 10 lenses covered.
- **Checks:** `compiler.py check` shows 0 problems and 0 warnings. Diversity exceptions (decades, languages, dominant official lens) are explained in `00-scope.md`.

## Coverage and gaps

Strong: official rules (canton, city, BGD), bee health, the wild-bee debate, courses in the city.
Thin or open: Zurich-city building/distance rules for hives inside the building zone; Swiss case law on bees on rented balconies; the current district bee inspector; Art. 700/719 ZGB text (not read); English-language courses (none found); prices of Varroa medicines and sugar (assumptions in the model); local urban honey contamination data. Prices and course dates are volatile (accessed 2026-09-28).

## Confidence markers

✅ well established · ⚠️ contested or weakly supported · 🔎 verify before relying on it.

## How to extend

- "Go deeper on X" (e.g. hive systems, swarm control, the WSL debate): add sources with `python3 <skill>/scripts/compiler.py add ...`, update the chapter, then run `bib` and `check`.
- Add your own files (course handouts, lease, Merkblätter) to `library/raw/`, then run `compiler.py ingest` and `compiler.py search <term>`.
- Re-run `workbench/model.py` with real quotes; update the options-matrix scores to your building.
- Check before acting: city FAQ (policy), Veterinäramt form (registration), course pages (dates/prices).
