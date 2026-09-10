# Auditing AI-Assisted Research: The VAR Framework and AIVS Schema

**Authors:** Hannah Ribbeck and Boggavarapu Kiran*

Department of Chemistry and Physics, McNeese State University, Lake Charles, LA 70609, USA

**Corresponding author:** *Boggavarapu Kiran (kiran@mcneese.edu)

**ORCID iDs:** Boggavarapu Kiran, 0000-0003-0751-6459; Hannah Ribbeck, 0009-0005-3084-5607

---

## Abstract

::: {custom-style="ChangedPara"}
AI-use disclosure statements tell a reader that generative AI was involved. They do not let anyone check what it produced or whether a human verified it. We frame the requirement as three checkable properties, verifiability, accountability, and reproducibility (VAR), and present AIVS, an open-source schema that records an AI-assisted workflow as an auditable artifact which can be constructed after the fact, from surviving evidence, when the workflow was never instrumented. AIVS performs no verification. It records who checked what, with what outcome, and how good the underlying evidence is. Its structure directs an audit: every methodological decision carries a verification status that defaults to unverified, so enumerating a workflow's decisions produces a work list before any checking begins. We report a retrospective audit of our own protein-variant pipeline, built on six AI-derived predictors across 3,409 ClinVar variants, which surfaced five defects that had survived unit tests, code review, and multiple drafts. Three are domain-independent. One renders a reported AUROC unachievable prospectively. The audit cost approximately 60 person-hours against approximately 520 hours of pipeline development. Its own primary evidence, the coding-assistant session logs, was destroyed by default tool retention within six months, which is the case for a record that is constructed and deposited rather than captured and assumed.
:::


**Index Terms:** AI-assisted research, research reproducibility, scientific workflows, provenance, verification, generative AI, scholarly communication, protein variant prediction

---

## 1. Introduction

::: {custom-style="ChangedPara"}
Consider three failures. A protein language model, handed a sequence longer than its context window, returns zeros instead of raising an error, and those zeros enter a reported performance figure as if they were measurements. A cross-validation routine allocates its prediction array with zeros and writes into it only where the data permit, so folds it skips are silently scored as confident predictions. An ensemble routes each test case to a sub-model chosen by the very label being predicted, producing a result that cannot be obtained prospectively.

All three occurred in our own work. All three survived unit tests, code review, and several drafts. None is a hallucinated citation, which is the failure mode most often associated with AI assistance. They are ordinary engineering defects, and what makes them a problem for the published record is not that AI caused them but that nothing in the record would let a reader find them.
:::


::: {custom-style="ChangedPara"}
The gap between AI use and AI verification is now documented quantitatively. A failure-mode taxonomy of NeurIPS 2025 identified 100 hallucinated references across 53 accepted papers, each of which had cleared three to five expert reviewers [8]. The SPOT benchmark, pairing 83 published papers with 91 errata-level errors, found that current language models detect such errors at 6.1% precision and 21.1% recall [3]. Fabrication rates across ten deployed models range from 11.4% to 56.8% depending on model and domain [2]. Meanwhile agentic platforms compose hundreds of generative invocations into a single research artifact [7].
:::


::: {custom-style="ChangedPara"}
Funder policy has responded with blanket restrictions [1], and publishers with screening tools, but these target ethics breaches and fraud rather than a workflow-level account of how AI shaped a particular result. What is missing is a documentation layer between a disclosure statement and full runtime provenance capture, one a reader can audit after the fact even when the workflow was never instrumented.

This paper defines three properties such a record must make checkable (§2), specifies AIVS, a schema that records them (§3), and reports a retrospective audit of a complete protein-variant pipeline we conducted ourselves (§4).

One boundary is worth setting at the outset. The threat model is honest error, not misconduct. An author-side retrospective record is written by the people who did the work, from artifacts they control, and it is not tamper-evident. What it changes is the cost of ordinary failure, which is where the defects above come from.
:::


---

## 2. The VAR Framework

VAR names three properties a verification record for AI-assisted research must make checkable: that every claim and citation resolves to a real object (verifiability), that a specific human is on record for each consequential decision (accountability), and that the workflow can be independently rerun (reproducibility). The properties are operational rather than aspirational: each translates into a check a reader, editor, or downstream researcher can perform on the deposited record without re-reading the paper.

::: {custom-style="ChangedPara"}
### 2.1 Verifiability

Verifiability is checkable. Citations can be resolved against CrossRef, PubMed, arXiv, and institutional repositories; partial matches are flagged separately from non-resolutions. Quoted passages can be resolved against the cited source. Numerical claims can be resolved against canonical output files in the deposited bundle. Code can be cloned and smoke-tested against the pinned environment. Image provenance can be scored with existing forensic tools. Each check is mechanical and, in principle, automatable. AIVS (§3) records the outcome of each such check as part of the workflow's audit trail.
:::


::: {custom-style="ChangedPara"}
### 2.2 Accountability

Accountability means a reader can tell who stood behind a decision.

Take a concrete case. A pipeline scores variants with ESM2 rather than a newer model, and the choice moves the reported result. Someone made that choice. Accountability requires the record to name them.

This matters because AI assistance has blurred something the byline used to handle. When a co-author wrote a section, the byline said who was answerable for it. When a model drafts the section and a co-author accepts it, the byline reads the same and carries less. The record has to hold what the byline no longer does: for each consequential choice, which tool produced the material, and which person endorsed it.

Not every choice, only the ones that change what the paper says. A model and its version. A rule for curating the dataset. A number that reaches the manuscript.

The purpose is deferred checking. A year from now, someone building on this work finds a number that looks wrong. They should be able to see which invocation produced it and who signed off, without writing to the authors.

Accountability here is author-side. It records what the authors did. It says nothing about reviewers or editors and is not a mechanism for judging them.
:::


::: {custom-style="ChangedPara"}
### 2.3 Reproducibility

A reader might object that this is hopeless. If a language model returns something different every time it is called, no record of when it was called will let anyone reproduce anything.

That is right about generation and wrong about the target. The workflow splits in two.

Most of it is ordinary computation: scripts, model weights, a curated dataset, a random seed. Given pinned inputs and pinned versions it reruns to the same numbers. This is standard computational reproducibility, and it is what the reported results actually rest on.

The rest is generative invocation, and it is not reproducible. Providers update and retire models, decoding is stochastic, and a fixed seed carries no guarantee across versions. No schema changes this.

So the target is not regeneration. It is that the generated artifact is deposited, so that what a reader cannot regenerate they can still inspect. AI-written code is the clearest case: producing it was nondeterministic, but the code is a file, and running it is as reproducible as running any other script. The same holds for a curated list or a drafted passage. Deposit the output and the nondeterminism stops propagating downstream.

Reproducibility in VAR therefore asks two things. That the deterministic part reruns from deposited inputs. And that the nondeterministic part is deposited rather than described, so the deterministic part has something fixed to run on.
:::


These three properties are not independent. A verifiability check requires accountability for the verifier; an accountability claim requires verifiable artifacts to anchor; a reproducibility deposit fails its purpose if neither verifier nor accountable author is recorded. AIVS treats them as the three views of a single audit record and serializes them together.

---

::: {custom-style="ChangedPara"}
## 3. AIVS: A Schema for Recording an AI-Assisted Workflow

Generative AI is a system of tools, not a tool. One article can route through a protein language model, two pathogenicity predictors, a code assistant, a chat assistant for prose and figure code, and an agent coordinating several of these, each with its own version, retention policy, and failure modes. The minimum-information-standard tradition, of which MIAME [12] is the best-known instance alongside MIQE and ARRIVE, solved the analogous problem for single instruments by fixing what must be reported. AIVS extends that idea to a multi-tool system.

The schema is deliberately small. It has a closed kernel of six entity types and an open vocabulary that grows from real audits. The kernel is what a reader can rely on; the vocabulary is what the field is still learning.

### 3.1 The kernel

An **Actor** is whoever or whatever performed an action. Its type comes from a closed list: human, AI advisory (the AI suggested, a human committed), AI generative (AI output used directly), AI autonomous (AI executed without per-step review), system, or unknown. The distinction between advisory and generative is the one that matters for accountability, and it is a judgment the author makes, not a property the tool reports.

An **Event** is the atomic unit: a timestamp, an Actor, an action, a target, and an optional content payload with its SHA-256 hash. Actions are open vocabulary, since a prompt, a file edit, a script run, and a model inference are all events and no fixed list survives contact with new tooling.

**Evidence** groups one or more Events into something that supports a claim about the workflow, with a confidence rating.

A **Decision** is the record that does the work. It is a point where a methodological choice was made: which dataset, which model version, which of two analyses becomes canonical. A Decision names its responsible Actor, points at its supporting Evidence, and carries a **verification status** drawn from a closed list: verified independently, verified partially, unverified, not applicable, or no evidence.

A **Claim** is a statement in the manuscript, with its location, traced back to the Decisions upstream of it.

An **AuditArtifact** holds these for one paper, with the schema version, the vocabulary version, the capture tier achieved, and the adapters used. A structural validator checks referential closure: every Evidence points at Events that exist, every Decision at Evidence that exists, every Claim at Decisions that exist.

The chain runs Events to Evidence to Decision to Claim, and it runs both ways (Fig 1). Forward, it shows what a given AI invocation ended up affecting. Backward, it answers the question a reader actually has: this number in the abstract, where did it come from, and did anyone check it.

That backward direction is also how the schema directs an audit rather than merely storing one. Every Decision must carry a verification status, and the default is unverified. Enumerating the Decisions in a workflow therefore produces a work list before any checking has been done: the unverified Decisions are the ones an auditor has to go look at. The schema detects nothing. It makes the places where nobody has looked impossible to skip past.

### 3.2 Capture tier: what the record costs

The obstacle to any provenance scheme is that most workflows are not instrumented when the work happens, and instrumenting them fully is expensive. AIVS grades the evidence rather than demanding a fixed level of it. Every audit declares the tier it achieved. **Tier 0** is a manual log written from memory and notes. **Tier 1** adds version control and notebooks, with no record of AI sessions. **Tier 2** adds AI session logs. **Tier 3** adds environment and reproducibility metadata.

The tier is not a grade on the authors. It tells a reader what the record can and cannot support. A tier 1 audit can establish that a decision was made and by whom; it cannot establish which prompt produced the code that implemented it. Stating the tier makes that limit visible instead of leaving a reader to assume completeness. It also means an author with no instrumentation at all can still produce a usable record, which is the common case and the one this paper is about.

### 3.3 An open vocabulary that grows from audits

Decision types are open vocabulary. Version 0.1 of that vocabulary contains one term, `unclassified`, and the schema requires any Decision using it to set a novel-pattern flag and emit a **SchemaDelta**: a proposal for a new term, with its justification and the evidence that prompted it.

This has a cost, and it shows in the case study. Every Decision in the audit reported in §4 is `unclassified`, because the vocabulary was empty when that audit was constructed. What the audit produced instead is a set of SchemaDeltas, which are the empirical input to the next vocabulary version. A term is promoted only after it recurs across independent audits. Publishing a rich vocabulary invented in advance would have produced tidier records and worse evidence about which categories are real.

### 3.4 Scope, audience, and threat model

AIVS does not perform verification. It records who or what performed a check and what the outcome was. Some checks can be automated (resolving citations against CrossRef, tracing a reported number to a canonical output file, smoke-testing deposited code) and some cannot (judging whether a curated annotation is appropriate). The schema records the verifier either way.

It does not assess scientific correctness, methodological appropriateness, novelty, or writing quality. Those remain with human reviewers.

The record is produced by authors and consumed by readers, reviewers, and downstream researchers. It is not a submission requirement, and nothing here depends on a venue adopting it. Whether editors should require such records is a policy question this paper does not address.

The threat model is honest error. An author-side retrospective record is written by the same people who did the work, from artifacts they control. It is not tamper-evident and does not claim to be. An author determined to conceal something can produce a clean AIVS record, exactly as they can produce a clean Methods section. Detecting deliberate fraud requires adversarial assumptions and third-party capture, and is a different problem.

### 3.5 Relation to existing provenance standards

W3C PROV-O [10] provides a general vocabulary for entities, activities, and agents, and RO-Crate [11], particularly its Workflow Run profile, packages an executed computational workflow with its provenance. PROV-AGENT [9] instruments agentic workflows through the Model Context Protocol and streams provenance into a consolidated database as the workflow runs.

These assume instrumentation at execution time, and where it exists they are the better tool: their records can populate an AIVS audit directly, and the kernel is deliberately mappable onto PROV-O's agent, activity, and entity triple. AIVS addresses the case where instrumentation was absent, which is most published work. Its unit is not the execution step but the methodological decision and its verification status, and its capture tier makes explicit how much of the record was reconstructed rather than captured. A profile of an existing standard cannot express that, because the standards assume the run was observed. The two are complementary: instrument if you can, reconstruct and grade the reconstruction if you cannot.

### 3.6 Redaction and disclosure

Prompts routinely carry unpublished data, patient-derived identifiers, or third-party material. The default posture is minimum capture: adapters run in redact mode, emitting Events with a content hash and no content, so an audit can demonstrate that an event occurred and verify any later disclosure without publishing the payload. Where content is captured, a publish step strips it from every Decision not explicitly marked for verbatim release; author-written descriptions are never stripped, since those are curated disclosure rather than captured content. A floor is always public: model identifiers and versions, verification outcomes, capture tier, and responsible actors. The record is append-only, so a re-run that newly resolves a previously failed check is added rather than substituted.

### 3.7 Availability

AIVS is released under AGPL-3.0-or-later and archived at Zenodo (§ Resource availability). The release ships the kernel, JSON serialization, structural validation, session adapters for three coding assistants, and four worked retrospective audits including the one below. The automated checks of §2.1 and adapters for submission systems are natural extensions, not implemented here and not claims of this paper.
:::


---

## 4. Case Study: An AI-Assisted Workflow on IDP Disease-Mechanism Prediction

::: {custom-style="ChangedPara"}
We demonstrate AIVS on a workflow we conducted ourselves: prediction of disease mechanism from missense variants in intrinsically disordered protein (IDP) genes implicated in neurodegeneration. The workflow draws on six generative-AI-derived predictors, including a 650-million-parameter protein language model invoked across thousands of variant positions, and uses AI assistance for drafting, literature synthesis, and figure code. The audit was conducted retrospectively over the complete pipeline.
:::


### 4.1 The research workflow

::: {custom-style="ChangedPara"}
Predictors like ESM2 [4], AlphaMissense [5], and EVE [6] score a mutation by how unusual it looks against evolutionary patterns learned from millions of protein sequences. A mutation at a position evolution has held fixed scores as damaging. This works because most well-studied disease proteins fold into a stable shape, and the positions evolution holds fixed are the ones that shape depends on.

Intrinsically disordered proteins have no stable shape. Their sequences drift, and individual positions are rarely conserved. Some still cause disease the familiar way, by losing function. Others cause disease by gaining one: the mutant protein acquires a new harmful behavior, typically aggregating where it should not, and the residue responsible need not be conserved at all. What matters instead is where it sits, for instance inside a nuclear localization signal that determines whether the protein stays in the nucleus.

If that account is right, conservation-based predictors should work on the loss-of-function cases and fail on the gain-of-toxic-function ones. That is the question the workflow asks, and the answer is that they do (§4.4).

The workflow runs in five stages (Table 1), across 3,409 missense variants in 22 genes from a content-hashed ClinVar snapshot, evaluated by leave-one-gene-out cross-validation so that no gene is ever tested on a model that saw it.

Two features make this a useful audit target rather than a convenient one. It runs a heterogeneous AI stack, three generative predictors plus three non-generative baselines plus AI-assisted code and prose, which is the configuration where a single disclosure line conveys least. And it is ours, which matters more than it may appear: a retrospective audit needs the superseded scripts, intermediate outputs, and internal audit notes that published work does not deposit. Auditing a third party's paper would demonstrate the opposite of this paper's claim.
:::


::: {custom-style="ChangedPara"}
**Table 1. Workflow stages.**

| Stage | What it does | Implementing script | Status |
|---|---|---|---|
| S1 Curate | ClinVar snapshot to clean-labeled variant set | `01_build_variant_set.py` | canonical |
| S2 Score | Six predictors, per variant | `06_approach_c_esm2.py` | scoring canonical; CV block superseded |
| S3 Model | Region annotation plus ESM2 LLR, two features | `10_two_step_predictor.py` | canonical |
| S4 Evaluate | LOGO-CV, bootstrap CIs, permutation controls | `10`, `11`, `17` | canonical |
| S5 Draft | AI-assisted prose, figures, methods | chat sessions | canonical |
| | Single-model baseline, superseded at S4 | `04_approach_a_xgboost.py` | withdrawn (F2) |
| | Mechanism-aware ensemble, superseded at S3 | `08_mechanism_aware_model.py` | exploratory (F3) |
:::


::: {custom-style="ChangedPara"}
### 4.2 What the audit found
:::


::: {custom-style="ChangedPara"}
The audit worked from the decision list. Enumerating the workflow's consequential decisions produced eight, three covering the workflow itself (dataset curation, predictor selection, canonical-model selection) and five recording the disposition of a defect. Each carries a verification status, and those still standing as unverified were the work list. Working that queue, rather than reading the code start to finish, is what put attention on the five defects below. All five had survived unit tests, code review, and multiple drafts.
:::


::: {custom-style="ChangedPara"}
**A truncated model silently returned zeros.** (S2) The HTT protein is 3,142 residues; ESM2 accepts 1,022 tokens. Rather than failing, the inference wrapper returned default values for variants whose context could not be tiled: log-likelihood ratio 0.0, entropy 0.0, rank 10. This affected 170 of 255 HTT variants, and all of them entered the pooled AUROC as real measurements. The signature was visible once looked for: identical default values repeating across consecutive positions, which computed features never do. HTT was excluded, leaving the 3,409-variant, 22-gene evaluable set the paper reports.

A residual weakness is worth stating. The fabrication is triggered by residue position, but every guard in the pipeline is triggered by gene name. The two coincide only because HTT is the sole protein in the panel above 1,022 residues, the next longest reaching 915. Adding one longer protein would make every gene-name filter silently insufficient while still appearing correct.
:::


::: {custom-style="ChangedPara"}
**Skipped cross-validation folds were scored as predictions of zero.** (S4) The early cross-validation code allocated a prediction array of zeros per fold and wrote into it only where both classes were present. Folds skipped for having a single class left their zeros in place, and the pooled AUROC consumed them as predictions. The effect was small on the full set and material on mechanism-stratified subsets, where some folds contain no benign variants at all. Comparing those outputs against the canonical bootstrap distribution exposed the gap.

The two affected scripts were retired differently, and the distinction matters. The single-model baseline was withdrawn entirely; nothing downstream reads its outputs. The ESM2 script was not, because its cross-validation block and its scoring block are separate: the defective cross-validation was replaced, while the feature table it writes remains the canonical input to the paper-facing predictor, the bootstrap intervals, the predictor comparisons, the permutation control, and every main figure. Retiring the script wholesale would have retired the paper's own inputs. What was superseded is a block, not a file.
:::


::: {custom-style="ChangedPara"}
**The ensemble was reading the answer.** (S3) An exploratory ensemble routed each test gene to a sub-model chosen by that gene's disease mechanism. Under leave-one-gene-out cross-validation the mechanism of the held-out gene is exactly what is not known, so its reported AUROC of 0.738 is unachievable prospectively. Checking what the routing function could see at test time found it reading a mechanism field that blinding should have withheld. The ensemble was demoted to exploratory and excluded from every headline claim.
:::


::: {custom-style="ChangedPara"}
**Numbers in the draft did not match the files they came from.** (S5) Tracing each reported value to its canonical output found three discrepancies. A pooled ESM2 AUROC given as 0.70 was the VUS-included figure; the clean-label value is 0.772. A comparison quoting 0.784 against 0.676 mixed the VUS-included set with a five-feature model, not the two-feature model the surrounding text described; corrected, it reads 0.873 against 0.748 clean-label, with the VUS-included figures disclosed as sensitivity. And loss-of-function performance described as comparable at 0.76 for both methods was in fact 0.813 against 0.650, a degradation rather than a tie. That last one is the case for tracing every number rather than the surprising ones: it read as unremarkable and reversed the finding.
:::


::: {custom-style="ChangedPara"}
**A probability was reported that the method could not produce.** (S5) A draft gave P(two-step > ESM2) = 1.000 from 1,000 bootstrap resamples. A resample of size n cannot estimate a probability below 1/n, so 0.999 is the ceiling. Corrected to P < 0.001.
:::


::: {custom-style="ChangedPara"}
The same pass caught three lesser problems, each now disclosed with its consequence: a methods table naming IUPred2A where metapredict was used, with a window reported as ±10 residues rather than ±15; bootstrap failures for genes with too few minority-class variants; and class imbalance disclosed only in aggregate rather than per gene.

Three of the five are domain-independent. A model returning defaults instead of failing, an array initialized to a value that is also a legal prediction, and a test-time feature that encodes the label are failures available to any computational scientist.

A sixth defect surfaced during revision, after review. The session-log adapter derived its search path by replacing path separators, but the tool it reads also collapses underscores and dots, so the adapter could not locate sessions for any project whose path contained an underscore, including this case study. It shipped because the test suite built its fixtures with the same wrong transformation: fixture and implementation agreed, and a test that reproduces the defect it guards cannot fail. Correcting the adapter caused four passing tests to fail, which is how the defect became visible. This is the fourth domain-independent failure in this list and the least visible, since every conventional signal said the code was covered.

**Table 2. Where each finding is recorded.**

| Finding | Stage | Disposition | Audit document | Corrected output |
|---|---|---|---|---|
| Context-window defaults | S2 | locus excluded, metrics recomputed | 2026-02-20 audit, finding 3 | evaluable-set CSV |
| Zero-filled skipped folds | S4 | baseline withdrawn, CV block replaced | 2026-02-20 audit, findings 2, 5 | `bootstrap_cis.csv` |
| Mechanism-label leakage | S3 | demoted to exploratory | 2026-02-20 audit, finding 4 | `results_two_step.csv` |
| Untraced numerical claims | S5 | three values corrected | `CRITICAL_EVALUATION.md` | canonical CSVs |
| Impossible probability | S5 | corrected to P < 0.001 | `CRITICAL_EVALUATION.md` §3.3 | `bootstrap_cis.csv` |
| Self-confirming adapter test | tooling | adapter corrected, fixtures rebuilt | revision audit, `docs/audit-record-corrections.md` | regression test |

Each row is one Decision in the deposited record, with Events citing the script lines, the audit document, and the corrected output.
:::


::: {custom-style="ChangedPara"}
### 4.3 The record itself
:::


::: {custom-style="ChangedPara"}
*Verifiability.* Every quantitative claim traces to a specific cell in a canonical output file; the numerical-audit log records ten headline numbers with their source references and outcomes. Citation resolution succeeded for all references in the current draft.

We audited every reference, not only those an AI suggested. The boundary between AI-suggested and author-supplied citations in a drafted bibliography is not recoverable after the fact, and reconstructing it would cost more than checking all of them. A reference is also not AI-authored content: each was read and assessed by an author before citing, and the record holds the suggestion and the human verification as separate entries. Attribution for a citation belongs to the author who chose to stand behind it.
:::


::: {custom-style="ChangedPara"}
*Accountability.* Authorship is disclosed at the granularity of section and task. The pipeline (variant curation, feature engineering, cross-validation, mechanism-stratified analysis, permutation controls) is attributed to H.R.; schema design, AI-assisted drafting, and figure preparation to B.K. Each Event and Decision carries an Actor identified by ORCID.

The record does not contain the coding-assistant session logs. They existed when the audit was constructed and were destroyed by the tool's default retention policy before this revision; their absence was confirmed on 2026-08-27. The audit is therefore capture tier 1, not tier 2, and the deposited artifact has been corrected to say so. This is a real limitation and it is the kind the capture tier exists to make visible.
:::


::: {custom-style="ChangedPara"}
*Reproducibility.* The pipeline is deposited (§ Resource availability). The ClinVar snapshot is pinned to February 2026 with a content hash and the ESM2 checkpoint to `esm2_t33_650M_UR50D`; AlphaMissense and EVE access dates and provider-stated retention policies are recorded. Recomputation of the headline AUROCs was verified on 2026-03-16 and reproduced them to three decimal places.

That verification ran in the authors' environment. During revision we found that the deposited copy could not have reproduced it: the first script in the chain reached a feature-computation module through a hardcoded absolute path into a separate, undeposited project, so a third party cloning the deposit would have failed at the first step. The module is now vendored into the repository with provenance, and self-containment was confirmed by running the pipeline from a clean export with the external path removed. No reported number is affected, because the outputs of that script were deposited; what was broken was re-execution, which is the property this section claims.

One property the deposited audit record does not have is byte-level reproducibility: re-running the audit script regenerates fresh identifiers, so the output differs from the deposited copy while carrying identical content. The deposited copies are the reference and are checksummed. This is the §2.3 argument applied to the record itself, and the repository states it rather than leaving a reader to discover it.
:::


### 4.4 Results under verification

::: {custom-style="ChangedPara"}
The prediction in §4.1 holds, and the separation is clean (Fig 2).

Conservation-based scoring works where the structural assumption holds and fails where it does not. ESM2 reaches AUROC 0.813 on loss-of-function structured genes (LMNA, SOD1, CRYAB, VCP) and 0.813 on toxic-aggregation amyloid genes (SNCA, TTR, PRNP, IAPP), but 0.493 on gain-of-toxic-function non-amyloid genes (FUS, TARDBP, HNRNPA1, TIA1, HNRNPA2B1, EWSR1, TAF15), which is chance. A predictor at 0.493 is not weakly informative; it carries no information about which variants cause disease.

The failure is not specific to one model. AlphaMissense reaches 0.620 on that subset, falling to 0.398 with FUS excluded, and EVE reaches 0.342, below chance. Three independently trained generative architectures fail the same subset, which points at the shared assumption rather than any one implementation.

Where sequence conservation carries no signal, position does. Binary membership of a curated functional region alone reaches 0.792 overall, and combining it with the ESM2 score reaches 0.873. On the non-amyloid subset the two-step model recovers to 0.822, a gain of 0.329 (bootstrap 95% CI [0.305, 0.441], P < 0.001), while degrading the loss-of-function structured subset to 0.650. That trade-off is disclosed rather than averaged away.

The FUS case is the sharpest instance: membership of the PY-nuclear localization signal alone predicts pathogenicity at 0.916, and a 10,000-permutation control against length-matched random regions gives p = 0.002, so the signal is specific to that region rather than to any region of that size.
:::


::: {custom-style="ChangedPara"}
### 4.5 Cost, and what the record cannot certify
:::


::: {custom-style="ChangedPara"}
Building the pipeline took approximately 520 person-hours, six months at roughly twenty hours per week, from variant curation through the first draft of results. The retrospective audit took approximately 60 person-hours, four weeks at roughly fifteen hours per week, covering both audit passes, the corrections they required, and construction of the record. The audit added roughly twelve percent to the cost of the work, about one hour of checking for every eight of development.

Both figures are author estimates rather than measurements, reported at capture tier 0 accordingly. The evidence that would have measured them was the session logs described in §4.3. That loss is itself informative: a record that depends on the retention behavior of the tools it documents is not durable, which is the argument for constructing and depositing an audit artifact rather than assuming the underlying logs persist.

The 60 hours includes authoring such a record for the first time, with no existing tooling and while the vocabulary was still empty, so it is an upper bound on the recording cost rather than a steady-state figure. We make no claim about how that cost scales with workflow complexity; an earlier version of this paper did, on the strength of a single observation, and that claim is withdrawn.
:::


::: {custom-style="ChangedPara"}
The record also cannot certify substance. It shows that the FUS PY-NLS is annotated as residues 502 to 526 with a stated literature source, and that a permutation control returned p = 0.002 for that annotation. It does not establish that 502 to 526 is the correct boundary. The record makes the verification chain visible; it does not replace it.
:::


### Figures

![](figures/figure_1_aivs_schema.png)

::: {custom-style="ChangedPara"}
**Figure 1. The AIVS record graph.** Events carry an Actor, an action, and an optional hashed payload. Evidence groups Events. Decisions name a responsible Actor, cite Evidence, and carry a verification status. Claims point to the manuscript locations they support. The kernel is closed at these entity types; the vocabularies for actions and decision types are open and grow through SchemaDelta proposals from completed audits.
:::


![](figures/figure_1.png)

::: {custom-style="ChangedPara"}
**Figure 2. Conservation-based prediction is mechanism-dependent.** (A) Per-gene ESM2 AUROC for 22 genes grouped by disease mechanism, with bootstrap 95% CIs; the dashed line marks chance. Gain-of-function non-amyloid genes fall to chance while loss-of-function structured genes cluster above 0.65. (B) ESM2 score distributions for benign or uncertain versus pathogenic variants in each group. Pathogenic variants score higher in loss-of-function structured genes (Δμ = +2.98) and lower in gain-of-function non-amyloid genes (Δμ = −0.87), so the score is not merely uninformative there but inverted. (C) Four predictors on the non-amyloid subset. Functional-region membership outperforms all three conservation-based predictors. EVE was unavailable for FUS.
:::


---

## 5. Discussion

::: {custom-style="ChangedPara"}
The contribution is a documentation layer between disclosure and full workflow capture. Disclosure without verification lets fabrications enter print unless a reviewer happens to notice. An audit record makes the verification of each AI-assisted claim explicit, so a missed check is visible in the trail rather than invisible. The contribution is the record and the discipline of constructing it, not the serialization format, and not an enforcement mechanism.
:::


::: {custom-style="ChangedPara"}
The case for it grows with agentic platforms, which compose many generative invocations into one artifact and emit internal logs that could populate such a record [7]. That mapping is not built here. What this paper establishes is narrower and prior to it: that the record is constructible for a genuine workflow, at what cost, and that constructing it caught errors disclosure would not.

Two limitations bound the claim. The evidence is one workflow, self-audited, and a single case cannot separate what the schema contributed from what a careful auditor would have found anyway. And the practice is author-side: it depends on authors choosing to produce a record and readers choosing to inspect it.
:::


The framework has a reach limitation. As demonstrated here it is an author-side practice: it produces an auditable record, but it depends on authors choosing to produce one and on readers and reviewers choosing to inspect it. Whether venues require or automate such records is an editorial-policy question this paper does not address. What this paper does address is whether the record itself is constructible and useful, and the case study answers both.

---

## 6. Conclusion

::: {custom-style="ChangedPara"}
The question is not whether AI use should be permitted but how AI-assisted work can be documented to a standard science can defend. VAR names what such documentation must make checkable; AIVS records it; the case study shows the record is constructible for a real workflow, costs roughly twelve percent of the work it documents, and surfaced five defects that had survived ordinary review. As generative components compose into longer chains, the distance between their internal complexity and the auditability of their published outputs widens. Closing it does not require a new institution, only a record that says what was done and who checked it.
:::


---

## Experimental procedures

::: {custom-style="ChangedPara"}
**Dataset.** 3,409 missense variants across 22 IDP-associated genes from the content-hashed ClinVar February 2026 snapshot at ≥1-star review status, cross-validated against UniProt canonical sequences. HTT is excluded from all paper-facing analyses (§4.2).

**Predictors.** ESM2 (`esm2_t33_650M_UR50D`, loaded through HuggingFace `transformers`) supplying log-likelihood ratios and position entropies; AlphaMissense and EVE for pathogenicity scores; CADD, REVEL, and PolyPhen-2 as non-generative baselines. Functional-region annotations from primary sources (FUS PY-NLS 502–526; TARDBP LCD 274–414; HNRNPA1 PrLD 185–372).

**Model.** Two-step logistic regression combining a binary curated-region-membership indicator with the raw ESM2 log-likelihood ratio.

**Evaluation.** Leave-one-gene-out cross-validation with deterministic folds; 1,000-resample bootstrap CIs; 10,000-permutation random-region control; mechanism-stratified subgroup AUROCs. The environment is pinned in `requirements.txt`.

**Verification.** The AIVS v0.2.1 kernel was used to structure the record. The five defects of §4.2 were found by manual audit and recorded as Decisions, each linked to Events citing the offending code, the audit document, and the corrected canonical output. Capture tier 1.
:::


---

## Resource availability

**Lead contact.** Requests for further information should be directed to Boggavarapu Kiran (kiran@mcneese.edu).

::: {custom-style="ChangedPara"}
**Data and code availability.** The AIVS schema (AGPL-3.0-or-later) is at https://github.com/khatvangi/aivs, archived at Zenodo: concept DOI 10.5281/zenodo.20723558, version DOI 10.5281/zenodo.22698585. The variant dataset, analysis scripts, figure-generation scripts, environment manifest, and canonical output tables are at https://github.com/khatvangi/idp-mechanism-classifier, archived at Zenodo: concept DOI 10.5281/zenodo.20723560, version DOI 10.5281/zenodo.22698586. The AIVS verification record for this case study is deposited in the AIVS repository at `examples/mechanism_classifier_audit.py` with serialized outputs under `examples/out/`; both repositories carry a README mapping each manuscript claim to the file that supports it. The large public source tables (ClinVar `variant_summary`, AlphaMissense substitutions) are re-downloadable and excluded by design. The coding-assistant session logs are not deposited and no longer exist (§4.3).
:::


---

## References

::: {custom-style="ChangedPara"}
[1] National Institutes of Health. Supporting fairness and originality in NIH research applications. NOT-OD-25-132, July 2025. https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-132.html

[2] Naser MZ. How LLMs cite and why it matters: a cross-model audit of reference fabrication in AI-assisted academic writing. arXiv:2603.03299, February 2026. https://doi.org/10.48550/arXiv.2603.03299

[3] Son G, Hong S, Choi H, et al. When AI co-scientists fail: SPOT, a benchmark for automated verification of scientific research. arXiv:2505.11855, May 2025. https://doi.org/10.48550/arXiv.2505.11855

[4] Lin Z, Akin H, Rao R, et al. Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science* 2023;379:1123–1130. https://doi.org/10.1126/science.ade2574

[5] Cheng J, Novati G, Pan J, et al. Accurate proteome-wide missense variant effect prediction with AlphaMissense. *Science* 2023;381:eadg7492. https://doi.org/10.1126/science.adg7492

[6] Frazer J, Notin P, Dias M, et al. Disease variant prediction with deep generative models of evolutionary data. *Nature* 2021;599:91–95. https://doi.org/10.1038/s41586-021-04043-8

[7] Gottweis J, Weng W-H, Daryin A, et al. Towards an AI co-scientist. arXiv:2502.18864, February 2025. https://doi.org/10.48550/arXiv.2502.18864

[8] Ansari S. Compound deception in elite peer review: a failure-mode taxonomy of 100 fabricated citations at NeurIPS 2025. arXiv:2602.05930, February 2026. https://doi.org/10.48550/arXiv.2602.05930

[9] Souza R, Gueroudji A, DeWitt S, et al. PROV-AGENT: unified provenance for tracking AI agent interactions in agentic workflows. IEEE e-Science 2025. arXiv:2508.02866. https://doi.org/10.1109/eScience65000.2025.00093

[10] Lebo T, Sahoo S, McGuinness D, eds. PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. https://www.w3.org/TR/2013/REC-prov-o-20130430/

[11] Soiland-Reyes S, Sefton P, Crosas M, et al. Packaging research artefacts with RO-Crate. *Data Science* 2022;5:97–138. https://doi.org/10.3233/DS-210053

[12] Brazma A, Hingamp P, Quackenbush J, et al. Minimum information about a microarray experiment (MIAME). *Nature Genetics* 2001;29:365–371. https://doi.org/10.1038/ng1201-365
:::


---

**Author contributions:** Conceptualization, B.K.; Methodology, B.K. and H.R.; Software, B.K.; Investigation, H.R.; Data curation, H.R.; Formal analysis, H.R.; Writing – original draft, B.K.; Writing – review & editing, B.K. and H.R.

**Declaration of interests:** The authors declare no competing interests.

**Acknowledgments:** This work was supported by internal funds from McNeese State University; no external funding was received.

::: {custom-style="ChangedPara"}
**Generative AI use:** AI assistance was used for literature synthesis, methods and prose drafting, figure-code generation, and analysis-code generation, and generative models were used as instruments for per-variant scoring (ESM2, AlphaMissense, EVE). Drafting and code assistance used Anthropic Claude models accessed through the Claude web interface and through Claude Code, over a project-scoped range of 2026-03-16 to 2026-09-09. The models were Claude Opus 4.6 class; this is recorded from author recollection at capture tier 0, and the author does not recall with confidence which exact version was in use at each point across that period. One model identifier survives in local configuration, but it belongs to a tooling session rather than to drafting or audit construction and is not cited as evidence for either. No per-invocation attribution is recoverable: the session logs were destroyed by the tool's default retention policy and confirmed absent on 2026-08-27. This disclosure is therefore capture tier 0 for drafting and tier 1 for the case-study workflow. All AI-suggested content, including every citation, was read and verified by an author before inclusion, and the authors take responsibility for it.
:::


**Author biographies:**

**Hannah Ribbeck** is an undergraduate researcher in the Department of Chemistry and Physics at McNeese State University, working on computational biology of intrinsically disordered proteins and variant interpretation.

**Boggavarapu Kiran** is on the faculty of the Department of Chemistry and Physics at McNeese State University. His research interests span computational biology, the philosophy and methodology of AI-assisted research, and scientific publishing infrastructure. He received a Ph.D. in chemistry. Contact: kiran@mcneese.edu.
