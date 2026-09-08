#!/usr/bin/env python3
"""
apply_qss_revisions.py  —  QSS descriptive-pivot revision of var_manuscript.md

Run ON BORON (where the file lives). Self-checking: every anchor must match
exactly once or the script aborts before writing anything. Backs up to
var_manuscript.md.bak first. Recommend: git commit (or branch) before running.

What it does (the agreed QSS pivot):
  - Reframes the prescriptive "enforceable editorial standard / submission
    platform" claims into descriptive "documentation schema + retrospective
    audit" claims, matching the current AIVS design.
  - Cuts/demotes the unbuilt machinery: the automated submission-time
    verification platform (3.4), the reviewer/editor enforcement log (3.6),
    the adapter/API roadmap (3.7), and the Adoption Pathways subsection (5.2).
  - Adds the PROV-AGENT/Flowcept prior-art differentiation in 3.1 (+ ref [28]).
  - Fixes the prospective -> retrospective contradiction.
  - Removes the [X] hours placeholder.
  - All replacement text is em-dash-free.

NOT done here (flagged separately): global em-dash sweep of UNTOUCHED prose;
ORCID byline; Declaration of Interests re: ABCD; QSS cover letter.
"""

import shutil, sys, re

PATH = "/storage/kiran-stuff/aivs/var_manuscript.md"
EMDASH = "—"

# ---- surgical sentence/paragraph swaps: (label, OLD, NEW) -------------------
EDITS = []

EDITS.append(("byline: add ORCID iDs",
"**Corresponding author:** *Boggavarapu Kiran (kiran@mcneese.edu)",
"**Corresponding author:** *Boggavarapu Kiran (kiran@mcneese.edu)\n\n**ORCID iDs:** Boggavarapu Kiran, 0000-0003-0751-6459; Hannah Ribbeck, [ORCID required: add before submission]"))

EDITS.append(("summary: thesis sentence -> descriptive",
"We propose VAR (Verifiability, Accountability, Reproducibility) as an operational, enforceable standard for AI-integrated publication, and AIVS, an open-source verification schema that implements it at submission and review; together they form the AIVS-VAR method.",
"We frame the requirements for AI-integrated research as three checkable properties (verifiability, accountability, reproducibility; VAR) and present AIVS, an open-source schema that documents an AI-assisted workflow as a structured, auditable record. AIVS extends the minimum-information-standard tradition (MIAME, MIQE, ARRIVE) from single instruments to the system-of-tools that generative AI introduces; together they are the AIVS-VAR method."))

EDITS.append(("summary: prospective -> retrospective, drop em-dashes",
"Applied prospectively during manuscript preparation, manual verification audits " + EMDASH + " captured as records against the AIVS schema " + EMDASH + " caught five categories of failure, from fabricated model features to leaked cross-validation labels, that disclosure-only review would have missed.",
"Applied as a retrospective audit of our own end-to-end workflow and recorded against the schema, manual verification caught five categories of failure, from fabricated model features to leaked cross-validation labels, that disclosure-only review would have missed."))

EDITS.append(("summary: de-advocacy closing sentence",
"We argue that VAR-compliant publication is achievable, auditable, and editorially enforceable, and is the precondition for AI-integrated science to remain accountable.",
"The result is a portable verification record that travels with a paper and lets a reader reconstruct how its AI-generated content was produced and checked, a documentation layer that disclosure statements do not provide."))

EDITS.append(("bigger picture: enforceable standard -> verification record",
"We argue that AI-assisted research needs an enforceable standard, not a disclosure habit, and supply one. It rests on three checkable properties: every claim and citation resolves to a real object (verifiability), a specific person is on record for each decision (accountability), and the workflow can be independently rerun (reproducibility). A companion open-source schema turns these properties into mechanical checks a submission system can run.",
"We argue that AI-assisted research needs a verification record, not a disclosure habit, and supply the schema for one. It rests on three checkable properties: every claim and citation resolves to a real object (verifiability), a specific person is on record for each decision (accountability), and the workflow can be independently rerun (reproducibility). A companion open-source schema captures these properties as a structured audit record that a reader, reviewer, or editor can inspect after the fact."))

EDITS.append(("intro: enforceable framework -> operational account",
"We argue that AI-integrated science requires an explicit, operational, enforceable framework that addresses these failure modes directly. We propose three principles (verifiability, accountability, and reproducibility) that together constitute such a framework, and we name the framework VAR.",
"We argue that AI-integrated science requires an explicit, operational account of how AI shaped a given result, framed around the failure modes above. We propose three properties (verifiability, accountability, and reproducibility) that together constitute such an account, and we name them VAR."))

EDITS.append(("intro: contribution -> documentation schema, not enforcement",
"The contribution lies in making them the explicit basis of editorial decision-making for AI-integrated submissions, and in providing the procedural infrastructure (a verification schema named AIVS, together yielding the AIVS-VAR method) that allows the principles to be enforced consistently rather than aspirationally.",
"The contribution lies in turning them into a concrete documentation schema (AIVS, together yielding the AIVS-VAR method) that records, at the granularity at which AI-assisted work can fail, what an independent reader needs in order to audit it, rather than leaving the properties aspirational."))

EDITS.append(("intro: roadmap-of-paper line",
"discusses adoption pathways and limitations (Section 5), and concludes (Section 6).",
"discusses limitations and the agentic-platform case (Section 5), and concludes (Section 6)."))

EDITS.append(("S2 intro: editorial standard -> analytical frame",
"Together they constitute the editorial standard we propose for AI-integrated publication.",
"Together they constitute the analytical frame the rest of the paper operationalizes as a documentation schema."))

EDITS.append(("S2.1: enforceable at submission -> checkable",
"Verifiability is enforceable at submission. Citations can be resolved against CrossRef, PubMed, arXiv, and institutional repositories.",
"Verifiability is checkable. Citations can be resolved against CrossRef, PubMed, arXiv, and institutional repositories."))

EDITS.append(("S2.1: verification surface -> schema records outcomes",
"Each check is mechanical; the cost is a one-time investment in tooling rather than an ongoing burden on reviewers. The verification surface that AIVS implements (Section 3) makes these checks systematic rather than incidental.",
"Each check is mechanical and, in principle, automatable. The AIVS schema (Section 3) records the outcome of each such check as part of the workflow's audit trail, making verification systematic rather than incidental."))

EDITS.append(("S2.2: reviewer/editor enforcement platform -> author-side record",
"Accountability extends beyond authorship. Reviewers carry accountability for the judgments rendered in their reviews; reviews that recommend acceptance of submissions later found to contain unverified fabrications are tracked across the platform and affect future reviewer assignment. Editors carry accountability for the integrity of the review process and for decisions to publish despite flagged verification failures. The mechanism is record-keeping, not punishment. The platform retains a log of decisions; consequences attach to systematic patterns, not isolated incidents.",
"Accountability in AIVS is author-side and record-based: it documents which human certified each AI-assisted decision. It is not a system that adjudicates reviewers or editors. How a venue might use such records in its review process is outside the scope of this paper; the schema's claim is only that the authorship record exists and is auditable."))

EDITS.append(("S3.1: insert PROV-AGENT differentiation before agentic-platforms para",
"The argument intensifies for the class of end-to-end agentic AI platforms",
"Provenance systems address an adjacent but distinct problem. PROV-AGENT [28], which extends W3C PROV and instruments agentic workflows through the Model Context Protocol and data-observability hooks, captures agent prompts, responses, and decisions automatically and at runtime, streaming them into a consolidated provenance database as the workflow executes. That design is capture-maximal and system-side: it records the workflow as it runs, on infrastructure the authors instrument. AIVS occupies the opposite corner of the design space. It is retrospective, author-side, and manuscript-anchored: it documents, after the fact, only the invocations that materially shaped a published claim, and it does not require the workflow to have been instrumented in advance, which is the common case for heterogeneous pipelines that mix closed commercial tools with local code. The two are complementary. Where a runtime provenance system was in place, its records can populate AIVS Evaluation and Curation fields; where none was, AIVS is the schema an author uses to reconstruct an auditable record from the workflow's surviving artifacts.\n\nThe argument intensifies for the class of end-to-end agentic AI platforms"))

EDITS.append(("S3.3: soften v1.0 serializer forward-promise",
"v1.0 surfaces the application vocabulary in the editorial-facing view without changing the underlying records.",
"a planned serializer would surface the application vocabulary in an editorial-facing view without changing the underlying records, and is not a claim of this paper."))

EDITS.append(("S3.4 intro sentence (bridge before checks)",
"AIVS v1.0 specifies the verification checks an AIVS-compliant submission platform performs automatically on every AI-assisted submission. The v0.1.0 release defines the schema against which check outputs are recorded as Evaluation records (kernel-level Events with verifier Actors and check-type targets); the implementation of the checks themselves is staged as adapter and parser releases (see " + "§" + "3.7). In what follows, present tense refers to the v1.0 target behaviour of the verification surface. The checks operate on the Evaluation records in the bundle and on the artifacts they reference, and are bounded by what can be mechanically verified. The submission is not rejected automatically on failure; the verification report is attached to the submission and routed to editors and reviewers as part of the review record.",
"AIVS does not perform verification; it records it. Each Evaluation record holds the outcome of a check performed on an Invocation's output, drawn from a controlled vocabulary that maps to the failure modes of " + "§" + "2.1. Some of these checks can be automated and some require human judgment; the schema is agnostic as to which, recording the verifier (a human ORCID or an automated-tool identifier) alongside each outcome. The descriptions below define what each check establishes, not a built pipeline. Whether a venue automates any of them at submission, and how, is an implementation question this paper does not address; what the schema fixes is the record against which any such check is logged."))

EDITS.append(("S3.4: bounded surface -> bounded scope",
"The verification surface is intentionally bounded. AIVS does not assess the scientific correctness of claims, the appropriateness of methods, the novelty of contributions, or the quality of writing.",
"The verification scope is intentionally bounded. AIVS does not assess the scientific correctness of claims, the appropriateness of methods, the novelty of contributions, or the quality of writing."))

EDITS.append(("S4.2 opener: prospective -> retrospective",
"The case study is informative principally because AIVS-VAR was applied prospectively during manuscript preparation rather than retrofitted afterwards. The verification surface caught five categories of failure that would have entered the literature under disclosure-only review.",
"The case study is informative principally because AIVS was applied as a retrospective audit over a genuine end-to-end workflow, looking back across the analysis and the draft to record what materially affected the reported result. The audit caught five categories of failure that would have entered the literature under disclosure-only review."))

EDITS.append(("S4.5: remove [X] hours placeholder + overstated automation",
"The five categories above were caught in approximately [X] hours of audit work distributed across variant-table validation, code-version comparison, and canonical-CSV cross-referencing. Citation resolution was effectively automated; figure provenance was effectively automated; the bulk of authoring time was unaffected.",
"The five categories above were caught during targeted audit work distributed across variant-table validation, code-version comparison, and canonical-CSV cross-referencing, rather than through line-by-line re-reading of the entire manuscript. The bulk of authoring time was unaffected."))

EDITS.append(("S5 disc: explicit operational standard -> auditable account",
"The VAR framework proposes that AI-integrated science requires an explicit operational standard, not a disclosure norm. The distinction matters. Disclosure shifts the burden of judgment to the reader, who is asked to discount a published claim by some unspecified factor on learning that AI was involved in its production. Verification, accountability, and reproducibility shift the burden back to the publication system, which is asked to ensure that published claims meet a defined standard regardless of how they were produced. The latter is more consistent with what scientific publishing has historically promised.",
"The VAR framing holds that AI-integrated science requires an explicit, auditable account of how AI shaped a result, not a disclosure norm. The distinction matters. Disclosure shifts the burden of judgment to the reader, who is asked to discount a published claim by some unspecified factor on learning that AI was involved. A verification record shifts that burden onto the author, who assembles, before submission, the evidence that the AI-assisted claims resolve to real objects and were checked. The reader then audits a record rather than guessing at a discount."))

EDITS.append(("S5 disc: 'enforced standard is the contribution' -> documentation layer",
"The framework differs in what it requires at submission and review. Disclosure-without-verification policies permit fabrications to enter print unless a reviewer happens to notice. The VAR framework prevents publication of fabricated content as a matter of process, through the AIVS verification surface, rather than as a matter of reviewer diligence. The shift from aspirational standard to enforced standard is the contribution.",
"The framework differs in what it makes auditable. Disclosure-without-verification leaves fabrications to enter print unless a reviewer happens to notice; an AIVS record makes the verification of each AI-assisted claim explicit and inspectable, so that a missed check is visible in the audit trail rather than invisible. The contribution is this documentation layer, which disclosure statements do not provide. It is not an enforcement mechanism, which would require infrastructure and community adoption that no single paper can establish."))

EDITS.append(("S5 disc: infrastructure-investment advocacy -> reach limitation",
"The framework also depends on infrastructure investment. Implementing AIVS at a publication venue requires technical staff, ongoing maintenance, and integration with submission and review platforms. The open-source release of the AIVS schema is intended to lower the marginal cost of adoption, but the first-mover venue absorbs implementation cost that subsequent adopters can avoid. We argue that this investment is justified by the alternative: the costs of publishing fabricated content are eventually borne by the scientific community in the form of retractions, replication failures, and erosion of trust in published work, and these costs are increasing as AI-assisted writing becomes more common.",
"The framework also has a reach limitation. As demonstrated here it is an author-side practice: it produces an auditable record, but it depends on authors choosing to produce one and on readers and reviewers choosing to inspect it. Whether and how venues might require or automate such records is a question of editorial policy and infrastructure beyond the scope of this paper. What the paper establishes is that the record is constructible for a genuine AI-integrated workflow and that constructing it caught errors disclosure would not."))

EDITS.append(("S5.1: 'integration straightforward / venues that require AIVS' -> expressivity claim",
"The integration is straightforward. Platforms emit internal logs already; the AIVS adapter pattern (" + "§" + "3.7) translates platform-specific representations into the standardized Invocation, Evaluation, and Curation records that editors and reviewers can read. A *Nature* paper produced by Robin or Co-Scientist can submit an AIVS bundle alongside the manuscript, and the editorial workflow proceeds as for any other AIVS-compliant submission. The platforms gain a uniform path to publication under venues that require AIVS; the venues gain the verification surface they cannot construct from disclosure alone; readers gain a verification trail that survives independent of the platform vendor's commercial trajectory.",
"Such platforms emit internal logs already. Those logs could be mapped to AIVS Invocation, Evaluation, and Curation records, so that a paper produced by an agentic platform carries an auditable record of its internal steps rather than a single disclosure line, and readers gain a verification trail that survives independent of the platform vendor's commercial trajectory. The mapping tooling is not built here; the point is that the schema is expressive enough to represent these workflows at the granularity at which they fail."))

EDITS.append(("S6: operational standard we propose -> properties define documentation",
"The pertinent editorial question is not whether AI use should be permitted but how AI-assisted work can be published to a standard that science can defend. The VAR framework (Verifiability, Accountability, Reproducibility) is the operational standard we propose. The AIVS schema implements it. The IDP case study demonstrates that the standard is achievable.",
"The pertinent question is not whether AI use should be permitted but how AI-assisted work can be documented to a standard that science can defend. The VAR properties (verifiability, accountability, reproducibility) define what that documentation must make auditable. The AIVS schema records it. The IDP case study demonstrates that the record is constructible for a genuine workflow and that constructing it caught errors disclosure would not."))

EDITS.append(("S6: tail - editorial layer / adoption -> missing record",
"as these platforms scale, the verification surface they cannot supply for themselves becomes the editorial layer that AIVS-VAR is designed to provide. Adoption is incremental, the cost is bounded, and the alternative, a publication environment in which fabricated content cannot be reliably distinguished from real content, is not a stable equilibrium for a discipline that depends on shared trust in its literature.",
"as these platforms scale, the gap between their internal sophistication and the external auditability of their published outputs widens, and a schema that can represent their internal steps at the granularity at which they fail is the missing record. The alternative, a publication environment in which fabricated and genuine content cannot be reliably distinguished, is not a stable equilibrium for a discipline that depends on shared trust in its literature."))

EDITS.append(("Experimental/Verification: v1.0-target surface -> manual checks recorded",
"The mechanical verification surface of " + "§" + "3.4 (citation resolution against CrossRef and PubMed, automated numerical-claim resolution against canonical output files, code-execution comparison across script versions, image-provenance checks, and schema-validation against statistical-claim types) is the v1.0 target; v0.1.0 ships the schema against which the audit outputs are stored, not the automated checks themselves. The discrepancy is disclosed in " + "§" + "3.3, " + "§" + "3.4, " + "§" + "3.7, and " + "§" + "4.1; the case study demonstrates the structural deposit that v1.0 will mechanize.",
"The checks catalogued in " + "§" + "3.4 (citation resolution, numerical-claim resolution against canonical output files, code-execution comparison across script versions, image-provenance checks, and schema validation against statistical-claim types) were performed manually here and recorded against the schema; their automation is a possible extension, not a claim of this paper. The released version ships the schema against which the audit outputs are stored, not an automated checking pipeline."))

EDITS.append(("Resource availability: roadmap-items sentence -> released vs extensions",
"The adapter and parser implementations, manuscript parsers, application-vocabulary serializer, and submission-platform API described in Section 3 are roadmap items staged for v0.2 through v1.0 releases.",
"The released repository provides the meta-schema kernel, JSON serialization, structural-integrity validation, and four worked retrospective audit examples; automated checks, an application-vocabulary serializer, and submission-system or platform adapters are possible extensions and are not part of the deposit accompanying this paper."))

EDITS.append(("References: append [28] PROV-AGENT",
"[27] Elsevier. Elsevier expands article submission screening tool to strengthen research credibility. Press release. 18 March 2026. https://www.elsevier.com/about/press-releases/elsevier-expands-article-submission-screening-tool-to-strengthen-research",
"[27] Elsevier. Elsevier expands article submission screening tool to strengthen research credibility. Press release. 18 March 2026. https://www.elsevier.com/about/press-releases/elsevier-expands-article-submission-screening-tool-to-strengthen-research\n\n[28] Souza R, Gueroudji A, DeWitt S, et al. PROV-AGENT: unified provenance for tracking AI agent interactions in agentic workflows. In: Proceedings of the 2025 IEEE 21st International Conference on e-Science (e-Science), Chicago, IL, USA, 2025. arXiv:2508.02866."))

# ---- block deletions/replacements: (label, START_anchor, END_anchor, NEW) ---
BLOCKS = []

# S3.4: replace the six present-tense "platform performs automatically" check
# descriptions (between the reframed intro and the bounded-scope paragraph)
# with a compact descriptive list. START = first check; END = last check.
BLOCKS.append(("S3.4 six automated checks -> compact descriptive list",
"*Citation resolution* checks every reference in the manuscript against CrossRef",
"every Source has a retrievable URI or a documented redaction.",
"The vocabulary covers: citation resolution (references resolved against CrossRef, PubMed, arXiv, and institutional repositories, with partial matches flagged separately from non-resolutions); quote matching (quoted passages checked against the cited source); data retrievability (repository identifiers resolved and access confirmed); code execution (the deposited repository cloned and a smoke test run against the deposited environment); image-forensic analysis (provenance and manipulation scoring via existing tools such as Bik-style pipelines, ImageTwin, or Proofig); and schema validation (structural integrity of the bundle: every Curation references a real Invocation, every Invocation whose output appears in the manuscript carries at least one Evaluation, every Deposition resolves to a public URI, every accountable_author ORCID is present, and every Source has a retrievable URI or a documented redaction)."))

# S3.6: replace the reviewer/editor enforcement log with append-only persistence
BLOCKS.append(("S3.6 accountability log -> persistence & re-verification",
"### 3.6 The accountability log",
"consequences attach to systematic patterns across multiple manuscripts, not to isolated incidents.",
"### 3.6 Persistence and re-verification\n\nAIVS records persist with the published artifact, and the log is append-only: a verification re-run against an updated database that newly resolves a previously failed citation is recorded as a new Evaluation, leaving the original outcome visible in the audit trail. This supports post-publication re-verification by readers and downstream researchers, who can re-run the checks against the published bundle and compare the results to the publication-time record. The schema takes no position on how venues act on such records; that is editorial policy, not schema design."))

# S3.7: strip adapter/API roadmap; keep real release facts + interop + versioning
BLOCKS.append(("S3.7 implementation+interop -> released facts only",
"### 3.7 Implementation and interoperability",
"the version under which a given manuscript was submitted is recorded in the bundle metadata and pinned to the published record.",
"### 3.7 Implementation and interoperability\n\nAIVS is released under AGPL-3.0-or-later at https://github.com/khatvangi/aivs. The released version ships the meta-schema kernel (the record types of " + "§" + "3.3), the JSON serialization specification, structural-integrity validation, the redact-by-default privacy posture of " + "§" + "3.5, and four worked retrospective audit examples (the case study of " + "§" + "4 plus three prior workflows on protein-design and educational-content paper preparation). The automated checks of " + "§" + "3.4, an application-vocabulary serializer, and adapters for specific submission systems or agentic platforms are natural extensions but are not implemented here and are not claims of this paper; the schema is defined independently of any such tooling.\n\nInteroperability with existing minimum-information standards is preserved. AIVS records may carry external schema references (a CLAIM checklist for a clinical-imaging submission, a TRIPOD-AI declaration for a discriminative-ML submission, an ARRIVE compliance statement for animal-research components) without conflict. AIVS documents the AI workflow; the external standards document their respective tool-systems; the records coexist in the same bundle.\n\nThe schema is versioned: backward compatibility is guaranteed within major versions, and the version under which a manuscript was prepared is recorded in the bundle metadata and pinned to the published record."))

# S5.2: delete Adoption Pathways subsection entirely
BLOCKS.append(("S5.2 Adoption pathways -> deleted",
"### 5.2 Adoption pathways",
"is implementing VAR at a level appropriate to its operational maturity.",
""))


def apply_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        print("  !! ABORT  [%s]: anchor found %d times (need exactly 1)" % (label, n))
        sys.exit(1)
    return text.replace(old, new, 1)


def apply_block(text, start, end, new, label):
    i = text.find(start)
    if i == -1 or text.count(start) != 1:
        print("  !! ABORT  [%s]: START anchor missing or non-unique" % label)
        sys.exit(1)
    j = text.find(end, i)
    if j == -1:
        print("  !! ABORT  [%s]: END anchor not found after START" % label)
        sys.exit(1)
    j += len(end)
    return text[:i] + new + text[j:]


def main():
    with open(PATH, encoding="utf-8") as f:
        text = f.read()
    orig = text

    for label, old, new in EDITS:
        text = apply_once(text, old, new, label)
        print("  ok   edit   %s" % label)
    for label, start, end, new in BLOCKS:
        text = apply_block(text, start, end, new, label)
        print("  ok   block  %s" % label)

    # leftover quick sanity: high-risk prescriptive phrases that should be gone
    for phrase in ["enforced standard is the contribution",
                   "venues that require AIVS",
                   "applied prospectively",
                   "[X] hours",
                   "### 5.2 Adoption pathways"]:
        if phrase in text:
            print("  WARN  residual phrase still present: %r" % phrase)

    shutil.copyfile(PATH, PATH + ".bak")
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(text)

    em_before = orig.count(EMDASH)
    em_after = text.count(EMDASH)
    print("\nWROTE %s  (backup: %s.bak)" % (PATH, PATH))
    print("chars: %d -> %d" % (len(orig), len(text)))
    print("em-dashes remaining in file: %d (was %d) -- untouched prose; do a separate humanizer-stem pass"
          % (em_after, em_before))


if __name__ == "__main__":
    main()
