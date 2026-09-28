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
1. **Scope** the topic and your purpose, and map it on three axes:
   - **facets**: history, concepts, methods, evidence, debates, tools…
   - **fields**: every discipline that studies it (e.g. microbiology, food
     history and law for sourdough)
   - **lenses**: ten kinds of voice (scholarly, practitioner, historical,
     cultural and non-English, critical, official, industry, community,
     popular, data)
2. **Gather** in rounds:
   - web search;
   - direct catalogue searches (Open Library, Europe PMC, Crossref,
     OpenAlex, Internet Archive, Hacker News, Stack Exchange);
   - a sweep of any thin fields and lenses;
   - snowballing from bibliographies.
3. **Log and verify** every source: type, rating, lens, field, language.
   Sources are automatically checked against catalogues, and each is marked as
   read, confirmed or unverified.
4. **Compile** a compendium in its own words: chapters per facet, citations,
   confidence flags (✅ ⚠️ 🔎), an overview with the best sources by type and a
   coverage table, a glossary and a generated bibliography.
5. Set up a **workbench** for your purpose: a book outline and keep/cut log, a
   course syllabus and supply list, a decision matrix with a runnable cost
   model, or a learning path.

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

Examples from the test runs (each compiled by the skill from one sentence):
- [`examples/sourdough-baking`](examples/sourdough-baking/README.md): beginner's book, 156 sources, 4 languages
- [`examples/home-battery-switzerland`](examples/home-battery-switzerland/README.md): buying decision with a payback model
- [`examples/mokuhanga`](examples/mokuhanga/README.md): weekend workshop on Japanese woodblock printing, syllabus and budget
- [`examples/silk-road-750`](examples/silk-road-750/README.md): research bible for a historical novel, 6 languages
- [`examples/urban-beekeeping-zurich`](examples/urban-beekeeping-zurich/README.md): Zurich rules, courses, costs, learning path

Test scores per skill version are in [`evals/topic-compiler/RESULTS.md`](evals/topic-compiler/RESULTS.md).

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
