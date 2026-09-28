# Source Hunting

## Contents
1. Where to look, by source type
2. Query patterns
3. Snowballing
4. Reliability rubric
5. Domain-specific starting points
6. Coverage checklist

---

## 1. Where to look, by source type

| Type (`--type`) | Where to find it | Search patterns |
|---|---|---|
| **book** | Publisher catalogues, Google Books, Open Library, WorldCat, Goodreads lists, "further reading" in reviews and Wikipedia, syllabi | `best books on <topic>`, `<topic> book recommendations`, `<topic> reading list`, `<topic> handbook / encyclopedia / introduction` |
| **paper** | Google Scholar, PubMed, Semantic Scholar, arXiv/bioRxiv/SSRN, CORE, journal sites, OpenAlex | `<topic> study`, `<topic> randomized`, `<topic> filetype:pdf`, key authors' names |
| **review** | Cochrane, PubMed ("review"[pt]), Annual Reviews, Stanford Encyclopedia of Philosophy | `<topic> systematic review`, `meta-analysis`, `scoping review`, `state of the art` |
| **thesis** | ProQuest, national/university repositories, EThOS/DART-Europe | `<topic> dissertation`, `<topic> thesis pdf` |
| **primary-text** | Sacred-texts, Perseus, Gutenberg, Wikisource, archives, digital libraries | `<text name> translation`, `<text name> critical edition` |
| **website / article** | Expert blogs, magazines, Substack, Medium, trade press | `<topic> explained`, `<topic> guide`, `<topic> history of` |
| **official-doc / standard** | Government, WHO/NIH/NICE, standards bodies (ISO, W3C, IETF), professional associations | `<topic> guidelines`, `<topic> standard`, `site:gov`, `site:who.int` |
| **dataset** | Kaggle, Zenodo, data.gov, Our World in Data, Hugging Face, figshare | `<topic> dataset`, `<topic> data download` |
| **video** | YouTube (lectures, conference talks, documentaries), Vimeo, university channels | `<topic> lecture`, `<topic> talk`, `<topic> documentary`, `<expert> interview` |
| **podcast** | Apple/Spotify podcast search, Listen Notes | `<topic> podcast`, `<expert> podcast episode` |
| **course** | Coursera, edX, MIT OCW, YouTube playlists, trainings and certifications, syllabi | `<topic> course`, `<topic> syllabus`, `<topic> teacher training` |
| **tool / software** | GitHub (search, awesome-lists), app stores, Product Hunt, comparison articles | `awesome <topic>`, `<topic> app`, `<topic> tool`, `<topic> open source` |
| **community** | Reddit, Discord, forums, Stack Exchange, associations, Meetup, LinkedIn/Facebook groups | `<topic> forum`, `r/<topic>`, `<topic> association` |
| **person / organization** | Author pages, institutes, labs, schools/lineages, conference speakers | `leading experts <topic>`, `<topic> institute`, `<topic> researchers` |
| **news** | News search, trade press | `<topic> 2025`, `<topic> news`, `<topic> controversy` |

## 2. Query patterns

- **Vocabulary first.** Early results teach the field's terms, synonyms,
  schools and key names. Feed them back into new queries.
- **Other languages.** Search in the languages where the field is strong
  (e.g., German for philosophy, Sanskrit/Hindi terms for yoga, Japanese for
  certain crafts).
- **Contrarian queries.** `<topic> criticism`, `<topic> debunked`,
  `<topic> controversy`, `<topic> limitations`, `<topic> risks`. A compendium
  without the criticisms is marketing.
- **Recency.** `<topic> 2024`, `<topic> 2025`, `new research <topic>`.
- **Operators.** `site:`, `filetype:pdf`, quotation marks for exact
  phrases, `intitle:`.

## 3. Snowballing

The most productive move once you have a few good sources:
- **Backward:** read the reference lists of the best reviews and books.
- **Forward:** "cited by" in Google Scholar/Semantic Scholar for a key paper.
- **Lists:** Wikipedia references and "further reading", awesome-lists,
  syllabi, "best of" threads from experts.
- **People:** once you know the 5–10 key people, search each name. Their
  books, talks, interviews and podcasts are often the best non-academic
  sources.

## 4. Reliability rubric (`--reliability`)

| Score | Meaning | Typical examples |
|---|---|---|
| 5 | Authoritative | Systematic reviews, critical editions, standards, foundational works by the field's recognized authorities, official guidelines |
| 4 | Strong | Peer-reviewed studies, academic books, well-regarded practitioner books by recognized experts |
| 3 | Useful | Serious popular books, expert blogs/talks, quality journalism, established courses |
| 2 | Weak | Marketing-adjacent content, small uncontrolled studies, anonymous or undated web pages |
| 1 | Unreliable | Content farms, unsupported claims, sources with clear conflicts of interest |

Weak sources can still be worth recording: they show what people believe,
market or argue about. Just don't rest claims on them.

## 5. Domain-specific starting points

- **Health, medicine, therapy:** PubMed, Cochrane, ClinicalTrials.gov,
  NIH/NCCIH, NICE, WHO. Always cover safety and contraindications.
- **Spiritual / contemplative traditions:** primary texts in translation,
  academic religious studies (e.g., Jason Birch-style philology), lineage
  teachers' books, critical histories. Separate traditional claims from
  historical findings.
- **Technology / software:** official docs, GitHub, RFCs/standards,
  conference talks, benchmark studies, changelogs.
- **Business / markets:** industry reports, company filings, trade press,
  case studies, expert newsletters.
- **History / humanities:** academic monographs, journal articles, primary
  archives, museum collections.
- **Crafts / skills / hobbies:** masters' books, video tutorials,
  communities, workshops, tool and material suppliers.
- **Science:** review articles, textbooks, key experiments, lab pages,
  preprint servers.

## 6. Coverage checklist

Before compiling, check with `compiler.py stats`:
- [ ] Every facet has at least 3 good sources (or a note on why not).
- [ ] At least one foundational/classic source and one recent one.
- [ ] Critical/contrarian perspectives are represented.
- [ ] Every relevant source type is covered, or noted as not existing.
- [ ] Key people and organizations are identified.
- [ ] New queries return mostly known sources (saturation).
