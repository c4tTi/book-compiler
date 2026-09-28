#!/usr/bin/env python3
"""Project, source-registry, verification and file-ingest helper for the topic-compiler skill.

Commands (PROJECT is a directory, e.g. projects/yoga-nidra):
  init PROJECT --title T [--purpose P] [--request R]
  add PROJECT --title T --type TYPE [--author A] [--year Y] [--url U] [--publisher P]
              [--reliability 1-5] [--status seen|confirmed|unverified] [--facets f1,f2]
              [--lens L1,L2] [--field F1,F2] [--lang en] [--license L] [--no-url-reason R]
              [--accessed YYYY-MM-DD] [--notes N] [--id ID]
  add PROJECT --from-jsonl FILE [--pick c1,c4] [--lens ... --field ... (defaults)]
                                    batch add (one JSON object per line, same keys as above;
                                    facets/lens/field may be lists or comma strings)
  delete PROJECT ID1,ID2 [--force]  remove sources (refuses if still cited unless --force)
  update PROJECT ID [same options as add]   change fields of an existing source
  rename PROJECT OLD NEW            change a source ID and rewrite its citations in all project .md files
  sources PROJECT [--type T] [--facet F] [--lens L] [--status S]
  log PROJECT QUERY [--found N] [--notes N] | log PROJECT --from-tsv FILE
                                    append rows to the search log in 00-scope.md
  verify PROJECT [--ids a,b] [--limit N] [--dry-run]
                                    confirm unverified sources against Crossref (papers),
                                    Open Library (books), YouTube oEmbed (videos) or the URL itself;
                                    fills missing year/publisher/url/doi and sets status=confirmed
  discover PROJECT QUERY [--catalogues books,papers,crossref,openalex,archive,hn,stackexchange]
           [--rows N] [--lang de] [--sort relevance|cited] [--se-site cooking] [--out candidates.jsonl]
                                    search open catalogues directly (Open Library, Europe PMC,
                                    Crossref, OpenAlex, Internet Archive, Hacker News, Stack Exchange) and
                                    write new candidates for review and batch add
  abstract PROJECT ID [--mark-read] print a paper's abstract (Europe PMC, then Crossref, then
                                    OpenAlex); works when the publisher site is blocked
  pdf URL|PATH [--pages 1-5] [--grep term]   print a PDF's text (fetch tools often can't read PDFs)
  stats PROJECT                     coverage by type, lens, field, facet, language, decade, status
  check PROJECT [--strict]          PROBLEMs (exit 1): duplicates, bad fields, dangling citations.
                                    WARNings: thin diversity, facets not in scope; notes: uncited sources.
                                    --strict makes warnings fail too.
  bib PROJECT                       write compendium/99-bibliography.md
  ingest PROJECT                    extract text from PROJECT/library/raw/ (pdf needs: pip install pypdf)
  search PROJECT TERM [--context N] search the extracted files

Statuses: seen = the source's own content was opened and read in this session;
confirmed = existence and details confirmed (catalogue record, the item's own page
title, a DOI record) but the content was not read; unverified = from memory or a
second-hand mention only.
"""

import argparse
import html
import json
import re
import signal
import sys
import unicodedata
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from xml.etree import ElementTree

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # allow piping into head

SOURCE_TYPES = [
    "book", "book-chapter", "paper", "review", "thesis", "primary-text", "website", "article",
    "official-doc", "standard", "dataset", "archive", "video", "audio", "podcast", "course",
    "app", "tool", "software", "community", "person", "organization", "news", "other",
]
HEADINGS = {"book-chapter": "Book chapters", "primary-text": "Primary texts", "official-doc": "Official documents",
            "software": "Software", "news": "News", "person": "People", "other": "Other",
            "dataset": "Datasets", "thesis": "Theses", "audio": "Audio recordings", "archive": "Archives & collections"}
NO_URL_OK = {"book", "book-chapter", "primary-text", "person", "thesis", "audio"}

# Lenses: the perspective a source brings. A compilation drawing on one or two
# lenses is lopsided however many sources it has.
LENSES = {
    "scholarly": "academic research, reviews, university presses",
    "practitioner": "people who do it: experts, teachers, professionals, makers",
    "historical": "primary sources, archives, historical scholarship, classic texts",
    "cultural": "regional, non-English, indigenous or tradition-specific perspectives",
    "critical": "skeptics, critics, debunkers, ethical and safety critiques",
    "official": "government, regulators, standards bodies, professional associations",
    "industry": "companies, market reports, trade press, product documentation",
    "community": "forums, lived experience, user reviews, grassroots groups",
    "popular": "journalism, popular books, podcasts, documentaries, influencers",
    "data": "datasets, statistics, tools, calculators, software",
}
STATUSES = ["seen", "confirmed", "unverified"]
LIST_FIELDS = ("facets", "lens", "field")
FIELD_ORDER = ["id", "type", "title", "author", "year", "publisher", "url", "doi", "reliability", "status",
               "facets", "lens", "field", "lang", "license", "no_url_reason", "accessed", "notes", "added", "verified_by"]

PROJECT_DIRS = ["compendium", "workbench", "library/raw", "library/extracted"]
GITIGNORE = """# The user's own files and their extracted text stay local (copyright).
library/raw/*
library/extracted/*
!library/raw/.gitkeep
!library/extracted/.gitkeep
# Scratch files for this project (candidate batches, helper scripts)
.work/
"""
USER_AGENT = "topic-compiler/2.0 (research bibliography tool)"


# ---------------------------------------------------------------- registry

def registry_path(project):
    return Path(project) / "sources.jsonl"


def load_sources(project):
    path = registry_path(project)
    if not path.exists():
        sys.exit(f"No sources.jsonl in {project}. Run init first.")
    with path.open(encoding="utf-8") as lines:
        return [json.loads(line) for line in lines if line.strip()]


def save_sources(project, sources):
    path = registry_path(project)
    tmp = path.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as out:
        for s in sources:
            ordered = {k: s[k] for k in FIELD_ORDER if k in s}
            ordered.update({k: v for k, v in s.items() if k not in ordered})
            out.write(json.dumps(ordered, ensure_ascii=False) + "\n")
    tmp.replace(path)


TRANSLIT = str.maketrans({
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i",
    "й": "i", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "",
    "э": "e", "ю": "iu", "я": "ia", "і": "i", "ї": "i", "є": "e", "ґ": "g",
    "α": "a", "β": "b", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "e", "θ": "th", "ι": "i", "κ": "k",
    "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o", "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t",
    "υ": "y", "φ": "ph", "χ": "ch", "ψ": "ps", "ω": "o"})


def slug(text):
    """ASCII slug for IDs and file names (Cyrillic/Greek transliterated); empty for e.g. CJK-only text."""
    text = unicodedata.normalize("NFKD", str(text).lower().translate(TRANSLIT)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def title_key(text):
    """Unicode-aware key for duplicate detection (keeps Japanese, Hindi, ...)."""
    text = unicodedata.normalize("NFKC", str(text)).casefold()
    return re.sub(r"[\W_]+", "", text)


ISO_639 = {  # catalogue codes (ISO 639-2/B and /T) -> the 2-letter codes used in the registry
    "eng": "en", "ger": "de", "deu": "de", "fre": "fr", "fra": "fr", "ita": "it", "spa": "es",
    "por": "pt", "dut": "nl", "nld": "nl", "jpn": "ja", "chi": "zh", "zho": "zh", "kor": "ko",
    "hin": "hi", "san": "sa", "rus": "ru", "tur": "tr", "ara": "ar", "pol": "pl", "swe": "sv",
    "dan": "da", "nor": "no", "fin": "fi", "gre": "el", "ell": "el", "heb": "he", "tha": "th",
    "vie": "vi", "ind": "id", "cze": "cs", "ces": "cs", "hun": "hu", "rum": "ro", "ron": "ro",
    "per": "fa", "fas": "fa", "ben": "bn", "tam": "ta", "urd": "ur", "lat": "la", "tib": "bo", "bod": "bo",
}
ISO_639_B = {"de": "ger", "fr": "fre", "nl": "dut", "zh": "chi", "el": "gre", "cs": "cze", "ro": "rum", "fa": "per", "bo": "tib"}


LANG_NAMES = {"english": "en", "german": "de", "deutsch": "de", "french": "fr", "français": "fr", "italian": "it",
              "spanish": "es", "portuguese": "pt", "dutch": "nl", "japanese": "ja", "chinese": "zh", "korean": "ko",
              "hindi": "hi", "sanskrit": "sa", "russian": "ru", "turkish": "tr", "arabic": "ar", "persian": "fa",
              "latin": "la", "greek": "el", "polish": "pl", "swedish": "sv", "tibetan": "bo", "ge": "de", "jp": "ja"}


def lang2(code):
    code = str(code or "").strip().lower()
    if code in LANG_NAMES:
        return LANG_NAMES[code]
    return ISO_639.get(code, code[:2] if len(code) == 3 and code not in ISO_639 else code)


def lang3(code):
    """2-letter -> Open Library's 3-letter (bibliographic) code."""
    code = lang2(code)
    return ISO_639_B.get(code) or next((k for k, v in ISO_639.items() if v == code), code)


INITIAL = re.compile(r"[A-Z][A-Z]?\.?|[A-Z]\.[A-Z]\.?")


def first_surname(author):
    first = re.split(r";|&| and |,? et al\.?", author)[0].strip()
    comma_form = "," in first
    if comma_form:  # "van der Berg, K." or Europe PMC "Watters SA, Smith B"
        first = first.split(",")[0].strip()
    parts = first.split()
    if len(parts) > 1 and INITIAL.fullmatch(parts[-1]):  # "Watters SA"
        return " ".join(w for w in parts if not INITIAL.fullmatch(w))
    if comma_form:
        return first
    words = [w for w in parts if not INITIAL.fullmatch(w)]
    return words[-1] if words else first


def surname_first(name):
    """'Hokusai Katsushika' stays, 'Laura Boswell' -> 'Boswell, L.', 'Smith, J.' stays."""
    name = name.strip()
    if not name or "," in name or len(name.split()) < 2 or not name.isascii():
        return name
    *given, last = name.split()
    return f"{last}, " + " ".join(g[0] + "." for g in given)


STOP_WORDS = {"the", "a", "an", "of", "on", "and", "in", "to", "for", "with", "is", "are", "why", "how",
              "what", "when", "does", "do", "can", "my", "your", "i", "you", "it", "this", "should"}


def make_id(author, year, title, taken):
    if author and slug(first_surname(author)):
        base_word = first_surname(author)
    else:
        words_ = [w for w in re.findall(r"[A-Za-z]+", slug(title).replace("-", " ")) if w.lower() not in STOP_WORDS]
        base_word = "".join(words_[:2]) or "src"
    base = (re.sub(r"[^a-z0-9]", "", slug(base_word))[:20] or "src") + (re.sub(r"\D", "", str(year or ""))[:4])
    candidate, suffix = base, ord("a")
    while candidate in taken:
        candidate = f"{base}{chr(suffix)}"
        suffix += 1
    return candidate


def as_list(value):
    if value is None:
        return None
    if isinstance(value, list):
        return [v.strip() for v in value if str(v).strip()]
    return [v.strip() for v in str(value).split(",") if v.strip()]


def validate(record):
    errors = []
    if record.get("type") not in SOURCE_TYPES:
        errors.append(f"unknown type '{record.get('type')}' (use one of: {', '.join(SOURCE_TYPES)})")
    if record.get("status", "unverified") not in STATUSES:
        errors.append(f"unknown status '{record.get('status')}'")
    for lens in record.get("lens", []):
        if lens not in LENSES:
            errors.append(f"unknown lens '{lens}' (use: {', '.join(LENSES)})")
    rel = record.get("reliability")
    if rel is not None and rel not in (1, 2, 3, 4, 5):
        errors.append(f"reliability must be 1-5, got {rel}")
    return errors


def normalize(raw):
    record = {k: v for k, v in raw.items() if v not in (None, "", [])}
    for key in LIST_FIELDS:
        if key in record:
            record[key] = as_list(record[key])
    if "reliability" in record:
        record["reliability"] = int(record["reliability"])
    if "year" in record:
        record["year"] = str(record["year"])
    if "lang" in record:
        record["lang"] = lang2(record["lang"])
    return record


def insert_source(sources, raw):
    """Validate and append; returns (record, error)."""
    record = normalize(raw)
    record.setdefault("status", "unverified")
    if not record.get("title") or not record.get("type"):
        return None, "title and type are required"
    errors = validate(record)
    if errors:
        return None, "; ".join(errors)
    if record.get("url") and any(s.get("url") == record["url"] for s in sources):
        return None, f"already registered: {record['url']}"
    dup = next((s for s in sources if title_key(s["title"]) == title_key(record["title"])
                and (s.get("author") or "")[:6].lower() == (record.get("author") or "")[:6].lower()
                and s["type"] == record["type"]), None)
    if dup:
        return None, f"possible duplicate of [{dup['id']}] {dup['title']}"
    taken = {s["id"] for s in sources}
    if record.get("id") and record["id"] in taken:
        return None, f"ID already used: {record['id']}"
    record["id"] = record.get("id") or make_id(record.get("author"), record.get("year"), record["title"], taken)
    record["added"] = date.today().isoformat()
    sources.append(record)
    return record, None


def source_fields(args):
    return {"title": args.title, "type": args.type, "author": args.author, "year": args.year,
            "publisher": args.publisher, "url": args.url, "doi": args.doi, "reliability": args.reliability,
            "status": args.status, "facets": args.facets, "lens": args.lens, "field": args.field,
            "lang": args.lang, "license": args.license, "no_url_reason": args.no_url_reason,
            "accessed": args.accessed, "notes": args.notes, "id": getattr(args, "id", None)}


def cmd_init(args):
    project = Path(args.project)
    for sub in PROJECT_DIRS:
        (project / sub).mkdir(parents=True, exist_ok=True)
    for keep in ("library/raw/.gitkeep", "library/extracted/.gitkeep"):
        (project / keep).touch()
    (project / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
    registry_path(project).touch()
    scope = project / "00-scope.md"
    if not scope.exists():
        lens_rows = "\n".join(f"| {k} | {v} | | |" for k, v in LENSES.items())
        scope.write_text(
            f"# Scope: {args.title}\n\n"
            f"- **Request:** {args.request or ''}\n"
            f"- **Purpose:** {args.purpose or ''}\n"
            "- **Audience:** \n- **Depth:** \n- **Languages / regions:** \n- **Out of scope:** \n"
            f"- **Started:** {date.today().isoformat()}\n\n"
            "This file is a working document: edit or rewrite any part of it freely.\n\n"
            "## Facets\n\n| Facet | Key questions | Chapter | Status |\n|---|---|---|---|\n\n"
            "## Fields\n\nDisciplines and domains that have something to say about this topic "
            "(e.g. microbiology, food history, economics, law, psychology, design):\n\n- \n\n"
            "## Lenses\n\n| Lens | What it means | Where to look for this topic | Covered |\n|---|---|---|---|\n"
            f"{lens_rows}\n\n"
            "## Diversity exceptions\n\nWhen a diversity warning from `check` doesn't fit this topic, "
            "explain it here as `- <key>: <reason>` and the warning is downgraded to a note. Keys: "
            f"{', '.join(EXCEPTION_KEYS)}. Example: `- decades: home batteries are a post-2010 technology`.\n\n"
            "## Search log\n\n| Query / place searched | New sources | Notes |\n|---|---|---|\n",
            encoding="utf-8",
        )
    print(f"Initialized {project}/ (00-scope.md, sources.jsonl, compendium/, workbench/, library/)")


def cmd_add(args):
    sources = load_sources(args.project)
    if args.from_jsonl and args.id:
        sys.exit("--id can't be combined with --from-jsonl; put \"id\" in the JSONL line, or rename afterwards")
    if args.from_jsonl:
        text = sys.stdin.read() if args.from_jsonl == "-" else Path(args.from_jsonl).read_text(encoding="utf-8")
        picks = set(as_list(args.pick) or [])
        # --lens/--field/... given with --from-jsonl are defaults for records that lack them
        defaults = {k: v for k, v in normalize({k: v for k, v in source_fields(args).items()
                                                  if k not in ("id", "title", "type")}).items()}
        added, failures = 0, []
        for n, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                failures.append(f"line {n}: invalid JSON ({exc})")
                continue
            if picks and raw.get("cand") not in picks:
                continue
            raw.pop("cand", None)
            for key, value in defaults.items():
                raw.setdefault(key, value)
            record, error = insert_source(sources, raw)
            if error:
                failures.append(f"line {n}: skipped: {error}")
            else:
                print(f"[{record['id']}] {record['title']}")
                added += 1
        save_sources(args.project, sources)
        for f in failures:
            print(f)
        print(f"{added} added, {len(failures)} skipped")
        if failures and (added == 0 or len(failures) > added):
            reasons = Counter(re.sub(r"line \d+: (skipped: )?", "", f).split(":")[0] for f in failures)
            sys.exit("MOST LINES FAILED. Reasons: " + "; ".join(f"{r} ×{n}" for r, n in reasons.most_common(5)))
        return
    if not args.title or not args.type:
        sys.exit("add needs --title and --type (or --from-jsonl FILE)")
    record, error = insert_source(sources, source_fields(args))
    if error:
        sys.exit(error)
    save_sources(args.project, sources)
    print(f"[{record['id']}] {record['title']}")


def cmd_update(args):
    sources = load_sources(args.project)
    target = next((s for s in sources if s["id"] == args.source_id), None)
    if not target:
        sys.exit(f"No source with id {args.source_id}")
    raw = {k: v for k, v in source_fields(args).items() if k != "id"}
    for key in LIST_FIELDS:  # "+x,y" appends, "-x" removes, plain value replaces
        value = raw.get(key)
        if value and value[0] in "+-":
            items = as_list(value[1:])
            current = list(target.get(key, []))
            current = current + [i for i in items if i not in current] if value[0] == "+" else \
                [c for c in current if c not in items]
            raw[key] = current
            if not current:
                target.pop(key, None)
    changes = normalize(raw)
    target.update(changes)
    errors = validate(target)
    if errors:
        sys.exit("; ".join(errors))
    save_sources(args.project, sources)
    print(f"[{target['id']}] updated: {', '.join(changes) or 'nothing'}")


def cmd_delete(args):
    sources = load_sources(args.project)
    doomed = set(as_list(args.ids))
    missing = doomed - {s["id"] for s in sources}
    if missing:
        sys.exit(f"No such id(s): {', '.join(sorted(missing))}")
    still_cited = [i for i in doomed if cited_ids(args.project).get(i)]
    if still_cited and not args.force:
        sys.exit(f"Still cited in the project: {', '.join(still_cited)} (remove the citations or use --force)")
    save_sources(args.project, [s for s in sources if s["id"] not in doomed])
    print(f"Deleted {len(doomed)} source(s): {', '.join(sorted(doomed))}")


def cmd_rename(args):
    sources = load_sources(args.project)
    if any(s["id"] == args.new for s in sources):
        sys.exit(f"ID already used: {args.new}")
    target = next((s for s in sources if s["id"] == args.old), None)
    if not target:
        sys.exit(f"No source with id {args.old}")
    target["id"] = args.new
    save_sources(args.project, sources)
    pattern = re.compile(rf"@{re.escape(args.old)}(?![A-Za-z0-9_-])")
    changed = 0
    for md in Path(args.project).rglob("*.md"):
        if "library" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        new_text = pattern.sub(f"@{args.new}", text)
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
            changed += 1
    print(f"Renamed {args.old} -> {args.new}; citations rewritten in {changed} file(s)")


def cmd_sources(args):
    for s in load_sources(args.project):
        if args.type and s["type"] != args.type:
            continue
        if args.facet and args.facet not in s.get("facets", []):
            continue
        if args.lens and args.lens not in s.get("lens", []):
            continue
        if args.status and s.get("status", "unverified") != args.status:
            continue
        lens = ",".join(s.get("lens", [])) or "-"
        print(f"[{s['id']}] {s['type']:<12} r{s.get('reliability', '?')} {s.get('status', 'unverified'):<10} "
              f"{lens:<22} {s['title']}")


def cmd_log(args):
    scope = Path(args.project) / "00-scope.md"
    text = scope.read_text(encoding="utf-8")
    entries = []
    if args.from_tsv:
        lines_in = sys.stdin.read() if args.from_tsv == "-" else Path(args.from_tsv).read_text(encoding="utf-8")
        for line in lines_in.splitlines():
            if line.strip():
                cells = (line.split("\t") + ["", ""])[:3]
                entries.append(cells)
    if args.query:
        entries.append([args.query, "" if args.found is None else str(args.found), args.notes or ""])
    if not entries:
        sys.exit("log needs QUERY or --from-tsv FILE (query<TAB>found<TAB>notes per line)")
    row = "\n".join(f"| {q.replace('|', '/')} | {f} | {n.replace('|', '/')} |" for q, f, n in entries)
    if "## Search log" not in text:
        text += "\n## Search log\n\n| Query / place searched | New sources | Notes |\n|---|---|---|\n"
    head, tail = text.split("## Search log", 1)
    section, sep, rest = tail.partition("\n## ")  # only touch the search-log section
    lines = section.rstrip("\n").split("\n")
    last_table = max((i for i, line in enumerate(lines) if line.startswith("|")), default=len(lines) - 1)
    lines.insert(last_table + 1, row)
    section = "\n".join(lines) + ("\n\n" if sep else "\n")
    scope.write_text(head + "## Search log" + section + (sep.lstrip("\n") + rest if sep else ""), encoding="utf-8")
    print(f"logged {len(entries)} row(s)")


# ------------------------------------------------------------------ verify

def fetch_json(url, timeout=20, retries=3):
    """GET JSON, retrying politely on rate limits (429) and transient 5xx errors."""
    import time
    import urllib.error
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 502, 503, 504) or attempt == retries:
                raise
            wait = int(exc.headers.get("Retry-After") or 0) or 2 ** (attempt + 1)
            time.sleep(min(wait, 20))


def words(text):
    return set(re.findall(r"[a-z0-9]{3,}", slug(text).replace("-", " ")))


def format_authors(names):
    names = [n.strip().strip(",") for n in names if n and n.strip().strip(",")]
    if not names:
        return None
    if len(names) > 3:
        return f"{names[0]} et al."
    return " & ".join(names)


def title_match(a, b):
    wa, wb = words(a), words(b)
    if not wa or not wb:
        return False
    return len(wa & wb) / min(len(wa), len(wb)) >= 0.7


def verify_paper(s):
    if s.get("doi"):
        data = fetch_json("https://api.crossref.org/works/" + urllib.parse.quote(s["doi"]))["message"]
        items = [data]
    else:
        query = urllib.parse.urlencode({"query.bibliographic": f"{s['title']} {s.get('author', '')}", "rows": 3})
        items = fetch_json("https://api.crossref.org/works?" + query)["message"]["items"]
    for item in items:
        title = (item.get("title") or [""])[0]
        if title_match(title, s["title"]):
            year = (item.get("issued", {}).get("date-parts") or [[None]])[0][0]
            journal = (item.get("container-title") or [""])[0]
            detail = {"doi": item.get("DOI"), "year": str(year) if year else None,
                      "author": format_authors([f"{a.get('family', '')}, {a.get('given', '')[:1]}." if a.get("given")
                                                else a.get("family", "") for a in item.get("author", [])])}
            if journal:
                vol = "".join(filter(None, [item.get("volume"), f"({item['issue']})" if item.get("issue") else None]))
                pages = item.get("page")
                detail["publisher"] = f"{journal} {vol}{':' + pages if pages else ''}".strip()
            if item.get("DOI"):
                detail["url"] = "https://doi.org/" + item["DOI"]
            return "crossref", detail
    return None, None


def main_title(title):
    return re.split(r"\s*[:–—]\s+|\s+-\s+|\. ", title, maxsplit=1)[0]


def verify_book(s):
    params = {"title": main_title(s["title"]), "limit": 8, "fields": "title,author_name,first_publish_year,publisher,key"}
    if s.get("author"):
        params["author"] = first_surname(s["author"])
    docs = fetch_json("https://openlibrary.org/search.json?" + urllib.parse.urlencode(params)).get("docs", [])
    for doc in docs:
        if title_match(doc.get("title", ""), s["title"]) or title_match(doc.get("title", ""), main_title(s["title"])):
            detail = {"year": str(doc["first_publish_year"]) if doc.get("first_publish_year") else None,
                      "author": format_authors([surname_first(a) for a in doc.get("author_name", [])])}
            if doc.get("publisher"):
                detail["publisher"] = doc["publisher"][0]
            if doc.get("key"):
                detail["url"] = "https://openlibrary.org" + doc["key"]
            return "openlibrary", detail
    return None, None


def verify_youtube(s):
    data = fetch_json("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(s["url"], safe=""))
    if data.get("title"):
        return "youtube-oembed", {"notes_append": f"channel: {data.get('author_name')}"} if data.get("author_name") else {}
    return None, None


def verify_url(s):
    request = urllib.request.Request(s["url"], headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read(200_000).decode("utf-8", errors="replace")
    match = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    page_title = html.unescape(match.group(1)).strip() if match else ""
    if title_match(page_title, s["title"]) or title_match(page_title, main_title(s["title"])):
        return "url-title", {}
    return None, {"page_title": page_title[:120]}


def cmd_verify(args):
    sources = load_sources(args.project)
    wanted = set(as_list(args.ids) or [])
    todo = [s for s in sources if (s["id"] in wanted) if wanted] if wanted else \
        [s for s in sources if s.get("status", "unverified") == "unverified"]
    if args.limit:
        todo = todo[:args.limit]
    confirmed = 0
    for s in todo:
        methods = []
        if s["type"] in ("paper", "review", "thesis", "book-chapter") or s.get("doi"):
            methods.append(verify_paper)
        if s["type"] in ("book", "primary-text"):
            methods.append(verify_book)
        if s.get("url") and re.search(r"youtube\.com|youtu\.be", s["url"]):
            methods.append(verify_youtube)
        if s.get("url"):
            methods.append(verify_url)
        result, info = None, None
        for method in methods:
            try:
                result, info = method(s)
            except Exception as exc:  # network errors, 403s, bad JSON: try the next method
                info = {"error": str(exc)[:80]}
                continue
            if result:
                break
        if not result:
            print(f"[{s['id']}] not confirmed {info or ''}")
            continue
        confirmed += 1
        filled = []
        for key, value in (info or {}).items():
            if key == "notes_append":
                continue
            if value and not s.get(key):
                s[key] = value
                filled.append(key)
        if (info or {}).get("year") and s.get("year") and s["year"][:4] != info["year"]:
            print(f"[{s['id']}] note: registry year {s['year']} vs {result} {info['year']}")
        if s.get("status", "unverified") == "unverified":
            s["status"] = "confirmed"
        s["verified_by"] = result
        print(f"[{s['id']}] confirmed via {result}" + (f", filled {', '.join(filled)}" if filled else ""))
    if not args.dry_run:
        save_sources(args.project, sources)
    print(f"{confirmed}/{len(todo)} confirmed" + (" (dry run, nothing saved)" if args.dry_run else ""))


# ---------------------------------------------------- discover / abstract

PIRATE_HOSTS = re.compile(r"dokumen\.pub|vdoc\.pub|ebin\.pub|epdf\.pub|pdfdrive|z-?lib|zlibrary|libgen|"
                          r"library\.lol|annas-archive|b-ok\.|1lib\.|pdfcoffee|dokumen\.tips|sci-hub", re.I)
PIRACY = re.compile(r"z-?lib|libgen|anna'?s[-_ ]?archive|pdfdrive|b-ok\.|1lib", re.I)


def epmc_authors(author_string):
    """'Watters SA, Smith B, Jones C.' -> 'Watters, S. et al.' style."""
    names = []
    for part in (author_string or "").rstrip(".").split(","):
        bits = part.strip().split()
        if not bits:
            continue
        if len(bits) > 1 and INITIAL.fullmatch(bits[-1]):
            names.append(f"{' '.join(bits[:-1])}, {bits[-1][0]}.")
        else:
            names.append(part.strip())
    return format_authors(names)


def crossref_authors(item):
    return format_authors([f"{a.get('family', '')}, {a['given'][0]}." if a.get("given") else a.get("family", "")
                           for a in item.get("author", [])])


def discover_openlibrary(query, rows, lang, sort):
    params = {"q": query, "limit": rows, "fields": "title,author_name,first_publish_year,publisher,key,language"}
    if lang:
        params["language"] = lang3(lang)
    for d in fetch_json("https://openlibrary.org/search.json?" + urllib.parse.urlencode(params)).get("docs", []):
        yield {"type": "book", "title": d.get("title"),
               "author": format_authors([surname_first(a) for a in d.get("author_name") or []]),
               "year": d.get("first_publish_year"), "publisher": (d.get("publisher") or [None])[0],
               "url": "https://openlibrary.org" + d["key"], "lang": lang2((d.get("language") or [lang or ""])[0])}


def discover_europepmc(query, rows, lang, sort):
    params = {"query": f"TITLE_ABS:({query})" if sort == "cited" else query, "format": "json",
              "pageSize": rows, "resultType": "lite"}
    if sort == "cited":
        params["sort"] = "CITED desc"
    for r in fetch_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params))["resultList"]["result"]:
        kind = "review" if "review" in (r.get("pubType") or "").lower() else "paper"
        yield {"type": kind, "title": re.sub(r"<[^>]+>", "", html.unescape(r.get("title", ""))).rstrip("."),
               "author": epmc_authors(r.get("authorString")), "year": r.get("pubYear"),
               "publisher": r.get("journalTitle"), "doi": r.get("doi"),
               "url": f"https://doi.org/{r['doi']}" if r.get("doi") else f"https://europepmc.org/article/{r.get('source')}/{r.get('id')}",
               "notes": f"cited by {r.get('citedByCount', 0)}"}


def discover_crossref(query, rows, lang, sort):
    # Crossref's own citation sort ignores relevance (returns famous unrelated papers), so for
    # --sort cited take a wider relevance-ranked set and order that by citations.
    params = {"query.bibliographic": query, "rows": rows * 4 if sort == "cited" else rows}
    items = fetch_json("https://api.crossref.org/works?" + urllib.parse.urlencode(params))["message"]["items"]
    if sort == "cited":
        items = sorted(items, key=lambda i: -(i.get("is-referenced-by-count") or 0))[:rows]
    for item in items:
        if item.get("type") in ("component", "peer-review", "grant"):
            continue
        kind = {"book": "book", "monograph": "book", "edited-book": "book", "book-chapter": "book-chapter",
                "dissertation": "thesis", "dataset": "dataset", "standard": "standard",
                "report": "official-doc"}.get(item.get("type"), "paper")
        year = (item.get("issued", {}).get("date-parts") or [[None]])[0][0]
        yield {"type": kind, "title": re.sub(r"<[^>]+>", "", (item.get("title") or [""])[0]),
               "author": crossref_authors(item), "year": year,
               "publisher": (item.get("container-title") or [item.get("publisher")])[0],
               "doi": item.get("DOI"), "url": "https://doi.org/" + item["DOI"] if item.get("DOI") else None,
               "lang": lang2(item.get("language")) if item.get("language") else None,
               "notes": f"cited by {item.get('is-referenced-by-count', 0)}"}


def discover_openalex(query, rows, lang, sort):
    params = {"search": query, "per-page": rows, "mailto": "topic-compiler@example.org",
              "select": "id,doi,display_name,publication_year,type,authorships,primary_location,language,cited_by_count"}
    if sort == "cited":
        params["sort"] = "cited_by_count:desc"
    if lang:
        params["filter"] = f"language:{lang2(lang)}"
    kinds = {"book": "book", "book-chapter": "book-chapter", "dissertation": "thesis", "dataset": "dataset",
             "review": "review", "report": "official-doc", "standard": "standard"}
    for w in fetch_json("https://api.openalex.org/works?" + urllib.parse.urlencode(params))["results"]:
        venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
        authors = [surname_first(a["author"]["display_name"]) for a in w.get("authorships", []) if a.get("author")]
        doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
        yield {"type": kinds.get(w.get("type"), "paper"), "title": w.get("display_name"),
               "author": format_authors(authors), "year": w.get("publication_year"), "publisher": venue,
               "doi": doi, "url": w.get("doi") or w.get("id"), "lang": lang2(w.get("language")),
               "notes": f"cited by {w.get('cited_by_count', 0)}"}


def discover_archive(query, rows, lang, sort):
    q = f"title:({query})"
    if lang:
        q += f" AND language:({lang3(lang)} OR {lang2(lang)})"
    params = [("q", q), ("rows", rows * 2), ("output", "json")]
    params += [("fl[]", f) for f in ("identifier", "title", "creator", "year", "mediatype", "language", "collection")]
    if sort == "cited":
        params.append(("sort[]", "downloads desc"))
    kinds = {"texts": "book", "audio": "audio", "movies": "video", "data": "dataset", "image": "archive"}
    count = 0
    for d in fetch_json("https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(params))["response"]["docs"]:
        collections = d.get("collection") if isinstance(d.get("collection"), list) else [d.get("collection") or ""]
        if PIRACY.search(d["identifier"]) or any(PIRACY.search(c) for c in collections):
            continue  # pirated uploads: never register or link these
        creator = d.get("creator")
        language = d.get("language")
        user_upload = any(c.startswith("opensource") for c in collections)
        yield {"type": kinds.get(d.get("mediatype"), "archive"), "title": d.get("title"),
               "author": creator[0] if isinstance(creator, list) else creator, "year": d.get("year"),
               "url": "https://archive.org/details/" + d["identifier"], "publisher": "Internet Archive",
               "lang": lang2(language[0] if isinstance(language, list) else language) if language else None,
               "notes": "user upload: check it is legitimately shared" if user_upload else None}
        count += 1
        if count >= rows:
            break


def discover_hn(query, rows, lang, sort):
    params = {"query": query, "hitsPerPage": rows, "tags": "story"}
    for h in fetch_json("https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(params))["hits"]:
        yield {"type": "community", "title": h.get("title"), "author": h.get("author"),
               "year": (h.get("created_at") or "")[:4], "publisher": "Hacker News discussion",
               "url": f"https://news.ycombinator.com/item?id={h['objectID']}",
               "notes": f"{h.get('num_comments', 0)} comments; links to {h.get('url') or 'text post'}"}


def discover_stackexchange(query, rows, lang, sort, site="stackoverflow"):
    params = {"order": "desc", "sort": "votes", "q": query, "site": site, "pagesize": rows}
    for q in fetch_json("https://api.stackexchange.com/2.3/search/advanced?" + urllib.parse.urlencode(params))["items"]:
        yield {"type": "community", "title": html.unescape(q.get("title", "")), "publisher": f"Stack Exchange ({site})",
               "year": date.fromtimestamp(q.get("creation_date", 0)).year, "url": q.get("link"),
               "notes": f"score {q.get('score')}, {q.get('answer_count')} answers"}


CATALOGUES = {"books": discover_openlibrary, "papers": discover_europepmc, "crossref": discover_crossref,
              "openalex": discover_openalex, "archive": discover_archive, "hn": discover_hn,
              "stackexchange": discover_stackexchange}


def cmd_discover(args):
    sources = load_sources(args.project)
    known_urls = {s.get("url") for s in sources}
    known_titles = {(title_key(s["title"]), s.get("author") or "") for s in sources}
    next_cand = 1
    if args.out and Path(args.out).exists():
        for line in Path(args.out).read_text(encoding="utf-8").splitlines():
            match = re.search(r'"cand": "c(\d+)"', line)
            if match:
                next_cand = max(next_cand, int(match.group(1)) + 1)
    out = open(args.out, "a", encoding="utf-8") if args.out else None
    total = 0
    for name in as_list(args.catalogues):
        func = CATALOGUES.get(name)
        if not func:
            sys.exit(f"unknown catalogue {name} (use: {', '.join(CATALOGUES)})")
        try:
            kwargs = {"site": args.se_site} if name == "stackexchange" else {}
            results = list(func(args.query, args.rows, args.lang, args.sort, **kwargs))
        except Exception as exc:
            print(f"# {name}: failed ({str(exc)[:80]})")
            continue
        print(f"# {name}: {len(results)} result(s)")
        for r in results:
            if not r.get("title"):
                continue
            r["title"] = re.sub(r"\s+", " ", str(r["title"])).strip()
            new = r.get("url") not in known_urls and not any(
                title_key(r["title"]) == tk and (not ra or not r.get("author") or ra[:5].lower() == str(r["author"])[:5].lower())
                for tk, ra in known_titles)
            r = {k: v for k, v in r.items() if v not in (None, "", [])}
            r.update({"status": "confirmed", "verified_by": name})
            if new:
                r = {"cand": f"c{next_cand}", **r}
                next_cand += 1
            print(("  NEW " if new else "  had ") + json.dumps(r, ensure_ascii=False))
            if new and out:
                out.write(json.dumps(r, ensure_ascii=False) + "\n")
                total += 1
    if out:
        out.close()
        print(f"{total} new candidate(s) appended to {args.out}. Pick the relevant ones and add them with shared tags, e.g.:\n"
              f"  add {args.project} --from-jsonl {args.out} --pick c1,c4,c7 --lens scholarly --field X "
              f"--facets Y --reliability 4")


def abstract_europepmc(s):
    query = f'DOI:"{s["doi"]}"' if s.get("doi") else f'TITLE:"{s["title"]}"'
    params = {"query": query, "format": "json", "resultType": "core", "pageSize": 1}
    results = fetch_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params))["resultList"]["result"]
    if results and results[0].get("abstractText") and title_match(results[0].get("title", ""), s["title"]):
        r = results[0]
        extra = f"Open access full text: https://europepmc.org/article/PMC/{r['pmcid']}" \
            if r.get("isOpenAccess") == "Y" and r.get("pmcid") else ""
        return r.get("doi"), r["abstractText"], extra
    return None


def abstract_crossref(s):
    if s.get("doi"):
        item = fetch_json("https://api.crossref.org/works/" + urllib.parse.quote(s["doi"]))["message"]
    else:
        items = fetch_json("https://api.crossref.org/works?" + urllib.parse.urlencode(
            {"query.bibliographic": s["title"], "rows": 3}))["message"]["items"]
        item = next((i for i in items if title_match((i.get("title") or [""])[0], s["title"])), None)
    if item and item.get("abstract"):
        return item.get("DOI"), item["abstract"], ""
    return None


def abstract_openalex(s):
    if s.get("doi"):
        work = fetch_json("https://api.openalex.org/works/doi:" + urllib.parse.quote(s["doi"]) + "?mailto=topic-compiler@example.org")
    else:
        results = fetch_json("https://api.openalex.org/works?" + urllib.parse.urlencode(
            {"search": s["title"], "per-page": 3, "mailto": "topic-compiler@example.org"}))["results"]
        work = next((w for w in results if title_match(w.get("display_name", ""), s["title"])), None)
    index = (work or {}).get("abstract_inverted_index")
    if not index:
        return None
    positions = sorted((pos, word) for word, poss in index.items() for pos in poss)
    doi = (work.get("doi") or "").replace("https://doi.org/", "") or None
    return doi, " ".join(word for _, word in positions), ""


BOILERPLATE = re.compile(r"cookie|log ?in|sign ?in|subscribe|access options|purchase|javascript|"
                         r"all rights reserved|this (article|chapter|book) (is|was) published|no abstract", re.I)


def plausible_abstract(text):
    text = re.sub(r"<[^>]+>", " ", text or "").strip()
    return len(text) >= 200 and len(BOILERPLATE.findall(text[:600])) == 0


def cmd_abstract(args):
    sources = load_sources(args.project)
    s = next((x for x in sources if x["id"] == args.source_id), None)
    if not s:
        sys.exit(f"No source with id {args.source_id}")
    found, via = None, None
    for name, func in (("europepmc", abstract_europepmc), ("crossref", abstract_crossref), ("openalex", abstract_openalex)):
        try:
            found = func(s)
        except Exception as exc:
            print(f"# {name}: failed ({str(exc)[:60]})")
            continue
        if found and plausible_abstract(found[1]):
            via = name
            break
        if found:
            print(f"# {name}: returned text that doesn't look like an abstract (too short or boilerplate); skipped")
            found = None
    if not found:
        sys.exit("No abstract found (Europe PMC, Crossref, OpenAlex). Try the publisher page or an open-access copy.")
    doi, text, extra = found
    body = html.unescape(re.sub(r"<[^>]+>", " ", text)).strip()
    print(f"{s['title']}  [abstract via {via}]\n")
    print(body[:args.max_chars] + (" [...]" if len(body) > args.max_chars else ""))
    if extra:
        print("\n" + extra)
    if args.mark_read:
        s["status"] = "seen"
        s["verified_by"] = f"{via}-abstract"
        if "abstract" not in (s.get("notes") or ""):
            s["notes"] = ((s.get("notes") or "") + " [read: abstract only]").strip()
        if not s.get("doi") and doi:
            s["doi"] = doi
        save_sources(args.project, sources)
        print(f"\n[{s['id']}] marked seen (abstract only)")


def cmd_pdf(args):
    """Download a PDF (or read a local one) and print its text, since web fetch tools often can't."""
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("needs pypdf: pip install pypdf  (if that fails: pip install cffi pypdf)")
    import io
    import logging
    logging.getLogger("pypdf").setLevel(logging.ERROR)  # silence font/encoding warnings
    if re.match(r"https?://", args.source):
        request = urllib.request.Request(args.source, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read()
        except Exception as exc:
            sys.exit(f"Could not download: {str(exc)[:120]}")
    else:
        data = Path(args.source).read_bytes()
    if not data.lstrip()[:5].startswith(b"%PDF"):
        head = data[:300].decode("utf-8", errors="replace")
        kind = "an HTML page (paywall, cookie wall or landing page?)" if "<html" in head.lower() else "not a PDF"
        sys.exit(f"The response is {kind}; fetch it as a web page instead, or find a direct PDF link.")
    try:
        reader = PdfReader(io.BytesIO(data))
    except Exception as exc:
        sys.exit(f"Unreadable PDF: {str(exc)[:120]}")
    first, _, last = (args.pages or f"1-{len(reader.pages)}").partition("-")
    first, last = int(first), int(last or first)
    pattern = re.compile(args.grep, re.I) if args.grep else None  # a regular expression, e.g. "distance|abstand"
    print(f"# {len(reader.pages)} pages; showing {first}-{min(last, len(reader.pages))}")
    for number in range(first, min(last, len(reader.pages)) + 1):
        text = clean(reader.pages[number - 1].extract_text() or "")
        if pattern:
            for match in pattern.finditer(text):
                snippet = text[max(0, match.start() - 200):match.end() + 200].replace("\n", " ")
                print(f"[p. {number}] ...{snippet}...\n")
        else:
            print(f"\n--- p. {number} ---\n{text}")


# ------------------------------------------------------- stats and checks

def decade(year):
    match = re.search(r"-?\d{3,4}", str(year or ""))
    if not match:
        return None
    y = int(match.group())
    if y < 1900:
        return "pre-1900"
    return f"{y // 10 * 10}s"


def scope_lines(project, heading):
    """Bullet lines under '## <heading>' in 00-scope.md, markdown stripped."""
    scope = Path(project) / "00-scope.md"
    if not scope.exists():
        return []
    text = scope.read_text(encoding="utf-8")
    if f"## {heading}" not in text:
        return []
    section = text.split(f"## {heading}", 1)[1].split("\n## ", 1)[0]
    lines = []
    for line in section.splitlines():
        match = re.match(r"\s*[-*]\s+(.+)", line)
        if match:
            clean_line = re.sub(r"[*`_]", "", match.group(1)).strip()
            if clean_line:
                lines.append(clean_line)
    return lines


def tag_matches_line(tag, line):
    """Loose match: 'food-chemistry' matches 'Food chemistry / cereal science: ...'."""
    tag_slug, line_slug = slug(tag), slug(line)
    if tag_slug and tag_slug in line_slug:
        return True
    tag_words = {w for w in tag_slug.split("-") if len(w) >= 5}
    return bool(tag_words & set(line_slug.split("-")))


def scope_facets(project):
    scope = Path(project) / "00-scope.md"
    if not scope.exists():
        return set()
    section = scope.read_text(encoding="utf-8").split("## Facets", 1)[-1].split("\n## ", 1)[0]
    names = set()
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and cells and cells[0] and not set(cells[0]) <= set("-: ") and cells[0].lower() != "facet":
            names.add(slug(cells[0]))
    return names


EXCEPTION_KEYS = ["lenses", "types", "fields", "languages", "decades", "read", "unverified", "dominant-lens"]


def diversity_exceptions(project):
    """Keys explained under '## Diversity exceptions' in 00-scope.md, as {key: reason}."""
    scope = Path(project) / "00-scope.md"
    if not scope.exists() or "## Diversity exceptions" not in scope.read_text(encoding="utf-8"):
        return {}
    section = scope.read_text(encoding="utf-8").split("## Diversity exceptions", 1)[1].split("\n## ", 1)[0]
    found = {}
    for key, reason in re.findall(r"^\s*[-*]\s*`?([a-z-]+)`?\s*:\s*(.+)$", section, re.M):
        if key in EXCEPTION_KEYS and reason.strip():
            found[key] = reason.strip()
    return found


def diversity_warnings(sources):
    """List of (key, message) diversity warnings."""
    warnings = []
    n = len(sources)
    if n == 0:
        return [("types", "no sources yet")]
    lenses = Counter(l for s in sources for l in s.get("lens", []))
    types = Counter(s["type"] for s in sources)
    fields = Counter(f for s in sources for f in s.get("field", []))
    langs = Counter(lang2(s.get("lang", "en")) for s in sources)
    decades = Counter(d for d in (decade(s.get("year")) for s in sources) if d)
    missing_lens = [l for l in LENSES if l not in lenses]
    untagged = sum(1 for s in sources if not s.get("lens"))
    if untagged:
        warnings.append(("lenses", f"{untagged} source(s) have no --lens"))
    if len(lenses) < 7:
        warnings.append(("lenses", f"only {len(lenses)}/10 lenses covered; missing: {', '.join(missing_lens)}"))
    if lenses and lenses.most_common(1)[0][1] > 0.5 * n:
        top = lenses.most_common(1)[0]
        warnings.append(("dominant-lens", f"lens '{top[0]}' dominates ({top[1]}/{n} sources)"))
    if len(types) < 8:
        warnings.append(("types", f"only {len(types)} source types used"))
    if len(fields) < 4:
        warnings.append(("fields", f"only {len(fields)} field(s)/disciplines tagged; aim for 4+"))
    if len(langs) < 2:
        warnings.append(("languages", f"all sources in one language ({next(iter(langs))}); add others if the topic has them"))
    if len(decades) < 3:
        warnings.append(("decades", f"sources span only {len(decades)} decade(s); add classic or recent work, "
                                    "or explain in the scope that the field is young"))
    unverified = sum(1 for s in sources if s.get("status", "unverified") == "unverified")
    if unverified > 0.3 * n:
        warnings.append(("unverified", f"{unverified}/{n} sources unverified; run verify, then open the key ones"))
    seen = sum(1 for s in sources if s.get("status") == "seen")
    if seen < 0.2 * n:
        warnings.append(("read", f"only {seen}/{n} sources read (status seen); make sure every load-bearing "
                                 "source is read"))
    return warnings


def split_warnings(project, sources):
    """Diversity warnings minus those the scope explains; returns (warnings, excused notes)."""
    excused = diversity_exceptions(project)
    active, notes = [], []
    for key, message in diversity_warnings(sources):
        if key in excused:
            notes.append(f"{message} (excepted: {excused[key]})")
        else:
            active.append(message)
    return active, notes


def cmd_stats(args):
    sources = load_sources(args.project)
    print(f"{len(sources)} sources")
    counters = [
        ("type", Counter(s["type"] for s in sources)),
        ("lens", Counter(l for s in sources for l in s.get("lens", []))),
        ("field", Counter(f for s in sources for f in s.get("field", []))),
        ("facet", Counter(f for s in sources for f in s.get("facets", []))),
        ("language", Counter(lang2(s.get("lang", "en")) for s in sources)),
        ("decade", Counter(decade(s.get("year")) or "undated" for s in sources)),
        ("reliability", Counter(str(s.get("reliability", "?")) for s in sources)),
        ("status", Counter(s.get("status", "unverified") for s in sources)),
    ]
    for label, counter in counters:
        print(f"\nby {label}:")
        for key, n in sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0]))):
            print(f"  {str(key):<22} {n}")
    facet_lens = defaultdict(Counter)
    for s in sources:
        for f in s.get("facets", []):
            for l in s.get("lens", []):
                facet_lens[f][l] += 1
    if facet_lens:
        print("\nlenses per facet (facets with < 3 lenses are one-sided):")
        for f, lc in sorted(facet_lens.items(), key=lambda kv: len(kv[1])):
            print(f"  {f:<22} {len(lc)} lens(es): {', '.join(sorted(lc))}")
    print(f"\nlenses not yet covered: {', '.join(l for l in LENSES if l not in counters[1][1]) or 'none'}")
    print(f"types not yet represented: {', '.join(t for t in SOURCE_TYPES if t not in counters[0][1])}")
    active, excused = split_warnings(args.project, sources)
    print("\ndiversity warnings:")
    for w in active or ["none"]:
        print("  -", w)
    for note in excused:
        print("  - note:", note)


def cited_ids(project):
    cited = Counter()
    for md in Path(project).rglob("*.md"):
        if md.name == "99-bibliography.md" or "library" in md.parts:
            continue
        # ignore code spans and blocks, where [@id] appears as an example
        text = re.sub(r"```.*?```|`[^`\n]*`", "", md.read_text(encoding="utf-8"), flags=re.S)
        for group in re.findall(r"\[(@[^\]]+)\]", text):
            for ref in re.findall(r"@([A-Za-z0-9_-]+)", group):
                cited[ref] += 1
    return cited


def cmd_check(args):
    sources = load_sources(args.project)
    ids = Counter(s["id"] for s in sources)
    urls = Counter(s["url"] for s in sources if s.get("url"))
    problems, warnings = [], []
    problems += [f"duplicate id: {i}" for i, n in ids.items() if n > 1]
    problems += [f"duplicate url: {u}" for u, n in urls.items() if n > 1]
    titles = Counter((slug(s["title"]), (s.get("author") or "")[:6].lower()) for s in sources)
    problems += [f"duplicate title: {t[0]}" for t, n in titles.items() if n > 1]
    for s in sources:
        problems += [f"[{s['id']}] {e}" for e in validate(s)]
        if not s.get("url") and s["type"] not in NO_URL_OK and not s.get("no_url_reason"):
            problems.append(f"[{s['id']}] no url (add one, or --no-url-reason if none exists)")
        if "reliability" not in s:
            problems.append(f"[{s['id']}] no reliability rating")
        if s.get("url") and PIRATE_HOSTS.search(s["url"]):
            problems.append(f"[{s['id']}] links to a pirate host ({s['url'][:50]}); use a publisher, catalogue or library record")
    cited = cited_ids(args.project)
    problems += [f"cited but not registered: @{c}" for c in cited if c not in ids]
    unused = [i for i in ids if i not in cited]
    notes = []
    if unused:
        notes.append(f"{len(unused)} source(s) not cited in the text (fine: they appear in the bibliography "
                     f"as further reading): {', '.join(unused[:15])}" + (" ..." if len(unused) > 15 else ""))
    known = scope_facets(args.project)
    if known:
        stray = sorted({f for s in sources for f in s.get("facets", []) if slug(f) not in known
                        and not any(slug(f) in k or k in slug(f) for k in known)})
        if stray:
            warnings.append(f"facets not in 00-scope.md table: {', '.join(stray)}")
    scope_fields = scope_lines(args.project, "Fields")
    if scope_fields:
        tags = {f for s in sources for f in s.get("field", [])}
        stray = sorted(tag for tag in tags if not any(tag_matches_line(tag, line) for line in scope_fields))
        if stray:
            notes.append(f"field tags not matching any line under ## Fields in 00-scope.md: {', '.join(stray[:20])}")
        thin = []
        for line in scope_fields:
            n = sum(1 for s in sources if any(tag_matches_line(f, line) for f in s.get("field", [])))
            if n < 3:
                thin.append(f"{line.split(':')[0][:50]} ({n})")
        if thin:
            warnings.append(f"scope fields with fewer than 3 sources: {'; '.join(thin)}")
    no_lang = sum(1 for s in sources if not s.get("lang"))
    if no_lang:
        notes.append(f"{no_lang} source(s) have no --lang (counted as en)")
    active, excused = split_warnings(args.project, sources)
    warnings += active
    notes += excused
    for p in problems:
        print("PROBLEM", p)
    for w in warnings:
        print("WARN   ", w)
    for note in notes:
        print("note   ", note)
    print(f"{len(sources)} sources, {len(problems)} problem(s), {len(warnings)} warning(s)")
    sys.exit(1 if problems or (args.strict and warnings) else 0)


def cmd_bib(args):
    sources = load_sources(args.project)
    cited = cited_ids(args.project)
    lines = ["# Bibliography", "",
             "Generated from `sources.jsonl`. Reliability r1 (weak) – r5 (authoritative). "
             "Status: *read* = opened and read during compilation; *confirmed* = existence and details "
             "checked against a catalogue or the source's own page; *unverified* = not checked, verify "
             "before relying on it.", ""]
    by_type = defaultdict(list)
    for s in sources:
        by_type[s["type"]].append(s)
    for kind in SOURCE_TYPES:
        if kind not in by_type:
            continue
        lines += [f"## {HEADINGS.get(kind, kind.replace('-', ' ').capitalize() + 's')}", ""]
        for s in sorted(by_type[kind], key=lambda s: (s.get("author") or s["title"]).lower()):
            parts = [f"**[@{s['id']}]**"]
            if s.get("author"):
                parts.append(s["author"].rstrip(".") + ".")
            parts.append(f"*{s['title']}*" + ("" if s["title"].endswith((".", "?", "!")) else "."))
            if s.get("publisher"):
                parts.append(s["publisher"].rstrip(".") + ".")
            if s.get("year"):
                parts.append(f"{s['year']}.")
            if s.get("url"):
                parts.append(f"<{s['url']}>")
            status = {"seen": "read", "confirmed": "confirmed"}.get(s.get("status"), "*unverified*")
            tags = [f"r{s.get('reliability', '?')}", status]
            if s.get("lens"):
                tags.append("/".join(s["lens"]))
            if s.get("lang") and s["lang"] != "en":
                tags.append(s["lang"])
            if s.get("license"):
                tags.append(s["license"])
            if cited.get(s["id"]):
                tags.append(f"cited ×{cited[s['id']]}")
            parts.append(f"({', '.join(tags)})")
            if s.get("notes"):
                parts.append(f"— {s['notes']}")
            lines.append("- " + " ".join(parts))
        lines.append("")
    target = Path(args.project) / "compendium" / "99-bibliography.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {target} ({len(sources)} sources)")


# ------------------------------------------------------------------ ingest

def clean(text):
    text = re.sub(r"-\n(\w)", r"\1", text)  # rejoin hyphenated line breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("PDF support needs pypdf: pip install pypdf  (if that fails: pip install cffi pypdf)")
    for number, page in enumerate(PdfReader(str(path)).pages, start=1):
        yield f"p. {number}", clean(page.extract_text() or "")


def html_to_text(markup):
    markup = re.sub(r"(?is)<(script|style).*?</\1>", "", markup)
    markup = re.sub(r"(?i)<br\s*/?>|</(p|div|h[1-6]|li)>", "\n", markup)
    return clean(html.unescape(re.sub(r"<[^>]+>", "", markup)))


def extract_epub(path):
    with zipfile.ZipFile(path) as book:
        container = ElementTree.fromstring(book.read("META-INF/container.xml"))
        opf_path = container.find(".//{*}rootfile").get("full-path")
        opf = ElementTree.fromstring(book.read(opf_path))
        base = opf_path.rsplit("/", 1)[0] + "/" if "/" in opf_path else ""
        manifest = {item.get("id"): item.get("href") for item in opf.find("{*}manifest")}
        for number, ref in enumerate(opf.find("{*}spine"), start=1):
            href = manifest.get(ref.get("idref"))
            try:
                yield f"ch. {number}", html_to_text(book.read(base + href).decode("utf-8", errors="replace"))
            except (KeyError, TypeError):
                continue


def extract_html(path):
    yield "page", html_to_text(path.read_text(encoding="utf-8", errors="replace"))


def extract_text(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    for number, block in enumerate(re.split(r"\n\s*\n\s*\n", text), start=1):
        yield f"part {number}", clean(block)


EXTRACTORS = {".pdf": extract_pdf, ".epub": extract_epub, ".html": extract_html, ".htm": extract_html,
              ".txt": extract_text, ".md": extract_text, ".srt": extract_text, ".vtt": extract_text}


def cmd_ingest(args):
    raw = Path(args.project) / "library" / "raw"
    out = Path(args.project) / "library" / "extracted"
    out.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in raw.iterdir() if p.suffix.lower() in EXTRACTORS) if raw.exists() else []
    if not files:
        print(f"No files in {raw}/ (supported: {', '.join(EXTRACTORS)})")
        return
    for path in files:
        target = out / f"{path.name}.jsonl"
        count = 0
        with target.open("w", encoding="utf-8") as sink:
            for location, text in EXTRACTORS[path.suffix.lower()](path):
                if text:
                    sink.write(json.dumps({"file": path.name, "loc": location, "text": text}, ensure_ascii=False) + "\n")
                    count += 1
        print(f"{path.name}: {count} sections -> {target}")


def cmd_search(args):
    pattern = re.compile(re.escape(args.term), re.IGNORECASE)
    hits = 0
    for target in sorted((Path(args.project) / "library" / "extracted").glob("*.jsonl")):
        with target.open(encoding="utf-8") as lines:
            for line in lines:
                record = json.loads(line)
                for match in pattern.finditer(record["text"]):
                    start = max(0, match.start() - args.context)
                    snippet = record["text"][start:match.end() + args.context].replace("\n", " ")
                    print(f"[{record['file']}, {record['loc']}] ...{pattern.sub(lambda m: f'**{m.group(0)}**', snippet)}...\n")
                    hits += 1
    print(f"{hits} match(es) for '{args.term}'")


# -------------------------------------------------------------------- main

def add_source_options(p, required=False):
    p.add_argument("--title")
    p.add_argument("--type", choices=SOURCE_TYPES)
    p.add_argument("--author", help='"Surname, A." ; several: "Surname, A. & Surname, B." or "Surname, A. et al."')
    p.add_argument("--year")
    p.add_argument("--publisher", help="publisher, or journal with volume(issue):pages")
    p.add_argument("--url")
    p.add_argument("--doi")
    p.add_argument("--reliability", type=int, choices=range(1, 6))
    p.add_argument("--status", choices=STATUSES)
    p.add_argument("--facets", help="comma-separated facet names from 00-scope.md (update: +x appends, -x removes)")
    p.add_argument("--lens", help=f"comma-separated: {', '.join(LENSES)}")
    p.add_argument("--field", help="comma-separated disciplines/domains, e.g. microbiology,food-history")
    p.add_argument("--lang", help="ISO language code of the source, default en")
    p.add_argument("--license", help="e.g. CC BY-SA 4.0, public domain (reusable material)")
    p.add_argument("--no-url-reason", help="why no URL exists (out-of-print tape, archive item...)")
    p.add_argument("--accessed", help="date a volatile fact (price, availability) was seen, e.g. 2026-09-28")
    p.add_argument("--notes")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("project")
    p.add_argument("--title", required=True)
    p.add_argument("--purpose")
    p.add_argument("--request")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add")
    p.add_argument("project")
    add_source_options(p)
    p.add_argument("--id")
    p.add_argument("--from-jsonl", help="batch file with one JSON source per line ('-' for stdin); "
                                        "other options given act as defaults for every record")
    p.add_argument("--pick", help="with --from-jsonl: only add these candidate ids (c1,c4,...) from discover")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("update")
    p.add_argument("project")
    p.add_argument("source_id")
    add_source_options(p)
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("delete")
    p.add_argument("project")
    p.add_argument("ids", help="comma-separated source ids")
    p.add_argument("--force", action="store_true", help="delete even if still cited")
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("rename")
    p.add_argument("project")
    p.add_argument("old")
    p.add_argument("new")
    p.set_defaults(func=cmd_rename)

    p = sub.add_parser("sources")
    p.add_argument("project")
    p.add_argument("--type")
    p.add_argument("--facet")
    p.add_argument("--lens")
    p.add_argument("--status", choices=STATUSES)
    p.set_defaults(func=cmd_sources)

    p = sub.add_parser("log")
    p.add_argument("project")
    p.add_argument("query", nargs="?")
    p.add_argument("--from-tsv", help="many rows at once: query<TAB>found<TAB>notes per line ('-' for stdin)")
    p.add_argument("--found", help="how many new sources (number or short text)")
    p.add_argument("--notes")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("verify")
    p.add_argument("project")
    p.add_argument("--ids")
    p.add_argument("--limit", type=int)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("discover")
    p.add_argument("project")
    p.add_argument("query")
    p.add_argument("--catalogues", default="books,papers,archive", help=f"comma-separated: {', '.join(CATALOGUES)}")
    p.add_argument("--rows", type=int, default=10)
    p.add_argument("--sort", choices=["relevance", "cited"], default="relevance",
                   help="cited = most-cited/most-downloaded first (finds classics); searches titles/abstracts")
    p.add_argument("--lang", help="language filter for books, e.g. de, fr")
    p.add_argument("--se-site", default="stackoverflow", help="Stack Exchange site, e.g. cooking, history, fitness")
    p.add_argument("--out", help="append new candidates to this JSONL file for review and batch add")
    p.set_defaults(func=cmd_discover)

    p = sub.add_parser("abstract")
    p.add_argument("project")
    p.add_argument("source_id")
    p.add_argument("--mark-read", action="store_true", help="set status=seen (abstract only) after reading")
    p.add_argument("--max-chars", type=int, default=3000, help="truncate long abstracts (use instead of piping to head)")
    p.set_defaults(func=cmd_abstract)

    p = sub.add_parser("pdf")
    p.add_argument("source", help="PDF URL or local path")
    p.add_argument("--pages", help="e.g. 1-5")
    p.add_argument("--grep", help="only print passages matching this case-insensitive regular expression")
    p.set_defaults(func=cmd_pdf)

    p = sub.add_parser("check")
    p.add_argument("project")
    p.add_argument("--strict", action="store_true")
    p.set_defaults(func=cmd_check)

    for name, func in (("bib", cmd_bib), ("stats", cmd_stats), ("ingest", cmd_ingest)):
        p = sub.add_parser(name)
        p.add_argument("project")
        p.set_defaults(func=func)

    p = sub.add_parser("search")
    p.add_argument("project")
    p.add_argument("term")
    p.add_argument("--context", type=int, default=150)
    p.set_defaults(func=cmd_search)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
