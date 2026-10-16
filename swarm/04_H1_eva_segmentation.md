# 04 H1: is low Voynich h2 an artifact of EVA segmentation?

Scripts: `swarm/scripts/h1_seg.py` (python -I; args: parsed json, baselines dir, out json). Voynich = ZL3b parse (`parsed_zl3b.json`, 37,954 words). Raw numbers: scratchpad `h1_res.json`.

## Method
- Stream = words joined by one space symbol; h2 = H(X_n | X_n-1) (plug-in, bigram entropy minus unigram entropy). "sp" = space counted as a symbol; "nosp" = spaces removed, words concatenated.
- Equal sample size: 8 random contiguous chunks of 40,000 symbols per condition (units after segmentation, spaces counted when present); mean +- sd across chunks (chunks overlap, so sd understates true uncertainty; Currier A has under 40k symbols, so its single chunk has sd ~0). Alphabet = distinct symbols incl. space over the full stream. wl = mean word length in units.
- Segmentation by greedy longest match inside words:
  - S1: ckh cth cph cfh ch sh (benched gallows and ch/sh as single letters; Currier/FSG/v101-style units)
  - S2: S1 + iiin iin iii ii in (minim sequences as units)
  - S3: S2 + eee ee
  - S4 (aggressive, NOT a published standard): S3 + aiin aiir ain aii ai dy ol or al ar. Upper bound.
  - BPEk: data-driven, k most frequent within-word pair merges. The same BPE applied to natural texts is the fair control, because ANY merging raises h2 by inflating the alphabet.
- Baselines (Gutenberg, saved in scratchpad/baselines; language verified from metadata and text samples; header/footer stripped, lowercased, diacritics removed, a-z only, no abbreviations):
  - Latin: Caesar, De Bello Gallico I-IV, PG218 https://www.gutenberg.org/cache/epub/218/pg218.txt and V-VIII, PG18837 https://www.gutenberg.org/cache/epub/18837/pg18837.txt (369k symbols; classical prose, not medieval; no medieval Latin text found quickly).
  - Italian: Dante, Divina Commedia, PG1000 https://www.gutenberg.org/cache/epub/1000/pg1000.txt (verse, 507k).
  - German: Goethe, Faust I, PG2229 https://www.gutenberg.org/cache/epub/2229/pg2229.txt (verse, 180k).
  - English: Austen, Pride and Prejudice, PG1342 https://www.gutenberg.org/cache/epub/1342/pg1342.txt (692k).
  - Wrong guesses downloaded and deleted (English, not used): PG10657, 12816, 23700, 2701. Total download ~5.7 MB.
- Verbose cipher: each plaintext letter -> fixed 2-glyph code from a random 6x5 grid (11 distinct glyphs used + space); h2 measured on the glyph stream. A unit-level check (code read as 2-glyph units) reproduces plain h2, as expected.

## 1. Voynich, segmentation (ZL, all text)
| condition | alphabet | wl | h0 | h1 | h2 (sp) | h2 (nosp) |
|---|---|---|---|---|---|---|
| EVA raw | 27 | 5.07 | 4.63 | 3.86 | 2.19 +- .06 | 2.38 +- .06 |
| S1 | 33 | 4.59 | 4.94 | 3.85 | 2.26 +- .10 | 2.51 +- .11 |
| S2 | 38 | 4.31 | 5.13 | 3.80 | 2.26 +- .17 | 2.53 +- .19 |
| S3 | 40 | 4.07 | 5.23 | 3.89 | 2.43 +- .11 | 2.73 +- .12 |
| S4 (aggressive) | 50 | 3.40 | 5.57 | 4.14 | 2.68 +- .14 | 3.16 +- .16 |
| BPE8 | 35 | 3.80 | 5.04 | 4.22 | 2.59 +- .08 | 2.99 +- .08 |
| BPE15 | 42 | 3.08 | 5.32 | 4.38 | 2.84 +- .08 | 3.45 +- .07 |
| BPE25 | 52 | 2.76 | 5.64 | 4.58 | 3.17 +- .04 | 3.96 +- .02 |

## 2. Natural-language baselines (same chunk size, plain letters)
| text | alphabet | wl | h0 | h1 | h2 (sp) | h2 (nosp) | BPE12: alphabet / h2 sp / h2 nosp |
|---|---|---|---|---|---|---|---|
| Latin (Caesar) | 25 | 6.17 | 4.54 | 4.02 | 3.29 +- .01 | 3.44 +- .01 | 37 / 3.62 / 3.96 |
| Italian (Dante) | 25 | 3.96 | 4.54 | 3.93 | 3.10 +- .01 | 3.37 +- .01 | 37 / 3.35 / 3.85 |
| German (Faust) | 27 | 4.79 | 4.75 | 4.05 | 3.14 +- .01 | 3.38 +- .02 | 39 / 3.51 / 4.05 |
| English (P&P) | 27 | 4.38 | 4.75 | 4.09 | 3.28 +- .02 | 3.57 +- .02 | 39 / 3.54 / 4.07 |

(Word lengths for verse texts are affected by elision/verse; irrelevant to h2.)

## 3. Verbose-cipher transform (letter -> 2 glyphs), glyph level
| text | alphabet | wl (glyphs) | h1 | h2 (sp) | h2 (nosp) |
|---|---|---|---|---|---|
| Latin | 12 | 12.5 | 3.45 | 2.11 | 1.98 |
| Italian | 12 | 8.0 | 3.47 | 2.08 | 1.97 |
| German | 12 | 9.7 | 3.54 | 2.10 | 2.00 |
| English | 12 | 8.7 | 3.55 | 2.17 | 2.06 |

Encoding alone drops h2 from ~3.1-3.3 to ~2.1, i.e. Voynich's raw value (2.0-2.2). But the cipher has a 12-symbol alphabet, 8-12 glyph words (Voynich ~5), strictly periodic 2-glyph structure, and nosp h2 below sp h2 (Voynich is the opposite: 2.38 vs 2.19). The match is on h2 only.

## 4. Currier A vs B
| | EVA raw | S2 | S4 |
|---|---|---|---|
| A (single chunk, <40k) | 2.18 (nosp 2.36) | 2.48 (2.77) | 2.85 (3.35) |
| B | 2.00 (2.19) | 2.19 (2.45) | 2.54 (3.01) |

B is lower than A under every segmentation by ~0.2-0.3 bit. Neither reaches plain-language sp values (3.1-3.3) except A under S4 with spaces removed (3.35), the most aggressive and least justified condition.

## 5. Verdicts per sub-claim
1. "Segmentation explains part of the low h2": TRUE but small. Under the standard defensible segmentations (S1, S2) h2 rises only ~0.07 bit (2.19 -> 2.26; nosp 2.38 -> 2.53), within noise. S3 (+ee) gives +0.24. Defensible-segmentation h2 stays ~0.9-1.0 bit below any plain language (3.10-3.29).
2. "h2 reaches natural range under a plausible segmentation": NOT SUPPORTED. Only S4 (merging ol/or/al/ar/dy/ai/ain/aiin, nearly every frequent bigram) reaches 2.68 sp / 3.16 nosp, with alphabet inflated to 50; that is alphabet inflation, not recovery of letters.
3. Inflation-matched control: natural text with BPE12 (alphabet 37-39) has h2(sp) 3.35-3.62 versus Voynich BPE8-BPE15 (alphabet 35-42) 2.59-2.84, a stable gap of ~0.75 bit. Voynich is lower-entropy than natural language at every granularity tested, including purely data-driven units.
4. The low raw h2 is therefore mostly a real property of the glyph sequence (strong local predictability), not an artifact of EVA's alphabet design.
5. Verbose cipher: reproduces the raw h2 (~2.1) from any of the four languages, so low h2 alone cannot discriminate "unusual language" from "verbose encoding".

## 6. What is firm, what stays open
Firm (h2 at all defensible segmentations is <= ~2.7 sp vs >= 3.1 in four plain languages):
- Not a simple monoalphabetic substitution (one glyph or one S1/S2-type glyph-unit per letter) of Latin, Italian, German or English plaintext; renaming symbols leaves h2 unchanged (unit-level check), and segmentation does not close the ~0.9 bit gap.
- Not explainable by EVA transcription choices alone.
Open:
- Verbose/nomenclator-type cipher (reproduces h2, but must also explain 5-glyph words, narrow word-length distribution, and the sp/nosp pattern; test in a later wave).
- Syllabary (BPE shows the data cannot be ruled out by h2 alone at larger unit sizes; also units can be bigger than letters, making per-symbol h2 higher but still below baselines at matched alphabet).
- Abjad / heavily abbreviated text (not directly tested; dropping vowels would normally raise per-symbol entropy, which argues against it, but unverified).
- Other source languages (Hebrew, Arabic, Slavic, medieval abbreviated Latin) and generative-process hypotheses (self-citation, table lookup) are untouched.

## 7. Caveats
- Chunks overlap and come from one stream; sd is optimistic. Plug-in h2 is biased low for large alphabets (S4, BPE25: ~2500 bigram cells vs 40k samples); same bias applies to baselines in the matched comparison but absolute S4/BPE25 numbers are less reliable.
- Genres differ (verse vs prose vs Voynich); Latin is classical Caesar, not medieval; no Latin abbreviations modelled.
- Line breaks treated as spaces; ZL3b parse only (RF1b not rerun, but prior work shows near-identical h2 2.17).
- S3/S4 unit inventories are my own constructions, not published standards; greedy longest-match ordering is arbitrary.
