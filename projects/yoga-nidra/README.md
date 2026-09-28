# Yoga Nidra: Compiled Resource

The source base for writing my own yoga nidra book. It covers the history,
the major books, concepts, practice structures, techniques, research,
safety and the debates in the field.

| | |
|---|---|
| `00-scope.md` | Scope, facets, search log |
| `sources.jsonl` | Registry of every source (cited in the text as `[@id]`) |
| `compendium/` | The compiled resource, chapters 01–10, plus `99-bibliography.md` (generated). Chapter 10 covers recordings, apps, video, trainings, podcasts and communities |
| `workbench/` | Book writing: keep/cut log, positions, outline |
| `library/` | Your own copies of books go in `library/raw/` (git-ignored) |

**Status and gaps**
- The first compilation was written largely from background knowledge. Sources
  marked *unverified* in the bibliography have not been opened yet, so check
  them before quoting. The research-paper details are being verified separately.
- **Extended 2026-09-28** with audio recordings, video, trainings/courses,
  apps, podcasts, teachers and communities (`compendium/10-...`), plus seven
  more books and four history sources in `02` (notably Boyes 1973, which
  predates Satyananda, and Singleton 2005 on Western relaxation roots).
  23 of the 49 new sources were opened on their own pages in this session;
  the other 26 are marked unverified.
- Gaps: YouTube, Reddit, app-store and some training pages (Kripalu,
  Himalayan Institute, Yoga International) could not be opened from the
  compiling environment. Follower counts, prices and hours in chapter 10 are
  a September 2026 snapshot. No documentary film on yoga nidra was found.
  Non-English media (e.g., French, German, Scandinavian schools) are barely
  covered.
- Worth checking: which recording the Copenhagen PET studies used (`10` §10.2)
  and the date of Nirlipta Tuli's death given on the Yoga Nidrā Network site.

**Adding your own books**
```bash
cp ~/Books/*.pdf projects/yoga-nidra/library/raw/
python3 .claude/skills/topic-compiler/scripts/compiler.py ingest projects/yoga-nidra
python3 .claude/skills/topic-compiler/scripts/compiler.py search projects/yoga-nidra sankalpa
```
