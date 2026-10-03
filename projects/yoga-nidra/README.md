# Yoga Nidra: Compiled Resource

The source base for writing my own yoga nidra book. It covers the history,
the major books, concepts, practice structures, techniques, research,
safety and the debates in the field, drawing on yoga books and on
religious studies, history of modern yoga, neuroscience, sleep medicine,
clinical psychology, nursing, hypnosis research, anthropology, official
bodies, industry and trial registries, in English, German, French and Hindi.

| | |
|---|---|
| `00-scope.md` | Scope, facets, fields, lenses, search log |
| `sources.jsonl` | Registry of every source (cited in the text as `[@id]`) |
| `compendium/` | `00-overview.md` (the field on one page, best sources, coverage), chapters 01–11, `90-glossary.md`, `99-bibliography.md` (generated). Chapter 10 covers recordings, apps, video, trainings, podcasts and communities; chapter 11 covers German, French and Hindi sources, institutions and markets |
| `reading/` | Personal reading summaries of 64 yoga nidra books; start with `reading/00-index.md` |
| `workbench/` | Book writing: keep/cut log, positions, outline |
| `library/` | Your own copies of books go in `library/raw/` (git-ignored) |

**Status and gaps** (updated 2026-09-28, extension 2)
- **158 sources**: 81 read (`seen`; many papers from abstracts only), 68
  confirmed, 9 unverified. All ten lenses covered; 16 fields; languages en
  137, de 9, hi 6, fr 5, es 1. `compiler.py check`: 0 problems, 0 warnings.
- **Extension 2 (2026-09-28): "sources from all areas, not just yoga
  books."** Tagged all older sources with lens/field/language; added 83
  sources: the 2025–26 meta-analyses and trials, fMRI/EEG work, meditation
  adverse-event research, Indology (Nidrā-Kālarātri), history of modern
  yoga and anthropology, free primary-text translations (Pargiter, Pancham
  Sinh, Nikhilananda), the Western relaxation classics, NIH/VA/AYUSH and the
  Royal Commission, app-market material, trial registries, and German,
  French and Hindi sources. Woven into `01`, `02` §F, `03`, `06`, `07`,
  `08`, `10`, new `11`, and summarised in `00-overview.md`. The glossary is
  now `90-glossary.md`.
- The first compilation was written largely from background knowledge.
  Sources marked *unverified* in the bibliography have not been checked, so
  check them before quoting.
- **Extended 2026-09-28 (extension 1)** with audio recordings, video,
  trainings/courses, apps, podcasts, teachers and communities (`10`), plus
  seven more books and four history sources in `02`.
- **Gaps:** the Royal Commission's findings report could not be opened (site
  down), so its findings are quoted second-hand; Satyananda's 1964 talk is
  known only second-hand; most German/French books are confirmed from
  publisher pages, not read; no ethnography of yoga nidra classes exists in
  the registry; Scandinavian, Spanish and Italian material is thin;
  YouTube, Reddit, app-store and some training pages (Kripalu, Himalayan
  Institute, Yoga International) could not be opened. Follower counts,
  prices and market figures are September 2026 snapshots. No documentary
  film on yoga nidra was found.
- **Worth checking before publishing:** Royal Commission report release
  date (April vs. September 2016) and wording; which recording the
  Copenhagen PET studies used (`10` §10.2); the date of Nirlipta Tuli's
  death given on the Yoga Nidrā Network site; exact verse numbers of
  medieval yoganidrā passages.

**Adding your own books**
```bash
cp ~/Books/*.pdf projects/yoga-nidra/library/raw/
python3 .claude/skills/topic-compiler/scripts/compiler.py ingest projects/yoga-nidra
python3 .claude/skills/topic-compiler/scripts/compiler.py search projects/yoga-nidra sankalpa
```
