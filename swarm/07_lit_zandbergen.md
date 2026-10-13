# 07 Literature check: Zandbergen (voynich.nu) and linked sources

Scope and honesty note: voynich.nu pages fetched and read via a summarising fetcher (a1-a5 analysis pages). Several PDFs (Bowern & Lindemann 2021, Gaskell & Bowern CEUR paper) could NOT be text-extracted; claims about them come from search snippets and secondary pages and are marked [secondary]. Nothing below about Davis 2020, Montemurro 2013, Rugg 2004 was read at primary level; those are from memory/secondary and flagged. Verify before citing.

Sources actually read:
- https://www.voynich.nu/ (index; author note 27/03/2026; Voynich 2026 conference, Malta: https://www.um.edu.mt/events/voynich2026/)
- https://voynich.nu/analysis.html (updated 25/05/2025; structure of statistical analysis pages a1-a5)
- https://voynich.nu/a2_char.html (entropy, word-position, line-position effects)
- https://voynich.nu/a3_para.html (word structure models)
- https://voynich.nu/a5_synt.html (sentences, paragraphs, sections)
- Search results: https://ceur-ws.org/Vol-3313/paper6.pdf (Bowern & Gaskell, manipulation tests) [snippet only]; https://lingbuzz.net/lingbuzz/005939 (review of Bowern & Lindemann) [snippet only]; Voynich.ninja threads (forum, not peer reviewed); Stolfi notes https://www.ic.unicamp.br/~stolfi/voynich/Notes/063/077/dics/note/Notebook-old/Notebook-5.txt

## Per-finding

### (a) Jaccard anomaly / line independence (refuted: consecutive lines slightly MORE similar than shuffle)
- Known: Currier (1976, via voynich.nu a2_char) found NO repeated group running from the end of one line to the start of the next; he treats the line as a functional unit. Missing repeated multi-word phrases is a long-noted oddity (a5_synt section 5.3, citing Segre Rutz 2000 for herbals). Voynich.ninja posts report mutual information persisting at 50-100 char distances [forum, unreviewed]; Smith and Ponzi report anomalies on second words of lines [forum].
- New: a quantified consecutive-line vs shuffled-line similarity test with a null model. I found no published equivalent. Your result (slight positive adjacency) is consistent with local topic/vocabulary drift (also Montemurro & Zanette 2013, topic-like burstiness [from memory]) but contrasts with Currier's "no cross-line repeats" (which concerns exact boundary repeats, a different statistic).
- Implication: state the refutation as "weak positive adjacency, effect size X, vs shuffle null". Do not frame as contradicting Currier; different quantity. Control for section/page-level drift by shuffling within page or paragraph, otherwise adjacency is just topical clustering.

### (b) Low h2 about 2.2 bits; not an EVA segmentation artifact; verbose cipher matches h2 but word length 8-12 vs about 5
- Known: Bennett (1976): H1 3.66, H2 2.22, H3 1.86 vs languages 3.91-4.14 / 3.01-3.37 / 2.12-2.62; confirmed by Stallings (a2_char). Zandbergen: no modern European language matches in H1-vs-H2 plot (UDHR); some Asian/Austronesian near (Tagalog, Hawaiian, Minjiang). Lindemann & Bowern (2020/2021): h2 distinctly below all 316 comparison texts, driven by positional restriction of common characters. a3_para: restrictive word structure "explains the anomalously low conditional entropy", cause/effect unresolved; implies unlikely an encipherment of an Indo-European plaintext with 15th-c methods. Bowern & Gaskell (CEUR Vol-3313) [snippet]: several encipherments lower conditional entropy, bigraph encoding of Latin reaches Voynich-like character entropy, so low entropy alone does not prove gibberish or exclude cipher.
- New: the matched-alphabet gap of about 0.75 bit, and the cross-check that a verbose cipher can match h2 only at the cost of 8-12 glyph words. This joint (h2 + word length) constraint is the strongest part; the literature mostly argues entropy alone. Vogt/Zandbergen note EVA is not ideal for statistics; your segmentation-robustness check answers that directly.
- Implication: present as a two-statistic constraint. Verbose-cipher rebuttal must test the Bowern/Gaskell bigraph schemes at matched word length.

### (c) Line as functional unit: line-final -m 15.3% vs 1.0% mid-line (also -g), outermost word only, both A and B (B stronger); line-initial y, p, t enriched; -m words are ordinary stems ending -l/-r/-n mid-line
- Known: Currier (1976): line start/end character frequencies differ markedly from interior; some characters never line-initial, some about 1/100 expected; small letter groups only at line ends; one symbol ends the last word 85% of lines (a2_char). Currier: "unattached finals" much more frequent in B than A (a5_synt). Vogt (2012) "The Voynich Line": first word of a line about 1 char longer (EVA). Community term LAAFU (line as a functional unit), second-word anomalies (Smith, Ponzi) [forum]. Stolfi raises transcription word-break disagreements as a possible source of line-edge artifacts [Notebook-5].
- Already known: the phenomenon in general, B>A, finals. Probably not new: -m/-g line-final enrichment per se (Currier's "85%" symbol is likely the -m/-g class; check).
- New / under-explored: (i) the "outermost word only, every line" localisation; (ii) the stem-identity result: line-final -m words are the same stems as mid-line words ending -l/-r/-n, i.e. a line-end suffix substitution, not a separate vocabulary; (iii) quantified rates 15.3% vs 1.0% with A/B split. I found no published stem-level decomposition.
- Implication: points to a layout/scribal mechanism (line-end marker or line-fill/justification) rather than linguistic content. Test against line length and right-margin position (line-fill hypothesis).

### (d) Paragraph-initial gallows 83% (mostly p), first word only
- Known: D'Imperio (1978): split gallows occur only on first lines of paragraphs and in labels (a5_synt). Widely discussed "Grove words"/ first-letter-of-paragraph gallows (Sean/Stolfi/Zandbergen forum lore) [not verified].
- New: the 83% figure with p dominance and the restriction to the first word only. Treat as quantification, not discovery.
- Implication: cite D'Imperio; check whether the effect is the first word of the paragraph, not first word of the line (distinguish from line-initial y/p/t).

### (e) Currier A/B, Davis hands, sections differ in vocabulary and h2
- Known: Currier A/B (1976); Davis (Manuscript Studies, 2020): five scribes vs Currier's seven; scribe D1 about 113 of 227 pages; 67 pages Currier left unclassified, 32 disagreements [secondary: Nick Pelling blog/Goodreads, Voynich.ninja]. Lindemann & Bowern: A/B are different in word statistics, consistent with scribal/topic/ dialect variation, not resolved. Zandbergen (a4_word, page clustering) not read.
- New: h2 differences by hand and a hand-by-section decomposition (A/B vs hand vs section confounded: Currier pages are section-specific). Under-explored: whether h2 differences survive within one section.
- Implication: need a nested/partial analysis (hand within section) before attributing to hand.

## Methods lessons (from the field)
1. EVA is a transliteration for convenience, not an alphabet; word-length and entropy depend on the glyph parsing (a2/analysis.html). Always run a second parsing (e.g. ch/sh/cth/ckh as units; Currier/Takahashi) and report both.
2. Uncertain spaces and transcription disagreements can create line-edge artifacts (Stolfi). Use a consensus or multiple transcriptions (Takahashi, Zandbergen-Landini, Currier) and test line effects across them.
3. Labels vs paragraph text vs circular text must be separated; gallows and positional rules differ (D'Imperio). Exclude labels and radial/circular text from paragraph line statistics.
4. Section/hand/language confounding: Currier A/B tracks sections; any between-group claim needs partial controls.
5. Comparison corpora matter: Timm & Schinner (2021) criticise Bowern & Lindemann's Wikipedia parsing; match genre, alphabet, orthography, and text length. Small samples bias h2 (finite-size correction needed).
6. Low entropy alone is weak evidence for or against language: ciphers, abbreviations and bigraph encodings (Bowern & Gaskell) also lower it. Use multi-statistic profiles.
7. Gibberish-generation baselines (Rugg 2004 grille; Gaskell & Bowern 2022 human-generated gibberish) are the proper null, rather than only natural language or random text [from memory, not read].
8. Forum findings (Voynich.ninja) are often unreviewed: use as hypothesis sources only.

## Most promising open questions (field)
Origin of the restrictive word structure; the line-position effects (LAAFU); lack of repeated phrases; A/B explained by scribe vs system; relation between paragraphs and gallows initials.

## Recommended novel next tests
1. Line-length / right-margin test of -m/-g: does line-final -m probability rise when line ends near the margin or when the line is short vs long (line-fill hypothesis)? Use per-folio line geometry from the Zandbergen/ Landini ZL or Takahashi data with line-end coordinates if available.
2. Stem-substitution test: for each stem occurring both mid-line (-l/-r/-n) and line-final (-m), test if the line-final alternation is a deterministic function of position (paired design), and whether the alternation also occurs in the second-last word at lower rate (gradient).
3. Gibberish-null calibration: apply the line-final and h2/word-length joint statistics to Rugg-style grille output and a human-written pseudo-text corpus (Gaskell & Bowern) to see whether a line-edge effect of 15x arises from copying/line-breaking habits.
4. Wrapped-vs-natural line test: compare lines ending at a paragraph end vs lines wrapped mid-paragraph; if -m is a line-wrap phenomenon it should hold at wraps, and differ at paragraph ends. Plus: compare first-word y/p/t after a -m ending (cross-line dependency, linking (a) and (c)).
5. Within-section A vs B h2 and -m rate comparison (partial-control design) using Davis hands as a third factor, with bootstrap by page.
