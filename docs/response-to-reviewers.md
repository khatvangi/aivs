# Response to Reviewers

**Manuscript:** CiSE-2026-06-0105, "Auditing AI-Assisted Research: The VAR Framework and AIVS Schema"

We thank the five reviewers for the time they spent on this manuscript, and particularly those
who opened the deposits and checked them against the text. Two reviewers did so independently and
both found the deposits wanting. They were right, and finding that out was worth more to this
paper than any amount of favourable comment.

Four changes are structural, and we summarise them here before the point-by-point.

**Section 3 now specifies the schema that exists.** Reviewer 3 observed that §3 defined five
record types while §4 described the record in a different vocabulary, and that the relationship
was never stated. This was correct: the five types were designed on paper and never implemented,
and the audit was built on a different kernel. Reviewer 3 offered two remedies and we have taken
the second, revising §3 to specify the model actually built.

**The central claim is narrowed.** The abstract credited the schema with catching errors that the
rest of the paper attributed to manual auditing. It now claims what is supportable, and states
the mechanism by which the schema's structure directed the audit.

**Cost is reported and the scaling claim is withdrawn.** Approximately 60 person-hours of audit
against approximately 520 hours of development, roughly twelve percent overhead.

**The deposits are repaired.** They did not contain what the manuscript said they contained.

Three comments are declined, with reasons: R4.3, R4.5, and R5.4. One further defect was found
during revision, is disclosed in the manuscript, and is described at R3.8 below.

---

## Reviewer 1

**1.1. Section 3.1 describes the record types, but it is not clear how they map onto the files in
the supplemental data. How does the AIVS record graph in Figure 1 get instantiated for the case
study?**

They did not map, and Figure 1 was not instantiated. The five record types in the submitted §3
were never implemented; the deposited audit was built on a different kernel. Section 3 has been
rewritten to specify the built kernel (Actor, Event, Evidence, Decision, Claim, AuditArtifact) and
Figure 1 redrawn to match. New Table 2 maps each of the five findings to its Decision in the
deposited record, the audit document that supports it, and the corrected output file. Both
repositories now carry a README mapping each manuscript claim to the file that supports it.

**1.2. A clear description of the research workflow that is more accessible to researchers from
other domains would be useful in §4.1.**

Section 4.1 is rewritten. It now states what conservation-based predictors assume, why
intrinsically disordered proteins violate that assumption, and why gain-of-toxic-function
variants should defeat them specifically, before naming any method. Reviewer 4 raised the same
point more sharply and we address it there.

**1.3. Numbered scripts are referenced (e.g. Script 04) and it is not clear what they do.
Perhaps a figure with analysis tasks that could be referenced in §4.2.**

Adopted. New Table 1 names five workflow stages, S1 through S5, maps each to its implementing
script, and lists the superseded scripts alongside the defect that retired each. Section 4.2 now
references stage names rather than script numbers.

**1.4. How long did the manual audit process take in comparison to the agentic workflow itself?**

Now reported in §4.5: approximately 60 person-hours of audit against approximately 520 hours of
pipeline development, roughly twelve percent overhead, about one hour of checking per eight hours
of building. Both figures are author estimates rather than measurements, and the manuscript says
so. The evidence that would have measured them, the coding-assistant session logs, was destroyed
by the tool's default retention policy before this revision. We report that loss rather than
concealing it, and §4.5 treats it as an argument for depositing a constructed record rather than
relying on logs persisting.

**1.5. Section 4.4 could benefit from context for non-experts. Figure 2 does not seem to be
referenced. What is the significance of the numerical results?**

Section 4.4 is rewritten to lead with interpretation. It now states what an AUROC of 0.493
implies (not weak information but none), notes that three independently trained architectures
fail the same subset and what that points at, and explains the permutation control. Figure 2 is
cited at first mention, and its caption now explains the inverted score distribution rather than
only reporting it.

**1.6. Include references for the minimum information standards described in §3 (MIAME, MIQE,
ARRIVE).**

Partly adopted. MIAME is now cited. The twelve-reference limit does not accommodate all three
alongside the two provenance standards Reviewer 3 asked us to address, so MIQE and ARRIVE are
named in the text without citation. We would add them if the limit permits.

**1.C5. Organization could be improved.**

Addressed through 1.1 to 1.3. The vocabulary mismatch between §3 and §4 was the main source of
the difficulty.

---

## Reviewer 2

**2.1. The AIVS schema in §3 is difficult to understand and it is unclear how it could be
implemented in a general research workflow.**

The root cause was the same defect Reviewer 3 identified: §3 specified a schema that was never
built, so no reader could have connected it to the demonstrated record. Section 3 now specifies
the built kernel, which is smaller and has fewer moving parts.

**2.2. The section leaves out an implementation discussion that would help to understand its
impact and level of effort required to use.**

This was a real omission and we take it as the substance of your recommendation. Two additions
respond to it. New §3.2 specifies capture tiers 0 to 3, which state what evidence a given level of
instrumentation supports: tier 0 is a manual log from memory, tier 3 adds environment metadata.
The point of grading rather than requiring is that an author with no instrumentation can still
produce a usable record, which is the common case. New cost figures in §4.5 give the level of
effort in hours.

**2.3. It was unclear how AIVS was used in the case-study workflow.**

Section 4.2 now names, for each finding, the Decision it produced in the record, and Table 2 maps
each to its audit document and corrected output. Section 4.2 also opens by describing how the
audit proceeded: enumerating decisions produces a queue of unverified ones, and working that
queue is what put attention on the defects.

**2.C4. The introduction thesis could be improved.**

Section 1 now opens with three of the documented defects, stated concretely, before any
discussion of AI adoption, and states the thesis, the contribution, and the threat model within
the section.

**2.C7. Length could be improved.**

The agentic-platform discussion in §5 is cut from roughly 230 words to two sentences, and the
§4.1 record-type mapping paragraph is removed. Net growth is small and the manuscript remains
within the 6,250-word limit.

---

## Reviewer 3

**3.1. Section 3.1 defines five record types; §§4.1 to 4.3 describe the record entirely in terms
of Decisions, Events, and Actors. The authors should either show a complete record instantiating
the five types, or revise §3 to specify the model actually built.**

We have taken the second option. The five types were specified before any audit was constructed,
and when we built one we reached for a different kernel. That is evidence about which model
works, and preserving the specification would have meant building machinery to match a document
rather than reporting what the work produced.

Section 3 now specifies Actor, Event, Evidence, Decision, Claim, and AuditArtifact. The five
workflow-stage terms survive as open-vocabulary decision types, which is what the code already
treated them as.

Two features of the built kernel that the submitted §3 never mentioned now do substantial work:
capture tier, and the verification status that defaults to unverified.

**3.2. The paper credits the schema with work it attributes elsewhere to manual auditing.
Strengthening the claim would require a comparison case or an account of how the schema's
structure directed the auditor.**

The narrower claim is now what the paper makes, in the abstract, §4.2, §4.5, and the Experimental
procedures.

On the mechanism you asked for: every Decision in the schema carries a verification status, and
the default is unverified. Enumerating a workflow's decisions therefore produces a work list
before any checking has been done, and the unverified entries are what an auditor has to examine.
This is stated in §3.1 and again at the head of §4.2. We have not attempted a comparison case,
which would require auditing a second workflow without the schema, and we agree that a single
self-audited case cannot separate the schema's contribution from the auditor's. Section 5 now
says so as an explicit limitation.

**3.3. The sub-linear scaling claim rests on one observation with no cost measurement. Reporting
the audit's cost in person-hours would be the single most useful addition.**

The claim is withdrawn, and §4.5 says that it is withdrawn rather than deleting it quietly. Cost
is reported as described at 1.4 above. We note in §4.5 that the 60 hours includes constructing
such a record for the first time with no tooling, so it is an upper bound rather than a
steady-state figure, and we make no scaling claim of any kind.

**3.4. It would help to state the threat model.**

Added in §3.4, with a short statement at the end of §1 so a reader meets the boundary early. The
threat model is honest error. The record is author-side, written by the people who did the work
from artifacts they control, and it is not tamper-evident. An author determined to conceal
something can produce a clean AIVS record exactly as they can produce a clean Methods section.

**3.5. The paper does not position itself against W3C PROV-O or RO-Crate, particularly the
Workflow Run profile.**

This was the sharpest technical gap in the reviews and is addressed in new §3.5. The argument in
brief: those standards assume instrumentation at execution time and are the better tool wherever
it exists, and their records can populate an AIVS audit directly. AIVS addresses the case where
instrumentation was absent, which is most published work. Its unit is the methodological decision
and its verification status rather than the execution step, and capture tier expresses how much
of a record was reconstructed rather than captured, which a profile of an
instrumentation-assuming standard cannot express. Both references are added.

**3.6. The data availability statement lists four items that do not appear in the deposit it
cites.**

Confirmed, and we are grateful you checked. A verification pass found that the figure-generation
scripts and environment manifest were absent, that the AIVS verification record was deposited in
the sibling repository rather than the one cited, that the variant dataset was stale, and that
twelve of twenty-one analysis scripts were deposited. The deposit was frozen at a commit well
behind the work the manuscript describes, which is why the numbers in §4.4 could not be traced.

The deposits have been repaired and re-released with new version DOIs; the concept DOIs are
unchanged. The availability statement now describes what is actually deposited, states explicitly
where the verification record lives, and both repositories carry a README mapping manuscript
claims to files.

**3.7. The manuscript's own AI disclosure names no tool, model, or version for drafting, which is
exactly what §3.1 requires of others.**

A fair and uncomfortable observation. The disclosure now names the tools, interfaces, date ranges,
and the model identifiers recoverable from surviving configuration, and declares its own capture
tier, which is 0 for drafting and 1 for the case-study workflow. Where the record is incomplete
the disclosure says so and says why, rather than omitting the field.

**3.8. Additional defect identified during revision (not raised by a reviewer).**

While verifying the deposits we found that the submitted §4.3 stated that agent-session logs were
deposited under access control. No such deposit exists. The logs existed when the audit was
constructed and were destroyed by the tool's default retention policy; their absence was confirmed
on 2026-08-27. The deposited audit artifact also declared capture tier 2, which requires those
logs.

Section 4.3 now states the loss plainly and the artifact is corrected to tier 1. We report this
because a paper arguing for auditable records should not quietly repair its own.

**3.C4. Introduction could be improved.**

See 2.C4.

---

## Reviewer 4

**4.1. The biomedical example was not scientifically coherent; the stated goal was
incomprehensible to a reviewer with deep biomedical expertise.**

We take this as a writing failure rather than an analysis failure, and the sentence you quoted
supports that reading: it stated the question in the vocabulary of the answer.

Section 4.1 is rewritten. The question is now built in three steps. Conservation-based predictors
score a variant by how unusual it looks against evolutionary patterns, which works because
positions evolution holds fixed are the ones a folded structure depends on. Intrinsically
disordered proteins have no fixed structure and are weakly conserved, and several cause disease
by the mutant protein gaining a harmful behaviour rather than losing function, in which case the
responsible residue need not be conserved at all; what matters is where it sits. It follows that
these predictors should work on the loss-of-function cases and fail on the gain-of-function ones,
and they do, at 0.813 against 0.493.

**4.2. The manuscript has a "word salad" quality. Simplify the language and concepts, use jargon
only when necessary.**

The paragraph you quoted is rewritten, along with the rest of §2 and a general pass over the
manuscript. Section 2.2 now opens with a one-sentence definition and a concrete case before any
abstraction, and explains why the byline no longer carries the work that accountability requires.
Sentences are shorter and nested parentheticals are removed throughout.

**4.3. Use a published, credible, substantive, scientifically meaningful workflow from any
domain, rather than the authors' own. (Declined)**

We decline this, and state the reason in §4.1 so it reaches readers rather than only reviewers.

A retrospective audit of the kind this paper describes requires the workflow's internal artifacts:
superseded scripts, intermediate outputs, abandoned analyses, and internal audit notes. Published
work does not deposit these. Auditing a third party's paper would have been limited to what they
chose to deposit, which is precisely the material a disclosure statement already covers, and
would have demonstrated the opposite of the paper's claim. Every one of the five defects reported
here was recoverable only because we had access to material no journal requires anyone to
publish. The ensemble that read its own labels, for instance, is visible only in a superseded
script that no deposit would have contained.

We recognise the cost of this choice: a self-audit cannot separate the schema's contribution from
the auditor's, and §5 now states that as an explicit limitation.

**4.4. Provide evidence for the problem beyond the fact that LLMs exist and people use them.**

Partly adopted. The introduction now opens with three concrete defects from this paper's own case
study rather than with AI adoption, and the quantitative evidence follows: 100 fabricated
references across 53 papers that had cleared expert review, and detection rates of 6.1% precision
and 21.1% recall on a benchmark of errata-level errors. We agree that the reproducibility crisis
predates language models and is driven by incentives rather than tools; the manuscript does not
claim otherwise, and confines itself to the narrower question of what a record should contain.

**4.5. An additional "homespun" (JSON) layer probably does not add much value. (Partly declined)**

We decline the framing while accepting the underlying point about presentation. The contribution
is the record and the discipline of constructing it, not the serialization format; JSON is an
implementation detail and the schema is defined independently of it. Section 5 now states the
contribution in those terms. We note that Reviewer 3, reviewing the same manuscript,
independently identified the documentation layer between disclosure and runtime capture as a
genuine gap in the literature.

**4.6. Focus and length could be improved.**

See 2.C7.

---

## Reviewer 5

**5.1. I had to hunt through git repos to find records. Some records discussed in the manuscript
don't appear in the repos.**

You were right, and Reviewer 3 found the same thing independently. Beyond the missing files
described at 3.6, one cause was specific and avoidable: the AIVS repository's README described the
release as shipping the meta-schema only, with adapters and examples out of scope. That was true
of an earlier version and false of the released one, so a reader landing on the repository was
told the audit records did not exist. It is corrected, and both repositories now carry a README
mapping each manuscript claim to its supporting file.

**5.2. It's impossible to parse the records because they aren't documented in much detail in the
manuscript.**

New Table 2 maps each finding to its record, its audit document, and its corrected output. Section
3 is rewritten around the six entity types the records actually use, so the vocabulary in the
manuscript now matches the vocabulary in the files.

**5.3. Why include an audit of all references? This makes it impossible to disentangle what was
AI generated and human generated.**

Section 4.3 now states the reason. The boundary between AI-suggested and author-supplied
citations in a drafted bibliography is not recoverable after the fact; the drafting process
interleaves them and no artifact records which was which. Auditing all references costs less than
reconstructing that boundary would, and produces a stronger guarantee.

**5.4. Why include AI-generated references at all? If the authors haven't read them it seems
inappropriate. For content produced by an AI, wouldn't the correct attribution be to the AI?
(Declined)**

We decline the premise rather than the concern. A reference is not AI-authored content. Where a
model suggested a citation, an author read the source and assessed its relevance before it
entered the manuscript, and the record holds the suggestion and the human verification as
separate entries. Attribution belongs to the author who chose to stand behind the citation, which
is the same standard that applies to a reference found through any other search tool. We agree
entirely that citing unread references is inappropriate, which is why every reference here was
read, and why §4.3 now says so.

**5.5. Substantially more context is needed for the case study.**

See 4.1.

**5.6. The case study includes data dumps that are difficult or impossible to parse.**

Section 4.4 no longer presents results as a sequence of numbers. Interpretation leads, the
numbers support it, and the repetitive provenance sentences that followed each finding in §4.2
have moved into Table 2.

**5.7. It's not clear where the authors imagine AIVS being used. Are the records for reviewers, or
just for authors, or both?**

This was never stated and now is, in §3.4. Authors produce the record; readers, reviewers, and
downstream researchers consume it. It is not a submission requirement and nothing in the paper
depends on a venue adopting it. Whether editors should require such records is a policy question
we explicitly place out of scope.

**5.8. Reproducibility seems out of reach. How would only knowing when one used a model let
another reproduce the results?**

This is the strongest objection in your review and the submitted §2.3 did not engage it. Section
2.3 now states the objection first, then separates two things. The pipeline is ordinary
computation and reruns to the same numbers from pinned inputs; that is what the reported results
rest on. Generative invocation is not reproducible and no schema makes it so. The target is
therefore deposit rather than regeneration: what a reader cannot regenerate they can still
inspect. AI-written code is the clear case, since producing it was nondeterministic but the code
is a file and running it is as reproducible as any script.

We apply the same standard to the audit record itself. Re-running the audit script regenerates
fresh identifiers, so its output does not match the deposited copy byte for byte. Section 4.3 and
the repository both state this rather than leaving a reader to discover that a provenance paper
ships an artifact that fails checksum reproduction.

**5.9. Define AIVS. What's the difference between AIVS and AIVS-VAR?**

There is none; the compound term was an artifact of earlier drafts and should not have survived.
It is removed from the manuscript, the audit scripts, and the deposited records. AIVS is the
schema. VAR names the three properties it records.

**5.10. The text is extraordinarily dense and monotonous.**

See 4.2. The repeated provenance sentence in §4.2, which appeared in near-identical form after
each of the five findings, was a specific contributor and has moved into a table.

**5.11. There's overlapping text in the figures.**

Both figures are regenerated with the overlap corrected.
