"""
OpenAI Codex CLI session adapter (stub).

Codex CLI stores session data under ~/.codex/sessions/ (format
varies by release; recent versions use JSON files per session with
fields: id, created_at, messages[]). This stub documents the contract
but does not implement extraction. The contract for a working
implementation:

    detect:
        return True if ~/.codex/sessions/ exists AND there is at least
        one session whose working_directory matches project_path (or
        a session referencing files inside project_path).

    extract:
        for each matching session JSON file:
            for each message in session.messages:
                if message.role == 'user':
                    yield Event(actor=human, action=prompt, ...)
                if message.role == 'assistant':
                    yield Event(actor=ai_generative, action=respond, ...)
                if message.tool_calls:
                    for call in message.tool_calls:
                        yield Event(actor=ai_autonomous,
                                    action=tool_use,
                                    target=f"tool:{call.name}", ...)

Real implementation deferred — Codex session format is unstable across
releases and there's currently no example data on Kiran's system
(/storage/kiran-stuff/.codex is an empty file, not a directory).
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional

from aivs.meta_schema import CaptureTier, Event
from aivs.adapters.base import EvidenceAdapter, register_adapter


@register_adapter
class CodexAdapter(EvidenceAdapter):
    """Stub adapter for OpenAI Codex CLI sessions. Detection only."""

    name = "codex"
    version = "0.0.0-stub"
    capture_tier = CaptureTier.TIER_2

    def __init__(self, codex_home: Optional[Path] = None) -> None:
        self.codex_home = (
            codex_home
            if codex_home is not None
            else Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        )

    def detect(self, project_path: Path) -> bool:
        sessions_dir = self.codex_home / "sessions"
        if not sessions_dir.is_dir():
            return False
        # Stub: report present if there's any session file at all.
        # A real implementation would cross-reference session metadata
        # with project_path.
        try:
            return any(sessions_dir.iterdir())
        except OSError:
            return False

    def extract(
        self,
        project_path: Path,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> Iterator[Event]:
        # Stub: yield nothing. A NotImplementedError would break
        # discover_adapters() callers, so we silently emit no events.
        # When implementation lands, replace this body with the parser.
        return
        yield  # unreachable; preserves generator typing


__all__ = ["CodexAdapter"]
