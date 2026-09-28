#!/usr/bin/env python3
"""Project, source-registry, verification and file-ingest helper for the topic-compiler skill.

Commands (PROJECT is a directory, e.g. projects/yoga-nidra):
  init PROJECT --title T [--purpose P] [--request R]
  add PROJECT --title T --type TYPE [--author A] [--year Y] [--url U] [--publisher P]
              [--reliability 1-5] [--status seen|confirmed|unverified] [--facets f1,f2]
              [--lens L1,L2] [--field F1,F2] [--lang en] [--license L] [--no-url-reason R]
              [--notes N] [--id ID]
  add PROJECT --from-jsonl FILE     batch add (one JSON object per line, same keys as above;
                                    facets/lens/field may be lists or comma strings)
  update PROJECT ID [same options as add]   change fields of an existing source
  rename PROJECT OLD NEW            change a source ID and rewrite its citations in all project .md files
  sources PROJECT [--type T] [--facet F] [--lens L] [--status S]
  log PROJECT QUERY [--found N] [--notes N]   append a row to the search log in 00-scope.md
  verify PROJECT [--ids a,b] [--limit N] [--dry-run]
                                    confirm unverified sources against Crossref (papers),
                                    Open Library (books), YouTube oEmbed (videos) or the URL itself;
                                    fills missing year/publisher/url/doi and sets status=confirmed
  discover PROJECT QUERY [--catalogues books,papers,crossref,archive,hn,stackexchange]
           [--rows N] [--lang de] [--se-site cooking] [--out candidates.jsonl]
                                    search open catalogues directly (Open Library, Europe PMC,
                                    Crossref, Internet Archive, Hacker News, Stack Exchange) and
                                    write new candidates for review and batch add
  abstract PROJECT ID [--mark-read] print a paper's abstract from Europe PMC (works when the
                                    publisher site is blocked)
  stats PROJECT                     coverage by type, lens, field, facet, language, decade, status
  check PROJECT [--strict]          PROBLEMs (exit 1): duplicates, bad fields, dangling citations.
                                    WARNings: thin diversity, unused sources, facets not in scope.
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
               "facets", "lens", "field", "lang", "license", "no_url_reason", "notes", "added", "verified_by"]

PROJECT_DIRS = ["compendium", "workbench", "library/raw", "library/extracted"]
GITIGNORE = """# The user's own files and their extracted text stay local (copyright).
library/raw/*
library/extracted/*
!library/raw/.gitkeep
!library/extracted/.gitkeep
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


def slug(text):
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def first_surname(author):
    first = re.split(r";|&| and |,? et al\.?", author)[0].strip()
    if "," in first:  # "Surname, A."
        return first.split(",")[0]
    words = [w for w in first.split() if not re.fullmatch(r"[A-Z]\.?", w)]
    return words[-1] if words else first


def make_id(author, year, title, taken):
    base_word = first_surname(author) if author else next(
        (w for w in re.findall(r"[A-Za-z]+", title) if w.lower() not in {"the", "a", "an", "of", "on", "and"}), "src")
    base = (re.sub(r"[^a-z0-9]", "", slug(base_word)) or "src") + (re.sub(r"\D", "", str(year or ""))[:4])
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
    dup = next((s for s in sources if slug(s["title"]) == slug(record["title"])
                and (s.get("author") or "") [:6].lower() == (record.get("author") or "")[:6].lower()), None)
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
            "notes": args.notes, "id": getattr(args, "id", None)}


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
            "## Search log\n\n| Query / place searched | New sources | Notes |\n|---|---|---|\n",
            encoding="utf-8",
        )
    print(f"Initialized {project}/ (00-scope.md, sources.jsonl, compendium/, workbench/, library/)")


def cmd_add(args):
    sources = load_sources(args.project)
    if args.from_jsonl:
        text = sys.stdin.read() if args.from_jsonl == "-" else Path(args.from_jsonl).read_text(encoding="utf-8")
        added = failed = 0
        for n, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"line {n}: invalid JSON ({exc})")
                failed += 1
                continue
            record, error = insert_source(sources, raw)
            if error:
                print(f"line {n}: skipped: {error}")
                failed += 1
            else:
                print(f"[{record['id']}] {record['title']}")
                added += 1
        save_sources(args.project, sources)
        print(f"{added} added, {failed} skipped")
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
    changes = normalize({k: v for k, v in source_fields(args).items() if k != "id"})
    target.update(changes)
    errors = validate(target)
    if errors:
        sys.exit("; ".join(errors))
    save_sources(args.project, sources)
    print(f"[{target['id']}] updated: {', '.join(changes) or 'nothing'}")


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
    row = f"| {args.query.replace('|', '/')} | {args.found if args.found is not None else ''} | {(args.notes or '').replace('|', '/')} |"
    if "## Search log" not in text:
        text += "\n## Search log\n\n| Query / place searched | New sources | Notes |\n|---|---|---|\n"
    head, tail = text.split("## Search log", 1)
    section, sep, rest = tail.partition("\n## ")  # only touch the search-log section
    lines = section.rstrip("\n").split("\n")
    last_table = max((i for i, line in enumerate(lines) if line.startswith("|")), default=len(lines) - 1)
    lines.insert(last_table + 1, row)
    section = "\n".join(lines) + ("\n\n" if sep else "\n")
    scope.write_text(head + "## Search log" + section + (sep.lstrip("\n") + rest if sep else ""), encoding="utf-8")
    print("logged:", row)


# ------------------------------------------------------------------ verify

def fetch_json(url, timeout=20):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def words(text):
    return set(re.findall(r"[a-z0-9]{3,}", slug(text).replace("-", " ")))


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
            detail = {"doi": item.get("DOI"), "year": str(year) if year else None}
            if journal:
                vol = "".join(filter(None, [item.get("volume"), f"({item['issue']})" if item.get("issue") else None]))
                pages = item.get("page")
                detail["publisher"] = f"{journal} {vol}{':' + pages if pages else ''}".strip()
            if item.get("DOI"):
                detail["url"] = "https://doi.org/" + item["DOI"]
            return "crossref", detail
    return None, None


def verify_book(s):
    params = {"title": s["title"], "limit": 5}
    if s.get("author"):
        params["author"] = first_surname(s["author"])
    docs = fetch_json("https://openlibrary.org/search.json?" + urllib.parse.urlencode(params)).get("docs", [])
    for doc in docs:
        if title_match(doc.get("title", ""), s["title"]):
            detail = {"year": str(doc["first_publish_year"]) if doc.get("first_publish_year") else None}
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
    if title_match(page_title, s["title"]) or title_match(s["title"], page_title):
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

def discover_openlibrary(query, rows, lang):
    params = {"q": query, "limit": rows, "fields": "title,author_name,first_publish_year,publisher,key,language"}
    if lang:
        params["language"] = {"en": "eng", "de": "ger", "fr": "fre", "es": "spa", "it": "ita"}.get(lang, lang)
    for d in fetch_json("https://openlibrary.org/search.json?" + urllib.parse.urlencode(params)).get("docs", []):
        yield {"type": "book", "title": d.get("title"), "author": " & ".join((d.get("author_name") or [])[:3]),
               "year": d.get("first_publish_year"), "publisher": (d.get("publisher") or [None])[0],
               "url": "https://openlibrary.org" + d["key"], "lang": (d.get("language") or [None])[0]}


def discover_europepmc(query, rows, lang):
    params = {"query": query, "format": "json", "pageSize": rows, "resultType": "lite"}
    for r in fetch_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params))["resultList"]["result"]:
        kind = "review" if "review" in (r.get("pubType") or "").lower() else "paper"
        yield {"type": kind, "title": re.sub(r"<[^>]+>", "", html.unescape(r.get("title", ""))).rstrip("."), "author": r.get("authorString"),
               "year": r.get("pubYear"), "publisher": r.get("journalTitle"), "doi": r.get("doi"),
               "url": f"https://doi.org/{r['doi']}" if r.get("doi") else f"https://europepmc.org/article/{r.get('source')}/{r.get('id')}",
               "notes": f"cited by {r.get('citedByCount', 0)}"}


def discover_crossref(query, rows, lang):
    params = {"query.bibliographic": query, "rows": rows}
    for item in fetch_json("https://api.crossref.org/works?" + urllib.parse.urlencode(params))["message"]["items"]:
        if item.get("type") in ("component", "peer-review", "grant"):
            continue
        kind = {"book": "book", "monograph": "book", "book-chapter": "book-chapter", "dissertation": "thesis",
                "dataset": "dataset", "standard": "standard", "report": "official-doc"}.get(item.get("type"), "paper")
        authors = [a.get("family", "") for a in item.get("author", [])][:3]
        year = (item.get("issued", {}).get("date-parts") or [[None]])[0][0]
        yield {"type": kind, "title": (item.get("title") or [""])[0], "author": " & ".join(filter(None, authors)),
               "year": year, "publisher": (item.get("container-title") or [item.get("publisher")])[0],
               "doi": item.get("DOI"), "url": "https://doi.org/" + item["DOI"] if item.get("DOI") else None,
               "notes": f"cited by {item.get('is-referenced-by-count', 0)}"}


def discover_archive(query, rows, lang):
    params = [("q", f"title:({query})"), ("rows", rows), ("output", "json")]
    params += [("fl[]", f) for f in ("identifier", "title", "creator", "year", "mediatype", "language")]
    kinds = {"texts": "book", "audio": "audio", "movies": "video", "data": "dataset", "image": "archive"}
    for d in fetch_json("https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(params))["response"]["docs"]:
        creator = d.get("creator")
        yield {"type": kinds.get(d.get("mediatype"), "archive"), "title": d.get("title"),
               "author": creator[0] if isinstance(creator, list) else creator, "year": d.get("year"),
               "url": "https://archive.org/details/" + d["identifier"], "publisher": "Internet Archive",
               "lang": (d.get("language") or [None])[0] if isinstance(d.get("language"), list) else d.get("language")}


def discover_hn(query, rows, lang):
    params = {"query": query, "hitsPerPage": rows, "tags": "story"}
    for h in fetch_json("https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(params))["hits"]:
        yield {"type": "community", "title": h.get("title"), "author": h.get("author"),
               "year": (h.get("created_at") or "")[:4], "publisher": "Hacker News discussion",
               "url": f"https://news.ycombinator.com/item?id={h['objectID']}",
               "notes": f"{h.get('num_comments', 0)} comments; links to {h.get('url') or 'text post'}"}


def discover_stackexchange(query, rows, lang, site="stackoverflow"):
    params = {"order": "desc", "sort": "votes", "q": query, "site": site, "pagesize": rows}
    for q in fetch_json("https://api.stackexchange.com/2.3/search/advanced?" + urllib.parse.urlencode(params))["items"]:
        yield {"type": "community", "title": html.unescape(q.get("title", "")), "publisher": f"Stack Exchange ({site})",
               "year": date.fromtimestamp(q.get("creation_date", 0)).year, "url": q.get("link"),
               "notes": f"score {q.get('score')}, {q.get('answer_count')} answers"}


CATALOGUES = {"books": discover_openlibrary, "papers": discover_europepmc, "crossref": discover_crossref,
              "archive": discover_archive, "hn": discover_hn, "stackexchange": discover_stackexchange}


def cmd_discover(args):
    known_urls = {s.get("url") for s in load_sources(args.project)}
    known_titles = {slug(s["title"]) for s in load_sources(args.project)}
    out = open(args.out, "a", encoding="utf-8") if args.out else None
    total = 0
    for name in as_list(args.catalogues):
        func = CATALOGUES.get(name)
        if not func:
            sys.exit(f"unknown catalogue {name} (use: {', '.join(CATALOGUES)})")
        try:
            if name == "stackexchange":
                results = list(func(args.query, args.rows, args.lang, site=args.se_site))
            else:
                results = list(func(args.query, args.rows, args.lang))
        except Exception as exc:
            print(f"# {name}: failed ({str(exc)[:80]})")
            continue
        print(f"# {name}: {len(results)} result(s)")
        for r in results:
            if not r.get("title"):
                continue
            new = r.get("url") not in known_urls and slug(r["title"]) not in known_titles
            r = {k: v for k, v in r.items() if v not in (None, "", [])}
            r.update({"status": "confirmed", "verified_by": name})
            print(("  NEW " if new else "  had ") + json.dumps(r, ensure_ascii=False))
            if new and out:
                out.write(json.dumps(r, ensure_ascii=False) + "\n")
                total += 1
    if out:
        out.close()
        print(f"{total} new candidate(s) appended to {args.out}. Review them, add reliability/lens/field/facets, "
              f"delete the irrelevant ones, then: add {args.project} --from-jsonl {args.out}")


def cmd_abstract(args):
    sources = load_sources(args.project)
    s = next((x for x in sources if x["id"] == args.source_id), None)
    if not s:
        sys.exit(f"No source with id {args.source_id}")
    query = f'DOI:"{s["doi"]}"' if s.get("doi") else f'TITLE:"{s["title"]}"'
    params = {"query": query, "format": "json", "resultType": "core", "pageSize": 1}
    results = fetch_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params))["resultList"]["result"]
    if not results or not results[0].get("abstractText"):
        sys.exit("No abstract found in Europe PMC")
    r = results[0]
    print(f"{r.get('title')}\n{r.get('authorString')} ({r.get('pubYear')}) {r.get('journalInfo', {}).get('journal', {}).get('title', '')}\n")
    print(re.sub(r"<[^>]+>", "", r["abstractText"]))
    if r.get("isOpenAccess") == "Y" and r.get("pmcid"):
        print(f"\nOpen access full text: https://europepmc.org/article/PMC/{r['pmcid']}")
    if args.mark_read:
        s["status"] = "seen"
        s["verified_by"] = "europepmc-abstract"
        if "abstract" not in (s.get("notes") or ""):
            s["notes"] = ((s.get("notes") or "") + " [read: abstract only]").strip()
        if not s.get("doi") and r.get("doi"):
            s["doi"] = r["doi"]
        save_sources(args.project, sources)
        print(f"\n[{s['id']}] marked seen (abstract only)")


# ------------------------------------------------------- stats and checks

def decade(year):
    match = re.search(r"-?\d{3,4}", str(year or ""))
    if not match:
        return None
    y = int(match.group())
    if y < 1900:
        return "pre-1900"
    return f"{y // 10 * 10}s"


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


def diversity_warnings(sources):
    warnings = []
    n = len(sources)
    if n == 0:
        return ["no sources yet"]
    lenses = Counter(l for s in sources for l in s.get("lens", []))
    types = Counter(s["type"] for s in sources)
    fields = Counter(f for s in sources for f in s.get("field", []))
    langs = Counter(s.get("lang", "en") for s in sources)
    decades = Counter(d for d in (decade(s.get("year")) for s in sources) if d)
    missing_lens = [l for l in LENSES if l not in lenses]
    untagged = sum(1 for s in sources if not s.get("lens"))
    if untagged:
        warnings.append(f"{untagged} source(s) have no --lens")
    if len(lenses) < 7:
        warnings.append(f"only {len(lenses)}/10 lenses covered; missing: {', '.join(missing_lens)}")
    if lenses and lenses.most_common(1)[0][1] > 0.5 * n:
        top = lenses.most_common(1)[0]
        warnings.append(f"lens '{top[0]}' dominates ({top[1]}/{n} sources)")
    if len(types) < 8:
        warnings.append(f"only {len(types)} source types used")
    if len(fields) < 4:
        warnings.append(f"only {len(fields)} field(s)/disciplines tagged; aim for 4+")
    if len(langs) < 2:
        warnings.append(f"all sources in one language ({next(iter(langs))}); add others if the field has them")
    if len(decades) < 3:
        warnings.append(f"sources span only {len(decades)} decade(s); add older/classic or newer work")
    unverified = sum(1 for s in sources if s.get("status", "unverified") == "unverified")
    if unverified > 0.3 * n:
        warnings.append(f"{unverified}/{n} sources unverified; run verify, then open the key ones")
    seen = sum(1 for s in sources if s.get("status") == "seen")
    if seen < 0.3 * n:
        warnings.append(f"only {seen}/{n} sources actually read (status seen)")
    return warnings


def cmd_stats(args):
    sources = load_sources(args.project)
    print(f"{len(sources)} sources")
    counters = [
        ("type", Counter(s["type"] for s in sources)),
        ("lens", Counter(l for s in sources for l in s.get("lens", []))),
        ("field", Counter(f for s in sources for f in s.get("field", []))),
        ("facet", Counter(f for s in sources for f in s.get("facets", []))),
        ("language", Counter(s.get("lang", "en") for s in sources)),
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
    print("\ndiversity warnings:")
    for w in diversity_warnings(sources) or ["none"]:
        print("  -", w)


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
    cited = cited_ids(args.project)
    problems += [f"cited but not registered: @{c}" for c in cited if c not in ids]
    unused = [i for i in ids if i not in cited]
    if unused:
        warnings.append(f"{len(unused)} source(s) not cited anywhere: {', '.join(unused[:25])}"
                        + (" ..." if len(unused) > 25 else ""))
    known = scope_facets(args.project)
    if known:
        stray = sorted({f for s in sources for f in s.get("facets", []) if slug(f) not in known
                        and not any(slug(f) in k or k in slug(f) for k in known)})
        if stray:
            warnings.append(f"facets not in 00-scope.md table: {', '.join(stray)}")
    warnings += diversity_warnings(sources)
    for p in problems:
        print("PROBLEM", p)
    for w in warnings:
        print("WARN   ", w)
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
    p.add_argument("--facets", help="comma-separated facet names from 00-scope.md")
    p.add_argument("--lens", help=f"comma-separated: {', '.join(LENSES)}")
    p.add_argument("--field", help="comma-separated disciplines/domains, e.g. microbiology,food-history")
    p.add_argument("--lang", help="ISO language code of the source, default en")
    p.add_argument("--license", help="e.g. CC BY-SA 4.0, public domain (reusable material)")
    p.add_argument("--no-url-reason", help="why no URL exists (out-of-print tape, archive item...)")
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
    p.add_argument("--from-jsonl", help="batch file with one JSON source per line ('-' for stdin)")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("update")
    p.add_argument("project")
    p.add_argument("source_id")
    add_source_options(p)
    p.set_defaults(func=cmd_update)

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
    p.add_argument("query")
    p.add_argument("--found", type=int)
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
    p.add_argument("--lang", help="language filter for books, e.g. de, fr")
    p.add_argument("--se-site", default="stackoverflow", help="Stack Exchange site, e.g. cooking, history, fitness")
    p.add_argument("--out", help="append new candidates to this JSONL file for review and batch add")
    p.set_defaults(func=cmd_discover)

    p = sub.add_parser("abstract")
    p.add_argument("project")
    p.add_argument("source_id")
    p.add_argument("--mark-read", action="store_true", help="set status=seen (abstract only) after reading")
    p.set_defaults(func=cmd_abstract)

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
