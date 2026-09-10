# Audit record corrections — Job 2

Run 2026-09-08 on host `boron`, for CiSE-2026-06-0105.
Branch **`cise-r1-audit-record`**, four commits, **not pushed**.

`pytest tests/` → **45 passed** (37 before, 8 added).

## New checksums

The audit is not byte-reproducible — every `uuid4()` is regenerated per run —
so these are the checksums of the **committed** bytes, which are what any
future archive will contain. Re-running the example produces a structurally
identical record with different identifiers and therefore different hashes.

| File | Size | md5 (new) | md5 (deposited, superseded) |
|---|---:|---|---|
| `examples/out/mechanism_classifier_audit.json` | 37,216 | `1e6f79d02be3447c33c3c4c1ec5d3b55` | `4aaac341a56d7bed17711a6dc8ec4d81` |
| `examples/out/mechanism_classifier_audit_published.json` | 33,808 | `82585f4355045dab7196cc59a958c56d` | `348ec95ed46c144f7efb6fd4cdc1c8b3` |

sha256 of the published record:
`8e98cd4640e167a691b9b8bb16391129cb5cdc606a1a8b4c19811570c3d54c1f`

Structural counts unchanged: 22 events, 8 evidence, 8 decisions, 4 claims,
7 schema deltas. `validate_integrity()` → OK.

`docs/deposit-verification-2026-08-27.md` carries the old md5s. That table was
**not rewritten** — it is a dated record of what was true on 2026-08-27, and
falsifying it would be the precise failure this paper argues against. A dated
"SUPERSEDED" note was appended beneath it pointing here instead.

---

## 1. Capture tier 2 → 1

`capture_tier_achieved`, the `manual` AdapterUsage tier, and the per-event
default all move to `TIER_1`. Tier 2 requires AI logs; tier 1 is VCS plus
author-written records, which is what this audit actually has.

Notes rewritten to state that the session logs existed when the audit was
constructed, were never adapter-ingested, were verified absent on 2026-08-27,
and were expired by Claude Code default retention with no `cleanupPeriodDays`
configured (`docs/audit-cost-summary.md:84`). Recorded as an honest-omission
gap rather than worked around.

**Date correction.** The work order gave audit construction as 2026-04-06.
`AUDIT_TS` in `examples/mechanism_classifier_audit.py:81` is
**2026-06-04** — the digits were transposed. The record states 2026-06-04,
which also matches the `audit_timestamp` in the deposited copy.

## 2. "Prospective" → retrospective

The section 4.2 Claim read "caught five categories of failure during
prospective preparation". Now "during retrospective audit", consistent with
the manuscript.

## 3. `AIVS-VAR` purge — scope, and three deliberate exclusions

Removed from `examples/mechanism_classifier_audit.py` (docstring and
`audit_target`), from `README.md` (2), and consequently from both regenerated
JSON records. **Zero occurrences remain in any of those.**

Three tracked files still contain the term, each deliberately:

| File | n | Why it stays |
|---|---:|---|
| `docs/cise-r1-response-matrix.md` | 1 | It is the **verbatim reviewer question** in row 5.9 — *"What is the difference between AIVS and AIVS-VAR?"*. Purging it would make the row incoherent and would edit a reviewer's words. |
| `HISTORY.md` | 1 | Dated decision log. Rewriting history entries to match a later decision is the anti-pattern this paper is about. |
| `var_manuscript.md` | 8 | The superseded *Patterns*-era manuscript, not the CiSE submission. Per the project's own guidance, abandoned material belongs in legacy rather than being edited as if active. |

Two untracked files also carry it and were **not** touched:
`var_manuscript_cise.md` (6) is explicitly protected — Job 5 owns it, and
matrix row 5.9 already assigns the manuscript purge there;
`var_manuscript.md.bak` (11) and `apply_qss_revisions.py` (6) are *Patterns*-era
artefacts.

**Decision needed:** whether the *Patterns* material (`var_manuscript.md`,
`.bak`, `apply_qss_revisions.py`) should be moved to a `legacy/` directory
before the archive is cut. It is currently tracked and will ship inside the
Zenodo deposit, where a reader will find a second, differently-argued
manuscript alongside the real one.

## 4. Stale docstring

Replaced "AIVS v0.1.x ships the meta-schema only and has no adapters yet" with
an accurate statement: three adapters ship under `src/aivs/adapters/`, and the
reason none was used here is that the session logs were expired before they
could be ingested.

## 5. Superseded dispositions — deliberately asymmetric

| Decision | Script | Disposition |
|---|---|---|
| **F2** | `04_approach_a_xgboost.py` | superseded **IN FULL**, withdrawn from the paper-facing path. Its three outputs (`results_approach_a.csv`, `predictions_approach_a.csv`, `feature_importance_a.csv`) have **zero consumers** in `scripts/`. |
| **F1** | `06_approach_c_esm2.py` | superseded **IN PART only**. LOGO-CV block (lines 189-226, 366-385) superseded by script 10; feature-generation block (56-139, 310-319) **not** superseded — it is the sole writer of `esm2_features.csv`, canonical input to **seventeen** downstream files including every headline output and all thirteen figures. Canonical *conditional on* the HTT exclusion, because 170 of its rows carry the F1 fabricated defaults. |

The F2 text states explicitly that its disposition is stronger than F1's, so
the two cannot be read as equivalent. Both scopes were re-verified by grep and
the checks are recorded in each decision's `verification_notes`.

This closes the gap where the manuscript said scripts were "marked superseded"
while no disposition in the record used the word.

## 6. Adapter bug — `claude_code.py` session-directory derivation

`_project_dir` derived the directory with `str(absolute).replace("/", "-")`.
Claude Code collapses `_` and `.` to `-` as well.

```
/storage/kiran-stuff/IDP_projects/mechanism_classifier
  old impl → -storage-kiran-stuff-IDP_projects-mechanism_classifier   (does not exist)
  actual   → -storage-kiran-stuff-IDP-projects-mechanism-classifier
```

As shipped, the adapter could never have located sessions for **its own case
study**.

**Verified empirically, not assumed.** Of every session directory under
`~/.claude/projects` on this host, **zero** contain `_` or `.`. Five real paths
confirmed to resolve to directories that exist, including
`/home/kiran/.claude/double-shot-latte` →
`-home-kiran--claude-double-shot-latte` (dot → `-`, producing the double dash)
and `/storage/kiran-stuff/USPEX-v10.5` → `-storage-kiran-stuff-USPEX-v10-5`.

Fix: mapping extracted to a module-level `_session_dir_name()` backed by
`re.compile(r"[/_.]")`, testable without constructing an adapter or touching
the filesystem.

### Why the test suite never caught it

`tests/test_adapters.py` built its fixture session directories with the **same
bare `replace("/", "-")`** — at two sites, lines 40 and 252. Fixture and
implementation agreed only because both were wrong. pytest `tmp_path` names
contain underscores (`test_claude_code_redact_defaul0`), so the moment the
implementation was corrected, four pre-existing tests failed. They were failing
*correctly*: the fixture, not the fix, was wrong. Both sites now use
`_session_dir_name`.

This is worth noting in its own right — a test that reproduces the bug it is
meant to guard cannot fail, and this one hid a defect that disabled the
package's reference adapter on its own headline case study.

### Regression tests added (8)

Five parametrised mappings (underscore-free control; underscores in two path
segments; leading hidden directory; dotted version directory; underscore and
dot combined), a no-separator-survives invariant, a `_project_dir` test, and an
end-to-end `detect()` on an underscored project path. **All eight fail against
the old implementation** — verified, not assumed.

---

## Additions requested alongside Job 2

**Checklist A.10** — phase 1 correctly deferred this as a deletion outside its
brief. `aivs` had **no `.gitignore` at all**; one was added, and the 16 tracked
`__pycache__/*.pyc` files were untracked. Tracked compiled artefacts: **0**.
They will no longer ship inside the Zenodo archive.

**`pyproject.toml`** — `version = "0.1.0"` → `"0.2.2"`. It declared 0.1.0 while
`META_SCHEMA_VERSION` is 0.2.0 and the manuscript will cite v0.2.2, so a
reviewer who `pip install`ed from the archive saw 0.1.0.

**Response matrix row 3.9** — added for the §4.3 recomputation claim, alongside
3.8 and self-identified in the same style. The matrix is now tracked (it was
untracked). Stated totals updated: line 43 `39 → 40` total and Reviewer 3
`9 → 10`; line 120's separate "three of 38 rows", which excludes the `AE.0`
placeholder, becomes 39. Both figures shift by exactly the one added row.

The revised §4.3 paragraph text itself belongs to the Job 5 patch list and was
**not** applied — `var_manuscript_cise.md` remains unmodified.

---

## Commits (branch `cise-r1-audit-record`, not pushed)

| SHA | Scope |
|---|---|
| `97370f8` | items 1-5: audit record corrections + regenerated outputs |
| `04d3b53` | item 6: adapter fix, fixture correction, 8 regression tests |
| `28770c0` | A.10: `.gitignore`, untrack 16 compiled artefacts |
| `f3a9071` | pyproject version, README purge, matrix row 3.9 |

An earlier three-commit version of this branch was discarded by soft reset
before any push: `git add -u` had swept `HISTORY.md`, `cover_letter.*` and
`var_manuscript.md` — uncommitted authoring work unrelated to Job 2 — into a
Job 2 commit, and the `.pyc` deletions had landed in the audit-record commit
rather than the A.10 one. The four commits above are correctly scoped. Those
working files remain uncommitted, exactly as they were.

## Open for the tagging pass

- Whether to move the *Patterns*-era material to `legacy/` before the archive
  is cut (see §3).
- `var_manuscript_cise.md` still contains 6 `AIVS-VAR` occurrences; matrix row
  5.9 assigns these to the manuscript pass (Job 5).
