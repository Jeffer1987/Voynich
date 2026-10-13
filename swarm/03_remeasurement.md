# 03 Independent re-measurement (ZL3b, spot-check RF1b)

Method: fresh parser (no prior scripts read). Strip locus tags/comments, split on "." and ",", [a:b] -> first option, {..} ligature braces and "'" removed, words containing ? @ ! ; digits dropped. Page vars $I $L $H $Q kept. Paragraph = lines between <%> and <$> markers (ZL only; RF1b has no <%>).
Parsed data: `C:/Users/Jeffrey/AppData/Local/Temp/claude/J--Mijn-Drive-00-Voynich-Red-team-magnetic-cosmos--claude-worktrees-voynich-subagents-hypotheses-593993/194b83ce-2de0-4696-8833-e22ebb22ff7d/scratchpad/parsed_zl3b.json` (5352 lines; fields folio, line, lt, pstart, pend, par, I, L, H, Q, words) and `parsed_rf1b.json` (same dir). Scripts: parse.py, analyze.py; raw results res_zl.json, res_rf.json.
Natural-language baseline: only English available offline = Python stdlib pydoc_data.topics (technical English, 76k tokens, 34k used, 2412 types; poor but usable). Synthetic: iid unigram, Zipf s=1 (V=8424). Nulls are means of 5-20 shuffles.

## 1. Basic statistics
| | ZL3b | RF1b | English (pydoc) |
|---|---|---|---|
| tokens / types | 37954 / 8424 | 33728 / 7850 | 76059 / 3359 |
| hapax share of types | 0.71 | 0.71 | - |
| h0 (alphabet incl. space) | 4.75 (27) | 4.70 (26) | 4.75 |
| h1 | 3.87 | 3.88 | 4.10 |
| h2 (conditional) | 2.16 | 2.17 | 3.32 |
| mean word length | 5.09 | 5.08 | 4.88 |

Word length share (ZL): 1:.035 2:.062 3:.088 4:.176 5:.244 6:.193 7:.116 8:.049 9:.020 10+:.014 (narrow, near-binomial, peak at 5).
- Finding: h2 about 1.1 bit below English with similar h0/word length: ANOMALOUS (strong; replicates in RF1b). h1 only mildly low.

## 2. Line-to-line vocabulary Jaccard (consecutive lines within paragraph, n=3390)
| condition | mean | median |
|---|---|---|
| ZL3b real | 0.032 | 0 |
| shuffle lines globally | 0.012 | 0 |
| shuffle lines within folio | 0.025 | 0 |
| iid words (unigram, same line lengths) | 0.013 | 0 |
| Zipf s=1 synthetic | 0.051 | 0.05 |
| English sequential, same line-length profile | 0.092 | 0.067 |
| RF1b real / global shuffle / within-folio | 0.026 / 0.011 / 0.023 | 0 |
By line length (words): 1-4: .017, 5-8: .026, 9-12: .037, 13+: .042 (Jaccard rises with line length, so length must be matched).
- Finding: low ABSOLUTE Jaccard is NOT by itself anomalous; it is driven by lexical richness (71% hapax types, TTR 0.22 vs English 0.07, no function-word core). Relative to shuffles the real value is 2.7x the global null and 1.3x the within-folio null: slightly ABOVE chance (page/topic drift), not "lines are independent". English is higher mainly because of repeated function words; the English comparison is weak (small, technical, different TTR). Do not cite "low Jaccard" as an anomaly without a richness-matched baseline.

## 3. Stratification (ZL, tokens; h1/h2)
| stratum | tok | h1 | h2 | top words |
|---|---|---|---|---|
| Currier A | 10974 | 3.85 | 2.20 | daiin chol chor s shol ol |
| Currier B | 23724 | 3.87 | 2.02 | chedy ol shedy aiin daiin qokeedy |
| Hand 1 | 10402 | 3.84 | 2.20 | daiin chol chor |
| Hand 2 | 10960 | 3.86 | 1.97 | shedy ol chedy qokedy qokain |
| Hand 3 | 11685 | 3.88 | 2.03 | aiin chedy qokeey ar al |
| Hand 4 | 3558 | 3.80 | 2.26 | ar aiin al oteey |
| Herbal(H) | 10845 | 3.86 | 2.22 | daiin chol s chor |
| Stars/recipes(S) | 11586 | 3.88 | 2.02 | aiin chedy ar qokeey |
| Biological(B) | 6306 | 3.82 | 1.82 | ol shedy chedy qokain qokedy |
| Pharma(P) | 2519 | 3.80 | 2.14 | daiin chol ol |
| Cosmo(C) / Text(T) / Zodiac(Z) | 2193/2346/1291 | 3.85/3.90/3.76 | 2.27/2.09/2.11 | |
Line-final glyph "y": A 34%, B 43% (B-section 53%); line-initial top: A "o" 18%, B "s" 16%, B-section "q" 25%.
- Finding: h1 is flat across strata; h2 varies 1.8-2.3 (A/hand 1 higher than B/hand 2,3). A/B vocabularies differ strongly (top words disjoint-ish): REAL, well-known, anomalous vs a single-language null; B-section (biological) most repetitive/lowest h2.

Line position effects (Jensen-Shannon, real vs permutation null mean/max over 100 perms, ZL lines >=3 words):
| contrast | real | null mean | null max |
|---|---|---|---|
| first word vs middle: initial glyph | 0.180 | 0.001 | 0.002 |
| last word vs middle: final glyph | 0.084 | 0.001 | 0.002 |
| last vs middle: initial glyph | 0.038 | 0.001 | 0.002 |
| first vs middle: word length | 0.017 | 0.0005 | 0.001 |
Mean word length first/mid/last = 5.44 / 5.08 / 4.87. Line-final glyph: y 39% (mid-line 42%), m 15.5% (vs ~1-3% mid), n 15%; line-initial: d .15 s .15 y .15 o .14 q .13; mid-line initial c .21 o .21 q .17. RF1b replicates (0.163 / 0.080).
- Finding: line-as-unit effect (first-word glyph, final "m", shorter last word): ANOMALOUS, >100x permutation null, replicates in RF1b. English chunked arbitrarily would be 0 by construction (sentence breaks aside), so this is a real property of the layout.

Paragraph-initial gallows (ZL, 740 paragraphs): first word of paragraph begins with k/t/p/f in 82.7%; first word of other lines 8.6%; mid-line words 6.3%.
- Finding: ANOMALOUS (13x enrichment; first-line effect); RF1b cannot test (no paragraph markers).

## 4. Word structure
Slot grammar P?G?C?E?V?Fin (P: qo|q|o|y|d|s; G: k t p f cth ckh cph cfh; C: ch|sh; E: e{1-3}; V: o|a; Fin: dy aiin ain iin in ol or ar al am y l r s m n d g), full-match:
| | tokens | types |
|---|---|---|
| ZL3b | 0.657 | 0.216 |
| RF1b | 0.653 | 0.221 |
| same words with letters shuffled within word | 0.111 | |
| English words | 0.163 | |
Endings (ZL, tokens): y .228, dy .175, aiin .101, ol .091, ar .073, or .057, al .054, in .053, other .168. Prefixes: o .23, ch .16, q .14 (qo .138), s .12, d .09, sh .08.
- Finding: tokens fit the grammar 6x more than letter-shuffled controls (slot structure is real), BUT the grammar was hand-specified by me with many optional slots and covers only 22% of types (type-level fit is low: rare words violate it), so "fits slot grammar" is weak evidence of anything beyond heavy positional letter constraints. Anomalous vs shuffled-letters; not tested against a fitted-to-English null.

Repetition (consecutive words in a line):
| | identical | edit distance 1 |
|---|---|---|
| ZL real | 0.88% | 3.76% |
| word-shuffled globally | 0.28% | 1.58% |
| word-shuffled within folio | 0.64% | 2.53% |
| English (same line profile) | 0.56% | 1.62% |
| RF1b real / global null | 0.85% / 0.33% | 3.62% / 1.62% |
- Finding: identical consecutive words 3x global null, 1.4x within-folio null (mostly frequency + page effect): modest. Edit-distance-1 neighbours 2.4x global, 1.5x within-folio null: ANOMALOUS-mild (known self-similarity/copy effect), small in absolute terms.

## Summary of verdicts
- h2 conditional entropy ~2.16 vs English 3.3: anomalous.
- Low line Jaccard: not anomalous after shuffle/richness control (slightly above chance).
- Line-initial/final glyph and paragraph-initial gallows effects: anomalous, replicated.
- A/B and hand/section differences in vocabulary and h2: real.
- Slot-grammar fit: above letter-shuffle control, but hand-built and weak at type level.
Caveats: no real Latin/Italian/Hebrew comparison text offline; English baseline is technical and small; ZL words with ? / @ dropped (~4%).
