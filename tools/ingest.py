#!/usr/bin/env python3
"""Extract text from your own yoga nidra books and search across them.

Usage:
    python3 tools/ingest.py                      # extract all files in library/raw/
    python3 tools/ingest.py search <term> [--context N]
    python3 tools/ingest.py list                 # list extracted books

Supported formats: .pdf (needs `pip install pypdf`), .epub, .txt, .md.
Extracted text is written to library/extracted/<file name>.jsonl, one record per
page (PDF) or chapter (EPUB). Both library folders are git-ignored so
copyrighted text never ends up in the repository.
"""

import argparse
import html
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "library" / "raw"
OUT = ROOT / "library" / "extracted"


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
    reader = PdfReader(str(path))
    for number, page in enumerate(reader.pages, start=1):
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
        spine = [ref.get("idref") for ref in opf.find("{*}spine")]
        for number, idref in enumerate(spine, start=1):
            href = manifest.get(idref)
            if not href:
                continue
            try:
                markup = book.read(base + href).decode("utf-8", errors="replace")
            except KeyError:
                continue
            yield f"ch. {number}", html_to_text(markup)


def extract_text(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    for number, block in enumerate(re.split(r"\n\s*\n\s*\n", text), start=1):
        yield f"part {number}", clean(block)


EXTRACTORS = {".pdf": extract_pdf, ".epub": extract_epub, ".txt": extract_text, ".md": extract_text}


def ingest():
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in RAW.iterdir() if p.suffix.lower() in EXTRACTORS)
    if not files:
        print(f"No books found. Put .pdf/.epub/.txt/.md files in {RAW.relative_to(ROOT)}/")
        return
    for path in files:
        target = OUT / f"{path.name}.jsonl"
        count = 0
        with target.open("w", encoding="utf-8") as out:
            for location, text in EXTRACTORS[path.suffix.lower()](path):
                if text:
                    out.write(json.dumps({"book": path.name, "loc": location, "text": text}) + "\n")
                    count += 1
        print(f"{path.name}: {count} sections -> {target.relative_to(ROOT)}")


def records():
    for target in sorted(OUT.glob("*.jsonl")):
        with target.open(encoding="utf-8") as lines:
            for line in lines:
                yield json.loads(line)


def search(term, context):
    pattern = re.compile(re.escape(term), re.IGNORECASE)
    hits = 0
    for record in records():
        for match in pattern.finditer(record["text"]):
            start = max(0, match.start() - context)
            end = min(len(record["text"]), match.end() + context)
            snippet = record["text"][start:end].replace("\n", " ")
            snippet = pattern.sub(lambda m: f"**{m.group(0)}**", snippet)
            print(f"[{record['book']}, {record['loc']}] ...{snippet}...\n")
            hits += 1
    print(f"{hits} match(es) for '{term}'")


def list_books():
    counts = {}
    for record in records():
        counts[record["book"]] = counts.get(record["book"], 0) + 1
    if not counts:
        print("Nothing extracted yet. Run: python3 tools/ingest.py")
    for book, sections in counts.items():
        print(f"{book}: {sections} sections")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command")
    find = sub.add_parser("search", help="search extracted books")
    find.add_argument("term")
    find.add_argument("--context", type=int, default=150, help="characters of context around each hit")
    sub.add_parser("list", help="list extracted books")
    args = parser.parse_args()
    if args.command == "search":
        search(args.term, args.context)
    elif args.command == "list":
        list_books()
    else:
        ingest()


if __name__ == "__main__":
    main()
