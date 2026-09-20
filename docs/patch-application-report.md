# Patch application report — Job 5

2026-09-08, host `boron`. CiSE-2026-06-0105.

## Outcome: all 36 edits applied. Under the word limit. No em dashes.

| Artifact | Size |
|---|---|
| `var_manuscript_cise_r1.md` | 337 lines |
| `var_manuscript_cise_r1.docx` | 621,541 B |
| `var_manuscript_cise_r1.pdf` | 352,842 B, 20 pages |

**The submitted manuscript was not modified.** `var_manuscript_cise.md` md5
`34ef424c8f9ecefd95a1ced65fd1f414`, verified identical before and after.

Tooling, both deposited: `apply_revision_patch.py` (applies the patch list,
emits a per-edit JSON trace) and `postprocess_r1.py` (fills resolved
placeholders). The per-edit trace is `docs/patch-application-trace.json`.

## Pre-flight residuals, folded in as instructed

1. `docs/cise-r1-response-matrix.md:121` — "Three of 39 rows" → **"Three of 41
   rows"**. Row count verified independently: 40 numbered/C rows + 1 AE row =
   41, matching line 43's "Total rows: 41". Note this denominator now includes
   the `AE.0` placeholder, where the earlier figure appeared to exclude it;
   applied as instructed.
2. `docs/revision-patch-list.md` placeholder table — the §4.2 decision-count row
   is struck and cross-referenced to open item 1, which was already marked
   RESOLVED. The table and the open-items list now agree.

## Edits applied

All 36, in descending line order. Anchors re-validated against the source
immediately before application: **all in range, none blank, no duplicates, no
overlapping spans.**

| | |
|---|---|
| Single-line edits | 34 |
| Block edits | 2 — E8 (lines 45-71, §3 in full), E35 (163-185, references) |
| Replacement text inline in the patch list | 29 |
| Replacement text drawn from `docs/var_manuscript_cise_r1.md` | 5 — E8, E33, E34, E35, E36 |
| Instruction-style, applied against the source line | 2 — E5, E9 |

E5 and E9 were applied with an assertion on the source text first, so a drifted
anchor would have failed loudly rather than silently mis-editing:

- **E5** — inserts `### 2.1 Verifiability` and demotes the bolded lead-in;
  asserted `**Verifiability** is checkable.` at line 35.
- **E9** — asserted `We demonstrate AIVS-VAR on a workflow` at line 77 before
  replacing the clause.

Line growth: 201 → 337. Largest expansions E8 (27→59) and E35 (23→29).

**No edit failed.** Full per-edit record, with the replaced and written line
counts and the first 80 characters of each, in
`docs/patch-application-trace.json`.

## Placeholders

| Placeholder | Status |
|---|---|
| Reference DOIs, all 12 | **FILLED** |
| Date range, AI-use disclosure | **FILLED** — 2026-03-16 to 2026-09-09 |
| Model identifiers, AI-use disclosure | **NOT FILLABLE — see below** |
| Two Zenodo version DOIs | **LEFT AS PLACEHOLDER**, as instructed |
| Word count | **RESOLVED** — 6,088 |

### Reference identifiers — 12 of 12

Ten carry a DOI. References 1 (NIH Guide notice) and 10 (W3C PROV-O
Recommendation) carry a verified live URL instead, because neither document
type is DOI-registered — a property of the source, not a failed lookup. Every
identifier came from the Job 4 resolution against CrossRef, DataCite and the
arXiv API; none was written from recall.

PROV-AGENT `[9]` carries the IEEE publisher DOI
`10.1109/eScience65000.2025.00093` as primary with `arXiv:2508.02866` retained.

### Date range — filled, with its scope stated

`2026-03-16 to 2026-09-09`, from `~/.claude/history.jsonl` filtered to the two
project paths: `mechanism_classifier` (4 entries, all 2026-03-16) and `aivs`
(81 entries, 2026-05-11 to 2026-09-09). The host-wide range in that file is
2025-11-16 to 2026-09-09 and covers unrelated projects; it was **not** used.

Caveat worth carrying into the disclosure: `history.jsonl` records Claude Code
prompts only. Drafting done through the web interface leaves no entry, so this
range is a lower bound on the Claude Code portion, not a complete span.

### Model identifiers — could not be filled, and that is the finding

The brief said to take model strings from `~/.claude.json` and
`history.jsonl` only. Neither yields an attributable answer:

- `history.jsonl` records no model field at all.
- `~/.claude.json` lists 16 model strings, but host-wide across every project
  on the machine. Nothing ties any of them to this manuscript's sessions.
- The only surviving session log is one `aivs` session on 2026-08-25 using
  `claude-opus-5` — and `docs/audit-cost-summary.md` states of that session
  that it *"is not evidence about the AIVS audit construction or manuscript
  preparation, and it should not be cited as such."*

Rather than leave a bare placeholder or infer a plausible list, the disclosure
now states the actual evidentiary position: that one identifier survives, that
it belongs to a tooling session rather than to drafting, and that no per-model
attribution for the drafting work can be made from surviving evidence.

This is the §4.3 retention argument applied to the paper's own disclosure. A
fabricated model list in this manuscript would be self-refuting.

**If a fuller list is wanted it must come from author recollection, explicitly
marked as recollection.** That is an author decision, not something recoverable
from disk.

## Word count

**Corrected. The first figure of 6,088 was wrong, and wrong in the unsafe
direction.**

The original counter treated everything after the `## References` heading as
references and excluded it. That silently dropped the back matter — author
contributions, declaration, acknowledgments, the AI-use disclosure and the
author biographies — from the total. CiSE counts biography text. Reference
entries are now identified specifically by their `[n] ` prefix, so back matter
is counted where it belongs.

| Component | Words |
|---|---:|
| Body text, including back matter and biographies | 6,252 |
| Tables, as word-equivalents (17 rows) | 160 |
| **Total including figure captions** | **6,412** — over by 162 |
| of which figure captions | 184 |
| **Total excluding figure captions** | **6,228** — under by 22 |
| Reference list, not counted | 282 |

### The caption convention decides this, and it is not mine to assume

The two conventions straddle the limit. Excluding captions gives 22 words of
headroom; including them puts the manuscript 162 over. `wordcount_r1.py`
reports both and exits non-zero only on the excluding-captions figure, with the
ambiguity printed. **Confirm against CiSE's author guidelines before upload.**

The 6,228 is four words above the 6,224 predicted, and the four are accounted
for exactly: the two restored §2 subsection headings (see *Defects found*
below).

## Em dashes

**Zero** U+2014 in the output, including inside cited titles. Step 6 satisfied.

Nine U+2013 en dashes remain. Seven are numeric ranges (residue ranges
`502–526`, `274–414`, `185–372`; page ranges `1123–1130`, `91–95`, `97–138`,
`365–371`). The remaining two are on the **Author contributions** line:
`Writing – original draft` and `Writing – review & editing`.

Correction to an expectation carried into this run: the duplication fix did
**not** clear those two. They sit on the *surviving* copy of that line, not the
removed duplicate, so deduplication could not have touched them. They are also
correct as written — those are the official CRediT role labels, which contain
an en dash. No action needed.

## Change marking

Changed passages render in red (`#C00000`); unchanged text is black. The
journal accepts colour in place of Word track changes.

Mechanism: the applier emits `docs/var_manuscript_cise_r1_marked.md`, in which
every changed paragraph is wrapped in a `ChangedPara` div, derived from the
same application pass rather than from a post-hoc diff. DOCX rendering uses a
patched `reference.docx` carrying a red `ChangedPara` paragraph style; the PDF
is converted from that DOCX with LibreOffice, so the two artifacts cannot
disagree.

Verified in the rendered PDF, not merely in the markup: **105 of 226
paragraphs** carry the style. Page 1 shows the Abstract in red with the title,
authors, ORCID and Index Terms in black; page 9 shows correctly mixed content.

### Table cells — fixed

Previously only table captions rendered red, because Word's table styling
overrides the paragraph style on cells, so a wholly new table read as
unchanged. `render_r1.py` now colours cell runs directly, treating a table as
changed when the paragraph immediately preceding it is itself ChangedPara —
the same marking the applier produced, not a separate hand-kept list of table
numbers. Both tables now colour: **2 of 2, 75 cell runs.** Verified in the
rendered PDF.

`render_r1.py` also refuses to render at all unless the marked file carries
twelve resolved reference identifiers and no remaining placeholder. That guard
exists because the markdown was correct while the render input was not: the
marked file is a second output of the applier and needs the same placeholder
fill, and running `postprocess_r1.py` on only one of the two silently produced
a render with no DOIs. The mechanical signal said fine and the artifact was
not — the same shape as the self-confirming adapter test.

Note pandoc's own PDF path fails on this host (`Package bookmark Error:
Unsupported driver 'pdftex'`, from a stale `~/texmf/tex/latex/bookmark/`).
Unrelated to the manuscript; the LibreOffice route is better here anyway, since
converting from the finished DOCX means the two artifacts cannot disagree about
what is marked.

## Defects found in the patch list itself

Both were application bugs producing a wrong artifact, not content decisions,
and both were fixed in `apply_revision_patch.py` rather than by editing prose.

**1. E35 range over-ran by six lines, duplicating back matter.** The reference
block was taken as lines 289-317 of `docs/var_manuscript_cise_r1.md`, but
reference `[12]` ends at 311. Lines 313-317 are the `---` rule, **Author
contributions** and **Declaration of interests** — which the source already
carries further down. The output therefore contained each of those paragraphs
twice, with the injected copy landing ahead of the source's own. Range
corrected to 289-311.

This is what inflated the count. Removing a paragraph that appears twice takes
nothing out of the paper.

**2. E6 and E7 carried no subsection heading, E5 did.** The rendered §2 had a
`### 2.1 Verifiability` with no 2.2 and no 2.3, which reads as a structural
defect against §3's seven numbered subsections. `docs/var_manuscript_cise_r1.md`
— the assembled target — has all three, so the intent was unambiguous.
`### 2.2 Accountability` and `### 2.3 Reproducibility` are restored in the
applier, guarded by an assertion that the replacement does not already begin
with a heading. Cost: four words.

## Still outstanding

1. **Two Zenodo version DOIs** — the only remaining placeholders, at
   `var_manuscript_cise_r1.md:286`. Blocked on the Zenodo outage recorded in
   `docs/tagging-and-mint-report.md`; both repos are tagged and released, but
   every webhook delivery failed and nothing minted.
2. **Model identifiers** — author decision, per above.
3. Re-render after 1 and 2 are resolved. The word count has 162 words of
   headroom, and substituting two DOIs for two placeholders will not consume it.

---

# Addendum — Job 6: disclosure, table marking, denominator, re-render

2026-09-08, host `boron`. CiSE-2026-06-0105.

## Outcome: all three items done. One blocking issue found, not fixed: word count is 11 over.

> **Superseded by Addendum 2 below (2026-09-09).** The overage was not a
> content problem. It was a patch-application bug that duplicated back
> matter, plus a counter that excluded back matter it should have counted.
> Both are fixed; nothing was cut.

`var_manuscript_cise.md` md5 `34ef424c8f9ecefd95a1ced65fd1f414`, verified
unchanged before and after. Nothing committed, nothing pushed, Zenodo untouched;
the two version DOIs at `var_manuscript_cise_r1.md:286` remain placeholders.

## 1. AI-use disclosure — filled from author recollection

The supplied paragraph is in place verbatim, byte-compared against the brief in
both `var_manuscript_cise_r1.md` and `docs/var_manuscript_cise_r1_marked.md`.
No model identifier beyond "Claude Opus 4.6 class" appears; the date range is
`2026-03-16 to 2026-09-09` and was not widened.

It was written at its **source**, not in the output. The root file is generated:
`apply_revision_patch.py` splices reference blocks into the untouched submitted
manuscript and emits the change-marked copy in the same pass. Editing the root
file directly would have been reverted by the next re-render, and — worse — the
marked copy that feeds the DOCX would have kept the old text, so the new
disclosure would have rendered *unmarked*. The text therefore went into
`docs/var_manuscript_cise_r1.md:321`, the E36 block source.

The two placeholder substitutions in `postprocess_r1.py` are now obsolete and
have been replaced by an assertion, so a surviving `[DATE RANGE]` or
`[MODEL STRINGS TO BE CONFIRMED]` fails the build instead of shipping.

Two things worth recording against the previous position in this file:

- The earlier refusal to name a model is superseded, not overturned on the
  evidence. Nothing new was recovered from disk. What changed is the standard:
  §4.5 already reports cost as an author estimate at tier 0 because the logs
  that would have measured it are gone, and the disclosure now answers the same
  evidentiary situation the same way.
- The new text says the surviving identifier "survives in local configuration".
  The earlier finding located it in a session log, and `~/.claude.json` also
  carries model strings host-wide. Both readings are true of the machine and
  neither is cited as evidence for drafting, which is what the sentence says.

## 2. Table shading — fixed and verified in the PDF

Table 1 and Table 2 now render their cell contents in `#C00000`, the same
colour as the surrounding revised text.

Mechanism: `render_r1.py` (new, in the repo) sets `<w:color w:val="C00000"/>`
explicitly on every run inside a changed table, rather than relying on the
paragraph or table style, which Word overrides on cells. The colour is inserted
at its correct position in the `CT_RPr` sequence, so runs that already carry
`w:rStyle` (the `VerbatimChar` script names) or `w:b` keep valid run properties.

**Which tables get coloured is derived, not hardcoded.** A table is treated as
changed when the paragraph immediately preceding it carries `ChangedPara` —
which is its caption, marked by the same applier pass. Both tables qualify;
`2 of 2 coloured, 75 cell runs`.

Verified in the rendered PDF by pixel inspection, not in the markup. Pages
rasterized at 150 dpi, ink pixels classified as red (`R − max(G,B) > 40`) or
black:

| Region | ink px | red | black |
|---|---:|---:|---:|
| p1 title and authors (control, expect black) | 13,714 | 0.0% | 13,714 |
| p9 Table 1 caption (control, expect red) | 3,065 | 100.0% | 0 |
| Table 1 rows, p9 | 43,429 | 97.8% | 969 |
| Table 2 rows, p11 | 29,123 | 93.3% | 1,938 |
| Table 2 rows, p12 | 26,338 | 96.3% | 969 |

The residual black is not text. In every table region it lies on one or two
full-width scanlines: the header rules LibreOffice draws. **Cell text is 100%
red.**

## 3. Denominator — one figure changed, one already correct

| Document | Figure | Action |
|---|---|---|
| `docs/summary-of-changes.md:5` | "Thirty-eight reviewer comments were addressed" | **changed to "Thirty-four"** |
| `docs/summary-of-changes.md:6` | "three were declined" | already correct, untouched |
| `docs/response-to-reviewers.md:27` | "Three comments are declined: R4.3, R4.5, R5.4" | already correct, untouched |

No other count of comments or declines exists in either file. The three
declines themselves were not altered.

**Why 34 and not 38.** The matrix's 41 rows are not 41 reviewer comments.
Three of them say so in their own text — rows 3.8, 3.9 and 3.10 are marked
*"not raised by a reviewer"*, being defects found during revision — and AE.0 is
a placeholder for an Associate Editor review that is not in ScholarOne. Genuine
reviewer comments: 40 − 3 = **37**, of which 3 are declined, leaving **34
addressed**.

That reconciles exactly against the response letter, which carries 38 numbered
response sections: 37 reviewer comments plus one self-identified defect section
(letter §3.8, whose text is matrix row 3.10). Nothing is missing from the
letter; the two files simply number the self-identified rows differently. The
old figure of 38 matched the letter's section count rather than its reviewer
count.

If the intended convention is instead "rows in the matrix", the figure is 38 and
this is a one-word revert. Flagged rather than assumed.

## 4. Re-render

`render_r1.py` is new and now carries the render, which previously lived only in
a `/tmp` scratch directory and would not have survived. It builds the reference
document, converts with pandoc, applies the table colouring, and converts to PDF
with LibreOffice from the finished DOCX so the two artifacts cannot disagree.

| Artifact | Size |
|---|---|
| `var_manuscript_cise_r1.docx` | 621,741 B |
| `var_manuscript_cise_r1.pdf` | 352,918 B, 20 pages |
| `docs/response-to-reviewers.docx` | 19,949 B |
| `docs/summary-of-changes.docx` | 17,358 B |

Diffed against the previous render: the only content differences are the
disclosure paragraph and the two tables' run properties. Nothing else moved.

### A regression I introduced and caught

The first render silently dropped every reference DOI. `postprocess_r1.py`
takes several paths because the applier writes **two** files, and running it on
only the root file leaves the marked file — the actual render source — with
bare references. The PDF lost a page and nobody would have seen it in the
markdown. `render_r1.py` now refuses to render unless the marked file carries
12 resolved identifiers and no placeholder.

### Change marking

**226 paragraphs, 105 marked, 121 unmarked.** Sixteen of the unmarked are empty
spacer paragraphs; on non-empty paragraphs the split is 105 marked / 105
unmarked. The 67 table cell paragraphs are additionally coloured by explicit run
colour, which is not counted in the 105 since it is not carried by `pStyle`.

### Em dashes

**Zero** U+2014, in the markdown and in the rendered DOCX text, including inside
cited titles. Nine U+2013 remain. Seven are numeric ranges. **The other two are
not**: `Writing – original draft` and `Writing – review & editing`, in the
duplicated declarations block described below. The earlier claim that all nine
were numeric ranges was wrong.

## 5. BLOCKING — word count is 6,261, which is 11 over

| Component | Words |
|---|---:|
| Body, excluding tables and references | 6,106 |
| Tables, cell text, 67 cells | 155 |
| **Body + tables** | **6,261** |
| References, 12 entries | 252 |
| Body + tables + references | 6,513 |

Counted from the rendered DOCX text, which is what Word and ScholarOne see:
paragraphs partitioned into table and non-table, reference entries identified by
a leading `[n]`, tokens counted if they contain an alphanumeric. Body includes
abstract, headings, figure captions and all back matter, since CiSE's limit is
explicitly inclusive of biography text.

**The disclosure did push it over.** It added 33 words to a file that measured
6,228 by the same method. Per instruction, nothing was cut.

**The earlier figure of 6,088 in this file was wrong, by 173.** Its reference
bucket was 615 words for 12 references that actually total 252; it had swept
~350 words of back matter — acknowledgments, the AI-use disclosure, author
contributions, the biographies — into "references" and excluded them from the
body. Its paragraph counts (105 of 226) reproduce exactly, so the method was
DOCX-based and the segmentation was the error.

### The 11 words are available without cutting anything

`var_manuscript_cise_r1.md:318-320` and `:324-326` carry the **same
declarations block twice**:

```
**Author contributions:** ... Writing, original draft, ...      <- line 318, revised copy
**Declaration of interests:** ...                               <- line 320
---
**Author contributions:** ... Writing – original draft, ...     <- line 324, source copy
**Declaration of interests:** ...                               <- line 326
```

Cause: `apply_revision_patch.py` sets E35 to `ref_block(289, 317)`. Reference
[12] ends at reference line 311; lines 313-317 are a rule and the declarations
block. The block edit meant to carry the references also carries the back
matter, which lands ahead of the source's own copy at source lines 189-191.

The one-character fix is `ref_block(289, 311)`. It removes 37 words and takes
the count to **6,224, under by 26**. It also removes the two non-numeric en
dashes, since the surviving copy would then be the *source* copy — which is the
one with the en dashes and the ampersand. So the correct repair is two-part:

1. `edits["E35"]["repl"] = ref_block(289, 311)`;
2. a new edit replacing source lines 189 and 191 with reference lines 315 and
   317, so the surviving copy is the de-dashed one.

Not applied. Deleting a duplicated block is the obvious remedy for the overage,
and the overage is exactly the decision that was reserved.

## Still outstanding

1. **Word count 11 over.** Decide on the E35 range fix above, or accept.
2. **Two Zenodo version DOIs** at `var_manuscript_cise_r1.md:286`, unchanged.
3. **The 34 / 38 convention** in `docs/summary-of-changes.md:5`, if the intended
   denominator is matrix rows rather than reviewer comments.


---

# Addendum 2 — Job 6b: duplication fix, counter fix, §2 headings

2026-09-09, host `boron`. CiSE-2026-06-0105.

## Outcome: the overage was a bug, not a content problem. Nothing was cut.

`var_manuscript_cise.md` md5 `34ef424c8f9ecefd95a1ced65fd1f414`, unchanged.
Nothing committed, nothing pushed, Zenodo untouched. The two version DOIs at
`var_manuscript_cise_r1.md:286` remain the only placeholders.

## 1. E35 duplicated the back matter

The reference block was taken as lines 289-317 of
`docs/var_manuscript_cise_r1.md`. Reference `[12]` ends at **311**; 313-317 are
the `---` rule, **Author contributions** and **Declaration of interests**, which
the source already carries. Each appeared twice in the output, the injected copy
landing ahead of the source's own — confirmed before the fix at lines 318/324
and 320/326.

Range corrected to **289-311**. Both now appear once. Removing a paragraph that
appears twice takes nothing out of the paper.

## 2. The counter excluded back matter it should have counted

The original counter bucketed everything after the `## References` heading as
references. That dropped author contributions, declaration, acknowledgments, the
AI-use disclosure and the author biographies. **CiSE counts biography text.**
Reference entries are now matched specifically on their `[n] ` prefix.

The 6,088 first reported was therefore wrong in the unsafe direction — it made
the manuscript look further under the limit than it was. Finding this at render
time rather than at upload is the argument for rendering before minting.

## 3. §2 had a 2.1 with no 2.2 or 2.3

Found while itemising the count by section: the 2.1 bucket was absorbing 581
words, far more than a subsection. E5 inserts `### 2.1 Verifiability`; E6 and E7
carry no heading at all, so §2 rendered with one numbered subsection against
§3's seven. `docs/var_manuscript_cise_r1.md` has all three, so the intent was
unambiguous. Restored in the applier under an assertion that the replacement
does not already start with a heading. **Cost: four words** — which is exactly
the gap between the 6,224 predicted and the 6,228 measured.

## 4. Final counts

| Component | Words |
|---|---:|
| Body, including back matter and biographies | 6,252 |
| Tables, as word-equivalents | 160 |
| **Excluding figure captions** | **6,228 — under by 22** |
| Including figure captions | 6,412 — over by 162 |
| References, not counted | 282 |

**The caption convention decides this and is unconfirmed.** `wordcount_r1.py`
prints both and exits non-zero only on the excluding-captions figure, with the
ambiguity stated. Confirm against CiSE's author guidelines before upload.

## 5. Render

Full pipeline clean: apply → postprocess (both outputs) → preflight → render.

- 36 edits applied, 335 lines out
- preflight passed: 12 reference identifiers, no placeholders
- **tables: 2 of 2 coloured, 75 cell runs** — verified in the rendered PDF, not
  only in the markup
- `var_manuscript_cise_r1.docx` 621,770 B; `var_manuscript_cise_r1.pdf`
  352,734 B

## 6. One expectation corrected

The duplication fix was expected to clear two non-numeric en dashes. It did not,
and could not: they sit on the *surviving* Author contributions line, not the
removed duplicate. They read `Writing – original draft` and
`Writing – review & editing`, which are the official CRediT role labels — the en
dash is correct there. Em dashes remain at **zero**, which is what step 6
required.

## Still outstanding

1. **Two Zenodo version DOIs** — blocked on the outage in
   `docs/tagging-and-mint-report.md`. Both repos are tagged and released; every
   webhook delivery failed, so nothing minted and nothing is queued.
2. **Figure-caption convention** — confirm before upload.
3. **Comment-count convention** — Addendum 1 §3 flagged 34 vs 38; unresolved.


---

# Addendum 3 — Zenodo DOIs substituted

2026-09-10. The last two placeholders are gone.

`docs/var_manuscript_cise_r1.md:281` now carries both version DOIs, substituted
in the E36 source rather than the generated root so they render marked as
changed. Each was anchored on its own concept DOI, so the two cannot have been
swapped:

- concept `10.5281/zenodo.20723558` → version **`10.5281/zenodo.22698585`** (aivs)
- concept `10.5281/zenodo.20723560` → version **`10.5281/zenodo.22698586`** (idp)

`render_r1.py`'s preflight now also refuses to render on a surviving
`TO BE UPDATED AFTER RE-DEPOSIT`, alongside the twelve-identifier check.

## Final state

| Check | Result |
|---|---|
| Placeholders remaining | **0**, in both the root and marked files |
| Source manuscript | md5 `34ef424c8f9ecefd95a1ced65fd1f414`, unchanged |
| Edits applied | 36 of 36 |
| Em dashes | 0 |
| Back-matter duplication | none |
| Tables coloured | 2 of 2, 75 cell runs |
| **Word count, excluding figure captions** | **6,218 — under by 32** |
| Word count, including figure captions | 6,402 — over by 152 |
| Reference identifiers | 12 of 12 |
| DOIs present in rendered PDF | both, confirmed by `pdftotext` |

Substituting the DOIs *reduced* the count by 10 words, since two bracketed
placeholders were longer than the DOIs replacing them.

## Remaining open items

1. **Figure-caption convention** — the two conventions straddle the limit.
   Confirm against CiSE author guidelines before upload.
2. **Comment count 34 vs 38** — flagged in Addendum 1 §3, unresolved.
3. **Zenodo license metadata** `apgl-v3` → `agpl-3.0` on four records — needs a
   token or the web UI. See `docs/tagging-and-mint-report.md`.


---

# Addendum 4 — Job 7: E35 part 2 applied, counts re-verified from the PDF

2026-09-19, host `boron`. CiSE-2026-06-0105.

## Outcome: part 2 applied. Nothing cut. Under the limit on the rendered document.

`var_manuscript_cise.md` md5 `34ef424c8f9ecefd95a1ced65fd1f414`, verified
unchanged before and after. Nothing committed, nothing pushed, Zenodo untouched.

## 1. Part 1 was already applied — correcting the record

The brief for this job described the pre-Addendum-2 state: 6,261 words, the
declarations block duplicated at `var_manuscript_cise_r1.md:318-320` and
`:324-326`. That state no longer existed on disk. `apply_revision_patch.py:71`
already read `ref_block(289, 311)`, the block already appeared once, and the
committed artifacts measured 6,218 on `wordcount_r1.py`'s excluding-captions
figure. Addenda 2 and 3 had already landed part 1.

Nothing was changed for part 1. Two assertions were added instead, so the range
is self-checking rather than merely correct:

```python
assert ref_lines[310].startswith("[12] Brazma"), "E35 range no longer ends on [12]"
assert ref_lines[312].strip() == "---",          "E35 range: line 313 is not the rule"
```

A drifted reference file now fails the build rather than quietly re-importing
the back matter — which is the failure mode that produced the duplication.

## 2. Part 2 applied as written

Two new edits in `apply_revision_patch.py`, under anchor and content assertions:

| Edit | Source anchor | Replacement | Effect |
|---|---|---|---|
| `E35a` | `var_manuscript_cise.md:189` | `docs/var_manuscript_cise_r1.md:315` | `Writing – original draft` → `Writing, original draft`; `Writing – review & editing` → `Writing, review and editing` |
| `E35b` | `var_manuscript_cise.md:191` | `docs/var_manuscript_cise_r1.md:317` | none — the two lines are byte-identical |

Both went into the applier, not the generated root file. The root is an output;
an edit written there is reverted by the next run, and the marked copy that
feeds the DOCX would keep the old text, so the change would render *unmarked*.

`E35b` writes no new text. It is kept because the documented fix names both
lines and it keeps the two declarations marked as a pair. **The consequence is
worth stating plainly: Declaration of interests now renders red although its
text is unchanged.** Confirmed in the PDF. If that is unwanted, dropping
`E35b` removes it and changes nothing else.

Also carried forward from Addendum 2 §6, which this job overrides: the two en
dashes were the official CRediT role labels, and they are now gone. That was an
author decision, taken with the finding on the table.

Trace: 38 entries in `docs/patch-application-trace.json`, was 36.

## 3. Re-render

```
apply        : 38 edits, source 202 lines -> output 335 lines, 219 changed lines
postprocess  : 12 reference identifiers inserted into each of the two outputs
preflight    : 12 reference identifiers present, no placeholders
docx         : var_manuscript_cise_r1.docx (621,737 B)
tables       : 2 of 2 coloured, 75 cell runs
pdf          : var_manuscript_cise_r1.pdf (352,162 B, 19 pages)
```

Table cell colouring from the previous run is preserved: 2 of 2, 75 cell runs,
the same figures as Addendum 2 §5.

## 4. Verified in the rendered PDF, not in the markdown

Extraction by `pdftotext`; colour by PyMuPDF span colour, which reads the
rendered page rather than the markup.

| Check | Result |
|---|---|
| `**Author contributions:**` | **1 occurrence** |
| `**Declaration of interests:**` | **1 occurrence** |
| `**Acknowledgments:**` | 1 occurrence |
| `**Generative AI use:**` | **1 occurrence**, and all 17 of its rendered lines are `#C00000` |
| Reference identifiers in the render input | **12**, enforced by `render_r1.py` preflight before the render was spent |
| Reference entries `[1]`–`[12]` in the PDF | all 12 present; 12 identifier URLs |
| Em dashes U+2014 | **0** |
| En dashes U+2013 | **7, every one a numeric range** — `502–526`, `274–414`, `185–372`, `1123–1130`, `91–95`, `97–138`, `365–371` |

Marked versus unmarked, non-blank paragraphs in the rendered DOCX:

| | baseline (HEAD) | this run |
|---|---:|---:|
| marked, `ChangedPara` | 103 | **105** |
| unmarked | 107 | **105** |
| total non-blank | 210 | 210 |

Exactly +2, which is `E35a` and `E35b` and nothing else. The diff of
`docs/var_manuscript_cise_r1_marked.md` against its committed version is those
two paragraphs alone. `ChangedPara` divs 36 → 38.

In the PDF itself: 785 rendered text lines, 714 `#C00000`, 42 black, 29 in
pandoc's heading colour.

### One pre-existing gap, not fixed

Headings never render red — pandoc's Heading styles override `ChangedPara` the
same way table styles override it on cells. So `### 2.2 Accountability` and
`### 2.3 Reproducibility`, both added by the applier, are not visibly
change-marked. Out of scope here and the same class of defect as the table-cell
problem fixed in Addendum 2 §2; recording it rather than fixing it silently.

## 5. Word count — and a defect in the counter

**From the rendered DOCX text, which is what Word and ScholarOne see:**

| Component | Words |
|---|---:|
| Body, including back matter and biographies | 6,067 |
| Tables, cell text, 65 cells | 156 |
| **Body + tables, including figure captions** | **6,223 — UNDER by 27** |
| of which figure captions | 163 |
| Body + tables, excluding figure captions | 6,060 — under by 190 |
| References, 12 entries, not counted | 252 |

Method as in Addendum 1 §5: paragraphs partitioned into table and non-table,
reference entries identified by a leading `[n]`, tokens counted if they contain
an alphanumeric.

**`wordcount_r1.py` disagrees, and it is the one that is wrong.** It reports
body 6,240, tables 160, 6,400 including captions and 6,216 excluding them.
Line 34 is `re.sub(r"[#*_>|\-]+", " ", t)`, which strips the ASCII hyphen along
with the markdown markup. The manuscript contains **176 hyphenated compounds**
in the body — `AI-assisted`, `machine-readable`, `open-source`, `person-hours`
— and each is counted twice. Removing `\-` from that character class takes the
markdown body from 6,240 to 6,034, which agrees with the DOCX-derived 6,067 to
within ordinary markup noise.

Two consequences:

1. The manuscript is **under 6,250 on both caption conventions**, by 27 and by
   190. The "the two conventions straddle the limit" item carried since
   Addendum 1 is an artefact of the hyphen splitting, not a property of the
   manuscript.
2. `wordcount_r1.py` was **not changed**. It gates the build on the
   excluding-captions figure and currently passes, and altering a reported
   count is the class of decision reserved to the author. The one-character
   fix is recommended, not applied.

Nothing was cut, condensed or reworded. The 2-word reduction from 6,218 to
6,216 on the old counter is the two en dashes and the ampersand leaving, offset
by `and` arriving.

## Still outstanding

1. **`wordcount_r1.py` hyphen splitting** — one-character fix, author's call.
   Until it is made, prefer the DOCX-derived figure.
2. **Comment count 34 vs 38** — Addendum 1 §3, unresolved.
3. **Zenodo license metadata** `apgl-v3` → `agpl-3.0` on four records — needs a
   token or the web UI. See `docs/tagging-and-mint-report.md`.
4. **`E35b` marks an unchanged paragraph** — drop the edit if that is unwanted.
5. **Headings are not visibly change-marked** — §4 above.
