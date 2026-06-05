# AIVS Chat Handling Protocol

**Version:** 0.1 (draft)
**Status:** Canonical spec for chat-history evidence under the AIVS framework.

## Scope

This protocol governs how AI chat history (claude.ai, ChatGPT, Gemini, or any
other interactive AI interface) enters AIVS as audit evidence. It applies the
same materiality and privacy discipline as the rest of the framework, adapted
to the structural differences of chat data.

## Provider-agnostic

The protocol treats all chat providers uniformly. The `provider` field in each
register entry names the source; behavior does not branch on it.

## Materiality classification

Each chat segment relevant to a project receives one of four labels:

- **Material**: the segment produced a specific decision, code edit, manuscript
  change, observable choice, retraction, claim revision, or other output
  captured as a Decision or Claim in the project's AIVS audit. Material
  segments get full register entries with cross-reference to Decision/Claim
  IDs.
- **Background**: the segment shaped the author's thinking but did not produce
  a specific auditable output. One-line register entry, no excerpt, no
  cross-reference.
- **Exploratory**: tangents, dead ends, abandoned hypotheses, philosophical
  asides that touched the project without affecting it. Bulk-count entry only
  ("N exploratory exchanges within otherwise-material chat X; not enumerated").
- **Out of scope**: unrelated to the project entirely. Excluded; bulk-counted
  at register footer with date range.

Borderline cases default to *background*, not *material*. The author can
manually promote later.

## Privacy defaults (hard rules)

- No verbatim quotes longer than 15 words from chat content. Paraphrase.
- Maximum one direct quote per register entry, used only when exact wording
  carries meaning that paraphrase loses.
- No interpretation of the author's tone, mood, or psychological state. Stick
  to factual content.
- Chats containing mixed material and personal/off-topic content: extract only
  the material slice. Do not summarize the rest.
- Failed attempts and abandoned ideas are private unless they produced a
  decision in the published work.

## Register format

Per-project `chat_register.md`, append-only, dated entries. Permanent numbering
(`CR001`, `CR002`, ...) — never renumbered when new entries arrive. Each
material entry contains:

- `chat_id` (opaque identifier or URL)
- `provider`
- date range
- topic one-liner
- materiality label
- cross-references to Decision/Claim IDs
- paraphrased excerpt ≤80 words

## Cross-reference discipline

Every *material* register entry must link to at least one Decision or Claim ID
in the project's AIVS audit. If a chat segment is judged material but cannot
be linked to any existing audit entry, flag it as a *candidate missing
decision* in the register — these are evidence that the audit itself may be
incomplete.

## Adapter layer

- **v0.1–0.2**: chat registers are Tier-3 hand-curated evidence ingested via
  `manual_log_adapter`. No new adapter required.
- **v0.3 and beyond**: an optional `chat_export_adapter` can ingest raw chat
  exports (JSON, Markdown, HTML) with `redact=True` by default, mirroring
  `claude_code_adapter`'s bulk-reference-with-redaction pattern. The
  hand-curated register remains canonical even when an adapter is used.

## Schema entries (v0.2 candidates)

These are candidates pending empirical confirmation from at least one real
chat audit before promotion. See `NEXT.md` (c.9) for sequencing.

- New `source_type` value: `chat_session` (alongside `claude_code_session`,
  `git`, `latex_manuscript`, `data_artifact`).
- New `decision_type` value: `chat_register_curation` — the act of deciding
  what enters the register is itself an auditable Decision.
- `AuditArtifact.audit_scope` field added: declares what is excluded by
  author scoping ("private brainstorming sessions excluded; bulk reference at
  register footer").

## Recursion principle

A chat that discusses Project A goes into Project A's register. A chat that
discusses the methodology paper goes into the methodology paper's register,
not the substrate paper's register. When a single chat substantively crosses
projects, it appears in each affected register with project-scoped slicing.

## Re-auditability

The register is append-only. If new material is later identified in a chat
previously classified background or out-of-scope, a new dated entry is added;
the old entry is not rewritten. The audit JSON regenerated from the updated
register reflects the augmented evidence.

## Disclosure as positive statement

The register's footer states what was excluded by scoping ("N additional chats
spanning [date range] excluded as out-of-scope; M exploratory exchanges within
in-scope chats bulk-referenced not enumerated; private content paraphrased per
privacy discipline"). This converts absences into honest disclosure rather
than evasion.
