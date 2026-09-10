#!/usr/bin/env python3
"""Word count for the CiSE revision.

CiSE counts the two tables as word-equivalents and counts back matter,
including author biographies. It does not count the reference list.

The earlier counter treated everything after the "## References" heading as
references and excluded it, which silently dropped ~350 words of back matter
(author contributions, declaration, acknowledgments, AI-use disclosure,
biographies) out of the total. Reference entries are now identified
specifically, by the "[n] " prefix, so back matter is counted where it belongs.
"""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else "var_manuscript_cise_r1.md"
lines = open(path).read().split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith("## Abstract"))

body, table, refs = [], [], []
ref_entry = re.compile(r"^\[\d+\]\s")
for l in lines[start:]:
    s = l.strip()
    if s.startswith("|"):
        table.append(l)
    elif ref_entry.match(s) or s == "## References" or s == "---":
        refs.append(l)
    else:
        body.append(l)

def wc(ls):
    t = "\n".join(ls)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"[#*_>|\-]+", " ", t)
    return len(t.split())

# Figure captions are reported separately: venues differ on whether they count
# toward the limit, and here that choice is the difference between 26 under and
# 158 over. Do not collapse the two figures into one number.
cap = [l for l in body if l.strip().startswith("**Figure ")
       or l.strip() == "### Figures"]
b, tb, rf, cp = wc(body), wc(table), wc(refs), wc(cap)
total = b + tb
LIMIT = 6250
print(f"  body text, incl. back matter and biographies : {b:5d}")
print(f"  tables, as word-equivalents ({len(table)} rows)      : {tb:5d}")
print(f"  ------------------------------------------------------")
print(f"  COUNTED TOTAL (body + tables)                : {total:5d}")
print(f"  limit                                        : {LIMIT:5d}")
print(f"  {'UNDER by ' + str(LIMIT - total) if total <= LIMIT else 'OVER by ' + str(total - LIMIT):>54}")
print()
print(f"  of which figure captions                     : {cp:5d}")
print(f"  TOTAL EXCLUDING figure captions              : {total - cp:5d}"
      f"   -> {'UNDER by ' + str(LIMIT - (total - cp)) if total - cp <= LIMIT else 'OVER by ' + str((total - cp) - LIMIT)}")
print()
print(f"  reference list, not counted                  : {rf:5d}")
print(f"  (body + tables + references)                 : {total + rf:5d}")
print()
print("  NOTE: whether CiSE counts figure captions decides this. Confirm before")
print("        upload; the two conventions straddle the limit.")
sys.exit(0 if (total - cp) <= LIMIT else 1)
