# Deposit repair — phase 2 report

Run 2026-09-08 on host `boron`, for CiSE-2026-06-0105 (due 22 September 2026).

**Scope executed: Job 1 steps 1–5, plus the push.** On the author's instruction,
steps 6–9 were **deliberately not run**: no tag was created, no GitHub release
was made, and Zenodo was not contacted. Tagging and minting are deferred until
Jobs 2 and 3 land, because both change files that will be inside the archives —
Job 2 rewrites `examples/out/mechanism_classifier_audit*.json` in `aivs`, and
Job 3 changes `table_s1_regions.csv` in the idp repo and both Figure 1 assets.
Minting now would produce archives that are stale the day they are issued, which
is the failure this whole exercise is repairing.

**Consequence for the rest of the work order: there are no new version DOIs yet.**
Job 5 step 3 depends on them and is therefore blocked. Job 4 does not depend on
them (it resolves reference DOIs against CrossRef) and can proceed.

## Push result

| Repo | Before | After | Tags added |
|---|---|---|---|
| `khatvangi/idp-mechanism-classifier` | `3ca6dead` | **`f72f008`** | none |
| `khatvangi/aivs` | `daabff7b` | **`0e47e2a`** | none |

Feature branches also pushed: `cise-r1-deposit-repair` (idp, at `9eb1159`) and
`cise-r1-readme-fix` (aivs, at `0e47e2a`). Zenodo records `20723559` and
`20723561` are untouched and still point at the old commits.

Note: the idp feature branch sits one commit behind its master. The step 5
vendoring commit `f72f008` was made on `master` after the merge rather than on
the branch. The content is identical; only the branch pointer lags.

---

## Step 1 — divergence re-verified before acting

Re-ran the phase 1 checks against a fresh `git fetch`. **Unchanged in every
particular**, so the phase 1 analysis was not stale:

| Check | Phase 1 | Phase 2 re-check |
|---|---|---|
| Merge-base | `8f8b944` | `8f8b944` |
| Commits unique to `origin/master` | 2 | 2 |
| Remote-only work (`8f8b944..origin/master`) | 13 files, 2,888 insertions | 13 files, 2,888 insertions |
| `origin/master` HEAD | `3ca6dead` | `3ca6dead` |
| Ten overlap files: worktree vs `origin/master` | byte-identical | byte-identical (md5 re-checked, 10/10) |
| `CRITICAL_EVALUATION.md`, `manuscript/draft_from_kdense.md` | untracked, identical | untracked, identical |
| `LICENSE` | remote-only | remote-only |

## Step 2 — merge

Committed the worktree state first, in two units:

- `d571693` — the six paths already byte-identical to `origin/master`
  (`bootstrap_cis.csv` 20bb64f3, `results_section5_draft.md` b3cc2b70,
  `10_two_step_predictor.py` cdb1cf1b, `11_bootstrap_cis.py` dfb0969b,
  `CRITICAL_EVALUATION.md` 23e68174, `manuscript/draft_from_kdense.md` 74883ab0)
- `2a02213` — local-only work: `MANUSCRIPT_STATUS.md`, draft sections 1–4,
  `pathB/`, `exploratory/`. The last two are referenced by README's k-dense
  merge table, so without them the README pointed at directories absent from
  the deposit.

Then `git merge origin/master` → **`9eb1159`, clean, zero conflicts, one file
added: `LICENSE` (34,523 B).** Exactly the phase 1 prediction. Committing the
worktree first is what made it trivial: both sides then made *identical* changes
relative to `8f8b944`, which the ort strategy resolves silently. Merging first
would have produced ten conflicts with the same end state and ten chances to err.

Post-merge, `git merge-base --is-ancestor origin/master HEAD` → **true**: the
remote history is fully contained. Nothing was orphaned; `3ca6dead` remains
reachable, so both existing Zenodo deposits still resolve.

### One difference that looks like data loss and is not

`data/variants/variants_with_regions.csv` goes 3,410 → 779 lines across the
merge. Verified by md5 that no rows were lost:

| File | md5 | Equals |
|---|---|---|
| `origin/master:variants_with_regions.csv` | `8c3e704b` | `HEAD:variants_with_regions_full_vus.csv` (`8c3e704b`) |
| `HEAD:variants_with_regions.csv` | `1b1a62cd` | `HEAD:variants_with_regions_clean.csv` (`1b1a62cd`) |

The local branch redefined the bare filename to mean the clean primary set and
deposits both halves separately, exactly as README's "Dataset conventions"
section describes. Every row present on the remote survives in
`variants_with_regions_full_vus.csv`.

## Step 3 — merge to master

`master` fast-forwarded to `9eb1159`, 8 commits ahead of `origin/master`.
No rebase, no force-push.

## Step 4 — availability-statement verification

Zero absent. **260 tracked files on `master`, against 104 in the current
Zenodo deposit.**

| Item | Count | Status |
|---|---|---|
| Variant dataset (core) | 13/13 | PRESENT |
| EVE data (14 genes) | 14/14 | PRESENT |
| Analysis scripts `01`–`21` | 21/21 | PRESENT |
| Figure scripts | 10/10 | PRESENT |
| Figure outputs (`figure_1..6`, `figure_s1..s7`, png+pdf) | 26/26 | PRESENT |
| Environment manifest | 1/1 | PRESENT |
| README.md | 1/1 | PRESENT |
| LICENSE | 1/1 | PRESENT |
| Named data tables | 13/13 | PRESENT |
| kdense_predictors | 8/8 | PRESENT |

`requirements.txt` carries `torch>=2.0` (verified 2.9.1) and
`transformers>=4.30` (verified 4.57.6), Python 3.12.11, the ESM2 checkpoint
pinned by HF snapshot revision `08e4846e537177426273712802403f7ba8261b6c`, and
an explicit statement that **`fair-esm` is not a dependency** — the code loads
ESM2 through HuggingFace `transformers` (`EsmForMaskedLM`).

### Public reader view, re-checked unauthenticated after the push

Every path that returned 404 for Reviewers 3 and 5 now returns 200:

| Repo | Path | Before | After |
|---|---|---|---|
| idp | `scripts/figures` | 404 | **200** (10 files) |
| idp | `figures/paper` | 404 | **200** |
| idp | `requirements.txt` | 404 | **200** |
| idp | `README.md` / `/readme` | 404 | **200** |
| idp | `scripts/mutation` | 12 files | **21 files** |
| idp | `data/eve` | absent | **200** |
| idp | `src` | absent | **200** |
| aivs | `examples/out` | 200 but unnavigable | **200**, now named in README |
| aivs | README scope line | "Current scope (v0.1.0) … meta-schema only" | **"Current scope (v0.2.1)"** + "## Audit records" |

## Step 5 — the `src/` problem, and why the work order's premise was wrong

The work order said to locate a missing module and add it. **No module was
missing.** `scripts/mutation/03_disorder_and_features.py:15-19` and
`scripts/03_maturation_grammar.py:15-19` both reached the code through a
hardcoded absolute path:

```python
GRAMMAR_ROOT = Path("/storage/kiran-stuff/condensate-maturation-theory/condensate_maturation")
sys.path.insert(0, str(GRAMMAR_ROOT))
from src.sequence import ProteinSequence
from src.grammar import SequenceGrammar
```

`condensate-maturation-theory` is a **separate project**: not a git repository,
no remote, no LICENSE file, deposited nowhere, containing the unpublished
`maturation-theory-v6.md` / `v7.md`. The import succeeds on this host and fails
as `ModuleNotFoundError: No module named 'src'` for anyone holding only the
deposit.

Severity: `03_disorder_and_features.py` writes `feature_matrix.csv`, read by
scripts 04/05/06; script 06 writes `esm2_features.csv`, read by seventeen files
including every canonical output and all thirteen figures. The entire
re-execution path began at a script that could not run. Both of 03's outputs
*are* deposited, so the reported numbers are unaffected — this was a
re-execution defect, not a numbers defect.

Because this meant publishing part of a separate unpublished project rather than
restoring a lost file, the decision was referred to the author, who chose to
vendor.

**Resolution** (`f72f008`): copied `src/sequence.py` (94 lines) and
`src/grammar.py` (280 lines) into the repository, plus a package `__init__.py`.
Numpy-only, no transitive dependencies, used at three call sites
(`03:234`, `243-244`). Each carries a provenance header naming the origin path,
the vendoring date, the reason, and a warning not to fix analysis bugs in the
copy without reconciling upstream. Bodies verified **verbatim** against origin
(md5 `42f1859b` and `ef414443`). Both scripts now resolve the module from the
repository root.

**Verified self-contained.** `git archive master` was exported to a clean
directory (263 files) and the module imported with the external path removed
from `sys.path`, then exercised with the real `GRAMMAR_CONFIG` copied from
`03_disorder_and_features.py:167-177` on a real FUS LCD sequence.
`SequenceGrammar.compute_all()` returned its five matrices. Every remaining
`sys.path.insert` in the exported tree points inside the repository.

Same author; released here under the repository's AGPL-3.0.

---

## Deferred to the tagging pass (after Jobs 2 and 3)

1. Tag idp `v1.0-cise-r1`; GitHub release; Zenodo version under concept DOI
   `10.5281/zenodo.20723560`.
2. Tag aivs `v0.2.2-paper`; GitHub release; Zenodo version under concept DOI
   `10.5281/zenodo.20723558`.
3. Verify each minted archive's file listing against the step 4 table above.
4. Fix the malformed Zenodo license identifier on both records:
   `apgl-v3` → `agpl-3.0` (checklist A.9).
5. Update the version DOIs in `var_manuscript_cise.md` §157 and in the idp
   `README.md` Archived-releases table, which currently reads "version DOI to be
   updated in phase 2" in both places.
6. Fast-forward the idp `cise-r1-deposit-repair` branch to master, or delete it.

## Still open, carried from phase 1

- `aivs` has no `.gitignore` and tracks 16 `__pycache__/*.pyc` files.
- `aivs/pyproject.toml` still declares `version = "0.1.0"` at tag `v0.2.1-paper`
  with `META_SCHEMA_VERSION = "0.2.0"`.
- Audit records are not byte-reproducible (fresh `uuid4()` per run). Job 2
  regenerates them, so the documented md5s must be updated there.
- `requirements_kdense.txt` remains untracked, superseded by `requirements.txt`.
