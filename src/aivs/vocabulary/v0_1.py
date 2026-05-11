"""
AIVS open vocabulary — version 0.1.

Intentionally near-empty. The vocabulary accretes from real audits via
SchemaDelta proposals, not from speculation. Each version is immutable
once published; new terms produce a new version.

The single seed term is `"unclassified"`, which is required by the
meta-schema as the placeholder for novel patterns surfaced via
`schema_gap = "novel_pattern"`.
"""

from __future__ import annotations

VOCABULARY_VERSION = "0.1.0"


# Decision types observed and accepted in audits.
# `unclassified` is reserved and always present.
DECISION_TYPES: frozenset[str] = frozenset(
    {
        "unclassified",
    }
)


# Action terms used by adapters when emitting Events.
# Adapters MAY emit terms not in this set; novel terms surface as
# SchemaDelta(proposed_kind=ACTION_TYPE) downstream.
KNOWN_ACTIONS: frozenset[str] = frozenset(set())


# Named evidence relations between Decisions and Evidence
# (e.g. "produced_by", "verified_by", "contradicted_by"). Empty in v0.1.
EVIDENCE_RELATIONS: frozenset[str] = frozenset(set())


def is_known_decision_type(term: str) -> bool:
    return term in DECISION_TYPES


def is_known_action(term: str) -> bool:
    return term in KNOWN_ACTIONS


def is_known_evidence_relation(term: str) -> bool:
    return term in EVIDENCE_RELATIONS


__all__ = [
    "VOCABULARY_VERSION",
    "DECISION_TYPES",
    "KNOWN_ACTIONS",
    "EVIDENCE_RELATIONS",
    "is_known_decision_type",
    "is_known_action",
    "is_known_evidence_relation",
]
