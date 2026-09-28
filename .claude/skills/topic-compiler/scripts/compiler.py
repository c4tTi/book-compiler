#!/usr/bin/env python3
"""Project, source-registry and file-ingest helper for the topic-compiler skill.

Commands (PROJECT is a directory, e.g. projects/yoga-nidra):
    init PROJECT --title "Yoga Nidra" [--purpose "write a book"]
    add PROJECT --title T --type TYPE [--author A] [--year Y] [--url U]
                [--publisher P] [--reliability 1-5] [--status seen|unverified]
                [--facets f1,f2] [--notes N] [--id ID]
    sources PROJECT [--type TYPE] [--facet F]     list registered sources
    check PROJECT                                  duplicates, missing fields, unused/unknown citations
    bib PROJECT                                    write compendium/99-bibliography.md
    stats PROJECT                                  coverage by type, facet, reliability
    ingest PROJECT                                 extract text from PROJECT/library/raw/
    search PROJECT TERM [--context N]              search the extracted files

Sources live in PROJECT/sources.jsonl, one JSON object per line.
The user's own files (library/raw, library/extracted) should be git-ignored.
"""

import argparse
import html
import json
import re
import sys
import unicodedata
import zipfile
from collections import Counter
from datetime import date
from pathlib import Path
from xml.etree import ElementTree

SOURCE_TYPES = [
    "book", "paper", "review", "thesis", "primary-text", "website", "article",
    "official-doc", "standard", "dataset", "video", "podcast", "course",
    "tool", "software", "community", "person", "organization", "news", "other",
]

HEADINGS = {"primary-text": "Primary texts", "official-doc": "Official documents", "software": "Software",
            "news": "News", "person": "People", "other": "Other", "dataset": "Datasets", "thesis": "Theses"}

PROJECT_DIRS = ["compendium", "workbench", "library/raw", "library/extracted"]
GITIGNORE = """# The user's own files and their extracted text stay local (copyright).
library/raw/*
library/extracted/*
!library/raw/.gitkeep
!library/extracted/.gitkeep
"""


# ---------------------------------------------------------------- registry

def registry_path(project):
    return Path(project) / "sources.jsonl"


def load_sources(project):
    path = registry_path(project)
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as lines:
        return [json.loads(line) for line in lines if line.strip()]


def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def make_id(author, year, title, taken):
    surname = (author or title).split(",")[0].split(" & ")[0].split()[-1] if (author or title) else "src"
    base = f"{slug(surname)}{year or ''}" or "src"
    candidate, suffix = base, ord("a")
    while candidate in taken:
        candidate = f"{base}{chr(suffix)}"
        suffix += 1
    return candidate


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
        scope.write_text(
            f"# Scope: {args.title}\n\n"
            f"- **Request:** {args.request or ''}\n"
            f"- **Purpose:** {args.purpose or ''}\n"
            f"- **Audience:** \n- **Depth:** \n- **Languages:** \n- **Out of scope:** \n"
            f"- **Started:** {date.today().isoformat()}\n\n"
            "## Facets\n\n| Facet | Key questions | Status |\n|---|---|---|\n\n"
            "## Search log\n\n| Query / place searched | New sources | Notes |\n|---|---|---|\n",
            encoding="utf-8",
        )
    print(f"Initialized {project}/ (scope, sources.jsonl, compendium/, workbench/, library/)")


def cmd_add(args):
    sources = load_sources(args.project)
    taken = {s["id"] for s in sources}
    if args.url and any(s.get("url") == args.url for s in sources):
        sys.exit(f"Already registered: {args.url}")
    same_title = [s for s in sources if slug(s["title"]) == slug(args.title)]
    if same_title:
        sys.exit(f"Possible duplicate of [{same_title[0]['id']}] {same_title[0]['title']}")
    source_id = args.id or make_id(args.author, args.year, args.title, taken)
    if source_id in taken:
        sys.exit(f"ID already used: {source_id}")
    record = {
        "id": source_id, "type": args.type, "title": args.title, "author": args.author,
        "year": args.year, "publisher": args.publisher, "url": args.url,
        "reliability": args.reliability, "status": args.status,
        "facets": [f.strip() for f in args.facets.split(",")] if args.facets else [],
        "notes": args.notes, "added": date.today().isoformat(),
    }
    record = {k: v for k, v in record.items() if v not in (None, "", [])}
    with registry_path(args.project).open("a", encoding="utf-8") as out:
        out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"[{source_id}] {args.title}")


def cmd_sources(args):
    for s in load_sources(args.project):
        if args.type and s["type"] != args.type:
            continue
        if args.facet and args.facet not in s.get("facets", []):
            continue
        flag = "" if s.get("status") == "seen" else " (unverified)"
        print(f"[{s['id']}] {s['type']:<12} r{s.get('reliability', '?')} {s['title']}{flag}")


def cited_ids(project):
    cited = Counter()
    for md in (Path(project) / "compendium").glob("*.md"):
        if md.name == "99-bibliography.md":
            continue
        for group in re.findall(r"\[@([^\]]+)\]", md.read_text(encoding="utf-8")):
            for ref in re.split(r"[;,]\s*@?", group):
                cited[ref.strip().lstrip("@")] += 1
    return cited


def cmd_check(args):
    sources = load_sources(args.project)
    ids = Counter(s["id"] for s in sources)
    urls = Counter(s["url"] for s in sources if s.get("url"))
    titles = Counter(slug(s["title"]) for s in sources)
    problems = []
    problems += [f"duplicate id: {i}" for i, n in ids.items() if n > 1]
    problems += [f"duplicate url: {u}" for u, n in urls.items() if n > 1]
    problems += [f"duplicate title: {t}" for t, n in titles.items() if n > 1]
    for s in sources:
        if s["type"] not in SOURCE_TYPES:
            problems.append(f"[{s['id']}] unknown type '{s['type']}'")
        if not s.get("url") and s["type"] not in ("book", "primary-text", "person", "thesis"):
            problems.append(f"[{s['id']}] no url")
        if "reliability" not in s:
            problems.append(f"[{s['id']}] no reliability rating")
    cited = cited_ids(args.project)
    problems += [f"cited but not registered: @{c}" for c in cited if c not in ids]
    unused = [i for i in ids if i not in cited]
    for p in problems:
        print("PROBLEM", p)
    if unused:
        print(f"note: {len(unused)} registered source(s) not cited in compendium: {', '.join(unused[:20])}")
    print(f"{len(sources)} sources, {len(problems)} problem(s)")
    sys.exit(1 if problems else 0)


def cmd_bib(args):
    sources = load_sources(args.project)
    cited = cited_ids(args.project)
    lines = ["# Bibliography", "",
             "Generated from `sources.jsonl`. Reliability 1 (weak) – 5 (authoritative). "
             "*Unverified* means the source was not opened during compilation; check it before relying on it.", ""]
    by_type = {}
    for s in sources:
        by_type.setdefault(s["type"], []).append(s)
    for kind in SOURCE_TYPES:
        if kind not in by_type:
            continue
        lines += [f"## {HEADINGS.get(kind, kind.title() + 's')}", ""]
        for s in sorted(by_type[kind], key=lambda s: (s.get("author") or s["title"]).lower()):
            parts = [f"**[@{s['id']}]**"]
            if s.get("author"):
                parts.append(s["author"].rstrip(".") + ".")
            parts.append(f"*{s['title']}*" + ("." if not s["title"].endswith((".", "?", "!")) else ""))
            if s.get("publisher"):
                parts.append(f"{s['publisher']}.")
            if s.get("year"):
                parts.append(f"{s['year']}.")
            if s.get("url"):
                parts.append(f"<{s['url']}>")
            tags = [f"r{s['reliability']}" if "reliability" in s else "r?"]
            if s.get("status") != "seen":
                tags.append("*unverified*")
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


def cmd_stats(args):
    sources = load_sources(args.project)
    print(f"{len(sources)} sources")
    for label, counter in (
        ("type", Counter(s["type"] for s in sources)),
        ("facet", Counter(f for s in sources for f in s.get("facets", []))),
        ("reliability", Counter(str(s.get("reliability", "?")) for s in sources)),
        ("status", Counter(s.get("status", "unverified") for s in sources)),
    ):
        print(f"\nby {label}:")
        for key, n in counter.most_common():
            print(f"  {key:<16} {n}")
    missing = [t for t in SOURCE_TYPES if t not in {s['type'] for s in sources}]
    print(f"\nsource types not yet represented: {', '.join(missing)}")


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
        sys.exit("PDF support needs pypdf: pip install pypdf")
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
    p.add_argument("--title", required=True)
    p.add_argument("--type", required=True, choices=SOURCE_TYPES)
    p.add_argument("--author")
    p.add_argument("--year")
    p.add_argument("--publisher")
    p.add_argument("--url")
    p.add_argument("--reliability", type=int, choices=range(1, 6))
    p.add_argument("--status", choices=["seen", "unverified"], default="unverified")
    p.add_argument("--facets")
    p.add_argument("--notes")
    p.add_argument("--id")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("sources")
    p.add_argument("project")
    p.add_argument("--type")
    p.add_argument("--facet")
    p.set_defaults(func=cmd_sources)

    for name, func in (("check", cmd_check), ("bib", cmd_bib), ("stats", cmd_stats), ("ingest", cmd_ingest)):
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
