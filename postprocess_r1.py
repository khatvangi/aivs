#!/usr/bin/env python3
"""Fill resolved placeholders in the revised manuscript.

Reference identifiers come from Job 4 (docs/reference-dois.md), each verified
against CrossRef/DataCite. Refs 1 and 10 are document types that are not
DOI-registered and carry a verified live URL instead. The two Zenodo version
DOIs stay as placeholders until the deposit is minted.
"""
import sys
from pathlib import Path

REFS = {
 "[1]":  ("url", "https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-132.html"),
 "[2]":  ("doi", "10.48550/arXiv.2603.03299"),
 "[3]":  ("doi", "10.48550/arXiv.2505.11855"),
 "[4]":  ("doi", "10.1126/science.ade2574"),
 "[5]":  ("doi", "10.1126/science.adg7492"),
 "[6]":  ("doi", "10.1038/s41586-021-04043-8"),
 "[7]":  ("doi", "10.48550/arXiv.2502.18864"),
 "[8]":  ("doi", "10.48550/arXiv.2602.05930"),
 "[9]":  ("doi", "10.1109/eScience65000.2025.00093"),
 "[10]": ("url", "https://www.w3.org/TR/2013/REC-prov-o-20130430/"),
 "[11]": ("doi", "10.3233/DS-210053"),
 "[12]": ("doi", "10.1038/ng1201-365"),
}

def fill(path: Path) -> int:
    t = path.read_text()
    lines = t.split("\n"); n = 0
    for i, ln in enumerate(lines):
        for tag, (kind, val) in REFS.items():
            if ln.startswith(tag + " "):
                if "doi.org" in ln or "grants.nih.gov" in ln or "w3.org" in ln:
                    break
                s = ln.rstrip()
                if not s.endswith("."):
                    s += "."
                lines[i] = s + (f" https://doi.org/{val}" if kind == "doi" else f" {val}")
                n += 1
                break
    t = "\n".join(lines)
    t = t.replace("*DOIs to be inserted for all entries prior to submission.*\n\n", "", 1)
    # The AI-use disclosure no longer needs substitution here: the date range and the
    # model statement are final in docs/var_manuscript_cise_r1.md (the E36 block source),
    # written from author recollection and marked as tier 0 in the text itself. Assert
    # instead, so a surviving placeholder fails the build rather than reaching submission.
    for ph in ("[DATE RANGE]", "[MODEL STRINGS TO BE CONFIRMED]"):
        if ph in t:
            raise SystemExit(f"FAIL: unfilled placeholder {ph} in {path.name}")
    path.write_text(t)
    return n

for p in sys.argv[1:]:
    path = Path(p)
    print(f"  {path.name}: {fill(path)} reference identifiers inserted")
