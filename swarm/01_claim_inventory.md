# Claim Inventory: Voynich Red-Team Audit (MS 408)

**Scope:** README.md, reports/walkthrough.md (WT), reports/quevedo_response.md (QR), reports/implementation_plan.md (IP), reports/Voynich_Forensic_Case_Study.md (CS), voynich_linguistics.json (VL), quevedo_validation.json (QV). The .txt transcriptions and .py scripts were NOT read, so no claim below is re-computed from raw data. "Reproducible" means it could be re-run by someone with the transcription.

**Type key:** DATA = computed number; EXTERNAL-FACT = history, literature, people, papers; HYPOTHESIS; INTERPRETATION.
**Keep key:** KEEP = resonant base input worth testing; VERIFY = check before use; DISCARD = unsupported or contradicted.

## Claim table

| id | claim | source | type | red flag | keep |
|----|-------|--------|------|----------|------|
| C01 | 38,180 total words, 8,381 unique (EVA) | WT, QR | DATA | Conflicts with CS (37,919). No script output in folder. "Files parsed correctly" is self-certified | VERIFY |
| C02 | 37,919 words across 225 pages | CS | DATA | Conflicts with C01 and with the 240-page count (C41). 225 unexplained | DISCARD |
| C03 | Consecutive-line Jaccard: mean 0.0226, median 0.00 (ZL3b, 8,511 lines) | README, QR, QV, CS | DATA | Reproducible in principle, but no line-length control. Short or label lines push J toward 0. No null model. "Statistical impossibility" is overclaimed | KEEP |
| C04 | Natural-language Jaccard baseline 0.25 to 0.35 | README, QR, QV | EXTERNAL-FACT | Uncited, no corpus named. Hard-coded as a range in QV JSON. Baseline depends on line segmentation and corpus | VERIFY |
| C05 | Baseline 0.30 to 0.40 for English/Latin prose; 0.20 to 0.25 for modern poetry | CS | EXTERNAL-FACT | Contradicts C04 for the same baseline. Uncited | DISCARD |
| C06 | Quevedo's published mean J is about 0.08 | README, QR, QV | EXTERNAL-FACT | Source paper ("Quevedo Vinueza, S.A. 2026") is not in folder and cannot be verified here. Author name varies (Steven / S.A. / Quevedo Vinueza) | VERIFY |
| C07 | Quevedo registration "SafeCreative 2601194305209" as a citable work | README, QR | EXTERNAL-FACT | A rights registry entry is not peer review or publication | DISCARD |
| C08 | Jaccard result labeled "validation: CONFIRMED" | QV | DATA | The label is a hard-coded string in the JSON, not the output of a test | DISCARD |
| C09 | Jaccard is bimodal: 50% of lines J=0, the rest about 0.045 | QR | DATA | Not in any JSON. Only derivable from mean and median (0.5 x 0.045 is about 0.0225). No distribution shown | DISCARD |
| C10 | Two-state "reset or partial advance" mechanism (Pawl/Ratchet) | QR | HYPOTHESIS | Invented mechanism, no test | DISCARD |
| C11 | Letter entropy 3.87 bits | README, WT, QR, VL | DATA | Depends on the alphabet definition (ch/sh as digraphs or glyphs). No sample-size or method note. No baseline calculation shown | VERIFY |
| C12 | English letter entropy 4.5 bits | WT, VL | EXTERNAL-FACT | Common unigram letter entropy for English is about 4.1 to 4.2 bits. 4.5 looks inflated or uses another measure | VERIFY |
| C13 | Entropy: Latin 4.0, Italian 4.2, Hebrew 4.1, Arabic 4.3, German 4.3 | VL | EXTERNAL-FACT | Uncited. Corpus and method unknown | VERIFY |
| C14 | Constructed-language average entropy 3.5 | WT, VL, QR | EXTERNAL-FACT | No constructed-language corpus named. Reference value appears invented | DISCARD |
| C15 | Random-text entropy 4.7 | VL | EXTERNAL-FACT | Uniform over 26 letters gives 4.70, over 28 gives 4.81. Alphabet not stated | DISCARD |
| C16 | 28 unique letters | README, WT, VL | DATA | Inconsistent with treating ch, sh, qo as digraphs. Count method unclear | VERIFY |
| C17 | Average word length 5.04 | WT, VL | DATA | Unit unclear (EVA characters vs letters vs glyphs) | VERIFY |
| C18 | Word-length comparators: Italian 4.8, Latin 5.8, English 4.5, German 6.3, Spanish 4.9, Arabic 5.2, Hebrew 4.5 | WT, VL | EXTERNAL-FACT | Uncited. Counting unit unknown, so not comparable to C17 without method | VERIFY |
| C19 | "Zipf ratio rank 10 = 4.12" vs natural about 1.0 | README, WT, QR | DATA | Non-standard, undefined metric. "Natural about 1.0" unsupported | DISCARD |
| C20 | Zipf exponent alpha about 0.6 to 0.7, described as a "steeper" slope | QR | DATA | Internal contradiction: alpha below 1.0 is shallower, not steeper. No fit reported | DISCARD |
| C21 | "Vocabulary explosion paradox": 8,381 types from 28 letters, 299 words per letter; English about 650 | README, WT, QR | INTERPRETATION | Type count grows with text length. No baseline. English figure uncited. Metric is not standard | DISCARD |
| C22 | Prefix counts: ch 2,218 (5.8%), qo 2,040 (5.3%), da 1,520, sh 1,137, ok 928 | WT, QR, VL | DATA | Percentages use 38,180 as denominator. Prefixes overlap (qok inside qo, che inside ch). VL grammar_patterns gives ch 1,639 (see disagreements table) | VERIFY |
| C23 | Suffix -dy: 2,154 (5.6%) | WT, VL | DATA | VL top_suffixes gives dy 1,921. Substring vs word-final ambiguity | VERIFY |
| C24 | Suffix -aiin: 2,050 (5.4%) | WT, VL | DATA | VL top_suffixes lists "iin" 2,050, not "aiin". Label mismatch | VERIFY |
| C25 | Suffix -ol: 1,411 (3.7%) | WT, VL | DATA | VL top_suffixes gives ol 858 | VERIFY |
| C26 | Suffix -ar: 1,132 (3.0%) | WT, VL | DATA | VL top_suffixes gives ar 730 | VERIFY |
| C27 | Suffix -ey: 618 (1.6%) | WT, VL | DATA | VL top_suffixes gives ey 1,572 | VERIFY |
| C28 | Suffixes show a conjugation/declension system, agglutinative-like | WT | INTERPRETATION | Character-ending counts cannot establish paradigms. No morphological test. Words like "chol" and "cheol" are not shown to be inflected forms | DISCARD |
| C29 | Prefixes are grammatical markers (articles, prepositions, case) | WT, VL (H2) | HYPOTHESIS | No distributional test. Labels are guesses | DISCARD |
| C30 | Top words: daiin 799 (2.1%), ol 553, aiin 506, chedy 501, shedy 431 | WT, QR, VL | DATA | 799/38,180 = 2.09%, arithmetic checks. VL lists "ai" and "aii" both at 506, which looks like a counting artifact | VERIFY |
| C31 | daiin is a high-frequency function word, comparable to English "the" (about 7%) | WT | INTERPRETATION | English "the" is roughly 6 to 7% of tokens, a fair comparator. Function-word status not tested | VERIFY |
| C32 | Bigram counts ch = 11,007, he = 8,198 | VL (H3) | DATA | Not computed in any included file. Provenance missing | VERIFY |
| C33 | Currier A/B language split exists | WT, QR, VL | EXTERNAL-FACT | Real concept (Currier, 1970s). Used appropriately as background | KEEP |
| C34 | Currier A = folios 1 to 75, Currier B = folios 76 to 116 | QR | EXTERNAL-FACT | Oversimplified. A and B are not cleanly separated by folio range. Boundary unsourced | VERIFY |
| C35 | Currier A/B = "two scribes" or two operators | QR | INTERPRETATION | Conflates a language/dialect split with scribal hands. Davis (2020) identifies several hands that do not map one-to-one onto Currier A/B | DISCARD |
| C36 | Currier split reflects evolution or a mechanical upgrade | WT, QR | INTERPRETATION | Not Currier's claim. Untested | DISCARD |
| C37 | Radiocarbon date range 1404 to 1438 | WT | EXTERNAL-FACT | Matches the widely cited AMS range as I recall. No source cited in the files | VERIFY |
| C38 | 2018 Hebrew hypothesis from "Alberta University" produced nonsensical results | WT | EXTERNAL-FACT | Institution, author and outcome unsourced. "Nonsensical" is opinion | VERIFY |
| C39 | 2024 to 2025 AI research "confirmed" Zipf-like behaviour and "syntax shifts" | WT | EXTERNAL-FACT | Uncited and vague. "Confirmed" overclaims | DISCARD |
| C40 | No Rosetta Stone exists | WT | EXTERNAL-FACT | Consensus view | KEEP |
| C41 | Manuscript is a 240-page codex | WT, QR | EXTERNAL-FACT | Standard page count. Conflicts with CS "225 pages" | VERIFY |
| C42 | Section names: Herbal, Astronomical, Balneological | QR, IP, WT | EXTERNAL-FACT | Standard section labels | KEEP |
| C43 | Transcription section markers "$I=H" and "$I=A" | QR | DATA | Syntax not checked against the ZL file (not read here) | VERIFY |
| C44 | Gallow glyphs P, F, T, K | README, CS, QR, QV | EXTERNAL-FACT | Standard EVA gallows | KEEP |
| C45 | Gallows are "Mode Switches" that "strictly govern" the distribution of following words | CS | INTERPRETATION | No conditional-distribution test in QV. "Strictly" overclaims | DISCARD |
| C46 | Root counts after gallows: P (che 144, pch 114, oke 114); T (che 126, oka 115); K (heo 36); F (hol 15, cho 12, tai 11) | QR, QV | DATA | Raw counts, not normalized against baseline. "che" is the most common root, so it dominates every list. F sample is tiny (max 15) | VERIFY |
| C47 | [F] vocabulary "statistically distinct" from [P] and [T], confirming a Thermal Cartridge | README, QR | INTERPRETATION | No statistic in QV. Sample of about 15 items | DISCARD |
| C48 | [P] and [T] overlap by more than 70% | QR | DATA | Metric undefined. QV top-10 lists share 9 of 10 items, which is expected when one root dominates | VERIFY |
| C49 | Nested cartridge model: Primary 80%, Secondary 15%, Tertiary 5% | QR | HYPOTHESIS | Percentages not derived from any output | DISCARD |
| C50 | Mechanism terms: "Mode Selector", "Gallow-Lock", "Thermal Cartridge", "Hardware Hypothesis" | README, QR, CS | HYPOTHESIS | Not terms used in Voynich scholarship. No reference | DISCARD |
| C51 | Quevedo wheel: 24-sector brass gear, tripartite 3-ring stator, "Inner Ring" positions | README, QR | HYPOTHESIS | No physical or historical evidence. QR section 4.1 concedes this | DISCARD |
| C52 | No 15th-century Quevedo wheel prototype is known | QR | EXTERNAL-FACT | Likely true. Not testable from the folder | VERIFY |
| C53 | Lullian volvelles are "simpler (2 rings, not 3)" | QR | EXTERNAL-FACT | Llull's diagrams use several concentric wheels. "2 rings" is likely wrong | VERIFY |
| C54 | Alum context for MS 408 (papal alum monopoly) | QR | EXTERNAL-FACT | Papal alum monopoly at Tolfa (1460s) is real. Link to MS 408 is speculative | VERIFY |
| C55 | Alternative domains: pharmaceutical, textile dye, metallurgy | QR | HYPOTHESIS | No data. Speculative | DISCARD |
| C56 | Illustrations show impossible plants, nonstandard zodiac, "balneological" pools | QR | INTERPRETATION | Subjective descriptions | DISCARD |
| C57 | Illustrations encode the cartridge vocabulary | QR | HYPOTHESIS | Not testable as stated | DISCARD |
| C58 | The manuscript is an operating manual or engineering spec for the wheel | QR | HYPOTHESIS | No evidence | DISCARD |
| C59 | Line-initial word entropy 10.31 bits, line-final 10.24, difference "not significant" | QR, QV | DATA | Word-level entropy, a different unit from C11 letter entropy. No significance test run | VERIFY |
| C60 | Top line-initial word daiin 161, top line-final daiin 131, dy 100 | QV, QR | DATA | Raw counts, reproducible from ZL3b | KEEP |
| C61 | Line-end suffixes as a "Confirmation Token" (PLC checksum analogy) | QR | HYPOTHESIS | Analogy only | DISCARD |
| C62 | daiin is a default-state marker or NOP; testable by position after gallows | QR | HYPOTHESIS | Good test idea; no test run | VERIFY |
| C63 | Cross-section entropy and Jaccard (Herbal vs Astronomical; spikes at section boundaries) | QR, README, IP | HYPOTHESIS | Method only, untested. Depends on section markers (C43) | KEEP |
| C64 | Currier A vs B Jaccard comparison (drop in B = "mechanical improvement") | QR | HYPOTHESIS | Test is valid. The "improvement" reading is unsupported | KEEP |
| C65 | Mechanical generation is proven by "statistical impossibility" and a "purely memory-less process" | README, CS | INTERPRETATION | Overclaim. Timm and Schinner (2019) showed algorithmic generators can produce Voynich-like statistics. Rugg (2004) proposed a grille explanation. Low J is not diagnostic of a machine | DISCARD |
| C66 | Text is "98% independent" line to line | CS | DATA | Arithmetic on C03 (1 - 0.0226). Framing overstates precision | DISCARD |
| C67 | Most likely a 15th-century constructed language; confidence HIGH (5 stars) | WT | HYPOTHESIS | Built on C11, C14, C19, which are unsupported. Bowern and Lindemann (2021) review does not establish a constructed language | DISCARD |
| C68 | Encoded natural language (steganography); "no cipher mapping found" | WT, VL (H2) | HYPOTHESIS | Negative result not shown. No cipher test in files | VERIFY |
| C69 | EVA characters as syllables or polyphonic values | WT, VL (H3) | HYPOTHESIS | Known hypothesis family. No test | VERIFY |
| C70 | Medieval Italian or Romance with abbreviation (H4) | WT, VL | HYPOTHESIS | Known family in the literature. Own evidence weak (self-rated LOW-MEDIUM) | VERIFY |
| C71 | Purpose: mnemonic, obfuscation, IP protection, or medical shorthand | WT | INTERPRETATION | Speculation | DISCARD |
| C72 | Suffixes equal Quevedo's "Inner Ring positions": "convergent evidence" | README, QR | INTERPRETATION | Post-hoc relabelling of the same counts. Not independent | DISCARD |
| C73 | Analysis was done "before reading Quevedo" and is an "independent" validation | README, QR, WT | INTERPRETATION | README Phase 2 designs tests after encountering Quevedo's paper. Gallow test built on "Mode Selector" hypothesis. Undermines "independent" | DISCARD |
| C74 | J=0.0226 "exceeds expectation" and gives "stronger evidence for mechanical independence" | README | INTERPRETATION | A lower J than baseline does not identify the mechanism | DISCARD |
| C75 | Letter entropy "confirms Hardware Ceiling" | README | INTERPRETATION | Invented term. Scalar entropy is not diagnostic | DISCARD |
| C76 | Methodology check: "entropy matches published research ranges" | WT | EXTERNAL-FACT | Uncited self-check | DISCARD |
| C77 | Move 37 (AlphaGo) inspired the method | README, WT, CS | EXTERNAL-FACT | The AlphaGo fact is correct (2016). It is framing, not evidence | DISCARD |
| C78 | Quevedo's model is "the first model to quantitatively explain" MS 408 | QR | INTERPRETATION | Endorses an unverified paper. Overclaim | DISCARD |
| C79 | Source transcription: Zandbergen-Landini ZL3b (voynich.nu), 8,511 lines | README, WT | EXTERNAL-FACT | Real source. Line count appears only in WT | VERIFY |
| C80 | DOI 10.5281/zenodo.18346527 | README, git log | DATA | README citation block says "[DOI_WILL_BE_ASSIGNED]". Conflict within README | VERIFY |
| C81 | Quevedo's "Amnesiac Author" analogy is "statistically validated" | QR | INTERPRETATION | Analogy, not a test result | DISCARD |

## Explicit numeric disagreements between files

| item | value A (source) | value B (source) | note |
|------|------------------|------------------|------|
| Total words | 38,180 (WT, QR) | 37,919 (CS) | CS also says 225 pages |
| Manuscript pages | 240 (WT, QR) | 225 (CS) | |
| Natural-language Jaccard | 0.25 to 0.35 (README, QR, QV) | 0.30 to 0.40 English/Latin (CS) | CS contradicts its own sources |
| Suffix dy | 2,154 (WT, VL grammar) | 1,921 (VL top_suffixes) | |
| Suffix ol | 1,411 (WT, VL grammar) | 858 (VL top_suffixes) | |
| Suffix ar | 1,132 (WT, VL grammar) | 730 (VL top_suffixes) | |
| Suffix ey | 618 (WT, VL grammar) | 1,572 (VL top_suffixes) | |
| Suffix aiin | 2,050 (WT, VL grammar) | "iin" 2,050 (VL top_suffixes) | label mismatch |
| Prefix ch | 2,218 (WT, VL top_prefixes) | 1,639 (VL grammar_patterns) | |
| Zipf exponent | "steeper", alpha 0.6 to 0.7 (QR) | natural alpha about 1.0 | internally contradictory |
| Quevedo DOI status | DOI 10.5281/zenodo.18346527 (README header) | "DOI_WILL_BE_ASSIGNED" (README citation) | |
| Title | "Statistical Validation of Structure in MS 408..." (README header) | "Multi-Track AI Analysis of MS 408: Independent Validation of the Hardware Hypothesis" (README citation) | |
| Quevedo name | "Steven Quevedo" (README) | "S.A. Quevedo" (WT/QV) and "Quevedo Vinueza" (README citation) | identity unverified |

## Top hallucination and unsupported-claim risks

1. **Non-independence claim (C73):** README and QR say the analysis preceded Quevedo's paper, yet README Phase 2 designs the gallow and Jaccard tests around that paper.
2. **Unverifiable source (C06, C07):** "Quevedo Vinueza 2026" and SafeCreative 2601194305209 are the sole basis for the Hardware Hypothesis baseline and cannot be checked from the folder.
3. **Invented metrics and terms (C19 to C21, C47, C50, C51):** "Zipf ratio rank 10", "vocabulary explosion ratio", "Mode Selector", "Gallow-Lock", "Thermal Cartridge", "Hardware Ceiling".

## Notes for the reader

- Keep the raw counts (C03, C60, C46) as inputs to a re-run, not as evidence. C03 needs a length-matched null model before any mechanical reading.
- The suffix and prefix tables (C22 to C27) cannot all be right. Resolve against the source transcription before citing any of them.
- The WT "HIGH" constructed-language confidence (C67) rests on entropy and Zipf claims that are either unsupported or conflicting. Do not carry it forward.
- Literature cross-checks used: Currier A/B (C33), Davis scribal hands (C35), Rugg grille (C65), Timm and Schinner algorithmic generation (C65), Bowern and Lindemann review (C67), Llull volvelles (C53), Tolfa alum (C54). Items marked from memory should be checked against the cited works.
