# Workbenches by Purpose

The compendium is the neutral map of the field. The workbench is where the
user turns it into *their* thing. Pick the template for the stated purpose,
combine templates when purposes overlap, and adapt the headings to the topic.

---

## Writing a book (or long article)

**`workbench/keep-cut-log.md`**: a table with one row per topic from the
compendium:
`| # | Topic | Compendium section | Suggested (KEEP/BRIEF/CUT) | Decision | Why |`
Fill in "Suggested" from the chapters' purpose notes. Leave "Decision" empty.
Add a second table, "Your own material", for what the user knows that the
literature doesn't cover.

**`workbench/voice-and-positions.md`**: audience; the reader's promise;
one entry per debate in the compendium ("My position: ___"); "What makes my
book different"; "What I'm deliberately leaving out".

**`workbench/book-outline.md`**: parts → chapters, each chapter pointing to
the compendium sections it draws on, e.g. `[03 §3.2]`.

## Teaching a course / workshop

**`workbench/syllabus.md`**: learning outcomes; sessions (title, goals,
readings from the registry by `[@id]`, activities, time); assessments.
**`workbench/reading-list.md`**: core / recommended / advanced, per session.
**`workbench/supply-list.md`** (hands-on subjects): materials and tools per
participant, suppliers with prices (`--accessed` date on those sources), and
a small budget script if group size varies.

## Making a decision (buying, choosing a method, tool or strategy)

**`workbench/options-matrix.md`**: options × criteria, with evidence cited
per cell, weights, and a recommendation with its confidence.
**`workbench/open-questions.md`**: what would change the decision and how
to find out.

When money is involved (payback, total cost of ownership, budget), add a
small runnable model: `workbench/model.py`. Put the inputs at the top, each
with its source `[@id]` and date. Print the result for a base case plus a
sensitivity table (e.g. price ±20%, usage low/high, subsidy yes/no). Put the
printed output into the options matrix. Readers can then rerun it with their
own numbers. Compute weighted-matrix totals with the same script, never by
hand.

## Learning a field (self-study)

**`workbench/learning-path.md`**: stages (foundations → core → advanced),
each with 2–5 resources of mixed type (a book, a video, a course, a
practice), time estimates, and "you're ready to move on when you can...".

## Building a product / business

**`workbench/landscape.md`**: players, tools, pricing, gaps in the market.
**`workbench/opportunities.md`**: unmet needs found in communities and
reviews, cited.

## General reference

No workbench needed. Put extra effort into `00-overview.md` and the glossary.
