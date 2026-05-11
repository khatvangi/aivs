"""Tests for the AIVS meta-schema."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from aivs.meta_schema import (
    META_SCHEMA_VERSION,
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
    SchemaDeltaStatus,
    SourceRef,
    VerificationStatus,
)


# --- helpers -----------------------------------------------------------------


def _now() -> datetime:
    return datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc)


def _event(action: str = "edit", actor_type: ActorType = ActorType.HUMAN) -> Event:
    return Event(
        timestamp=_now(),
        actor=Actor(actor_type=actor_type),
        action=action,
        target="src/foo.py",
        content="some content",
        source_ref=SourceRef(
            adapter_name="test",
            adapter_version="0.0.0",
            raw_location="src/foo.py:1",
            extracted_at=_now(),
        ),
        tier=CaptureTier.TIER_2,
    )


def _minimal_audit(audit_id: str | None = None) -> AuditArtifact:
    audit_kwargs = dict(
        audit_target="doi:10.0000/example",
        vocabulary_version="0.1.0",
        capture_tier_achieved=CaptureTier.TIER_2,
        audit_timestamp=_now(),
        adapters_used=[
            AdapterUsage(
                adapter_name="test",
                adapter_version="0.0.0",
                capture_tier=CaptureTier.TIER_2,
            )
        ],
    )
    if audit_id is not None:
        audit_kwargs["audit_id"] = audit_id
    return AuditArtifact(**audit_kwargs)


# --- round-trip serialization -----------------------------------------------


class TestRoundTrip:

    def test_event_round_trip(self) -> None:
        e = _event()
        e2 = Event.model_validate_json(e.model_dump_json())
        assert e == e2

    def test_audit_artifact_round_trip(self) -> None:
        audit = _minimal_audit()
        audit2 = AuditArtifact.model_validate_json(audit.model_dump_json())
        assert audit == audit2

    def test_full_audit_round_trip(self) -> None:
        audit = _minimal_audit()
        ev = _event(action="run", actor_type=ActorType.AI_AUTONOMOUS)
        evid = Evidence(
            event_ids=[ev.event_id],
            description="MD run executed via slurm",
            confidence=EvidenceConfidence.HIGH,
        )
        dec = Decision(
            timestamp=_now(),
            decision_type="unclassified",
            description="chose force field for production MD",
            actor=Actor(actor_type=ActorType.HUMAN),
            evidence_ids=[evid.evidence_id],
            schema_gap="novel_pattern",
            verification_status=VerificationStatus.UNVERIFIED,
        )
        cl = Claim(
            text="The protein remained stable over 1 us.",
            location="Results §2.1",
            upstream_decision_ids=[dec.decision_id],
        )
        sd = SchemaDelta(
            proposed_term="force_field_selection",
            proposed_kind=SchemaDeltaKind.DECISION_TYPE,
            justification="Recurring choice point in MD workflows.",
            source_audit_id=audit.audit_id,
            raw_evidence_ids=[evid.evidence_id],
            proposed_at=_now(),
        )
        audit.events.append(ev)
        audit.evidence.append(evid)
        audit.decisions.append(dec)
        audit.claims.append(cl)
        audit.schema_deltas.append(sd)

        audit2 = AuditArtifact.model_validate_json(audit.model_dump_json())
        assert audit == audit2


# --- integrity validation ----------------------------------------------------


class TestIntegrity:

    def test_minimal_audit_is_valid(self) -> None:
        audit = _minimal_audit()
        assert audit.validate_integrity() == []

    def test_evidence_referencing_missing_event(self) -> None:
        audit = _minimal_audit()
        audit.evidence.append(
            Evidence(event_ids=["nonexistent-event"], description="dangling")
        )
        errors = audit.validate_integrity()
        assert any("missing event nonexistent-event" in e for e in errors)

    def test_decision_referencing_missing_evidence(self) -> None:
        audit = _minimal_audit()
        audit.decisions.append(
            Decision(
                timestamp=_now(),
                decision_type="unclassified",
                description="orphan decision",
                actor=Actor(actor_type=ActorType.HUMAN),
                evidence_ids=["nonexistent-evidence"],
                schema_gap="novel_pattern",
            )
        )
        errors = audit.validate_integrity()
        assert any("missing evidence nonexistent-evidence" in e for e in errors)

    def test_claim_referencing_missing_decision(self) -> None:
        audit = _minimal_audit()
        audit.claims.append(
            Claim(
                text="bare claim",
                location="§1",
                upstream_decision_ids=["nonexistent-decision"],
            )
        )
        errors = audit.validate_integrity()
        assert any("missing decision nonexistent-decision" in e for e in errors)

    def test_schema_delta_audit_id_must_match(self) -> None:
        audit = _minimal_audit(audit_id="audit-A")
        ev = _event()
        evid = Evidence(event_ids=[ev.event_id], description="ev")
        audit.events.append(ev)
        audit.evidence.append(evid)
        audit.schema_deltas.append(
            SchemaDelta(
                proposed_term="x",
                proposed_kind=SchemaDeltaKind.DECISION_TYPE,
                justification="...",
                source_audit_id="audit-B",  # wrong
                raw_evidence_ids=[evid.evidence_id],
                proposed_at=_now(),
            )
        )
        errors = audit.validate_integrity()
        assert any("audit-B" in e and "audit-A" in e for e in errors)


# --- meta-schema invariants --------------------------------------------------


class TestInvariants:

    def test_unclassified_requires_schema_gap(self) -> None:
        with pytest.raises(ValidationError):
            Decision(
                timestamp=_now(),
                decision_type="unclassified",
                description="x",
                actor=Actor(actor_type=ActorType.HUMAN),
                evidence_ids=[],
                # missing schema_gap
            )

    def test_schema_gap_requires_unclassified(self) -> None:
        with pytest.raises(ValidationError):
            Decision(
                timestamp=_now(),
                decision_type="some_real_type",
                description="x",
                actor=Actor(actor_type=ActorType.HUMAN),
                evidence_ids=[],
                schema_gap="novel_pattern",  # not allowed unless unclassified
            )

    def test_classified_decision_without_gap_is_valid(self) -> None:
        d = Decision(
            timestamp=_now(),
            decision_type="some_known_type",
            description="x",
            actor=Actor(actor_type=ActorType.HUMAN),
            evidence_ids=[],
        )
        assert d.schema_gap is None

    def test_merged_into_requires_target(self) -> None:
        with pytest.raises(ValidationError):
            SchemaDelta(
                proposed_term="x",
                proposed_kind=SchemaDeltaKind.DECISION_TYPE,
                justification="...",
                source_audit_id="a",
                raw_evidence_ids=[],
                proposed_at=_now(),
                status=SchemaDeltaStatus.MERGED_INTO,
                # missing merged_into
            )

    def test_merged_into_target_only_when_merged(self) -> None:
        with pytest.raises(ValidationError):
            SchemaDelta(
                proposed_term="x",
                proposed_kind=SchemaDeltaKind.DECISION_TYPE,
                justification="...",
                source_audit_id="a",
                raw_evidence_ids=[],
                proposed_at=_now(),
                status=SchemaDeltaStatus.PROPOSED,
                merged_into="some_other_term",  # not allowed
            )

    def test_meta_schema_version_constant(self) -> None:
        # Sanity: artifacts default to the current version.
        audit = _minimal_audit()
        assert audit.meta_schema_version == META_SCHEMA_VERSION


# --- v0.2 privacy posture ----------------------------------------------------


class TestPrivacyPosture:
    """Tests for v0.2 changes: content/content_hash duality, Decision
    publish_level, and AuditArtifact.to_published()."""

    def test_event_content_hash_autocomputed(self) -> None:
        import hashlib
        e = _event(action="prompt")
        expected = hashlib.sha256(b"some content").hexdigest()
        assert e.content == "some content"
        assert e.content_hash == expected

    def test_event_redacted_form(self) -> None:
        """An Event with content=None and a pre-set content_hash is a
        valid redact-mode event."""
        e = Event(
            timestamp=_now(),
            actor=Actor(actor_type=ActorType.HUMAN),
            action="prompt",
            target="src/foo.py",
            content=None,
            content_hash="abc123",
            source_ref=SourceRef(
                adapter_name="test",
                adapter_version="0.0.0",
                raw_location="x:1",
                extracted_at=_now(),
            ),
            tier=CaptureTier.TIER_2,
        )
        assert e.content is None
        assert e.content_hash == "abc123"

    def test_event_empty_form_allowed(self) -> None:
        """Pure structural Events with neither content nor hash are
        permitted (per directive: 'invariant not enforced for events
        where neither makes sense')."""
        e = Event(
            timestamp=_now(),
            actor=Actor(actor_type=ActorType.HUMAN),
            action="hook",
            target="hook:Stop",
            source_ref=SourceRef(
                adapter_name="test",
                adapter_version="0.0.0",
                raw_location="x:1",
                extracted_at=_now(),
            ),
            tier=CaptureTier.TIER_2,
        )
        assert e.content is None
        assert e.content_hash is None

    def test_decision_publish_level_default_is_summary(self) -> None:
        d = Decision(
            timestamp=_now(),
            decision_type="some_real_type",
            description="x",
            actor=Actor(actor_type=ActorType.HUMAN),
            evidence_ids=[],
        )
        assert d.publish_level == "summary"

    def test_audit_to_published_strips_summary_keeps_verbatim(self) -> None:
        """to_published() should strip content from summary-decision
        events and preserve content on verbatim-decision events."""
        audit = _minimal_audit()

        # Two events with content.
        e_summary = _event(action="prompt")
        e_summary_content = e_summary.content  # snapshot before to_published
        e_verbatim = _event(action="respond", actor_type=ActorType.AI_GENERATIVE)
        e_verbatim_content = e_verbatim.content

        ev_summary = Evidence(
            event_ids=[e_summary.event_id],
            description="summary-bucket evidence",
        )
        ev_verbatim = Evidence(
            event_ids=[e_verbatim.event_id],
            description="verbatim-bucket evidence",
        )

        d_summary = Decision(
            timestamp=_now(),
            decision_type="some_real_type",
            description="summary decision",
            actor=Actor(actor_type=ActorType.HUMAN),
            evidence_ids=[ev_summary.evidence_id],
        )
        d_verbatim = Decision(
            timestamp=_now(),
            decision_type="another_real_type",
            description="verbatim decision",
            actor=Actor(actor_type=ActorType.HUMAN),
            evidence_ids=[ev_verbatim.evidence_id],
            publish_level="verbatim",
        )

        audit.events = [e_summary, e_verbatim]
        audit.evidence = [ev_summary, ev_verbatim]
        audit.decisions = [d_summary, d_verbatim]

        published = audit.to_published()

        pub_summary = next(e for e in published.events if e.event_id == e_summary.event_id)
        pub_verbatim = next(e for e in published.events if e.event_id == e_verbatim.event_id)

        assert pub_summary.content is None
        assert pub_summary.content_hash is not None  # hash preserved
        assert pub_verbatim.content == e_verbatim_content
        assert pub_verbatim.content_hash is not None

        # Original audit should be untouched.
        orig_summary = next(e for e in audit.events if e.event_id == e_summary.event_id)
        assert orig_summary.content == e_summary_content

    def test_audit_to_published_preserves_author_fields(self) -> None:
        """to_published() must never touch author-written fields:
        Decision.description, Evidence.description, Claim.text, notes."""
        audit = _minimal_audit()
        audit.notes = "audit-level note"

        ev = _event()
        evid = Evidence(event_ids=[ev.event_id], description="ev description")
        dec = Decision(
            timestamp=_now(),
            decision_type="some_type",
            description="decision description",
            actor=Actor(actor_type=ActorType.HUMAN),
            evidence_ids=[evid.evidence_id],
        )
        claim = Claim(
            text="claim text",
            location="§1",
            upstream_decision_ids=[dec.decision_id],
        )
        audit.events = [ev]
        audit.evidence = [evid]
        audit.decisions = [dec]
        audit.claims = [claim]

        published = audit.to_published()

        assert published.notes == "audit-level note"
        assert published.evidence[0].description == "ev description"
        assert published.decisions[0].description == "decision description"
        assert published.claims[0].text == "claim text"

    def test_audit_to_published_no_verbatim_strips_everything(self) -> None:
        """When no Decision is verbatim, every Event's content is
        stripped (matches triplet-proof real-data behaviour)."""
        audit = _minimal_audit()
        e1 = _event(action="prompt")
        e2 = _event(action="run")
        ev = Evidence(event_ids=[e1.event_id, e2.event_id], description="bucket")
        d = Decision(
            timestamp=_now(),
            decision_type="some_type",
            description="d",
            actor=Actor(actor_type=ActorType.HUMAN),
            evidence_ids=[ev.evidence_id],
        )
        audit.events = [e1, e2]
        audit.evidence = [ev]
        audit.decisions = [d]

        published = audit.to_published()
        assert all(e.content is None for e in published.events)
        assert all(e.content_hash is not None for e in published.events)

    def test_meta_schema_version_is_0_2_0(self) -> None:
        assert META_SCHEMA_VERSION == "0.2.0"


# --- adapter interface -------------------------------------------------------


class TestAdapterInterface:

    def test_adapter_is_abstract(self) -> None:
        from aivs.adapters import EvidenceAdapter

        with pytest.raises(TypeError):
            EvidenceAdapter()  # type: ignore[abstract]
