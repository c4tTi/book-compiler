# Yoga Nidra Book Compiler

One working resource that brings together the major yoga nidra literature
(traditional sources, modern lineages, the research, and the debates), plus a
workbench for writing your own yoga nidra book from it.

## What's here

```
compendium/          The compiled resource, synthesized and cross-referenced
  01-history-and-lineages.md   From Vishnu's cosmic sleep to iRest
  02-source-books.md           Annotated bibliography: every major book, what it adds
  03-core-concepts.md          States of consciousness, koshas, sankalpa, witness...
  04-practice-structures.md    The stage sequences of each lineage, side by side
  05-techniques-library.md     Every technique, with where it comes from and how it's used
  06-research.md               The science: what's shown, what's claimed, what's weak
  07-teaching-and-safety.md    Trauma-sensitivity, contraindications, voice, language
  08-debates.md                The contested questions an author has to take a position on
  09-glossary.md               Sanskrit and technical terms

workbench/           Your book
  keep-cut-log.md              Decide what goes in and what you leave out, and why
  book-outline.md              Skeleton outline to fill in
  voice-and-positions.md       Your stances on the debates, so the book stays consistent

tools/ingest.py      Turn your own PDFs/EPUBs/TXT into searchable, page-cited notes
library/raw/         Put your book files here (git-ignored)
library/extracted/   Extracted text lands here (git-ignored)
```

## How the compendium is written

- **Synthesized, not copied.** Everything is paraphrased and attributed, with
  a source tag like `[Satyananda 1976]` or `[Miller 2005]`, so you always know
  where an idea came from. The full reference list is in
  `compendium/02-source-books.md`. Copyrighted books are not reproduced.
- **Confidence flags.** Where a claim is historically or scientifically
  shaky, it is marked:
  - ✅ well established
  - ⚠️ contested or weakly supported
  - 🔎 verify against the original before you quote or publish
- **Built for cutting.** Every section ends with an *Author's note* on what is
  essential and what is optional, to help you decide what to leave out.

## Adding the books you own

```bash
pip install pypdf          # only needed for PDFs; EPUB/TXT/MD use the standard library
cp ~/Books/*.pdf ~/Books/*.epub library/raw/
python3 tools/ingest.py                  # extract everything in library/raw/
python3 tools/ingest.py search sankalpa  # find every passage mentioning "sankalpa"
python3 tools/ingest.py search "rotation of consciousness" --context 300
```

Each result shows the book and the page (or chapter), so you can check the
original and cite it properly. Extracted text never leaves your machine
because `library/` is git-ignored.

## Suggested workflow

1. Read `compendium/` end to end once. It is the map of the field.
2. In `workbench/voice-and-positions.md`, decide where you stand on the
   debates in `08-debates.md`.
3. Go through `workbench/keep-cut-log.md` and mark each topic
   **keep / brief / cut**.
4. Build `workbench/book-outline.md` from what you kept, adding your own
   experience and teaching.
5. Use `tools/ingest.py search` to check any fact against your own copies of
   the books before you publish.
