"""
Claude Code session adapter.

Reads Claude Code session JSONL files stored under
~/.claude/projects/<path-hash>/<session-uuid>.jsonl on the machine
where Claude Code ran. Each line is one JSONL event; the adapter
emits one or more NormalizedEvents per line depending on event type.

Event types observed (Claude Code 2.1.97):
    queue-operation        — task-queue bookkeeping; skipped by default
    attachment             — hooks, MCP tool-listings, skill listings,
                             deferred-tools deltas. Most are skipped at
                             default verbosity; hook events surface at
                             verbosity=verbose.
    user                   — user prompt (message.content=string) OR
                             tool result (message.content=list)
    assistant              — assistant text response, thinking block,
                             or tool_use call (message.content=list of
                             typed blocks)
    last-prompt            — session-end metadata; skipped

Mapping into NormalizedEvent:
    user (string)          → action=prompt, actor=human
    user (tool_result)     → action=tool_result, actor=system
    assistant.text         → action=respond, actor=ai_generative
    assistant.thinking     → action=think, actor=ai_generative
                             (verbosity=verbose only)
    assistant.tool_use     → action=tool_use, actor=ai_autonomous
    attachment.hook_*      → action=hook, actor=system
                             (verbosity=verbose only)

Project-path discovery:
    Claude Code stores sessions under ~/.claude/projects/<hash>/ where
    <hash> is the absolute project path with "/" replaced by "-". The
    adapter resolves project_path to that hash and reads every .jsonl
    file in the corresponding directory. If ~/.claude/projects is not
    present, detect() returns False.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, Literal, Optional

from aivs.meta_schema import (
    Actor,
    ActorType,
    CaptureTier,
    Event,
    SourceRef,
)
from aivs.adapters.base import EvidenceAdapter, register_adapter

Verbosity = Literal["summary", "default", "verbose"]


# Event types we know about and intentionally drop before type-dispatch.
# These are session bookkeeping with no decision content. Two of them
# (permission-mode, file-history-snapshot) are candidates for explicit
# modeling in v0.2 — in particular permission-mode toggles (plan →
# default → bypass) are arguably meta-decisions about *how* to run
# Claude Code on a given task. See NEXT.md.
_SKIP_EVENT_TYPES = frozenset(
    {
        "queue-operation",
        "last-prompt",
        "permission-mode",
        "file-history-snapshot",
        "system",
    }
)


@register_adapter
class ClaudeCodeAdapter(EvidenceAdapter):
    """Adapter for Claude Code session JSONL logs."""

    name = "claude_code"
    version = "0.1.0"
    capture_tier = CaptureTier.TIER_3

    def __init__(
        self,
        verbosity: Verbosity = "default",
        claude_home: Optional[Path] = None,
    ) -> None:
        self.verbosity = verbosity
        self.claude_home = (
            claude_home
            if claude_home is not None
            else Path(os.environ.get("CLAUDE_HOME", Path.home() / ".claude"))
        )

    # -- Discovery -----------------------------------------------------

    def _projects_root(self) -> Path:
        return self.claude_home / "projects"

    def _project_dir(self, project_path: Path) -> Path:
        """Translate /storage/kiran-stuff/triplet-proof to
        ~/.claude/projects/-storage-kiran-stuff-triplet-proof"""
        absolute = project_path.resolve()
        hash_name = str(absolute).replace("/", "-")
        return self._projects_root() / hash_name

    def detect(self, project_path: Path) -> bool:
        if not self._projects_root().is_dir():
            return False
        pdir = self._project_dir(project_path)
        if not pdir.is_dir():
            return False
        # Require at least one non-empty JSONL.
        for f in pdir.glob("*.jsonl"):
            try:
                if f.stat().st_size > 0:
                    return True
            except OSError:
                continue
        return False

    # -- Extraction ----------------------------------------------------

    def extract(
        self,
        project_path: Path,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> Iterator[Event]:
        pdir = self._project_dir(project_path)
        for jsonl_path in sorted(pdir.glob("*.jsonl")):
            yield from self._extract_one(jsonl_path, since, until)

    def _extract_one(
        self,
        jsonl_path: Path,
        since: Optional[datetime],
        until: Optional[datetime],
    ) -> Iterator[Event]:
        with jsonl_path.open("r", encoding="utf-8") as fh:
            for line_no, raw in enumerate(fh, start=1):
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    obj = json.loads(raw)
                except json.JSONDecodeError:
                    # Malformed line — skip but don't fail the whole file.
                    continue

                ts = self._parse_ts(obj.get("timestamp"))
                if ts is None:
                    continue
                if since is not None and ts < since:
                    continue
                if until is not None and ts > until:
                    continue

                yield from self._emit(obj, ts, jsonl_path, line_no)

    # -- Per-event emission --------------------------------------------

    def _emit(
        self,
        obj: Dict[str, Any],
        ts: datetime,
        jsonl_path: Path,
        line_no: int,
    ) -> Iterator[Event]:
        kind = obj.get("type")
        session_id = obj.get("sessionId", "unknown")
        cwd = obj.get("cwd")
        git_branch = obj.get("gitBranch")
        cc_version = obj.get("version")
        src = self._src(jsonl_path, line_no)

        if kind in _SKIP_EVENT_TYPES:
            return

        if kind == "user":
            yield from self._emit_user(obj, ts, session_id, src, cwd, git_branch)
            return

        if kind == "assistant":
            yield from self._emit_assistant(
                obj, ts, session_id, src, cwd, git_branch, cc_version
            )
            return

        if kind == "attachment":
            if self.verbosity == "verbose":
                yield from self._emit_attachment(obj, ts, session_id, src)
            return

        # Unknown event type — only surface at verbose for forensic value.
        if self.verbosity == "verbose":
            yield Event(
                timestamp=ts,
                actor=Actor(actor_type=ActorType.UNKNOWN, identifier="unknown"),
                action="unknown_event",
                target=f"event_type:{kind}",
                content=json.dumps(obj)[:500],
                source_ref=src,
                tier=self.capture_tier,
            )

    def _emit_user(
        self,
        obj: Dict[str, Any],
        ts: datetime,
        session_id: str,
        src: SourceRef,
        cwd: Optional[str],
        git_branch: Optional[str],
    ) -> Iterator[Event]:
        message = obj.get("message", {})
        content = message.get("content")

        if isinstance(content, str):
            yield Event(
                timestamp=ts,
                actor=Actor(actor_type=ActorType.HUMAN, identifier="user"),
                action="prompt",
                target=f"session:{session_id}",
                content=content,
                source_ref=src,
                tier=self.capture_tier,
            )
            return

        if isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_result":
                    yield Event(
                        timestamp=ts,
                        actor=Actor(
                            actor_type=ActorType.SYSTEM,
                            identifier="tool_runtime",
                        ),
                        action="tool_result",
                        target=f"tool_use:{block.get('tool_use_id', 'unknown')}",
                        content=self._stringify(block.get("content")),
                        source_ref=src,
                        tier=self.capture_tier,
                    )

    def _emit_assistant(
        self,
        obj: Dict[str, Any],
        ts: datetime,
        session_id: str,
        src: SourceRef,
        cwd: Optional[str],
        git_branch: Optional[str],
        cc_version: Optional[str],
    ) -> Iterator[Event]:
        message = obj.get("message", {})
        content = message.get("content", [])
        model = message.get("model")

        ai_actor = Actor(
            actor_type=ActorType.AI_GENERATIVE,
            identifier="Claude Code",
            model_metadata={
                "model": model,
                "claude_code_version": cc_version,
                "cwd": cwd,
                "git_branch": git_branch,
            },
        )
        ai_autonomous = Actor(
            actor_type=ActorType.AI_AUTONOMOUS,
            identifier="Claude Code",
            model_metadata={
                "model": model,
                "claude_code_version": cc_version,
            },
        )

        if not isinstance(content, list):
            return

        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type")

            if btype == "text":
                if self.verbosity != "summary" or True:
                    # Text is high-signal; always emit.
                    yield Event(
                        timestamp=ts,
                        actor=ai_actor,
                        action="respond",
                        target=f"session:{session_id}",
                        content=block.get("text", ""),
                        source_ref=src,
                        tier=self.capture_tier,
                    )

            elif btype == "thinking":
                if self.verbosity == "verbose":
                    yield Event(
                        timestamp=ts,
                        actor=ai_actor,
                        action="think",
                        target=f"session:{session_id}",
                        content=block.get("thinking", ""),
                        source_ref=src,
                        tier=self.capture_tier,
                    )

            elif btype == "tool_use":
                tool_name = block.get("name", "unknown")
                tool_input = block.get("input", {})
                tool_id = block.get("id", "")
                yield Event(
                    timestamp=ts,
                    actor=ai_autonomous,
                    action="tool_use",
                    target=f"tool:{tool_name}",
                    content=json.dumps(
                        {"tool_use_id": tool_id, "input": tool_input},
                        default=str,
                    ),
                    source_ref=src,
                    tier=self.capture_tier,
                )

    def _emit_attachment(
        self,
        obj: Dict[str, Any],
        ts: datetime,
        session_id: str,
        src: SourceRef,
    ) -> Iterator[Event]:
        att = obj.get("attachment", {})
        att_type = att.get("type", "unknown")

        if att_type.startswith("hook_"):
            hook_name = att.get("hookName", "unknown")
            yield Event(
                timestamp=ts,
                actor=Actor(
                    actor_type=ActorType.SYSTEM,
                    identifier="claude_code_hook",
                ),
                action="hook",
                target=f"hook:{hook_name}",
                content=self._stringify(att.get("stdout") or att.get("content")),
                source_ref=src,
                tier=self.capture_tier,
            )
        # Other attachment types (deferred_tools_delta, skill_listing,
        # mcp_instructions_delta) are session-setup noise; skip even in
        # verbose mode.

    # -- Helpers -------------------------------------------------------

    def _src(self, jsonl_path: Path, line_no: int) -> SourceRef:
        return SourceRef(
            adapter_name=self.name,
            adapter_version=self.version,
            raw_location=f"{jsonl_path}:{line_no}",
            extracted_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _parse_ts(ts_str: Optional[str]) -> Optional[datetime]:
        if not ts_str:
            return None
        try:
            # Handle trailing 'Z' (UTC).
            if ts_str.endswith("Z"):
                ts_str = ts_str[:-1] + "+00:00"
            return datetime.fromisoformat(ts_str)
        except ValueError:
            return None

    @staticmethod
    def _stringify(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, (dict, list)):
            return json.dumps(value, default=str)
        return str(value)


__all__ = ["ClaudeCodeAdapter"]
