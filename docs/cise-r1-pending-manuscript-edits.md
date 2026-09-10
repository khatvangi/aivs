# Pending manuscript edits — for the Job 5 patch list

Text decided during revision but **not yet applied**. `var_manuscript_cise.md`
remains unmodified; Job 5 owns it. Collected here so these passages are not
held only in conversation.

---

## 1. §4.3 final paragraph — replaces E23 (response-matrix row 3.9)

Author-approved 2026-09-08.

> Recomputation of the headline AUROCs was verified on 2026-03-16 and
> reproduced them to three decimal places. That verification ran in the
> authors' environment. During revision we found that the deposited copy could
> not have reproduced it: the first script in the chain reached a
> feature-computation module through a hardcoded absolute path into a separate,
> undeposited project, so a third party cloning the deposit would have failed
> at the first step. The module is now vendored into the repository with
> provenance, and self-containment was confirmed by running the pipeline from a
> clean export with the external path removed. No reported number is affected,
> because the outputs of that script were deposited; what was broken was
> re-execution, which is the property this section claims.

Supporting facts, all verified (see `deposit-repair-phase2-report.md` §5):
the module is `src/{sequence,grammar}.py`, 374 lines, vendored verbatim
(bodies md5 `42f1859b`, `ef414443`); the external project was
`condensate-maturation-theory`, not a git repository and deposited nowhere;
the failure was `ModuleNotFoundError: No module named 'src'`; script 03 is
upstream of `feature_matrix.csv` → scripts 04/05/06 → `esm2_features.csv` →
seventeen files.

---

## 2. §4.2 — sixth defect, inserted after the fifth finding

Author-drafted 2026-09-08.

> A sixth defect surfaced during revision, after review. The session-log
> adapter derived its search path by replacing path separators, but the tool it
> reads also collapses underscores and dots, so the adapter could not locate
> sessions for any project whose path contained an underscore, including this
> case study. It shipped because the test suite built its fixtures with the
> same wrong transformation: fixture and implementation agreed, and a test that
> reproduces the defect it guards cannot fail. Correcting the adapter caused
> four passing tests to fail, which is how the defect became visible. This is
> the fourth domain-independent failure in this list and the least visible,
> since every conventional signal said the code was covered.

### ✅ RESOLVED 2026-09-08 — the ordinal is correct; my earlier objection was wrong

I previously flagged "the fourth domain-independent failure in this list" as
unsupported, on the grounds that §4.2 never establishes the category. That was
based on the **submitted** `var_manuscript_cise.md`, where it does not.

`revision-patch-list.md` (now on disk) introduces it. **E19**, replacing line
99, adds:

> Three of the five are domain-independent. A model returning defaults instead
> of failing, an array initialized to a value that is also a legal prediction,
> and a test-time feature that encodes the label are failures available to any
> computational scientist.

That names exactly three — findings 1, 2 and 3 — and excludes findings 4 and 5
(untraced numerical claims, impossible probability). So the category exists in
the revised text, the count is three, and the adapter defect is the **fourth**.

**The draft paragraph's closing sentence is correct as written. No change
needed.** Disregard the two options I proposed.

### ⚠ What does need attention when this paragraph is folded in

E19's text says *"Three of the **five**"* and Table 2 (which E19 creates) has
**five** rows. Adding a sixth defect makes both stale:

- *"Three of the five are domain-independent"* → still true of the original
  five, but a reader who has just been given a sixth will read "the five" as an
  error. Needs rewording, e.g. *"Three of those five are domain-independent"*
  before the sixth is introduced, or *"Four of the six"* after it.
- Table 2's caption is *"Where each finding is recorded"* — a sixth finding
  omitted from it contradicts "each".
- The sixth defect is post-review, so its Table 2 row has no 2026-02-20 audit
  document. Its "Audit document" cell should name the revision audit, not a
  finding number that does not exist.

---

## 3. Table 2 — new row

**Correction:** Table 2 does not exist in the submitted manuscript. It is
*created* by **E19**, and its columns are *Finding · Stage · Disposition ·
Audit document · Corrected output* — not the check/failure-mode/judgment
columns I assumed. The new entry is therefore a **sixth row inside E19's
replacement text**, not a separate edit, and must use E19's columns:

| Finding | Stage | Disposition | Audit document | Corrected output |
|---|---|---|---|---|
| Adapter path derivation, mirrored by its own test fixture | S1 | adapter corrected; fixture re-derived independently; 8 regression tests | revision audit 2026-09-08 | `claude_code.py`, `test_adapters.py` |

Stage cell is a guess — E19's S-codes are assigned in the finding paragraphs
(S2, S4, S3, S5, S5) and the adapter defect has no stage yet. Assign one or
leave the cell blank.

Rationale: the generalisable check is not "run the tests" — the tests passed.
It is whether a fixture derives its expected values *independently of the
implementation under test*. Here both applied `replace("/", "-")`, so the suite
could only ever confirm the implementation against itself.

This is also the row that answers Reviewer 3's question about whether the
schema directs attention rather than merely storing findings: correcting the
implementation caused four green tests to fail, which is a detection produced
by the chain, not a record of one made elsewhere.

---

## 4. Reference changes settled in Job 4

- **PROV-AGENT primary DOI → `10.1109/escience65000.2025.00093`** (IEEE
  eScience 2025, pp. 467-473), with `arXiv:2508.02866` secondary. Upgrades the
  load-bearing prior-art citation from preprint to peer-reviewed, which
  strengthens §3.5 against Reviewer 3's "why not a profile of an existing
  standard" question.
- **Naser `arXiv:2603.03299` verified genuine** from four independent sources;
  the ID-month anomaly is arXiv-side. **No change to the reference.**
- Ten of twelve references carry a DOI; refs 1 (NIH notice) and 10 (W3C
  PROV-O) have none because that document type is not DOI-registered. Full
  table in `reference-dois.md`.
