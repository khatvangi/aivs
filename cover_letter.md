Dr. Andrew-Hufton
Editor, *Patterns*
Cell Press

Dear Dr. Andrew-Hufton,

Following our pre-submission inquiry, we are pleased to submit our manuscript, "Verifiable, accountable, and reproducible AI-assisted research: the VAR framework and the AIVS verification schema, demonstrated on an end-to-end protein-variant workflow," for consideration as a research article in *Patterns*.

Generative AI is now embedded in everyday research workflows, but editorial oversight has not kept pace. Disclosure statements do not catch the fabricated citations, ungrounded claims, and irreproducible pipelines that AI introduces; they shift the verification burden to the reader. We propose VAR (Verifiability, Accountability, Reproducibility) as an operational, enforceable standard for AI-integrated publication, and AIVS, an open-source verification schema that implements it. We demonstrate the method on a complete AI-assisted computational-biology workflow (disease-mechanism prediction for intrinsically disordered protein genes across 3,409 ClinVar variants), where manual verification audits — recorded as records against the AIVS schema — caught five categories of failure during prospective manuscript preparation that disclosure-only review would have missed. Figure 1 visualizes the headline scientific result the framework is anchored to: ESM2, AlphaMissense, and EVE all fail systematically on gain-of-function non-amyloid intrinsically disordered region variants, where conservation is anti-predictive (group AUROC = 0.42) rather than merely uninformative.

The work fits *Patterns* on four counts that map directly to the journal's scope. First, it pairs a methodological advance (the AIVS schema and its VAR framework) with a transparent, reproducible worked example end-to-end through one complete research workflow. Second, it is built around open-source code (AGPL-3.0), FAIR data, and independent reproducibility, the criteria *Patterns* assesses centrally. Third, it treats the deposited verification record as part of the publishable artifact rather than as peripheral supplementary material — directly answering the call for data and computational pipelines to travel with the paper. Fourth, its primary audience — data scientists, research-software engineers, and reproducibility-minded researchers across the life and physical sciences — overlaps the *Patterns* readership directly. The schema and the case-study pipeline are openly available — AIVS at https://github.com/khatvangi/aivs (Zenodo DOI 10.5281/zenodo.20723559; concept DOI 10.5281/zenodo.20723558) and the mechanism_classifier case-study repository at https://github.com/khatvangi/idp-mechanism-classifier (Zenodo DOI 10.5281/zenodo.20723561; concept DOI 10.5281/zenodo.20723560) — and the manuscript's own AIVS verification trail is included as supplemental information.

This manuscript has not been published elsewhere, is not under consideration at another journal, and all authors have approved its submission. The authors declare no competing interests.

Sincerely,

Boggavarapu Kiran
Corresponding author
Department of Chemistry and Physics
McNeese State University
Lake Charles, LA 70609, USA
kiran@mcneese.edu
