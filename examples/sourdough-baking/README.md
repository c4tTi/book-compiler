# Sourdough Bread Baking: research compendium

Source material for writing a **beginner's guide book on sourdough bread baking**. Compiled 2026-09-28 with the `topic-compiler` skill.

## What's here
| Path | Contents |
|---|---|
| `00-scope.md` | Scope, defaults chosen (the user was away), facets, fields, lenses, coverage notes, full search log |
| `sources.jsonl` | Registry of 156 sources (type, reliability 1–5, status, facets, lens, field, language, notes) |
| `compendium/00-overview.md` | The field on one page, main debates, best sources by type, coverage & gaps |
| `compendium/01–14` | One chapter per facet, cited `[@id]`, with confidence flags (✅ ⚠️ 🔎) and a purpose note |
| `compendium/90-glossary.md` | Terms |
| `compendium/99-bibliography.md` | Generated bibliography |
| `workbench/keep-cut-log.md` | Topic-by-topic KEEP/BRIEF/CUT suggestions for your decisions |
| `workbench/voice-and-positions.md` | Audience, promise, positions to take on 8 debates |
| `workbench/book-outline.md` | Draft 5-part outline mapped to compendium sections |
| `library/` | Empty. Put your own PDFs/EPUBs in `library/raw/` (git-ignored) |

## How it was compiled
- **Defaults assumed:** complete-beginner home bakers; English-language book; practice first, with the science behind the "why".
- **Strategies:** web search by facet (51 queries); page reading (40 fetch attempts, 35 successful); catalogue searches with `compiler.py discover` (Open Library incl. German/French/Italian, Europe PMC, Crossref, Internet Archive, Stack Exchange Seasoned Advice, Hacker News); snowballing from Wikipedia references and review author lists; abstract reading via Europe PMC.
- **Statuses:** 47 read (page or abstract), 108 confirmed (catalogue record or own page seen in results), 1 unverified.
- **Blocked:** Reddit, Atlas Obscura, Beyond Celiac, PeerJ (403); the German Leitsätze PDF (503); the Dunn lab page (JS-rendered). Details are in the search log.

## Coverage and gaps
All 10 lenses, 11 fields, 20 source types and 4 languages are covered, and `check` reports no warnings. Gaps:
- The core practitioner books (Forkish, Robertson, Leo, Hamelman) were confirmed through publisher pages, not read. Treat quoted parameters as that author's view and test them.
- Non-English literature is catalogue-only. There's no sensory or flavour science, no sustainability angle, and no UK/EU flour-type conversion table.
- Items marked 🔎 in chapters need checking before publication (e.g. Boudin 1906 earthquake story, "Serratia" pink-streak claim, current bacterial names).

## How to extend
```bash
C="python3 .claude/skills/topic-compiler/scripts/compiler.py"
C stats <this folder>                       # what's thin
C discover <this folder> "rye sourdough" --catalogues books,papers --out cand.jsonl
C add <this folder> --from-jsonl cand.jsonl
C ingest <this folder>                      # after adding your own files to library/raw/
C bib <this folder> && C check <this folder>
```
Ask for things like: "go deeper on rye", "read the Forkish and Leo books properly", "add my PDFs", "draft chapter 4 (making a starter)".
