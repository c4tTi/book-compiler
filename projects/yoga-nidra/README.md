# Yoga Nidra: Compiled Resource

The source base for writing my own yoga nidra book. It covers the history,
the major books, concepts, practice structures, techniques, research,
safety and the debates in the field.

| | |
|---|---|
| `00-scope.md` | Scope, facets, search log |
| `sources.jsonl` | Registry of every source (cited in the text as `[@id]`) |
| `compendium/` | The compiled resource, chapters 01–09, plus `99-bibliography.md` (generated) |
| `workbench/` | Book writing: keep/cut log, positions, outline |
| `library/` | Your own copies of books go in `library/raw/` (git-ignored) |

**Status and gaps**
- The first compilation was written largely from background knowledge. Sources
  marked *unverified* in the bibliography have not been opened yet, so check
  them before quoting.
- Not yet covered: audio recordings, video, trainings/courses, online
  communities. Ask Claude: "extend the yoga nidra compilation with audio,
  video, courses and communities".

**Adding your own books**
```bash
cp ~/Books/*.pdf projects/yoga-nidra/library/raw/
python3 .claude/skills/topic-compiler/scripts/compiler.py ingest projects/yoga-nidra
python3 .claude/skills/topic-compiler/scripts/compiler.py search projects/yoga-nidra sankalpa
```
