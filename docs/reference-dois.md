# Reference DOIs — Job 4

Resolved 2026-09-08 against the CrossRef REST API, the DataCite REST API
(arXiv registers its DOIs with DataCite, not CrossRef), and the arXiv API.
Every DOI below was fetched, not recalled. Titles and authors returned by the
registry were compared against the reference as written; no DOI was
constructed, guessed, or pattern-completed.

The journal requires a DOI for every reference. **Ten of twelve have one.
Two do not exist and are recorded by URL.**

## Table

| # | Reference | DOI | Source of resolution | Confidence |
|---|---|---|---|---|
| 1 | NIH, *Supporting fairness and originality in NIH research applications*, NOT-OD-25-132 | **none — no DOI exists** | CrossRef: no record. URL verified live (HTTP 200) | High (policy notice; NIH Guide notices are not DOI-registered) |
| 2 | Naser MZ, *How LLMs Cite and Why It Matters* | **10.48550/arXiv.2603.03299** | DataCite + arXiv API + landing page + title search (4 sources) | High — **preprint; verified genuine, see §Naser** |
| 3 | Son G et al., *When AI Co-Scientists Fail: SPOT* | **10.48550/arXiv.2505.11855** | DataCite: registered. arXiv API: title + authors match | High — **preprint** |
| 4 | Lin Z et al., ESM2, *Science* 2023;379:1123 | **10.1126/science.ade2574** | CrossRef by DOI: *Science*, 2023 | High |
| 5 | Cheng J et al., AlphaMissense, *Science* 2023;381:eadg7492 | **10.1126/science.adg7492** | CrossRef by DOI: *Science*, 2023 | High |
| 6 | Frazer J et al., EVE, *Nature* 2021;599:91 | **10.1038/s41586-021-04043-8** | CrossRef by DOI: *Nature*, 2021 | High |
| 7 | Gottweis J et al., AI co-scientist | **10.48550/arXiv.2502.18864** | DataCite: registered. arXiv API: title + authors match | High — **preprint** |
| 8 | Ansari S, NeurIPS failure-mode taxonomy | **10.48550/arXiv.2602.05930** | DataCite: registered. arXiv API: title + author match | High — **preprint** |
| 9 | Souza R et al., PROV-AGENT | **10.1109/escience65000.2025.00093** | CrossRef bibliographic search → exact title match | High — **published version, see note** |
| 10 | Lebo T, Sahoo S, McGuinness D (eds), *PROV-O: The PROV Ontology*, W3C Recommendation 2013 | **none — no DOI exists** | CrossRef: no record for the Recommendation. URL verified live (HTTP 200) | High (W3C Recommendations are not DOI-registered) |
| 11 | Soiland-Reyes S et al., RO-Crate, *Data Science* 2022;5:97 | **10.3233/DS-210053** | CrossRef by DOI: *Data Science*, 2022 | High |
| 12 | Brazma A et al., MIAME, *Nature Genetics* 2001;29:365 | **10.1038/ng1201-365** | CrossRef by DOI: *Nature Genetics*, 2001 | High |

**Unresolved: none.** Two references (1 and 10) have no DOI because none was
ever registered for that document type — that is a fact about the source, not
a failed lookup. Neither is flagged as an error; both carry a verified URL.

## Note on #9 — prefer the published version

The work order asked whether the e-Science proceedings version now carries a
publisher DOI. **It does.** Verified in CrossRef:

- DOI `10.1109/escience65000.2025.00093`
- *PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions in Agentic Workflows*
- 2025 IEEE International Conference on eScience (eScience), pp. 467-473
- Souza R, Gueroudji A, DeWitt S, Rosendo D, Ghosal T
- Issued 2025-09-15, type `proceedings-article`

**DECIDED 2026-09-08: the IEEE DOI is primary**, with **arXiv:2508.02866**
(DOI `10.48550/arXiv.2508.02866`, DataCite-registered) retained as the
secondary identifier. This also upgrades the paper's most important
prior-art citation from a preprint to a peer-reviewed proceedings paper.

## Verified titles, as returned by the registries

Recorded so a reader can confirm each DOI points at the intended work rather
than a same-named item:

| # | Registry-returned title |
|---|---|
| 2 | How LLMs Cite and Why It Matters: A Cross-Model Audit of Reference Fabrication in AI-Assisted… |
| 3 | When AI Co-Scientists Fail: SPOT — a Benchmark for Automated Verification of Scientific Research |
| 4 | Evolutionary-scale prediction of atomic-level protein structure with a language model |
| 5 | Accurate proteome-wide missense variant effect prediction with AlphaMissense |
| 6 | Disease variant prediction with deep generative models of evolutionary data |
| 7 | Accelerating scientific discovery with Co-Scientist |
| 8 | Compound Deception in Elite Peer Review: A Failure Mode Taxonomy of 100 Fabricated Citations |
| 9 | PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions in Agentic Workflows |
| 11 | Packaging research artefacts with RO-Crate |
| 12 | Minimum information about a microarray experiment (MIAME)—toward standards for microarray data |

## Discrepancies found

1. **#2 Naser — RESOLVED 2026-09-08, citation is genuine.** The identifier
   `2603.03299` implies March 2026 while arXiv reports submission on
   **7 February 2026**. Because this manuscript cites this very paper for the
   prevalence of fabricated citations, the reference was re-checked against
   four independent sources, all agreeing:

   | Source | Result |
   |---|---|
   | DataCite `10.48550/arXiv.2603.03299` | registered, title matches |
   | arXiv API by id | title + author `Naser, MZ` match |
   | arXiv landing page `arxiv.org/abs/2603.03299` (HTTP 200) | `citation_title` exact match; `citation_author` `Naser, MZ`; `citation_date` 2026/02/07; dateline "Submitted on 7 Feb 2026" |
   | arXiv title search | **exactly one** entry, `2603.03299v1`, no alternate canonical id |

   The paper exists, the identifier is authoritative and resolves, and the
   author matches. The ID/month mismatch is an arXiv-side numbering anomaly,
   not a citation defect. **No change to the reference is required**: the
   manuscript's "arXiv:2603.03299, February 2026" agrees with arXiv's own
   metadata on both fields.

2. **#11 RO-Crate page range.** CrossRef reports *Data Science* vol. 5,
   pp. **97-138**. The reference as written gives "5:97", the start page only.
   Correct, but if CiSE style wants a full range it is 97-138. Authors as
   registered: Soiland-Reyes, Sefton, Crosas, Castro (+ others).

3. **#4 ESM2 — the DOI is not derived from the article number.** `science.ade2574`
   does not match the "379:1123" locator pattern the way #5's
   `science.adg7492` matches "381:eadg7492". Both were verified by direct
   CrossRef lookup and both return the expected titles; noting it only so the
   asymmetry is not later mistaken for a transcription error.

4. **#9 doi.org returns HTTP 202, not 200,** for the IEEE DOI. That is IEEE
   Xplore's bot-mitigation response to an automated HEAD request, not a broken
   DOI — the DOI is present in CrossRef with full metadata. The arXiv DOI
   returns 200 normally.

## Method

- CrossRef: `GET https://api.crossref.org/works/{doi}` for candidate DOIs;
  `GET .../works?query.bibliographic=...` for #9 and #10.
- DataCite: `GET https://api.datacite.org/dois/10.48550/arXiv.{id}` for all
  five preprints.
- arXiv: `GET https://export.arxiv.org/api/query?id_list={id}` to confirm each
  identifier resolves to the claimed title and author list.
- URL liveness for #1 and #10 by `curl -L -o /dev/null -w '%{http_code}'`.
- Polite `User-Agent` with contact address throughout; requests rate-limited.

No DOI in this document was written from recall. Candidate DOIs for #4, #5,
#6, #11 and #12 were proposed and then **verified** by direct lookup; had any
returned a mismatched title it would be recorded here as unresolved rather
than corrected silently.
