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

## Current scope (v0.2.1)

Meta-schema version **0.2.0**; vocabulary version **0.1.0**; package release
tag `v0.2.1-paper`.

Shipped:

- the meta-schema — entity types, relationships, cross-field invariants and
  referential-closure validation (`src/aivs/meta_schema/core.py`)
- three evidence adapters — `claude_code` (reference implementation, reads
  Claude Code session JSONL), `aider` (markdown chat-history parser),
  `codex` (detect-only stub) — behind a registry and a `discover_adapters()`
  entry point
- JSON Schema exports for both meta-schema versions (`schema/`)
- four completed audits of real published or submitted work, with their
  emitted audit artifacts under `examples/out/` (see **Audit records** below)

Still out of scope: manuscript parsers, agent prompts, RO-Crate / PROV-O
serialization, and the governance protocol for schema deltas.

The v0.1 vocabulary remains deliberately near-empty. Vocabulary content is
generated from real audits, not authored in advance; terms appearing in two or
more independent audits are promotion candidates for v0.2.

## Audit records

Four audits are included, each as a runnable script under `examples/` and as
emitted artifacts under `examples/out/`. Each audit emits two files: the full
record, and the `_published` subset that honours the per-Decision
`publish_level` (see **Privacy posture**).

| Audit | Script | Published record | Tier | Events | Decisions | Claims |
|---|---|---|---:|---:|---:|---:|
| **mechanism_classifier** — the AIVS-VAR manuscript case study | `examples/mechanism_classifier_audit.py` | `examples/out/mechanism_classifier_audit_published.json` | 2 | 22 | 8 | 4 |
| Smith 2026 (doi:10.1021/acs.jchemed.5c01652) | `examples/smith_2026_audit.py` | `examples/out/smith_2026_audit_published.json` | 3 | 12 | 11 | 5 |
| triplet-proof (JME submission) | `examples/kiran_triplet_proof_audit.py` | `examples/out/kiran_triplet_proof_audit_published.json` | 3 | 532 | 14 | 7 |
| kappa_friction (JPCB submission) | `examples/kappa_friction_audit.py` | `examples/out/kappa_friction_audit_published.json` | 3 | 380 | 10 | 7 |

**If you arrived here from the AIVS-VAR manuscript**, the verification record
for its §4 case study is
[`examples/out/mechanism_classifier_audit_published.json`](examples/out/mechanism_classifier_audit_published.json),
generated by [`examples/mechanism_classifier_audit.py`](examples/mechanism_classifier_audit.py).
The full (unredacted-subset) record is
`examples/out/mechanism_classifier_audit.json`. The data and analysis code
that record audits are in the companion repository
<https://github.com/khatvangi/idp-mechanism-classifier>
(concept DOI [10.5281/zenodo.20723560](https://doi.org/10.5281/zenodo.20723560)).

Regenerate any record with, e.g.:

```bash
python -m examples.mechanism_classifier_audit
```

Regeneration reproduces the record's *structure and content* exactly — same
events, decisions, claims, evidence and schema deltas — but not its bytes:
`audit_id` and every `event_id` / `evidence_id` / `decision_id` are fresh
`uuid4()` values on each run. Compare regenerated records by content, not by
checksum. Making identifiers deterministic (content-addressed rather than
random) is an open item for a future schema version.

## Archived releases

| DOI | Resolves to |
|-----|-------------|
| [10.5281/zenodo.20723558](https://doi.org/10.5281/zenodo.20723558) | concept DOI — always the latest version |
| 10.5281/zenodo.20723559 | version DOI, release `v0.2.1-paper` (2026-06-16) |

Cite the concept DOI unless you need a specific version.

## Repository layout

```
src/aivs/
├── meta_schema/          # entity types, relationships, validation, versioning
├── vocabulary/           # open vocabulary; accretes from audits
└── adapters/             # base + claude_code, aider, codex implementations
examples/                 # runnable audits; emitted artifacts in examples/out/
schema/                   # JSON Schema exports (0.1.0, 0.2.0)
docs/                     # positioning, design origins, case-study sources
tests/                    # schema integrity and round-trip tests
```
src/aivs/
├── meta_schema/          # entity types, validation, versioning
├── vocabulary/           # open vocabulary; accretes from audits
└── adapters/             # adapter interface (no implementations yet)
tests/                    # schema integrity and round-trip tests
```

## License

AGPL-3.0-or-later. See `LICENSE`.
