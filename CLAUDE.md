# AIVS — AI-Integrated Verification System

## Working style (NON-NEGOTIABLE)

This project is run by Kiran. Working style preferences:

- **Direct.** No filler. No "great question", "absolutely", "I'd be happy to",
  "it's worth noting", "I understand your concern", or any praise of the
  question before answering. If you catch yourself writing these, delete
  them and start over.
- **Peer-level register.** Computational biology, protein design,
  molecular dynamics, Advaita Vedanta, philosophy of science — graduate-
  level literacy assumed in all of these.
- **Skepticism > agreement.** If the premise is wrong, say so. No false
  balance. Steel-man the strongest counter-argument to your own points.
- **Match length to question.** Short question, short answer. Don't pad.
- **Default to prose.** Bullet points only when data structure genuinely
  requires it. No excessive bolding or headers in conversational replies.
- **Correct errors immediately.** No social softening when Kiran is wrong.
  Same applies in reverse: when you're wrong, acknowledge and correct
  without abasement.
- **Treat HISTORY.md style Q/A as the canonical decision log format.**
  Each session ends with appending Q/A entries documenting what was
  decided and why.

## What AIVS is

Open-source descriptive audit framework for AI-mediated scientific
workflows. AGPL-3.0. Domain-first design: chemistry was the original
target; protein design / MD / computational biology became the empirical
foundation because that's Kiran's home domain and has retrospective
ground truth.

Audience: authors who want to produce machine-readable provenance for
their submitted manuscripts, *plus* journals / grant offices / integrity
offices that want to consume it.

Tagline: **"Smith voluntarily wrote what is essentially an AIVS audit
in prose. AIVS formalizes that discipline into a schema."**

## Constitutional principle (overrides defaults where they conflict)

**Minimum capture for purpose.** The audit's published resolution
matches the audit's stated purpose. For tool use and reproducibility,
that means: which tools were used, at which consequential decisions,
what artifacts (code, data, configs, environment) regenerate the work.

Verbatim content — prompts, AI outputs, tool results, thinking blocks,
intermediate exploration — is PRIVATE BY DEFAULT. Authors opt-in per
Decision to publish verbatim content where they want maximum
transparency. Smith 2026 is the exemplar of opt-in (chat history WAS
the deliverable). Otherwise, the published audit references content
by hash and summary statistic, not by quotation.

Fine-grained adapter output is diagnostic, retained locally if at
all, surfaced only if a specific claim is actively disputed.

AIVS does NOT recapitulate the disclosure-maximalist impulse of
CONSORT-AI / SPIRIT-AI / ICMJE. Those standards implicitly treat AI
use as more suspicious than human collaboration; AIVS rejects the
asymmetry. Tool use accounting and reproducibility are reasonable
asks; demanding every prompt is not.

## Strategic decisions — LOCKED. Do NOT re-litigate.

1. **Reproducibility verification, not workflow surveillance.** AIVS
   verifies that the manuscript's claims map to identifiable workflow
   decisions, that those decisions have evidence, and that the
   artifacts (code, data, env) regenerate the work. AIVS does NOT
   demand documentation of every prompt, every thought, or every
   exploratory step.
2. **Decision point is the unit of audit.** Workflow tasks anchor below,
   manuscript claims anchor above.
3. **Author-side retrospective.** ASRS-style independence. No coupling
   to journal acceptance.
4. **Descriptive, not prescriptive.** Open vocabulary, closed meta-
   schema. v0.1 vocabulary is intentionally empty. New terms accrete
   via SchemaDelta proposals from real audits. Terms appearing in 2+
   independent audits get promoted to v0.2.
5. **Adapter-based.** Each evidence source (git, Claude Code, Codex,
   Aider, Jupyter, slurm, conda env, ELN, etc.) has its own adapter
   emitting a normalized event stream. Downstream agents never see
   raw source formats.
6. **Four-agent topology.** Workflow Extractor → Decision Surfacer →
   Manuscript Anchor → Audit Assembler. Schema Validator is fifth,
   deferred.
7. **PROV-AGENT (Souza et al., IEEE eScience 2025; arXiv:2508.02866)
   is the critical prior art.** AIVS is COMPLEMENTARY, not competing:
   PROV-AGENT = real-time, workflow-anchored, HPC-instrumented capture.
   AIVS = retrospective, manuscript-anchored, author-side audit.
   AIVS adopts PROV-compatible terminology. Flowcept as evidence
   adapter is option B. Joint authorship is premature.
8. **AGPL-3.0.** Repo name `aivs`.

## Current state of the codebase

Package skeleton (lives at `/storage/kiran-stuff/aivs/`):

```
aivs/
├── LICENSE                                  AGPL-3.0 SPDX stub
├── README.md                                with PROV-AGENT positioning paragraph
├── NEXT.md                                  v0.2 candidates, build order
├── pyproject.toml                           pydantic>=2.6, hatchling
├── docs/
│   ├── positioning/prov-agent-alignment.md  AIVS ↔ PROV-AGENT
│   ├── origins/                             design history (primary sources)
│   │   ├── brainstorming-session.md         early strategic framing
│   │   ├── design-conversation.md           main design conversation; primary source of the 7 adapter files
│   │   └── distribution-archives/           original v0.1.0 distribution zips (forensic)
│   └── case_studies/                        source PDFs cited by audit examples
│       ├── smith_2026_jce_main.pdf
│       └── smith_2026_jce_si.pdf
├── examples/
│   ├── minimal_audit.py                     synthetic demo
│   ├── smith_2026_audit.py                  first real audit
│   ├── kiran_triplet_proof_audit.py         second real audit
│   ├── kappa_friction_audit.py              third real audit (v0.2-native)
│   └── run_claude_code_adapter.py           adapter demo
├── schema/audit_artifact-0.1.0.json         JSON Schema export
├── src/aivs/
│   ├── meta_schema/
│   │   ├── __init__.py
│   │   └── core.py                          Pydantic models, META_SCHEMA_VERSION="0.1.0"
│   ├── vocabulary/
│   │   ├── __init__.py
│   │   └── v0_1.py                          empty except "unclassified" reserved
│   └── adapters/
│       ├── __init__.py                      registers concrete adapters
│       ├── base.py                          ABC + registry
│       ├── claude_code.py                   REFERENCE IMPL
│       ├── codex.py                         stub (no real data on machine)
│       └── aider.py                         minimal parser stub
└── tests/
    ├── test_meta_schema.py                  15 passing
    └── test_adapters.py                     8 cases
```

## Meta-schema reference

`src/aivs/meta_schema/core.py` defines (Pydantic v2):

Closed enums:
- `ActorType`: HUMAN, AI_ADVISORY, AI_GENERATIVE, AI_AUTONOMOUS, SYSTEM, UNKNOWN
- `CaptureTier`: TIER_0 (manual log only), TIER_1 (+ VCS/notebooks),
  TIER_2 (+ AI logs), TIER_3 (+ env metadata)
- `VerificationStatus`: VERIFIED_INDEPENDENTLY, VERIFIED_PARTIALLY,
  UNVERIFIED, NO_EVIDENCE, NOT_APPLICABLE
- `EvidenceConfidence`: HIGH, MEDIUM, LOW, NONE
- `SchemaDeltaKind`: DECISION_TYPE, ACTOR_SUBTYPE, EVIDENCE_RELATION,
  ACTION_TYPE
- `SchemaDeltaStatus`: PROPOSED, ACCEPTED, MERGED_INTO, REJECTED, DEPRECATED

Core types: `SourceRef`, `Actor`, `Event`, `Evidence`, `Decision`,
`Claim`, `SchemaDelta`, `AdapterUsage`, `AuditArtifact`.

Cross-field invariants (validated):
- `decision_type="unclassified"` ↔ `schema_gap="novel_pattern"`
- `SchemaDeltaStatus.MERGED_INTO` ↔ `merged_into` target required

`AuditArtifact.validate_integrity()` checks referential closure
(every evidence_id, decision_id, event_id reference resolves).

## Completed audits

### Audit 1 — Smith 2026 JCE

Target: doi:10.1021/acs.jchemed.5c01652
File: `examples/smith_2026_audit.py` → `smith_2026_audit.json` (~38 KB)
12 events, 13 evidence, 11 decisions, 5 claims, 9 schema deltas.
Tier 3 capture (Smith's voluntary SI included full AI chat history).

Vocabulary candidates surfaced: tool_selection_via_ai,
source_material_selection, source_material_revision, prompt_engineering,
iterative_ai_generation, ai_error_disposition,
content_curation_from_multiple_ai_outputs, ai_assisted_transcription,
human_authored_supplementary_visual.

### Audit 2 — Kiran's triplet-proof (JME submission)

Target: `/storage/kiran-stuff/triplet-proof` @ git origin/main 41c451b
File: `examples/kiran_triplet_proof_audit.py` → `kiran_triplet_proof_audit.json` (~49 KB)
15 events, 10 evidence, 14 decisions, 7 claims, 11 schema deltas.

Three Claude Code session JSONLs (8.1 MB total) referenced as bulk
evidence — fine-grained event extraction is the next deliverable now
that the adapter is in place.

Vocabulary candidates surfaced (additional to Smith):
target_journal_change, prior_art_verification, factorial_cell_exclusion,
sensitivity_protocol_revision, manuscript_internal_discrepancy_disposition,
defensive_metric_precomputation, repository_consolidation_for_submission,
figure_panel_authorship_split, design_decision_documentation_via_qa_log,
introduction_repositioning, vocabulary_term_recurrence_signal.

**Three terms appear in BOTH audits in structurally similar form**
(promotion candidates for v0.2): prompt_engineering, iterative_ai_generation,
internal_discrepancy_disposition.

## Pending TODOs on triplet-proof (BLOCKING submission)

These are flagged in `kiran_triplet_proof_audit.json` as decisions with
`verification_status="unverified"`. The audit closes when these close:

1. **Introduction rewrite** — cite Tlusty 2007, Tlusty 2010, Radvanyi
   & Kun 2021. Frame contribution as factorial + empirical null, NOT
   novel metrics. Guidance in `literature_comparison.md`.
2. **Methods prose fix** — replace "sensitivity <0.5 units" with
   actual ranges: D = 0.56 units, E = 0.92 units (from 3-seed random
   protocol). Draft wording in `rebuild_notes.md`.
3. **Fig 1c prose fix** — "‖Δf‖ = 8.7 for radical" is impossible
   (max pairwise PC distance = 6.23, G-P). Either update to actual
   Ala-neighborhood values (0 / 3.5-4.9) or swap to a real radical
   pair (G-P @ 6.23 or E-P @ 5.81).
4. (Optional) Hand-draw Fig 1 panels (a) and (c) in Illustrator/Inkscape.
5. Submit.

## Adapter layer

`base.py` — `EvidenceAdapter` ABC plus `register_adapter`,
`registered_adapters`, `discover_adapters(project_path)`.

`claude_code.py` — full reference implementation. Reads
`~/.claude/projects/<path-hash>/*.jsonl`. Path hash is the absolute
project path with `/` → `-`. Handles event types: queue-operation
(skipped), attachment (hooks at verbosity=verbose), user (string
prompt OR list of tool_result), assistant (text / thinking /
tool_use), last-prompt (skipped). Three verbosity levels: summary,
default, verbose.

`codex.py` — stub. `.codex` directory on Boron is a 0-byte file, not
a directory; no real data to map against. Detect-only.

`aider.py` — minimal markdown parser for `.aider.chat.history.md`.
Tier 1 capture (lower fidelity than JSONL).

`tests/test_adapters.py` — 8 tests using synthetic JSONL fixtures
written to `tmp_path`. Tests don't depend on real machine state.

## Validation sequence (run on first session)

```bash
cd /storage/kiran-stuff/aivs

# Sanity: meta-schema tests
python -m pytest tests/test_meta_schema.py -v
# Expect: 15 passed

# Adapter tests
python -m pytest tests/test_adapters.py -v
# Expect: 8 passed. If any fail, fix before proceeding.

# Both audits should still run
python -m examples.smith_2026_audit
python -m examples.kiran_triplet_proof_audit
# Each should print "integrity: OK" and counts matching the documented numbers.

# Real-data validation: claude_code adapter against triplet-proof
python -m examples.run_claude_code_adapter \
  /storage/kiran-stuff/triplet-proof --verbosity default
# Expect: thousands of events (the 7.9 MB JSONL alone is ~10K-50K events).
# Verify the time range spans the documented sessions
# (2026-04-14 to 2026-04-22).
```

## High-leverage next tasks (in order)

1. **Validate adapter layer.** Run pytest + smoke-test against
   `/storage/kiran-stuff/triplet-proof`. Spot-check that prompts,
   tool uses, and tool results are correctly classified.

2. **Re-run kiran_triplet_proof_audit with adapter-derived events.**
   Replace the three `session_bulk_reference` events with the real
   event stream. Each Decision's `evidence_ids` should now point to
   specific event UUIDs rather than to "session 101e5996..." bulk
   references. Audit integrity should still pass.

3. **Help Kiran close the three triplet-proof TODOs** and submit.

4. **Then, and only then:** v0.2 schema work. Candidates (from
   PROV-AGENT alignment + audit feedback):
   - AIModel as first-class typed entity (replace
     `Actor.model_metadata: dict`)
   - AIModelInvocation activity type
   - AgentTool activity type
   - Adopt PROV relationship names (wasGeneratedBy, used,
     wasInformedBy)
   - `Event.timestamp_precision: known | approximate | sequence_only`
   - `Decision.verification_mode: domain_expertise_self |
     domain_expertise_peer | empirical_test | replication |
     external_benchmark | none`

## Design principles — internalize these

- **Honest-omission.** Gaps are first-class. An audit that omits a
  decision is FAR worse than one that surfaces "we made a decision
  here but didn't document the rationale."
- **Closed schema, open vocabulary.** The meta-schema (entities,
  fields, enums) is governance-controlled and slow to change. The
  vocabulary (decision_type strings, action strings) is data and
  evolves audit-by-audit.
- **Tier honesty.** Tier 0-3 reflects what evidence the auditor
  *actually has*. Don't inflate tier just because the project is
  capable of better capture.
- **Adapters are dumb.** Adapters emit events. They don't reason,
  don't classify decisions, don't make verification judgments.
  Reasoning lives in the four-agent layer above.
- **Verification ≠ third-party verification.** A `verified_independently`
  decision means the author checked independently of the AI output
  (e.g., domain expertise check, recomputation). It does NOT mean a
  third party verified it. The `verification_mode` enum (v0.2) will
  make this precise.
- **Don't theorize ahead of evidence.** The vocabulary terms surface
  from real audits. Don't pre-author terms. If a term seems obvious
  but hasn't appeared in an audit, leave it out.

## Prior art Claude Code should know about (don't re-search)

- **PROV-AGENT** (Souza et al., IEEE eScience 2025; arXiv:2508.02866;
  Flowcept at github.com/ORNL/flowcept) — critical prior art. AIVS is
  retrospective + manuscript-anchored; PROV-AGENT is real-time +
  workflow-anchored. Complementary.
- **CONSORT-AI / SPIRIT-AI / ICMJE / COPE / Nature** — disclosure
  standards. AIVS does NOT compete here.
- **ASRS (Aviation Safety Reporting System)** — author-side
  independent reporting model. AIVS borrows the structural idea.
- **TOP (Transparency and Openness Promotion)** — adjacent norms;
  not directly relevant but worth knowing.
- **NIH (Sept 25, 2025)** — application policy: rejects work
  "substantially developed by AI." 6-app-per-PI cap. AI prohibited
  in peer review. Enforcement unclear. Creates demand for
  originality-defense tools (AIVS-adjacent use case).
- **NSF** — disclosure-encouraged, not prohibited.

## What NOT to do

- Don't re-debate the strategic decisions. They're locked.
- Don't add new audits before the adapter is validated. The
  marginal value of audit #3 is small; adapter validation is high.
- Don't write code without tests.
- Don't soften the no-sycophancy rules.
- Don't ask permission for small things (creating files in the
  package, running pytest, etc.) — just do them. Ask for input
  on substantive decisions: schema changes, vocabulary promotions,
  submission-blocking issues.
- Don't pretend to have run code you haven't run. If something is
  drafted but unvalidated, say so.

## Communication norms with Kiran

- Mobile/voice dictation: typos are frequent. Read charitably.
- Forward motion preferred: "yes", "good", "proceed" means execute.
- Course corrections will be direct ("no, I meant X" — accept and
  pivot, don't apologize).
- HISTORY.md-style Q/A append at the end of each substantive session.
- Default deliverable format: actual files in the repo + brief
  prose summary of what was done. Not lengthy reports.
