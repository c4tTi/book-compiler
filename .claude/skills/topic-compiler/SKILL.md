---
name: topic-compiler
description: Research any topic in depth and compile everything findable (books, papers, reviews, primary texts, websites, videos, podcasts, courses, tools, datasets, communities, experts and the user's own files) into one structured, cited compendium the user can build on, e.g. to write a book, prepare a course, make a decision or learn a field. Use this whenever the user asks to "compile", "gather everything on", "collect all resources/books/sources about", "build a knowledge base / reference / resource on", "research X thoroughly", "do a literature review", or wants material on a subject to write from, even if they don't say "compile". Not for compiling source code or build errors.
---

# Topic Compiler

Turn "gather everything about X" into a **project folder** with a cited,
organized compendium, a registry of every source found, and a workbench
geared to what the user will do with it.

The value is in three things the user can't easily do alone. Do them all:
1. **Breadth:** find sources across *all* types and angles, not the first ten
   search hits.
2. **Structure:** organize the field into a map (history, concepts, methods,
   evidence, debates...) instead of a pile of links.
3. **Trust:** every claim traceable to a source, every source rated, and a
   clear line between what was checked and what was not.

The bundled helper `scripts/compiler.py` (Python 3, standard library) does
the bookkeeping. Run it with `python3 <skill-dir>/scripts/compiler.py
<command> ...`. Run `--help` for all commands.

---

## Step 1: Scope (brief)

Work out from the request:
- **Topic** and its likely boundaries.
- **Purpose:** writing a book, teaching, a decision, learning, a product,
  general reference. This shapes the workbench (see
  `references/workbenches.md`) and what counts as relevant.
- **Audience, depth, languages, exclusions.**

Ask **at most one** short question, and only when the purpose is truly
unclear *and* would change the output. Otherwise pick sensible defaults, write
them down, and go. The user can redirect.

Create the project:
```bash
python3 scripts/compiler.py init projects/<topic-slug> --title "<Topic>" \
  --purpose "<purpose>" --request "<the user's words>"
```
Use `projects/` under the current repo or working directory unless the user
names another place. If a project for this topic already exists, **extend it**
rather than starting over: read its `00-scope.md` and `sources.jsonl` first.

## Step 2: Map the field (facets)

Before searching widely, write 6–12 **facets** into `00-scope.md`. These are the
angles a complete treatment needs. Start from the generic list and adapt it to
the topic:

origins & history · key people & schools · core concepts & vocabulary ·
methods / practices / how-to · evidence & research · applications & use
cases · debates & criticism · risks, safety & ethics · tools & resources ·
current state & trends · adjacent fields.

For each facet, note the questions it must answer. The facets become the
compendium chapters and the axes for checking coverage.

## Step 3: Gather (the main work)

Search broadly with every tool you have: web search, web fetch, scholarly
search, connectors (Google Drive, Notion, etc.) when the user points to them,
and files the user supplies. `references/source-hunting.md` has search
patterns and a checklist of **where to look for each source type**. Read it
at the start of this step.

How to do this well:
- **Run many queries.** Vary the wording, use the field's own jargon (which
  you learn as you go), search in the field's key languages, and search by
  source type ("<topic> systematic review", "<topic> podcast", "best books on
  <topic>", "<topic> site:reddit.com", "<topic> syllabus").
- **Snowball.** The best sources come from bibliographies, "further reading"
  lists, citations in reviews, awesome-lists, course syllabi and Wikipedia
  references. Follow them.
- **Parallelize** for big topics: when subagents are available, give each
  one a facet or source type. Have each return structured source entries
  (title, author, year, type, url, one-line value, reliability) plus key
  findings with the citations they came from.
- **Register every source as you find it:**
  ```bash
  python3 scripts/compiler.py add projects/<slug> --type paper \
    --title "..." --author "Surname, A. & Surname, B." --year 2020 \
    --url "https://..." --reliability 4 --status seen \
    --facets evidence,history --notes "RCT, n=120; strongest trial on X"
  ```
  The ID it prints (e.g. `kjaer2002`) is what you cite as `[@kjaer2002]`.
  It refuses duplicates, which keeps the registry clean over long sessions.
- **Rate reliability** from 1 to 5 using the rubric in
  `references/source-hunting.md`. Use `--status seen` only if you actually
  opened the source in this session. Sources recalled from memory are
  `unverified`. That distinction is what lets the user trust the result.
- **Log searches** in the search-log table of `00-scope.md`, so a later
  session can extend the work without repeating it.
- **Know when to stop.** Run `compiler.py stats` periodically. Keep going
  until every facet has solid sources, the major source types are covered
  (or are known not to exist), and new queries mostly return sources you
  already have. Say explicitly where coverage is thin.

**User's own files:** put them in `projects/<slug>/library/raw/`, then run
`compiler.py ingest` and `compiler.py search <term>`. Supported formats:
PDF (needs `pip install pypdf`), EPUB, HTML, TXT, MD, and SRT/VTT
transcripts. Results carry file and page/chapter, so they can be cited
precisely.

## Step 4: Compile

Write `compendium/` as numbered chapters, one per facet (merge or split
as needed): `01-<facet>.md`, `02-...`. Then add the glossary and the
bibliography.

Each chapter:
- **Synthesizes in your own words.** Compare sources, show where they agree
  or disagree, and cite with `[@id]` or `[@id1; @id2]`. Aim for synthesis,
  not source-by-source summaries.
- **Flags confidence:** ✅ well established · ⚠️ contested or weakly
  supported · 🔎 verify before relying on it (unverified source, uncertain
  detail, or recalled from memory).
- **Ends with a purpose note:** what is essential for the user's purpose,
  what is optional, what can be cut.

Also write:
- `compendium/00-overview.md`: the field on one page. Its shape, the
  5–10 must-know sources, and the main open questions.
- A **"Best sources by type"** section in the overview: top picks per type
  (books, papers, videos, podcasts, courses, tools, communities) with one
  line on why.
- `compendium/9x-glossary.md` when the field has its own vocabulary.

**Copyright:** summarize and link, don't reproduce. Short quotes are fine
when attributed; don't copy whole chapters, articles, transcripts or
paywalled text into the project. The user's own files stay in the
git-ignored `library/`.

Then generate the bibliography and check integrity:
```bash
python3 scripts/compiler.py bib projects/<slug>     # writes compendium/99-bibliography.md
python3 scripts/compiler.py check projects/<slug>   # duplicates, missing fields, dangling citations
```
Fix every problem `check` reports. Citing an ID that isn't registered is the
most common one.

## Step 5: Workbench and handoff

Create `workbench/` files for the user's purpose (templates in
`references/workbenches.md`). For example: a keep/cut log and outline for a
book, a syllabus for a course, an options matrix for a decision, a learning
path for self-study.

Write `projects/<slug>/README.md`: what's there, how it was compiled
(date, scope, main search strategies), coverage and known gaps, and how to
extend it.

If you're in a git repository, commit the project, following the repo's
branch and commit rules.

In the final reply, tell the user:
- How many sources were found, by type, and how many were actually opened
  vs. unverified.
- The 3–5 most important findings or sources.
- Where coverage is thin, and anything they should verify before publishing.
- What they can ask next ("go deeper on facet X", "add my PDFs", "draft
  chapter 1").

---

## Extending an existing project

For requests like "add more on X", "I added some PDFs", or "update this":
read the scope, run `stats`, register only new sources, update the chapters
they affect, then run `bib` and `check` again. Record new searches in the
search log. The goal is one growing, consistent resource per topic.
