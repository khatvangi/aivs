# Deposit repair — phase 1 report

Run 2026-09-01 on host `boron`, for CiSE-2026-06-0105 revision (due 22 Sep 2026,
internal target 5 Sep). Scope: **local only**. Nothing was pushed, no tag was
created or moved, no GitHub release was made, Zenodo was not contacted, and no
existing commit was rewritten, rebased or force-pushed. Both remotes are
unchanged: `khatvangi/aivs` master is still `daabff7b`, `khatvangi/idp-mechanism-classifier`
master is still `3ca6dead`.

Source checklist: `docs/deposit-verification-2026-08-27.md`, section 6, part A.

## Branches created

| Repo | Branch | Base | Commits |
|---|---|---|---:|
| `/storage/kiran-stuff/IDP_projects/mechanism_classifier` | `cise-r1-deposit-repair` | `reviewer-ready-mechanism` @ `10d85122` | 4 |
| `/storage/kiran-stuff/aivs` | `cise-r1-readme-fix` | `master` @ `daabff7b` | 3 |

---

## 1. Per checklist item

### Headline correction to the checklist's framing

The checklist measured everything against the **deposited tag** `v0.2.1-paper`
(= `3ca6dead` = GitHub master). Measured that way, 155 files look untracked.
Measured against the **local branch** `reviewer-ready-mechanism` @ `10d85122`,
most of them are already committed — they simply live on a branch that was
never pushed.

This materially changes the work. A.2 required no action at all, and A.3 and
A.4 were largely already done. The real defect is not "files were never
committed"; it is **"the branch holding them was never pushed, and the deposit
was cut from the other head."** That is a phase-2 problem, and it is the
divergence analysed in section 3.

### Repo 1 — `mechanism_classifier`, branch `cise-r1-deposit-repair`

**A.1 Environment manifest — DONE** (`c56eeb4`)

Added tracked `requirements.txt` (55 lines). `requirements_kdense.txt` was left
in place, untracked, rather than deleted.

Recorded: Python **3.12.11**; ESM2 checkpoint `facebook/esm2_t33_650M_UR50D`
pinned by HuggingFace Hub snapshot revision
**`08e4846e537177426273712802403f7ba8261b6c`**, read from the real HF cache at
`/storage/kiran-stuff/soft/hf_cache/hub/models--facebook--esm2_t33_650M_UR50D/snapshots/`.

Dependencies added that `requirements_kdense.txt` omitted, derived by grepping
every import in `scripts/`: `torch`, `transformers`, `xgboost`, `statsmodels`,
`umap-learn`.

> **Correction to the checklist.** A.1 (and verification-doc note (d)) asks for
> `fair-esm`. **The scripts do not use `fair-esm`.** They load ESM2 through
> HuggingFace `transformers` — `AutoTokenizer` + `EsmForMaskedLM.from_pretrained("facebook/esm2_t33_650M_UR50D")`
> in `scripts/mutation/06_approach_c_esm2.py:33`, `09_masked_marginals_fus.py:32-34`
> and `scripts/05_esm2_embeddings.py:26`. The `facebook/` org prefix is a
> HuggingFace Hub identifier; Meta's `fair-esm` package uses a different API
> (`esm.pretrained.esm2_t33_650M_UR50D()`) and is imported nowhere in the repo.
> Pinning `fair-esm` would have shipped a manifest installing a package the code
> never imports while still omitting the one it does. `transformers>=4.30` is
> pinned instead, and the manifest carries a comment saying explicitly that
> `fair-esm` is not a dependency. **This needs a matching correction wherever
> the manuscript or response matrix repeats the `fair-esm` claim.**

Version-honesty: no lockfile was captured when the analyses ran (2026-02 to
2026-03). The manifest uses `>=` floors as the reproducible contract and
carries the exact installed versions as `# verified` comments, under an
explicit header note that these were read from installed package metadata on
2026-09-01 and are **not** independently attested as the versions that produced
the originally reported numbers. No version was invented; every `# verified`
value came from `importlib.metadata.version()`.

**A.2 Figure scripts and outputs — ALREADY SATISFIED, no commit needed**

Verified on the branch: `scripts/figures/` = **10 tracked** scripts
(`fig1_mechanism_split.py` … `fig6_disorder_not_problem.py`,
`figS1_masked_marginals.py` … `figS4_gene_landscapes.py`);
`figures/paper/` = **26 tracked** files (`figure_1..6` and `figure_s1..s7`,
each `.png` + `.pdf`).

The brief expected `figure_s1..s4`; `s5`, `s6`, `s7` also exist. They are not
orphans: `figure_s5/s6/s7` are written by `scripts/mutation/17_random_region_control.py`,
`18_kappa_scd.py` and `19_fus_ortholog_conservation.py` respectively, all
tracked. Every figure output has deposited generating code.

**A.3 Missing analysis scripts — DONE** (`8aa7c10`)

`13_` … `19_` were already tracked. Added the two that were not:

- `scripts/mutation/20_cadd_revel_pp2.py` (809 lines) — CADD/REVEL/PolyPhen-2
  scoring via myvariant.info; referenced by README's six-predictor table
- `scripts/mutation/21_calibration.py` (295 lines) — reliability diagrams,
  Brier score, ECE

`13_`–`21_` is now complete. The two scripts the checklist called load-bearing —
`17_random_region_control.py` (FUS NLS p = 0.002) and `15_eve_comparison.py`
(EVE = 0.342) — were already tracked and are confirmed present.

**A.4 Data files — DONE** (`ca8451e`)

All twelve files A.4 names by hand were confirmed to **exist locally and be
already tracked**: `vus_excluded_sensitivity.csv`,
`variants_with_regions_full_vus.csv`, `results_two_step_by_mechanism.csv`,
`results_two_step_by_gene.csv`, `table_1_mechanism_split.csv`,
`variants_with_eve.csv`, `table_s1_regions.csv`, `table_s2_gene_summary.csv`,
`table_s3_features.csv`, plus `eve_comparison.csv`, `kappa_scd_results.csv`,
`fus_ortholog_nls.csv`. `data/eve/` = **14 tracked** `*_eve.csv` files (APP, AR,
CRYAB, HNRNPA1, HNRNPA2B1, LMNA, PRNP, SNCA, SOD1, SQSTM1, TARDBP, TIA1, TTR,
VCP). Nothing was missing; no placeholder was created.

The remaining A.4-class gap, from §3.1 of the checklist, was added:
`data/variants/kdense_predictors/` (8 files — the CADD/REVEL/PolyPhen-2 AUROC
results behind README's six-predictor table, including the sensitivity,
gnomAD-filtered, confirmed-only and with-CADD variants, plus the raw and scored
ClinVar CSVs and the gene summary), and `figures/calibration_reliability.png`,
the output of script 21.

**A.6 README — DONE** (`9e3d782`)

Extended the existing local `README.md` (which had never been pushed) with:
what the repository is; the manuscript citation (Ribbeck H and Kiran B,
CiSE-2026-06-0105, with corresponding author and ORCID); an **Archived releases**
table carrying concept DOI `10.5281/zenodo.20723560` and version DOI
`10.5281/zenodo.20723561`, with an explicit note that the version deposit is
stale, that the concept DOI is the one to cite, and that the version DOI is to
be updated in phase 2; a dedicated **"AIVS verification record — in the sibling
repository"** section naming `khatvangi/aivs`,
`examples/mechanism_classifier_audit.py` and
`examples/out/mechanism_classifier_audit{,_published}.json` — which is the
direct answer to Reviewer 3's misplaced item; an environment section pointing at
`requirements.txt`; and `pip install -r requirements.txt` at the head of the
reproduce block.

Also added a **Deliberate exclusions** section naming the two gitignored public
source tables as the *only* intended omissions (this is checklist item B.15,
which lands naturally here).

Note: this commit necessarily also carried the pre-existing uncommitted README
edits that were in the working tree when the branch was cut.

**A.10 Ignore compiled artefacts — ALREADY SATISFIED, no commit needed**

`.gitignore` already contains `__pycache__/`, `*.pyc` and `*.pyo` (lines 6–8).
Tracked compiled artefacts on the branch: **0**. At tag `v0.2.1-paper`: **0**.

The checklist's "16 compiled artefacts across the two archives" are **all in the
`aivs` repo**, not this one — see section 4.

### Repo 2 — `aivs`, branch `cise-r1-readme-fix`

**A.7 README scope — DONE** (`6a0cbcc`, plus addendum `0e47e2a`)

Replaced the false `## Current scope (v0.1.0)` block. It had claimed the release
"ships the meta-schema only" and listed "adapter implementations" as out of
scope, at a commit that ships meta-schema **0.2.0**, three adapters, JSON Schema
exports for both schema versions, and four completed audits. This is the finding
most likely to explain Reviewer 5.

Changes: scope rewritten to v0.2.1 enumerating what actually ships (the
vocabulary-still-near-empty statement was kept, because it is still true); new
**Audit records** section with a table of all four audits; new **Archived
releases** section with concept DOI `10.5281/zenodo.20723558` and version DOI
`10.5281/zenodo.20723559`; repository-layout block now lists `examples/`,
`schema/` and `docs/`, and no longer says the adapters directory has "no
implementations yet".

`examples/out/mechanism_classifier_audit_published.json` is named explicitly, as
a linked table row *and* in a standalone "if you arrived here from the AIVS-VAR
manuscript" paragraph that also cross-links `khatvangi/idp-mechanism-classifier`.

Table counts were read out of the emitted JSON, not transcribed:

| Audit | Tier | Events | Evidence | Decisions | Claims | Deltas |
|---|---:|---:|---:|---:|---:|---:|
| mechanism_classifier | 2 | 22 | 8 | 8 | 4 | 7 |
| smith_2026 | 3 | 12 | 13 | 11 | 5 | 9 |
| kiran_triplet_proof | 3 | 532 | 14 | 14 | 7 | 11 |
| kappa_friction | 3 | 380 | 12 | 10 | 7 | 7 |

**A.8 Figure assets — DONE** (`c4e185d`)

Finding as requested. `figures/figure_1.{png,pdf}` through
`figure_6.{png,pdf}` — **12 files, already tracked**. Not tracked, now added:
`figures/make_aivs_schema.py` (147 lines, generates the manuscript's Figure 1
schema diagram) and its two outputs `figures/figure_1_aivs_schema.{png,pdf}`.

**Verification.** `pytest tests/` → **37 passed**. `python -m examples.mechanism_classifier_audit`
runs and validates.

---

## 2. Expected but not found, and other findings

1. **`fair-esm` is not a dependency.** See A.1 above. The checklist is wrong on
   this point and the error should be corrected wherever it propagated.

2. **`src/` does not exist in the idp repo, but two scripts import from it.**
   `scripts/mutation/03_disorder_and_features.py:18-19` and
   `scripts/03_maturation_grammar.py:18-19` both do
   `from src.sequence import ProteinSequence` / `from src.grammar import SequenceGrammar`.
   There is no `src/` directory locally, it is not tracked, and it is not in the
   deposit. **Those two scripts cannot run as deposited.** This is a
   reproducibility hole the 2026-08-27 verification did not catch. It is not in
   the phase-1 brief and nothing was invented to fill it; `03_disorder_and_features.py`
   is on the manuscript path, so it needs a decision before resubmission.

3. **Audit records are not byte-reproducible.** Re-running
   `python -m examples.mechanism_classifier_audit` emits a structurally
   identical record — same 22 events, 8 evidence, 8 decisions, 4 claims, 7
   deltas — with entirely fresh `uuid4()` identifiers for `audit_id` and every
   event/evidence/decision id, so 218 lines differ and the checksum does not
   match. The deposited copies were **restored** and re-verified against the
   md5s in the 2026-08-27 document: `4aaac341a56d7bed17711a6dc8ec4d81` and
   `348ec95ed46c144f7efb6fd4cdc1c8b3`. Both match. The README now states this
   limitation openly (commit `0e47e2a`) and flags deterministic,
   content-addressed identifiers as an open schema item. A paper arguing for
   auditable provenance should not ship an artifact that silently fails
   checksum reproduction; better to disclose it than to have a reviewer find it.

4. **`aivs/pyproject.toml` still says `version = "0.1.0"`** while the release tag
   is `v0.2.1-paper` and `META_SCHEMA_VERSION` is `0.2.0`. Same class of staleness
   as A.7. Not changed — a package version bump is a release decision, not a
   documentation fix. Phase 2.

5. **The 16 tracked `__pycache__/*.pyc` files are in `aivs`, not in the idp repo,
   and `aivs` has no `.gitignore` at all.** A.10 assigned the cleanup to repo 1,
   where it was already done and there was nothing to clean. Untracking files in
   repo 2 is a deletion of tracked content and was outside the phase-1 brief, so
   it was not done. Phase 2.

6. **The idp working tree is dirty in a way that matters.** See section 3.

---

## 3. Divergence analysis — `idp-mechanism-classifier`

### The histories did not diverge the way the verification document implies

`3ca6dead` is indeed not an ancestor of `10d85122`, and `git diff v0.2.1-paper`
does report 132,669 insertions. Both facts are true and both are misleading,
because they compare branch *tips*. There is a clean shared ancestor.

```
                          ┌── dbea9d3 ── 3ca6dea   origin/master, tag v0.2.1-paper, GitHub HEAD
5cf3480 ── 4662223 ── 8f8b944
                          └── 10d8512               reviewer-ready-mechanism (local, never pushed)
```

| Question | Answer |
|---|---|
| Merge-base | **`8f8b9444841e4b7ea062915798b9633669de359e`** — exists, is clean |
| Commits unique to `origin/master` | **2** — `dbea9d3` (LICENSE), `3ca6dea` (audit-referenced evidence docs + verified script versions) |
| Commits unique to local HEAD | **1** — `10d8512` "Prepare reviewer-ready mutation manuscript package" |
| Real remote-only work | `git diff 8f8b944 origin/master` = 13 files, **2,888 insertions** — not 132,669 |

This is an ordinary two-headed divergence: `dbea9d3`+`3ca6dea` were committed
and pushed on `master`, while `10d8512` was committed separately on
`reviewer-ready-mechanism` from the same base. No history was rewritten.

### Does the remote contain anything not present locally?

**Files on `origin/master` and not in local HEAD's tree — 3:**

| File | Present in local *working tree*? |
|---|---|
| `LICENSE` (34,523 B, AGPL-3.0) | **NO** — genuinely absent |
| `CRITICAL_EVALUATION.md` | yes, untracked, **md5-identical** (`23e68174…`) |
| `manuscript/draft_from_kdense.md` | yes, untracked, **md5-identical** (`74883ab0…`) |

**Files both sides modified — 10.** Three-way md5 comparison (merge-base /
origin/master / local HEAD / local working tree):

| File | base | origin | HEAD | worktree | |
|---|---|---|---|---|---|
| `data/variants/bootstrap_cis.csv` | `d61590d6` | `20bb64f3` | `9a4325db` | `20bb64f3` | wt = origin |
| `data/variants/results_two_step.csv` | `52e60dbf` | `f9c45db4` | `f9c45db4` | `f9c45db4` | identical |
| `data/variants/variants_with_regions_clean.csv` | absent | `1b1a62cd` | `1b1a62cd` | `1b1a62cd` | identical |
| `docs/2026-02-20-audit-code-science-logic.md` | absent | `0db5e843` | `0db5e843` | `0db5e843` | identical |
| `docs/paper/results_section5_draft.md` | absent | `b3cc2b70` | `c9c4bb09` | `b3cc2b70` | wt = origin |
| `scripts/mutation/04_approach_a_xgboost.py` | `87757602` | `1775ea74` | `1775ea74` | `1775ea74` | identical |
| `scripts/mutation/06_approach_c_esm2.py` | `2cd61d5e` | `b92d96d3` | `b92d96d3` | `b92d96d3` | identical |
| `scripts/mutation/08_mechanism_aware_model.py` | `9028cd1f` | `716481f3` | `716481f3` | `716481f3` | identical |
| `scripts/mutation/10_two_step_predictor.py` | `36aca6b6` | `cdb1cf1b` | `1926746b` | `cdb1cf1b` | wt = origin |
| `scripts/mutation/11_bootstrap_cis.py` | `6673b75a` | `dfb0969b` | `3df13140` | `dfb0969b` | wt = origin |

**For all ten, the local working tree is byte-identical to `origin/master`.**

### Why the divergence exists

The evidence reads unambiguously. `10d8512` was committed *before* the remote's
`3ca6dead` content reached this checkout. Afterwards, the remote's versions of
those ten files were brought into the working tree — checked out or copied —
and **never committed**. Same for `CRITICAL_EVALUATION.md` and
`manuscript/draft_from_kdense.md`, which sit untracked and byte-identical to
their remote copies. Only `LICENSE` was never brought across at all.

So: **the working tree is already a content superset of `origin/master`, minus
`LICENSE`.** The divergence is a bookkeeping artefact, not a content conflict.
Nothing on the remote is at risk.

### Recommendation — merge. Do not force-push.

**Recommended sequence for phase 2** (not executed):

1. On `cise-r1-deposit-repair`, commit the working-tree state that already
   matches `origin/master` — the ten modified files plus untracked
   `CRITICAL_EVALUATION.md` and `manuscript/`. This is what makes the merge
   trivial, and it is currently the single largest loose end.
2. `git merge origin/master`. Expect it to be **clean**. For the ten overlap
   files both sides now make the *same* change relative to `8f8b944`, and git
   auto-resolves identical changes. `CRITICAL_EVALUATION.md` and
   `manuscript/draft_from_kdense.md` become add/add with identical content —
   also auto-resolved. `LICENSE` is a clean one-sided add.
3. Resolve `docs/paper/results_section5_draft.md` deliberately if it does
   conflict — it is the one file where HEAD (`c9c4bb09`) and the worktree
   (`b3cc2b70`) genuinely disagree and a human should pick.
4. Verify `LICENSE` landed, then fast-forward `master` and push.

**Risk: LOW.** Every byte on the remote either already exists in the working
tree or is a clean one-sided addition. Nothing can be lost. The failure mode is
a merge conflict, which is recoverable, not data loss.

**Risk of the alternatives, for the record:**

- *Fresh branch and merge* — same result, more ceremony, no added safety. The
  merge-base is clean; a fresh branch buys nothing a `git merge` on the repair
  branch does not already give.
- *Documented force-push* — **rejected.** The precondition stated in the brief
  ("if and only if the remote provably contains nothing unique") **fails**:
  `LICENSE` exists only on the remote. Force-pushing would delete the AGPL-3.0
  license text from a repository the manuscript cites as AGPL-licensed, and
  would orphan `3ca6dead`, which is the commit both the GitHub release and the
  Zenodo deposit `10.5281/zenodo.20723561` are minted from. Do not do this.

**No action was taken on this recommendation.**

### `aivs` divergence: none

`v0.2.1-paper` (`8406bca6`) is an ancestor of local `master` `daabff7b`, nine
commits back. Local `master` == `origin/master`. Nothing to reconcile.

---

## 4. Remaining for phase 2

**Blocking, deposit-side:**

1. Commit the idp working-tree state matching `origin/master` (10 modified
   files + `CRITICAL_EVALUATION.md` + `manuscript/`), then `git merge origin/master`
   per section 3. Confirm `LICENSE` is present afterwards.
2. Decide `docs/paper/results_section5_draft.md` if it conflicts.
3. Merge `cise-r1-deposit-repair` into idp `master` and push.
4. Merge `cise-r1-readme-fix` into aivs `master` and push.
5. Cut a new tag on idp `master`, create the GitHub release, mint the new Zenodo
   version under concept DOI `10.5281/zenodo.20723560` (checklist A.5).
6. Cut a new tag on aivs `master`, release, mint under concept DOI
   `10.5281/zenodo.20723558` (checklist A.8, deposit half).
7. Update the version DOIs in `var_manuscript_cise.md` §157 **and** in the idp
   `README.md` Archived-releases table, which currently says "to be updated in
   phase 2" in both places.
8. Deposit the aivs-side manuscript figures and `supplementary_information.md`
   (checklist A.8) — the SI is promised in §157 and is in no deposit.
9. Fix the Zenodo license identifier on both records: `apgl-v3` → `agpl-v3`
   (checklist A.9).
10. Add `.gitignore` to `aivs` and untrack its 16 `__pycache__/*.pyc` files
    (checklist A.10, misassigned to repo 1; nothing to do there).

**Blocking, manuscript-side — untouched in phase 1, all in `var_manuscript_cise.md`:**

11. B.11 — rewrite the line-105 parenthetical about access-controlled session logs.
12. B.12 — split the availability statement so each item points at the deposit
    that holds it.
13. B.13 — do not report a person-hours/audit-cost figure derived from destroyed
    session telemetry.
14. B.14 — re-verify §4.3's "reproduces every headline AUROC to three decimal
    places" against the *new* deposit.
15. **New, from this pass:** correct every `fair-esm` reference to `transformers`.
16. **New, from this pass:** resolve the missing `src/` package, or drop
    `scripts/mutation/03_disorder_and_features.py` from the reproduce path.

**Non-blocking:**

17. `aivs/pyproject.toml` version `0.1.0` → `0.2.1`.
18. Deterministic, content-addressed audit identifiers so records reproduce by
    checksum (v0.3 schema item).
19. `examples/mechanism_classifier_audit.py` corrections — a separate task,
    deliberately untouched here.
