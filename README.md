# AIVS — AI-Integrated Verification System

Descriptive (not prescriptive) audit of AI-mediated research workflows.
AIVS reads what's there, verifies what evidence supports, and emits both an
audit artifact and proposed extensions to its open vocabulary.

## Design stance

- **Verification, not disclosure.** Inspect actual research artifacts (git,
  chat logs, notebooks, env exports, manuscript) rather than structuring
  self-reported claims.
- **Decision points** are the unit of audit. Workflow tasks are evidence below;
  manuscript claims are outcomes above.
- **Author-side, retrospective.** Run AIVS against your own published work.
  No coupling to journal acceptance — the ASRS-style independence principle.
- **Adapter-based capture.** Heterogeneous workflows are absorbed by pluggable
  adapters. Same downstream pipeline regardless of source.
- **Capture tiers (0–3).** Audits are honest about evidence fidelity. Lower
  tiers are valid; the audit reports the tier it achieved.
- **Open vocabulary, closed meta-schema.** The meta-schema (entity types and
  relationships) is small, stable, versioned. The vocabulary (decision types,
  evidence types) is open and accretes from real audits.
- **Honest omission.** Decisions with no evidence are marked `no_evidence`;
  patterns the vocabulary can't classify are marked `schema_gap: novel_pattern`.
  AIVS does not interpolate or force-fit.

## Privacy posture (v0.2)

**Minimum capture for purpose.** AIVS's published audit resolution matches
the audit's stated purpose. For tool use and reproducibility, that means:
which tools were used, at which consequential decisions, what artifacts
(code, data, configs, environment) regenerate the work. Verbatim content —
prompts, AI outputs, tool results, thinking blocks, intermediate
exploration — is **private by default**.

Adapters (e.g., `claude_code`, `aider`) run in `redact=True` mode by
default: emitted events carry an SHA-256 `content_hash` but no `content`.
The hash demonstrates the event existed and, if a specific claim is ever
actively disputed, the author can produce the original content and have it
verified against the hash recorded in the audit. The minimum-capture
default never publishes the original.

Authors opt into verbatim publishing **per Decision** by setting
`publish_level="verbatim"` on Decisions where verbatim content is itself
the deliverable. The `Smith 2026` audit example marks D3/D5/D9 verbatim
because the chat history was Smith's voluntary disclosure (the prompts
and AI outputs *are* the contribution). The `triplet-proof` audit example
marks no decisions verbatim — author-curated `HISTORY.md` and
`rebuild_notes.md` provide the human-readable record; the audit itself
publishes only hashes for adapter-extracted events.

AIVS deliberately does not recapitulate the disclosure-maximalist impulse
of CONSORT-AI / SPIRIT-AI / ICMJE. Those standards implicitly treat AI use
as more suspicious than human collaboration; AIVS rejects the asymmetry.
Tool use accounting and reproducibility are reasonable asks; demanding
every prompt is not.

## Positioning

AIVS occupies the layer between trust-based disclosure (current journal /
funder policy) and real-time agentic provenance (ORNL's PROV-AGENT, Souza et
al. 2025). It is descriptive rather than prescriptive, retrospective rather
than real-time, and anchored to scientific manuscripts rather than to
workflow execution graphs. AIVS adopts PROV-compatible terminology and can
optionally consume Flowcept-generated provenance as evidence. See
[`docs/positioning/prov-agent-alignment.md`](docs/positioning/prov-agent-alignment.md)
for the full technical alignment.

## Current scope (v0.1.0)

This release ships the **meta-schema only**: the entity types, relationships,
and validation logic that all audits will share. The v0.1 vocabulary file is a
placeholder; vocabulary content is generated from real audits, not authored in
advance.

Out of scope here: adapter implementations, manuscript parsers, agent prompts,
RO-Crate / PROV-O serialization, governance protocol for schema deltas. Each
follows in its own pass.

## Repository layout

```
src/aivs/
├── meta_schema/          # entity types, validation, versioning
├── vocabulary/           # open vocabulary; accretes from audits
└── adapters/             # adapter interface (no implementations yet)
tests/                    # schema integrity and round-trip tests
```

## License

AGPL-3.0-or-later. See `LICENSE`.
