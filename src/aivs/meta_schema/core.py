"""
AIVS meta-schema — core entity types.

The meta-schema is small, stable, and versioned. The open vocabulary
(`decision_type`, `action`, evidence relations) lives in `aivs.vocabulary`
and is allowed to grow audit-by-audit; the entity types and relationships
defined here are not.

Bumping META_SCHEMA_VERSION requires a migration plan for existing audits.
Adding terms to the open vocabulary does not.
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, model_validator


META_SCHEMA_VERSION = "0.2.0"


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Closed enumerations (part of the meta-schema; cannot be extended by audits)
# ---------------------------------------------------------------------------


class ActorType(str, Enum):
    """Source-agnostic taxonomy of who or what performed an action."""

    HUMAN = "human"
    AI_ADVISORY = "ai_advisory"          # AI suggested; human committed
    AI_GENERATIVE = "ai_generative"      # AI produced content directly used
    AI_AUTONOMOUS = "ai_autonomous"      # AI executed without per-step review
    SYSTEM = "system"                    # automated tooling, non-AI
    UNKNOWN = "unknown"                  # involvement detected, kind unclear


class CaptureTier(int, Enum):
    """Evidence fidelity gradient. Audits report the tier they achieved."""

    TIER_0 = 0   # manual log only
    TIER_1 = 1   # VCS + notebooks; no AI logs
    TIER_2 = 2   # + AI session logs
    TIER_3 = 3   # + env / reproducibility metadata


class VerificationStatus(str, Enum):
    """Whether a decision's downstream effect was independently verified."""

    VERIFIED_INDEPENDENTLY = "verified_independently"
    VERIFIED_PARTIALLY = "verified_partially"
    UNVERIFIED = "unverified"
    NOT_APPLICABLE = "not_applicable"
    NO_EVIDENCE = "no_evidence"


class EvidenceConfidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class SchemaDeltaKind(str, Enum):
    DECISION_TYPE = "decision_type"
    ACTOR_SUBTYPE = "actor_subtype"
    EVIDENCE_RELATION = "evidence_relation"
    ACTION_TYPE = "action_type"


class SchemaDeltaStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    MERGED_INTO = "merged_into"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"


# ---------------------------------------------------------------------------
# Core entities
# ---------------------------------------------------------------------------


def _new_id() -> str:
    return str(uuid.uuid4())


class SourceRef(BaseModel):
    """Provenance for a piece of evidence: which adapter saw it, where, when."""

    adapter_name: str
    adapter_version: str
    raw_location: str           # path, URL, or adapter-internal identifier
    extracted_at: datetime


class Actor(BaseModel):
    """Who or what performed an action."""

    actor_type: ActorType
    identifier: Optional[str] = None             # e.g. "claude-3-5-sonnet", username
    model_metadata: Optional[dict[str, Any]] = None  # AI model details if known


class Event(BaseModel):
    """A normalized event from any adapter. The atomic unit.

    `action` is open-vocabulary; the meta-schema does not constrain its
    values. Adapters emit whatever action terms make sense in their
    source domain; novel terms surface as schema deltas downstream.

    Privacy posture (v0.2):
        ``content`` is optional. When set, ``content_hash`` is
        auto-computed (sha256 over the UTF-8 encoded string) by the
        model validator. Adapters that run in redact mode supply
        ``content_hash`` directly and leave ``content`` unset, so the
        audit can demonstrate that an event existed and verify its
        content without publishing it. ``AuditArtifact.to_published()``
        strips ``content`` from events that are not covered by a
        Decision with ``publish_level="verbatim"``.

        Both fields may be ``None`` for purely structural events that
        carry no payload (e.g., a hook firing with no stdout).
    """

    event_id: str = Field(default_factory=_new_id)
    timestamp: datetime
    actor: Actor
    action: str                  # open vocab: write|edit|run|prompt|generate|...
    target: str                  # what was acted upon
    content: Optional[str] = None
    content_hash: Optional[str] = None
    source_ref: SourceRef
    tier: CaptureTier

    @model_validator(mode="after")
    def _auto_hash(self) -> "Event":
        """Auto-fill ``content_hash`` from ``content`` when content is set
        and hash is not. Never overwrites an existing hash (so redact-mode
        events keep the hash the adapter supplied, and re-parsed audits
        round-trip cleanly)."""
        if self.content is not None and self.content_hash is None:
            self.content_hash = _sha256(self.content)
        return self


class Evidence(BaseModel):
    """Composite of one or more events supporting a decision."""

    evidence_id: str = Field(default_factory=_new_id)
    event_ids: list[str]
    description: str
    confidence: EvidenceConfidence = EvidenceConfidence.MEDIUM


class Decision(BaseModel):
    """A point where a methodological choice was made.

    ``decision_type`` draws from the open vocabulary. If the audit
    cannot classify the decision under any existing vocabulary term,
    set ``decision_type = "unclassified"`` and
    ``schema_gap = "novel_pattern"``; a corresponding SchemaDelta should
    accompany the audit.

    ``publish_level`` (v0.2) controls what
    ``AuditArtifact.to_published()`` does with this Decision's evidence:
        - ``"summary"`` (default): events backing this Decision have
          ``content`` stripped at publish time; only ``content_hash``
          and structural fields survive. The author's own description
          on the Decision and Evidence objects is preserved — that is
          curated disclosure, not adapter capture.
        - ``"verbatim"``: events backing this Decision keep their
          ``content``. Use when verbatim content is itself the
          deliverable (e.g., Smith 2026 podcast prompts/outputs).
    """

    decision_id: str = Field(default_factory=_new_id)
    timestamp: datetime
    decision_type: str           # open vocab; "unclassified" allowed with schema_gap
    description: str
    actor: Actor                 # primary actor responsible for the decision
    evidence_ids: list[str]
    schema_gap: Optional[Literal["novel_pattern"]] = None
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    verification_notes: Optional[str] = None
    publish_level: Literal["summary", "verbatim"] = "summary"

    @model_validator(mode="after")
    def _gap_iff_unclassified(self) -> "Decision":
        if self.decision_type == "unclassified" and self.schema_gap is None:
            raise ValueError(
                "decision_type='unclassified' requires schema_gap='novel_pattern'"
            )
        if self.schema_gap == "novel_pattern" and self.decision_type != "unclassified":
            raise ValueError(
                "schema_gap='novel_pattern' requires decision_type='unclassified'"
            )
        return self


class Claim(BaseModel):
    """A manuscript-level claim, traced to upstream decisions."""

    claim_id: str = Field(default_factory=_new_id)
    text: str
    location: str                # section/page/anchor in manuscript
    upstream_decision_ids: list[str]
    evidence_confidence: EvidenceConfidence = EvidenceConfidence.MEDIUM


class SchemaDelta(BaseModel):
    """A proposed extension to the open vocabulary, emitted by an audit.

    Deltas are second-class citizens until adjudicated. The governance
    protocol for accepting, merging, or rejecting deltas is out of scope
    for this release.
    """

    delta_id: str = Field(default_factory=_new_id)
    proposed_term: str
    proposed_kind: SchemaDeltaKind
    justification: str
    source_audit_id: str
    raw_evidence_ids: list[str]
    proposed_at: datetime
    status: SchemaDeltaStatus = SchemaDeltaStatus.PROPOSED
    merged_into: Optional[str] = None  # required iff status == MERGED_INTO

    @model_validator(mode="after")
    def _merge_target_iff_merged(self) -> "SchemaDelta":
        if self.status == SchemaDeltaStatus.MERGED_INTO and not self.merged_into:
            raise ValueError("status=merged_into requires merged_into target")
        if self.status != SchemaDeltaStatus.MERGED_INTO and self.merged_into:
            raise ValueError("merged_into is only valid when status=merged_into")
        return self


# ---------------------------------------------------------------------------
# Top-level container
# ---------------------------------------------------------------------------


class AdapterUsage(BaseModel):
    """Record of which adapter (and version) contributed to this audit."""

    adapter_name: str
    adapter_version: str
    capture_tier: CaptureTier


class AuditArtifact(BaseModel):
    """Top-level audit output for a single paper or project.

    Integrity (referential closure of IDs within the artifact) is checked by
    `validate_integrity()`. Pydantic's per-field validation does not catch
    cross-entity reference errors; call `validate_integrity()` explicitly.
    """

    audit_id: str = Field(default_factory=_new_id)
    audit_target: str                          # paper DOI, repo URL, project ID
    meta_schema_version: str = META_SCHEMA_VERSION
    vocabulary_version: str                    # vocabulary version used for this audit
    capture_tier_achieved: CaptureTier
    audit_timestamp: datetime
    adapters_used: list[AdapterUsage]

    events: list[Event] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    schema_deltas: list[SchemaDelta] = Field(default_factory=list)

    notes: Optional[str] = None

    # ---- publishing posture (v0.2) ----

    def to_published(self) -> "AuditArtifact":
        """Return a copy with non-verbatim Event content stripped.

        Algorithm:
            1. Walk every Decision whose ``publish_level == "verbatim"``;
               collect ``decision.evidence_ids`` and follow them to
               ``evidence.event_ids``. The union of those event_ids is
               the verbatim set.
            2. Copy ``self``. For every Event whose ``event_id`` is NOT
               in the verbatim set, set ``content = None``.
               ``content_hash`` is preserved so the published artifact
               still demonstrates the event existed and can verify any
               later disclosure.
            3. Author-written fields (Decision.description,
               Evidence.description, Claim.text, AuditArtifact.notes)
               are NEVER touched. Those are curated disclosure, not
               adapter capture.

        For audits where no Decision is marked verbatim (the default,
        minimum-capture case), every Event's content is stripped. If
        the source adapter already ran with ``redact=True``, the
        Events arrived with ``content=None`` and this method is a
        near-no-op (content was never set to begin with).
        """
        evidence_by_id = {e.evidence_id: e for e in self.evidence}

        verbatim_event_ids: set[str] = set()
        for d in self.decisions:
            if d.publish_level != "verbatim":
                continue
            for eid in d.evidence_ids:
                ev = evidence_by_id.get(eid)
                if ev is None:
                    continue
                verbatim_event_ids.update(ev.event_ids)

        new_events: list[Event] = []
        for ev in self.events:
            if ev.event_id in verbatim_event_ids:
                new_events.append(ev)
            else:
                new_events.append(ev.model_copy(update={"content": None}))

        return self.model_copy(update={"events": new_events})

    # ---- integrity ----

    def validate_integrity(self) -> list[str]:
        """Return a list of integrity errors. Empty list means valid.

        Checks:
        - Every event_id referenced by Evidence exists in self.events
        - Every evidence_id referenced by Decision exists in self.evidence
        - Every decision_id referenced by Claim exists in self.decisions
        - Every raw_evidence_id referenced by SchemaDelta exists in self.evidence
        - source_audit_id on each SchemaDelta matches self.audit_id
        - meta_schema_version matches the META_SCHEMA_VERSION this code declares
        """
        errors: list[str] = []

        event_ids = {e.event_id for e in self.events}
        evidence_ids = {e.evidence_id for e in self.evidence}
        decision_ids = {d.decision_id for d in self.decisions}

        for ev in self.evidence:
            for eid in ev.event_ids:
                if eid not in event_ids:
                    errors.append(
                        f"Evidence {ev.evidence_id} references missing event {eid}"
                    )

        for d in self.decisions:
            for eid in d.evidence_ids:
                if eid not in evidence_ids:
                    errors.append(
                        f"Decision {d.decision_id} references missing evidence {eid}"
                    )

        for c in self.claims:
            for did in c.upstream_decision_ids:
                if did not in decision_ids:
                    errors.append(
                        f"Claim {c.claim_id} references missing decision {did}"
                    )

        for sd in self.schema_deltas:
            for eid in sd.raw_evidence_ids:
                if eid not in evidence_ids:
                    errors.append(
                        f"SchemaDelta {sd.delta_id} references missing evidence {eid}"
                    )
            if sd.source_audit_id != self.audit_id:
                errors.append(
                    f"SchemaDelta {sd.delta_id} source_audit_id "
                    f"{sd.source_audit_id} != audit_id {self.audit_id}"
                )

        if self.meta_schema_version != META_SCHEMA_VERSION:
            errors.append(
                f"meta_schema_version {self.meta_schema_version} does not match "
                f"installed META_SCHEMA_VERSION {META_SCHEMA_VERSION}; "
                f"a migration may be required"
            )

        return errors


__all__ = [
    "META_SCHEMA_VERSION",
    "ActorType",
    "CaptureTier",
    "VerificationStatus",
    "EvidenceConfidence",
    "SchemaDeltaKind",
    "SchemaDeltaStatus",
    "SourceRef",
    "Actor",
    "Event",
    "Evidence",
    "Decision",
    "Claim",
    "SchemaDelta",
    "AdapterUsage",
    "AuditArtifact",
]
