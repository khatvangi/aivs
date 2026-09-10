# HTT exclusion verification — scripts 17, 18, and the figure pipeline

**Date:** 2026-09-01
**Repository:** `/storage/kiran-stuff/IDP_projects/mechanism_classifier`
**Branch:** `cise-r1-deposit-repair`
**Context:** blocking verification for CiSE-2026-06-0105 revision
**Method:** read-only static inspection + inspection of on-disk artifacts. No script was
re-run, no file in the classifier repo was modified.

---

## 1. What is actually being guarded against

`scripts/mutation/06_approach_c_esm2.py:126-136` writes fabricated default features
(`esm2_llr: 0.0`, `esm2_ref_logprob: 0.0`, `esm2_alt_logprob: 0.0`, `esm2_entropy: 0.0`,
`esm2_rank_ref: 10`, `esm2_rank_alt: 10`) for any variant whose position exceeds ESM2's
1022-token context.

Empirical confirmation against `data/variants/esm2_features.csv` (3,664 rows):

| check | result |
|---|---|
| rows with `position >= 1022` | 170 — **all HTT** |
| rows carrying the exact fabricated signature (`esm2_llr==0.0 & esm2_rank_ref==10 & esm2_rank_alt==10`) | 170 — **all HTT** |
| HTT rows in file | 255 |
| next-longest protein by max variant position | AR, max position 915 (protein length 920) |

Two consequences that matter for the revision:

1. **`gene != "HTT"` is exactly equivalent to "drop all fabricated rows."** No other
   protein in the panel comes within 100 residues of the 1022 limit, so the gene filter is
   both necessary and sufficient. There is no second contaminated gene hiding behind a
   position-based rather than gene-based defect.
2. **The in-code comment's count is slightly off.** `06:128` says "170 of 259 HTT
   variants"; the file contains 255 HTT rows, so it is 170 of 255. The 170 is correct;
   the denominator is not. Worth correcting if that number is quoted in the manuscript.

---

## 2. Corrected scope: which figure scripts actually read `esm2_features.csv`

The task brief expected seven figure scripts (fig1–fig6 and figS4). **The actual set is
six.** `fig5_two_step.py` does *not* read `esm2_features.csv`; it reads
`variants_with_regions.csv`, which is written by script 10 from an already-HTT-filtered
frame and empirically contains 0 HTT rows (778 rows, 20 genes, no HTT).

Full inventory of `esm2_features.csv` readers under `scripts/figures/`:
`fig1`, `fig2`, `fig3`, `fig4`, `fig6`, `figS4`.
Not readers: `fig5`, `figS1` (`fus_masked_marginals.csv`), `figS2` (`bootstrap_cis.csv`),
`figS3` (`alphamissense_comparison.csv`, `eve_comparison.csv`).

---

## 3. Per-script table

| Script | Reads | HTT filter present | Line | Contamination possible |
|---|---|---|---|---|
| `scripts/mutation/17_random_region_control.py` | `esm2_features.csv` directly, L120 | **Yes — explicit** `df = df[df["gene"] != "HTT"].copy()` | **L121** | **No** |
| `scripts/mutation/18_kappa_scd.py` | `esm2_features.csv` directly, L153 | **Yes — explicit** `df = df[df["gene"] != "HTT"].copy()` | **L156** | **No** |
| `scripts/figures/fig1_mechanism_split.py` | `esm2_features.csv` directly, L62 | **Yes — explicit** `df = df[df["gene"] != "HTT"].copy()` | **L63** | **No** |
| `scripts/figures/fig2_fus_nls.py` | `esm2_features.csv` directly, L53 | **No explicit filter.** Implicit: `fus = df[df["gene"] == "FUS"].copy()` | **L54** | **No** (verified: `df` occurs on only L53–L54 in 278 lines) |
| `scripts/figures/fig3_tardbp_lcd.py` | `esm2_features.csv` directly, L49; also `variants_with_alphamissense.csv` L53 (0 HTT rows) | **No explicit filter.** Implicit: `tdp = df[df["gene"] == "TARDBP"].copy()` | **L50** | **No** (verified: `df` occurs on only L49–L50 in 219 lines) |
| `scripts/figures/fig4_hnrnpa1_sticker.py` | `esm2_features.csv` directly, L52 | **No explicit filter.** Implicit: `hnr = df[df["gene"] == "HNRNPA1"].copy()` | **L53** | **No** (verified: `df` occurs on only L52–L53 in 221 lines) |
| `scripts/figures/fig5_two_step.py` | **Does not read `esm2_features.csv`.** Reads `variants_with_regions.csv`, L55 | Upstream — written by `10_two_step_predictor.py:569` from a frame filtered at L243 | — | **No** (file empirically contains 0 HTT rows) |
| `scripts/figures/fig6_disorder_not_problem.py` | `esm2_features.csv` directly, L51 | **Yes — explicit** `df = df[df["gene"] != "HTT"].copy()` | **L52** | **No** |
| `scripts/figures/figS4_gene_landscapes.py` | `esm2_features.csv` directly, L36; also `variants_with_regions.csv` L39 (0 HTT) and `bootstrap_cis.csv` L40 (0 HTT entities) | **Yes — explicit** `df = df[df["gene"] != "HTT"].copy()` | **L37** | **No** |

In every case the filter or the gene subset occurs on the line immediately following the
`read_csv`, before any statistic, plot call, or write. For the three implicit cases
(fig2/3/4) the full unfiltered frame `df` is referenced on exactly two lines — the read
and the subset — and never again, so no HTT row can reach any downstream computation.

Auxiliary files consumed by these scripts were checked directly and are HTT-free where it
matters: `variants_with_regions.csv` (778 rows, no HTT), `variants_with_alphamissense.csv`
(3,409 rows = 3,664 − 255, no HTT), `bootstrap_cis.csv` (no HTT entity),
`fus_masked_marginals.csv` (168 rows, FUS only). `per_residue_disorder.csv` is subset by
gene at the point of use in fig2/fig3/fig4.

---

## 4. Spot-check of scripts 09–16

Four were checked rather than three. The in-code claim at `06:130` — "all paper-facing
analyses (scripts 09-16) exclude HTT entirely" — is **true in outcome for every script
checked**, but the stated mechanism is not uniform.

| Script | Filter | Verified how |
|---|---|---|
| `10_two_step_predictor.py` | Explicit, **L243**, immediately after read at L242 | Filter precedes all five `roc_auc_score` calls (L367–L538) and all six `to_csv` writes (L559–L573). Empirical: `results_two_step.csv`, `results_two_step_by_gene.csv`, `results_two_step_by_mechanism.csv`, `variants_with_regions.csv` all contain **0** HTT rows. |
| `11_bootstrap_cis.py` | Explicit, **L63**, immediately after read at L62 | Filter precedes both AUROC points (L88, L133) and the single write (L145). Empirical: `bootstrap_cis.csv` entity list contains 22 genes + 5 mechanism groups, **no HTT**. |
| `14_physics_calculations.py` | **No explicit filter.** Read at L59 with no `!= "HTT"` anywhere in the file | HTT-free by construction only: every use of `df` is a single-gene subset — FUS (L96), HNRNPA1 (L141–L142), TARDBP (L173), and the Part 4 loop is `for gene in ["FUS", "TARDBP"]` (L244). Script writes no file; output is stdout only. **Conclusion holds, but not by the mechanism the comment asserts.** |
| `16_supplementary_tables.py` | Explicit, **L169**, immediately after read at L168 | Filter precedes all AUROC calls (L228, L234, L267) and writes. Empirical: `table_s2_gene_summary.csv`, `table_s3_features.csv`, `table_1_mechanism_split.csv` contain **0** HTT rows. |

Additionally checked by inspection: `09_masked_marginals_fus.py` has **no explicit
filter** either — it reads at L117 and subsets to FUS at L118; its output
`fus_masked_marginals.csv` is 168 rows, FUS only. `12_alphamissense_comparison.py` (L175)
and `15_eve_comparison.py` (L119) filter explicitly. `13_boundary_sensitivity.py` never
reads `esm2_features.csv` at all — it reads the already-clean `variants_with_regions.csv`
(L126), while its printed banner claims "(HTT excluded)".

### One artifact-level note, not a numerical defect

`table_s1_regions.csv` contains **two HTT rows** (`Exon 1 (polyQ)`, `HEAT repeats`). These
originate from the hardcoded literature-annotation literal at `16_supplementary_tables.py:112-114`,
labelled in-source as "HTT (not used in analysis — excluded for repeat expansion)". They
carry only start/end coordinates and a citation — no ESM2 value, no AUROC, no computed
statistic. This is not fabricated-feature contamination. It is, however, a
**consistency point for the revision**: a supplementary table lists HTT regions while the
manuscript states HTT is excluded. Reviewers may notice the tension.

---

## 5. Out-of-scope contamination found (reported, not fixed)

`07_deep_dive_failures.py` (reads at L125) and `08_mechanism_aware_model.py` (reads at
L87) **do not exclude HTT** and actively group it into a "Repeat expansion" mechanism
class (`07:303`, `08:41`, `08:445`). Exact scope:

- **Script 08** plots a panel literally titled `"Repeat Expansion\n(AR, HTT, ATXN3)"`
  (L445) and saves to `figures/mechanism_aware_llr_distributions.png` (L483). That panel
  is drawn over the 170 fabricated HTT rows.
- **Script 07** saves three PNGs to `figures/` (L394, L443, L478) and one CSV,
  `data/variants/regional_esm2_analysis.csv` (L613).

**Manuscript impact: none.** Both write to `figures/`, the exploratory directory — not
`figures/paper/`, which holds the submitted set (`figure_1`–`figure_6`, `figure_s1`–`figure_s7`).
`regional_esm2_analysis.csv` contains 0 HTT rows and is read by no other script in the
repository. No reported number and no submitted figure derives from 07 or 08.

The accurate statement of scope for the revision is therefore: HTT is excluded from every
script that feeds a manuscript number or a `figures/paper/` artifact; HTT is *not*
excluded from two exploratory scripts (07, 08) whose outputs are not submitted.

---

## 6. Verdicts

### Verdict 1 — FUS NLS permutation p = 0.002 (`17_random_region_control.py`, manuscript §4.4)

**Computed over an HTT-free set. Determinate; no re-run required.**

Three independent guarantees, any one of which is sufficient:

1. **Explicit filter.** `17:121` removes HTT immediately after the read at `17:120`,
   before the per-gene loop, before every `roc_auc_score` call, and before the figure.
2. **Structural unreachability.** The FUS panel operates on `gene_df = df[df["gene"] == gene]`
   at `17:127` with `gene == "FUS"`. HTT rows cannot enter that frame whether or not
   line 121 executes. The same holds for all four panels of figure S5 — `GENE_REGIONS`
   contains only FUS, TARDBP, HNRNPA1 (`17:32-36`), and the pooled panel is
   `df[df["gene"].isin(pooled_genes)]` over those same three genes (`17:150`).
3. **The test never touches ESM2 at all.** The predictor is region membership computed
   from `position` alone (`17:58-59`), scored against `target` (`17:55`). No ESM2 column
   is read anywhere in the script. The fabricated `esm2_llr`/`esm2_rank_ref` values
   therefore cannot influence this p-value even in principle.

Reason 3 means the reported `p = 0.002` (paired with the NLS-membership AUROC of 0.916)
is immune to the F1 defect by construction, not merely by filtering. Git supports this:
`17_random_region_control.py` has exactly one commit (`10d8512`), which already contained
line 121, and the working tree is unmodified.

### Verdict 2 — anything plotted in the main figures

**Computed over an HTT-free set. Determinate; no re-run required.**

| Figure | Basis |
|---|---|
| `figure_1` | Explicit filter, `fig1:63` |
| `figure_2` | FUS-only subset, `fig2:54`; full frame never reused |
| `figure_3` | TARDBP-only subset, `fig3:50`; full frame never reused |
| `figure_4` | HNRNPA1-only subset, `fig4:53`; full frame never reused |
| `figure_5` | Reads `variants_with_regions.csv`, already HTT-free upstream |
| `figure_6` | Explicit filter, `fig6:52` |

Supplementary figures are equally clean: `s1` (FUS-only source), `s2` (`bootstrap_cis.csv`,
no HTT entity), `s3` (comparison files, no HTT), `s4` (explicit filter `figS4:37`),
`s5` (script 17, above), `s6` (script 18, explicit filter L156), `s7`
(`19_fus_ortholog_conservation.py`, does not read `esm2_features.csv`).

**Stated limitation.** These verdicts certify the code as it currently stands. All nine
scripts in scope have exactly one commit each, containing the filter or subset as
described, and `git status --porcelain` reports all nine unmodified. No run log was
retained, so I cannot prove from artifacts alone that the Feb 21 2026 PDFs in
`figures/paper/` were produced by exactly this code — but for `figure_2`, `figure_3`,
`figure_4` and all of figure S5 the argument is structural (single-gene subsetting) and
holds under any version of the filter line, and for `figure_1`, `figure_6`, `figure_s4`
and `figure_s6` git shows no version of the script ever lacked the filter.

**No fix required. No contamination reaches any reported number or submitted figure.**
