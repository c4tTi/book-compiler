# Topic-compiler test results

Each run gives the skill a realistic request and scores the output with
`grade.py`: 15 automatic checks covering structure, verification and
diversity (lenses, fields, languages, source types).

| Iteration | Skill version | Test | Score | Sources | Read / confirmed / unverified | Lenses | Fields | Languages |
|---|---|---|---|---|---|---|---|---|
| 1 | none (baseline) | sourdough book | 1/15 | ~72 URLs in one file | – | – | – | – |
| 1 | v1 | sourdough book | 10/15 | 90 | 20 / – / 70 | not tracked | not tracked | 1 |
| 1 | v1 | intermittent fasting decision | 10/15 | 90 | 22 / – / 68 | not tracked | not tracked | 1 |
| 2 | v2 | sourdough book | 15/15 | 156 | 47 / 108 / 1 | 10/10 | 11 | 4 |
| 2 | v2 | home battery decision (CH) | 15/15 | 105 | 33 / 69 / 3 | 10/10 | 12 | 4 |
| 2 | v2 | mokuhanga workshop | 15/15 | 189 | 59 / 129 / 1 | 10/10 | 9 | 6 |
| 2 | v2 | yoga nidra upgrade (real project) | – | 75 → 158 | 81 / 68 / 9 | 0 → 10 | 0 → 16 | 1 → 5 |

## What changed between versions

- **v1 → v2:**
  - lens, field and language tags with diversity warnings
  - catalogue discovery and automatic verification
  - a "confirmed" status between read and unverified
  - gathering in rounds, including a fields and lenses sweep
  - batch add, update, rename and log commands
- **v2 → v3:** fixes for friction reported in iteration 2:
  - OpenAlex catalogue, `--sort cited`, candidate picking with shared tags
  - fallbacks for blocked sites (abstracts via Crossref/OpenAlex, a `pdf`
    command, retry on rate limits)
  - Unicode-aware duplicate detection, language code normalisation, author
    formatting
  - diversity exceptions explained in the scope
  - field coverage checked against the scope
  - a filter for pirated uploads
