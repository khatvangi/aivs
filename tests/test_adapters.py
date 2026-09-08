"""Tests for the adapter layer.

These tests use synthetic fixtures written to a tmp_path so they
don't depend on any specific machine's session history.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from aivs.adapters import (
    discover_adapters,
    registered_adapters,
)
from aivs.adapters.claude_code import ClaudeCodeAdapter, _session_dir_name
from aivs.adapters.aider import AiderAdapter
from aivs.adapters.codex import CodexAdapter
from aivs.meta_schema import ActorType


# --- Registry -----------------------------------------------------------


def test_registry_contains_all_three():
    names = {cls.name for cls in registered_adapters()}
    assert {"claude_code", "codex", "aider"} <= names


# --- ClaudeCodeAdapter --------------------------------------------------


def _write_cc_fixture(tmp_path: Path) -> tuple[Path, Path]:
    """Write a minimal Claude Code session JSONL to a fake .claude tree."""
    project = tmp_path / "myproject"
    project.mkdir()
    claude_home = tmp_path / "fake_claude_home"
    # must use the same collapsing rule Claude Code uses ("/", "_" and "."
    # all map to "-"). This fixture previously hardcoded a bare "/"
    # replacement, which mirrored the adapter bug fixed on 2026-09-08 and
    # is why the suite could not detect it: pytest tmp_path names contain
    # underscores, so fixture and adapter agreed only while both were wrong.
    sessions = claude_home / "projects" / _session_dir_name(project.resolve())
    sessions.mkdir(parents=True)

    session_id = "abc12345-1234-1234-1234-123456789abc"
    events = [
        {
            "type": "queue-operation",
            "operation": "enqueue",
            "timestamp": "2026-05-01T10:00:00.000Z",
            "sessionId": session_id,
        },
        {
            "type": "user",
            "message": {"role": "user", "content": "Run the regression test."},
            "uuid": "u1",
            "timestamp": "2026-05-01T10:00:05.000Z",
            "sessionId": session_id,
            "cwd": str(project),
            "version": "2.1.97",
            "gitBranch": "main",
        },
        {
            "type": "assistant",
            "message": {
                "model": "claude-opus-4-6",
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "I'll run pytest."},
                    {
                        "type": "tool_use",
                        "id": "toolu_1",
                        "name": "Bash",
                        "input": {"command": "pytest -q"},
                    },
                ],
            },
            "uuid": "a1",
            "timestamp": "2026-05-01T10:00:06.000Z",
            "sessionId": session_id,
            "cwd": str(project),
            "version": "2.1.97",
        },
        {
            "type": "user",
            "message": {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "toolu_1",
                        "content": "8 passed in 0.20s",
                        "is_error": False,
                    }
                ],
            },
            "uuid": "u2",
            "timestamp": "2026-05-01T10:00:08.000Z",
            "sessionId": session_id,
        },
        {
            "type": "attachment",
            "attachment": {
                "type": "hook_success",
                "hookName": "Stop",
                "stdout": '{"decision": "approve"}',
            },
            "uuid": "att1",
            "timestamp": "2026-05-01T10:00:09.000Z",
            "sessionId": session_id,
        },
        {"type": "last-prompt", "lastPrompt": "...", "sessionId": session_id},
    ]
    jsonl_path = sessions / f"{session_id}.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev) + "\n")
    return project, claude_home


def test_claude_code_default_verbosity(tmp_path):
    project, claude_home = _write_cc_fixture(tmp_path)
    adapter = ClaudeCodeAdapter(verbosity="default", claude_home=claude_home)
    assert adapter.detect(project) is True

    events = list(adapter.extract(project))
    # default: prompt, assistant_text, tool_use, tool_result = 4 events
    actions = [e.action for e in events]
    assert actions == ["prompt", "respond", "tool_use", "tool_result"]
    assert events[0].actor.actor_type == ActorType.HUMAN
    assert events[1].actor.actor_type == ActorType.AI_GENERATIVE
    assert events[2].actor.actor_type == ActorType.AI_AUTONOMOUS
    assert events[3].actor.actor_type == ActorType.SYSTEM


def test_claude_code_verbose_includes_hooks(tmp_path):
    project, claude_home = _write_cc_fixture(tmp_path)
    adapter = ClaudeCodeAdapter(verbosity="verbose", claude_home=claude_home)
    events = list(adapter.extract(project))
    actions = [e.action for e in events]
    assert "hook" in actions


def test_claude_code_detect_negative(tmp_path):
    # No .claude directory at all.
    project = tmp_path / "lonely"
    project.mkdir()
    adapter = ClaudeCodeAdapter(claude_home=tmp_path / "absent")
    assert adapter.detect(project) is False


def test_claude_code_model_metadata_propagates(tmp_path):
    project, claude_home = _write_cc_fixture(tmp_path)
    adapter = ClaudeCodeAdapter(claude_home=claude_home)
    events = list(adapter.extract(project))
    respond = [e for e in events if e.action == "respond"][0]
    assert respond.actor.model_metadata["model"] == "claude-opus-4-6"
    assert respond.actor.model_metadata["claude_code_version"] == "2.1.97"


# --- AiderAdapter -------------------------------------------------------


def _write_aider_fixture(tmp_path: Path) -> Path:
    project = tmp_path / "aiderproj"
    project.mkdir()
    log = project / ".aider.chat.history.md"
    log.write_text(
        "# aider chat started at 2026-04-19 14:32:01\n"
        "> /add main.py\n"
        "#### Fix the off-by-one in the loop\n"
        "I'll change the range to start at 0.\n"
        "```python\n"
        "for i in range(0, n):\n"
        "```\n"
        "#### Run the tests now\n"
        "Tests pass: 12/12.\n",
        encoding="utf-8",
    )
    return project


def test_aider_detect_and_extract(tmp_path):
    project = _write_aider_fixture(tmp_path)
    adapter = AiderAdapter()
    assert adapter.detect(project) is True
    events = list(adapter.extract(project))
    actions = [e.action for e in events]
    # Two prompts → two prompt + two respond
    assert actions.count("prompt") == 2
    assert actions.count("respond") == 2


# --- CodexAdapter -------------------------------------------------------


def test_codex_detect_negative_when_absent(tmp_path):
    adapter = CodexAdapter(codex_home=tmp_path / "nope")
    assert adapter.detect(tmp_path) is False


def test_codex_extract_is_empty_stub(tmp_path):
    sessions = tmp_path / "codex_home" / "sessions"
    sessions.mkdir(parents=True)
    (sessions / "fake.json").write_text("{}", encoding="utf-8")
    adapter = CodexAdapter(codex_home=tmp_path / "codex_home")
    assert adapter.detect(tmp_path) is True
    assert list(adapter.extract(tmp_path)) == []  # stub yields nothing


# --- v0.2 privacy posture (redact mode) --------------------------------


def test_claude_code_redact_default_true(tmp_path):
    """With no redact arg, emitted Events carry only content_hash."""
    project, claude_home = _write_cc_fixture(tmp_path)
    adapter = ClaudeCodeAdapter(claude_home=claude_home)  # redact default
    events = list(adapter.extract(project))
    payload_events = [e for e in events if e.content_hash is not None]
    assert payload_events  # at least one event has a hash
    for e in payload_events:
        assert e.content is None
        assert isinstance(e.content_hash, str)
        assert len(e.content_hash) == 64  # sha256 hex


def test_claude_code_redact_false(tmp_path):
    """With redact=False, both content and content_hash are populated."""
    import hashlib
    project, claude_home = _write_cc_fixture(tmp_path)
    adapter = ClaudeCodeAdapter(claude_home=claude_home, redact=False)
    events = list(adapter.extract(project))
    prompt = next(e for e in events if e.action == "prompt")
    assert prompt.content == "Run the regression test."
    assert prompt.content_hash == hashlib.sha256(
        "Run the regression test.".encode("utf-8")
    ).hexdigest()


def test_claude_code_session_dir_override(tmp_path):
    """session_dir_override lets the adapter point at a non-default
    session directory — useful when a project has been renamed and the
    on-disk path no longer matches the path Claude Code originally
    hashed."""
    # Build a normal fixture, then point an override-configured adapter
    # at a path that bears no relation to the fixture's "project_path".
    project, claude_home = _write_cc_fixture(tmp_path)
    real_session_dir = (
        claude_home / "projects" / _session_dir_name(project.resolve())
    )
    fake_project = tmp_path / "renamed_after_sessions"
    fake_project.mkdir()

    adapter = ClaudeCodeAdapter(
        claude_home=claude_home,
        session_dir_override=real_session_dir,
    )
    assert adapter.detect(fake_project) is True
    events = list(adapter.extract(fake_project))
    actions = [e.action for e in events]
    assert "prompt" in actions  # fixture has a prompt event


def test_aider_redact_default_true(tmp_path):
    project = _write_aider_fixture(tmp_path)
    adapter = AiderAdapter()  # redact default
    events = list(adapter.extract(project))
    for e in events:
        assert e.content is None
        assert e.content_hash is not None
        assert len(e.content_hash) == 64


def test_aider_redact_false(tmp_path):
    project = _write_aider_fixture(tmp_path)
    adapter = AiderAdapter(redact=False)
    events = list(adapter.extract(project))
    prompts = [e for e in events if e.action == "prompt"]
    assert any("off-by-one" in e.content for e in prompts)


# --- Discovery integration ---------------------------------------------


def test_discover_adapters_finds_claude_code(tmp_path):
    project, claude_home = _write_cc_fixture(tmp_path)
    # discover_adapters uses default constructors → won't find our
    # fake claude_home. This is the documented limitation: discovery
    # uses zero-arg construction. We verify discovery is callable.
    discovered = discover_adapters(project)
    # No assertions about content; just confirm it returns a list.
    assert isinstance(discovered, list)


# --- Session-directory name derivation (regression) ---------------------
#
# Claude Code collapses "/", "_" and "." alike to "-". The adapter replaced
# only "/" until 2026-09-08, so it could never locate sessions for a project
# whose path contained an underscore or a dot. The case that exposed it was
# this package's own case study, mechanism_classifier.


@pytest.mark.parametrize(
    "project_path,expected",
    [
        # the original, underscore-free case that always worked
        ("/storage/kiran-stuff/triplet-proof",
         "-storage-kiran-stuff-triplet-proof"),
        # the regression: underscores in BOTH path segments
        ("/storage/kiran-stuff/IDP_projects/mechanism_classifier",
         "-storage-kiran-stuff-IDP-projects-mechanism-classifier"),
        # a dot in a leading hidden directory, yielding a double dash
        ("/home/kiran/.claude/double-shot-latte",
         "-home-kiran--claude-double-shot-latte"),
        # a dot inside a version-numbered directory name
        ("/storage/kiran-stuff/USPEX-v10.5",
         "-storage-kiran-stuff-USPEX-v10-5"),
        # underscore and dot together
        ("/a/b_c/d.e_f",
         "-a-b-c-d-e-f"),
    ],
)
def test_session_dir_name_collapses_slash_underscore_and_dot(project_path, expected):
    assert _session_dir_name(project_path) == expected


def test_session_dir_name_leaves_no_underscore_or_dot():
    """No derived name may retain a separator Claude Code would have collapsed."""
    name = _session_dir_name("/storage/kiran-stuff/IDP_projects/mechanism_classifier")
    assert "_" not in name
    assert "." not in name


def test_project_dir_uses_collapsed_name(tmp_path):
    """The adapter's _project_dir must go through the collapsing rule, not
    a bare "/" replacement."""
    adapter = ClaudeCodeAdapter(claude_home=tmp_path)
    pdir = adapter._project_dir(Path("/storage/kiran-stuff/IDP_projects/mechanism_classifier"))
    assert pdir.name == "-storage-kiran-stuff-IDP-projects-mechanism-classifier"
    assert pdir.parent == tmp_path / "projects"


def test_claude_code_detect_finds_underscored_project(tmp_path):
    """End-to-end: a session directory for an underscored project path must be
    discoverable. This failed before the fix."""
    projects = tmp_path / "projects"
    sess = projects / "-storage-kiran-stuff-IDP-projects-mechanism-classifier"
    sess.mkdir(parents=True)
    (sess / "s.jsonl").write_text(json.dumps({
        "type": "user", "uuid": "u1", "timestamp": "2026-02-10T00:00:00Z",
        "message": {"role": "user", "content": "hello"},
    }) + "\n")
    adapter = ClaudeCodeAdapter(claude_home=tmp_path)
    assert adapter.detect(Path("/storage/kiran-stuff/IDP_projects/mechanism_classifier")) is True
