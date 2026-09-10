# Deposit verification — CiSE-2026-06-0105 (GATE-DEPOSIT)

Verification run 2026-08-28 from host `boron`. Read-only: four Zenodo GET
requests, two deposit downloads, unauthenticated GitHub API GETs, and local
filesystem/git inspection. No repository, deposit, or manuscript was modified.

Triggered by Reviewer 3 ("the data availability statement lists four items ...
that do not appear in the deposit it cites") and Reviewer 5 ("I had to hunt
through git repos to find records"). Both reviewers are correct. This document
records what was verified, not what was inferred.

**Headline.** Both Zenodo records are GitHub-release source archives, so their
contents are exactly the git tree at each tag — nothing more. The
`idp-mechanism-classifier` deposit was cut from a commit that predates roughly
133,000 lines of the work the manuscript describes. Of the five items the
availability statement promises there, one is absent outright, one is in the
other deposit, and two are present only in a stale form that does not support
the manuscript's current numbers. The access-controlled session-log deposit
claimed at line 105 does not exist, and the primary evidence it would have
contained has been destroyed.

---

## 1. Verdict table — the five promised items

Promised at `var_manuscript_cise.md:157`: *"The variant dataset, analysis and
figure-generation scripts, environment manifest, and AIVS verification record
for this manuscript are at https://github.com/khatvangi/idp-mechanism-classifier
and archived at Zenodo: version DOI 10.5281/zenodo.20723561."*

| # | Item | Promised location | Actual location | Status |
|---|---|---|---|---|
| a | Variant dataset | Zenodo 20723561 | Zenodo 20723561 → `data/variants/` (19 files) and `data/sequences/`, `data/disorder/`, `data/alphamissense/am_our_genes.csv` | **PRESENT** (stale — see note a) |
| b | Analysis scripts | Zenodo 20723561 | Zenodo 20723561 → `scripts/02–10_*.py`, `scripts/mutation/01–12_*.py` | **PRESENT** (incomplete — see note b) |
| c | Figure-generation scripts | Zenodo 20723561 | Nowhere in either deposit. Local only, untracked: `/storage/kiran-stuff/IDP_projects/mechanism_classifier/scripts/figures/` (10 scripts) | **ABSENT** |
| d | Environment manifest | Zenodo 20723561 | Nowhere in either deposit. Local only, untracked: `requirements_kdense.txt` (16 lines) | **ABSENT** |
| e | AIVS verification record | Zenodo 20723561 | Zenodo **20723559** → `examples/mechanism_classifier_audit.py` + `examples/out/mechanism_classifier_audit.json` + `examples/out/mechanism_classifier_audit_published.json` | **MISPLACED** |

### Note (a) — the deposited variant dataset does not support the manuscript's numbers

Present, verified by name in the archive listing: `clinvar_idp_missense.csv`
(529,096 B), `clinvar_train_ready.csv` (108,918 B), `variants_with_regions.csv`
(802,127 B), `variants_with_regions_clean.csv` (188,457 B),
`variants_with_alphamissense.csv` (749,565 B), `esm2_features.csv`,
`feature_matrix.csv`, `bootstrap_cis.csv` (4,649 B), `results_two_step.csv`
(558 B), `fus_masked_marginals.csv`, `fus_masked_logprobs.npy`, and eight
others.

Absent, though the manuscript's §4.2/§4.4 numbers depend on them:

- `data/variants/vus_excluded_sensitivity.csv` and
  `data/variants/variants_with_regions_full_vus.csv` — the clean-label vs
  VUS-included split. §4.2 turns on exactly this distinction (0.772 vs 0.70;
  0.873 vs 0.766).
- `data/variants/results_two_step_by_mechanism.csv`,
  `results_two_step_by_gene.csv`, `table_1_mechanism_split.csv` — the
  mechanism-stratified table §4.2 says the correction is "now disclosed ... in
  the mechanism-split table".
- `data/eve/*_eve.csv` (14 genes) and `data/variants/variants_with_eve.csv` —
  §4.4 reports EVE AUROC = 0.342. No EVE data is deposited.
- `data/variants/kappa_scd_results.csv`, `fus_ortholog_nls.csv`,
  `table_s1_regions.csv`, `table_s2_gene_summary.csv`, `table_s3_features.csv`,
  and the whole `kdense_predictors/` results set (8 files).

Additionally, `data/variants/bootstrap_cis.csv` is *modified in the local tree
relative to the deposited tag*, so the deposited copy is not the one the
manuscript's confidence intervals were read from.

### Note (b) — analysis scripts stop at 12 of 21

Deposited: `scripts/mutation/01_download_clinvar.py` through
`12_alphamissense_comparison.py`. Absent: `13_boundary_sensitivity.py`,
`14_physics_calculations.py`, `15_eve_comparison.py`,
`16_supplementary_tables.py`, `17_random_region_control.py`, `18_kappa_scd.py`,
`19_fus_ortholog_conservation.py`, `20_cadd_revel_pp2.py`,
`21_calibration.py`.

Two of these are load-bearing for §4.4 as written:
`17_random_region_control.py` is the 10,000-permutation length-matched random-region
control behind "FUS NLS ... p = 0.002", and `15_eve_comparison.py` is behind
"EVE = 0.342". Also, `03_disorder_and_features.py`, `09_masked_marginals_fus.py`
and `12_alphamissense_comparison.py` differ between the deposited tag and the
local tree (`12_` by 112 lines), so the deposited versions are not the ones that
produced the reported results.

### Note (c) — no figure-generation scripts for the paper's figures

The deposit contains plotting code inside older exploratory scripts
(`scripts/06_integrate_landscape.py`, `07_permutation_test.py`,
`08_improved_figures.py`, `10_redundancy_removal.py`, and figure calls inside
`scripts/mutation/04,05,06,07,08,10`), which emit `figures/*.png` such as
`fig1_landscape_biplot.png` and `two_step_predictor.png`.

It contains none of the scripts that generate the manuscript's actual figures.
Verified locally: `scripts/figures/fig1_mechanism_split.py` … `fig6_disorder_not_problem.py`
and `figS1_masked_marginals.py` … `figS4_gene_landscapes.py` write to
`PROJECT/"figures"/"paper"` producing `figure_1..6.{png,pdf}` and
`figure_s1..s4.{png,pdf}`. Neither those scripts nor the `figures/paper/`
outputs (26 files) are in the deposit or in the public repo
(`GET .../contents/scripts/figures` → HTTP 404; `.../contents/figures/paper` →
HTTP 404).

### Note (d) — no environment manifest of any kind

Searched the complete 104-file deposit listing for `requirements*`,
`environment.y*ml`, `pyproject*`, `Pipfile`, `setup.py`, `setup.cfg`, `conda`,
`poetry`, `renv`, `*.lock`, `Dockerfile`, `*.toml`. **Zero matches.** The
promise is unmet in full, not partially.

A manifest does exist locally — `requirements_kdense.txt`, 16 lines, pinning
`numpy>=1.24`, `pandas>=2.0`, `scipy>=1.10`, `scikit-learn>=1.3`,
`matplotlib>=3.7`, `requests>=2.28`, `metapredict>=3.0`, `localcider`, with
`openmm>=8.0` commented out. It is untracked in git and therefore was never
deposited. Note it does not pin `torch`/`fair-esm`, which the ESM2 steps require.

(For contrast, the *aivs* deposit does carry `pyproject.toml`, 545 B.)

### Note (e) — the AIVS verification record is in the other deposit

Confirmed present in Zenodo **20723559** (`khatvangi/aivs`), byte-identical to
the local working tree:

| File | Size | MD5 (deposit) | MD5 (local) | Match |
|---|---:|---|---|---|
| `examples/mechanism_classifier_audit.py` | 29,504 | `9481d9d178bfea76a3260b8a7ad2a64e` | `9481d9d178bfea76a3260b8a7ad2a64e` | identical |
| `examples/out/mechanism_classifier_audit.json` | 35,564 | `4aaac341a56d7bed17711a6dc8ec4d81` | `4aaac341a56d7bed17711a6dc8ec4d81` | identical |
| `examples/out/mechanism_classifier_audit_published.json` | 32,156 | `348ec95ed46c144f7efb6fd4cdc1c8b3` | `348ec95ed46c144f7efb6fd4cdc1c8b3` | identical |

> **SUPERSEDED 2026-09-08.** The md5s above were correct on 2026-08-27 and are
> retained as the dated record of that verification. The audit record was
> corrected under Job 2 (capture tier 2 → 1, retrospective wording, AIVS-VAR
> purge, superseded dispositions) and regenerated, so the deposited copies no
> longer match these values. Current checksums are in
> `docs/audit-record-corrections.md`. Do not update this table; it documents
> what was true at the time of the verification run.

Content of the published record, read from the deposited copy:
`audit_id` `df8ec271-f26b-44f2-acfd-6bf87a8d7ed8`; `meta_schema_version` 0.2.0;
`vocabulary_version` 0.1.0; `capture_tier_achieved` 2; `audit_timestamp`
2026-06-04T00:00:00Z; `audit_target` `repo:github.com/khatvangi/idp-mechanism-classifier
(mechanism_classifier; AIVS-VAR case study)`; 22 events, 8 evidence, 8 decisions,
4 claims, 7 schema deltas, 2 adapters (`manual` tier 2, `git` tier 1).

Confirmed **absent** from Zenodo 20723561: a search of that deposit's listing
for `aivs|audit|provenance|verification` returns exactly one hit,
`docs/2026-02-20-audit-code-science-logic.md`. That is the project's own manual
code/science audit memo — one of the two source documents the AIVS record was
built *from* — not the AIVS verification record itself.

This single misdirection accounts for one of Reviewer 3's four items. It does
not account for (c) or (d), which are absent from both deposits.

---

## 2. Zenodo records — full listings

API reachable from this host. Four plain `GET https://zenodo.org/api/records/<id>`
requests, all **HTTP 200**. No fallback to the human-readable pages was needed.

The four DOIs are two concept/version pairs, not four distinct records. Each
concept-DOI request resolves to (returns the JSON of) its latest version record,
which is why 20723560 returns the 20723561 payload and 20723558 returns 20723559.

### Record 20723561 — version record (idp-mechanism-classifier)

| Field | Value |
|---|---|
| Resolves | HTTP 200 |
| Title | `khatvangi/idp-mechanism-classifier: v0.2.1-paper — AIVS-VAR manuscript companion deposit` |
| Version DOI | 10.5281/zenodo.20723561 |
| Concept DOI | 10.5281/zenodo.20723560 (`conceptrecid` 20723560) |
| Relationship | version index 0, `is_last: true`, parent recid 20723560 |
| Publication date | 2026-06-16 |
| Version string | `v0.2.1-paper` |
| Access right | `open` |
| Embargo date | none |
| Access conditions | none |
| Resource type | Software |
| License id | `apgl-v3` *(malformed — should be `agpl-v3`)* |

Complete file listing — **1 file**:

| Filename | Size (bytes) | Checksum |
|---|---:|---|
| `khatvangi/idp-mechanism-classifier-v0.2.1-paper.zip` | 7,600,698 | `md5:2a9b852474eeddafaa1ef7b210f2a17e` |

Downloaded and re-hashed locally: `2a9b852474eeddafaa1ef7b210f2a17e` — matches.
Archive comment records source commit `3ca6dead843b9200201e2cba8c318161fc96aa25`.
Expands to 119 entries / 104 regular files under
`khatvangi-idp-mechanism-classifier-c858090/`.

Deposit contents (104 files, prefix stripped):

```
.gitignore  ANALYSIS.md  CRITICAL_EVALUATION.md  LICENSE  LITERATURE_SYNTHESIS.md
PHASE3_CRITIQUE.md  PLAN.md  PROJECT.md  SESSION_LOG_2026-02-19.md  VALIDATION.md
data/alphamissense/am_our_genes.csv
data/disorder/per_residue_disorder.csv
data/sequences/all_proteins.fasta  data/sequences/protein_info.csv
data/variants/  alphamissense_comparison.csv  bootstrap_cis.csv
    clinvar_idp_missense.csv  clinvar_train_ready.csv  esm2_features.csv
    feature_importance_a.csv  feature_importance_combined.csv  feature_matrix.csv
    fus_masked_logprobs.npy  fus_masked_marginals.csv  predictions_approach_a.csv
    regional_esm2_analysis.csv  results_approach_a.csv  results_approach_b.csv
    results_approach_c.csv  results_two_step.csv  variants_with_alphamissense.csv
    variants_with_regions.csv  variants_with_regions_clean.csv
docs/2026-02-20-audit-code-science-logic.md
docs/paper/results_section5_draft.md
docs/plans/2026-02-19-idp-mutation-vulnerability-design.md
docs/plans/2026-02-19-idp-mutation-vulnerability-plan.md
docs/plans/2026-02-19-paper-outline.md
features/  amyloid_propensity.csv  combined_features.csv  esm2_embeddings.npy
    esm2_embeddings_summary.csv  esm2_names.txt  maturation_grammar.csv
    pca_loadings.csv  pca_loadings_reduced_all.csv  pca_loadings_reduced_interp.csv
    polymer_physics.csv  reduced_features.txt
figures/  (28 PNGs: approach_a_xgboost, approach_b_stratified,
    approach_c_esm2_comparison, axis_separation, deep_dive_* x11,
    feature_correlations, fig1_landscape_biplot, fig2_maturation_grammar,
    fig3_amyloid_vs_maturation, fig4_feature_comparison, landscape_no_esm2,
    landscape_reduced_all, landscape_reduced_interp,
    mechanism_aware_llr_distributions, mechanism_landscape_pca,
    mutation_effects, permutation_test, permutation_test_wt_only,
    permutation_wt_reduced_all, permutation_wt_reduced_interp,
    radar_mechanism_profiles, two_step_predictor)
manuscript/draft_from_kdense.md
scripts/  02_polymer_physics.py  03_maturation_grammar.py  04_amyloid_propensity.py
    05_esm2_embeddings.py  06_integrate_landscape.py  07_permutation_test.py
    08_improved_figures.py  09_expand_panel.py  10_redundancy_removal.py
scripts/mutation/  01_download_clinvar.py  02_fetch_sequences.py
    03_disorder_and_features.py  04_approach_a_xgboost.py
    05_approach_b_stratified.py  06_approach_c_esm2.py  07_deep_dive_failures.py
    08_mechanism_aware_model.py  09_masked_marginals_fus.py
    10_two_step_predictor.py  11_bootstrap_cis.py  12_alphamissense_comparison.py
sequences/all_proteins.fasta
```

**No `README.md`.** **No environment manifest.** **No `scripts/figures/`.**
**No `figures/paper/`.**

### Record 20723560 — concept record (idp-mechanism-classifier)

Resolves HTTP 200. Returns the 20723561 payload verbatim (`id: 20723561`,
`doi: 10.5281/zenodo.20723561`), i.e. it is the concept DOI resolving to the
single, latest version. Only one version exists in this concept group.
File listing identical to 20723561 above.

### Record 20723559 — version record (aivs)

| Field | Value |
|---|---|
| Resolves | HTTP 200 |
| Title | `khatvangi/aivs: AIVS v0.2.1 — Patterns manuscript deposit` |
| Version DOI | 10.5281/zenodo.20723559 |
| Concept DOI | 10.5281/zenodo.20723558 (`conceptrecid` 20723558) |
| Relationship | version index 0, `is_last: true`, parent recid 20723558 |
| Publication date | 2026-06-16 |
| Version string | `v0.2.1-paper` |
| Access right | `open` |
| Embargo date | none |
| Access conditions | none |
| Resource type | Software |
| License id | `apgl-v3` *(malformed — should be `agpl-v3`)* |

Complete file listing — **1 file**:

| Filename | Size (bytes) | Checksum |
|---|---:|---|
| `khatvangi/aivs-v0.2.1-paper.zip` | 2,925,436 | `md5:95797cb05b8dd74aa2d8e3de3ada7ac3` |

Downloaded and re-hashed locally: `95797cb05b8dd74aa2d8e3de3ada7ac3` — matches.
Archive comment records source commit `8406bca6f1a554511cd8969d20d35831f81b2416`.
Expands to 85 entries / 65 regular files under `khatvangi-aivs-86336e8/`.

Deposit contents (65 files, prefix stripped):

```
CHANGELOG.md  CLAUDE.md  HISTORY.md  LICENSE  NEXT.md  README.md
pyproject.toml  var_manuscript.md
docs/case_studies/README.md  smith_2026_jce_main.pdf  smith_2026_jce_si.pdf
docs/chat_handling_protocol.md
docs/origins/README.md  brainstorming-session.md  design-conversation.md
docs/origins/distribution-archives/aivs-0.1.0.zip
    kiran-triplet-audit-0.1.0.zip  smith-audit-0.1.0.zip
docs/positioning/prov-agent-alignment.md
examples/__init__.py  kappa_friction_audit.py  kiran_triplet_proof_audit.py
    mechanism_classifier_audit.py  minimal_audit.py  run_claude_code_adapter.py
    smith_2026_audit.py
examples/out/  kappa_friction_audit.json  kappa_friction_audit_published.json
    kiran_triplet_proof_audit.json  kiran_triplet_proof_audit_published.json
    mechanism_classifier_audit.json  mechanism_classifier_audit_published.json
    smith_2026_audit.json  smith_2026_audit_published.json
examples/__pycache__/  (5 .pyc files — build artefacts, should not be deposited)
schema/audit_artifact-0.1.0.json  audit_artifact-0.2.0.json
src/aivs/__init__.py
src/aivs/adapters/__init__.py  aider.py  base.py  claude_code.py  codex.py
src/aivs/meta_schema/__init__.py  core.py
src/aivs/vocabulary/__init__.py  v0_1.py
src/aivs/__pycache__/, adapters/__pycache__/, meta_schema/__pycache__/ (8 .pyc)
tests/__init__.py  test_adapters.py  test_meta_schema.py
tests/__pycache__/ (3 .pyc)
```

**No `figures/` directory** — the manuscript's own Figures 1–6 are not deposited.

### Record 20723558 — concept record (aivs)

Resolves HTTP 200. Returns the 20723559 payload verbatim (`id: 20723559`).
File listing identical to 20723559 above.

---

## 3. Local-vs-deposit diffs

### 3.1 `idp-mechanism-classifier` (Step 3)

**Deposit ≡ git tag.** File-name diff of the 104 deposit entries against
`git ls-tree -r --name-only v0.2.1-paper` (104 entries): **empty**. The deposit
is exactly the tagged tree, no additions or omissions.

**Which commit the deposit corresponds to.** Verified three independent ways,
all agreeing:

| Source | Value |
|---|---|
| ZIP archive comment | `3ca6dead843b9200201e2cba8c318161fc96aa25` |
| `git rev-parse v0.2.1-paper^{commit}` (local) | `3ca6dead843b9200201e2cba8c318161fc96aa25` |
| GitHub `master` HEAD | `3ca6dead843b9200201e2cba8c318161fc96aa25` |

Commit message: *"Add AIVS-audit-referenced evidence documents + verified script
versions"*, dated 2026-06-16T20:51:41Z. The annotated tag object is
`c8580905f47ad3bfb720157ade4638a3491e4bb7` (the `c858090` in the ZIP directory
name is the *tag object*, not the commit).

**Local divergence.** Local HEAD is `10d85122ded1c33dcc26f6cabb9b9a96e827461f`
("Prepare reviewer-ready mutation manuscript package"). The deposited commit is
**not an ancestor** of local HEAD (`git merge-base --is-ancestor` → false), so
the two histories have diverged; this is not a simple fast-forward. `git diff
v0.2.1-paper` against the working tree reports **87 files changed, 132,669
insertions, 4,291 deletions**.

**In deposit, absent locally** — 1 file:

- `LICENSE` (34,523 B). The AGPL text is in the deposit and on GitHub but not in
  the local working tree.

**Present locally, absent from deposit** — 155 files (excluding `__pycache__`).

*Legitimately excluded per the brief (gitignored large public source tables) — 2:*

- `data/variant_summary.txt.gz`
- `data/alphamissense/AlphaMissense_aa_substitutions.tsv.gz`

*Everything below is a real gap, not a deliberate exclusion:*

| Group | Files | Notes |
|---|---:|---|
| `scripts/figures/*.py` | 10 | fig1–fig6, figS1–figS4. **Item (c).** |
| `scripts/mutation/13_–21_*.py` | 9 | includes `17_random_region_control.py`, `15_eve_comparison.py`. **Item (b) gap.** |
| `figures/paper/*.{png,pdf}` | 26 | figure_1–6 + figure_s1–s7 |
| `data/eve/*_eve.csv` | 14 | APP, AR, CRYAB, HNRNPA1, HNRNPA2B1, LMNA, PRNP, SNCA, SOD1, SQSTM1, TARDBP, TIA1, TTR, VCP |
| `data/variants/` additions | 12 | `variants_with_eve.csv`, `eve_comparison.csv`, `variants_with_regions_full_vus.csv`, `vus_excluded_sensitivity.csv`, `results_two_step_by_gene.csv`, `results_two_step_by_mechanism.csv`, `table_1_mechanism_split.csv`, `table_s1_regions.csv`, `table_s2_gene_summary.csv`, `table_s3_features.csv`, `kappa_scd_results.csv`, `fus_ortholog_nls.csv` |
| `data/variants/kdense_predictors/` | 8 | 4 AUROC JSONs incl. sensitivity/gnomad/CADD variants, 2 CSVs, gene summary |
| `docs/paper/results_section*_draft.md` | 5 | sections 1,2,3,4,6 (only section 5 is deposited) |
| `README.md` | 1 | **not in deposit and not on GitHub** |
| `requirements_kdense.txt` | 1 | **Item (d).** |
| `MANUSCRIPT_STATUS.md`, `CLAUDE.md` | 2 | |
| `manuscript/PROVENANCE.md` | 1 | |
| `figures/calibration_reliability.png` | 1 | |
| `pathB/**` | 25 | separate analysis path incl. `PROVENANCE.md`, `README.md` |
| `exploratory/**` | 37 | eight-protein exploratory set incl. `PROVENANCE.md` |

Additionally, four tracked files differ between the deposited tag and the local
tree — `data/variants/bootstrap_cis.csv`, `scripts/mutation/03_disorder_and_features.py`,
`09_masked_marginals_fus.py`, `12_alphamissense_comparison.py` — plus
`figures/two_step_predictor.png` (133,348 → 125,385 B). The deposited copies are
therefore not the versions that produced the manuscript's reported values.

### 3.2 `aivs` (Step 4)

**Deposit ≡ git tag.** File-name diff of the 65 deposit entries against
`git ls-tree -r --name-only v0.2.1-paper` (65 entries): **empty**.

**Which commit.** ZIP archive comment `8406bca6f1a554511cd8969d20d35831f81b2416`
= `git rev-parse v0.2.1-paper^{commit}`. The annotated tag object is
`86336e887e0e2311964e18125edbd4dd173280d9`. Unlike the idp repo, this commit
**is** an ancestor of local HEAD `daabff7b80792b975c7ff00a8c5f37848367084d`,
nine commits back.

**In deposit, absent locally: none.** Every deposited file exists in the local
working tree.

**Explicitly confirmed present in the deposit (the Step 4 question):**

- `examples/mechanism_classifier_audit.py` — **present**, 29,504 B,
  md5 `9481d9d178bfea76a3260b8a7ad2a64e`, byte-identical to local.
- `examples/out/` — **present in full**, all 8 JSON files:
  `kappa_friction_audit.json` (398,324), `kappa_friction_audit_published.json`
  (393,639), `kiran_triplet_proof_audit.json` (559,417),
  `kiran_triplet_proof_audit_published.json` (558,759),
  `mechanism_classifier_audit.json` (35,564),
  `mechanism_classifier_audit_published.json` (32,156),
  `smith_2026_audit.json` (39,421), `smith_2026_audit_published.json` (38,627).
  The two mechanism_classifier JSONs were md5-verified byte-identical to local
  (table in §1 note e).

**Present locally, absent from deposit** — all post-tag manuscript-production
artefacts, which is expected for a tag cut on 2026-06-16, but two of these
matter for the submission:

| File(s) | Bearing |
|---|---|
| `var_manuscript_cise.{md,docx,pdf}`, `Var-manuscript-mse.md` | the CiSE revision itself |
| `figures/figure_1.{png,pdf}` … `figure_6.{png,pdf}`, `figure_1_aivs_schema.{png,pdf}`, `figures/make_aivs_schema.py` | **the manuscript's own figures and their generating script are in no deposit** |
| `supplementary_information.{md,docx}` | §157 says "This paper's own AIVS verification trail is provided in the supplemental information" — the SI is not deposited |
| `tables.{md,docx,pdf}`, `cover_letter.*`, `declaration_of_interests.*` | submission packaging |
| `docs/audit-cost-summary.md`, `docs/audit-cost-sessions.csv` | the retention-loss finding (see §4) |
| `docs/cise-r1-response-matrix.md`, `docs/cise-submission-guidelines.md`, `docs/qss-submission-guidelines.md` | working docs |
| `apply_qss_revisions.py`, `*.bak`, `.pytest_cache/*` | working artefacts, correctly undeposited |

Separately, both deposits contain compiled `__pycache__/*.pyc` build artefacts
(5 in `examples/`, 8 under `src/`, 3 under `tests/`) that should not be in an
archival software deposit.

---

## 4. Verdict on the access-controlled session-log deposit (Step 5)

Claim under test — `var_manuscript_cise.md:105`: *"The agent-session logs
(bulk-referenced by byte-size and session-id and deposited under access control)
provide the operator's invocation history."*

### VERDICT: **DOES NOT EXIST.**

Both limbs of the parenthetical are false as applied to the case-study record.
This is not a "cannot be determined" — six independent lines of evidence
converge, and one of them is the deposited audit record contradicting the
sentence in its own `notes` field.

**Evidence 1 — no Zenodo record is restricted or embargoed.** All four records
return `access_right: "open"`, `embargo_date: null`, `access_conditions: null`.
There is no closed, restricted, or embargoed sibling record in either concept
group; each group's `relations.version` array has exactly one entry with
`is_last: true`.

**Evidence 2 — no record contains a session-log archive.** Each record has
exactly one file, a GitHub source ZIP (7,600,698 B and 2,925,436 B). Neither
listing contains `.jsonl`, a session-named tarball, or any file whose size is
consistent with a session-log corpus. Searching both expanded deposits for
`session|jsonl|\.tar|\.gz` returns only `SESSION_LOG_2026-02-19.md` (a 21,664 B
hand-written markdown lab note), `docs/origins/brainstorming-session.md`, and
`data/variants/fus_masked_logprobs.npy`. None is an agent-session log.

**Evidence 3 — the deposited audit record contains no session references at
all.** Searching `mechanism_classifier_audit_published.json` for `session`,
`jsonl` or `byte` yields exactly one hit, inside the `notes` field, which reads
verbatim:

> "No adapters exist yet, so evidence was extracted by hand; capture tier 2
> reflects VCS history plus the audit records (**Claude Code session logs exist
> but are not yet adapter-ingested, so tier 3 is not claimed**)."

Its `adapters_used` are `manual` (tier 2) and `git` (tier 1). There is no
`claude_code` adapter usage, no session-id, and no byte-size bulk reference in
any of its 8 evidence records — all eight are workflow/finding descriptions
(variant-table construction, six-predictor panel, canonical model, F1–F5).

**Evidence 4 — the described pattern belongs to a different audit.** The
"bulk-referenced by byte-size and session-id" construction is real, but it lives
in `examples/out/kiran_triplet_proof_audit_published.json`, which does carry
`claude_code_session:101e5996-1d44-46d2-a9aa-ef58c8bc1cbf`,
`claude_code_session:2e5b0b3e-c809-45eb-8908-a40b22af0a97`,
`claude_code_session:e36c3254-ad1a-4463-a52e-d40c484bb5e5`, and the description
*"D14 (bulk): three Claude Code session JSONL logs (8.1 MB combined) taken as a
whole."* That is the triplet-proof audit of a different project, and it is not
the case study §4.3 describes. The sentence appears to have been transplanted.

**Evidence 5 — no local archived copy exists.** A filesystem search under
`/storage/kiran-stuff` to depth 6 for `*.jsonl`, `*session*log*`, `*log*session*`,
`*session*.tar*`, `*session*.zip`, `*provenance*.tar*`, `*provenance*.zip`, and a
depth-3 sweep for `*.jsonl`, `*session*`, `*provenance*`, `*.tar.gz`, `*.tgz`,
`*.zip`, found no agent-session log archive for either project. The only
`mechanism_classifier` hit in either sweep is
`IDP_projects/mechanism_classifier/SESSION_LOG_2026-02-19.md` (21,664 B), the
hand-written markdown lab note that is already in the deposit — not an agent
transcript. The only match inside `aivs/` is `docs/audit-cost-sessions.csv`
(332 B), the derived one-row timing table, not logs. Every other hit belongs to
unrelated projects (RAG corpora, graph datasets, a 2025
`UniversalChemicalAlphabets` tarball). `~/.claude/projects/` holds 1,087 `.jsonl` files
for other projects; the directory for
`/storage/kiran-stuff/IDP_projects/mechanism_classifier` does not exist under any
normalisation, and `-storage-kiran-stuff-aivs/` holds only sessions created after
the audit work.

**Evidence 6 — the primary evidence is confirmed destroyed.**
`docs/audit-cost-summary.md` (extraction dated 2026-08-25) records four
independent checks — fuzzy match over all 72 project directories, a content grep
across 1,043 JSONL files / ~750 MB, a `cwd`-field scan of every session, and a
filesystem-wide search for session UUID
`7d3cd00e-ea4a-45e6-88e1-128d0f99b98d` named in `~/.claude/history.jsonl` — and
concludes the transcript is deleted rather than misplaced. Only the MCP
side-log cache directory survives, with mtime 2026-03-16. No `cleanupPeriodDays`
was configured, so default retention expired the transcripts.

**Consequence.** The deposit cannot be created after the fact, because the
material no longer exists. The claim cannot be made true by depositing
something; it can only be made true by rewriting it. This also settles the open
question in the task brief: there is no surviving primary evidence, so real
audit-cost figures cannot be reported. The only defensible sources are the
`.claude.json` per-project telemetry in `docs/audit-cost-summary.md` (one session
per project: project A `lastCost` USD 4.11, `lastAPIDuration` 20.8 min; project B
USD 108.16, 2.02 h), which must be attributed to Claude Code's own telemetry,
scoped to a single session, and labelled a lower bound — or an author estimate
marked as such.

The retention loss is itself a reportable AIVS finding: a retrospective audit is
hostage to the retention policy of the tools it audits. That is an
`honest-omission` gap of exactly the kind the schema exists to surface.

---

## 5. Reader-view findings (Step 6)

Both repositories fetched unauthenticated, as any reader would.

### `khatvangi/aivs`

| Check | Result |
|---|---|
| Public | yes (`private: false`, not archived) |
| Default branch | `master`, HEAD `daabff7b8079…` (2026-06-17T15:49:18Z) |
| Root listing | `CHANGELOG.md CLAUDE.md HISTORY.md LICENSE NEXT.md README.md cover_letter.{docx,md,pdf} declaration_of_interests.{docx,md,pdf} docs/ examples/ figures/ pyproject.toml schema/ src/ tables.{docx,md,pdf} tests/ var_manuscript.{docx,md,pdf}` |
| `README.md` present | yes |
| Tag `v0.2.1-paper` | **yes** → `8406bca6f1` (matches deposit commit) |
| GitHub release | yes — "AIVS v0.2.1 — Patterns manuscript deposit", 2026-06-16T21:20:26Z |

**Navigation to the audit records: none.** Grepping the live README for
`examples/out`, `mechanism_classifier`, `audit record`, `zenodo`, `doi`, and
`case study` returns **zero matches**. There is no Zenodo badge and no DOI
anywhere in the README.

Worse, the README is stale in a way that actively misleads. Its "Repository
layout" section lists only `src/aivs/{meta_schema,vocabulary,adapters}` and
`tests/` — it does not mention `examples/` at all. Its scope section states:

> "## Current scope (v0.1.0) — This release ships the **meta-schema only** …
> Out of scope here: adapter implementations, manuscript parsers …"

The repository at that commit is v0.2.1 and ships three adapters, a v0.2.0
schema, and four completed audits under `examples/out/`. A reader following the
manuscript to this repo is told, by the README, that the thing they came for
does not exist yet. This is a sufficient explanation for Reviewer 5.

### `khatvangi/idp-mechanism-classifier`

| Check | Result |
|---|---|
| Public | yes (`private: false`, not archived) |
| Default branch | `master`, HEAD `3ca6dead8439…` (2026-06-16T20:51:41Z) |
| Root listing | `.gitignore ANALYSIS.md CRITICAL_EVALUATION.md LICENSE LITERATURE_SYNTHESIS.md PHASE3_CRITIQUE.md PLAN.md PROJECT.md SESSION_LOG_2026-02-19.md VALIDATION.md data/ docs/ features/ figures/ manuscript/ scripts/ sequences/` |
| `README.md` present | **NO** — `raw.githubusercontent.com/.../README.md` → HTTP 404; `GET /repos/.../readme` → "Not Found" |
| Tag `v0.2.1-paper` | **yes** → `3ca6dead84` (matches deposit commit) |
| GitHub release | yes — "v0.2.1-paper — AIVS-VAR manuscript companion deposit", 2026-06-16T21:20:27Z |

**Navigation: none, and no landing text at all.** With no README, GitHub renders
a bare file list. A reader arriving from the availability statement gets no
orientation, no pointer to the AIVS record in the sibling repo, and no DOI.

**The public repo has the same holes as the deposit,** because master HEAD *is*
the deposit commit:

- `GET /contents/scripts/figures` → HTTP 404
- `GET /contents/figures/paper` → HTTP 404
- `GET /contents/requirements.txt` → HTTP 404

So Reviewer 3's items (c) and (d) are missing from the GitHub URL as well as
from the Zenodo DOI. Both reviewers checked both locations and correctly found
nothing. Note also that the local `README.md`, which does exist and does describe
the canonical-output mapping, was never pushed.

**Tag summary:** `v0.2.1-paper` exists on both repositories, on both GitHub
releases, and in both Zenodo deposits, with commit SHAs matching in every case.
The tags are the one part of this that is fully consistent.

---

## 6. Corrections required

Ordered checklist. **[BLOCKING]** = must be done before resubmission, because
the manuscript currently asserts something a reviewer can check and disprove in
under five minutes.

### A. Actions that fix the deposits

1. **[BLOCKING] Add an environment manifest to the idp repo and re-deposit.**
   Item (d) is absent outright. Promote `requirements_kdense.txt` to a tracked
   `requirements.txt` (or `environment.yml`), and extend it — it currently omits
   `torch` and `fair-esm`, without which the ESM2 steps cannot be reproduced.
   Record the Python version and the pinned `esm2_t33_650M_UR50D` checkpoint.

2. **[BLOCKING] Add `scripts/figures/` (10 scripts) to the idp repo and
   re-deposit.** Item (c) is absent from both the repo and the deposit. These
   are the scripts that produce `figures/paper/figure_1..6` and
   `figure_s1..s4`; deposit the generated `figures/paper/` outputs alongside
   them so captions resolve.

3. **[BLOCKING] Add `scripts/mutation/13_–21_*.py`.** §4.4's FUS NLS
   permutation p = 0.002 (`17_random_region_control.py`) and EVE = 0.342
   (`15_eve_comparison.py`) currently have no deposited code.

4. **[BLOCKING] Add the data files the manuscript's numbers are read from** —
   `vus_excluded_sensitivity.csv`, `variants_with_regions_full_vus.csv`,
   `results_two_step_by_mechanism.csv`, `results_two_step_by_gene.csv`,
   `table_1_mechanism_split.csv`, `data/eve/*`, `variants_with_eve.csv`,
   `table_s1–s3`. §4.2 claims every number traces to a canonical CSV; for the
   clean-label/VUS split and the EVE comparison, the CSV is not deposited.

5. **[BLOCKING] Push local HEAD `10d85122` to GitHub, cut a new tag, and mint a
   new Zenodo version under concept DOI 10.5281/zenodo.20723560.** The deposit
   and the public repo are both frozen at `3ca6dead`, 132,669 insertions behind
   the work described. Note the histories have diverged — `3ca6dead` is not an
   ancestor of `10d85122` — so resolve that deliberately rather than
   force-pushing blind. Update the manuscript's version DOI to the new one; the
   concept DOI is unchanged.

6. **[BLOCKING] Add a `README.md` to the idp repo.** It has none, so its GitHub
   landing page is a bare file list. The local `README.md` already maps claims to
   canonical outputs — push it, and add: what the repo is, the manuscript
   citation, both Zenodo DOIs, and an explicit pointer to the AIVS verification
   record in `khatvangi/aivs` → `examples/out/mechanism_classifier_audit*.json`.

7. **[BLOCKING] Update the `aivs` README.** It currently says "Current scope
   (v0.1.0) — this release ships the meta-schema only … out of scope: adapter
   implementations", which is false at v0.2.1 and tells readers the audit records
   do not exist. Add an "Audit records" section linking
   `examples/out/mechanism_classifier_audit_published.json` by name, add the
   Zenodo DOI/badge, and list `examples/` in the repository-layout block.

8. Deposit the AIVS-side manuscript figures and the supplementary information.
   `figures/figure_1..6` and `make_aivs_schema.py` are in no deposit, and §157
   promises the paper's own verification trail "in the supplemental information",
   which is likewise undeposited. Re-tag `aivs` after the README fix and mint a
   new version under concept DOI 10.5281/zenodo.20723558.

9. Fix the Zenodo license identifier on both records: `apgl-v3` → `agpl-v3`.
   Non-blocking, but it is a visible metadata error on an AGPL-licensed deposit
   in a paper about provenance quality.

10. Exclude `__pycache__/*.pyc` from future deposits (16 compiled artefacts
    across the two archives). Non-blocking.

### B. Actions that fix the manuscript text

11. **[BLOCKING] Rewrite the line-105 parenthetical.** *"(bulk-referenced by
    byte-size and session-id and deposited under access control)"* is false on
    both limbs: the case-study audit record contains no session references and
    declines tier 3 in its own `notes`, and no access-controlled deposit exists
    or can now be created, because the logs were destroyed by default retention.
    Replace it with an accurate statement — that the record is capture tier 2
    (`manual` + `git`), that the agent-session logs were not adapter-ingested,
    and that they have since been expired by the tool's default retention policy.
    Report this as an `honest-omission` gap; it is a genuine finding about
    retrospective auditing and strengthens the paper's argument rather than
    weakening it. Do not describe the triplet-proof audit's bulk-reference
    pattern as if it were this case study's.

12. **[BLOCKING] Split the availability statement so each item points at the
    deposit that actually holds it.** As written, one sentence sends readers to
    the idp deposit for all five items, and the AIVS verification record is in
    the aivs deposit. State explicitly: the verification record
    (`examples/mechanism_classifier_audit.py` and
    `examples/out/mechanism_classifier_audit{,_published}.json`) is in
    10.5281/zenodo.20723559; the dataset, analysis scripts, figure scripts and
    environment manifest are in 10.5281/zenodo.20723561. Name the files. This
    alone answers one of Reviewer 3's four items and removes the cross-repo
    hunt Reviewer 5 described.

13. **[BLOCKING] Do not report a person-hours or audit-cost figure derived from
    session telemetry.** The logs do not exist. Either report the `.claude.json`
    single-session telemetry with its scope and lower-bound caveats stated
    explicitly, or report author recollection marked as an estimate. A
    reconstructed figure would be self-refuting in this paper.

14. Once the re-deposit in A.5 is done, update the version DOI in §157 and
    re-verify that §4.3's "Recomputation from the deposited inputs was tested on
    2026-03-16 and reproduces every headline AUROC to three decimal places" is
    true *of the new deposit*. It is not true of the current one: the inputs for
    the clean-label/VUS split and EVE are not deposited, and
    `bootstrap_cis.csv` plus three analysis scripts differ from the versions that
    produced the reported values.

15. Add an explicit sentence naming what is deliberately excluded and why. The
    current statement covers the ClinVar and AlphaMissense source tables, which
    is correct and verified — `.gitignore` excludes exactly
    `data/variant_summary.txt.gz` and
    `data/alphamissense/AlphaMissense_aa_substitutions.tsv.gz`. Keep that, and
    make clear it is the *only* intended exclusion, so a reader can distinguish
    design from oversight.

### Summary of blocking items

A.1, A.2, A.3, A.4, A.5, A.6, A.7 (deposit/repo) and B.11, B.12, B.13
(manuscript text). Items A.8–A.10, B.14–B.15 are strongly recommended but not
resubmission-blocking.
