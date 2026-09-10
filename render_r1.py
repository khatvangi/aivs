#!/usr/bin/env python3
"""Render the change-marked revision to DOCX and PDF.

  input  : docs/var_manuscript_cise_r1_marked.md   (emitted by apply_revision_patch.py)
  output : var_manuscript_cise_r1.docx, var_manuscript_cise_r1.pdf

Changed passages are wrapped in a ChangedPara div by the applier, so the colour
derives from the patch application rather than from a post-hoc diff.

Three steps:

1. Build a reference document from pandoc's default and inject a ChangedPara
   paragraph style coloured C00000.
2. Convert with pandoc, which maps custom-style to that paragraph style.
3. Colour table cell runs explicitly. Word's table style overrides the
   paragraph style on cells, so a table inside a ChangedPara div renders its
   caption red and its cells black. A wholly new table would then read as
   unchanged. A table is treated as changed when the paragraph immediately
   preceding it is itself ChangedPara, which is the same marking the applier
   produced, not a separate list of table numbers.

PDF is converted from the finished DOCX with LibreOffice, so the two artifacts
cannot disagree about what is marked.
"""

import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MARKED = ROOT / "docs" / "var_manuscript_cise_r1_marked.md"
DOCX = ROOT / "var_manuscript_cise_r1.docx"
PDF = ROOT / "var_manuscript_cise_r1.pdf"

CHANGE_COLOUR = "C00000"
STYLE = ('<w:style w:type="paragraph" w:customStyle="1" w:styleId="ChangedPara">'
         '<w:name w:val="ChangedPara"/><w:basedOn w:val="BodyText"/>'
         f'<w:rPr><w:color w:val="{CHANGE_COLOUR}"/></w:rPr></w:style>')

# CT_RPr is a sequence, so w:color has to sit in the right place among its
# siblings or Word rejects the run properties. Ranks below w:color come first.
RPR_ORDER = ["w:rStyle", "w:rFonts", "w:b", "w:bCs", "w:i", "w:iCs", "w:caps",
             "w:smallCaps", "w:strike", "w:dstrike", "w:outline", "w:shadow",
             "w:emboss", "w:imprint", "w:noProof", "w:snapToGrid", "w:vanish",
             "w:webHidden", "w:color", "w:spacing", "w:w", "w:kern", "w:position",
             "w:sz", "w:szCs", "w:highlight", "w:u", "w:effect", "w:bdr",
             "w:shd", "w:fitText", "w:vertAlign", "w:rtl", "w:cs", "w:em",
             "w:lang", "w:eastAsianLayout", "w:specVanish", "w:oMath"]
COLOUR_RANK = RPR_ORDER.index("w:color")


def build_reference(tmp: Path) -> Path:
    """pandoc's default reference.docx, plus the ChangedPara style."""
    ref = tmp / "ref.docx"
    with open(ref, "wb") as fh:
        subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                       stdout=fh, check=True)
    out = tmp / "ref_changed.docx"
    with zipfile.ZipFile(ref) as zin, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                s = data.decode("utf-8")
                assert "ChangedPara" not in s
                s = s.replace("</w:styles>", STYLE + "</w:styles>", 1)
                data = s.encode("utf-8")
            zout.writestr(item, data)
    return out


def rank(child: str) -> int:
    tag = re.match(r"<(w:[A-Za-z]+)", child)
    return RPR_ORDER.index(tag.group(1)) if tag and tag.group(1) in RPR_ORDER else len(RPR_ORDER)


def colour_run(run: str) -> str:
    """Set an explicit run colour, inserted at its schema position in w:rPr."""
    colour = f'<w:color w:val="{CHANGE_COLOUR}"/>'
    m = re.match(r"(<w:r(?:\s[^>]*)?>)(<w:rPr>(.*?)</w:rPr>)?(.*)$", run, re.S)
    open_tag, rpr, inner, rest = m.groups()
    if rpr is None:
        return f"{open_tag}<w:rPr>{colour}</w:rPr>{rest}"
    children = re.findall(r"<w:[A-Za-z]+(?:\s[^>]*?)?/>|<w:[A-Za-z]+.*?</w:[A-Za-z]+>",
                          inner, re.S)
    children = [c for c in children if not c.startswith("<w:color")]
    at = next((i for i, c in enumerate(children) if rank(c) > COLOUR_RANK), len(children))
    children.insert(at, colour)
    return f"{open_tag}<w:rPr>{''.join(children)}</w:rPr>{rest}"


def mark_tables(path: Path) -> tuple:
    """Colour every run in tables whose preceding paragraph is ChangedPara."""
    tmp = path.with_suffix(".tmp.docx")
    tables_marked = runs = 0
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                s = data.decode("utf-8")
                out, pos, total = [], 0, 0
                for m in re.finditer(r"<w:tbl>.*?</w:tbl>", s, re.S):
                    total += 1
                    before = s[:m.start()]
                    prev = re.findall(r"<w:p\b[^>]*>.*?</w:p>", before, re.S)
                    changed = bool(prev) and 'w:pStyle w:val="ChangedPara"' in prev[-1]
                    out.append(s[pos:m.start()])
                    if changed:
                        tbl = re.sub(r"<w:r(?:\s[^>]*)?>.*?</w:r>",
                                     lambda r: colour_run(r.group(0)), m.group(0), flags=re.S)
                        runs += len(re.findall(r"<w:r(?:\s[^>]*)?>", m.group(0)))
                        tables_marked += 1
                        out.append(tbl)
                    else:
                        out.append(m.group(0))
                    pos = m.end()
                out.append(s[pos:])
                data = "".join(out).encode("utf-8")
                found = total
            zout.writestr(item, data)
    tmp.replace(path)
    return tables_marked, found, runs


def preflight() -> None:
    """The marked file is a second output of the applier and needs the same
    placeholder fill as the root file. postprocess_r1.py takes several paths for
    exactly this reason; running it on only one of the two silently renders the
    references without their DOIs. Check before spending a render on it."""
    t = MARKED.read_text()
    for ph in ("[DATE RANGE]", "[MODEL STRINGS TO BE CONFIRMED]", "DOIs to be inserted",
               "TO BE UPDATED AFTER RE-DEPOSIT"):
        if ph in t:
            raise SystemExit(f"FAIL: {MARKED.name} still contains {ph!r}. "
                             f"Run: python3 postprocess_r1.py {MARKED} ")
    n = t.count("https://doi.org/") + t.count("https://grants.nih.gov/") + t.count("https://www.w3.org/")
    if n < 12:
        raise SystemExit(f"FAIL: {MARKED.name} carries {n} reference identifiers, expected 12. "
                         f"Run: python3 postprocess_r1.py {MARKED}")
    print(f"  preflight: {n} reference identifiers present, no placeholders")


def main() -> None:
    preflight()
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        ref = build_reference(tmp)
        subprocess.run(["pandoc", str(MARKED), "-o", str(DOCX),
                        f"--reference-doc={ref}", f"--resource-path={ROOT}"],
                       check=True, cwd=ROOT)
    marked, found, runs = mark_tables(DOCX)
    print(f"  docx   : {DOCX.name} ({DOCX.stat().st_size:,} B)")
    print(f"  tables : {marked} of {found} coloured, {runs} cell runs")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                    "--outdir", str(ROOT), str(DOCX)], check=True,
                   stdout=subprocess.DEVNULL, cwd=ROOT)
    print(f"  pdf    : {PDF.name} ({PDF.stat().st_size:,} B)")


if __name__ == "__main__":
    sys.exit(main())
