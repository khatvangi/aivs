# Tables

Companion document to the manuscript "Verifiable, accountable, and reproducible AI-assisted research: the VAR framework and the AIVS verification schema, demonstrated on an end-to-end protein-variant workflow" (Ribbeck and Kiran, submitted to *Patterns*).

The three tables below are also embedded in the main manuscript (§3.3, §3.4, §3.5); they are reproduced here as a separate document for production-side typesetting.

---

## Table 1

**Table 1.** AIVS record types, workflow stage, key fields, and typical cardinality per manuscript.

| Record | Workflow stage | Key fields | Cardinality |
|---|---|---|---|
| Source | Source | id, type, uri, content_hash, retrieved_at, license | One or more per workflow |
| Invocation | Generate | id, parent_id, tool, model, version, prompt, parameters, response, operator, access_date, retention_policy, purpose | One per AI call |
| Evaluation | Evaluate | id, invocation_ref, check_type, target, result, confidence, verifier, evidence_uri | Many per Invocation |
| Curation | Curate | id, invocation_refs, kept, rationale, accountable_author | One or more per workflow |
| Deposition | Deposit | id, artifact_type, uri, repository, doi, version, license, retention_policy | One per published artifact |

---

## Table 2

**Table 2.** AIVS submission-time verification checks, the failure mode each addresses, and the reviewer judgment that remains.

| Check | Failure mode addressed | Reviewer judgment retained |
|---|---|---|
| Citation resolution | Hallucinated references | Whether cited work supports the claim |
| Quote matching | Misattributed or invented quotations | Whether quoted material is interpreted accurately |
| Data retrievability | Phantom datasets | Whether data is sufficient for the claim |
| Code execution | Non-runnable analysis | Whether code implements the described method correctly |
| Image forensic analysis | Fabricated or manipulated figures | Whether figures support the textual claims |
| Schema validation | Incomplete provenance | Whether the documented workflow is appropriate |

---

## Table 3

**Table 3.** AIVS disclosure tiers, access scope, and floor fields.

| Tier | Public access | Editorial/reviewer access | Floor fields (always public) |
|---|---|---|---|
| Public | Full record content | Full record content | Model ID, version, parameters, verification results, accountable_author |
| Editorial | Existence and rationale only | Full record content | As above |
| Redacted | Redaction methodology only | Redacted content under controlled access | As above |
