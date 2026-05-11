"""
End-to-end demo: build a synthetic AuditArtifact and serialize it.

This is illustrative only. It uses a single fabricated decision with
schema_gap='novel_pattern' and a corresponding SchemaDelta proposal,
because the v0.1 vocabulary is intentionally empty. Real audits will
emit a mix of classified decisions and (where appropriate) novel-pattern
decisions paired with deltas.

Run:
    python -m examples.minimal_audit
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

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


def build_demo_audit() -> AuditArtifact:
    t = datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc)

    # An AI session event: a Claude Code prompt requesting a force-field choice.
    e_prompt = Event(
        timestamp=t,
        actor=Actor(
            actor_type=ActorType.HUMAN,
            identifier="researcher-1",
        ),
        action="prompt",
        target="claude-code-session://chat/42",
        content="Which force field should I use for an apo kinase in explicit water?",
        source_ref=SourceRef(
            adapter_name="claude_code",
            adapter_version="0.0.0",
            raw_location="~/.claude/projects/proj/sessions/42.jsonl#L120",
            extracted_at=t,
        ),
        tier=CaptureTier.TIER_2,
    )

    # The AI response, captured as a generative event.
    e_response = Event(
        timestamp=t,
        actor=Actor(
            actor_type=ActorType.AI_GENERATIVE,
            identifier="claude-3-5-sonnet",
        ),
        action="generate",
        target="claude-code-session://chat/42",
        content="Recommend AMBER ff14SB with TIP3P water for kinases at neutral pH.",
        source_ref=SourceRef(
            adapter_name="claude_code",
            adapter_version="0.0.0",
            raw_location="~/.claude/projects/proj/sessions/42.jsonl#L121",
            extracted_at=t,
        ),
        tier=CaptureTier.TIER_2,
    )

    # A git commit applying the force-field choice to the simulation config.
    e_commit = Event(
        timestamp=t,
        actor=Actor(
            actor_type=ActorType.HUMAN,
            identifier="researcher-1",
        ),
        action="edit",
        target="config/md_run.yaml",
        content="forcefield: amber/ff14SB\nwater_model: tip3p",
        source_ref=SourceRef(
            adapter_name="git",
            adapter_version="0.0.0",
            raw_location="commit:abc123",
            extracted_at=t,
        ),
        tier=CaptureTier.TIER_2,
    )

    evidence = Evidence(
        event_ids=[e_prompt.event_id, e_response.event_id, e_commit.event_id],
        description=(
            "Force-field selection: AI-advisory (model recommended ff14SB/TIP3P; "
            "human committed the change in commit abc123)."
        ),
        confidence=EvidenceConfidence.HIGH,
    )

    # The vocabulary is empty in v0.1, so this decision is necessarily
    # 'unclassified' with a schema gap. A real audit would also emit the
    # SchemaDelta below proposing 'force_field_selection' as a vocabulary term.
    decision = Decision(
        timestamp=t,
        decision_type="unclassified",
        description="Selected AMBER ff14SB / TIP3P for production MD on apo kinase.",
        actor=Actor(
            actor_type=ActorType.AI_ADVISORY,
            identifier="claude-3-5-sonnet",
        ),
        evidence_ids=[evidence.evidence_id],
        schema_gap="novel_pattern",
        verification_status=VerificationStatus.UNVERIFIED,
        verification_notes=(
            "No independent benchmark of ff14SB/TIP3P performance on this "
            "specific kinase reported in the manuscript."
        ),
    )

    claim = Claim(
        text="The protein backbone remained stable across the 1-microsecond trajectory.",
        location="Results §2.1",
        upstream_decision_ids=[decision.decision_id],
        evidence_confidence=EvidenceConfidence.MEDIUM,
    )

    audit = AuditArtifact(
        audit_target="doi:10.0000/example.kinase.md.2026",
        vocabulary_version="0.1.0",
        capture_tier_achieved=CaptureTier.TIER_2,
        audit_timestamp=t,
        adapters_used=[
            AdapterUsage(
                adapter_name="claude_code",
                adapter_version="0.0.0",
                capture_tier=CaptureTier.TIER_2,
            ),
            AdapterUsage(
                adapter_name="git",
                adapter_version="0.0.0",
                capture_tier=CaptureTier.TIER_1,
            ),
        ],
        events=[e_prompt, e_response, e_commit],
        evidence=[evidence],
        decisions=[decision],
        claims=[claim],
        notes="Demo audit. Single decision; vocabulary v0.1 is empty by design.",
    )

    # The accompanying schema-delta proposal.
    delta = SchemaDelta(
        proposed_term="force_field_selection",
        proposed_kind=SchemaDeltaKind.DECISION_TYPE,
        justification=(
            "Recurring methodological choice in MD workflows (force field, "
            "water model, ion parameters)."
        ),
        source_audit_id=audit.audit_id,
        raw_evidence_ids=[evidence.evidence_id],
        proposed_at=t,
    )
    audit.schema_deltas.append(delta)

    return audit


def main() -> None:
    audit = build_demo_audit()
    errors = audit.validate_integrity()
    if errors:
        print("INTEGRITY ERRORS:")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)

    print("=== AuditArtifact (JSON, abbreviated) ===")
    payload = json.loads(audit.model_dump_json())
    # Show top-level structure plus counts to keep stdout readable.
    summary = {
        "audit_id": payload["audit_id"],
        "audit_target": payload["audit_target"],
        "meta_schema_version": payload["meta_schema_version"],
        "vocabulary_version": payload["vocabulary_version"],
        "capture_tier_achieved": payload["capture_tier_achieved"],
        "counts": {
            "events": len(payload["events"]),
            "evidence": len(payload["evidence"]),
            "decisions": len(payload["decisions"]),
            "claims": len(payload["claims"]),
            "schema_deltas": len(payload["schema_deltas"]),
        },
        "first_decision": payload["decisions"][0],
        "first_schema_delta": payload["schema_deltas"][0],
    }
    print(json.dumps(summary, indent=2, default=str))
    print()
    print("Integrity: OK")


if __name__ == "__main__":
    main()
