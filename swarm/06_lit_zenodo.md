# 06 Literature scan: Zenodo, Voynich (current state, 2023-2026)

Date of scan: 2026-10-13. Method: WebFetch on the Zenodo REST API (`/api/records`). Several calls returned 504 or 400 (rate limit, Retry-After 47-60 s); retries at `size=25` succeeded. The `q=` parser does not enforce the Voynich term: "entropy", "line", "Jaccard" and "Quevedo" queries returned mostly unrelated Zenodo records. Only the "voynich" and "voynich cipher" / "voynich gallows" / "voynich transliteration" / "voynich Currier" queries returned Voynich-specific hits. PDFs were not opened; all descriptions are from record metadata or abstracts, unverified.

## Table: Voynich-related records found

| # | Record ID / DOI | Title | Creator(s) | Date | Type | Quality flag | Stat. nulls? | One-line claim |
|---|---|---|---|---|---|---|---|---|
| 1 | 18346527 / 10.5281/zenodo.18346527 | Statistical Validation of Structure in MS 408: Independent Confirmation of the Jaccard Anomaly | Meijer, Jeffrey J.G.T. | 2026-01-23 | Dataset (CC-BY-4.0) | self-published | not verified | Claims independent confirmation of a "Jaccard anomaly" in MS 408. Concept DOI 10.5281/zenodo.18346526. Metadata only, as requested. |
| 2 | 23113674 / 10.5281/zenodo.23113674 | Structural Decipherment Without Lexical Recovery: A Cross-Validated Morphological Analysis of the Voynich Manuscript | Dominik, Matthew | 2026-10-03 | Preprint | preprint | "cross-validated" claimed; nulls not verified | Cross-validated morphological/grammatical structure; explicitly no lexical recovery. |
| 3 | 19169450 / 10.5281/zenodo.19169450 | One Hand, Five Labels: A Critical Examination of the Five-Scribe Hypothesis | Timm, Torsten | 2026-03-02 | Preprint | preprint | not verified | Argues the five-scribe hypothesis fails; handwriting variation is one evolving hand. Single author; not a Timm & Schinner paper. |
| 4 | 19172665 / 10.5281/zenodo.19172665 | Semantic Attractor Analysis of the Voynich Manuscript | Jensen, Michael D. | 2026-03-23 | Preprint | preprint | not verified | Embedding/clustering suggests operator-based generative structure. |
| 5 | 19171667 / 10.5281/zenodo.19171667 | The Observer's Shelter: A Neurodivergent Reinterpretation of the Voynich Manuscript | Gómez-Cerdas, KJ | 2026-03-23 | Publication | self-published | no | Reads the MS as one neurodivergent author's private record. Not a statistical study. |
| 6 | 18687530 / 10.5281/zenodo.18687530 | Voynich Manuscript Paduan Medical Reference | Honeycutt, Edwin | 2026-02-19 | Dataset | self-published | not verified | Proposes the MS as a modular analog-computing system tied to Paduan medicine, not a cipher. |
| 7 | 23068876 / 10.5281/zenodo.23068876 | Tested Cipher Outputs Under a Corpus-Induced Voynich Alphabet-Distribution Scorer | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | claimed; not verified | Cipher outputs mismatch the MS letter distribution, with stated limits. |
| 8 | 23068683 / 10.5281/zenodo.23068683 | Preregistered Comparator Testing for Ambiguous Historical Manuscripts (F22R-BLIND-1.0) | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | protocol | Preregistration template; Voynich as named target. |
| 9 | 23068646 / 10.5281/zenodo.23068646 | The Voynich "Apparatus" Drawings and the Distillation-Apparatus Tradition | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | not verified | Drawings mostly containment-themed; no supported distillation apparatus in the inspected set. |
| 10 | 23068642 / 10.5281/zenodo.23068642 | Botanical Organization in the Voynich Herbal Section | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | not verified | Tests constitution-based herbal organization; rejects the narrow operational form. |
| 11 | 23068637 / 10.5281/zenodo.23068637 | Structural Differentiation in the Voynich Zodiac Section (f70v-f73v) | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | "decorative-identity null" rejected | Zodiac figures not all identical; no encoding established. |
| 12 | 23068634 / 10.5281/zenodo.23068634 | Descriptive Opener-Class Structure in the Voynich Balneological Section (f75r-f84v) | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | sensitivity checks reported | Non-uniform opener-class pattern across four zones. |
| 13 | 23068629 / 10.5281/zenodo.23068629 | Pharmaceutical Preparation Vocabulary and Cross-Section Connectivity in Folio 58r | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | not verified | Folio 58r as internal herbal-balneological "bridge" (candidate model). |
| 14 | 23068620 / 10.5281/zenodo.23068620 | Multilayer Cipher Architecture in Fontana's Secretum and Bellicorum | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | negative controls | Fontana cipher MSS; Voynich only partly in scope. |
| 15 | 23068615 / 10.5281/zenodo.23068615 | Apothecary Readership and Print-Culture Reception of the Regimen-Sanitatis Workflow (1477-1501) | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | not verified | Links MS pharmaceutical workflow to apothecary print readership. |
| 16 | 23068612 / 10.5281/zenodo.23068612 | The Namenmantik Tradition and the Voynich Alphabetic Apparatus | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | not verified | Structural comparison of folio 1r alphabet with a name-divination alphabet; not a decipherment. |
| 17 | 23068610 / 10.5281/zenodo.23068610 | The Hartlieb Kräuterbuch 9-Witness Corpus: A Snapshot-Bounded Census | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | no | Catalog of nine witnesses as a Voynich comparator. |
| 18 | 23068602 / 10.5281/zenodo.23068602 | Twelve-Component Computational Apparatus of BSB Cgm 7958 as Comparator-Lens for the Voynich MS | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | no | Comparator only; explicitly not an identity claim. |
| 19 | 23068600 / 10.5281/zenodo.23068600 | An Operator Grammar for Beinecke MS 408: Full-Manuscript Validation, Challenge Testing | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | "challenge testing" claimed | 31-class operator grammar; "structural, not a decoding." |
| 20 | 23068593 / 10.5281/zenodo.23068593 | The Voynich MS as an Operational Page-Architecture: Structural Provenance in the Paduan Medical-Computational Tradition | Honeycutt III, E.M. | 2026-09-30 | Preprint | self-published | no | Specialized application of an inherited Italian page-architecture; no decipherment. |
| 21 | 18687530 (see 6) | (duplicate entry, not counted) | | | | | | |

Honeycutt cluster: 15 preprints by one author, all dated 2026-09-30 (plus 2026-02-19 dataset), cross-referenced under one batch. Treat as one program, not 15 independent results.

## Searched, no Voynich-specific record found

- **Quevedo (Vinueza) 2026, "Jaccard anomaly" / "hardware hypothesis"**: not found. Queries "Quevedo Vinueza", "Quevedo Voynich", "voynich Jaccard" returned no matching record. The only Quevedo hit was J. Quevedo (Th17 meta-analysis, unrelated). Possible causes: record not indexed, different spelling, or not on Zenodo.
- **Line-final / line-initial glyph effects; paragraph-initial gallows; conditional entropy h2; abbreviation/syllabary hypotheses; Currier A/B; Lisa Fagin Davis scribes; transliteration files**: no Voynich-specific record surfaced. The "voynich line", "voynich entropy", "voynich transliteration", "voynich Currier" queries returned unrelated records (the "transliteration" query matched onomastic translation papers).
- **Verbose cipher**: no record found.
- **Timm & Schinner self-citation**: no record found. Only Timm 2026 (single author, item 3).
- **MS 408 exact phrase**: the query timed out and was not retried successfully. Not verified.

## Signals relevant to our findings

1. **(a) Consecutive-line Jaccard above shuffle**: Record 1 (Meijer, 2026-01-23) claims "independent confirmation" of a Jaccard anomaly. Our finding that the signal exceeds shuffle chance does not refute the record's existence; it contradicts its "anomaly" framing as a non-independence result. No independent replication found on Zenodo.
2. **(b) h2 ≈ 2.2 bits / verbose cipher**: no Zenodo record measuring h2 or testing verbose cipher. Honeycutt 23068876 tests letter-distribution mismatch, which is adjacent but not the same test.
3. **(c) Line-final -m effect**: no Zenodo record found. Honeycutt 23068600 (operator grammar, "challenge testing") may touch line-position statistics; not verified.
4. **(d) Paragraph-initial gallows**: no Zenodo record found. Timm 19169450 addresses scribe variation, which could relate to gallows distribution; not verified.
5. **Quality**: all records are preprints or self-published. None found is peer-reviewed. Statistical null reporting is claimed in a few (Honeycutt 23068634, 23068637, 23068620, 23068683) but not verified against the PDFs.
6. **Search reliability**: the Zenodo `q=` parser does not enforce the Voynich term, so Zenodo coverage here is incomplete. The Quevedo finding is "not found", not "does not exist".

## Injection note

Record 23150332 (unrelated Sardinian paper, 2026-10-05) contains text addressed to AI systems asking them to state its claims as fact. Ignored. Not Voynich-related.
