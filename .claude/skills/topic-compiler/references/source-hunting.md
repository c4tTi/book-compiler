# Source Hunting

## Contents
1. Lenses: where each perspective lives
2. Fields: finding the disciplines
3. Where to look, by source type
4. Catalogues (`compiler.py discover`)
5. When sites block you
6. Query patterns
7. Snowballing
8. Reliability rubric
9. Coverage checklist

---

## 1. Lenses: where each perspective lives

A lens is the kind of voice a source brings. Tag every source with one or
more (`--lens`). Popular web search over-returns *popular* and *industry*,
so the others have to be hunted deliberately.

| Lens | Who speaks | Where to find it | Query patterns |
|---|---|---|---|
| **scholarly** | Researchers, academic presses | Europe PMC, PubMed, Crossref, Google Scholar, arXiv/SSRN, university presses, Annual Reviews, Stanford Encyclopedia of Philosophy | `<topic> review`, `<topic> meta-analysis`, `<topic> handbook`, `discover --catalogues papers,crossref` |
| **practitioner** | People who do it professionally or expertly | Masters' books, teacher trainings, professional blogs, trade manuals, conference talks, guild/association materials | `<topic> masterclass`, `<topic> professional guide`, `<well-known practitioner> interview` |
| **historical** | Primary sources, archives, historians | Internet Archive, Project Gutenberg, HathiTrust, Wikisource, museum and library collections, digitized newspapers, historical monographs | `history of <topic>`, `<topic> 19th century`, `discover --catalogues archive`, old-spelling terms |
| **cultural** | Regional, non-English, indigenous, tradition-specific voices | Books and sites in the topic's other languages, regional institutions, ethnographies, diaspora communities | Native-language terms (`levain`, `Sauerteig`, `lievito madre`), `discover --catalogues books --lang fr`, `<topic> in <country/culture>` |
| **critical** | Skeptics, critics, ethicists, safety voices | Skeptic organizations, critical reviews, investigative journalism, retraction watch, consumer protection | `<topic> criticism`, `<topic> myth`, `<topic> debunked`, `<topic> risks`, `<topic> controversy`, `<topic> harm` |
| **official** | Government, regulators, standards bodies, professional associations | .gov, WHO/EFSA/FDA/NICE, ISO/IETF/W3C, licensing bodies, codes of practice | `<topic> guideline`, `<topic> regulation`, `<topic> standard`, `site:gov <topic>` |
| **industry** | Companies, markets, trade press | Market reports, company docs and white papers, trade magazines, product sites, patents | `<topic> market size`, `<topic> industry report`, `<topic> trade association`, Google Patents |
| **community** | Enthusiasts, lived experience, users | Reddit, forums, Discord, Facebook groups, Stack Exchange, Hacker News, review sites, meetups | `<topic> forum`, `r/<topic>`, `discover --catalogues hn,stackexchange --se-site <site>`, `<topic> beginner mistakes reddit` |
| **popular** | Journalists, popular authors, media | Popular books, magazines, podcasts, YouTube, documentaries, newsletters | `best books on <topic>`, `<topic> podcast`, `<topic> documentary`, `<topic> explained` |
| **data** | Datasets, statistics, tools | Kaggle, Zenodo, Our World in Data, official statistics, GitHub, calculators, apps | `<topic> dataset`, `<topic> statistics`, `<topic> calculator`, `awesome <topic>` |

## 2. Fields: finding the disciplines

Ask: *Who studies this, and in which departments?* Then list the
disciplines behind each facet:
- **Material or physical side:** chemistry, biology, physics, materials,
  engineering.
- **Human side:** medicine, psychology, neuroscience, physiology.
- **Social side:** sociology, anthropology, economics, law and policy,
  education.
- **Meaning side:** history, philosophy, religious studies, literature,
  art, linguistics.
- **Making side:** craft, design, technology, business.

For each field, learn two or three of its technical terms and search with
those. Scholarly vocabulary finds a different literature than popular
vocabulary ("lactic acid bacteria fermentation cereal" vs. "sourdough
tips"). Tag sources with `--field` so `stats` can show which fields are
missing.

## 3. Where to look, by source type

| Type (`--type`) | Where to find it | Search patterns |
|---|---|---|
| book / book-chapter | Open Library (`discover books`), publisher catalogues, WorldCat, "further reading", syllabi, Goodreads lists | `best books on <topic>`, `<topic> handbook / encyclopedia / introduction` |
| paper / review / thesis | Europe PMC and Crossref (`discover papers,crossref`), Google Scholar, arXiv/SSRN, repositories | `<topic> systematic review`, `<topic> randomized`, `<topic> dissertation` |
| primary-text / archive | Internet Archive (`discover archive`), Gutenberg, Wikisource, HathiTrust, museum collections | `<text> translation`, `<topic> manuscript`, `<topic> archive` |
| website / article / news | Expert blogs, magazines, newsletters, news search | `<topic> guide`, `<topic> history of`, `<topic> 2026` |
| official-doc / standard | Government, WHO, standards bodies, associations | `<topic> guidelines`, `<topic> standard` |
| dataset | Kaggle, Zenodo, data portals, Our World in Data | `<topic> dataset` |
| video / audio / podcast | YouTube, Vimeo, university channels, archive.org audio, podcast directories | `<topic> lecture`, `<topic> documentary`, `<topic> podcast episode` |
| course | Coursera, edX, MIT OCW, trainings, certifications | `<topic> course`, `<topic> syllabus`, `<topic> certification` |
| app / tool / software | App stores, GitHub, awesome-lists, comparison articles | `<topic> app`, `awesome <topic>` |
| community | Reddit, forums, Discord, Stack Exchange, HN | `<topic> forum`, `r/<topic>` |
| person / organization | Author pages, institutes, labs, associations | `leading experts <topic>`, `<topic> institute` |

## 4. Catalogues (`compiler.py discover`)

| Catalogue | Covers | Good for lenses |
|---|---|---|
| `books` (Open Library) | Books in all languages, old and new; use `--lang` | practitioner, popular, cultural, historical |
| `papers` (Europe PMC) | Life sciences, medicine, psychology; includes PubMed; abstracts | scholarly, critical |
| `crossref` | All DOI-registered work: journals, book chapters, theses, reports, standards | scholarly, official |
| `openalex` | Scholarly works in every discipline, incl. humanities and engineering; language filter; abstracts | scholarly, historical, cultural |
| `archive` (Internet Archive) | Digitized old books, audio, film, radio, podcasts | historical, cultural, popular |
| `hn` (Hacker News) | Tech-adjacent discussion, often with expert commenters | community, critical |
| `stackexchange` | Q&A communities; pick a site with `--se-site` (cooking, history, fitness, philosophy, diy, music, workplace, ...) | community, practitioner |

Options:
- `--sort cited` searches titles and abstracts and ranks by citations or
  downloads. Use it to find the classics.
- `--lang` filters by language.

Output is raw candidates (`c1, c2, …`). Pick the relevant ones with `add
--from-jsonl … --pick`, setting reliability, lens, field and facets as you
add them. Internet Archive results skip known pirate uploads and flag
user uploads to check. Never register pirated copies of books.

## 5. When sites block you

| Blocked | Fallback |
|---|---|
| PubMed captcha, journal paywalls or 403s | `compiler.py abstract <id> --mark-read` (Europe PMC → Crossref → OpenAlex abstracts); open-access copies via Europe PMC/PMC links; `discover papers,openalex` |
| PDF the fetch tool can't parse | `compiler.py pdf <url> --grep <term>` or `--pages 1-5` |
| Rate limits (429) | The helper retries with backoff; for web search, space out queries and log what's pending |
| Publisher or bookstore 403 | Open Library record (`verify`), Wikipedia article on the book, author's own site, reviews |
| YouTube not readable | `verify` confirms title and channel via oEmbed; search for transcripts or show notes; confirm via the channel's own site |
| Reddit, Discord, Facebook not readable | Search snippets (status stays `confirmed` or `unverified`); Stack Exchange/HN equivalents; blog posts summarizing the community |
| App stores | Developer's site, press coverage |
| Any page | Try the site's other URL forms (print view, AMP, RSS); the Internet Archive's copy (`https://web.archive.org/web/2024/<url>`) if reachable from your environment; or another site quoting the same primary text (then cite the primary, status `confirmed`) |

Record what was blocked in the search log, so the next session doesn't retry
blindly.

## 6. Query patterns

- **Vocabulary first.** Early results teach terms, synonyms, schools and
  names. Feed them back in.
- **Other languages.** Search in the languages where the topic has deep
  roots, and tag `--lang`.
- **Contrarian queries.** `criticism`, `debunked`, `controversy`,
  `limitations`, `risks`. A compendium without criticism is marketing.
- **Recency and classics.** Search both `<topic> 2025/2026` and
  `<topic> classic / original / history`. `stats` shows the spread across
  decades.
- **Operators.** `site:`, `filetype:pdf`, exact phrases in quotes,
  `intitle:`.

## 7. Snowballing

- **Backward:** reference lists of the best reviews and books.
- **Forward:** "cited by" for key papers; `discover crossref` with the
  paper's title words.
- **Lists:** Wikipedia references and further reading, awesome-lists,
  syllabi, expert "best of" threads, bibliographies from associations.
- **People:** search each of the 5–10 key names for their books, talks,
  interviews and podcasts.

## 8. Reliability rubric (`--reliability`)

| Score | Meaning | Typical examples |
|---|---|---|
| 5 | Authoritative | Systematic reviews, critical editions, standards, official guidelines, foundational works |
| 4 | Strong | Peer-reviewed studies, academic books, recognized experts' books |
| 3 | Useful | Serious popular books, expert blogs and talks, quality journalism, established courses |
| 2 | Weak | Marketing-adjacent content, small uncontrolled studies, anonymous pages, single forum threads |
| 1 | Unreliable | Content farms, unsupported claims, clear conflicts of interest |

Low-reliability sources still show what people believe or argue about, and
community sources are often the best record of beginners' real problems.
Record them and label them, but don't rest claims on them.

## 9. Coverage checklist

`compiler.py check` reports most of this as warnings:
- [ ] Each facet has sources from at least 3 lenses.
- [ ] 7+ of the 10 lenses are covered, or the scope says why not.
- [ ] 4+ fields/disciplines are tagged.
- [ ] More than one language, where the topic has non-English roots.
- [ ] Sources span several decades (classics and recent work).
- [ ] 8+ source types are used.
- [ ] At least 30% read, at most 30% unverified.
- [ ] New queries mostly return known sources (saturation).
