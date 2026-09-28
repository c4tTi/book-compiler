#!/usr/bin/env python3
"""Programmatic assertions for topic-compiler eval runs.

usage: grade.py RUN_DIR PURPOSE_KEYWORDS(comma-separated)
RUN_DIR contains outputs/. Writes RUN_DIR/grading.json.
"""
import json, re, subprocess, sys
from pathlib import Path

run = Path(sys.argv[1]); keywords = sys.argv[2].split(",")
out = run / "outputs"
projects = [p.parent for p in out.rglob("sources.jsonl")]
project = projects[0] if projects else out
md = [p for p in project.rglob("*.md") if "library" not in p.parts]
text = "\n".join(p.read_text(errors="replace") for p in md)
reg = []
if (project / "sources.jsonl").exists():
    reg = [json.loads(l) for l in (project / "sources.jsonl").read_text().splitlines() if l.strip()]
urls = set(re.findall(r"https?://[^\s)>\]\"']+", text)) | {s["url"] for s in reg if s.get("url")}
types = {s["type"] for s in reg}
seen = sum(1 for s in reg if s.get("status") == "seen")
unverified = sum(1 for s in reg if s.get("status", "unverified") == "unverified")
lenses = {l for s in reg for l in s.get("lens", [])}
fields = {f for s in reg for f in s.get("field", [])}
langs = {s.get("lang", "en") for s in reg}
chapters = [p for p in (project / "compendium").glob("*.md")] if (project / "compendium").exists() else []
body = [p for p in chapters if not re.match(r"(00|9\d)-", p.name)]
cited_per = {p.name: len(re.findall(r"@[a-z0-9]+", p.read_text())) for p in body}
flags = sum(text.count(f) for f in ("✅", "⚠️", "🔎"))
check_ok = None
if reg:
    script = Path(__file__).resolve().parents[2] / ".claude/skills/topic-compiler/scripts/compiler.py"
    r = subprocess.run([sys.executable, str(script), "check", str(project)], capture_output=True, text=True)
    check_ok = (r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
workbench = [p.name for p in (project / "workbench").glob("*")] if (project / "workbench").exists() else []
scope = (project / "00-scope.md").read_text() if (project / "00-scope.md").exists() else ""
facet_rows = len([l for l in scope.split("## Facets")[-1].split("##")[0].splitlines() if l.startswith("|") and "---" not in l]) - 1 if scope else 0
overview = next((p for p in chapters if p.name.startswith("00-")), None)
reply = (out / "final_reply.md").read_text() if (out / "final_reply.md").exists() else ""

def a(text, passed, evidence):
    return {"text": text, "passed": bool(passed), "evidence": str(evidence)}

exp = [
    a("At least 30 distinct sources found (registry or unique URLs)", max(len(reg), len(urls)) >= 30, f"registry={len(reg)}, unique urls={len(urls)}"),
    a("Sources span at least 6 source types", len(types) >= 6, f"types={sorted(types)}"),
    a("At least 30% of registered sources were actually read (status seen)", reg and seen >= 0.3 * len(reg), f"{seen}/{len(reg)} seen"),
    a("Scope file lists at least 6 facets", facet_rows >= 6, f"facet rows={facet_rows}"),
    a("Every compendium body chapter has at least 3 citations", body and all(n >= 3 for n in cited_per.values()), cited_per),
    a("Confidence flags used (at least 10)", flags >= 10, f"flags={flags}"),
    a("Overview chapter with a best-sources-by-type section", overview and re.search(r"best sources", overview.read_text(), re.I), overview.name if overview else "none"),
    a("compiler.py check passes with no problems", check_ok and check_ok[0], check_ok),
    a("Purpose-specific workbench file present", any(k in w.lower() for w in workbench for k in keywords), workbench),
    a("Sources cover at least 7 of 10 lenses (perspectives)", len(lenses) >= 7, f"lenses={sorted(lenses)}"),
    a("Sources tagged with at least 4 fields/disciplines", len(fields) >= 4, f"fields={sorted(fields)[:12]}"),
    a("Sources in at least 2 languages", len(langs) >= 2, f"langs={sorted(langs)}"),
    a("At least 8 source types", len(types) >= 8, f"{len(types)} types"),
    a("At most 30% of sources unverified", reg and unverified <= 0.3 * len(reg), f"{unverified}/{len(reg)} unverified"),
    a("Final reply reports seen vs unverified counts and gaps", reply and re.search(r"unverified|not (yet )?(opened|checked)|verified|confirmed|\bread\b", reply, re.I) and re.search(r"gap|thin|missing|to check", reply, re.I), reply[:200]),
]
passed = sum(e["passed"] for e in exp)
(run / "grading.json").write_text(json.dumps({"expectations": exp, "summary": {"passed": passed, "failed": len(exp) - passed, "total": len(exp), "pass_rate": passed / len(exp)}}, indent=2, ensure_ascii=False))
print(f"{run}: {passed}/{len(exp)}")
for e in exp:
    print(("PASS " if e["passed"] else "FAIL ") + e["text"] + "  -- " + e["evidence"][:150])
