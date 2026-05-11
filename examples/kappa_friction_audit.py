"""
Retrospective AIVS audit of:

Hannah E. Ribbeck and Boggavarapu Kiran. "Charge Segregation Suppresses
Conformational Exploration in Coarse-Grained Polyampholyte Models."
Submission-ready for *The Journal of Physical Chemistry B*.
Project at /storage/kiran-stuff/IDP_projects/kappa_friction.

Third AIVS audit (after Smith 2026 JCE and triplet-proof). The structural
backbone of this audit is the v1 -> v3 retraction-and-rewrite cycle: an
initial analysis (scalar end-to-end distance ACF + single-exponential fit
with p0=1000 ps as initial guess) produced four headline claims that turned
out to be fitting artifacts. The error was discovered (some fits returned
the initial guess unchanged), the manuscript was retracted internally, the
analysis was rebuilt around an end-to-end vector ACF + stretched exponential
+ a new arrest metric (Ree_CV), and the manuscript was rewritten around
conformational arrest rather than timescale slowing. This audit captures
that arc as Decisions and the affected claims as retractions.

Hand-curated evidence sources (Tier 3 substrate):
  - HISTORY.md (2 Q/A blocks: 2026-04-24, 2026-04-25 final-polish session)
  - MANUSCRIPT_STATUS.md (v1 -> v3 retraction account, 2026-03-14)
  - manuscript/REANALYSIS_VERIFICATION.md (bug discovery + fix detail)
  - CLAUDE.md (project rules, corrected headline numbers)
  - manuscript/JPCB_DRAFT_v3.md and manuscript/JPCB_submission_v3.tex
    (canonical claim locations)

Two Claude Code session JSONLs (bulk reference, no enumeration):
  - 55301b70-013b-46a6-a064-7f7f39552a97.jsonl (505 KB)
  - 61108e47-28e8-4acd-9565-f00a2eac0a42.jsonl (4.06 MB)
Path-hashed location:
  ~/.claude/projects/-storage-kiran-stuff-IDP-projects-kappa-friction/

Capture tier: 3 for the documented decisions; the session JSONLs would
push to Tier 3+ with finer-grained event resolution if the
claude_code_adapter were run against them in full. This audit references
them via the session_bulk pattern only (event_count not enumerated;
byte_size and session_id are the evidence), mirroring the corresponding
D14 pattern in the triplet-proof audit.

Run:
    python -m examples.kappa_friction_audit
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


AUDIT_TS = datetime(2026, 5, 11, 0, 0, 0, tzinfo=timezone.utc)

# Baseline: state of kappa_friction at the submission-ready milestone,
# the morning after the 2026-04-25 wrap-up session.
AUDIT_BASELINE_TS = datetime(2026, 4, 25, 23, 59, 59, tzinfo=timezone.utc)

KAPPA_PATH = Path("/storage/kiran-stuff/IDP_projects/kappa_friction")
CLAUDE_PROJECTS_PATH = (
    ".claude/projects/-storage-kiran-stuff-IDP-projects-kappa-friction"
)


# Documented timestamps drawn from file metadata + HISTORY.md blocks.
# Exact times are approximate (midnight or document mtime) where the
# source does not pin a clock; see actor.metadata notes per event.
T_V1_APPROX = datetime(2026, 3, 1, 0, 0, 0, tzinfo=timezone.utc)
T_BUG_DISCOVERY = datetime(2026, 3, 13, 0, 0, 0, tzinfo=timezone.utc)
T_V3_REANALYSIS = datetime(2026, 3, 14, 0, 0, 0, tzinfo=timezone.utc)
T_MANUSCRIPT_REWRITE = datetime(2026, 3, 14, 19, 31, 0, tzinfo=timezone.utc)
T_FINAL_POLISH = datetime(2026, 4, 24, 16, 57, 0, tzinfo=timezone.utc)
T_WRAP = datetime(2026, 4, 25, 9, 1, 0, tzinfo=timezone.utc)
T_SESSION_1_MTIME = datetime(2026, 4, 25, 9, 5, 0, tzinfo=timezone.utc)
T_SESSION_2_MTIME = datetime(2026, 4, 24, 16, 48, 0, tzinfo=timezone.utc)


# Actors
KIRAN = Actor(
    actor_type=ActorType.HUMAN,
    identifier="Boggavarapu Kiran (corresponding author / PI)",
)
RIBBECK = Actor(
    actor_type=ActorType.HUMAN,
    identifier="Hannah E. Ribbeck (first author)",
)
CLAUDE_CODE = Actor(
    actor_type=ActorType.AI_AUTONOMOUS,
    identifier="Claude Code (Anthropic)",
    model_metadata={
        "product": "Claude Code",
        "version_observed_in_sessions": "as installed during 2026-03 to 2026-04",
        "underlying_model_versioning": "not pinned in session metadata",
        "note": (
            "Two sessions cover the visible AI-augmented work: "
            "61108e47 (4.06 MB, mtime 2026-04-24) and 55301b70 "
            "(505 KB, mtime 2026-04-25). Earlier v1-era activity may "
            "predate Claude Code involvement."
        ),
    },
)


def _src_manual(location: str) -> SourceRef:
    """Hand-curated Tier-3 evidence source ref."""
    return SourceRef(
        adapter_name="manual_log_adapter",
        adapter_version="0.0.0-pre-implementation",
        raw_location=location,
        extracted_at=AUDIT_TS,
    )


def _src_claude_code(jsonl_relpath: str) -> SourceRef:
    """Claude Code session JSONL source ref (adapter not invoked here)."""
    return SourceRef(
        adapter_name="claude_code",
        adapter_version="0.1.0",
        raw_location=jsonl_relpath,
        extracted_at=AUDIT_TS,
    )


# Convenience for session references.
SESSION_1 = "55301b70-013b-46a6-a064-7f7f39552a97"  # 505 KB, mtime 2026-04-25
SESSION_2 = "61108e47-28e8-4acd-9565-f00a2eac0a42"  # 4.06 MB, mtime 2026-04-24


# ---------------------------------------------------------------------------
# Events
#
# Two sources contribute events to this audit:
#   (1) bulk_session_events() — two coarse session-scope Events, one per
#       JSONL. Bulk reference only; the claude_code_adapter exists but is
#       intentionally not invoked here (per audit-scope decision).
#   (2) documented_events() — ten manual-log Events drawn from Tier-3
#       hand-curated documents (HISTORY.md, MANUSCRIPT_STATUS.md,
#       REANALYSIS_VERIFICATION.md, CLAUDE.md) and the manuscript itself.
# ---------------------------------------------------------------------------


def bulk_session_events() -> list[Event]:
    """Two coarse Events, one per Claude Code session JSONL.

    Mirrors the D14 bulk-reference pattern from kiran_triplet_proof_audit:
    session_id and byte_size are the evidence; fine-grained event
    enumeration is deferred to a future adapter-driven re-audit.
    """
    events: list[Event] = []
    for sid, size_bytes, ts in [
        (SESSION_1, 505_418, T_SESSION_1_MTIME),
        (SESSION_2, 4_056_640, T_SESSION_2_MTIME),
    ]:
        events.append(
            Event(
                timestamp=ts,
                actor=KIRAN,
                action="session_bulk_reference",
                target=f"claude_code_session:{sid}",
                content=(
                    f"Bulk reference to Claude Code session {sid}: "
                    f"{size_bytes:,} bytes of JSONL. Adapter exists but "
                    f"is intentionally not invoked in this audit; "
                    f"event_count is not enumerated. session_id, "
                    f"byte_size, and mtime are the evidence."
                ),
                source_ref=_src_claude_code(
                    f"{CLAUDE_PROJECTS_PATH}/{sid}.jsonl"
                ),
                tier=CaptureTier.TIER_2,
            )
        )
    return events


def documented_events() -> list[Event]:
    """Ten manual-log Events covering the v1->v3 retraction arc and the
    2026-04-24 final-polish session. Each event references the Tier-3
    document(s) that record it."""
    return [
        # E1: original v1 analysis (date approximate)
        Event(
            event_id="E_v1_run",
            timestamp=T_V1_APPROX,
            actor=KIRAN,
            action="run_analysis",
            target="v1 analysis pipeline (scalar Ree ACF + single-exp fit)",
            content=(
                "Original analysis using the autocorrelation of the scalar "
                "end-to-end distance fluctuation, fit to a single exponential "
                "exp(-t/tau) with initial guess tau=1000 ps and a bare "
                "'except: return np.nan'. Exact run date not recorded; "
                "bounded above by 2026-03-14 (date of the reanalysis "
                "documented in REANALYSIS_VERIFICATION.md). Per the "
                "documented account, several blocky-chain fits returned "
                "tau = exactly 1000.0 ps (the initial guess unchanged) "
                "because the noisy scalar-ACF signal decayed in a few "
                "frames and the fit barely moved."
            ),
            source_ref=_src_manual("manuscript/REANALYSIS_VERIFICATION.md"),
            tier=CaptureTier.TIER_3,
        ),

        # E2: bug discovery
        Event(
            event_id="E_bug_discovery",
            timestamp=T_BUG_DISCOVERY,
            actor=KIRAN,
            action="identify_fitting_artifact",
            target="v1 single-exponential fit on scalar Ree ACF",
            content=(
                "Fitting artifact identified: stuck-chain fits returned "
                "tau = 1000.0 ps unchanged from the initial guess, "
                "producing an apparent 3.67x slowdown for blocky chains "
                "that did not reflect any actual chain dynamics. Exact "
                "discovery timestamp not pinned; bounded below by E_v1_run "
                "and above by the 2026-03-14 v3 reanalysis."
            ),
            source_ref=_src_manual("manuscript/REANALYSIS_VERIFICATION.md"),
            tier=CaptureTier.TIER_3,
        ),

        # E3: v3 reanalysis
        Event(
            event_id="E_v3_reanalysis",
            timestamp=T_V3_REANALYSIS,
            actor=KIRAN,
            action="rerun_analysis",
            target="v3 analysis pipeline (vector ACF + stretched-exp + Ree_CV)",
            content=(
                "Complete reanalysis on 2026-03-14: end-to-end VECTOR ACF "
                "C(t) = <R(0).R(t)> / <|R(0)|^2>, stretched exponential "
                "C(t) = exp(-(t/tau)^beta) with bounds tau in [1, 500000] "
                "and beta in [0.1, 1.0], adaptive window, R^2 diagnostics, "
                "and a new arrest metric Ree_CV = std(Ree)/mean(Ree). "
                "174 trajectories across five datasets, 173 clean fits, "
                "1 suspect (CALVADOS gradient, min R^2 = 0.846)."
            ),
            source_ref=_src_manual("manuscript/REANALYSIS_VERIFICATION.md"),
            tier=CaptureTier.TIER_3,
        ),

        # E4: manuscript rewrite
        Event(
            event_id="E_manuscript_rewrite",
            timestamp=T_MANUSCRIPT_REWRITE,
            actor=KIRAN,
            action="rewrite_manuscript",
            target="manuscript/JPCB_DRAFT_v3.md",
            content=(
                "Manuscript restructured around CONFORMATIONAL ARREST "
                "(Ree_CV as primary observable, 7-11x suppression across "
                "three force fields) rather than the original v1 framing "
                "of TIMESCALE SLOWING (tau increases, salt rescue). Four "
                "v1 headline claims retracted as fitting artifacts: tau "
                "3.67x, tau/Rg^2 6.4x, salt 4.1x rescue, glassy beta ~0.4."
            ),
            source_ref=_src_manual("MANUSCRIPT_STATUS.md"),
            tier=CaptureTier.TIER_3,
        ),

        # E5: final-polish number verification (2026-04-24)
        Event(
            event_id="E_number_verification",
            timestamp=T_FINAL_POLISH,
            actor=KIRAN,
            action="verify_numbers",
            target="manuscript/JPCB_submission_v3.tex",
            content=(
                "Every quantity in the abstract, Results sections, and "
                "Table 1 reproduced exactly against v3 CSVs: "
                "kappa_gradient_results_v3.csv, hps_urry_results_v3.csv, "
                "calvados_salt_summary_v3.csv, "
                "rigorous_calvados_summary_v3.csv, "
                "lambda_titration_results_v3.csv. Rg fold changes, Ree_CV "
                "fold changes, tau/Rg^2 fold changes, all Spearman rho/p "
                "values, salt-sweep tau decrease, lambda titration "
                "p-values all match. Salt-sweep '<4% variation' right at "
                "the boundary at 3.98% — defensible."
            ),
            source_ref=_src_manual("HISTORY.md (2026-04-24 block)"),
            tier=CaptureTier.TIER_3,
        ),

        # E6: fabricated URL replacement (2026-04-24)
        Event(
            event_id="E_url_replacement",
            timestamp=T_FINAL_POLISH,
            actor=KIRAN,
            action="replace_fabricated_url",
            target="manuscript/JPCB_submission_v3.tex Data/Code Availability",
            content=(
                "Fabricated GitHub URL "
                "(github.com/kiran-mcneese/kappa-friction — no git remote "
                "is configured for the project) replaced with 'available "
                "from the corresponding author upon reasonable request.' "
                "No fake URL committed to the manuscript."
            ),
            source_ref=_src_manual("HISTORY.md (2026-04-24 block)"),
            tier=CaptureTier.TIER_3,
        ),

        # E7: funding clarification (2026-04-24)
        Event(
            event_id="E_funding_clarification",
            timestamp=T_FINAL_POLISH,
            actor=KIRAN,
            action="clarify_funding",
            target="manuscript/JPCB_submission_v3.tex Acknowledgments",
            content=(
                "Acknowledgments tightened to 'supported by internal funds "
                "from McNeese State University; no external funding was "
                "received' — explicit local-funding statement consistent "
                "with the user's confirmation that funding is local-only."
            ),
            source_ref=_src_manual("HISTORY.md (2026-04-24 block)"),
            tier=CaptureTier.TIER_3,
        ),

        # E8: obsolete .tex deletion (2026-04-24)
        Event(
            event_id="E_obsolete_tex_deletion",
            timestamp=T_FINAL_POLISH,
            actor=KIRAN,
            action="delete_obsolete_artifact",
            target="manuscript/JPCB_submission.tex (v1 file)",
            content=(
                "Deleted obsolete v1 manuscript/JPCB_submission.tex (the "
                "file CLAUDE.md flagged as 'needs full rewrite from v3 "
                "draft'). Pasted final content saved to "
                "manuscript/JPCB_submission_v3.tex (the only remaining "
                ".tex file). Two-author block preserved as pasted: "
                "Hannah E. Ribbeck first, Boggavarapu Kiran corresponding."
            ),
            source_ref=_src_manual("HISTORY.md (2026-04-24 block)"),
            tier=CaptureTier.TIER_3,
        ),

        # E9: cross-force-field validation (consolidated)
        Event(
            event_id="E_cross_force_field",
            timestamp=T_V3_REANALYSIS,
            actor=KIRAN,
            action="cross_validate",
            target="3 force fields: K/E minimal, HPS-Urry, CALVADOS 2 (150 mM)",
            content=(
                "v3 reanalysis includes cross-model validation across "
                "three coarse-grained force fields. Ree_CV suppression "
                "is highly significant (p < 0.001) in all three: K/E "
                "9.8x, HPS-Urry 7.4x, CALVADOS 11.4x. tau/Rg^2 increase "
                "is modest and model-dependent (1.20-1.27x; significant "
                "in K/E and HPS-Urry, ns in CALVADOS at p = 0.10)."
            ),
            source_ref=_src_manual("CLAUDE.md (Cross-Model Robustness table)"),
            tier=CaptureTier.TIER_3,
        ),

        # E10: session wrap-up (2026-04-25)
        Event(
            event_id="E_session_wrap",
            timestamp=T_WRAP,
            actor=KIRAN,
            action="document_session",
            target="HISTORY.md, .claude/memory/",
            content=(
                "Updated HISTORY.md and refreshed memory. Reframing complete: "
                "JPCB_submission_v3.tex is the only .tex, two-author "
                "(Hannah E. Ribbeck first, Kiran corresponding), McNeese "
                "internal funding stated explicitly, no fabricated repo URL, "
                "all v3 numbers verified exact. Outstanding items: bib "
                "[VERIFY] tags, no Author Contributions section, "
                "REVIEWER_COVER_NOTE.md author block not yet synced, no "
                "real GitHub/Zenodo deposit before submission."
            ),
            source_ref=_src_manual("HISTORY.md (2026-04-25 block)"),
            tier=CaptureTier.TIER_3,
        ),
    ]


def build_events() -> list[Event]:
    return documented_events() + bulk_session_events()


# ---------------------------------------------------------------------------
# Evidence — one per Decision, plus a bulk-session Evidence covering both
# JSONLs. Each documented Evidence references the manual_log Event(s) that
# anchor it; the bulk Evidence references the two session events.
# ---------------------------------------------------------------------------


def build_evidence(events: list[Event]) -> list[Evidence]:
    by_id = {e.event_id: e for e in events}

    def E(label_prefix: str) -> str:
        for e in events:
            if e.event_id.startswith(label_prefix):
                return e.event_id
        raise KeyError(label_prefix)

    evidence: list[Evidence] = [
        Evidence(
            event_ids=[E("E_bug_discovery"), E("E_v3_reanalysis")],
            description=(
                "D1: observable replacement — scalar Ree ACF -> end-to-end "
                "vector ACF. Documented in REANALYSIS_VERIFICATION.md "
                "section 'Observable: scalar distance ACF -> vector ACF'."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[E("E_bug_discovery"), E("E_v3_reanalysis")],
            description=(
                "D2: fitting-method replacement — single-exponential with "
                "bare init guess + bare except -> stretched-exponential "
                "with bounds, adaptive window, R^2 diagnostics. Documented "
                "in REANALYSIS_VERIFICATION.md section 'Fitting: single "
                "exponential with p0=1000 -> stretched exponential with "
                "bounds'."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[E("E_v3_reanalysis")],
            description=(
                "D3: new primary observable — Ree_CV = std(Ree)/mean(Ree). "
                "Documented in REANALYSIS_VERIFICATION.md section 'New "
                "diagnostic: Ree_CV' and CLAUDE.md 'Ree_CV (Conformational "
                "Arrest Metric)' block."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[E("E_bug_discovery"), E("E_manuscript_rewrite")],
            description=(
                "D4: claim retraction — four v1 headline claims retracted "
                "as fitting artifacts. Documented in MANUSCRIPT_STATUS.md "
                "section 'What is NOT supported' and "
                "REANALYSIS_VERIFICATION.md section 'Conclusions NOT "
                "Supported'."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[E("E_manuscript_rewrite")],
            description=(
                "D5: manuscript reframing — primary claim shifted from "
                "'timescale slowing' to 'conformational arrest'. Documented "
                "in JPCB_DRAFT_v3.md abstract and JPCB_submission_v3.tex "
                "abstract/conclusions."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[E("E_cross_force_field"), E("E_v3_reanalysis")],
            description=(
                "D6: cross-force-field validation — three coarse-grained "
                "force fields (K/E, HPS-Urry, CALVADOS 2). Documented in "
                "CLAUDE.md 'Cross-Model Robustness' table and "
                "REANALYSIS_VERIFICATION.md cross-dataset summary table."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[E("E_number_verification")],
            description=(
                "D7: full manuscript-against-CSV verification during final "
                "polish. Documented in HISTORY.md 2026-04-24 block."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[E("E_url_replacement")],
            description=(
                "D8: anti-fabrication correction — refused to commit a "
                "fabricated GitHub URL; replaced with 'available upon "
                "request' because no real repo deposit exists yet. "
                "Documented in HISTORY.md 2026-04-24 block."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[E("E_funding_clarification")],
            description=(
                "D9: funding-disclosure — explicit internal-McNeese-only "
                "statement. Documented in HISTORY.md 2026-04-24 block and "
                "JPCB_submission_v3.tex Acknowledgments."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[E("E_obsolete_tex_deletion"), E("E_session_wrap")],
            description=(
                "D10: author-order — two-author paper with Hannah E. "
                "Ribbeck first, Boggavarapu Kiran corresponding. "
                "Documented in HISTORY.md 2026-04-24 / 2026-04-25 blocks "
                "and the \\author{} block of JPCB_submission_v3.tex."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        # Bulk session evidence covering both Claude Code JSONLs.
        Evidence(
            event_ids=[e.event_id for e in events if e.action == "session_bulk_reference"],
            description=(
                "BULK: two Claude Code session JSONL logs (~4.5 MB combined) "
                "taken as a whole. session_id and byte_size are the "
                "evidence; finer-grained event enumeration is deferred. "
                "Both sessions visibly span the 2026-04 final-polish work; "
                "their content is consumed indirectly through the "
                "hand-curated HISTORY.md Q/A entries."
            ),
            confidence=EvidenceConfidence.MEDIUM,
        ),
    ]
    return evidence


# ---------------------------------------------------------------------------
# Decisions
# ---------------------------------------------------------------------------


def build_decisions(evidence: list[Evidence]) -> list[Decision]:
    by_prefix = {e.description[:6]: e.evidence_id for e in evidence}

    def E(prefix: str) -> str:
        for k, v in by_prefix.items():
            if k.startswith(prefix):
                return v
        raise KeyError(prefix)

    decisions: list[Decision] = []

    # D1: observable replacement (scalar -> vector)
    decisions.append(
        Decision(
            timestamp=T_V3_REANALYSIS,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Observable replacement: the dynamical observable used to "
                "operationalize the conformational-arrest question was "
                "changed from the autocorrelation of the SCALAR end-to-end "
                "distance fluctuation (v1) to the autocorrelation of the "
                "end-to-end VECTOR (v3). The vector ACF C(t) = "
                "<R(0).R(t)> / <|R(0)|^2> is the standard polymer-physics "
                "observable for chain reorientation and is robust to "
                "chains that are conformationally trapped, whereas the "
                "scalar variant decays in a few frames for compact chains "
                "because the tiny mean-centered fluctuations are noise. "
                "This is a vocabulary-candidate decision type "
                "(observable_replacement) — see SchemaDelta proposals."
            ),
            actor=KIRAN,
            evidence_ids=[E("D1: ")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Verified by direct comparison: v1 fits returned tau = "
                "1000.0 ps (initial guess) for blocky chains; v3 vector "
                "ACF fits return reasonable tau values with R^2 > 0.85 "
                "across 173 of 174 trajectories. Documented in "
                "REANALYSIS_VERIFICATION.md."
            ),
        )
    )

    # D2: fitting-method replacement
    decisions.append(
        Decision(
            timestamp=T_V3_REANALYSIS,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Fitting-method replacement: single-exponential exp(-t/tau) "
                "with initial guess p0=1000 ps and a bare 'except: return "
                "np.nan' (v1) was replaced by stretched-exponential "
                "exp(-(t/tau)^beta) with bounds tau in [1, 500000] ps, "
                "beta in [0.1, 1.0], adaptive fit window, and R^2 "
                "goodness-of-fit reporting (v3). The v1 fitter silently "
                "swallowed failures and returned the initial-guess tau "
                "unchanged, producing apparent slowdowns that did not "
                "reflect chain dynamics."
            ),
            actor=KIRAN,
            evidence_ids=[E("D2: ")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "v3 fit-quality summary in REANALYSIS_VERIFICATION.md: "
                "173/174 clean fits with min R^2 = 0.846. The 1 suspect "
                "is in the CALVADOS gradient and is flagged, not "
                "silently absorbed."
            ),
        )
    )

    # D3: new primary observable (Ree_CV)
    decisions.append(
        Decision(
            timestamp=T_V3_REANALYSIS,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "New primary observable: introduce Ree_CV = std(Ree) / "
                "mean(Ree) as the headline conformational-arrest metric. "
                "Requires no fitting; directly reports how much a chain "
                "explores its conformational space during a trajectory. "
                "Turns out to be the strongest and most consistent signal "
                "across all datasets (7-11x suppression, p < 0.001 in "
                "every gradient dataset). Acknowledged as non-standard in "
                "the polymer-dynamics literature — flagged as a limitation "
                "in the manuscript's Discussion."
            ),
            actor=KIRAN,
            evidence_ids=[E("D3: ")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Verifiable by direct trajectory inspection: blocky chains "
                "show Rg standard deviations of 0.003-0.005 nm vs ~0.5 nm "
                "for mixed sequences (REANALYSIS_VERIFICATION.md)."
            ),
        )
    )

    # D4: claim retraction
    decisions.append(
        Decision(
            timestamp=T_MANUSCRIPT_REWRITE,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Claim retraction: four v1 headline claims explicitly "
                "retracted in light of the v3 reanalysis. "
                "(i) 'tau increases 3.67x with blockiness' — fitting "
                "artifact; actual fold change 0.76x, not significant. "
                "(ii) 'tau/Rg^2 increases 6.4x' — fitting artifact; "
                "actual increase 1.21x. "
                "(iii) 'Salt relieves the slowdown 4.1x' — actual "
                "decrease 0.83x. "
                "(iv) 'Glassy beta ~ 0.4' — beta trend is not "
                "significant. "
                "This is a vocabulary-candidate decision type "
                "(claim_retraction) — see SchemaDelta proposals."
            ),
            actor=KIRAN,
            evidence_ids=[E("D4: ")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Retracted numbers are documented side-by-side with the "
                "corrected numbers in MANUSCRIPT_STATUS.md's 'Corrected "
                "headline numbers' table and in REANALYSIS_VERIFICATION.md "
                "'Conclusions NOT Supported' section. The AI-augmented "
                "workflow caught its own error and recorded it openly."
            ),
        )
    )

    # D5: manuscript reframing
    decisions.append(
        Decision(
            timestamp=T_MANUSCRIPT_REWRITE,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Manuscript reframing: the primary scientific claim was "
                "shifted from 'timescale slowing' (v1: charge segregation "
                "slows tau) to 'conformational arrest' (v3: charge "
                "segregation suppresses Ree_CV). Title, abstract, "
                "introduction, results structure, discussion, and "
                "conclusions all rewritten around the corrected story. "
                "Headline now: 'Charge Segregation Suppresses "
                "Conformational Exploration in Coarse-Grained "
                "Polyampholyte Models'."
            ),
            actor=KIRAN,
            evidence_ids=[E("D5: ")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Reframing visible end-to-end in JPCB_submission_v3.tex "
                "and JPCB_DRAFT_v3.md. v1 draft (JPCB_DRAFT.md) marked "
                "OBSOLETE in CLAUDE.md."
            ),
        )
    )

    # D6: cross-force-field validation
    decisions.append(
        Decision(
            timestamp=T_V3_REANALYSIS,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Cross-force-field validation: validate the Ree_CV "
                "suppression across three independently-developed "
                "coarse-grained force fields (K/E minimal HPS-like, "
                "HPS-Urry residue-specific, CALVADOS 2 Ashbaugh-Hatch + "
                "Yukawa). Result: Ree_CV suppression is 7.4x-11.4x with "
                "p < 0.001 in all three models. Decision rationale: any "
                "single-model claim is vulnerable to model-specific "
                "artifacts; three-model agreement is the credibility "
                "argument."
            ),
            actor=KIRAN,
            evidence_ids=[E("D6: ")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Cross-model fold changes and p-values reproduced "
                "exactly against the v3 CSVs during the 2026-04-24 "
                "number-verification pass (HISTORY.md)."
            ),
        )
    )

    # D7: full number verification
    decisions.append(
        Decision(
            timestamp=T_FINAL_POLISH,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Full manuscript-against-CSV verification during final "
                "polish: every quantity in the abstract, Results sections, "
                "and Table 1 was reproduced against five v3 CSV files "
                "(kappa_gradient, hps_urry, calvados_salt_summary, "
                "rigorous_calvados_summary, lambda_titration). Salt-sweep "
                "'<4% variation' is right at the boundary (3.98%) — "
                "marked as defensible."
            ),
            actor=KIRAN,
            evidence_ids=[E("D7: ")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Documented in HISTORY.md 2026-04-24 block. This is the "
                "submission-readiness gate."
            ),
        )
    )

    # D8: anti-fabrication correction (URL)
    decisions.append(
        Decision(
            timestamp=T_FINAL_POLISH,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Anti-fabrication correction: refuse to commit a "
                "fabricated GitHub URL "
                "(github.com/kiran-mcneese/kappa-friction — no git remote "
                "is actually configured). Replaced with 'available from "
                "the corresponding author upon reasonable request'. The "
                "AI-augmented workflow could plausibly generate a "
                "convincing-looking URL; the decision was to surface the "
                "absence of a real deposit rather than paper over it. "
                "This is a vocabulary-candidate decision type "
                "(anti_fabrication_correction) — see SchemaDelta "
                "proposals."
            ),
            actor=KIRAN,
            evidence_ids=[E("D8: ")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Verified in JPCB_submission_v3.tex Supporting Information "
                "section: '... available from the corresponding author "
                "upon reasonable request.' No fabricated URL present in "
                "the .tex."
            ),
        )
    )

    # D9: funding disclosure
    decisions.append(
        Decision(
            timestamp=T_FINAL_POLISH,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Funding disclosure: declare internal McNeese State "
                "University funding only; explicitly state that no "
                "external funding was received. Computational resources "
                "provided by McNeese State University."
            ),
            actor=KIRAN,
            evidence_ids=[E("D9: ")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Verified in JPCB_submission_v3.tex Acknowledgments: "
                "'This work was supported by internal funds from McNeese "
                "State University; no external funding was received.'"
            ),
        )
    )

    # D10: author order
    decisions.append(
        Decision(
            timestamp=T_FINAL_POLISH,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Author-order decision: two-author paper, Hannah E. "
                "Ribbeck first, Boggavarapu Kiran corresponding. "
                "Confirmed in HISTORY.md 2026-04-24 and 2026-04-25 "
                "blocks; reflected in the \\author{} block of "
                "JPCB_submission_v3.tex with both at McNeese State "
                "University, Department of Chemistry and Physics."
            ),
            actor=KIRAN,
            evidence_ids=[E("D10:")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Verified in JPCB_submission_v3.tex lines 11-15. "
                "Outstanding items per HISTORY.md 2026-04-25: no "
                "Author Contributions section yet; "
                "REVIEWER_COVER_NOTE.md author block not yet synced."
            ),
        )
    )

    return decisions


# ---------------------------------------------------------------------------
# Claims (from JPCB_submission_v3.tex / JPCB_DRAFT_v3.md)
# ---------------------------------------------------------------------------


def build_claims(decisions: list[Decision]) -> list[Claim]:
    # Match decisions by description prefix (the first distinctive word).
    d = {dec.description[:35]: dec.decision_id for dec in decisions}

    def D(prefix: str) -> str:
        for k, v in d.items():
            if k.startswith(prefix):
                return v
        raise KeyError(prefix)

    return [
        # C1: compaction
        Claim(
            text=(
                "Charge segregation compacts polyampholytes: Rg fold "
                "0.66-0.88x across three force fields (K/E 0.81x p<0.001, "
                "HPS-Urry 0.88x p=0.006, CALVADOS 0.66x p<0.001), all "
                "significant at p < 0.01."
            ),
            location=(
                "JPCB_submission_v3.tex Abstract; Results subsec "
                "'Charge segregation compacts chains and suppresses "
                "conformational exploration'; Table 1"
            ),
            upstream_decision_ids=[
                D("Observable replacement"),
                D("Cross-force-field validation"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        # C2: arrest — PRIMARY CLAIM
        Claim(
            text=(
                "Charge segregation suppresses conformational exploration: "
                "Ree_CV 7.4-11.4x suppression across three force fields "
                "(K/E 9.8x, HPS-Urry 7.4x, CALVADOS 11.4x), p < 0.001 in "
                "all three. THIS IS THE PRIMARY HEADLINE CLAIM."
            ),
            location=(
                "JPCB_submission_v3.tex Abstract; Results subsec "
                "'Charge segregation compacts chains and suppresses "
                "conformational exploration'; Table 1; Conclusions"
            ),
            upstream_decision_ids=[
                D("Observable replacement"),
                D("New primary observable"),
                D("Manuscript reframing"),
                D("Cross-force-field validation"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        # C3: modest tau/Rg^2 increase
        Claim(
            text=(
                "Effective friction enhancement tau/Rg^2 increases modestly "
                "with blockiness: 1.20-1.27x fold change (K/E 1.21x "
                "p=0.020, HPS-Urry 1.27x p=0.007, CALVADOS 1.20x p=0.10 "
                "ns). Significant in K/E and HPS-Urry, ns in CALVADOS."
            ),
            location=(
                "JPCB_submission_v3.tex Results subsec 'Cross-model "
                "robustness'; Table 1; Figure 1C"
            ),
            upstream_decision_ids=[
                D("Observable replacement"),
                D("Fitting-method replacement"),
                D("Cross-force-field validation"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        # C4: stickiness control negative
        Claim(
            text=(
                "Generic stickiness does not reproduce the arrest: lambda "
                "titration shows Spearman rho_tau/Rg2 = -0.31, p = 0.54 "
                "(ns) and rho_Ree_CV = -0.03, p = 0.96 (ns). Argues "
                "against a simple cohesion-only mechanism."
            ),
            location=(
                "JPCB_submission_v3.tex Results subsec 'Salt and "
                "stickiness controls'; Figure S1"
            ),
            upstream_decision_ids=[
                D("Fitting-method replacement"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        # C5: salt-sweep tau modest, not 4.1x
        Claim(
            text=(
                "Salt-sweep tau decreases modestly from 735 ps at 10 mM "
                "to 612 ps at 1000 mM (0.83x), not the 4.1x rescue "
                "claimed in v1. The v1 number was a fitting artifact "
                "now retracted."
            ),
            location=(
                "JPCB_submission_v3.tex Results subsec 'Salt and "
                "stickiness controls'"
            ),
            upstream_decision_ids=[
                D("Observable replacement"),
                D("Fitting-method replacement"),
                D("Claim retraction"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        # C6: robustness statement
        Claim(
            text=(
                "Cross-model robustness: the Ree_CV suppression is "
                "preserved across three independently-developed "
                "coarse-grained force fields (K/E minimal, HPS-Urry, "
                "CALVADOS 2). Three-model agreement is the credibility "
                "argument against model-specific artifacts."
            ),
            location=(
                "JPCB_submission_v3.tex Abstract; Results subsec "
                "'Cross-model robustness'; Table 1"
            ),
            upstream_decision_ids=[
                D("Cross-force-field validation"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        # C7: arrest, not slowdown
        Claim(
            text=(
                "The dominant physical effect of charge segregation is "
                "conformational arrest (suppressed Ree_CV), not "
                "timescale slowing (raw tau does not increase with "
                "blockiness in any of the three models). Compact blocky "
                "chains tumble as rigid objects at a timescale set by "
                "their size, while their internal degrees of freedom "
                "are arrested. This decoupling is the corrected story "
                "vs the v1 framing."
            ),
            location=(
                "JPCB_submission_v3.tex Results subsec 'Synthesis "
                "across datasets'; Conclusions"
            ),
            upstream_decision_ids=[
                D("New primary observable"),
                D("Claim retraction"),
                D("Manuscript reframing"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
    ]


# ---------------------------------------------------------------------------
# Schema deltas
# ---------------------------------------------------------------------------


def build_schema_deltas(
    audit_id: str, evidence: list[Evidence]
) -> list[SchemaDelta]:
    ev_ids = [e.evidence_id for e in evidence]

    proposals = [
        (
            "observable_replacement",
            (
                "Changing the empirical observable used to operationalize "
                "a claim (e.g., scalar end-to-end distance ACF -> "
                "end-to-end vector ACF). Distinct from "
                "metric_choice_for_evaluation because the observable "
                "itself is replaced, not a metric over an existing "
                "observable. Instantiated by D1 here. Often appears as a "
                "downstream consequence of identifying a fitting artifact "
                "or model misspecification."
            ),
        ),
        (
            "claim_retraction",
            (
                "Explicit retraction of previously held claims in light of "
                "new evidence. A meta-decision about epistemology, not a "
                "methodology choice. Instantiated by D4 here, where four "
                "v1 headline claims (tau 3.67x slowdown, tau/Rg^2 6.4x "
                "increase, salt 4.1x rescue, glassy beta ~0.4) were "
                "explicitly retracted as fitting artifacts. Distinct from "
                "manuscript_internal_discrepancy_disposition (Smith 2026 / "
                "triplet-proof vocabulary candidate) because the retracted "
                "claims have already been internally accepted and "
                "communicated, not merely flagged as discrepant."
            ),
        ),
        (
            "anti_fabrication_correction",
            (
                "Replacing an AI-generated or potentially-AI-generated "
                "content item (e.g., a fabricated URL, a plausible-looking "
                "citation, a too-clean experimental detail) with a "
                "verified or honest-omission placeholder. Distinguishes "
                "this from general editing because the corrective motion "
                "is specifically about NOT-fabricating, even at the cost "
                "of leaving a polish gap. Instantiated by D8 here, where "
                "a plausible GitHub URL was replaced with 'available upon "
                "request' because no real repo deposit exists."
            ),
        ),
        (
            "v1_to_v3_retraction_rewrite_arc",
            (
                "Meta-pattern observation: a full project arc from "
                "v1 (initial analysis) through bug-discovery to v3 "
                "(complete reanalysis + manuscript rewrite) is itself "
                "a structurally coherent unit of audit. The decisions "
                "(observable replacement, fitting-method replacement, "
                "new primary observable, claim retraction, manuscript "
                "reframing) co-occur and are causally chained. Audits "
                "that surface this arc should be able to express the "
                "causal chain explicitly, not just list the decisions. "
                "Candidate for an evidence_relation kind rather than a "
                "decision_type, but proposed here because the audit "
                "structure does not yet have a relation primitive."
            ),
        ),
    ]

    return [
        SchemaDelta(
            proposed_term=term,
            proposed_kind=SchemaDeltaKind.DECISION_TYPE,
            justification=justification,
            source_audit_id=audit_id,
            raw_evidence_ids=ev_ids,
            proposed_at=AUDIT_TS,
        )
        for term, justification in proposals
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def build_audit() -> AuditArtifact:
    events = build_events()
    evidence = build_evidence(events)
    decisions = build_decisions(evidence)
    claims = build_claims(decisions)

    audit = AuditArtifact(
        audit_target=(
            "/storage/kiran-stuff/IDP_projects/kappa_friction "
            "(submission-ready for J. Phys. Chem. B; "
            "manuscript/JPCB_submission_v3.tex; two-author: "
            "Hannah E. Ribbeck, Boggavarapu Kiran)"
        ),
        vocabulary_version="0.1.0",
        capture_tier_achieved=CaptureTier.TIER_3,
        audit_timestamp=AUDIT_TS,
        adapters_used=[
            AdapterUsage(
                adapter_name="manual_log_adapter",
                adapter_version="0.0.0-pre-implementation",
                capture_tier=CaptureTier.TIER_3,
            ),
            AdapterUsage(
                adapter_name="claude_code",
                adapter_version="0.1.0",
                capture_tier=CaptureTier.TIER_2,
            ),
        ],
        events=events,
        evidence=evidence,
        decisions=decisions,
        claims=claims,
        notes=(
            "Third AIVS audit (after Smith 2026 JCE and triplet-proof). "
            "Structural backbone: the v1 -> v3 retraction-and-rewrite "
            "cycle. The v1 analysis (scalar Ree ACF + single-exponential "
            "fit with p0=1000 ps initial guess and a bare 'except' that "
            "silently returned NaN) produced four headline claims that "
            "were fitting artifacts. The error was discovered, the "
            "analysis was rebuilt around an end-to-end VECTOR ACF + "
            "stretched-exponential fit + a new arrest metric (Ree_CV), "
            "and the manuscript was rewritten around CONFORMATIONAL "
            "ARREST rather than TIMESCALE SLOWING. The AI-augmented "
            "workflow caught its own error and recorded the retraction "
            "openly. This audit anchors claims to the corrected v3 "
            "manuscript (JPCB_submission_v3.tex). The two Claude Code "
            "session JSONLs (~4.5 MB combined) are bulk-referenced; the "
            "claude_code_adapter exists but is intentionally not invoked "
            "here (session_id, byte_size, mtime are the evidence). A "
            "future adapter-driven re-audit can enumerate fine-grained "
            "events.\n\n"
            "Audit baseline: 2026-04-25 (after the final wrap-up "
            "session). Outstanding pre-submission items recorded in "
            "HISTORY.md 2026-04-25 but not blocking this audit's "
            "integrity: references.bib [VERIFY] tags, no Author "
            "Contributions section, REVIEWER_COVER_NOTE.md author block "
            "not yet synced, no real GitHub/Zenodo deposit before "
            "submission. These would surface as new Decisions in a "
            "post-submission audit."
        ),
    )

    audit.schema_deltas = build_schema_deltas(audit.audit_id, evidence)
    return audit


def main() -> None:
    audit = build_audit()
    errors = audit.validate_integrity()
    if errors:
        print("INTEGRITY ERRORS:")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)

    out_path_override = os.environ.get("AIVS_OUT_PATH")
    if out_path_override:
        out_path = Path(out_path_override)
    else:
        out_path = (
            Path(__file__).resolve().parent / "kappa_friction_audit.json"
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(audit.model_dump_json(indent=2))

    counts = {
        "events": len(audit.events),
        "evidence": len(audit.evidence),
        "decisions": len(audit.decisions),
        "claims": len(audit.claims),
        "schema_deltas": len(audit.schema_deltas),
    }
    print("=== AIVS retrospective audit ===")
    print(f"  target              : {audit.audit_target}")
    print(f"  audit_id            : {audit.audit_id}")
    print(f"  meta_schema_version : {audit.meta_schema_version}")
    print(f"  vocabulary_version  : {audit.vocabulary_version}")
    print(f"  capture_tier        : {audit.capture_tier_achieved.value}")
    print(f"  integrity           : OK")
    print(f"  counts              : {json.dumps(counts)}")
    print(f"  output              : {out_path}")
    print()
    print("Schema-delta proposals (candidate v0.2 vocabulary terms):")
    for sd in audit.schema_deltas:
        print(f"  - {sd.proposed_term}")


if __name__ == "__main__":
    main()
