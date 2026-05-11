"""
AIVS adapter interface and registry.

An EvidenceAdapter knows one source type (git, Claude Code session,
Jupyter notebook, slurm logs, conda env, Cursor chat export, Aider
markdown log, ...) and emits a normalized stream of Events. Downstream
agents operate on the normalized stream and never see raw source
formats.

The registry is a process-local list. Adapters register themselves
by being importable from `aivs.adapters` and calling
`register_adapter(cls)` at module load. `discover_adapters(path)`
returns the subset of registered adapters whose `.detect(path)` is
True. This is intentionally simple — no entry points, no plugin
discovery — so the registry can grow incrementally.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Iterator, List, Optional, Type

from aivs.meta_schema import CaptureTier, Event


class EvidenceAdapter(ABC):
    """Base class for all evidence adapters.

    Subclasses MUST set:
        name              — stable adapter identifier (e.g. "git",
                            "claude_code", "codex", "aider")
        version           — semver string for this adapter
                            implementation
        capture_tier      — the tier this adapter targets when its
                            source is present and well-formed

    Subclasses MUST implement:
        detect(project_path) -> bool
            Return True if this adapter's source is present in
            project_path and the adapter expects to be able to
            extract from it. Detection should be fast and side-effect
            free.

        extract(project_path, since=None, until=None) -> Iterator[Event]
            Yield normalized events. Each event MUST set
            source_ref.adapter_name to self.name and
            source_ref.adapter_version to self.version.
    """

    name: str
    version: str
    capture_tier: CaptureTier

    @abstractmethod
    def detect(self, project_path: Path) -> bool:
        ...

    @abstractmethod
    def extract(
        self,
        project_path: Path,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> Iterator[Event]:
        ...


_REGISTRY: List[Type[EvidenceAdapter]] = []


def register_adapter(cls: Type[EvidenceAdapter]) -> Type[EvidenceAdapter]:
    """Decorator/function to register an adapter class.

    Idempotent: registering the same class twice is a no-op.
    """
    if cls not in _REGISTRY:
        _REGISTRY.append(cls)
    return cls


def registered_adapters() -> List[Type[EvidenceAdapter]]:
    """Return a copy of the registered adapter classes."""
    return list(_REGISTRY)


def discover_adapters(project_path: Path) -> List[EvidenceAdapter]:
    """Return instances of adapters whose source is present in project_path.

    Adapters are instantiated with no arguments. Adapters needing
    configuration should accept optional kwargs at __init__ and provide
    sensible defaults.
    """
    out: List[EvidenceAdapter] = []
    for cls in _REGISTRY:
        try:
            instance = cls()
        except Exception:
            # An adapter that fails to instantiate is silently skipped;
            # we never want adapter discovery to fail the whole audit.
            continue
        try:
            if instance.detect(project_path):
                out.append(instance)
        except Exception:
            continue
    return out


__all__ = [
    "EvidenceAdapter",
    "register_adapter",
    "registered_adapters",
    "discover_adapters",
]
