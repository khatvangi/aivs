# Summary of Changes

**CiSE-2026-06-0105**, "Auditing AI-Assisted Research: The VAR Framework and AIVS Schema"

Every change below is keyed to the reviewer comment that prompted it. Thirty-four reviewer
comments were addressed; three were declined, with reasons given in the response letter.
One further defect was found during revision and is disclosed rather than quietly fixed.

---

## Structural changes

### Section 3 respecified to the schema that exists (R1.1, R2.1, R2.3, R3.1, R5.2)

Reviewer 3 observed that §3.1 specified five record types (Source, Invocation, Evaluation,
Curation, Deposition) while §4 described the constructed record entirely in terms of Actors,
Events, and Decisions, and that the relationship was never stated. This was correct. The five
types were designed on paper and never implemented; the released code implements a different
kernel, and the audit was built on that kernel.

Reviewer 3 offered two remedies. We have taken the second: §3 now specifies the model actually
built. The kernel is Actor, Event, Evidence, Decision, Claim, and AuditArtifact. The five
workflow-stage terms survive as open-vocabulary decision types, which is what the code already
treats them as. Figure 1 is redrawn accordingly.

Two consequences worth noting. First, §4 and §3 now use one vocabulary. Second, two features of
the built kernel that the submitted §3 never mentioned do substantive work in this revision:
capture tier (§3.2), which answers Reviewer 2's question about level of effort, and the
default-unverified verification status (§3.1), which answers Reviewer 3's question about how the
schema directed the audit.

### Central claim narrowed (R3.2)

The submitted abstract said AIVS caught five classes of error, while §3.2 said AIVS performs no
verification and §4.2 attributed every finding to manual work. The abstract, §4.2, §4.5, and the
Experimental procedures now state the supportable claim: a structured audit found the defects,
and the schema recorded them and directed attention to them. The mechanism is stated explicitly
in §3.1 and §4.2, since Reviewer 3 asked for it: enumerating decisions produces a queue of
unverified ones, and that queue is the audit's work list.

### Scaling claim withdrawn, cost reported (R1.4, R2.2, R3.3)

The third claim of the submitted §4.5, that verification effort scales sub-linearly with
manuscript complexity, rested on one observation with no measurement. It is withdrawn, and the
withdrawal is stated in the text rather than performed silently.

In its place §4.5 reports approximately 60 person-hours of audit against approximately 520 hours
of pipeline development, roughly twelve percent overhead. Both are author estimates reported at
capture tier 0, because the evidence that would have measured them no longer exists (below).

### Threat model and audience stated (R3.4, R5.7)

New material in §3.4 states that the threat model is honest error rather than misconduct, that
the record is author-side and not tamper-evident, and that authors produce the record while
readers, reviewers, and downstream researchers consume it. Venue policy is explicitly out of
scope. A short version appears at the end of §1 so a reader meets the boundary early.

### Positioning against existing standards (R3.5)

New §3.5 addresses W3C PROV-O and RO-Crate, including the Workflow Run profile, alongside
PROV-AGENT. The argument is that these assume instrumentation at execution time and are the
better tool where it exists, while AIVS addresses the case where it was absent; that the unit of
record differs (methodological decision rather than execution step); and that capture tier
expresses how much was reconstructed rather than captured, which a profile of an
instrumentation-assuming standard cannot express.

---

## Case study

### §4.1 rewritten for a general reader (R1.2, R4.1, R5.5)

Reviewer 4 reported being unable to comprehend the goal of the analysis. The submitted §4.1
stated the question in the vocabulary of its answer. It now builds the question in plain terms:
what conservation-based predictors assume, why intrinsically disordered proteins violate that
assumption, why gain-of-toxic-function variants should defeat them specifically, and what
therefore should be observed. The closing paragraph states why the workflow is our own, which is
the substance of our response to Reviewer 4's recommendation that we use a third-party workflow.

### Script numbers replaced by named stages (R1.3)

New Table 1 names five workflow stages, S1 through S5, and maps each to its implementing script
and status. Section 4.2 now references stage names. Superseded scripts appear in the same table
with the defect that retired each, so the audit's outcome is legible at a glance.

### §4.2 restructured (R3.2, R4.2, R5.2, R5.6, R5.10)

The submitted §4.2 repeated a near-identical provenance sentence after each finding, which
contributed to the density both Reviewer 4 and Reviewer 5 identified. That material now sits in
Table 2, one row per finding, mapping each to its disposition, audit document, and corrected
output. The prose carries only the account of what went wrong. A closing paragraph identifies the
three domain-independent defects, which Reviewer 3 noted are the material most useful to this
readership.

### §4.4 given interpretation, Figure 2 now cited (R1.5, R5.6)

The submitted §4.4 was a sequence of numbers with no reading. It now leads with what the numbers
mean, states what an AUROC of 0.493 does and does not imply, notes that three independently
trained architectures fail the same subset (which points at the shared assumption rather than an
implementation), and explains the FUS permutation control. Figure 2 is cited at first mention.
The figure caption now explains the inverted score distribution rather than only reporting it.

### Reference-audit rationale added (R5.3, R5.4)

Section 4.3 now states why all references were audited rather than only AI-suggested ones: the
boundary is not recoverable after the fact and reconstructing it would cost more than checking
everything. It also states that a reference is not AI-authored content, that each was read and
assessed by an author before citing, and that the record holds the AI suggestion and the human
verification as separate entries.

---

## Corrections of fact

### A number in §4.2 was wrong

The submitted text reported 170 of 259 HTT variants receiving fabricated defaults. The file holds
255 HTT rows, so it is 170 of 255. The count of 170 was confirmed two independent ways during
revision.

### Two scripts were described as superseded together, and are not equivalent

The submitted line stated that scripts 04 and 06 are superseded. Verification during revision
showed these are not symmetric. Script 04's outputs have no consumers and it is genuinely
withdrawn. Script 06's feature table is read by seventeen files, including the canonical
predictor, the bootstrap intervals, the permutation control, and every main figure; only its
cross-validation block was defective and replaced. Describing both as superseded would have
described the paper's own canonical inputs as retired. Section 4.2 now distinguishes them, and
the point that what was superseded is a block rather than a file is used to illustrate why the
audit unit is the decision.

### The data availability statement described a deposit that did not contain what was claimed (R3.6, R5.1)

Reviewer 3 listed four items absent from the cited deposit and Reviewer 5 reported being unable
to find records discussed in the manuscript. Verification on 2026-08-27 confirmed both were
correct: figure-generation scripts and the environment manifest were absent, the AIVS record was
in the sibling repository rather than the one cited, and the deposit was frozen at a commit well
behind the described work. The deposits have been repaired and re-released, and the statement now
describes what is actually there, including an explicit pointer to where the verification record
lives. Both repositories now carry a README mapping each manuscript claim to its supporting file.

### Manuscript line 105 claimed a deposit that does not exist (self-identified)

The submitted §4.3 stated that agent-session logs were deposited under access control. No such
deposit exists. The logs existed when the audit was constructed and were destroyed by the tool's
default retention policy; their absence was confirmed on 2026-08-27. Section 4.3 now says this
plainly, the deposited audit artifact has been corrected from capture tier 2 to tier 1, and the
loss is used in §4.5 as evidence for the paper's own argument that a constructed record outlives
the logs beneath it.

### The paper's own AI-use disclosure named no tool, model, or version (R3.7)

Reviewer 3 noted that the manuscript required of others what it did not supply itself. The
disclosure now names the tools, the interfaces, the date ranges, and the model identifiers
recoverable from surviving configuration, and states its own capture tier. Where the record is
incomplete it says so and says why, rather than omitting the field.

### The deposited audit record is not byte-reproducible

Re-running the audit script regenerates fresh identifiers, so its output differs from the
deposited copy while carrying identical content. Section 4.3 states this and the repository
documents it. The deposited copies are the checksummed reference. This is the §2.3 argument
applied to the record itself.

### A latent defect is disclosed although nothing is currently wrong

The context-window fabrication is triggered by residue position; every guard in the pipeline is
triggered by gene name. These coincide only because HTT is the sole protein in the panel above
the model's token limit. Adding one longer protein would make every filter silently insufficient
while still appearing correct. Section 4.2 states this.

---

## Prose and presentation

### Section 2.2 rewritten (R4.2)

Reviewer 4 quoted the Accountability paragraph as his example of the manuscript's "word salad"
quality. It defined a term using four further terms and gave no instance. It now opens with a
one-sentence definition and a concrete case, explains why the byline no longer does this work,
and states the granularity and the purpose in short sentences.

### Section 2.3 rewritten (R5.8)

Reviewer 5 asked how knowing when a model was used could let anyone reproduce a result. The
submitted §2.3 did not engage this. It now states the objection first, then separates the
deterministic pipeline (which reruns from pinned inputs) from generative invocation (which does
not and cannot), and states that the target is deposit and inspection rather than regeneration.

### "AIVS-VAR" removed (R5.9)

Reviewer 5 asked what distinguishes AIVS from AIVS-VAR. Nothing does; the compound was an
artifact of earlier drafts. It is removed from the manuscript, and from the audit scripts and
deposited records.

### Introduction reframed (R2.C4, R3.C4, R4.4)

Reviewer 4 asked for evidence of the problem beyond the fact that LLMs exist. The introduction
now opens with three of the defects this paper documents, stated concretely, before any
discussion of AI adoption. The quantitative evidence follows, and the thesis, contribution, and
threat model are stated within the first section.

### Discussion trimmed (R2.C7, R4.5, R4.6)

The agentic-platform paragraph is reduced from roughly 230 words to two sentences. It described
four platforms and a mapping that is not built, which is aspirational material in a paper whose
argument is what has been demonstrated. Section 5 now states the contribution as the record and
the discipline of constructing it rather than the serialization format, which is the substance of
our response to Reviewer 4's remark about a "homespun JSON layer", and adds an explicit
limitations paragraph noting that a single self-audited case cannot separate the schema's
contribution from the auditor's.

### Figures regenerated (R5.11)

Both figures are regenerated with the overlapping text corrected.

---

## References (R1.6)

References [9] Kosmos, [10] The AI Scientist, and [8] Robin are removed, following the trimming
of the agentic-platform discussion; one exemplar is retained. Three references are added: PROV-O
and RO-Crate for §3.5, and MIAME for the minimum-information-standard tradition. The total
remains at the twelve-reference limit.

Reviewer 1 asked for references for MIAME, MIQE, and ARRIVE. The twelve-reference cap does not
accommodate all three; MIAME is cited as the exemplar and the other two are named in the text.

DOIs have been added for every reference, as required.

---

## Word count

The revised manuscript is approximately [WORD COUNT] words including the two tables counted as
word-equivalents, within the 6,250-word limit.
