"""
Retrospective AIVS audit of:

Smith, D.K. "Creating a Podcast Using Generative Artificial Intelligence to
Support Student Learning of Organic Reaction Mechanisms."
J. Chem. Educ. 2026, 103, 2077-2084. DOI: 10.1021/acs.jchemed.5c01652

This is a manual audit, not a tool run — there are no adapters yet. Evidence
is drawn from (a) the paper body text and (b) the Supporting Information,
both of which are co-located with this script at
``docs/case_studies/smith_2026_jce_main.pdf`` and
``docs/case_studies/smith_2026_jce_si.pdf``. The audit treats the published
paper + SI as a Tier-3 capture:
Smith voluntarily provided full user prompts, full AI outputs, source-document
provenance, workload measurements, and explicit error-disposition decisions.

The audit is intentionally faithful to Smith's documented workflow. It does
not extrapolate or speculate about decisions Smith did not describe. Where
the paper is ambiguous (e.g., the relationship between the body text's
"initial podcast" prompt and the SI's V1 prompt), the audit prefers the SI
labeling and notes the ambiguity in `verification_notes`.

The v0.1 vocabulary is empty, so every decision is necessarily
`decision_type="unclassified"` with `schema_gap="novel_pattern"`. Each is
accompanied by a SchemaDelta proposing a candidate vocabulary term. These
deltas are the empirical foundation of v0.2 vocabulary.

Run:
    python -m examples.smith_2026_audit
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


# Audit timestamp (when this audit was constructed, not when events occurred).
AUDIT_TS = datetime(2026, 5, 11, 0, 0, 0, tzinfo=timezone.utc)

# Approximate workflow timestamps. Smith's paper gives a sequence but not
# absolute dates; we use the manuscript timeline (Received Nov 17 2025) to
# anchor the workflow to autumn 2025. Exact dates are unknown — `evidence:
# medium` and `verification_notes` document this honestly.
T_INITIAL = datetime(2025, 9, 1, 12, 0, 0, tzinfo=timezone.utc)
T_V1 = datetime(2025, 9, 15, 12, 0, 0, tzinfo=timezone.utc)
T_REVISION = datetime(2025, 9, 20, 12, 0, 0, tzinfo=timezone.utc)
T_V2 = datetime(2025, 9, 25, 12, 0, 0, tzinfo=timezone.utc)
T_V3 = datetime(2025, 9, 25, 14, 0, 0, tzinfo=timezone.utc)
T_CURATION = datetime(2025, 10, 5, 12, 0, 0, tzinfo=timezone.utc)
T_TRANSCRIPTION = datetime(2025, 10, 10, 12, 0, 0, tzinfo=timezone.utc)
T_VISUAL = datetime(2025, 10, 12, 12, 0, 0, tzinfo=timezone.utc)


# Actors.
SMITH = Actor(actor_type=ActorType.HUMAN, identifier="David K. Smith (ORCID 0000-0002-9881-2714)")
NOTEBOOKLM = Actor(
    actor_type=ActorType.AI_GENERATIVE,
    identifier="Google NotebookLM",
    model_metadata={
        "provider": "Google",
        "product": "NotebookLM",
        "feature": "Audio Overview / Deep Dive",
        "note": "Specific underlying model and version not disclosed in publication.",
    },
)
PANOPTO = Actor(
    actor_type=ActorType.SYSTEM,
    identifier="Panopto (University of York deployment)",
    model_metadata={"feature": "auto-captioning / transcription"},
)


# Source-ref helper: all evidence in this audit comes from two PDFs we read.
def _src(location: str) -> SourceRef:
    return SourceRef(
        adapter_name="manual_log_adapter",
        adapter_version="0.0.0-pre-implementation",
        raw_location=location,
        extracted_at=AUDIT_TS,
    )


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------


def build_events() -> list[Event]:
    events: list[Event] = []

    # Source-document selection: Smith provided his own 2023 JCE paper.
    events.append(
        Event(
            timestamp=T_INITIAL,
            actor=SMITH,
            action="select_input",
            target="source_document:Smith_2023_JCE_priority_rules_paper",
            content=(
                "'Google NotebookLM was provided with my open-access Journal "
                "of Chemical Education paper as source material.'"
            ),
            source_ref=_src("paper.body:Podcast_Generation:first_paragraph"),
            tier=CaptureTier.TIER_3,
        )
    )

    # Initial prompt (body text) — distinct from SI V1 prompt.
    events.append(
        Event(
            timestamp=T_INITIAL,
            actor=SMITH,
            action="prompt",
            target="notebooklm_session:initial",
            content=(
                "explore the importance of organic reaction mechanisms, "
                "explaining how priority and selectivity rules can enable "
                "students to predict organic reaction mechanisms"
            ),
            source_ref=_src("paper.body:Podcast_Generation:initial_prompt"),
            tier=CaptureTier.TIER_3,
        )
    )

    # SI Podcast Version 1 — full user prompt.
    events.append(
        Event(
            timestamp=T_V1,
            actor=SMITH,
            action="prompt",
            target="notebooklm_session:V1",
            content=(
                "Explain why having rules to predict organic reaction "
                "mechanisms is important and useful then describe all of the "
                "rules for predicting organic reaction mechanisms and discuss "
                "how to apply them."
            ),
            source_ref=_src("SI:PODCAST_VERSION_1:USER_PROMPT"),
            tier=CaptureTier.TIER_3,
        )
    )

    # AI generates V1 podcast.
    events.append(
        Event(
            timestamp=T_V1,
            actor=NOTEBOOKLM,
            action="generate",
            target="podcast_audio:V1",
            content=(
                "Title: 'Cracking the Code: The 5 Algorithmic Rules to Predict "
                "Organic Chemistry Mechanisms (No Memorization Required)'. "
                "Full transcript in SI."
            ),
            source_ref=_src("SI:PODCAST_VERSION_1:AI_OUTPUT"),
            tier=CaptureTier.TIER_3,
        )
    )

    # V2 — no user prompt; NotebookLM auto-generated from revised source.
    events.append(
        Event(
            timestamp=T_V2,
            actor=SMITH,
            action="prompt",
            target="notebooklm_session:V2",
            content="(No prompt given. NotebookLM auto-generated from source.)",
            source_ref=_src("SI:PODCAST_VERSION_2:USER_PROMPT"),
            tier=CaptureTier.TIER_3,
        )
    )

    events.append(
        Event(
            timestamp=T_V2,
            actor=NOTEBOOKLM,
            action="generate",
            target="podcast_audio:V2",
            content=(
                "Title: 'From Cookbook to Logic: Mastering Organic Chemistry "
                "Mechanisms with 5 Priority Rules'. Full transcript in SI."
            ),
            source_ref=_src("SI:PODCAST_VERSION_2:AI_OUTPUT"),
            tier=CaptureTier.TIER_3,
        )
    )

    # V3 — explicit student-facing reframing.
    events.append(
        Event(
            timestamp=T_V3,
            actor=SMITH,
            action="prompt",
            target="notebooklm_session:V3",
            content=(
                "Explain to a student why we need to develop priority and "
                "selectivity rules to understand organic mechanisms, and then "
                "explain the basics of the priority and selectivity rules and "
                "how they work in practice to predict organic reactions."
            ),
            source_ref=_src("SI:PODCAST_VERSION_3:USER_PROMPT"),
            tier=CaptureTier.TIER_3,
        )
    )

    events.append(
        Event(
            timestamp=T_V3,
            actor=NOTEBOOKLM,
            action="generate",
            target="podcast_audio:V3",
            content=(
                "Title: 'From Rote Memorization to Operating System: The "
                "Priority Rules That Unravel Organic Chemistry Mechanisms'. "
                "Full transcript in SI."
            ),
            source_ref=_src("SI:PODCAST_VERSION_3:AI_OUTPUT"),
            tier=CaptureTier.TIER_3,
        )
    )

    # Source-document revision after V1 review.
    events.append(
        Event(
            timestamp=T_REVISION,
            actor=SMITH,
            action="edit",
            target="source_document:Smith_2023_JCE_priority_rules_paper",
            content=(
                "Lidocaine example removed from source document; replaced with "
                "new text on salbutamol synthesis. Section on classic reaction "
                "types (nucleophilic substitution/addition; electrophilic "
                "substitution/addition) also removed."
            ),
            source_ref=_src("paper.body:Podcast_Generation:lidocaine_to_salbutamol"),
            tier=CaptureTier.TIER_3,
        )
    )

    # Final curation in Audacity.
    events.append(
        Event(
            timestamp=T_CURATION,
            actor=SMITH,
            action="curate",
            target="podcast_audio:final",
            content=(
                "Audio from the three podcasts combined using Audacity, "
                "selecting the best analogies and liveliest discussions, "
                "removing errors or confusing descriptions."
            ),
            source_ref=_src("paper.body:Podcast_Generation:audacity_combination"),
            tier=CaptureTier.TIER_3,
        )
    )

    # Panopto transcription.
    events.append(
        Event(
            timestamp=T_TRANSCRIPTION,
            actor=PANOPTO,
            action="execute",
            target="podcast_audio:final.transcript",
            content=(
                "Final podcast uploaded to Panopto for auto-captioning; "
                "minor manual editing applied. Smith notes Panopto generated "
                "more accurate transcripts than NotebookLM's own transcription."
            ),
            source_ref=_src("paper.body:Podcast_Generation:panopto"),
            tier=CaptureTier.TIER_3,
        )
    )

    # Visual material.
    events.append(
        Event(
            timestamp=T_VISUAL,
            actor=SMITH,
            action="create",
            target="visual:salbutamol_synthesis.pptx",
            content=(
                "PowerPoint image created to provide essential visual support "
                "for the salbutamol synthesis discussed in the podcast; "
                "attached to the audio file."
            ),
            source_ref=_src("paper.body:Podcast_Generation:powerpoint"),
            tier=CaptureTier.TIER_3,
        )
    )

    return events


# ---------------------------------------------------------------------------
# Evidence (composite of events; one or more events per Evidence item).
# ---------------------------------------------------------------------------


def build_evidence(events: list[Event]) -> list[Evidence]:
    by_target = {e.target: e for e in events}

    return [
        Evidence(
            event_ids=[by_target["source_document:Smith_2023_JCE_priority_rules_paper"].event_id],
            description=(
                "Smith chose his own 2023 JCE paper on priority and selectivity "
                "rules as the source material for NotebookLM. Rationale stated "
                "in body text: open access, copyright-free, owned by the author."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[by_target["notebooklm_session:initial"].event_id],
            description=(
                "Initial prompt provided to NotebookLM (body text quotation). "
                "Differs from SI V1 prompt; relationship between this initial "
                "podcast and SI V1 is ambiguous in the publication."
            ),
            confidence=EvidenceConfidence.MEDIUM,
        ),
        Evidence(
            event_ids=[
                by_target["notebooklm_session:V1"].event_id,
                by_target["podcast_audio:V1"].event_id,
            ],
            description="SI Podcast Version 1: user prompt + full AI-generated transcript.",
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[
                by_target["notebooklm_session:V2"].event_id,
                by_target["podcast_audio:V2"].event_id,
            ],
            description=(
                "SI Podcast Version 2: no user prompt (NotebookLM auto-generated "
                "from the revised source) + full AI-generated transcript."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[
                by_target["notebooklm_session:V3"].event_id,
                by_target["podcast_audio:V3"].event_id,
            ],
            description="SI Podcast Version 3: user prompt + full AI-generated transcript.",
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[by_target["source_document:Smith_2023_JCE_priority_rules_paper"].event_id],
            description=(
                "Source document was revised between V1 and V2: lidocaine example "
                "removed in favor of salbutamol; classic-reaction-types section "
                "removed. Documented in body text."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[by_target["podcast_audio:final"].event_id],
            description=(
                "Final curation in Audacity: best analogies, liveliest discussions, "
                "errors removed. Body text documents the rationale (3-version "
                "selection) without listing per-segment selections."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[by_target["podcast_audio:final.transcript"].event_id],
            description=(
                "Transcription performed via Panopto rather than NotebookLM, "
                "with reason given (greater accuracy)."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[by_target["visual:salbutamol_synthesis.pptx"].event_id],
            description="Human-authored PowerPoint visual attached; no AI involvement in the visual itself.",
            confidence=EvidenceConfidence.HIGH,
        ),
        # Error-disposition evidence (paper body text, not events directly).
        Evidence(
            event_ids=[by_target["podcast_audio:V1"].event_id],
            description=(
                "Epoxide error: 'when describing the salbutamol mechanism, the AI "
                "wrongly suggested an epoxide was present. This was edited out of "
                "the final podcast.' Body text §Limitations / Generation."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[by_target["podcast_audio:V1"].event_id],
            description=(
                "Chlorine vs chloride error: 'a chloride ion is the leaving group, "
                "but the AI referred to chlorine leaving. ... left in the final "
                "podcast; closed captioning was used to clear-up misunderstanding.'"
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[by_target["podcast_audio:V1"].event_id],
            description=(
                "HOMO/LUMO error: 'the AI said: the lowest unoccupied molecular "
                "orbital — the HOMO.' Kept in; captioned with corrected information."
            ),
            confidence=EvidenceConfidence.HIGH,
        ),
        Evidence(
            event_ids=[by_target["podcast_audio:final"].event_id],
            description=(
                "Workload measurement: 'about 3 h of academic work' total; "
                "audio editing ~2 h; caption editing ~20-30 min; source adaptation ~60 min."
            ),
            confidence=EvidenceConfidence.MEDIUM,
        ),
    ]


# ---------------------------------------------------------------------------
# Decisions
# ---------------------------------------------------------------------------


def build_decisions(evidence: list[Evidence]) -> list[Decision]:
    """All decisions are unclassified+novel_pattern under v0.1 vocabulary.

    Each is paired with a SchemaDelta proposing a vocabulary term.
    """
    # Map description fragments to evidence IDs for clarity.
    ev = {e.description[:40]: e.evidence_id for e in evidence}

    def find(prefix: str) -> str:
        for k, v in ev.items():
            if k.startswith(prefix):
                return v
        raise KeyError(prefix)

    decisions: list[Decision] = []

    # D1: tool selection — NotebookLM over alternatives.
    decisions.append(
        Decision(
            timestamp=T_INITIAL,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Tool selection: chose Google NotebookLM over ChatGPT, Microsoft "
                "Copilot, Google Gemini and other chatbots. Rationale per paper: "
                "'The use of defined sources reduces the risk of hallucinatory "
                "outputs, increasing reliability.'"
            ),
            actor=SMITH,
            evidence_ids=[find("Smith chose his own 2023 JCE paper")],
            verification_status=VerificationStatus.NOT_APPLICABLE,
            verification_notes=(
                "Selection decision; no AI output to verify. Verification N/A."
            ),
        )
    )

    # D2: source material selection.
    decisions.append(
        Decision(
            timestamp=T_INITIAL,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Source material selection: Smith's own 2023 JCE paper used as "
                "input to NotebookLM. Rationale: open access, copyright-free, "
                "owned by the author."
            ),
            actor=SMITH,
            evidence_ids=[find("Smith chose his own 2023 JCE paper")],
            verification_status=VerificationStatus.NOT_APPLICABLE,
            verification_notes="Author selecting own prior work as input.",
        )
    )

    # D3: prompt design (initial + V1 + V3).
    # publish_level=verbatim: Smith voluntarily disclosed the prompts in the
    # SI; the prompts themselves are the deliverable he wanted reviewers and
    # readers to inspect, not adapter-extracted ambient chatter.
    decisions.append(
        Decision(
            timestamp=T_V1,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Prompt engineering: initial prompt focused on 'importance of "
                "organic reaction mechanisms' and 'priority and selectivity rules'; "
                "V1 reformulated to 'Explain why having rules is important... "
                "describe all of the rules... discuss how to apply them.'; V3 "
                "explicitly reframed for a student audience."
            ),
            actor=SMITH,
            evidence_ids=[find("SI Podcast Version 1"), find("SI Podcast Version 3")],
            verification_status=VerificationStatus.NOT_APPLICABLE,
            publish_level="verbatim",
        )
    )

    # D4: source revision after V1 review.
    decisions.append(
        Decision(
            timestamp=T_REVISION,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Source revision: lidocaine example removed from source document "
                "in favor of salbutamol synthesis after V1 review revealed that "
                "lidocaine required Level 2 selectivity rules before they had "
                "been introduced, causing pedagogic confusion in the AI output. "
                "This decision changed the inputs to V2 and V3."
            ),
            actor=SMITH,
            evidence_ids=[find("Source document was revised")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Verified by Smith's domain knowledge: original source positioning "
                "of lidocaine was acknowledged as suboptimal in own writing. "
                "Verification mode: author's domain expertise as organic chemist."
            ),
        )
    )

    # D5: iterative generation (decision to run 3 versions).
    # publish_level=verbatim: the three AI outputs were the deliverable Smith
    # explicitly compared in the SI.
    decisions.append(
        Decision(
            timestamp=T_V2,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Iterative generation: decision to produce three podcast versions "
                "from the revised source rather than accepting a single output. "
                "Justification: 'beyond using different podcast versions to "
                "correct errors, in each case the AI discussed different examples. "
                "Some of these were pedagogically clearer, and some were better "
                "explained. Having a choice of audio streams was beneficial.'"
            ),
            actor=SMITH,
            evidence_ids=[
                find("SI Podcast Version 1"),
                find("SI Podcast Version 2"),
                find("SI Podcast Version 3"),
            ],
            verification_status=VerificationStatus.NOT_APPLICABLE,
            publish_level="verbatim",
        )
    )

    # D6-D8: error disposition (epoxide; chlorine; HOMO).
    decisions.append(
        Decision(
            timestamp=T_CURATION,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Error disposition (epoxide): AI suggested an epoxide intermediate "
                "in the salbutamol mechanism. No epoxide present in the reaction "
                "shown (Figure 2). Decision: EDIT OUT of final podcast. "
                "Smith hypothesizes the AI either pulled the intermediate from "
                "training data on the standard salbutamol synthesis, or confused "
                "an unrelated mention in the source document."
            ),
            actor=SMITH,
            evidence_ids=[find("Epoxide error")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Verified by Smith's domain knowledge as organic chemist; "
                "reviewer/editor of own field. No independent third-party check."
            ),
        )
    )

    decisions.append(
        Decision(
            timestamp=T_CURATION,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Error disposition (chlorine/chloride): AI referred to 'chlorine' "
                "as the leaving group when the correct species is the chloride ion. "
                "Decision: KEEP with closed captioning to correct the terminology. "
                "Rationale: error is a known AI pattern (citing one literature "
                "study showing Copilot makes the same mistake)."
            ),
            actor=SMITH,
            evidence_ids=[find("Chlorine vs chloride error")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes="Same verification mode as epoxide error.",
        )
    )

    decisions.append(
        Decision(
            timestamp=T_CURATION,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Error disposition (HOMO/LUMO): AI said 'the lowest unoccupied "
                "molecular orbital — the HOMO'. HOMO is highest occupied; LUMO is "
                "lowest unoccupied. Decision: KEEP with captioned correction. "
                "Rationale: surrounding orbital description was excellent in that "
                "take; not editable without re-running."
            ),
            actor=SMITH,
            evidence_ids=[find("HOMO/LUMO error")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes="Same verification mode as other technical errors.",
        )
    )

    # D9: content curation from multiple AI outputs.
    # publish_level=verbatim: the curation outcome is the final podcast and
    # the SI highlights show which segments were retained; preserving the
    # underlying Event content is what makes that traceable downstream.
    decisions.append(
        Decision(
            timestamp=T_CURATION,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Content curation from multiple AI outputs: combined three podcast "
                "audio streams using Audacity, selecting 'best analogies and "
                "liveliest discussions, removing errors or confusing descriptions.' "
                "Per-segment selection rationale not documented in publication."
            ),
            actor=SMITH,
            evidence_ids=[find("Final curation in Audacity")],
            verification_status=VerificationStatus.VERIFIED_PARTIALLY,
            verification_notes=(
                "Curation outcome partially verifiable via SI yellow highlighting "
                "showing which segments were retained, but the rationale for each "
                "selection is not recorded — only aggregate rationale."
            ),
            publish_level="verbatim",
        )
    )

    # D10: transcription tool selection (Panopto over NotebookLM).
    decisions.append(
        Decision(
            timestamp=T_TRANSCRIPTION,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Transcription tool selection: Panopto (with minor manual editing) "
                "chosen over NotebookLM's own transcription. Rationale: 'Google "
                "NotebookLM is not very good at creating a transcript from audio "
                "input (Panopto generates much more accurate transcripts).'"
            ),
            actor=SMITH,
            evidence_ids=[find("Transcription performed via Panopto")],
            verification_status=VerificationStatus.VERIFIED_INDEPENDENTLY,
            verification_notes=(
                "Smith independently verified by comparing outputs; comparison "
                "data not published. Claim grounded in author's direct experience."
            ),
        )
    )

    # D11: visual addition (PowerPoint).
    decisions.append(
        Decision(
            timestamp=T_VISUAL,
            decision_type="unclassified",
            schema_gap="novel_pattern",
            description=(
                "Supplementary visual addition: PowerPoint image of salbutamol "
                "synthesis (Figure 2 of the paper) created and attached to the "
                "audio file. Image is human-authored; no AI involvement. Decision "
                "is to address NotebookLM's audio-only limitation."
            ),
            actor=SMITH,
            evidence_ids=[find("Human-authored PowerPoint visual")],
            verification_status=VerificationStatus.NOT_APPLICABLE,
        )
    )

    return decisions


# ---------------------------------------------------------------------------
# Claims
# ---------------------------------------------------------------------------


def build_claims(decisions: list[Decision]) -> list[Claim]:
    # Build a description->id map.
    d = {dec.description[:40]: dec.decision_id for dec in decisions}

    def D(prefix: str) -> str:
        for k, v in d.items():
            if k.startswith(prefix):
                return v
        raise KeyError(prefix)

    return [
        Claim(
            text=(
                "Google NotebookLM can make engaging scientific podcasts with "
                "limited workload."
            ),
            location="Abstract; Conclusions",
            upstream_decision_ids=[
                D("Tool selection"),
                D("Source material selection"),
                D("Prompt engineering"),
                D("Iterative generation"),
                D("Content curation"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        Claim(
            text=(
                "All three podcast outputs were combined with academic curation "
                "to create a final output with minimal errors."
            ),
            location="Abstract",
            upstream_decision_ids=[
                D("Iterative generation"),
                D("Error disposition (epoxide)"),
                D("Error disposition (chlorine/chloride)"),
                D("Error disposition (HOMO/LUMO)"),
                D("Content curation"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
        Claim(
            text=(
                "Students who listened to the podcast reported it helped reinforce "
                "learning and was worth listening to."
            ),
            location="Abstract; Application of Podcast as Student Support",
            upstream_decision_ids=[D("Content curation")],
            evidence_confidence=EvidenceConfidence.MEDIUM,
        ),
        Claim(
            text="For about 3 h of academic work, a podcast was produced.",
            location="Workload Implications",
            upstream_decision_ids=[
                D("Source revision"),
                D("Iterative generation"),
                D("Content curation"),
                D("Transcription tool selection"),
            ],
            evidence_confidence=EvidenceConfidence.MEDIUM,
        ),
        Claim(
            text=(
                "The AI did very well with background and summary material, "
                "struggling more with technically or pedagogically challenging "
                "material."
            ),
            location="Conclusions",
            upstream_decision_ids=[
                D("Error disposition (epoxide)"),
                D("Error disposition (chlorine/chloride)"),
                D("Error disposition (HOMO/LUMO)"),
                D("Source revision"),
            ],
            evidence_confidence=EvidenceConfidence.HIGH,
        ),
    ]


# ---------------------------------------------------------------------------
# Schema deltas — vocabulary candidates surfaced by this audit
# ---------------------------------------------------------------------------


def build_schema_deltas(
    audit_id: str, evidence: list[Evidence]
) -> list[SchemaDelta]:
    ev_ids = [e.evidence_id for e in evidence]

    proposals = [
        (
            "tool_selection_via_ai",
            "Decision to use a specific AI tool over alternatives, with rationale.",
        ),
        (
            "source_material_selection",
            "Decision about which document(s) to provide as input to an AI tool.",
        ),
        (
            "source_material_revision",
            (
                "Modification of input materials to an AI tool after reviewing "
                "initial outputs, intended to change subsequent AI behavior."
            ),
        ),
        (
            "prompt_engineering",
            (
                "Formulation or reformulation of user prompts to an AI tool, "
                "including audience-targeted reframing and prompt-free runs."
            ),
        ),
        (
            "iterative_ai_generation",
            (
                "Running the same or similar prompts multiple times to obtain "
                "variation in AI output for downstream selection."
            ),
        ),
        (
            "ai_error_disposition",
            (
                "Decision about how to handle a specific identified error in AI "
                "output: edit out, keep with correction, keep as-is. Sub-types "
                "anticipated: edit_out, keep_with_caption, keep_as_is."
            ),
        ),
        (
            "content_curation_from_multiple_ai_outputs",
            (
                "Selection and combination of segments from multiple AI outputs "
                "into a single deliverable."
            ),
        ),
        (
            "ai_assisted_transcription",
            (
                "Use of an AI or auto-captioning system for transcription, "
                "possibly distinct from the AI used for content generation."
            ),
        ),
        (
            "human_authored_supplementary_visual",
            (
                "Addition of human-authored visual or supporting material to "
                "compensate for AI-tool limitations."
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
        audit_target="doi:10.1021/acs.jchemed.5c01652",
        vocabulary_version="0.1.0",
        capture_tier_achieved=CaptureTier.TIER_3,
        audit_timestamp=AUDIT_TS,
        adapters_used=[
            AdapterUsage(
                adapter_name="manual_log_adapter",
                adapter_version="0.0.0-pre-implementation",
                capture_tier=CaptureTier.TIER_3,
            )
        ],
        events=events,
        evidence=evidence,
        decisions=decisions,
        claims=claims,
        notes=(
            "Manual retrospective audit. No adapter implementations yet — "
            "evidence extracted by hand from the paper body and SI. Capture tier "
            "reaches 3 because Smith's voluntary disclosure includes full prompts, "
            "full AI outputs, source-document provenance, workload measurements, "
            "and explicit error-disposition rationales. The v0.1 vocabulary is "
            "empty by design; every decision is `unclassified` with a "
            "`schema_gap='novel_pattern'` marker and a corresponding SchemaDelta."
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

    out_dir = Path(
        os.environ.get(
            "AIVS_OUT_DIR",
            str(Path(__file__).resolve().parent / "out"),
        )
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    internal_path = out_dir / "smith_2026_audit.json"
    published_path = out_dir / "smith_2026_audit_published.json"

    internal_json = audit.model_dump_json(indent=2)
    internal_path.write_text(internal_json)

    # to_published() strips Event.content for all events NOT in a
    # verbatim-marked Decision's evidence chain. Smith marks D3, D5, D9
    # as verbatim; their evidence keeps verbatim content. Everything
    # else carries content_hash only.
    published = audit.to_published()
    published_json = published.model_dump_json(indent=2)
    published_path.write_text(published_json)

    # Console summary.
    counts = {
        "events": len(audit.events),
        "evidence": len(audit.evidence),
        "decisions": len(audit.decisions),
        "claims": len(audit.claims),
        "schema_deltas": len(audit.schema_deltas),
    }
    verbatim_count = sum(1 for d in audit.decisions if d.publish_level == "verbatim")
    print("=== AIVS retrospective audit ===")
    print(f"  target              : {audit.audit_target}")
    print(f"  audit_id            : {audit.audit_id}")
    print(f"  meta_schema_version : {audit.meta_schema_version}")
    print(f"  vocabulary_version  : {audit.vocabulary_version}")
    print(f"  capture_tier        : {audit.capture_tier_achieved.value}")
    print(f"  integrity           : OK")
    print(f"  counts              : {json.dumps(counts)}")
    print(f"  verbatim decisions  : {verbatim_count} / {len(audit.decisions)}")
    print(f"  internal artifact   : {internal_path} ({len(internal_json):,} bytes)")
    print(f"  published artifact  : {published_path} ({len(published_json):,} bytes)")
    print()
    print("Schema-delta proposals (candidate v0.2 vocabulary terms):")
    for sd in audit.schema_deltas:
        print(f"  - {sd.proposed_term}")


if __name__ == "__main__":
    main()
