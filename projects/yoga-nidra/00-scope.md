# Scope: Yoga Nidra

- **Request:** compile all yoga nidra books into one resource to write my own book from.
  Extension 2 (2026-09-28): "make the compilation draw sources from all kinds of
  different areas, not just yoga books."
- **Purpose:** source base for writing my own yoga nidra book, leaving out what I deem unnecessary
- **Audience:** the author (compendium); readers of the future book (workbench)
- **Depth:** comprehensive survey of the literature; research summarized, not exhaustive
- **Languages / regions:** English core; German, French and Hindi deliberately
  searched (the practice has deep roots in India and large markets in the
  German- and French-speaking world); Spanish opportunistically. Sanskrit terms
  with diacritics.
- **Out of scope:** reproducing copyrighted book text. (Audio/app catalogues were
  out of scope at first; brought in on 2026-09-28 at the user's request as
  facet 10, kept as a dated snapshot rather than an exhaustive catalogue.)
- **Started:** 2026-09-28

This file is a working document: edit or rewrite any part of it freely.

## Facets

The first column is the facet tag used in `sources.jsonl`.

| Facet | Key questions | Chapter | Status |
|---|---|---|---|
| history | Old term vs. modern method? Who shaped it? What do Indologists and historians of modern yoga say? | 01 | done; extended with religious-studies and primary texts |
| sources | What does each major book add? | 02 | done |
| concepts | States, kośas, sankalpa, witness, pratyāhāra; sleep onset, hypnagogia, hypnosis | 03 | done; extended |
| practice | Stage sequences per lineage; common skeleton | 04 | done |
| techniques | Every technique, source, use, variations; relaxation-therapy parallels | 05 | done |
| evidence | What research shows; myths; the 2025–26 meta-analyses | 06 | done; updated 2026-09-28 |
| safety | Contraindications, trauma-sensitivity, adverse events, institutional abuse | 07 | done; extended |
| debates | Contested questions an author must decide | 08 | done; extended |
| media | Landmark recordings, apps, video, podcasts, NSDR | 10 | done (snapshot) |
| training | Teacher trainings, courses, clinical programs (VA), pedagogy | 10 | done (snapshot) |
| community | Communities, networks, forums | 10 | done (snapshot); Reddit unreadable |
| reception | Yoga nidra outside the English yoga-book world: German, French, Hindi; state bodies; markets; trial registries | 11 | new 2026-09-28 |
| vocabulary | Sanskrit & technical terms | 90 | done |

## Fields

Disciplines and domains that have something to say about yoga nidra. Tag
values in `sources.jsonl` in brackets.

- **Yoga tradition and teaching** [yoga-tradition]: lineage books, recordings, schools.
- **Religious studies, Indology, philology** [religious-studies]: the word
  *yoganidrā* in epics, Purāṇas and medieval yoga texts; the sleep goddess;
  translations of primary texts; meditation-related experience.
- **History of modern yoga** [history-of-modern-yoga]: Satyananda, Western
  relaxation therapies, Boyes, transnational spread.
- **Neuroscience** [neuroscience]: PET, EEG, fMRI studies.
- **Sleep medicine** [sleep-medicine]: sleep onset, insomnia trials, NSDR claims.
- **Clinical psychology and trauma** [clinical-psychology]: iRest/PTSD,
  anxiety/depression, adverse effects, relaxation therapies.
- **Nursing and integrative medicine** [nursing], [integrative-medicine]:
  health-care worker trials, integrative reviews, NIH/VA guidance, pain,
  cardiovascular and women's health.
- **Hypnosis and relaxation research** [hypnosis-research]: autogenic training,
  autosuggestion, sophrology, yoga nidra vs. hypnosis.
- **Consciousness studies** [consciousness-studies]: hypnagogia, phenomenology.
- **Anthropology and sociology** [anthropology], [sociology]: ethnographies
  of modern yoga, rest as social critique, consumer yoga.
- **Pedagogy** [pedagogy]: teacher training, school and university programs,
  professional bodies.
- **Law and institutional accountability** [law]: the Royal Commission.
- **Gender studies** [gender-studies]: women's-health nidras.
- **Wellness industry** [wellness-industry]: apps, market reports, NSDR branding.

## Lenses

| Lens | What it means | Where to look for this topic | Covered |
|---|---|---|---|
| scholarly | academic research, reviews, university presses | Europe PMC / Crossref (IJYT, Int J Yoga, sleep and psychology journals); Birch, Singleton, De Michelis, Newcombe; British Academy and OUP Indology | strong: meta-analyses, history of modern yoga, Indology |
| practitioner | people who do it: experts, teachers, professionals, makers | lineage books, trainings, recordings, teacher sites | strong (60 sources; below 50% of the registry) |
| historical | primary sources, archives, historical scholarship, classic texts | archive.org (Pargiter, Pancham Sinh, Nikhilananda), Gallica (Boyes), Hindi catalogue records, Jacobson/Schultz/Coué | good; Satyananda's 1964 talk unverified |
| cultural | regional, non-English, indigenous or tradition-specific perspectives | German publishers (Ananda, Via Nova, GU), Yoga Vidya, French (Almora, sophrology), Hindi press (Akhand Jyoti), Italian and Icelandic research | good for de/fr/hi; Scandinavian and Spanish thin |
| critical | skeptics, critics, debunkers, ethical and safety critiques | Royal Commission, The Luminescent, meditation-harm research (Britton, Farias), Mind the Hype, NSDR critiques | adequate (12) |
| official | government, regulators, standards bodies, professional associations | NCCIH, VA, Royal Commission, AYUSH, Yoga Australia, IAYT, German insurers | adequate (11) |
| industry | companies, market reports, trade press, product documentation | app stores, Huberman Lab, market reports, Sleep Foundation | adequate (9); market reports paywalled |
| community | forums, lived experience, user reviews, grassroots groups | YNN, Reddit (unreadable), Yoga Vidya wiki, Stack Exchange, co-design studies | thin (8); Reddit/Discord unreadable from here |
| popular | journalism, popular books, podcasts, documentaries, influencers | podcasts, YouTube, NSDR media, German/Hindi web media | strong |
| data | datasets, statistics, tools, calculators, software | ClinicalTrials.gov, CTRI, OSF registrations, IAYT bibliography | adequate (7) |

### Known gaps (not diversity warnings, but worth saying)

- **Anthropology** has only general ethnographies of modern yoga (Strauss,
  Alter) plus one ritual study; no fieldwork on yoga nidra classes was found.
- **Scandinavian** (Janakananda's Swedish/Danish school) and **Spanish/Italian**
  literatures are represented by one or two items each.
- **Community** voices are thin because Reddit, Facebook and Discord cannot be
  read from the compiling environment.
- Several non-English books are only *confirmed* (publisher or bookseller
  listing), not read.

## Search log

| Query / place searched | New sources | Notes |
|---|---|---|
| First compilation from background knowledge | 26 | Most sources unverified; see bibliography |
| "Birch Hargreaves Yoganidrā luminescent" | 0 (verified birch2015) | Confirmed URL; added tantric and āsana uses |
| Extension 2026-09-28: training bodies (iRest Level 1, Total Yoga Nidra TT, I AM certification, Tracee Stanley, Kripalu Divine Sleep, Daring to Rest, Ally Boothroyd) | 10 courses + 3 orgs/communities | Most opened on the school's own page; Kripalu, Himalayan Institute, Yoga International returned 403/empty |
| "Yoga Nidra Network free recordings", biharyoga.net tribute & Satyam Yoga Prasad, iRest "Try iRest" | 5 | Free libraries; YNN 600+ nidras / 23 languages; Bihar ~100-108 languages |
| "Huberman NSDR", hubermanlab.com/nsdr, NSDR dopamine critique | 2 | 65% dopamine claim traced to Kjaer 2002 |
| "Swami Janakananda Experience Yoga Nidra", yogameditation.com | 1 | The Copenhagen PET studies used this lineage's guided nidra |
| IAYT bibliography (Lamb 2006), snowballed | 4 (Jnaneshvara CD, Miller tapes, Mishra 1959, + reference itself) | Also lists Shiva Rea, Muz Murray tapes (not registered) |
| Wikipedia "Yoga nidra", snowballed | 4 (Boyes 1973, Singleton 2005, Shearer 2020, + page) | Boyes 1973 predates Satyananda |
| Insight Timer topic page, Jennifer Piercy, Ally Boothroyd, yoga nidra apps | 5 | Kamini Desai app list has a conflict of interest |
| "yoga nidra podcast", Radiant Rest, Naropa/Miller, Uma interviews | 5 | Most guided-practice podcasts interchangeable |
| "best yoga nidra books" lists (kaminidesai.com, YNN shop), title searches | 7 books (Miller 2010, Bonnasse, Moore, Verma, Stanley 2023, Hersey, Yoni Shakti) | "The Little Book of Yoga Nidra" (Kate Taylor) could not be confirmed; not registered |
| "reddit r/yoganidra" | 1 | reddit.com cannot be fetched from this environment |
| "yoga nidra documentary" (implicit in Miller/Walter Reed search) | 0 | No documentary found |
| Extension 2 (2026-09-28, 'sources from all areas'): tagged all 75 old sources with lens/field/lang; verify + manual Open Library checks | 0 | verify's book check fails on long subtitles; 10 books confirmed by main-title OL search or publisher page |
| discover papers: yoga nidra review/meta-analysis; trial/randomized; iRest; nursing | 26 | A 2025-26 wave of meta-analyses (Ghai x3, Singh, Dutta, Sony), Moszeik RCT, YOGA-FDS, nursing reviews |
| discover crossref: yoganidra goddess Visnu sleep; yoga nidra history modern yoga; hypnosis autogenic | 9 | Sarkar 2017, Simmons 2025 (religious studies), De Michelis, Zaccaro 2021, Luu 2024, Hoye & Reddy 2016; Moszeik German monograph |
| discover archive 'yoga nidra'; archive.org searches for Pargiter Markandeya, Pancham Sinh HYP, Mandukya (Nikhilananda, Sauton), Yogataravali Hindi | 8 | Pargiter canto 81 read in full text; many Melissa West videos ignored |
| discover hn / stackexchange (hinduism, buddhism) | 0 | HN 'NSDR' returns unrelated hits; HN 'Yoga Nidra' thread was wrongly marked 'had' (title clash with satyananda1976); nothing substantive |
| German web: 'Yoga Nidra Buch Tiefenentspannung', 'Yoga Nidra Kritik', Krankenkasse/§20, Schlafforscher NSDR | 9 | Ananda Verlag (Satyananda tr., Marutdeva CD), Via Nova (Röcker), Kündig, Trökes, Yoga Vidya wiki, AOK, Moszeik dissertation; no §20 course specific to yoga nidra found |
| French web: 'yoga nidra livre sommeil conscient', sophrologie Caycedo | 4 | Bonnasse French original, Sauton Mandukya, Caycedo, Sophro-Nidra; sophrology link claimed, not documented |
| Hindi web: योग निद्रा पुस्तक / शोध | 4 | Akhand Jyoti 1983 (read), Art of Living, Webdunia; Hindi books by BSY exist but not catalogued |
| Royal Commission Case Study 21; Luminescent 'Culture of Silence'; Yoga Australia | 4 | childabuseroyalcommission.gov.au returned 503; findings PDF not downloadable; findings taken from secondary quotes |
| NCCIH relaxation / meditation safety; VA Whole Health, WRIISC iRest; AYUSH Common Yoga Protocol | 5 | All but VA Whole Health opened |
| NSDR critique; Huberman topics; Sleep Foundation; app market (Grand View, Mordor); App Store NSDR apps | 6 | Grand View and Worldcrunch 403; Mordor opened |
| Scholarly history: De Michelis, Singleton 2010, Newcombe, Strauss, Alter, Jain, Mallinson & Singleton; YNN Academic Resources page | 9 | Satyananda 1964 convention talk found second-hand |
| discover books --lang de / fr / hi 'yoga nidra' | 0 | Open Library holds almost no German yoga nidra books; --lang hi returns nothing (hi not mapped to hin). Direct OL query language=hin found Dikshit 1967, Bhattacharya 1969 |
| ClinicalTrials.gov API v2 'yoga nidra' and iRest | 1 | Registered as one dataset: 22 and 27 records; CTRI search is captcha-gated, IDs taken from papers |
