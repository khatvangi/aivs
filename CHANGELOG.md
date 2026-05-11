# Changelog

## v0.2.0 — 2026-05-11

**Constitutional fix: minimum-capture-for-purpose default; privacy
posture.** Audit resolution matches audit purpose. Verbatim content
(prompts, AI outputs, tool results, thinking blocks) is now
**private by default**; authors opt-in per Decision to publish.

### Meta-schema (`src/aivs/meta_schema/core.py`)

- `META_SCHEMA_VERSION` → `"0.2.0"`.
- `Event.content` is now `Optional[str]` (was required).
- `Event.content_hash: Optional[str]` added. A `@model_validator`
  auto-computes the SHA-256 hex digest from `content` when content is
  set and hash is not. Never overwrites a pre-set hash, so redact-mode
  Events round-trip cleanly.
- Pure-structural Events (neither content nor hash) are valid — the
  validator does not enforce that one of the two is set.
- `Decision.publish_level: Literal["summary", "verbatim"] = "summary"`
  added. Default flips the project's posture from disclosure-maximalist
  to reproducibility-anchored.
- `AuditArtifact.to_published()` method added. Returns a copy where
  every Event NOT in a verbatim Decision's evidence chain has
  `content` set to `None`; `content_hash` is preserved. Author-written
  fields (Decision.description, Evidence.description, Claim.text,
  audit `notes`) are never touched.

### Adapters (`src/aivs/adapters/`)

- `ClaudeCodeAdapter` (v0.2.0) and `AiderAdapter` (v0.2.0): added
  `redact: bool = True` constructor parameter. When True (default),
  emitted Events carry `content=None` and only `content_hash`.
- Module-level `_hash_content(s) -> str` helper in `claude_code.py`,
  reused by the aider adapter.

### Audit examples (`examples/`)

- `smith_2026_audit.py`: D3 (prompt engineering), D5 (iterative
  AI generation), D9 (content curation) marked `publish_level="verbatim"`.
  Smith voluntarily disclosed; verbatim chain preserved.
- `kiran_triplet_proof_audit.py`: all Decisions remain `publish_level="summary"`.
  HISTORY.md and rebuild_notes.md are the author-curated record.
- Both `main()` functions now emit two artifacts:
  - `<name>_audit.json` — internal artifact (adapter-redacted content for
    redact=True extractions; hand-written content otherwise).
  - `<name>_audit_published.json` — produced via `.to_published()`.
    Strips content for non-verbatim decision chains.

### Tests

- 7 new tests in `tests/test_meta_schema.py::TestPrivacyPosture` cover
  hash auto-computation, redacted form, structural-empty form, default
  publish_level, to_published behaviour (verbatim chain vs. summary),
  author-field preservation, and the version constant.
- 4 new tests in `tests/test_adapters.py` cover `redact=True` (default)
  and `redact=False` for both adapters.
- All 36 tests pass.

### Docs

- `README.md` gains a "Privacy posture (v0.2)" section.
- `CLAUDE.md` gains a top-level "Constitutional principle" section
  above "Strategic decisions"; the first strategic decision is
  reframed as "Reproducibility verification, not workflow surveillance."
- `NEXT.md (c.8)` notes that the v0.2.0 bump went to privacy and
  that (c.7)'s `evidence_fingerprint` and per-delta-evidence_ids
  refinements are now v0.3 candidates.

### Not changed (deliberately)

- `SchemaDelta`, `Claim`, `Evidence`, `Actor`, `SourceRef`,
  `CaptureTier`, `VerificationStatus`, `ActorType`, `AdapterUsage`,
  `validate_integrity()` — unchanged.
- Existing audit example structures (counts, decisions, evidence
  topology) — unchanged. Only `publish_level` and the additional
  published-artifact output are new.

## v0.1.0 — 2026-05-10

Initial release. Meta-schema only (entity types, validation, versioning).
Adapter interface defined; `claude_code`, `codex`, `aider` adapter
implementations land alongside. Two retrospective audits:
`smith_2026_audit` (J. Chem. Educ., podcast paper) and
`kiran_triplet_proof_audit` (JME submission).
