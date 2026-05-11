"""
Aider chat-history adapter (stub with minimal parser).

Aider writes a markdown log per project at <project>/.aider.chat.history.md
with a structure like:

    # aider chat started at 2026-04-19 14:32:01
    > /add foo.py
    #### what does foo.py do?
    Foo.py does X, Y, Z.
    > /diff
    ...

The format is human-readable and informal. This stub does a line-based
parse that identifies user prompts (lines starting with '#### ') and
assistant responses (everything until the next '> ' command or '#### '
prompt). Tool-use events are not separable in this format — aider
expresses them as diff blocks inline.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional

from aivs.meta_schema import (
    Actor,
    ActorType,
    CaptureTier,
    Event,
    SourceRef,
)
from aivs.adapters.base import EvidenceAdapter, register_adapter


_SESSION_HEADER = re.compile(
    r"^#\s+aider chat started at\s+(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})"
)
_PROMPT = re.compile(r"^####\s+(.*)$")


@register_adapter
class AiderAdapter(EvidenceAdapter):
    """Adapter for Aider .aider.chat.history.md logs."""

    name = "aider"
    version = "0.1.0"
    capture_tier = CaptureTier.TIER_1  # markdown is lower fidelity

    def _log_path(self, project_path: Path) -> Path:
        return project_path / ".aider.chat.history.md"

    def detect(self, project_path: Path) -> bool:
        p = self._log_path(project_path)
        try:
            return p.is_file() and p.stat().st_size > 0
        except OSError:
            return False

    def extract(
        self,
        project_path: Path,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> Iterator[Event]:
        path = self._log_path(project_path)
        current_ts: Optional[datetime] = None
        current_prompt: Optional[str] = None
        response_buf: list[str] = []
        line_no_of_prompt = 0

        def flush_response() -> Iterator[Event]:
            if current_prompt is None or current_ts is None:
                return
            if since is not None and current_ts < since:
                return
            if until is not None and current_ts > until:
                return
            # User prompt event.
            yield Event(
                timestamp=current_ts,
                actor=Actor(actor_type=ActorType.HUMAN, identifier="user"),
                action="prompt",
                target="aider_session",
                content=current_prompt,
                source_ref=SourceRef(
                    adapter_name=self.name,
                    adapter_version=self.version,
                    raw_location=f"{path}:{line_no_of_prompt}",
                    extracted_at=datetime.utcnow(),
                ),
                tier=self.capture_tier,
            )
            # Assistant response event.
            response_text = "\n".join(response_buf).strip()
            if response_text:
                yield Event(
                    timestamp=current_ts,
                    actor=Actor(
                        actor_type=ActorType.AI_GENERATIVE,
                        identifier="Aider",
                    ),
                    action="respond",
                    target="aider_session",
                    content=response_text,
                    source_ref=SourceRef(
                        adapter_name=self.name,
                        adapter_version=self.version,
                        raw_location=f"{path}:{line_no_of_prompt}+",
                        extracted_at=datetime.utcnow(),
                    ),
                    tier=self.capture_tier,
                )

        with path.open("r", encoding="utf-8") as fh:
            for line_no, raw in enumerate(fh, start=1):
                line = raw.rstrip("\n")
                m = _SESSION_HEADER.match(line)
                if m:
                    # New session header; flush previous prompt/response.
                    yield from flush_response()
                    current_prompt = None
                    response_buf = []
                    try:
                        current_ts = datetime.fromisoformat(
                            m.group(1).replace(" ", "T")
                        )
                    except ValueError:
                        current_ts = None
                    continue

                mp = _PROMPT.match(line)
                if mp:
                    # New prompt; flush previous if any.
                    yield from flush_response()
                    current_prompt = mp.group(1).strip()
                    response_buf = []
                    line_no_of_prompt = line_no
                    continue

                if current_prompt is not None:
                    response_buf.append(line)

        yield from flush_response()


__all__ = ["AiderAdapter"]
