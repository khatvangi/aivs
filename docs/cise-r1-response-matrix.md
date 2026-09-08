# CiSE-2026-06-0105: Response to Reviewers (working matrix)

**Manuscript:** "Auditing AI-Assisted Research: The VAR Framework and AIVS Schema"
**Venue:** IEEE Computing in Science & Engineering
**Decision date:** 2026-08-27
**Revision due:** 2026-09-22
**Reviewer recommendations:** R1 major revision; R2 reject; R3 major revision; R4 major revision; R5 reject

Note: the Associate Editor's referenced PDF attachment does not exist in ScholarOne. The emailed decision letter and the Research Exchange rendering were both checked on 2026-08-30; no file is present. The revision proceeds on the five reviewer reports.

## Gates

Three gates blocked eleven rows. Blocked rows carried the gate name in the Status column, prefixed with the character U+29D7 (⧗). All three were resolved on 2026-08-30; no row is now blocked. The blocked-row lists are retained below as an audit trail.

### GATE-SCHEMA

**To decide:** whether Section 3 is respecified to the built kernel (Actor / Event / Evidence / Decision / Claim / AuditArtifact, as implemented in `src/aivs/meta_schema/core.py`) instead of the five record types currently written (Source / Invocation / Evaluation / Curation / Deposition), which were never implemented. Recommended: respecify to the built kernel, which is Reviewer 3's own second proposed option.
**Resolved by:** author decision (Kiran).
**Resolution (2026-08-30):** Option A selected. Section 3 is respecified to the built kernel (Actor, Event, Evidence, Decision, Claim, AuditArtifact, as implemented in `src/aivs/meta_schema/core.py`). The five previously specified record types (Source, Invocation, Evaluation, Curation, Deposition) are demoted to open-vocabulary decision-type terms. No new schema code is built. This is Reviewer 3's second proposed option.
**Blocked rows (audit trail):** 1.1, 2.1, 2.3, 3.1, 5.2.
**Status:** RESOLVED.

### GATE-COST

**To find:** person-hours for the audit compared with person-hours for the pipeline. Claude Code session logs for both projects were destroyed by default retention (verified absent 2026-08-27, session 7cfde9e909d0; see `docs/audit-cost-summary.md`). Cost must therefore come from an author estimate reported at capture tier 0, unless the access-controlled session-log deposit referenced at manuscript line 105 turns out to exist.
**Resolved by:** author estimate (Kiran), contingent on checking the access-controlled deposit.
**Resolution (2026-08-30):** Author estimates reported at capture tier 0. Pipeline development approximately 520 person-hours (6 months at roughly 20 h/week, variant curation through first draft of results); retrospective audit approximately 60 person-hours (4 weeks at roughly 15 h/week, covering the 2026-02-20 code and logic pass, the 2026-03-16 numerical pass, the resulting corrections, and construction of the AIVS record). Audit overhead approximately 12 percent, roughly one hour of checking per eight hours of development. These are estimates, not measurements: the coding-assistant session logs that would have measured them were destroyed by default tool retention, verified absent 2026-08-27 (`docs/audit-cost-summary.md`). The contingency is closed by GATE-DEPOSIT: the access-controlled deposit does not exist.
**Blocked rows (audit trail):** 1.4, 2.2, 3.3.
**Status:** RESOLVED.

### GATE-DEPOSIT

**To find:** what the two Zenodo deposits actually contain, compared with what the Data Availability statement claims. R3 reported four listed items missing; R5 reported the same failure independently.
**Resolved by:** author verification of both deposits, then correction of the deposits before the statement.
**Resolution (2026-08-30):** Resolved as a finding; see `docs/deposit-verification-2026-08-27.md`. Both reviewers were factually correct. Figure-generation scripts and the environment manifest are absent from the idp deposit; the AIVS verification record is misplaced in the aivs deposit; the variant dataset is stale; analysis scripts are 12 of 21. The idp deposit is frozen at commit 3ca6dead, 132,669 insertions behind the described work, and that commit is not an ancestor of local HEAD. The access-controlled session-log deposit claimed at manuscript line 105 does not exist. Repair requires a new tagged release and a new Zenodo version DOI; concept DOIs remain stable. Fifteen corrections enumerated, ten blocking.
**Blocked rows (audit trail):** 3.6, 3.7, 5.1.
**Status:** RESOLVED.

## Status

Counts as of 2026-09-08, after gate resolution and the addition of row 3.10:

- Total rows: 41 (Reviewer 1: 7; Reviewer 2: 5; Reviewer 3: 11; Reviewer 4: 6; Reviewer 5: 11; Associate Editor: 1).
- DRAFTED: 6.
- OPEN: 35.
- Blocked: 0.

## Reviewer 1 (major revision)

| ID | Comment (condensed) | Response | Change (location) | Status |
|---|---|---|---|---|
| 1.1 | Record types do not map to files in the Zenodo repos; how is Fig 1 instantiated for the case study? | Accept. The specified types were never instantiated. | Section 3 respecified to built kernel; Fig 1 redrawn; new Table 2 mapping kernel records to deposited files | OPEN |
| 1.2 | Section 4.1 workflow description inaccessible to researchers from other domains | Accept | Section 4.1 rewritten in plain terms | DRAFTED |
| 1.3 | Script numbers (e.g. "Script 04") meaningless; suggests a workflow figure with named analysis tasks | Accept | New Table 1 with named stages S1-S5; Section 4.2 references stage names not script numbers | DRAFTED |
| 1.4 | How long did the manual audit take compared with the agentic workflow itself? | Accept | New cost paragraph in Section 4.5 | OPEN |
| 1.5 | Section 4.4 needs context for non-experts; Figure 2 is never referenced in the text; what is the significance of the numerical results? | Accept | Section 4.4 gains an interpretive lead sentence; Fig 2 cited at first mention; numbers moved to a table | OPEN |
| 1.6 | Include references for the minimum information standards named in Section 3 (MIAME, MIQE, ARRIVE) | Accept | Three references added at Section 3 opening; references [9] and [10] cut to stay within the 12-reference limit | OPEN |
| 1.C5 | Organization could be improved | Accept; addressed via rows 1.1-1.3 | No separate change | OPEN |

## Reviewer 2 (reject)

| ID | Comment (condensed) | Response | Change (location) | Status |
|---|---|---|---|---|
| 2.1 | Section 3 AIVS schema difficult to understand; unclear how it could be implemented in a general research workflow | Accept. Root cause is the same defect as row 3.1. | Section 3 respecified; capture tier foregrounded as the adoption gradient | OPEN |
| 2.2 | Section 3 leaves out an implementation discussion covering impact and level of effort required to use | Accept. This is central to this reviewer's reject recommendation. | New Section 3.2 specifying capture tiers 0-3; new cost paragraph in Section 4.5 | OPEN |
| 2.3 | Unclear how AIVS was actually used in the case-study workflow | Accept | New Table 2; Section 4.2 rewritten to name the record each finding produced | OPEN |
| 2.C4 | Introduction thesis could be improved | Accept | Section 1 states the gap, the claim, and the threat model within the first three paragraphs | OPEN |
| 2.C7 | Length could be improved | Partial accept. Net growth is approximately 400 words, remaining within the 6,250-word limit. | Cuts at the Section 4.1 record-type mapping paragraph and the Section 5 agentic-platform paragraph | OPEN |

## Reviewer 3 (major revision)

| ID | Comment (condensed) | Response | Change (location) | Status |
|---|---|---|---|---|
| 3.1 | Section 3.1 defines five record types; Sections 4.1-4.3 describe the record entirely in terms of Decisions, Events and Actors; the relationship is never stated | Accept, and adopt the reviewer's second proposed option: revise Section 3 to specify the model actually built. | Section 3 rewritten to Actor / Event / Evidence / Decision / Claim / AuditArtifact; workflow-stage terms demoted to open-vocabulary decision types | OPEN |
| 3.2 | The paper credits the schema with work it attributes elsewhere to manual auditing | Accept. Claim narrowed to what is supportable, and the mechanism the reviewer asked for is supplied: every Decision carries a verification status defaulting to unverified, so enumerating a workflow's decisions produces the audit work list before any checking begins. | Abstract rewritten; de-claimed at Sections 3.1, 4.2 and 4.5 | DRAFTED |
| 3.3 | The sub-linear scaling claim rests on one observation with no cost measurement | Accept in full; claim withdrawn. | Third claim in Section 4.5 deleted, replaced by an author-estimated cost reported at its capture tier; the replacement text reports approximately 60 audit hours against approximately 520 development hours, roughly 12 percent overhead, as an author estimate at capture tier 0, and states explicitly that the scaling claim is withdrawn | OPEN |
| 3.4 | State the threat model, since an author-side retrospective record addresses honest error rather than misconduct | Accept | New paragraph at Section 3.4: honest error not misconduct; the record is author-side and not tamper-evident | OPEN |
| 3.5 | The paper does not position itself against W3C PROV-O or RO-Crate, particularly the Workflow Run RO-Crate profile; why a new schema rather than a profile of an existing standard? | Accept. Strongest technical point in the reviews. | New Section 3.5; two references added | OPEN |
| 3.6 | The data availability statement lists four items that do not appear in the deposit it cites | Accept | Deposits corrected first, then the statement; navigation manifest added to both repositories; repair requires a new tagged release and a new Zenodo version DOI, while the concept DOIs are unchanged; see `docs/deposit-verification-2026-08-27.md` | OPEN |
| 3.7 | The manuscript's own AI disclosure names no tool, model or version for drafting, which is what Section 3.1 requires of others | Accept | Disclosure rewritten to name models, versions, dates, and its own capture tier; the AI-use disclosure must also record its own capture tier; manuscript line 105 must be rewritten as an honest-omission gap, because no such deposit exists | OPEN |
| 3.8 | Self-identified during revision, not raised by a reviewer: manuscript line 105 asserts an access-controlled deposit of agent-session logs that does not exist, and the deposited audit artifact declares capture tier 2 while its supporting session logs are gone | Accept; both corrected. | Line 105 rewritten as an honest-omission gap; the deposited AuditArtifact downgraded to tier 1 with a dated note recording the loss | OPEN |
| 3.9 | Self-identified during revision, not raised by a reviewer: Section 4.3 states that recomputation from the deposited inputs was verified on 2026-03-16 and reproduced every headline AUROC. That verification ran in the authors' environment, where a hardcoded absolute path into a separate, undeposited project resolved. From the deposit the first script in the chain raised ModuleNotFoundError, so the sentence asserted precisely the property the deposit lacked | Accept; corrected and disclosed. Same class of defect as 3.8. | Section 4.3 final paragraph rewritten to state the limitation and its repair; the feature-computation module vendored into the deposit with provenance and self-containment confirmed from a clean export. No reported number is affected, because that script's outputs were deposited | OPEN |
| 3.10 | Additional defect identified during revision (not raised by a reviewer); self-identified | Accept, disclosed rather than silently repaired. Two defects were found by our own revision audit. The section 4.3 recomputation claim held only in the authors' environment; from the deposit the first script in the chain failed on a hardcoded path into an undeposited project, so re-execution was broken although no reported number was affected. Separately, the session-log adapter could not locate sessions for any project path containing an underscore, including this paper's own case study, and shipped because the test suite built its fixtures with the same wrong transformation, so a test that reproduced the defect could not fail. | E23 revised to state the re-execution defect and its remedy; new paragraph and Table 2 row added at E19 for the adapter defect | OPEN |
| 3.C4 | Introduction could be improved | Accept; see row 2.C4 | No separate change | OPEN |

## Reviewer 4 (major revision)

| ID | Comment (condensed) | Response | Change (location) | Status |
|---|---|---|---|---|
| 4.1 | The biomedical example is not scientifically coherent; the stated goal of the analysis was incomprehensible to a reviewer with deep biomedical expertise | Accept as a writing failure rather than an analysis failure. The question is restated without the vocabulary of the answer. | Section 4.1 rewritten | DRAFTED |
| 4.2 | "Word salad" quality; simplify language and concepts, use jargon only when necessary | Accept. The Accountability paragraph quoted by the reviewer is rewritten. | Section 2.2 rewritten; full prose pass across the manuscript | OPEN |
| 4.3 | Use a published, credible, substantive third-party workflow instead of the authors' own | DECLINE, with reasons. A retrospective audit requires the superseded scripts, intermediate outputs and internal audit notes that published work does not deposit; auditing a third party's paper would demonstrate the opposite of the paper's claim. Self-audit is the only configuration in which the five defects were recoverable. | Reason stated in the closing paragraph of Section 4.1, not only in the response letter | DRAFTED |
| 4.4 | Provide evidence for the problem beyond the fact that LLMs exist and people use them | Partial accept. Existing evidence in references [2] and [3] is under-deployed, and the five documented defects are themselves the evidence. | Section 1 leads with the defect classes rather than with AI adoption | OPEN |
| 4.5 | An additional homespun JSON layer probably does not add much value | PARTIAL DECLINE. The contribution is the record and the discipline of constructing it; JSON is the serialization, not the claim. Reviewer 3 independently identifies the same gap as genuine. | Section 5 states the contribution as the documentation layer, not the format | OPEN |
| 4.6 | Focus and length could be improved | Accept; see row 2.C7 | No separate change | OPEN |

## Reviewer 5 (reject)

| ID | Comment (condensed) | Response | Change (location) | Status |
|---|---|---|---|---|
| 5.1 | Had to hunt through git repos to find records; some records discussed in the manuscript do not appear in the repos | Accept | Navigation manifest added; deposits corrected | OPEN |
| 5.2 | Records impossible to parse because they are not documented in much detail in the manuscript | Accept | New Table 2 maps each finding to its record and its file | OPEN |
| 5.3 | If the point is to audit AI-generated content, why include an audit of all references? This makes AI and human contributions impossible to disentangle. | Clarify; no substantive change. The AI/human boundary in a drafted bibliography is not recoverable after the fact, so auditing all references is cheaper than reconstructing provenance for each. | One sentence added at Section 4.3 Verifiability | OPEN |
| 5.4 | Why include AI-generated references at all? If the authors have not read them, attribution should go to the AI. | REBUT. A reference is not AI-authored content. Each was read and verified by an author before citing; AIVS records the AI suggestion and the human verification as separate entries. | Stated explicitly at Section 4.3 | OPEN |
| 5.5 | Substantially more context needed for the case study; this is a broad scientific audience | Accept; see row 4.1 | No separate change | DRAFTED |
| 5.6 | The case study includes data dumps that are difficult or impossible to parse | Accept | Section 4.4 numerical results moved to a table; prose carries interpretation only | OPEN |
| 5.7 | Not clear where AIVS records are meant to be used: by reviewers of papers, by authors, or both | Accept; never stated in the submitted version. | New paragraph at Section 3.4: authors produce the record, readers and reviewers consume it, venue policy is out of scope | OPEN |
| 5.8 | Reproducibility seems out of reach; how would knowing when one used a model let another reproduce the results? | Accept; a real gap. The reproducibility target is the pipeline, which is deterministic given pinned inputs. Generative nondeterminism is handled by depositing the output, not by promising regeneration. | Section 2.3 rewritten | OPEN |
| 5.9 | Define AIVS. What is the difference between AIVS and AIVS-VAR? | Accept. No difference exists; the compound term is an artifact of earlier drafts. | Term purged from the manuscript, the audit scripts, and the deposits | OPEN |
| 5.10 | The text is extraordinarily dense and monotonous | Accept; see row 4.2 | No separate change | OPEN |
| 5.11 | There is overlapping text in the figures | Accept | Both figures regenerated | OPEN |

## Associate Editor

| ID | Comment (condensed) | Response | Change (location) | Status |
|---|---|---|---|---|
| AE.0 | Placeholder: the Associate Editor's review PDF has not been retrieved from ScholarOne. AE rows take priority over reviewer rows where the two conflict. | Pending retrieval | Pending | OPEN |

## Declines

Three of 39 rows are declined or partly declined:

- **4.3** (DECLINE): a retrospective audit needs superseded scripts, intermediate outputs and internal notes that published third-party work does not deposit.
- **4.5** (PARTIAL DECLINE): the contribution is the record and the discipline of constructing it, not the JSON serialization.
- **5.4** (REBUT): a reference is not AI-authored content; each was read and verified by an author, and the AI suggestion and the human verification are recorded separately.

## Submission mechanics

- 6,250-word limit, including tables counted as word-equivalents.
- Maximum 12 references.
- DOIs required for every reference.
- Changes marked with coloured or bold text, since the source is Markdown rather than Word.
- Revision submitted through the ScholarOne Author Center under "Create a Revision".

## Drafted text held outside this file

The following passages have already been written and are awaiting integration into the manuscript:

- Abstract.
- Section 2.2 Accountability.
- Section 2.3 Reproducibility.
- Section 3 in full: kernel; capture tier; open vocabulary; threat model and audience; relation to PROV-O and RO-Crate; redaction; availability.
- Section 4.1.
- Table 1: workflow stages S1 to S5, with superseded scripts.
- Section 4.5 cost paragraph.

These exist in the working conversation only. None of them has yet been applied to `var_manuscript_cise.md`.
