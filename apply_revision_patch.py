#!/usr/bin/env python3
"""
Apply revision-patch-list.md to the submitted manuscript.

  source (never modified) : var_manuscript_cise.md            (201 lines)
  reference version       : docs/var_manuscript_cise_r1.md    (block source)
  output                  : var_manuscript_cise_r1.md         (repo root)

Every paragraph in the source occupies one line, so each edit is a whole-line
(or whole-block) replacement anchored by line number. Edits are applied in
DESCENDING line order so earlier anchors stay valid.

Emits a JSON trace to docs/patch-application-trace.json recording, per edit,
the anchor, the first 80 characters of the line it replaced, and the number of
lines written back. That trace is what makes the application auditable rather
than merely done.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "var_manuscript_cise.md"
PATCH = ROOT / "docs" / "revision-patch-list.md"
REF = ROOT / "docs" / "var_manuscript_cise_r1.md"
OUT = ROOT / "var_manuscript_cise_r1.md"
TRACE = ROOT / "docs" / "patch-application-trace.json"

src_lines = SRC.read_text().split("\n")
patch = PATCH.read_text()
ref_lines = REF.read_text().split("\n")


def ref_block(a, b):
    """Lines a..b inclusive, 1-indexed, from the reference version."""
    return ref_lines[a - 1:b]


# ── parse the patch list ─────────────────────────────────────────────────────
# Each edit: "## E<n> — Line(s) A[ to B] ..." then optional "> " blockquote.
edit_re = re.compile(
    r"^## (E\d+) — Lines? (\d+)(?:\s*(?:to|[-–—])\s*(\d+))?[^\n]*\n(.*?)(?=^## |\Z)",
    re.S | re.M)

edits = {}
for m in edit_re.finditer(patch):
    eid, a, b, body = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    b = int(b) if b else a
    quoted = [ln for ln in body.split("\n") if ln.startswith(">")]
    repl = None
    if quoted:
        # ">" alone is a paragraph break; the manuscript separates paragraphs
        # with a blank line, so emit one.
        repl = [re.sub(r"^> ?", "", ln) for ln in quoted]
    edits[eid] = {"start": a, "end": b, "repl": repl, "body": body}

# ── edits whose replacement text is not inline ───────────────────────────────
# E8  §3 in full            -> reference 77..135
# E33 Experimental procs    -> reference 265..273  (heading stays in source)
# E34 Data and code avail.  -> reference 281
# E35 References [1]..[12]  -> reference 289..311  (skip the DOI note at 287;
#                              STOP at 311. [12] ends there and 313-317 are the
#                              back matter, which the source already carries. A
#                              289..317 range duplicated Author contributions and
#                              Declaration of interests and inflated the count.)
# E36 Generative AI use     -> reference 321
edits["E8"]["repl"] = ref_block(77, 135)
edits["E33"]["repl"] = ref_block(265, 273)
edits["E34"]["repl"] = ref_block(281, 281)
edits["E35"]["repl"] = ref_block(289, 311)
edits["E36"]["repl"] = ref_block(321, 321)

# The E35 range above is load-bearing: assert what it stops on, so a drifted
# reference file fails loudly instead of quietly re-importing the back matter.
assert ref_lines[310].startswith("[12] Brazma"), "E35 range no longer ends on [12]"
assert ref_lines[312].strip() == "---", "E35 range: line 313 is not the rule"

# Part 2 of the E35 repair (docs/patch-application-report.md, Addendum 1 §5).
# Correcting the range left the *source* copy of the declarations block as the
# survivor, and that is the copy carrying the two non-numeric en dashes
# ("Writing - original draft") and the ampersand. Replace source 189 and 191
# with reference 315 and 317 so the de-dashed copy is the one that survives.
# Source 191 and reference 317 are byte-identical, so that half writes no new
# text; it is kept because the documented fix specifies both lines, and it
# keeps the two declarations marked as a pair.
assert src_lines[188].startswith("**Author contributions:**"), "E35a anchor drifted"
assert src_lines[190].startswith("**Declaration of interests:**"), "E35b anchor drifted"
assert ref_lines[314].startswith("**Author contributions:**"), "E35a block source drifted"
assert ref_lines[316].startswith("**Declaration of interests:**"), "E35b block source drifted"
assert "\u2013" not in ref_lines[314], "E35a replacement still carries an en dash"
edits["E35a"] = {"start": 189, "end": 189, "repl": ref_block(315, 315), "body": ""}
edits["E35b"] = {"start": 191, "end": 191, "repl": ref_block(317, 317), "body": ""}

# E5 and E9 are instruction-style, expressed against the source line itself.
l35 = src_lines[34]
assert l35.startswith("**Verifiability** is checkable."), "E5 anchor drifted"
edits["E5"]["repl"] = [
    "### 2.1 Verifiability",
    "",
    l35.replace("**Verifiability** is checkable.", "Verifiability is checkable.", 1),
]

l77 = src_lines[76]
assert "We demonstrate AIVS-VAR on a workflow" in l77, "E9 anchor drifted"
edits["E9"]["repl"] = [
    l77.replace("We demonstrate AIVS-VAR on a workflow",
                "We demonstrate AIVS on a workflow", 1)
]

# E6 and E7 carry no subsection heading in the patch list, while E5 does. Left
# alone the rendered §2 has a "2.1 Verifiability" with no 2.2 and no 3, which
# reads as a structural defect. docs/var_manuscript_cise_r1.md, the assembled
# target, has all three (### 2.1 / ### 2.2 Accountability / ### 2.3
# Reproducibility), so the intent is unambiguous and the headings are restored
# here rather than invented.
for eid, heading in (("E6", "### 2.2 Accountability"),
                     ("E7", "### 2.3 Reproducibility")):
    assert edits[eid]["repl"], f"{eid} has no replacement text"
    assert not edits[eid]["repl"][0].startswith("#"), f"{eid} already has a heading"
    edits[eid]["repl"] = [heading, ""] + edits[eid]["repl"]

missing = [e for e, d in edits.items() if d["repl"] is None]
if missing:
    raise SystemExit(f"FAIL: no replacement text resolved for {missing}")

# ── apply, descending ────────────────────────────────────────────────────────
out = list(src_lines)
trace = []
for eid in sorted(edits, key=lambda e: edits[e]["start"], reverse=True):
    d = edits[eid]
    a, b, repl = d["start"], d["end"], d["repl"]
    replaced = out[a - 1:b]
    out[a - 1:b] = repl
    trace.append({
        "edit": eid,
        "anchor": f"{a}" if a == b else f"{a}-{b}",
        "lines_replaced": len(replaced),
        "lines_written": len(repl),
        "was": replaced[0][:80] if replaced else "",
        "now": repl[0][:80] if repl else "",
    })

OUT.write_text("\n".join(out))

# ── change-marked copy, for coloured rendering ───────────────────────────────
# Rebuild with a per-line changed flag so the colouring derives from the same
# application rather than from a post-hoc diff.
marked = [(l, False) for l in src_lines]
for eid in sorted(edits, key=lambda e: edits[e]["start"], reverse=True):
    d = edits[eid]
    marked[d["start"] - 1:d["end"]] = [(l, True) for l in d["repl"]]

MARKED = ROOT / "docs" / "var_manuscript_cise_r1_marked.md"
buf, i = [], 0
while i < len(marked):
    line, chg = marked[i]
    if chg and line.strip():
        run = []
        while i < len(marked) and marked[i][1]:
            run.append(marked[i][0]); i += 1
        while run and not run[-1].strip():
            run.pop()
        buf.append('::: {custom-style="ChangedPara"}')
        buf.extend(run)
        buf.append(":::")
        buf.append("")
    else:
        buf.append(line); i += 1
MARKED.write_text("\n".join(buf))
print(f"  marked : {sum(1 for _, c in marked if c)} changed lines -> {MARKED.name}")
TRACE.write_text(json.dumps(sorted(trace, key=lambda t: t["edit"]),
                            indent=2, ensure_ascii=False))

print(f"applied {len(trace)} edits")
print(f"  source : {len(src_lines)} lines")
print(f"  output : {len(out)} lines -> {OUT.name}")
print(f"  trace  : {TRACE.relative_to(ROOT)}")
print(f"  source md5 unchanged check is the caller's job")
