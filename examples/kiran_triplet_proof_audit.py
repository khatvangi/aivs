"""
Retrospective AIVS audit of:

[Authors TBD]. "Triplet architecture enables deep error-minimization in the
genetic code." Submission-ready for Journal of Molecular Evolution (JME).
Project at /storage/kiran-stuff/triplet-proof, origin/main @ 41c451b (2026-04-22).

This is the second AIVS audit (after Smith 2026) and the first against a
computational research project of substantial scope. The author (Kiran)
maintains a structured Q/A decision log (HISTORY.md) which functions as a
hand-curated audit substrate. The audit consumes this log as primary
evidence, supplemented by:

  - manuscript_JME.md (17 KB) for claims
  - rebuild_notes.md (12 KB) for design rationale
  - .claude/memory/paper1_codon_length.md for project status
  - .claude/projects/-storage-kiran-stuff-triplet-proof/*.jsonl
    (three Claude Code session logs: 7.9 MB + 116 KB + 47 KB)

The full claude_code_adapter would parse these JSONL files into thousands of
NormalizedEvents. This audit references them as bulk evidence (event_count,
session_id, byte_size) without enumerating every event, because the
adapter does not exist yet. When it does, this audit can be re-run with
finer-grained event resolution.

Capture tier: 3 — Kiran's HISTORY.md alone reaches Tier 3 for the documented
decisions; the session JSONLs would push to Tier 3+ with adapter support.

Run:
    python -m examples.kiran_triplet_proof_audit
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
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
from aivs.adapters.claude_code import ClaudeCodeAdapter


AUDIT_TS = datetime(2026, 5, 11, 0, 0, 0, tzinfo=timezone.utc)


# The audit's baseline contract: state of triplet-proof at the submission-
# ready milestone, git origin/main @ 41c451b (2026-04-22). Adapter events
# are filtered to this cutoff so the artifact maps cleanly to that snapshot.
# A current-state audit (HEAD-anchored) would be a separate artifact.
AUDIT_BASELINE_TS = datetime(2026, 4, 22, 23, 59, 59, tzinfo=timezone.utc)

# Where the project lives on disk; the adapter uses this to locate the
# Claude Code session JSONLs via ~/.claude/projects/<path-hash>/.
TRIPLET_PROOF_PATH = Path("/storage/kiran-stuff/triplet-proof")

# Half-width of the per-decision evidence window around each Decision's
# documented timestamp. Empirically this covers a HISTORY.md session
# (early/mid/late/wrap sessions on the same calendar day fit within a
# 24-hour two-sided window).
DECISION_WINDOW = timedelta(hours=12)


# HISTORY.md timestamps (UTC, time-of-day approximate).
T_2026_04_14 = datetime(2026, 4, 14, 12, 0, 0, tzinfo=timezone.utc)
T_2026_04_21_EARLY = datetime(2026, 4, 21, 9, 0, 0, tzinfo=timezone.utc)
T_2026_04_21 = datetime(2026, 4, 21, 14, 0, 0, tzinfo=timezone.utc)
T_2026_04_21_LATE = datetime(2026, 4, 21, 19, 0, 0, tzinfo=timezone.utc)
T_2026_04_22 = datetime(2026, 4, 22, 12, 0, 0, tzinfo=timezone.utc)
T_2026_04_22_WRAP = datetime(2026, 4, 22, 17, 0, 0, tzinfo=timezone.utc)


# Actors
KIRAN = Actor(actor_type=ActorType.HUMAN, identifier="Kiran (author/PI)")
PAUDYAL = Actor(actor_type=ActorType.HUMAN, identifier="Paudyal (reviewer/colleague)")
CLAUDE_CODE = Actor(
    actor_type=ActorType.AI_AUTONOMOUS,
    identifier="Claude Code (Anthropic)",
    model_metadata={
        "product": "Claude Code",
        "version_observed_in_sessions": "2.1.97",
        "underlying_model_versioning": "not pinned in session metadata",
        "note": (
            "Sessions span late 2025 through 2026-04; underlying model may "
            "have rolled forward without explicit logging."
        ),
    },
)


def _src(location: str) -> SourceRef:
    return SourceRef(
        adapter_name="manual_log_adapter",
        adapter_version="0.0.0-pre-implementation",
        raw_location=location,
        extracted_at=AUDIT_TS,
    )


# Convenience for Claude Code session references (used in multiple events).
SESSION_1 = "101e5996-1d44-46d2-a9aa-ef58c8bc1cbf"  # 7.9 MB, origin session per memory
SESSION_2 = "2e5b0b3e-c809-45eb-8908-a40b22af0a97"  # 47 KB
SESSION_3 = "e36c3254-ad1a-4463-a52e-d40c484bb5e5"  # 116 KB

CLAUDE_PROJECTS_PATH = ".claude/projects/-storage-kiran-stuff-triplet-proof"


# ---------------------------------------------------------------------------
# Events
#
# Two sources now contribute events to this audit:
#   (1) build_bulk_session_events() — three coarse session-scope Events,
#       one per JSONL. Kept (rather than dropped in favor of fine-grained
#       adapter events) because D14 (Q/A development log methodology)
#       reasons over WHOLE SESSIONS, not over individual prompts/tool
#       uses within them.
#   (2) extract_adapter_events() — ~600 fine-grained Events emitted by
#       the claude_code_adapter, filtered to AUDIT_BASELINE_TS so the
#       artifact maps cleanly to the submission-ready milestone at
#       commit 41c451b (2026-04-22). Anything past that date belongs in
#       a separate HEAD-anchored audit, not this one.
# ---------------------------------------------------------------------------


def build_bulk_session_events() -> list[Event]:
    """Three coarse Events, one per Claude Code session JSONL."""
    events: list[Event] = []
    for sid, size_bytes in [
        (SESSION_1, 7_916_073),
        (SESSION_2, 47_112),
        (SESSION_3, 116_218),
    ]:
        events.append(
            Event(
                timestamp=T_2026_04_14,  # session start dates not parsed from JSONL here
                actor=KIRAN,
                action="session_bulk_reference",
                target=f"claude_code_session:{sid}",
                content=(
                    f"Bulk reference to Claude Code session {sid}: "
                    f"{size_bytes:,} bytes of JSONL. Fine-grained events "
                    f"extracted by the claude_code_adapter sit alongside "
                    f"this bulk reference in the artifact's events list."
                ),
                source_ref=_src(f"{CLAUDE_PROJECTS_PATH}/{sid}.jsonl"),
                tier=CaptureTier.TIER_2,
            )
        )
    return events


def extract_adapter_events() -> list[Event]:
    """Adapter-extracted events from the triplet-proof session JSONLs.

    Filtered to ``until=AUDIT_BASELINE_TS`` so the audit reflects only
    the submission-ready snapshot, not anything written after.
    """
    adapter = ClaudeCodeAdapter(verbosity="default")
    return list(
        adapter.extract(TRIPLET_PROOF_PATH, until=AUDIT_BASELINE_TS)
    )


# --- legacy stub kept for backward import compatibility ----------------------


def build_events() -> list[Event]:
    """Backwards-compatible entry point: returns bulk + adapter events.

    New code should call ``build_bulk_session_events()`` and
    ``extract_adapter_events()`` directly.
    """
    return build_bulk_session_events() + extract_adapter_events()


# ---------------------------------------------------------------------------
# Evidence — one per Decision, each scoped to a time window over the adapter
# event stream. D14 (Q/A development log methodology) is the exception:
# meta-methodological pattern over WHOLE sessions, so it gets a bulk Evidence.
#
# Each Evidence description starts with a "D<n>:" prefix so the decision
# builder can resolve them via a simple prefix lookup without coupling to
# Evidence ordering.
# ---------------------------------------------------------------------------


def _window_event_ids(
    adapter_events: list[Event],
    center: datetime,
    half: timedelta = DECISION_WINDOW,
) -> list[str]:
    """Adapter event_ids whose timestamps fall in [center-half, center+half],
    capped at AUDIT_BASELINE_TS so post-baseline activity never leaks in."""
    lo = center - half
    hi = min(center + half, AUDIT_BASELINE_TS)
    return [e.event_id for e in adapter_events if lo <= e.timestamp <= hi]


def build_evidence(
    adapter_events: list[Event],
    bulk_session_events: list[Event],
) -> list[Evidence]:
    """Build 14 Evidence objects: 13 windowed (D1–D13) + 1 bulk (D14)."""

    def windowed(d_key: str, center: datetime, label: str) -> Evidence:
        event_ids = _window_event_ids(adapter_events, center)
        return Evidence(
            event_ids=event_ids,
            description=(
                f"{d_key}: {label} — {len(event_ids)} Claude Code adapter "
                f"events within ±{int(DECISION_WINDOW.total_seconds() // 3600)}h "
                f"of {center:%Y-%m-%d %H:%M UTC}, capped at the audit "
                f"baseline {AUDIT_BASELINE_TS:%Y-%m-%d %H:%M UTC}."
            ),
            confidence=EvidenceConfidence.HIGH,
        )

    evidence: list[Evidence] = [
        windowed(
            "D1",
            T_2026_04_14,
            "MBE-Letter figure-generation session (initial work)",
        ),
        windowed(
            "D2",
            T_2026_04_21,
            "Prior-art verification session (D/E metrics vs Tlusty, Radvanyi-Kun)",
        ),
        windowed(
            "D3",
            T_2026_04_21,
            "Introduction repositioning consequent on D2",
        ),
        windowed(
            "D4",
            T_2026_04_22_WRAP,
            "Final-consolidation session: n=4 factorial cell exclusion",
        ),
        windowed(
            "D5",
            T_2026_04_21_EARLY,
            "Figure rebuild + supplementary cleanup (sensitivity 3-seed)",
        ),
        windowed(
            "D6",
            T_2026_04_21_EARLY,
            "Manuscript discrepancy disposition: Methods '<0.5 units'",
        ),
        windowed(
            "D7",
            T_2026_04_21_EARLY,
            "Manuscript discrepancy disposition: Fig 1c '‖Δf‖ = 8.7'",
        ),
        windowed(
            "D8",
            T_2026_04_21_LATE,
            "Stale Table S1 reconciliation session",
        ),
        windowed(
            "D9",
            T_2026_04_22,
            "Defensive metric precomputation (f^T L^2 f + Boltzmann D)",
        ),
        windowed(
            "D10",
            T_2026_04_22_WRAP,
            "Figure consolidation + repo cleanup commits 3941a48, 41c451b",
        ),
        windowed(
            "D11",
            T_2026_04_14,
            "Figure 1 (a)/(c) hand-drawn vs (b) programmatic split decision",
        ),
        windowed(
            "D12",
            T_2026_04_21_EARLY,
            "Figure 3 layout: single-axis overlay vs stacked mini-hists",
        ),
        windowed(
            "D13",
            T_2026_04_21_EARLY,
            "Figure 1(a) Hamming graph spring-layout parameters",
        ),
        # D14: bulk evidence — meta-methodological, spans whole sessions.
        Evidence(
            event_ids=[e.event_id for e in bulk_session_events],
            description=(
                "D14 (bulk): three Claude Code session JSONL logs (8.1 MB "
                "combined) taken as a whole. The Q/A development-log "
                "methodology is a pattern *over* sessions, not a windowed "
                "event stream within one. Each bulk session Event references "
                "the JSONL file at the raw_location of its source_ref."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
    ]
    return evidence


# ---------------------------------------------------------------------------
# Decisions
# ---------------------------------------------------------------------------


def build_decisions(evidence: list[Evidence]) -> list[Decision]:
    by_prefix = {e.description[:60]: e.evidence_id for e in evidence}

    def E(prefix: str) -> str:
        for k, v in by_prefix.items():
            if k.startswith(prefix):
                return v
        raise KeyError(prefix)

    decisions: list[Decision] = []

    # D1: Target journal change (MBE Letter → JME)
    decisions.append(
        Decision(
            timestamp=T_2026_04_14,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Target journal change: 2026-04-14 figure-generation session "
                "targeted MBE Letter; by 2026-04-21 onward all subsequent "
                "work targets JME (filenames manuscript_JME.md, "
                "cover_letter_JME.md, etc.). Reason for change not "
                "documented in available evidence."
            ),
            actor=KIRAN,
            evidence_ids=[E("D1:")],
            verification_status=VerificationStatus.NO_EVIDENCE,
            verification_notes="Change visible in filenames but rationale not captured.",
        )
    )

    # D2: Prior-art verification triggered by reviewer/colleague
    decisions.append(
        Decision(
            timestamp=T_2026_04_21,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Prior-art verification: Paudyal raised whether D and E "
                "metrics have prior art. Decision: explicitly verify against "
                "Tlusty 2007/2010 and Radvanyi & Kun 2021 BEFORE making "
                "citation decisions. Result: both metrics are not novel; "
                "novelty repositioned to factorial design + empirical null."
            ),
            actor=KIRAN,
            evidence_ids=[E("D2:")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Verified by verbatim equation comparison in "
                "literature_comparison.md."
            ),
        )
    )

    # D3: Introduction repositioning consequence of D2
    decisions.append(
        Decision(
            timestamp=T_2026_04_21,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Introduction repositioning: as a consequence of D2, decision "
                "to position Introduction as 'we adopt Tlusty's rate-distortion "
                "framework and add a factorial design with an empirical null' "
                "rather than claiming novel metrics. Methods section also "
                "frames metrics as specializations rather than introductions. "
                "(Still listed as TODO in paper1_codon_length.md.)"
            ),
            actor=KIRAN,
            evidence_ids=[E("D3:")],
            verification_status=VerificationStatus.UNVERIFIED,
            verification_notes="Introduction rewrite remains on TODO list at audit time.",
        )
    )

    # D4: Factorial cell exclusion (n=4)
    decisions.append(
        Decision(
            timestamp=T_2026_04_22_WRAP,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Factorial cell exclusion: n=4 dropped from the 2x2 factorial. "
                "Reason: n=4 baseline AA(b1 b2 b3 b4) := AA_SGC(b1 b2 b3) "
                "makes position 4 100% synonymous by construction, so the "
                "z-score is a construction artefact rather than a biological "
                "property. The n=4 machinery (run_phase2_n2n4.py, "
                "phase2_quadruplet.auto.json) is kept in the repo for "
                "exploratory use, with rationale added to docstrings."
            ),
            actor=KIRAN,
            evidence_ids=[E("D4:")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Reasoning is internal-consistency check: by construction the "
                "n=4 baseline cannot produce biologically meaningful z-score. "
                "Verified by author's own derivation; documented in commit "
                "41c451b and rebuild_notes.md."
            ),
        )
    )

    # D5: Sensitivity protocol revision (1-seed → 3-seed random)
    decisions.append(
        Decision(
            timestamp=T_2026_04_21_EARLY,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Sensitivity protocol revision: from 1 random seed to "
                "3-seed random-mean ± SD. Surfaced that the manuscript's "
                "'<0.5 units' sensitivity claim is FALSE for D (range 0.56) "
                "and was always false for E (range 0.92). Table S1 updated to "
                "report honest 3-seed numbers."
            ),
            actor=KIRAN,
            evidence_ids=[E("D5:")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes="Verified by direct recomputation at 3 seeds.",
        )
    )

    # D6: Manuscript discrepancy: "<0.5 units" stale claim
    decisions.append(
        Decision(
            timestamp=T_2026_04_21_EARLY,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Manuscript discrepancy disposition (<0.5 units): the Methods "
                "claim 'sensitivity <0.5 units' is false at 3 random seeds. "
                "Decision: keep claim provisional until Methods prose is "
                "rewritten; Table S1 in supplementary already reports honest "
                "0.56 and 0.92 values. Recommended replacement wording drafted "
                "in rebuild_notes.md. Listed as still-pending TODO in "
                "paper1_codon_length.md."
            ),
            actor=KIRAN,
            evidence_ids=[E("D6:")],
            verification_status=VerificationStatus.UNVERIFIED,
            verification_notes=(
                "Discrepancy IDENTIFIED but Methods prose not yet rewritten. "
                "Pending TODO at audit time."
            ),
        )
    )

    # D7: Manuscript discrepancy: "‖Δf‖ = 8.7 radical"
    decisions.append(
        Decision(
            timestamp=T_2026_04_21_EARLY,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Manuscript discrepancy disposition (||Δf|| = 8.7 for "
                "radical): the value 8.7 is outside the achievable range of "
                "the 8-PC space (max pairwise = 6.23, G-P). Two viable fixes: "
                "(i) update prose to actual values for Ala neighborhood "
                "(0 / 3.5-4.9); (ii) keep illustrative claim and substitute "
                "a real radical pair (e.g., G-P at 6.23 or E-P at 5.81). "
                "Choice deferred to author at submission time."
            ),
            actor=KIRAN,
            evidence_ids=[E("D7:")],
            verification_status=VerificationStatus.UNVERIFIED,
            verification_notes=(
                "Discrepancy IDENTIFIED but Fig 1c prose not yet rewritten. "
                "Pending TODO at audit time."
            ),
        )
    )

    # D8: Stale Table S1 reconciliation
    decisions.append(
        Decision(
            timestamp=T_2026_04_21_LATE,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Stale supplementary disposition: Table S1 reconciliation. "
                "Old z-scores (closest -14.87 / -13.41; farthest -14.57 / "
                "-13.12; random -15.08 / -13.73) traced to a prior Monte "
                "Carlo run; replaced with current values from "
                "publication_controls.json. Differences ~0.08 z-units "
                "across multiple cells. Decision: trust current run; "
                "replace stale values throughout supplementary."
            ),
            actor=KIRAN,
            evidence_ids=[E("D8:")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Reconciled against publication_controls.json (definitive numbers)."
            ),
        )
    )

    # D9: Defensive metric precomputation
    decisions.append(
        Decision(
            timestamp=T_2026_04_22,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Defensive metric precomputation: pre-emptively compute "
                "f^T L^2 f (Tlusty-style squared Laplacian) and Boltzmann-"
                "weighted D, anticipating reviewer pushback that the "
                "manuscript's specific metric choices are arbitrary. "
                "Result: both alternatives either track tightly (L^2 case) or "
                "strengthen the SGC result (Boltzmann case). Manuscript "
                "narrative changed to 'our choice is conservative.'"
            ),
            actor=KIRAN,
            evidence_ids=[E("D9:")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "100K-shuffle precomputation against publication_controls null; "
                "results in preempt_metrics.json. Conservatism claim is "
                "verifiable by side-by-side comparison."
            ),
        )
    )

    # D10: Figure consolidation (9 exploratory → 4 canonical)
    decisions.append(
        Decision(
            timestamp=T_2026_04_22_WRAP,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Figure consolidation: 9 exploratory figure scripts + 18 "
                "images replaced with canonical fig1.py-fig4.py + figS1 "
                "(20 files total). Each figure script emits .pdf (vector, "
                "fonttype 42), .png (300 DPI), and _caption.txt. Decision "
                "rationale: pre-submission clean state minimizes reviewer "
                "confusion; exploratory variants are archived in git history."
            ),
            actor=KIRAN,
            evidence_ids=[E("D10:")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
        )
    )

    # D11: Figure panel authorship split (programmatic vs hand-drawn)
    decisions.append(
        Decision(
            timestamp=T_2026_04_14,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Figure panel authorship split: Figure 1 panels (a) and (c) "
                "left for hand-drawing in Illustrator/Inkscape; only the "
                "data-driven panel (b) was generated programmatically. "
                "Rationale: schematic content of (a) and (c) is "
                "non-algorithmic. Listed as still-TODO in paper1_codon_length.md."
            ),
            actor=KIRAN,
            evidence_ids=[E("D11:")],
            verification_status=VerificationStatus.UNVERIFIED,
            verification_notes="Hand-drawing remains a TODO at audit time.",
        )
    )

    # D12: Figure 3 layout choice (overlay vs stacked)
    decisions.append(
        Decision(
            timestamp=T_2026_04_21_EARLY,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Figure 3 layout choice: single-x-axis overlay (alpha=0.5) "
                "over stacked mini-histograms. Rationale: the B and C null "
                "distributions substantially overlap in D-space (~28-34), and "
                "this co-location is the visual evidence that the factorial "
                "architecture effect dominates the alphabet effect. Stacked "
                "mini-histograms lose this property. Also dropped the (a)/"
                "(b)/(c) three-panel structure from the original prompt."
            ),
            actor=KIRAN,
            evidence_ids=[E("D12:")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Documented in rebuild_notes.md. Verification mode: design "
                "rationale by author with explicit comparison of alternatives "
                "tried."
            ),
        )
    )

    # D13: Hamming graph layout algorithm choice
    decisions.append(
        Decision(
            timestamp=T_2026_04_21_EARLY,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Figure 1(a) Hamming graph layout: spring layout (seed=7, "
                "k=0.35, 300 iterations) chosen over spectral and "
                "kamada_kawai, which produced more tangled layouts for the "
                "61-node, avg-degree-8.6 graph. Central nodes unlabelled; "
                "five peripheral anchors (UUU/GGG/CAG/AAA/UCC) provide "
                "compass orientation. AUG dropped from anchors because "
                "spring layout places it near centroid where label would "
                "collide."
            ),
            actor=KIRAN,
            evidence_ids=[E("D13:")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
        )
    )

    # D14: Q/A development log methodology itself
    decisions.append(
        Decision(
            timestamp=T_2026_04_14,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Q/A development log methodology: Kiran maintains HISTORY.md "
                "as a structured per-session Q/A record (question to Claude "
                "Code → answer/outcome). Decisions, design rationale, "
                "discrepancies, and TODOs are surfaced in this format. This "
                "methodology is itself an AIVS-relevant pattern — Kiran is "
                "performing a continuous, light-weight hand-audit which AIVS "
                "is formalizing into a machine-readable schema."
            ),
            actor=KIRAN,
            evidence_ids=[E("D14")],
            verification_status=VerificationStatus.NOT_APPLICABLE,
            verification_notes=(
                "Methodological choice; not subject to fact-verification. "
                "Notable as a vocabulary candidate."
            ),
        )
    )

    return decisions


# ---------------------------------------------------------------------------
# Claims (from manuscript)
# ---------------------------------------------------------------------------


def build_claims(decisions: list[Decision]) -> list[Claim]:
    d = {dec.description[:50]: dec.decision_id for dec in decisions}

    def D(prefix: str) -> str:
        for k, v in d.items():
            if k.startswith(prefix):
                return v
        raise KeyError(prefix)

    return [
        Claim(
            text=(
                "Against 1,000,000 random codes with matched codon-count "
                "degeneracy, the SGC outperformed all sampled alternatives "
                "on both metrics (Dirichlet z = -14.61; distortion z = -16.57; "
                "empirical p < 10^-6 for both)."
            ),
            location="Abstract; Results §3.1",
            upstream_decision_ids=[
                D("Prior-art verification"),
                D("Sensitivity protocol revision"),
                D("Defensive metric precomputation"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        Claim(
            text=(
                "The SGC-derived doublet projection (Condition A) remained "
                "better than most random codes but not exceptionally so "
                "(distortion z = -3.80; Dirichlet z = -3.32). Empirical tail "
                "probabilities 1.08e-4 and 4.66e-4 respectively."
            ),
            location="Abstract; Results §3.2",
            upstream_decision_ids=[
                D("Sensitivity protocol revision"),
                D("Factorial cell exclusion"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        Claim(
            text=(
                "Architecture effect (n=2 to n=3, same 10 AAs): -11.01 z-units "
                "for distortion and -10.02 for Dirichlet energy. Alphabet "
                "effect (10 to 20 AAs, same triplet length): -1.76 and -1.27. "
                "Architecture:alphabet ratio: 6.3:1 (D) and 7.9:1 (E)."
            ),
            location="Abstract; Results §3.3",
            upstream_decision_ids=[
                D("Factorial cell exclusion"),
                D("Figure 3 layout choice"),
                D("Sensitivity protocol revision"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        Claim(
            text=(
                "Position-3 synonymy in the SGC = 68.9%; position-1 = 4.4%; "
                "position-2 = 0%. In 10-AA triplet control: position-3 "
                "synonymy rises to 76.5%. Wobble-like third position is the "
                "mechanistic basis."
            ),
            location="Abstract; Results §3.4",
            upstream_decision_ids=[
                D("Figure 3 layout choice"),
                D("Figure 1(a) Hamming graph layout"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        Claim(
            text=(
                "Amino acids represented in an 8-dimensional PCA space "
                "explaining 97.1% of total variance from 20 standardized "
                "physicochemical descriptors."
            ),
            location="Methods §2.1",
            upstream_decision_ids=[D("Prior-art verification")],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        Claim(
            text=(
                "Sensitivity to representative-set choice: z-score ranges "
                "across strategies are 0.56 (D) and 0.92 (E) — small "
                "compared to ~15 SD displacement from the null. "
                "(Manuscript currently states '<0.5' — pending Methods prose fix.)"
            ),
            location="Methods §2.5 (pending correction)",
            upstream_decision_ids=[
                D("Sensitivity protocol revision"),
                D("Manuscript discrepancy disposition (<0.5"),
            ],
            evidence_confidence=EvidenceConfidence.MEDIUM,
        ),
        Claim(
            text=(
                "Defensive verification: f^T L^2 f tracks f^T L f at null "
                "r=0.987; Boltzmann-weighted D strengthens SGC z-score by "
                "5-8 units. Manuscript's uniform-D + unsquared Laplacian "
                "choice is conservative — a mechanism-minded reviewer would "
                "compute a stronger result."
            ),
            location="Discussion (defensive paragraph); preempt_metrics.json",
            upstream_decision_ids=[D("Defensive metric precomputation")],
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
            "target_journal_change",
            (
                "Decision to switch the target journal for a manuscript mid-"
                "project; tracks filename/template changes and reframing."
            ),
        ),
        (
            "prior_art_verification",
            (
                "Explicit decision to verify whether claimed novel methods or "
                "metrics have existing literature precedent, separate from the "
                "decision of how to cite afterwards."
            ),
        ),
        (
            "factorial_cell_exclusion",
            (
                "Decision to exclude a factorial design cell with documented "
                "rationale (e.g., construction artefact, identifiability "
                "failure, biological irrelevance)."
            ),
        ),
        (
            "sensitivity_protocol_revision",
            (
                "Mid-project change to the sensitivity-analysis protocol "
                "(e.g., increasing the number of random seeds, broadening the "
                "parameter sweep) that exposes manuscript claims requiring "
                "revision."
            ),
        ),
        (
            "manuscript_internal_discrepancy_disposition",
            (
                "Decision about a specific manuscript claim found to be "
                "inconsistent with the underlying data or scripts: fix-now, "
                "fix-later, or substantive revision. Smith 2026 audit "
                "surfaced a related pattern (ai_error_disposition); this is "
                "the human-author version."
            ),
        ),
        (
            "defensive_metric_precomputation",
            (
                "Decision to compute alternative metrics anticipating "
                "reviewer pushback, separate from the manuscript's headline "
                "metric. Outcome may strengthen or weaken the headline; "
                "either way, makes the choice of headline metric defensible."
            ),
        ),
        (
            "repository_consolidation_for_submission",
            (
                "Pre-submission decision to retire exploratory artifacts "
                "(scripts, figure variants) in favor of a clean canonical "
                "set, archiving variants in git history. Tracks commit IDs."
            ),
        ),
        (
            "figure_panel_authorship_split",
            (
                "Decision to assign different authorship modes to different "
                "panels of the same figure: programmatic (data-driven, "
                "scripted) vs hand-drawn (schematic, illustrator). Tracks "
                "which panels were AI-assisted vs not."
            ),
        ),
        (
            "design_decision_documentation_via_qa_log",
            (
                "Methodological pattern: maintaining a structured Q/A "
                "(prompt-and-outcome) journal alongside the project as a "
                "human-readable decision log. Kiran's HISTORY.md instantiates "
                "this pattern; AIVS formalizes it into structured Decision "
                "entities."
            ),
        ),
        (
            "introduction_repositioning",
            (
                "Decision to reframe the Introduction in response to "
                "prior-art verification: shift the novelty claim from a "
                "method or metric to a design choice (factorial design, "
                "empirical null protocol)."
            ),
        ),
        (
            "vocabulary_term_recurrence_signal",
            (
                "Meta-observation: vocabulary terms that surface in two or "
                "more independent audits should be promoted from "
                "schema_delta_proposed to vocabulary_accepted. In this audit, "
                "the candidates that overlap with Smith 2026 are: "
                "prompt_engineering (Smith's narrative; Kiran's HISTORY.md "
                "Q-entries), iterative_ai_generation (Smith's three "
                "podcasts; Kiran's three rebuild sessions), "
                "manuscript_internal_discrepancy_disposition (Smith's three "
                "AI errors; Kiran's two stale-claim findings — though Smith's "
                "are AI errors and Kiran's are human stale claims, the "
                "structural decision is the same)."
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
    # Event stream is built once at the top: three bulk-session Events plus
    # the adapter-extracted fine-grained stream, filtered to the audit's
    # baseline. Per-Decision Evidence is then windowed against the adapter
    # stream.
    bulk_events = build_bulk_session_events()
    adapter_events = extract_adapter_events()
    all_events = bulk_events + adapter_events

    evidence = build_evidence(adapter_events, bulk_events)
    decisions = build_decisions(evidence)
    claims = build_claims(decisions)

    audit = AuditArtifact(
        audit_target=(
            "/storage/kiran-stuff/triplet-proof "
            "(git origin/main @ 41c451b; submission-ready 2026-04-22; "
            "target journal JME)"
        ),
        vocabulary_version="0.1.0",
        capture_tier_achieved=CaptureTier.TIER_3,
        audit_timestamp=AUDIT_TS,
        adapters_used=[
            AdapterUsage(
                adapter_name="claude_code",
                adapter_version="0.1.0",
                capture_tier=CaptureTier.TIER_3,
            ),
            AdapterUsage(
                adapter_name="manual_log_adapter",
                adapter_version="0.0.0-pre-implementation",
                capture_tier=CaptureTier.TIER_2,
            ),
        ],
        events=all_events,
        evidence=evidence,
        decisions=decisions,
        claims=claims,
        notes=(
            "Second AIVS audit (after Smith 2026 JCE). First on a "
            "computational research project of substantial scope. "
            "Refreshed 2026-05-11 to use adapter-derived fine-grained "
            "Events: each Decision's Evidence is now windowed (±12h) "
            "against the claude_code_adapter event stream from "
            "/storage/kiran-stuff/triplet-proof. The three coarse "
            "session-bulk Events are retained for D14 (Q/A development "
            "log methodology), which reasons over whole sessions, not "
            "individual prompts. Adapter events are filtered to "
            f"{AUDIT_BASELINE_TS:%Y-%m-%d %H:%M UTC} so the artifact "
            "maps cleanly to the submission-ready baseline at git "
            "origin/main @ 41c451b. Post-baseline activity (the "
            "2026-04-23 SVG-panel render commit and any subsequent "
            "uncommitted work) is intentionally excluded; a "
            "HEAD-anchored audit would be a separate artifact.\n\n"
            "Significant: Kiran's HISTORY.md format functions as a hand-"
            "curated AIVS-style audit substrate. AIVS is essentially "
            "formalizing a discipline Kiran already practices."
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

    out_path = Path(
        os.environ.get(
            "AIVS_OUT_DIR",
            str(Path(__file__).resolve().parent / "out"),
        )
    ) / "kiran_triplet_proof_audit.json"
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
