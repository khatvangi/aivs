"""
Retrospective AIVS audit of the mechanism_classifier workflow:

    IDP disease-mechanism prediction (six AI-derived variant predictors over
    ClinVar variants in IDP-associated genes), the case study in the AIVS-VAR
    manuscript.

This is a MANUAL audit, not an autonomous tool run — AIVS v0.1.x ships the
meta-schema only and has no adapters yet, so (exactly as in the smith_2026,
kiran_triplet_proof, and kappa_friction examples) evidence is extracted by
hand and encoded against the schema. The audit is faithful to the documented
workflow and does not extrapolate beyond it. Every Decision, Evidence, and
Claim traces to a real artifact in the project repository:

    - docs/2026-02-20-audit-code-science-logic.md   (code / science / logic audit; 7 findings)
    - CRITICAL_EVALUATION.md                          (2026-03-16 numerical + statistical audit)
    - scripts/mutation/*.py                           (the implementing code, by line)
    - data/variants/*.csv                             (the canonical output files)
    - the project git history (github.com/khatvangi/idp-mechanism-classifier)

The five failure dispositions encoded here are the empirical basis for the
manuscript's claim (Results section 4.2) that a manuscript-anchored
verification audit caught five categories of failure that disclosure-only
review would have missed:

    F1  Fabricated default features for out-of-window (truncated) positions
        (audit 2026-02-20, finding 3; scripts/mutation/06_approach_c_esm2.py:96-139,366-385)
    F2  Silently biased overall AUROCs from skipped CV folds / undisclosed denominator
        (audit 2026-02-20, findings 5 and 2; 04_approach_a_xgboost.py:93-250, 10_two_step_predictor.py:269)
    F3  Oracle routing + incomparable score scales in the mechanism-aware ensemble
        (audit 2026-02-20, finding 4; 08_mechanism_aware_model.py:265-312)
    F4  Mixed-eval-set numerical claim drawn from the wrong CSV / wrong model
        (CRITICAL_EVALUATION.md section 2.2)
    F5  Impossible bootstrap probability P = 1.000 from 1,000 resamples
        (CRITICAL_EVALUATION.md section 3.3)

The v0.1 vocabulary is empty by design, so every Decision is
`decision_type="unclassified"` with `schema_gap="novel_pattern"`, each paired
with a SchemaDelta proposing a candidate vocabulary term. These deltas are the
empirical input to the v0.2 vocabulary.

Run (from the aivs repo root, same environment used for the other examples):
    python -m examples.mechanism_classifier_audit

Outputs (to examples/out/, override with AIVS_OUT_DIR):
    mechanism_classifier_audit.json            (internal: full content)
    mechanism_classifier_audit_published.json  (minimum-capture: content stripped, hashes kept)
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from aivs.meta_schema import (
    Actor,
    ActorType,
    AdapterUsage,
    AuditArtifact,
    CaptureTier,
    Claim,
    Decision,
    Evidence,
    EvidenceConfidence,
    Event,
    SchemaDelta,
    SchemaDeltaKind,
    SourceRef,
    VerificationStatus,
)

# ---------------------------------------------------------------------------
# Timestamps. Workflow events are approximate (the repo gives a sequence, not
# per-event clock times); the two audit dates are exact (file names / headers).
# ---------------------------------------------------------------------------
TS_WORK = datetime(2026, 2, 10, 0, 0, 0, tzinfo=timezone.utc)   # analysis code authored
TS_AUDIT1 = datetime(2026, 2, 20, 0, 0, 0, tzinfo=timezone.utc) # code/science/logic audit
TS_AUDIT2 = datetime(2026, 3, 16, 0, 0, 0, tzinfo=timezone.utc) # critical evaluation + fixes
AUDIT_TS = datetime(2026, 6, 4, 0, 0, 0, tzinfo=timezone.utc)   # this audit constructed

REPO = "github.com/khatvangi/idp-mechanism-classifier"

# Actors
HUMAN = Actor(actor_type=ActorType.HUMAN, identifier="author-1")
AI_GEN = Actor(actor_type=ActorType.AI_GENERATIVE, identifier="claude-code")
AI_ADV = Actor(actor_type=ActorType.AI_ADVISORY, identifier="claude-code")
GITSYS = Actor(actor_type=ActorType.SYSTEM, identifier="git")


def src(adapter: str, location: str, when: datetime = AUDIT_TS) -> SourceRef:
    return SourceRef(
        adapter_name=adapter,
        adapter_version="0.0.0",
        raw_location=location,
        extracted_at=when,
    )


def ev(
    actor: Actor,
    action: str,
    target: str,
    content: str,
    adapter: str,
    location: str,
    when: datetime,
    tier: CaptureTier = CaptureTier.TIER_2,
) -> Event:
    return Event(
        timestamp=when,
        actor=actor,
        action=action,
        target=target,
        content=content,
        source_ref=src(adapter, location, when),
        tier=tier,
    )


def build_audit() -> AuditArtifact:
    events: list[Event] = []
    evidence: list[Evidence] = []
    decisions: list[Decision] = []
    claims: list[Claim] = []

    def add_ev(e: Event) -> Event:
        events.append(e)
        return e

    def add_evid(x: Evidence) -> Evidence:
        evidence.append(x)
        return x

    def add_dec(d: Decision) -> Decision:
        decisions.append(d)
        return d

    # =====================================================================
    # WORKFLOW DECISIONS (context the failures sit inside)
    # =====================================================================

    # --- W1: dataset curation -------------------------------------------------
    e_w1_pull = add_ev(ev(
        HUMAN, "run", "data/variant_summary.txt.gz",
        "Pulled ClinVar February 2026 snapshot (content-hashed); restricted to "
        ">=1-star review status; 23 IDP-associated genes.",
        "git", "scripts/mutation/01_build_variant_table.py", TS_WORK))
    e_w1_xcheck = add_ev(ev(
        AI_ADV, "generate", "scripts/mutation/01_build_variant_table.py",
        "Cross-checked variant positions against UniProt canonical sequences "
        "(94.7% position-match); flagged mismatches.",
        "claude_code", "scripts/mutation/01_build_variant_table.py", TS_WORK))
    e_w1_excl = add_ev(ev(
        HUMAN, "edit", "data/variants/variants_with_regions_clean.csv",
        "Excluded variants with conflicting clinical interpretations and the "
        "HTT locus; final clean-label set 778 variants (672P/106B); 653 in "
        "evaluable genes; 3,409 variants / 22 genes overall.",
        "git", "data/variants/variants_with_regions_clean.csv", TS_AUDIT2))
    ed_w1 = add_evid(Evidence(
        event_ids=[e_w1_pull.event_id, e_w1_xcheck.event_id, e_w1_excl.event_id],
        description=(
            "Variant-table construction: ClinVar Feb-2026 snapshot, >=1-star, "
            "UniProt-canonical cross-check, exclusion of conflicting "
            "interpretations and HTT. AI-advisory cross-check script; human "
            "committed exclusions."),
        confidence=EvidenceConfidence.HIGH))
    d_w1 = add_dec(Decision(
        timestamp=TS_WORK, decision_type="unclassified", schema_gap="novel_pattern",
        description=(
            "Curated the evaluation dataset: ClinVar Feb-2026 (>=1-star), "
            "UniProt-canonical position validation, and documented exclusions "
            "(conflicting interpretations; HTT, see F1). Clean-label primary "
            "set = 778 variants (653 in evaluable genes); VUS-included "
            "sensitivity set = 3,102."),
        actor=HUMAN, evidence_ids=[ed_w1.evidence_id],
        verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
        verification_notes=(
            "Counts re-verified against bootstrap_cis.csv on 2026-03-16 "
            "(CRITICAL_EVALUATION.md section 2.1).")))

    # --- W2: predictor selection ---------------------------------------------
    e_w2 = add_ev(ev(
        HUMAN, "run", "scripts/mutation/",
        "Scored six independent predictors per variant: ESM2 "
        "(esm2_t33_650M_UR50D LLR), AlphaMissense, EVE, CADD, REVEL, "
        "PolyPhen-2.",
        "git", "scripts/mutation/05_score_predictors.py", TS_WORK))
    ed_w2 = add_evid(Evidence(
        event_ids=[e_w2.event_id],
        description=(
            "Six-predictor panel (three generative-AI-derived: ESM2, "
            "AlphaMissense, EVE; three baselines: CADD, REVEL, PolyPhen-2) "
            "scored over the curated variants."),
        confidence=EvidenceConfidence.HIGH))
    d_w2 = add_dec(Decision(
        timestamp=TS_WORK, decision_type="unclassified", schema_gap="novel_pattern",
        description=(
            "Selected and scored six independent variant-effect predictors to "
            "test convergence on the IDP gain-of-toxic-function blind spot."),
        actor=HUMAN, evidence_ids=[ed_w2.evidence_id],
        verification_status=VerificationStatus.VERIFIED_PARTIALLY,
        verification_notes="Per-predictor AUROCs in data/variants/*_comparison.csv."))

    # --- W3: canonical model selection (two-step) ----------------------------
    e_w3 = add_ev(ev(
        HUMAN, "edit", "scripts/mutation/10_two_step_predictor.py",
        "Adopted the two-step logistic model (binary curated-region-membership "
        "indicator + raw ESM2 LLR) as the canonical, paper-facing model; "
        "XGBoost retained only for exploratory feature screening.",
        "git", "scripts/mutation/10_two_step_predictor.py", TS_AUDIT2))
    ed_w3 = add_evid(Evidence(
        event_ids=[e_w3.event_id],
        description=(
            "Canonical model = parsimonious two-step (region membership + raw "
            "ESM2 LLR). Region membership is a curated functional annotation, "
            "not the held-out mechanism label (contrast F3)."),
        confidence=EvidenceConfidence.HIGH))
    d_w3 = add_dec(Decision(
        timestamp=TS_AUDIT2, decision_type="unclassified", schema_gap="novel_pattern",
        description=(
            "Chose the two-feature two-step model as canonical to avoid the "
            "oracle-routing and scale-mixing problems found in the "
            "mechanism-aware ensemble (F3)."),
        actor=HUMAN, evidence_ids=[ed_w3.evidence_id],
        verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
        verification_notes=(
            "Clean two-step overall AUROC 0.873 vs ESM2 0.748 verified against "
            "results_two_step.csv (CRITICAL_EVALUATION.md section 2.1).")))

    # =====================================================================
    # THE FIVE FAILURE DISPOSITIONS
    # =====================================================================

    # --- F1: fabricated default features for truncated positions -------------
    f1_gen = add_ev(ev(
        AI_GEN, "generate", "scripts/mutation/06_approach_c_esm2.py:96-136",
        "ESM2 feature script truncated long proteins (lines 96-100) and filled "
        "out-of-range variants with zero/default features (lines 126-139), "
        "then included those rows in overall AUROC/AUPRC (lines 366-385).",
        "claude_code", "scripts/mutation/06_approach_c_esm2.py", TS_WORK))
    f1_det = add_ev(ev(
        HUMAN, "audit", "docs/2026-02-20-audit-code-science-logic.md#finding-3",
        "Audit finding 3 (High): ESM2 baseline includes fabricated defaults for "
        "truncated HTT positions; 170/259 HTT variants carried default features.",
        "manual", "docs/2026-02-20-audit-code-science-logic.md", TS_AUDIT1))
    f1_fix = add_ev(ev(
        HUMAN, "edit", "data/variants/variants_with_regions_clean.csv",
        "Resolved by excluding the HTT locus (the gene whose length forced "
        "truncation) from the scored set; final set 3,409 variants / 22 genes.",
        "git", "data/variants/variants_with_regions_clean.csv", TS_AUDIT2))
    f1_evid = add_evid(Evidence(
        event_ids=[f1_gen.event_id, f1_det.event_id, f1_fix.event_id],
        description=(
            "F1 — Context-window truncation produced fabricated default "
            "feature values that silently entered the ESM2 baseline metrics. "
            "Caught by the 2026-02-20 audit (finding 3); resolved by excluding "
            "the truncation-affected locus."),
        confidence=EvidenceConfidence.HIGH))
    f1 = add_dec(Decision(
        timestamp=TS_AUDIT1, decision_type="unclassified", schema_gap="novel_pattern",
        description=(
            "F1: Fabricated default features for out-of-window positions. The "
            "AI-generated ESM2 script filled truncated positions with "
            "zero/default features and scored them as real, inflating the "
            "baseline. Disposition: locus excluded; metrics recomputed."),
        actor=HUMAN, evidence_ids=[f1_evid.evidence_id],
        verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
        verification_notes=(
            "Re-run after exclusion; HTT no longer in results_two_step.csv "
            "(verified 2026-03-16).")))

    # --- F2: skipped-fold bias / undisclosed denominator ---------------------
    f2_gen = add_ev(ev(
        AI_GEN, "generate", "scripts/mutation/04_approach_a_xgboost.py:93-250",
        "Fold-skipping logic: predictions initialized to zero (line 93), "
        "single-class held-out folds skipped (lines 108-110), yet overall AUROC "
        "computed on the full prediction vector (line 250). Same pattern in "
        "06_approach_c_esm2.py (LOGO-CV block, lines 366-385).",
        "claude_code", "scripts/mutation/04_approach_a_xgboost.py", TS_WORK))
    f2_gen2 = add_ev(ev(
        AI_GEN, "generate", "scripts/mutation/10_two_step_predictor.py:269",
        "Two-step scorer skipped held-out genes with single-class labels "
        "(line 269-270); results_two_step.csv did not report that "
        "denominator, so AUROC was valid for the evaluated subset only.",
        "claude_code", "scripts/mutation/10_two_step_predictor.py", TS_WORK))
    f2_det = add_ev(ev(
        HUMAN, "audit", "docs/2026-02-20-audit-code-science-logic.md#finding-5",
        "Audit findings 5 and 2 (High): skipped folds bias overall metrics; "
        "headline AUROC computed on a filtered subset without disclosed "
        "denominator.",
        "manual", "docs/2026-02-20-audit-code-science-logic.md", TS_AUDIT1))
    f2_fix = add_ev(ev(
        HUMAN, "edit", "data/variants/bootstrap_cis.csv",
        "Resolved by defining and disclosing the evaluable set (clean: 653 "
        "variants / 14 genes; VUS-included: 3,102) and reporting per-mechanism "
        "and per-gene denominators explicitly.",
        "git", "data/variants/bootstrap_cis.csv", TS_AUDIT2))
    f2_evid = add_evid(Evidence(
        event_ids=[f2_gen.event_id, f2_gen2.event_id, f2_det.event_id, f2_fix.event_id],
        description=(
            "F2 — Cross-validation fold skipping combined with metrics computed "
            "over the full vector produced silently biased AUROCs on an "
            "undisclosed denominator. Caught 2026-02-20 (findings 5, 2); "
            "resolved by explicit evaluable-set accounting."),
        confidence=EvidenceConfidence.HIGH))
    f2 = add_dec(Decision(
        timestamp=TS_AUDIT1, decision_type="unclassified", schema_gap="novel_pattern",
        description=(
            "F2: Silently biased AUROCs from skipped CV folds. Disposition: "
            "evaluable set defined and disclosed; denominators reported; "
            "per-gene estimates with <5 minority-class variants flagged as "
            "illustrative."),
        actor=HUMAN, evidence_ids=[f2_evid.evidence_id],
        verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
        verification_notes=(
            "Evaluable counts (653/14 clean; 3,102 VUS) verified against "
            "bootstrap_cis.csv 2026-03-16.")))

    # --- F3: oracle routing in mechanism-aware ensemble ----------------------
    f3_gen = add_ev(ev(
        AI_GEN, "generate", "scripts/mutation/08_mechanism_aware_model.py:265-312",
        "Mechanism-aware ensemble routed variants using the known mechanism "
        "label (line 265) — leakage of the held-out target — and mixed "
        "min-max-scaled LLR (lines 271-274) with model probabilities "
        "across groups, so cross-group ranking was not calibrated.",
        "claude_code", "scripts/mutation/08_mechanism_aware_model.py", TS_WORK))
    f3_det = add_ev(ev(
        HUMAN, "audit", "docs/2026-02-20-audit-code-science-logic.md#finding-4",
        "Audit finding 4 (Medium): ensemble uses oracle mechanism labels for "
        "routing and mixes incomparable score scales.",
        "manual", "docs/2026-02-20-audit-code-science-logic.md", TS_AUDIT1))
    f3_fix = add_ev(ev(
        HUMAN, "edit", "scripts/mutation/10_two_step_predictor.py",
        "Resolved by abandoning oracle-routed ensemble as the paper-facing "
        "model in favour of the two-step model (W3), which uses only a curated "
        "region-membership annotation and the raw ESM2 LLR — no held-out "
        "label, single score scale.",
        "git", "scripts/mutation/10_two_step_predictor.py", TS_AUDIT2))
    f3_evid = add_evid(Evidence(
        event_ids=[f3_gen.event_id, f3_det.event_id, f3_fix.event_id],
        description=(
            "F3 — Oracle (held-out-label) routing plus incomparable score "
            "scales in the mechanism-aware ensemble. Caught 2026-02-20 "
            "(finding 4); resolved by replacing it with the leakage-free "
            "two-step model."),
        confidence=EvidenceConfidence.HIGH))
    f3 = add_dec(Decision(
        timestamp=TS_AUDIT1, decision_type="unclassified", schema_gap="novel_pattern",
        description=(
            "F3: Oracle leakage in the mechanism-aware ensemble. Disposition: "
            "ensemble demoted to exploratory; canonical model uses no held-out "
            "label."),
        actor=HUMAN, evidence_ids=[f3_evid.evidence_id],
        verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
        verification_notes=(
            "Canonical two-step contains no mechanism-label feature; confirmed "
            "in 10_two_step_predictor.py.")))

    # --- F4: mixed-eval-set numerical claim ----------------------------------
    f4_gen = add_ev(ev(
        AI_GEN, "generate", "docs/paper/results_section5_draft.md",
        "Draft section 5 cited two-step AUROC = 0.784 with ESM2 = 0.676. The "
        "0.784 came from membership_plus_llr_plus_features (a 5-feature model) "
        "on the VUS-included set; 0.676 came from VUS-included ESM2 — i.e. two "
        "different eval sets/models reported as one comparison.",
        "claude_code", "docs/paper/results_section5_draft.md", TS_WORK))
    f4_csv = add_ev(ev(
        GITSYS, "run", "data/variants/results_two_step.csv",
        "Canonical outputs: clean two-step = 0.873, clean ESM2 = 0.748; "
        "VUS-included two-step (2-feature) = 0.766, VUS-included ESM2 = 0.676.",
        "git", "data/variants/results_two_step.csv", TS_AUDIT2))
    f4_det = add_ev(ev(
        HUMAN, "audit", "CRITICAL_EVALUATION.md#2.2",
        "Numerical audit section 2.2: identified the mixed eval-set/model "
        "conflation in the section-5 numbers.",
        "manual", "CRITICAL_EVALUATION.md", TS_AUDIT2))
    f4_fix = add_ev(ev(
        HUMAN, "edit", "docs/paper/results_section5_draft.md",
        "Resolved: section 5 now leads with clean-label (0.873 vs 0.748, "
        "delta +0.125) and reports VUS-included (0.766 vs 0.676, delta +0.090) "
        "as an explicit sensitivity analysis.",
        "git", "docs/paper/results_section5_draft.md", TS_AUDIT2))
    f4_evid = add_evid(Evidence(
        event_ids=[f4_gen.event_id, f4_csv.event_id, f4_det.event_id, f4_fix.event_id],
        description=(
            "F4 — A headline numerical claim conflated two eval sets and two "
            "models (0.784 from a 5-feature VUS-included model vs 0.676 ESM2). "
            "Caught by the 2026-03-16 numerical audit (section 2.2) by tracing "
            "each number to its source CSV; corrected to matched comparisons."),
        confidence=EvidenceConfidence.HIGH))
    f4 = add_dec(Decision(
        timestamp=TS_AUDIT2, decision_type="unclassified", schema_gap="novel_pattern",
        description=(
            "F4: Mixed-eval-set numerical claim drawn from the wrong CSV/model. "
            "Disposition: every headline number re-traced to a specific cell in "
            "a canonical output file; matched (same set, same model) "
            "comparisons substituted."),
        actor=HUMAN, evidence_ids=[f4_evid.evidence_id],
        verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
        verification_notes=(
            "All headline numbers traced to results_two_step.csv / "
            "results_two_step_by_mechanism.csv (CRITICAL_EVALUATION.md 2.1).")))

    # --- F5: impossible bootstrap probability --------------------------------
    f5_gen = add_ev(ev(
        AI_GEN, "generate", "scripts/mutation/11_bootstrap_cis.py",
        "Reported P(two-step > ESM2) = 1.000 from 1,000 bootstrap resamples.",
        "claude_code", "scripts/mutation/11_bootstrap_cis.py", TS_WORK))
    f5_det = add_ev(ev(
        HUMAN, "audit", "CRITICAL_EVALUATION.md#3.3",
        "Statistical audit section 3.3: a probability of exactly 1.000 cannot "
        "be estimated from 1,000 resamples (resolution floor is 1/n_bootstrap).",
        "manual", "CRITICAL_EVALUATION.md", TS_AUDIT2))
    f5_fix = add_ev(ev(
        HUMAN, "edit", "docs/paper/results_section5_draft.md",
        "Resolved: reported as P < 0.001.",
        "git", "docs/paper/results_section5_draft.md", TS_AUDIT2))
    f5_evid = add_evid(Evidence(
        event_ids=[f5_gen.event_id, f5_det.event_id, f5_fix.event_id],
        description=(
            "F5 — A bootstrap probability reported as exactly 1.000, below the "
            "estimator's resolution floor. Caught by the 2026-03-16 "
            "statistical audit (section 3.3); corrected to P < 0.001."),
        confidence=EvidenceConfidence.HIGH))
    f5 = add_dec(Decision(
        timestamp=TS_AUDIT2, decision_type="unclassified", schema_gap="novel_pattern",
        description=(
            "F5: Impossible bootstrap probability. Disposition: claim restated "
            "at the estimator's resolution floor (P < 0.001)."),
        actor=HUMAN, evidence_ids=[f5_evid.evidence_id],
        verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
        verification_notes="Wording corrected in section 5; 1/1000 floor honoured."))

    # =====================================================================
    # CLAIMS (manuscript-level, traced to the decisions above)
    # =====================================================================
    claims.append(Claim(
        text=(
            "A manuscript-anchored AIVS audit caught five categories of failure "
            "during prospective preparation that disclosure-only review would "
            "have missed."),
        location="Results, section 4.2",
        upstream_decision_ids=[f1.decision_id, f2.decision_id, f3.decision_id,
                               f4.decision_id, f5.decision_id],
        evidence_confidence=EvidenceConfidence.HIGH))
    claims.append(Claim(
        text=(
            "The clean-label two-step model reaches overall AUROC 0.873 vs "
            "0.748 for ESM2 alone (delta +0.125)."),
        location="Results, section 4.4",
        upstream_decision_ids=[d_w1.decision_id, d_w3.decision_id,
                               f1.decision_id, f2.decision_id, f4.decision_id],
        evidence_confidence=EvidenceConfidence.HIGH))
    claims.append(Claim(
        text=(
            "ESM2 fails on the gain-of-function non-amyloid subset (AUROC "
            "0.493); curated region context rescues it to 0.822 "
            "(delta +0.329)."),
        location="Results, section 4.4",
        upstream_decision_ids=[d_w2.decision_id, d_w3.decision_id, f3.decision_id],
        evidence_confidence=EvidenceConfidence.HIGH))
    claims.append(Claim(
        text="The two-step gain over ESM2 is significant at P < 0.001.",
        location="Results, section 4.4",
        upstream_decision_ids=[d_w3.decision_id, f5.decision_id],
        evidence_confidence=EvidenceConfidence.HIGH))

    audit = AuditArtifact(
        audit_target=f"repo:{REPO} (mechanism_classifier; AIVS-VAR case study)",
        vocabulary_version="0.1.0",
        capture_tier_achieved=CaptureTier.TIER_2,
        audit_timestamp=AUDIT_TS,
        adapters_used=[
            AdapterUsage(adapter_name="manual", adapter_version="0.0.0",
                         capture_tier=CaptureTier.TIER_2),
            AdapterUsage(adapter_name="git", adapter_version="0.0.0",
                         capture_tier=CaptureTier.TIER_1),
        ],
        events=events,
        evidence=evidence,
        decisions=decisions,
        claims=claims,
        notes=(
            "Manual retrospective AIVS audit of the mechanism_classifier "
            "workflow, faithful to two project audit documents "
            "(docs/2026-02-20-audit-code-science-logic.md; "
            "CRITICAL_EVALUATION.md, 2026-03-16) and the implementing code and "
            "canonical outputs. No adapters exist yet, so evidence was "
            "extracted by hand; capture tier 2 reflects VCS history plus the "
            "audit records (Claude Code session logs exist but are not yet "
            "adapter-ingested, so tier 3 is not claimed). The v0.1 vocabulary "
            "is empty by design; every decision is unclassified with a "
            "novel-pattern schema gap and a corresponding SchemaDelta."),
    )

    audit.schema_deltas = build_schema_deltas(audit.audit_id, {
        "f1": f1_evid, "f2": f2_evid, "f3": f3_evid, "f4": f4_evid, "f5": f5_evid,
        "w1": ed_w1, "w3": ed_w3,
    })
    return audit


def build_schema_deltas(audit_id: str, e: dict[str, Evidence]) -> list[SchemaDelta]:
    """Candidate v0.2 vocabulary terms surfaced by this audit."""
    defs = [
        ("context_window_truncation_handling",
         "How out-of-window positions are scored when a model's context is "
         "shorter than the sequence; recurring source of fabricated default "
         "features (F1).", e["f1"]),
        ("cv_fold_exclusion_accounting",
         "Disclosure of which folds/genes were skipped and on what denominator "
         "a cross-validated metric is computed (F2).", e["f2"]),
        ("oracle_routing_in_ensemble",
         "Use of a held-out target label to route inputs within an ensemble — "
         "a leakage pattern distinct from feature leakage (F3).", e["f3"]),
        ("eval_set_provenance_for_numerical_claims",
         "Binding each reported number to a specific eval set, model, and "
         "output file, so mixed-set comparisons are detectable (F4).", e["f4"]),
        ("bootstrap_resolution_floor",
         "Reporting resampled probabilities no finer than 1/n_resamples (F5).",
         e["f5"]),
        ("dataset_exclusion_rationale",
         "Curated, documented exclusion of loci/variants with stated grounds "
         "(W1).", e["w1"]),
        ("canonical_model_selection",
         "Designation of one paper-facing model among exploratory alternatives, "
         "with the leakage/parsimony rationale (W3).", e["w3"]),
    ]
    return [
        SchemaDelta(
            proposed_term=term,
            proposed_kind=SchemaDeltaKind.DECISION_TYPE,
            justification=just,
            source_audit_id=audit_id,
            raw_evidence_ids=[evid.evidence_id],
            proposed_at=AUDIT_TS,
        )
        for term, just, evid in defs
    ]


def main() -> None:
    audit = build_audit()
    errors = audit.validate_integrity()
    if errors:
        print("INTEGRITY ERRORS:")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)

    out_dir = Path(
        os.environ.get("AIVS_OUT_DIR", str(Path(__file__).resolve().parent / "out"))
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    internal_path = out_dir / "mechanism_classifier_audit.json"
    published_path = out_dir / "mechanism_classifier_audit_published.json"

    internal_json = audit.model_dump_json(indent=2)
    internal_path.write_text(internal_json)

    published = audit.to_published()
    published_json = published.model_dump_json(indent=2)
    published_path.write_text(published_json)

    counts = {
        "events": len(audit.events),
        "evidence": len(audit.evidence),
        "decisions": len(audit.decisions),
        "claims": len(audit.claims),
        "schema_deltas": len(audit.schema_deltas),
    }
    print("=== AIVS retrospective audit: mechanism_classifier ===")
    print(f"  target              : {audit.audit_target}")
    print(f"  audit_id            : {audit.audit_id}")
    print(f"  meta_schema_version : {audit.meta_schema_version}")
    print(f"  vocabulary_version  : {audit.vocabulary_version}")
    print(f"  capture_tier        : {audit.capture_tier_achieved.value}")
    print(f"  integrity           : OK")
    print(f"  counts              : {json.dumps(counts)}")
    print(f"  internal artifact   : {internal_path} ({len(internal_json):,} bytes)")
    print(f"  published artifact  : {published_path} ({len(published_json):,} bytes)")
    print()
    print("Schema-delta proposals (candidate v0.2 vocabulary terms):")
    for sd in audit.schema_deltas:
        print(f"  - {sd.proposed_term}")


if __name__ == "__main__":
    main()
