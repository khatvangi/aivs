# AIVS Origins

Primary source material for the framework's design history. These files
predate the v0.1.0 code release and contain the conversational record
in which the meta-schema, adapter layer, and audit pattern were worked
out.

## Contents

### `brainstorming-session.md` (89 KB)

Early-stage design discussion. Strategic framing: pushback on
locked decisions, the verification-vs-disclosure choice, the
decision-point-as-unit-of-audit argument, the four-agent topology, the
ASRS independence principle, the PROV-AGENT positioning. No code.

### `design-conversation.md` (137 KB)

Main design conversation (Claude.ai chat thread, 2026-05-09 to
2026-05-11). The primary source for:

- Meta-schema design (entity types, enums, validators)
- Capture-tier honesty (Tier 0–3) and the open-vocabulary /
  closed-meta-schema split
- Adapter layer specification including the 7 code files for
  `claude_code.py`, `codex.py`, `aider.py`, `tests/test_adapters.py`,
  `examples/run_claude_code_adapter.py`, and the updates to `base.py`
  and `adapters/__init__.py`. **These files were extracted from this
  document and written to disk in commit `a756104`** ("Initial AIVS
  v0.1.0 + adapter layer dropped from chat history"). The design
  conversation is the only verbatim source of the original adapter-
  code listings; if a future migration ever needs to compare the
  delivered code against the conversation-time design, this is the
  primary record.
- Smith 2026 (JCE podcast paper) audit construction
- Triplet-proof (JME submission) audit construction
- Kappa-friction (JPCB submission) audit construction
- The 2026-05-11 v0.2.0 constitutional fix (minimum-capture-for-purpose
  default, privacy posture)

### `distribution-archives/`

The three original distribution zips, exactly as they were when the
v0.1.0 package was first delivered. Each zip contains the
`aivs-0.1.0.tar.gz` package plus (where applicable) the
audit-script/audit-JSON pair for that audit.

- `aivs-0.1.0.zip` — canonical release bundle
- `kiran-triplet-audit-0.1.0.zip` — tarball + the manual triplet-proof
  audit script and its JSON output
- `smith-audit-0.1.0.zip` — tarball + the manual Smith-2026 audit
  script and its JSON output

These are redundant with git history at commit `a756104`; they are kept
here for forensic completeness ("what was originally distributed?").
Future-state code lives in the working tree, not in these zips.
