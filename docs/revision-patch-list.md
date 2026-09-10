# Revision patch list

**Source:** `/storage/kiran-stuff/aivs/var_manuscript_cise.md` (201 lines, unchanged)
**Target:** `var_manuscript_cise_r1.md`

Every paragraph in the source occupies one line, so each edit below is a whole-line replacement
anchored by line number. Apply in descending line order, or re-read line numbers after each edit.
Unlisted lines are unchanged.

Thirty-six edits. Format: line, reviewer rows, why, replacement text. Two are multi-line block
replacements: E8 (lines 45 to 71) and E35 (lines 163 to 185); the remainder are single-line.

---

## E1 — Line 15 (Abstract) — R3.2, R3.3, R1.4

Removes the claim that AIVS caught the errors, which contradicted §3.2 and §4.2. Adds cost and
the retention finding.

> AI-use disclosure statements tell a reader that generative AI was involved. They do not let anyone check what it produced or whether a human verified it. We frame the requirement as three checkable properties, verifiability, accountability, and reproducibility (VAR), and present AIVS, an open-source schema that records an AI-assisted workflow as an auditable artifact which can be constructed after the fact, from surviving evidence, when the workflow was never instrumented. AIVS performs no verification. It records who checked what, with what outcome, and how good the underlying evidence is. Its structure directs an audit: every methodological decision carries a verification status that defaults to unverified, so enumerating a workflow's decisions produces a work list before any checking begins. We report a retrospective audit of our own protein-variant pipeline, built on six AI-derived predictors across 3,409 ClinVar variants, which surfaced five defects that had survived unit tests, code review, and multiple drafts. Three are domain-independent. One renders a reported AUROC unachievable prospectively. The audit cost approximately 60 person-hours against approximately 520 hours of pipeline development. Its own primary evidence, the coding-assistant session logs, was destroyed by default tool retention within six months, which is the case for a record that is constructed and deposited rather than captured and assumed.

## E2 — Line 23 (Introduction, opening) — R4.4, R2.C4

Reviewer 4 asked for evidence of the problem beyond the existence of LLMs. Opens with three
concrete defects from this paper's own case study.

> Consider three failures. A protein language model, handed a sequence longer than its context window, returns zeros instead of raising an error, and those zeros enter a reported performance figure as if they were measurements. A cross-validation routine allocates its prediction array with zeros and writes into it only where the data permit, so folds it skips are silently scored as confident predictions. An ensemble routes each test case to a sub-model chosen by the very label being predicted, producing a result that cannot be obtained prospectively.
>
> All three occurred in our own work. All three survived unit tests, code review, and several drafts. None is a hallucinated citation, which is the failure mode most often associated with AI assistance. They are ordinary engineering defects, and what makes them a problem for the published record is not that AI caused them but that nothing in the record would let a reader find them.

## E3 — Line 25 — reference renumbering (see E32)

Drops the three agentic-platform citations being removed. `[11]` becomes `[8]`. Also replaces the
unquantified fabrication claim with a measured rate, which addresses R4.4, evidence for the problem
beyond the existence of LLMs.

> The gap between AI use and AI verification is now documented quantitatively. A failure-mode taxonomy of NeurIPS 2025 identified 100 hallucinated references across 53 accepted papers, each of which had cleared three to five expert reviewers [8]. The SPOT benchmark, pairing 83 published papers with 91 errata-level errors, found that current language models detect such errors at 6.1% precision and 21.1% recall [3]. Fabrication rates across ten deployed models range from 11.4% to 56.8% depending on model and domain [2]. Meanwhile agentic platforms compose hundreds of generative invocations into a single research artifact [7].

## E4 — Line 27 — R5.9, R3.4, R2.C4

Removes "AIVS-VAR" and adds the threat model early.

> Funder policy has responded with blanket restrictions [1], and publishers with screening tools, but these target ethics breaches and fraud rather than a workflow-level account of how AI shaped a particular result. What is missing is a documentation layer between a disclosure statement and full runtime provenance capture, one a reader can audit after the fact even when the workflow was never instrumented.
>
> This paper defines three properties such a record must make checkable (§2), specifies AIVS, a schema that records them (§3), and reports a retrospective audit of a complete protein-variant pipeline we conducted ourselves (§4).
>
> One boundary is worth setting at the outset. The threat model is honest error, not misconduct. An author-side retrospective record is written by the people who did the work, from artifacts they control, and it is not tamper-evident. What it changes is the cost of ordinary failure, which is where the defects above come from.

## E5 — Line 35 — subsection heading

Insert `### 2.1 Verifiability` immediately before line 35. Line 35 itself is unchanged except that
its leading `**Verifiability** is checkable.` becomes `Verifiability is checkable.`

## E6 — Line 37 (Accountability) — R4.2

This is the paragraph Reviewer 4 quoted as his example of word salad. Insert heading
`### 2.2 Accountability` before it and replace the line with:

> Accountability means a reader can tell who stood behind a decision.
>
> Take a concrete case. A pipeline scores variants with ESM2 rather than a newer model, and the choice moves the reported result. Someone made that choice. Accountability requires the record to name them.
>
> This matters because AI assistance has blurred something the byline used to handle. When a co-author wrote a section, the byline said who was answerable for it. When a model drafts the section and a co-author accepts it, the byline reads the same and carries less. The record has to hold what the byline no longer does: for each consequential choice, which tool produced the material, and which person endorsed it.
>
> Not every choice, only the ones that change what the paper says. A model and its version. A rule for curating the dataset. A number that reaches the manuscript.
>
> The purpose is deferred checking. A year from now, someone building on this work finds a number that looks wrong. They should be able to see which invocation produced it and who signed off, without writing to the authors.
>
> Accountability here is author-side. It records what the authors did. It says nothing about reviewers or editors and is not a mechanism for judging them.

## E7 — Line 39 (Reproducibility) — R5.8

Reviewer 5 asked how knowing when a model was used could let anyone reproduce a result. The
submitted paragraph did not engage the objection. Insert heading `### 2.3 Reproducibility` before
it and replace with:

> A reader might object that this is hopeless. If a language model returns something different every time it is called, no record of when it was called will let anyone reproduce anything.
>
> That is right about generation and wrong about the target. The workflow splits in two.
>
> Most of it is ordinary computation: scripts, model weights, a curated dataset, a random seed. Given pinned inputs and pinned versions it reruns to the same numbers. This is standard computational reproducibility, and it is what the reported results actually rest on.
>
> The rest is generative invocation, and it is not reproducible. Providers update and retire models, decoding is stochastic, and a fixed seed carries no guarantee across versions. No schema changes this.
>
> So the target is not regeneration. It is that the generated artifact is deposited, so that what a reader cannot regenerate they can still inspect. AI-written code is the clearest case: producing it was nondeterministic, but the code is a file, and running it is as reproducible as running any other script. The same holds for a curated list or a drafted passage. Deposit the output and the nondeterminism stops propagating downstream.
>
> Reproducibility in VAR therefore asks two things. That the deterministic part reruns from deposited inputs. And that the nondeterministic part is deposited rather than described, so the deterministic part has something fixed to run on.

## E8 — Lines 45 to 71 (all of §3) — R3.1, R1.1, R2.1, R2.3, R5.2

The only replacement of an entire section, and unavoidable: the submitted §3 specifies
five record types that were never implemented, and Reviewer 3 asked us either to instantiate them
or to specify what was built. Replace the entire block, headings included, with §3 as given in
`var_manuscript_cise_r1.md`, subsections 3.1 through 3.7.

Structure changes from three subsections to seven. The additions carry specific reviewer load:
3.2 capture tier answers R2.2 on level of effort; 3.4 answers R3.4 threat model and R5.7 audience;
3.5 answers R3.5 on PROV-O and RO-Crate.

## E9 — Line 77 — R5.9

Remove "AIVS-VAR". Replace the opening clause `We demonstrate AIVS-VAR on a workflow` with
`We demonstrate AIVS on a workflow`. Rest of line unchanged.

## E10 — Line 81 (§4.1) — R1.2, R4.1, R5.5

Reviewer 4, with deep biomedical expertise, could not comprehend the stated goal. Replace with:

> Predictors like ESM2 [4], AlphaMissense [5], and EVE [6] score a mutation by how unusual it looks against evolutionary patterns learned from millions of protein sequences. A mutation at a position evolution has held fixed scores as damaging. This works because most well-studied disease proteins fold into a stable shape, and the positions evolution holds fixed are the ones that shape depends on.
>
> Intrinsically disordered proteins have no stable shape. Their sequences drift, and individual positions are rarely conserved. Some still cause disease the familiar way, by losing function. Others cause disease by gaining one: the mutant protein acquires a new harmful behavior, typically aggregating where it should not, and the residue responsible need not be conserved at all. What matters instead is where it sits, for instance inside a nuclear localization signal that determines whether the protein stays in the nucleus.
>
> If that account is right, conservation-based predictors should work on the loss-of-function cases and fail on the gain-of-toxic-function ones. That is the question the workflow asks, and the answer is that they do (§4.4).
>
> The workflow runs in five stages (Table 1), across 3,409 missense variants in 22 genes from a content-hashed ClinVar snapshot, evaluated by leave-one-gene-out cross-validation so that no gene is ever tested on a model that saw it.
>
> Two features make this a useful audit target rather than a convenient one. It runs a heterogeneous AI stack, three generative predictors plus three non-generative baselines plus AI-assisted code and prose, which is the configuration where a single disclosure line conveys least. And it is ours, which matters more than it may appear: a retrospective audit needs the superseded scripts, intermediate outputs, and internal audit notes that published work does not deposit. Auditing a third party's paper would demonstrate the opposite of this paper's claim.

The final paragraph is our answer to R4.3, placed where readers see it rather than only reviewers.

## E11 — Line 83 — R1.3, R3.1

Delete. This is the paragraph mapping the workflow onto the five record types, which do not exist.
Replace with Table 1:

> **Table 1. Workflow stages.**
>
> | Stage | What it does | Implementing script | Status |
> |---|---|---|---|
> | S1 Curate | ClinVar snapshot to clean-labeled variant set | `01_build_variant_set.py` | canonical |
> | S2 Score | Six predictors, per variant | `06_approach_c_esm2.py` | scoring canonical; CV block superseded |
> | S3 Model | Region annotation plus ESM2 LLR, two features | `10_two_step_predictor.py` | canonical |
> | S4 Evaluate | LOGO-CV, bootstrap CIs, permutation controls | `10`, `11`, `17` | canonical |
> | S5 Draft | AI-assisted prose, figures, methods | chat sessions | canonical |
> | | Single-model baseline, superseded at S4 | `04_approach_a_xgboost.py` | withdrawn (F2) |
> | | Mechanism-aware ensemble, superseded at S3 | `08_mechanism_aware_model.py` | exploratory (F3) |

## E12 — Line 85 (heading) — R3.2, R5.9

> ### 4.2 What the audit found

## E13 — Line 87 — R3.2

States the mechanism Reviewer 3 asked for and stops crediting the schema with the finding.

> The audit worked from the decision list. Enumerating the workflow's consequential decisions produced eight, three covering the workflow itself (dataset curation, predictor selection, canonical-model selection) and five recording the disposition of a defect. Each carries a verification status, and those still standing as unverified were the work list. Working that queue, rather than reading the code start to finish, is what put attention on the five defects below. All five had survived unit tests, code review, and multiple drafts.

## E14 — Line 89 (finding 1) — R1.3, R5.10, plus factual correction

The submitted text says 170 of 259; the file holds 255 HTT rows. Adds the latent-defect
disclosure. Drops the repeated provenance sentence, now in Table 2.

> **A truncated model silently returned zeros.** (S2) The HTT protein is 3,142 residues; ESM2 accepts 1,022 tokens. Rather than failing, the inference wrapper returned default values for variants whose context could not be tiled: log-likelihood ratio 0.0, entropy 0.0, rank 10. This affected 170 of 255 HTT variants, and all of them entered the pooled AUROC as real measurements. The signature was visible once looked for: identical default values repeating across consecutive positions, which computed features never do. HTT was excluded, leaving the 3,409-variant, 22-gene evaluable set the paper reports.
>
> A residual weakness is worth stating. The fabrication is triggered by residue position, but every guard in the pipeline is triggered by gene name. The two coincide only because HTT is the sole protein in the panel above 1,022 residues, the next longest reaching 915. Adding one longer protein would make every gene-name filter silently insufficient while still appearing correct.

## E15 — Line 91 (finding 2) — R1.3, factual correction

The submitted line says scripts 04 and 06 are both superseded. They are not equivalent: 04 has no
consumers, while 06's feature table is read by seventeen files including every canonical path. A
reviewer who greps the feature table finds this in a minute.

> **Skipped cross-validation folds were scored as predictions of zero.** (S4) The early cross-validation code allocated a prediction array of zeros per fold and wrote into it only where both classes were present. Folds skipped for having a single class left their zeros in place, and the pooled AUROC consumed them as predictions. The effect was small on the full set and material on mechanism-stratified subsets, where some folds contain no benign variants at all. Comparing those outputs against the canonical bootstrap distribution exposed the gap.
>
> The two affected scripts were retired differently, and the distinction matters. The single-model baseline was withdrawn entirely; nothing downstream reads its outputs. The ESM2 script was not, because its cross-validation block and its scoring block are separate: the defective cross-validation was replaced, while the feature table it writes remains the canonical input to the paper-facing predictor, the bootstrap intervals, the predictor comparisons, the permutation control, and every main figure. Retiring the script wholesale would have retired the paper's own inputs. What was superseded is a block, not a file.

## E16 — Line 93 (finding 3) — R1.3, R5.10

> **The ensemble was reading the answer.** (S3) An exploratory ensemble routed each test gene to a sub-model chosen by that gene's disease mechanism. Under leave-one-gene-out cross-validation the mechanism of the held-out gene is exactly what is not known, so its reported AUROC of 0.738 is unachievable prospectively. Checking what the routing function could see at test time found it reading a mechanism field that blinding should have withheld. The ensemble was demoted to exploratory and excluded from every headline claim.

## E17 — Line 95 (finding 4) — R5.6, R5.10

> **Numbers in the draft did not match the files they came from.** (S5) Tracing each reported value to its canonical output found three discrepancies. A pooled ESM2 AUROC given as 0.70 was the VUS-included figure; the clean-label value is 0.772. A comparison quoting 0.784 against 0.676 mixed the VUS-included set with a five-feature model, not the two-feature model the surrounding text described; corrected, it reads 0.873 against 0.748 clean-label, with the VUS-included figures disclosed as sensitivity. And loss-of-function performance described as comparable at 0.76 for both methods was in fact 0.813 against 0.650, a degradation rather than a tie. That last one is the case for tracing every number rather than the surprising ones: it read as unremarkable and reversed the finding.

## E18 — Line 97 (finding 5) — R5.10

> **A probability was reported that the method could not produce.** (S5) A draft gave P(two-step > ESM2) = 1.000 from 1,000 bootstrap resamples. A resample of size n cannot estimate a probability below 1/n, so 0.999 is the ceiling. Corrected to P < 0.001.

## E19 — Line 99 — R3.2, R5.2, R3.10 (self-identified)

Adds the domain-independence point Reviewer 3 valued, the post-review adapter defect, and Table 2.

> The same pass caught three lesser problems, each now disclosed with its consequence: a methods table naming IUPred2A where metapredict was used, with a window reported as ±10 residues rather than ±15; bootstrap failures for genes with too few minority-class variants; and class imbalance disclosed only in aggregate rather than per gene.
>
> Three of the five are domain-independent. A model returning defaults instead of failing, an array initialized to a value that is also a legal prediction, and a test-time feature that encodes the label are failures available to any computational scientist.
>
> A sixth defect surfaced during revision, after review. The session-log adapter derived its search path by replacing path separators, but the tool it reads also collapses underscores and dots, so the adapter could not locate sessions for any project whose path contained an underscore, including this case study. It shipped because the test suite built its fixtures with the same wrong transformation: fixture and implementation agreed, and a test that reproduces the defect it guards cannot fail. Correcting the adapter caused four passing tests to fail, which is how the defect became visible. This is the fourth domain-independent failure in this list and the least visible, since every conventional signal said the code was covered.
>
> **Table 2. Where each finding is recorded.**
>
> | Finding | Stage | Disposition | Audit document | Corrected output |
> |---|---|---|---|---|
> | Context-window defaults | S2 | locus excluded, metrics recomputed | 2026-02-20 audit, finding 3 | evaluable-set CSV |
> | Zero-filled skipped folds | S4 | baseline withdrawn, CV block replaced | 2026-02-20 audit, findings 2, 5 | `bootstrap_cis.csv` |
> | Mechanism-label leakage | S3 | demoted to exploratory | 2026-02-20 audit, finding 4 | `results_two_step.csv` |
> | Untraced numerical claims | S5 | three values corrected | `CRITICAL_EVALUATION.md` | canonical CSVs |
> | Impossible probability | S5 | corrected to P < 0.001 | `CRITICAL_EVALUATION.md` §3.3 | `bootstrap_cis.csv` |
> | Self-confirming adapter test | tooling | adapter corrected, fixtures rebuilt | revision audit, `docs/audit-record-corrections.md` | regression test |
>
> Each row is one Decision in the deposited record, with Events citing the script lines, the audit document, and the corrected output.

## E20 — Line 101 (heading) — R5.9

> ### 4.3 The record itself

## E21 — Line 103 — R5.3, R5.4

Adds the reference-audit rationale Reviewer 5 asked for twice.

> *Verifiability.* Every quantitative claim traces to a specific cell in a canonical output file; the numerical-audit log records ten headline numbers with their source references and outcomes. Citation resolution succeeded for all references in the current draft.
>
> We audited every reference, not only those an AI suggested. The boundary between AI-suggested and author-supplied citations in a drafted bibliography is not recoverable after the fact, and reconstructing it would cost more than checking all of them. A reference is also not AI-authored content: each was read and assessed by an author before citing, and the record holds the suggestion and the human verification as separate entries. Attribution for a citation belongs to the author who chose to stand behind it.

## E22 — Line 105 — R3.8 (self-identified)

The submitted line claims the session logs were "deposited under access control". No such deposit
exists, and the logs no longer exist either. This is the most important single correction in the
patch.

> *Accountability.* Authorship is disclosed at the granularity of section and task. The pipeline (variant curation, feature engineering, cross-validation, mechanism-stratified analysis, permutation controls) is attributed to H.R.; schema design, AI-assisted drafting, and figure preparation to B.K. Each Event and Decision carries an Actor identified by ORCID.
>
> The record does not contain the coding-assistant session logs. They existed when the audit was constructed and were destroyed by the tool's default retention policy before this revision; their absence was confirmed on 2026-08-27. The audit is therefore capture tier 1, not tier 2, and the deposited artifact has been corrected to say so. This is a real limitation and it is the kind the capture tier exists to make visible.

## E23 — Line 107 — R5.8, R3.6, R3.10 (self-identified)

Adds the re-execution defect found by our own revision audit and keeps the byte-reproducibility
disclosure. Version DOI becomes a placeholder until re-deposit.

> *Reproducibility.* The pipeline is deposited (§ Resource availability). The ClinVar snapshot is pinned to February 2026 with a content hash and the ESM2 checkpoint to `esm2_t33_650M_UR50D`; AlphaMissense and EVE access dates and provider-stated retention policies are recorded. Recomputation of the headline AUROCs was verified on 2026-03-16 and reproduced them to three decimal places.
>
> That verification ran in the authors' environment. During revision we found that the deposited copy could not have reproduced it: the first script in the chain reached a feature-computation module through a hardcoded absolute path into a separate, undeposited project, so a third party cloning the deposit would have failed at the first step. The module is now vendored into the repository with provenance, and self-containment was confirmed by running the pipeline from a clean export with the external path removed. No reported number is affected, because the outputs of that script were deposited; what was broken was re-execution, which is the property this section claims.
>
> One property the deposited audit record does not have is byte-level reproducibility: re-running the audit script regenerates fresh identifiers, so the output differs from the deposited copy while carrying identical content. The deposited copies are the reference and are checksummed. This is the §2.3 argument applied to the record itself, and the repository states it rather than leaving a reader to discover it.

## E24 — Line 111 (§4.4) — R1.5, R5.6

Reviewer 1 noted Figure 2 was never cited and asked what the numbers signify.

> The prediction in §4.1 holds, and the separation is clean (Fig 2).
>
> Conservation-based scoring works where the structural assumption holds and fails where it does not. ESM2 reaches AUROC 0.813 on loss-of-function structured genes (LMNA, SOD1, CRYAB, VCP) and 0.813 on toxic-aggregation amyloid genes (SNCA, TTR, PRNP, IAPP), but 0.493 on gain-of-toxic-function non-amyloid genes (FUS, TARDBP, HNRNPA1, TIA1, HNRNPA2B1, EWSR1, TAF15), which is chance. A predictor at 0.493 is not weakly informative; it carries no information about which variants cause disease.
>
> The failure is not specific to one model. AlphaMissense reaches 0.620 on that subset, falling to 0.398 with FUS excluded, and EVE reaches 0.342, below chance. Three independently trained generative architectures fail the same subset, which points at the shared assumption rather than any one implementation.
>
> Where sequence conservation carries no signal, position does. Binary membership of a curated functional region alone reaches 0.792 overall, and combining it with the ESM2 score reaches 0.873. On the non-amyloid subset the two-step model recovers to 0.822, a gain of 0.329 (bootstrap 95% CI [0.305, 0.441], P < 0.001), while degrading the loss-of-function structured subset to 0.650. That trade-off is disclosed rather than averaged away.
>
> The FUS case is the sharpest instance: membership of the PY-nuclear localization signal alone predicts pathogenicity at 0.916, and a 10,000-permutation control against length-matched random regions gives p = 0.002, so the signal is specific to that region rather than to any region of that size.

## E25 — Line 113 (heading) — R1.4

> ### 4.5 Cost, and what the record cannot certify

## E26 — Line 115 — R1.4, R2.2, R3.2, R3.3

Withdraws the sub-linear scaling claim explicitly and replaces it with measured-in-hours cost.

> Building the pipeline took approximately 520 person-hours, six months at roughly twenty hours per week, from variant curation through the first draft of results. The retrospective audit took approximately 60 person-hours, four weeks at roughly fifteen hours per week, covering both audit passes, the corrections they required, and construction of the record. The audit added roughly twelve percent to the cost of the work, about one hour of checking for every eight of development.
>
> Both figures are author estimates rather than measurements, reported at capture tier 0 accordingly. The evidence that would have measured them was the session logs described in §4.3. That loss is itself informative: a record that depends on the retention behavior of the tools it documents is not durable, which is the argument for constructing and depositing an audit artifact rather than assuming the underlying logs persist.
>
> The 60 hours includes authoring such a record for the first time, with no existing tooling and while the vocabulary was still empty, so it is an upper bound on the recording cost rather than a steady-state figure. We make no claim about how that cost scales with workflow complexity; an earlier version of this paper did, on the strength of a single observation, and that claim is withdrawn.

## E27 — Line 117 — R5.9

Remove "AIVS-VAR" twice.

> The record also cannot certify substance. It shows that the FUS PY-NLS is annotated as residues 502 to 526 with a stated literature source, and that a permutation control returned p = 0.002 for that annotation. It does not establish that 502 to 526 is the correct boundary. The record makes the verification chain visible; it does not replace it.

## E28 — Line 123 (Figure 1 caption) — R3.1, R5.11

Must match the redrawn figure and the rewritten §3.

> **Figure 1. The AIVS record graph.** Events carry an Actor, an action, and an optional hashed payload. Evidence groups Events. Decisions name a responsible Actor, cite Evidence, and carry a verification status. Claims point to the manuscript locations they support. The kernel is closed at these entity types; the vocabularies for actions and decision types are open and grow through SchemaDelta proposals from completed audits.

## E29 — Line 127 (Figure 2 caption) — R1.5

Explains the inverted distribution rather than only reporting it.

> **Figure 2. Conservation-based prediction is mechanism-dependent.** (A) Per-gene ESM2 AUROC for 22 genes grouped by disease mechanism, with bootstrap 95% CIs; the dashed line marks chance. Gain-of-function non-amyloid genes fall to chance while loss-of-function structured genes cluster above 0.65. (B) ESM2 score distributions for benign or uncertain versus pathogenic variants in each group. Pathogenic variants score higher in loss-of-function structured genes (Δμ = +2.98) and lower in gain-of-function non-amyloid genes (Δμ = −0.87), so the score is not merely uninformative there but inverted. (C) Four predictors on the non-amyloid subset. Functional-region membership outperforms all three conservation-based predictors. EVE was unavailable for FUS.

## E30 — Line 133 — R4.5

States the contribution as the record rather than the format, answering the "homespun JSON layer"
remark.

> The contribution is a documentation layer between disclosure and full workflow capture. Disclosure without verification lets fabrications enter print unless a reviewer happens to notice. An audit record makes the verification of each AI-assisted claim explicit, so a missed check is visible in the trail rather than invisible. The contribution is the record and the discipline of constructing it, not the serialization format, and not an enforcement mechanism.

## E31 — Lines 135 and 137 — R2.C7, R3.2

Cuts the agentic-platform paragraph from roughly 230 words to two sentences, freeing three
references, and replaces the reach-limitation paragraph with an explicit limitations statement
including the one Reviewer 3 identified.

> The case for it grows with agentic platforms, which compose many generative invocations into one artifact and emit internal logs that could populate such a record [7]. That mapping is not built here. What this paper establishes is narrower and prior to it: that the record is constructible for a genuine workflow, at what cost, and that constructing it caught errors disclosure would not.
>
> Two limitations bound the claim. The evidence is one workflow, self-audited, and a single case cannot separate what the schema contributed from what a careful auditor would have found anyway. And the practice is author-side: it depends on authors choosing to produce a record and readers choosing to inspect it.

## E32 — Line 143 (Conclusion) — R2.C7

> The question is not whether AI use should be permitted but how AI-assisted work can be documented to a standard science can defend. VAR names what such documentation must make checkable; AIVS records it; the case study shows the record is constructible for a real workflow, costs roughly twelve percent of the work it documents, and surfaced five defects that had survived ordinary review. As generative components compose into longer chains, the distance between their internal complexity and the auditability of their published outputs widens. Closing it does not require a new institution, only a record that says what was done and who checked it.

## E33 — Line 149 (Experimental procedures) — R3.7, factual corrections

Version corrected to v0.2.1, manifest filename corrected, capture tier stated, ESM2 loading path
corrected (the code uses HuggingFace `transformers`, not `fair-esm`).

Replace with the Experimental procedures block of `var_manuscript_cise_r1.md`.

## E34 — Line 157 (Resource availability) — R3.6, R5.1

The submitted statement lists four items the deposit does not contain, which both Reviewer 3 and
Reviewer 5 verified independently.

Replace with the Resource availability block of `var_manuscript_cise_r1.md`. Version DOIs are
placeholders until re-deposit; concept DOIs are unchanged.

## E35 — Lines 163 to 185 (References) — R1.6, R3.5

Remove `[8]` Robin, `[9]` Kosmos, `[10]` The AI Scientist, following the §5 trim. Renumber `[11]`
to `[8]` and `[12]` to `[9]`. Add `[10]` PROV-O, `[11]` RO-Crate, `[12]` MIAME. Total stays at 12.

In-text consequences: line 25 and line 135 lose the dropped citations (handled in E3 and E31);
line 69 no longer exists (E8); the PROV-AGENT citation moves to `[9]` inside the new §3.5.

Add DOIs to every entry. **Do not fabricate any DOI.** Resolve each against CrossRef and leave
unresolved entries marked.

Correct entry `[2]`, whose title is truncated. In full it reads:

> Naser MZ. How LLMs cite and why it matters: a cross-model audit of reference fabrication in AI-assisted academic writing and methods to detect phantom citations. arXiv:2603.03299, February 2026.

Identifier verified against the arXiv landing page on 2026-09-08: the paper was submitted 7 February
2026 and carries a 2603-series identifier because its browse context is 2026-03; the apparent month
mismatch is an announcement boundary, not an error.

MIQE and ARRIVE remain uncited by author decision, named in text only, because the twelve-reference
cap is full and every substitution candidate is load-bearing.

## E36 — Line 195 (Generative AI use) — R3.7

Reviewer 3: the manuscript required of others what it did not supply itself.

Replace with the Generative AI use block of `var_manuscript_cise_r1.md`. Model identifiers and
date ranges are placeholders, recoverable from `~/.claude.json` and `history.jsonl` on the
compute host.

---

## Placeholders that must be resolved before submission

| Placeholder | Where | Source |
|---|---|---|
| Reference DOIs, all 12 (RESOLVED, see note below) | E35 | CrossRef resolution |
| Two Zenodo version DOIs | E34 | minted by deposit repair phase 2 |
| Model identifiers, date ranges | E36 | `~/.claude.json`, `history.jsonl` |
| Word count | final | after render |
| ~~Decision count in §4.2 opener~~ (RESOLVED, see open item 1) | E13 | deposited artifact, or omit |

**RESOLVED by Job 4: reference DOIs.** Ten of twelve carry DOIs. References 1 (NIH notice) and 10
(W3C PROV-O) are document types that are not DOI-registered and carry verified live URLs instead;
this is a property of the sources, not a failed lookup. PROV-AGENT now has a publisher DOI,
10.1109/escience65000.2025.00093, IEEE eScience 2025, pages 467 to 473, to be cited as primary with
arXiv:2508.02866 secondary.

## Open items requiring an author decision

1. **§4.2 decision count.** E13 currently states no number. If one is wanted it must come from the
   deposited artifact, which holds eight top-level decisions, not from the drafting.
   **RESOLVED.** Resolved by author decision, eight decisions stated, three workflow and five
   failure-disposition, with no claim about the unverified count.
2. **"Superseded" in Table 2.** The deposited record's dispositions never use the word. Either add
   the disposition to the record or align the table's wording to the artifact.
   **RESOLVED.** Job 2 added asymmetric dispositions to the record; Table 2 row 2 already matches.
3. **Two HTT rows in `table_s1_regions.csv`.** A hardcoded literature annotation, no computed
   quantity. A supplementary table listing a gene the paper excludes invites a question. Drop or
   footnote.
   **RESOLVED.** Job 3 removed them and fixed the generator defect in `16_supplementary_tables.py`,
   hoisting an `EXCLUDED_GENES` constant so the removal is reproducible; documented in the idp
   README.
4. **MIQE and ARRIVE.** Named in text but uncited, because the 12-reference cap fits only MIAME. If
   you would rather cut something else to fit all three, say which.
   **RESOLVED.** Resolved by author decision, MIAME cited as the single exemplar, MIQE and ARRIVE
   named in text, cap explained at row 1.6 of the response letter.
5. **Naser reference arXiv identifier.** Verify 2603.03299 against its arXiv landing page. The
   identifier implies March 2026, but arXiv reports the posting as February 2026. This matters more
   than usual because that reference is cited for the prevalence of fabricated citations.
   **RESOLVED.** Verified against the arXiv landing page on 2026-09-08: the paper was submitted
   7 February 2026 and carries a 2603-series identifier because its browse context is 2026-03; the
   apparent month mismatch is an announcement boundary, not an error.

All five items above are resolved. The only item still open is the two Zenodo version DOIs at E34,
which await the deferred minting pass.
