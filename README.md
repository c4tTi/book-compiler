# Topic Compiler

Ask for any topic, and Claude gathers as many resources as it can find
(books, papers, reviews, primary texts, websites, videos, podcasts, courses,
tools, datasets, communities, experts and your own files) and compiles
them into one structured, cited resource you can build on.

It's a **Claude skill** (`topic-compiler`), so it can be reused for any
topic, in this repo or anywhere you install it.

## Using it

Just ask, in your own words:

> Compile everything about permaculture food forests. I want to teach a
> weekend workshop.

> Gather all the resources you can find on the history of tarot, for an article.

> Extend the yoga nidra compilation with audio recordings, trainings and communities.

Claude will:
1. **Scope** the topic and your purpose, and split it into facets
   (history, concepts, methods, evidence, debates, tools...).
2. **Gather** sources of every type, snowballing through bibliographies,
   reviews, syllabi and expert lists, and log each one with a reliability rating.
3. **Compile** a compendium in its own words: chapters per facet, citations,
   confidence flags (✅ ⚠️ 🔎), a one-page overview, best sources by type,
   glossary and a generated bibliography.
4. Set up a **workbench** for your purpose: book outline and keep/cut log,
   course syllabus, decision matrix, learning path...

## Layout

```
.claude/skills/topic-compiler/    The skill
  SKILL.md                          Workflow Claude follows
  references/source-hunting.md      Where to look per source type, reliability rubric
  references/workbenches.md         Templates per purpose (book, course, decision...)
  scripts/compiler.py               Project setup, source registry, bibliography, checks, file ingest

projects/<topic>/                 One folder per compiled topic
  00-scope.md                       Scope, facets, search log
  sources.jsonl                     Every source found, rated
  compendium/                       The compiled resource (+ 99-bibliography.md)
  workbench/                        Your working files for your purpose
  library/raw/                      Your own PDFs/EPUBs/notes (git-ignored)
```

Projects so far:
- [`projects/yoga-nidra`](projects/yoga-nidra/README.md): source base for a yoga nidra book

## Adding your own files to a project

```bash
cp ~/Books/*.pdf ~/Books/*.epub projects/<topic>/library/raw/
pip install pypdf     # only for PDFs
python3 .claude/skills/topic-compiler/scripts/compiler.py ingest projects/<topic>
python3 .claude/skills/topic-compiler/scripts/compiler.py search projects/<topic> "some term"
```
Then ask Claude to fold them into the compilation.

## Installing the skill elsewhere

- **Claude Code in this repo:** it works automatically (`.claude/skills/`).
- **Claude Code everywhere:** copy the skill folder to `~/.claude/skills/topic-compiler/`.
- **Claude.ai / the Claude app:** upload `dist/topic-compiler.skill` in the
  Skills section of your Claude settings. After changing the skill, ask
  Claude to repackage it.
