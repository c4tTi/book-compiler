---
name: topic-compiler
description: Research any topic in depth and compile everything findable (books, papers, reviews, primary texts, archives, websites, videos, audio, podcasts, courses, apps, tools, datasets, communities, experts and the user's own files), drawn from many disciplines, perspectives and languages, into one structured, cited compendium the user can build on, e.g. to write a book, prepare a course, make a decision or learn a field. Use this whenever the user asks to "compile", "gather everything on", "collect all resources/books/sources about", "build a knowledge base / reference / resource on", "research X thoroughly", "do a literature review", or wants material on a subject to write from, even if they don't say "compile". Not for compiling source code or build errors.
---

# Topic Compiler

Turn "gather everything about X" into a **project folder** with a cited,
organized compendium, a registry of every source found, and a workbench
geared to what the user will do with it.

The value is in three things the user can't easily do alone. Do them all:
1. **Breadth across areas:** sources from every discipline that studies the
   topic, every kind of voice (scholars, practitioners, critics, officials,
   industry, communities, historical and non-English traditions) and every
   medium. Not the first ten search hits, which mostly repeat one popular
   viewpoint.
2. **Structure:** a map of the field (history, concepts, methods, evidence,
   debates...) instead of a pile of links.
3. **Trust:** every claim traceable to a source, every source rated, and an
   honest record of what was actually read versus only confirmed to exist.

The helper `scripts/compiler.py` (Python 3, standard library) does the
bookkeeping, catalogue searches and verification. Run it as `python3
<skill-dir>/scripts/compiler.py <command> ...`; `--help` lists all commands.
Below, `C` stands for that invocation.

---

## Step 1: Scope (brief)

Work out from the request:
- **Topic** and its likely boundaries.
- **Purpose:** book, course, decision, learning, product, general
  reference. This shapes the workbench (`references/workbenches.md`) and
  what counts as relevant.
- **Audience, depth, languages, exclusions.**

Ask **at most one** short question, and only when the purpose is truly
unclear *and* would change the output. Otherwise pick sensible defaults, write
them down, and go. The user can redirect.

```bash
C init projects/<topic-slug> --title "<Topic>" --purpose "<purpose>" --request "<the user's words>"
```
Use `projects/` under the current repo or working directory unless the user
names another place. If the project already exists, go to **Extending an
existing project** below.

## Step 2: Map the field on three axes

Fill in `00-scope.md` (a working document; rewrite it freely):

1. **Facets:** 6–12 angles a complete treatment needs. These become
   chapters. Generic starting list: origins & history · key people &
   schools · core concepts · methods / practice · evidence & research ·
   applications · debates & criticism · risks, safety & ethics · tools &
   resources · current state & trends · adjacent fields.
2. **Fields:** list the disciplines and domains that have something to say
   about the topic. Think wider than the obvious. For sourdough, that means
   microbiology, food chemistry, nutrition, gastroenterology, food history,
   anthropology, economics of bakeries, and craft/culinary practice. For a
   meditation practice, it means neuroscience, clinical psychology, religious
   studies and philology, history, sleep medicine, and trauma therapy. Each
   field is a separate search territory with its own vocabulary and venues.
3. **Lenses:** for each of the ten lenses (scholarly, practitioner,
   historical, cultural, critical, official, industry, community, popular,
   data), fill in the "Where to look for this topic" column of the table
   `init` creates. `references/source-hunting.md` §1 has ideas.

Write fields as bullets under `## Fields` (e.g. `- microbiology: starter
ecology, lactic acid bacteria`). `check` matches each source's `--field`
tags against these lines and warns about fields with fewer than 3 sources.

These three axes are how you'll check coverage. A compilation with 100 sources
that all come from blogs and popular books has breadth in count only.

## Step 3: Gather in rounds

Read `references/source-hunting.md` at the start of this step. It has search
patterns, the catalogue list, fallbacks for blocked sites and the reliability
rubric.

Work in rounds. Run `C stats` after each round and aim the next round at
what it shows is missing.

- **Round 1, web search by facet.** Several queries per facet. Pick up the
  field's jargon, key names and classic works as you go, and feed them into
  later queries.
- **Round 2, catalogues.** `C discover <project> "<query>" --catalogues
  <list> --out candidates.jsonl` searches open catalogues directly. They
  surface academic work, old and out-of-print texts, recordings and community
  discussion that web search buries. Pick catalogues by topic:
  - `openalex` and `crossref` cover every discipline (humanities and
    engineering too);
  - `papers` (Europe PMC) covers life sciences, medicine and psychology;
  - `books` (Open Library) covers books in all languages;
  - `archive` (Internet Archive) has old texts, audio and film;
  - `hn` and `stackexchange --se-site <site>` are communities.

  Tips:
  - Use the field's own terms.
  - Add `--sort cited` to find the classics.
  - Add `--lang` for non-English literatures. Open Library covers some
    languages thinly, so also search the web in that language.

  Candidates are raw and noisy and get numbered `c1, c2, …`. Pick the
  relevant ones and add them with shared tags:
  `C add <project> --from-jsonl candidates.jsonl --pick c2,c5,c9 --lens
  scholarly --field microbiology --facets science --reliability 4`.
- **Round 3, fields and lenses sweep.** For every field in the scope that
  has fewer than ~3 sources, and every lens `stats` reports as missing or
  thin, run targeted searches (patterns in `source-hunting.md` §1–2). This
  round is what makes the compilation draw from all areas instead of the most
  visible one. If a lens truly doesn't exist for the topic (e.g. no official
  bodies regulate it), say so in the scope rather than forcing it.
- **Round 4, snowball.** Follow the bibliographies of the best reviews and
  books, "further reading" lists, syllabi, Wikipedia references and awesome-
  lists. Search the names of the 5–10 key people.

**Parallelize** broad topics when you have a subagent tool (you may not, for
example when you are yourself a subagent): give each one a
field or a lens (not only a facet, since facet-split agents all find the
same popular sources). Each should return candidate sources as JSONL lines
in the registry format, plus key findings with their citations.

**Register sources** as you go, or batch them:
```bash
C add <project> --type paper --title "..." --author "Surname, A. & Surname, B." --year 2020 \
  --url "https://..." --reliability 4 --status seen --facets evidence \
  --lens scholarly --field microbiology --lang en --notes "RCT, n=120; via Smith 2021 review"
C add <project> --from-jsonl batch.jsonl          # one JSON object per line, same keys
```
- Set `--lens`, `--field` and `--lang` on every source. `stats` and
  `check` use them to show which areas are covered.
- The URL is the source's **own** page (DOI, catalogue record, product page,
  episode page). Where you found it goes in `--notes` ("via ..."). Two books
  found on one list page therefore get two different URLs.
- `--license` marks reusable material (CC BY, public domain). Authors care.
  `--accessed` dates volatile facts such as prices and availability.
- Never register or link pirated copies (Z-Library, LibGen and similar
  uploads). `discover` filters the known ones out.
- Use the helper instead of editing `sources.jsonl` by hand:
  - `C update <id>` fixes fields (`--facets +x` appends, `-x` removes).
  - `C rename` changes an ID and rewrites its citations.
  - `C delete` removes sources.
  - `C log` appends to the search log; `--from-tsv` takes many rows at once.

**Status** is what makes the compilation trustworthy, so set it honestly:
- `seen`: you read the source's own content in this session: the page
  itself via fetch (a fetch tool's summary counts, so note it if you only had
  a summary), the full text, or the abstract via `C abstract <id>
  --mark-read` (which notes "abstract only").
- `confirmed`: existence and details checked (catalogue or DOI record, the
  item's own page title in results, a publisher or product page for a book,
  `C verify`) but the content wasn't read.
- `unverified`: from memory, or only mentioned second-hand (a list, a
  citation in another work).

**Verify before you write.**
1. Run `C verify <project>`. It checks unverified sources against Crossref,
   Open Library, YouTube and the URL itself, and fills in missing authors,
   years, DOIs and publishers.
2. Read every source that carries a load-bearing claim or appears in "best
   sources":
   - fetch the page;
   - for papers whose publisher blocks you, use `C abstract <id>
     --mark-read` (Europe PMC, Crossref, OpenAlex);
   - for PDFs the fetch tool can't parse, use `C pdf <url> --grep <term>`.

The aim is that no key claim rests on a source you haven't read. Ratios
(`check` warns under 20% read or over 30% unverified) are a symptom check.
Don't open low-value pages just to raise a number.

**Scale and stopping.** A focused topic typically needs 60–120 sources, and
roughly 40–80 searches plus catalogue runs. A broad one needs more, with
subagents. Stop when:
- `C check` shows no diversity warnings. When one doesn't fit the topic
  (a young technology has no pre-2000 literature; a craft has no regulators),
  explain it under `## Diversity exceptions` in the scope as `- decades:
  <reason>`, and it becomes a note;
- every facet has solid sources from at least 3 lenses (`stats` → "lenses
  per facet");
- new queries mostly return known sources.
Say plainly where coverage is still thin.

**User's own files:** put them in `<project>/library/raw/`, then run `C
ingest` and `C search <term>`. Supported: PDF (needs `pip install pypdf`, and
if that fails, `pip install cffi pypdf`), EPUB, HTML, TXT, MD, SRT/VTT. Hits
carry the file name and page or chapter, so they can be cited precisely.

## Step 4: Compile

File numbering in `compendium/`:
- `00-overview.md`
- chapters `01-…` to `89-…`, one per facet (merge or split as needed)
- `90-glossary.md`
- `99-bibliography.md` (generated)

Each chapter:
- **Synthesizes in your own words.** Compare sources and show where fields
  and lenses agree or clash (e.g. scientists vs. practitioners, official
  guidance vs. community experience). Cite as `[@id]` or `[@id1; @id2]`.
- **Flags confidence:** ✅ well established · ⚠️ contested or weakly
  supported · 🔎 verify before relying on it (unverified source, uncertain
  detail).
- **Ends with a purpose note:** what is essential for the user's purpose,
  what is optional, what can be cut.

`00-overview.md` covers the field on one page (its shape, the fields and
schools involved, the main open questions), plus:
- **Best sources by type:** top picks for books, papers/reviews, primary or
  historical texts, video, audio/podcasts, courses, tools/apps/data, and
  communities, one line each on why.
- **Coverage:** a short table of lenses and fields with how well each is
  represented, and the known gaps.

**Copyright:** summarize and link; short attributed quotes are fine. Don't
copy whole chapters, articles, transcripts or paywalled text into the project.
The user's own files stay in the git-ignored `library/`.

When a workbench needs numbers (weighted matrices, totals), compute them
with a short script rather than by hand.

Then:
```bash
C bib <project>      # writes compendium/99-bibliography.md
C check <project>    # PROBLEMs must be fixed; WARNings must be fixed or explained in 00-scope.md
```

## Step 5: Workbench and handoff

Create `workbench/` files for the user's purpose (see
`references/workbenches.md`).

Write `<project>/README.md`: what's there, how it was compiled (date,
scope, strategies, catalogues used), coverage and gaps, and how to extend it.

If you're in a git repository, commit the project, following the repo's
branch and commit rules.

The final reply should include:
- **Sources:** total; by status (read / confirmed / unverified); number of
  types, lenses and fields covered, and languages.
- **The 3–5 most important findings or sources**, stated plainly.
- **Gaps:** thin lenses or fields, and what must be verified before
  publishing or acting on it.
- **Next steps** they can ask for ("go deeper on X", "add my PDFs", "draft
  chapter 1").

---

## Extending an existing project

For requests like "add more on X", "I added some PDFs" or "update this":
1. Read `00-scope.md`, `README.md` and `C stats`. Update the scope first if
   the request widens it, including its facet table and Fields list, so that
   they match the tags you'll use.
2. Gather as above, registering only new sources, with lens, field and lang
   set. Log the new searches with `C log`.
3. Update the affected chapters, add new ones in the 01–89 range, and
   update `00-overview.md` (best sources, coverage) and the glossary. Create
   the overview if it is missing.
4. If older sources lack lens or field tags, add them with `C update`.
   Run `C verify` on any unverified sources.
5. Run `C bib` and `C check`, and update the README's status and gaps.
