# Figure regeneration — Job 3

2026-09-08, host `boron`. **Not pushed.**

| Repo | Branch | Commits |
|---|---|---|
| `IDP_projects/mechanism_classifier` | `cise-r1-figures` | `69a350c`, and the Figure 2 layout fix |
| `aivs` | `cise-r1-audit-record` | `ce779b0` (figures), `2e1c43c` (legacy move) |

Note the work order placed all of Job 3 on one branch "in the idp repo". It
spans both: `table_s1_regions.csv` and the Figure 2 generator are in the idp
repo, while `make_aivs_schema.py` and the embedded copies the manuscript
references are in `aivs`.

---

## 3.1 Table S1 — two HTT rows removed

`data/variants/table_s1_regions.csv`, 81 → 79 rows. Diff is exactly:

```
< HTT,Repeat expansion,Exon 1 (polyQ),1,90,90,,DiFiglia et al. 1997 Science
< HTT,Repeat expansion,HEAT repeats,91,3144,3054,,Li et al. 2006 JBC
```

**This was a generator defect, not a stale file.**
`scripts/mutation/16_supplementary_tables.py` applied the HTT exclusion to the
variant data at line 169 but not to the Table S1 construction loop — even
though the annotation block was already commented *"HTT (not used in analysis —
excluded for repeat expansion)"*. Deleting the CSV rows alone would have been
cosmetic: the next run of the script would have restored them.

Fixed by hoisting the exclusion to a single named constant applied in both
places:

```python
EXCLUDED_GENES = {"HTT"}
```

`REGION_ANNOTATIONS` still carries the HTT entries as a literature record; they
are filtered at emission. The removal is now reproducible by re-running the
script.

**Regeneration side-effects checked.** The script also emits Tables S2 and S3.
Both came back **byte-identical** (0 changed lines), so no other supplementary
value moved.

Documented in the idp `README.md` under a new *"Changes made during the CiSE
revision"* section, per the instruction not to delete silently — these deposits
have already been diffed between versions by a reviewer.

---

## 3.2 Figure 1 — AIVS schema, redrawn

`figures/make_aivs_schema.py` rewritten. Two independent problems.

### (a) It showed entities that do not exist

The old figure drew **Source, Invocation, Evaluation, Curation, Deposition** —
the five record types. `src/aivs/meta_schema/core.py` defines no such classes.
The kernel is **Actor, Event, Evidence, Decision, Claim, AuditArtifact**, with
**SourceRef**, **AdapterUsage** and **SchemaDelta** supporting.

Every box and edge label in the new figure was extracted from `core.py`, not
transcribed. The edges name the field that encodes each link:

| Edge | Field |
|---|---|
| Event → Evidence | `event_ids` |
| Evidence → Decision | `evidence_ids` |
| Decision → Claim | `upstream_decision_ids` |
| Actor → Event, Actor → Decision | `actor` |
| SourceRef → Event | `source_ref` |
| Decision ⇢ SchemaDelta | `schema_gap = "novel_pattern"` |

### (b) Reviewer 5's overlap

In the old figure a curved self-loop on Invocation crossed the **interior** of
the node, cutting through both its bold title and its field text, and its label
`parent_invocation_id (iteration)` landed on top of the Source box and the
adjacent horizontal arrow.

Two structural fixes: **all routing is orthogonal**, so no edge crosses a box;
and **every edge label is drawn on an opaque white patch**, so it masks its own
edge rather than colliding with it.

### Collisions found by inspecting the first redraw

The first render was not clean. Rendering and looking at it surfaced four more,
all fixed:

| # | Collision | Fix |
|---|---|---|
| 1 | Actor box occluded the AuditArtifact field line | field line moved to the container floor |
| 2 | `upstream_decision_ids` overran its gap into both neighbours | wrapped to two lines; gap widened 1.4 → 1.8 |
| 3 | Decision's field list was wider than its box | split to three lines |
| 4 | The "each entity references…" line collided with the `schema_gap` label | folded into the footer |

### ⚠ BLOCKING follow-up for Job 5

`var_manuscript_cise.md` **still describes the five record types**:

- **line 47** — *"AIVS is that schema: a closed meta-schema of five record
  types that captures the generate-evaluate-iterate-curate-deposit loop"*
- **line 123**, the Figure 1 caption — *"Directed graph rooted at Source
  records … terminating at Deposition records … The schema is closed at the
  meta-level (these five record types)"*

The figure and its own caption now contradict each other. **Both lines must be
rewritten in the Job 5 patch pass**, or the submission ships a figure that
disagrees with the text describing it. `var_manuscript_cise.md` was not
modified here.

---

## 3.3 Figure 2 — mechanism figure, layout fixed

`scripts/figures/fig1_mechanism_split.py` → `figures/paper/figure_1.{png,pdf}`,
synced to `aivs/figures/figure_1.{png,pdf}` (verified byte-identical,
md5 `c2b48288c37b…`). Four collisions:

| # | Collision | Cause | Fix |
|---|---|---|---|
| 1 | Every labelled bar's gene name sat on its own error bar | labels drawn at `x = auroc + 0.015`, exactly where the CI whisker extends | gene names moved out of the data area to **y-tick labels** |
| 2 | Group labels clipped — *"Repeat expans"*, *"Condensate/ot"* — and running into panel B's y-axis | placed at `x = 1.02` in axis coords with `wspace=0.35` | `wspace` 0.35 → 0.62, explicit gridspec margins, figure widened 11 → 12.4 in |
| 3 | `Δμ` annotations in the title band under the panel letter **B** | placed at *global* data max + 1.5, above the axes | ylim headroom added; annotations moved inside the axes |
| 4 | *(introduced by fix 3)* GoF `Δμ` then landed on the legend | both annotations used the global max, so the GoF label rode up | each annotation anchored to **its own group's** max |

Weak-evidence genes keep their italic grey treatment and `(P=n)` suffix as
tick labels.

**No value changed.** Per-gene AUROCs, `Δμ = +2.98` / `−0.87`, and panel C
(0.42, 0.45, 0.62, 0.40, 0.34, 0.82, 0.76) all render identically to the
previous version. This is a layout fix only.

---

## Verification

Both figures were **rendered and visually inspected**, not merely regenerated.
That is how collisions 1-4 in each figure were found — the first redraw of
Figure 1 passed every mechanical check and still had four overlaps in it.

Outputs: PNG at 400 dpi (Figure 1) and 300 dpi (Figure 2), plus vector PDF for
submission, both `bbox_inches="tight"`.

## Note on plotting library

The project standard is seaborn or plotly, with matplotlib reserved for backend
use. Figure 1 is a **node-link diagram**, not a statistical plot; neither
seaborn nor plotly has a node-link primitive, so it stays on matplotlib patches
and this is recorded in the script's docstring.

Figure 2 **is** a statistical figure and is raw matplotlib, so the standard
says it should migrate to seaborn. It was **not** migrated: the defect was
label placement, and rewriting a correct publication figure two weeks before
the deadline risks the numbers for no reviewer-visible gain. Flagged rather
than done silently — say the word if you want the migration.
