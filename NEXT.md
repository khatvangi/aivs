# NEXT — build order

This release (v0.1.0) ships the **meta-schema only**. The remaining pieces, in
the order committed in the design conversation:

## (b) v0.1 vocabulary — derived from a real audit

Run the audit pipeline (manually, by hand, with Claude Code) against one of
your published or in-progress protein design / MD papers. As decisions surface,
record the recurring `decision_type` candidates as schema deltas. Promote the
deltas that survive across two or more papers into the v0.1 vocabulary.

Do not pre-author a vocabulary. The point of "descriptive, not prescriptive"
is that vocabulary content is empirical, not speculative.

Anticipated v0.1 candidates from MD / protein design (only ones that actually
appear should be promoted):

- `force_field_selection`
- `water_model_selection`
- `simulation_length_choice`
- `replica_count_choice`
- `clustering_method_choice`
- `outlier_exclusion`
- `structure_starting_model`
- `prompt_for_code_generation`
- `prompt_for_methods_text`
- `model_choice_for_design` (e.g. ProteinMPNN, RFdiffusion, AlphaFold)
- `metric_choice_for_evaluation`

## (c) Schema-delta governance protocol

Out of scope for v0.1. The data structure exists (`SchemaDelta`); the
adjudication workflow does not. When you have ~20 deltas to triage, design the
governance pattern then. Likely shape: maintainer review, pull-request-style
proposals, semver bumps to `vocabulary_version` on accept, deprecation for
merged terms.

Reference patterns: Bioconductor package review, Zenodo community curation,
Gene Ontology term submission. Lightweight, not a foundation.

## (c.5) v0.2 meta-schema refinements informed by PROV-AGENT alignment

See `docs/positioning/prov-agent-alignment.md`. Candidate refinements (none
breaking; introduce as optional fields then deprecate fallbacks):

1. Promote `AIModel` to a first-class entity with typed fields (`provider`,
   `name`, `version`, `parameters`).
2. Add `AIModelInvocation` activity type grouping `Prompt` + `Response` +
   `AIModel`.
3. Add `AgentTool` activity type for tool calls in agentic settings (Claude
   Code's bash/edit/search; CrewAI/LangChain tool calls).
4. Adopt PROV relationship names (`used`, `wasGeneratedBy`, `wasAttributedTo`,
   `wasAssociatedWith`, `wasInformedBy`) as the canonical internal vocabulary
   for relations.

Do these after the first retrospective audit run, not before — the audit will
reveal which refinements actually matter in practice.

## (c.6) v0.2 adapter refinements surfaced by triplet-proof real-data run

The `claude_code_adapter` smoke-run against `/storage/kiran-stuff/triplet-proof`
on 2026-05-11 surfaced three event types currently in
`_SKIP_EVENT_TYPES` that are candidates for explicit modeling:

- `permission-mode` (74 lines in the 3-session triplet-proof corpus).
  Records the user toggling between `default`, `plan`, `acceptEdits`, and
  `bypassPermissions`. Arguably a **meta-decision**: choice of *how* to
  run Claude Code on a given task. Belongs as a typed `Event` with
  `action="permission_toggle"` and `actor=human`. May also warrant a
  first-class `Decision` candidate `decision_type=execution_mode_choice`
  when it surfaces repeatedly in an audit.
- `file-history-snapshot` (54 lines). Claude Code's internal pre/post
  edit snapshots used for revert. Probably stays skipped, but worth a
  comment explaining that the data is recoverable from the snapshot
  field if a redaction-resistant audit ever needs it.
- `system` (45 lines). System messages (session start banners, error
  prompts). Most are noise; a small subset (compaction events) might be
  worth surfacing as `Event(action="context_compacted", actor=system)`.

Defer until at least one more audit (probably the VeRNET enzyme-design
paper) confirms whether these patterns recur. Don't expand the adapter
schema for a single corpus.

## (d) AuditArtifact serialization to RO-Crate / PROV-O

The internal Python representation is stable. Layer an exporter that writes
the artifact as an RO-Crate (`ro-crate-metadata.json`) with PROV-O annotations
on the entity graph. Use the `rocrate-py` library; do not reinvent.

Mapping sketch:
- `Event` → `prov:Activity`
- `Actor` → `prov:Agent`
- `Decision` → `prov:Activity` with custom `aivs:decisionType`
- `Evidence` → `prov:Entity`
- `Claim` → `prov:Entity` with `aivs:manuscriptLocation`
- `wasGeneratedBy`, `wasAttributedTo`, `used` for the relations

## Adapter implementations (parallelizable; v1 scope)

In rough priority for your stack:

1. `manual_log_adapter` (universal Tier-0 fallback; simplest)
2. `git_adapter` (commits, diffs, messages → events)
3. `claude_code_adapter` (session JSONL → prompt/generate events)
4. `jupyter_adapter` (cell history → run/edit events)
5. `latex_adapter` (manuscript parser for the Manuscript Anchor agent)
6. `slurm_adapter` (job submissions → execute events)
7. `conda_adapter` (env exports → tier-3 metadata)

Each adapter is a separate concrete subclass of `EvidenceAdapter`. The contract
is fixed; implementations don't need cross-coordination.

## Agent prompts

After at least the Workflow Extractor (Adapter Layer) and the LaTeX adapter
exist, write the prompt scaffolds for:

1. **Decision Surfacer** — input: normalized event stream; output: list of
   Decision candidates with linked Evidence.
2. **Manuscript Anchor** — input: parsed manuscript + decision list; output:
   Claim list with upstream_decision_ids populated.
3. **Audit Assembler** — input: events, evidence, decisions, claims; output:
   AuditArtifact JSON; runs `validate_integrity()` and emits any
   non-classifiable decisions paired with `SchemaDelta` proposals.

Do not write agent prompts before adapters exist; without a normalized input,
the prompts cannot be specified concretely.

## Validation case

The first complete pipeline run is against one of your own published papers,
with full retrospective access to logs. This is the empirical foundation for
v0.1 vocabulary and the smoke test for the whole architecture. Do this run
before adding a second domain or recruiting external contributors.
