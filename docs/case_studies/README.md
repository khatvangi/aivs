# AIVS Case-Study Source Material

PDFs and supporting documents for the AIVS audit examples in
`examples/`. Each case-study source is referenced by exactly one
audit script; the audit's `SourceRef` entries point back to these
files.

## Contents

### Smith 2026 (J. Chem. Educ.) — podcast paper

Smith, D.K. "Creating a Podcast Using Generative Artificial
Intelligence to Support Student Learning of Organic Reaction
Mechanisms." *J. Chem. Educ.* 2026, 103, 2077–2084.
DOI: `10.1021/acs.jchemed.5c01652`.

- `smith_2026_jce_main.pdf` — main article (2.1 MB)
- `smith_2026_jce_si.pdf` — supporting information (420 KB).
  Contains the AI chat history: ethics statement, V1/V2/V3 user
  prompts, full NotebookLM outputs, curation highlights, final
  time-stamped transcript.

Smith voluntarily submitted the full chat history as SI — an unusual
disclosure that effectively predates AIVS. The Smith audit
(`examples/smith_2026_audit.py`) marks D3, D5, and D9 as
`publish_level="verbatim"` because Smith's verbatim disclosure was
itself the deliverable. The audit reproduces Smith's voluntary
transparency in structured form.

### Triplet-proof (JME submission) — separate project tree

The triplet-proof audit (`examples/kiran_triplet_proof_audit.py`)
references files at `/storage/kiran-stuff/triplet-proof/` —
manuscript_JME.md, HISTORY.md, rebuild_notes.md, the three Claude Code
session JSONLs. Those files are not duplicated here; the audit
script's `SourceRef` entries point at the live project paths.

### Kappa-friction (JPCB submission) — separate project tree

Same pattern. The kappa_friction audit
(`examples/kappa_friction_audit.py`) references files at
`/storage/kiran-stuff/IDP_projects/kappa_friction/` and the two
Claude Code session JSONLs at
`~/.claude/projects/-storage-kiran-stuff-IDP-projects-kappa-friction/`.

## Why these PDFs are co-located with the audit code

A future reader of `examples/smith_2026_audit.py` needs to be able to
verify the audit's claims against the source material it cites. The
audit script's `_src("ed5c01652_si_001.pdf:p4")` reference is only
useful if the reader can find that file. Co-locating the case-study
PDFs with the audit code is the file-system-level analog of the VAR
framework's reproducibility envelope.
