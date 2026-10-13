# 05  H2 (line as functional unit) and H3 (paragraph-initial gallows as layout device)

Data: parsed ZL3b (primary) and RF1b (replication) from 03_remeasurement. Scripts (run `python -I`): `scripts/h23_common.py`, `h2a.py`, `h2bc.py`, `h3.py` (args: `zl3b|rf1b <n_shuffles>`).
Nulls: words permuted within folio among slots of the tested line class (line lengths and positions fixed), 300-1000 shuffles. Permutation p floors at 1/(B+1); z is quoted as the effect-size measure.
Definitions. P-lines = paragraph text (locus type P), 3 or more words for position tests. "Continuation lines" = P-lines that are not paragraph-first. Mid = positions 2..n-1. Paragraph-first = ZL `<%>` marker (740 paragraphs); RF1b has no markers, so only `@P` lines are used (263), and RF1b "later-line" bins therefore still contain some paragraph starts (this inflates RF1b line-initial gallows from 8.6% to 16.7%; see caveats).

## H2: the line is a functional unit

### H2a  Which glyphs/endings sit at line start / end (ZL3b continuation lines, N=27,286 words; RF1b in brackets)
| position | feature | rate at pos | rate mid | ratio | z vs shuffle |
|---|---|---|---|---|---|
| line-final | last glyph m | 15.3% [14.9%] | 1.0% [0.8%] | 15.8x [17.7x] | +51 [+49] |
| line-final | last glyph g | 2.3% [2.3%] | 0.08% | 30x [24x] | +20 [+22] |
| line-final | last glyph r / l / o | 8.4 / 11.2 / 1.2% | 14.8 / 17.1 / 3.2% | 0.57 / 0.65 / 0.38 | -11 / -8 / -8 |
| line-final | ending -am | 12.0% | 0.66% | 18x | +42 |
| line-final | endings -ry, -om, -ly | 2.8, 2.4, 3.4% | 0.16, 0.22, 0.64% | 17x, 11x, 5x | +16..+20 |
| line-final | endings -ey, -ol (depleted) | 3.9, 4.5% | 12.3, 10.4% | 0.31, 0.43 | -15, -11 |
| line-start | first glyph y | 17.5% [14.5%] | 3.4% | 5.2x [4.8x] | +33 [+32] |
| line-start | first glyph d | 18.4% [15.0%] | 7.3% | 2.5x | +19 [+16] |
| line-start | first glyph t / p | 6.7 / 1.3% | 1.9 / 0.2% | 3.5x / 7.2x | +18 / +12 |
| line-start | first glyph c (depleted) | 4.4% [5.5%] | 22.9% | 0.19x | -23 [-25] |
| line-start | first glyph a, k | 0.4, 0.8% | 5.5, 3.8% | 0.08, 0.21 | -15, -9 |
| line-start | last glyph m (depleted) | 0.3% | 1.0% | 0.34 | -9 |

Whole words at line start: dshedy, sol, saiin, sor, sain, sar, daiin (x2.4..x14, z 9-13). At line end: am, dam, oly, otam, okam (x11..x34, z 9-16); chol (x0.06) and qokeedy (x0.14) are strongly avoided. All entries above have permutation p <= 0.0033 (the floor).

Gradient (lines with n>=10 words, ZL3b; baseline = positions 5..n-4): the effect is confined to the single outermost word.
| feature | baseline | pos 1 | 2 | 3 | 4 | (from start/end) |
|---|---|---|---|---|---|---|
| final -m, counting from line end | 0.5% | 22.8% | 1.9% | 0.8% | 1.3% | rest ~baseline |
| final -g, from end | 0.0% | 2.2% | 0.1% | 0 | 0.2% | |
| initial gallows, from start | 5.6% | 10.0% | 4.9% | 6.2% | 5.6% | |
| initial y, from start | 3.4% | 18.2% | 3.0% | 3.3% | 3.3% | |
| initial d, from start | 6.1% | 20.9% | 3.3% | 5.4% | 5.9% | |
| initial c, from start | 20.4% | 2.9% | 21.4% | 20.5% | 20.3% | |
No gradient: the second-to-last word has only 1.9% -m (RF1b 1.2%). It is a first-word / last-word property.

Strata (ZL3b; rate at position / mid-rate / ratio; every cell z >= +4 unless noted). RF1b gives the same pattern in every stratum.
| stratum | n lines | final -m | final -g | initial y | initial d | initial c |
|---|---|---|---|---|---|---|
| all | 3310 | 15.3/1.0 x15.8 | 2.3/0.1 x30 | 17.5/3.4 x5.2 | 18.4/7.3 x2.5 | 4.4/22.9 x0.2 |
| Currier A | 1281 | 11.7/1.8 x6.4 | 3.4/0.1 x26 | 17.4/4.4 x4.0 | 17.6/12.6 x1.4 | 6.1/31.9 x0.2 |
| Currier B | 1971 | 17.4/0.6 x31 | 1.6/0.0 x32 | 17.4/2.9 x6.1 | 18.6/4.9 x3.8 | 3.4/18.8 x0.2 |
| hand 1 | 1208 | 10.8 x6.6 | 3.4 x28 | 17.2 x4.1 | 17.7 x1.4 | 6.5 x0.2 |
| hand 2 | 1044 | 14.0 x28 | 1.4 x25 | 13.9 x4.2 | 16.4 x2.5 | 2.8 x0.2 |
| hand 3 | 888 | 22.7 x25 | 1.6 x27 | 21.5 x8.8 | 20.0 x6.5 | 3.5 x0.2 |
| sect. Herbal | 1321 | 12.7 x8.0 | 3.7 x39 | 17.6 x3.6 | 17.0 x1.5 | 5.7 x0.2 |
| sect. Stars/recipes | 868 | 22.4 x24 | 1.6 x27 | 22.0 x9.6 | 20.5 x6.6 | 4.0 x0.2 |
| sect. Balneo | 640 | 8.0 x330 (z 7) | 0.5 (n.s.) | 9.2 x6 (z 3) | 15.0 x2 (n.s.) | 3.3 x0.2 |
| sect. Pharma / Cosmo / Text | 178/82/192 | 17/27/19 x12..27 | n.s. | 22/24/17 | 26/23/21 | 3.4/1.2/3.6 |
Replicates in every stratum for the m, y and c effects; the magnitude is variable (m: 8% Balneo to 27% Cosmological; Currier A 11.7% vs B 17.4%; hand 3 22.7%). Hand 4 (60 lines), Balneo -g and Balneo y/d are not significant (small n / weak).

### H2b  Truncated, padded, or variant-ending? (ZL3b [RF1b])
| test | result |
|---|---|
| mean word length start / end / mid | 5.24 / 4.84 / 4.98 [5.40 / 4.90 / 5.02]; shuffle null 5.00 +- 0.03 (so first words +0.24 longer, last words -0.14 shorter, both z>4) |
| final -m word vs other final | 4.58 vs 4.88 chars; mid-line -m words are 4.63 (final-m words are NOT shorter than mid-line -m words) |
| corr(chars before last word, last-word length) | -0.182 (null sd 0.017, z -10) [-0.207, z -12.5]: last word is shorter on longer lines |
| final -m rate by line fill (prefix length tercile) | short 10.4% / mid 15.0% / long 25.2% [10.1 / 12.7 / 21.2]. Rate rises 2.4x with line fill |
| final -m in paragraph-last line (ZL only) | 9.2% vs 13.7-18.3% in other lines |
| exact type of final-m token also occurs mid-line | 56% [51%] of tokens (208 types); 67% of mid-line -m types also occur line-final |
| tokens (mid-line, any position) sharing the stem of a final-m word | endings -l 2426, -r 2204, -n 1176, -s 318, -y 288, -o 126, versus -m only 134 (about 2%, versus 15% at line end) |
| stem+X attested anywhere (208 final-m stems) | +r 55%, +l 52%, +iin 46%, +in 35%, +n 18%, +y 12%, +g 11% |

Reading: the stems of line-final -m words are ordinary mid-line words, where they carry -l/-r/-n/-iin. So -m is a line-position-conditioned ending (allograph/variant) of the same stems, not a separate lexical class. The shortening is modest (about 0.3 char) and not a truncation signature (final-m words are no shorter than mid-line -m words); the fill-dependence (r = -0.18; -m rate 10% to 25% with line length) is weak-to-moderate evidence that -m behaves as an end-of-line/space-fitting marker. It does not behave like a general "last word is cut" rule, since 85% of line-final words do not end in -m. Also note -m is depleted (not enriched) at the paragraph-final line end, and -g/-m share the slot.

### H2c  First line vs every line; paragraph text vs labels / circular / radial (ZL3b)
| line class | n lines (>=2 w) | first-word gallows | y | d | c | last-word -m | last-word -g |
|---|---|---|---|---|---|---|---|
| paragraph line 1 | 740 | 82.7% | 1.8% | 2.0% | 1.1% | 16.2% | 1.6% |
| paragraph line 2 | 750 | 6.1% | 19.9% | 25.6% | 3.5% | 16.3% | 3.2% |
| line 3 | 668 | 9.7% | 16.8% | 18.0% | 4.2% | 18.3% | 2.1% |
| line 4 / 5 / 6+ | 495/348/1067 | 9.5/9.2/9.6% | 18/18/16% | 17/15/16% | 4.6-4.9% | 13.5/14.4/13.7% | 1.5-2.9% |
| paragraph last line | 728 | 8.0% | 21.7% | 18.1% | 4.8% | 9.2% | 1.0% |
| label (type L) | 130 | 0.8% | 11.5% | 8.5% | 8.5% | 10.8% | 1.5% |
| circular text (C) | 83 | 3.6% | 2.4% | 7.2% | 3.6% | 9.6% | 0% |
| radial (R) | 97 | 6.2% | 16.5% | 14.4% | 6.2% | 9.3% | 2.1% |
| single-word labels (n=867) | | 3.5% | 7.7% | | | 5.7% (m) | 1.4% (g) |
- The line-start y/d/s/t slot applies to every continuation line (lines 2..n, steady 16-20% y, 15-26% d), not only to line 1. In paragraph line 1 that slot is instead filled by a gallows (83%) and y/d vanish (about 2%), i.e. the paragraph start occupies the same line-start slot with a different class.
- The line-final -m/-g effect is identical for line 1 and later lines (16% vs 14-18%) and weaker in last lines of a paragraph (9%).
- Labels / radial / circular text: end-m about 9-11% (about 9x the paragraph mid-line rate; single-word labels 5.7%) so the end effect also exists outside paragraphs. The start effect (y/d, gallows) is weak or absent in circular text (y 2.4%), partial in labels and radial text. Counts small (83-130 lines) and many "lines" of labels are 1-2 words, so the two ends are not independent there.
- RF1b: same picture (line-final m 8.2%..20%, line 2 y/d 14/27%).

## H3: paragraph-initial gallows

### Magnitude and replication (permutation: shuffle words within folio across P-lines)
| | ZL3b | RF1b (only `@P`, n=263) |
|---|---|---|
| gallows-initial: paragraph-first word | 82.7% (n=740) | 70.7% |
| later line-initial / mid-line / line-final | 8.6% / 6.5% / 5.3% | 16.7% (contaminated) / 5.8% / 4.6% |
| null for paragraph-first slots | 8.0% +- 1.0% (z = +79, p < 0.001) | 7.8% +- 1.7% (z +38) |
Strata (paragraph-first gallows rate; ZL3b): Currier A 81.6, B 86.0; hand 1 81.1, 2 83.2, 3 88.1, 4 only 34.5 (n=29); sections: Herbal 87.0, Stars 88.0, Balneo 76.7, Pharma 68.2, Cosmo 60.9, Text 83.9, Astro 23.5 (n=17). Page-first paragraph (`@P`) 77.7% vs later paragraphs on a page 85.4%. RF1b: A 78.2, B 71.8; hand 1 78.6, 2 70.3, 3 74.2; Herbal 81.7, Stars 80.0, Balneo 60.0, Pharma 61.1, Cosmo 59.1, Astro 22.2. So the effect replicates in the large strata and in RF1b, but is clearly weaker in Cosmological/Pharma/Balneo, and almost absent in hand 4 and Astronomical (small n; these may be labels/circular text mislabelled as paragraphs, a transcription-class caveat).

### H3a  Scope: first glyph, first word, or whole first line?
| word position (lines with n >= 8) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| gallows-initial, paragraph line 1 | 86.0% | 6.5 | 9.3 | 6.7 | 11.8 | 7.4 | 7.3 | 7.8 |
| paragraph line 2 | 6.2 | 5.2 | 4.8 | 6.0 | 5.0 | 6.4 | 4.7 | 6.2 |
| paragraph line 3+ | 11.1 | 4.9 | 5.8 | 5.4 | 4.7 | 4.8 | 6.2 | 4.6 |
- Word-initial gallows is a first-word effect: word 2 is back at 6.5% (baseline 5-6%). The first word is also almost never "gallows as 2nd glyph" (4.9% vs 20.8% mid-line): the gallows is the first glyph, rather than being preceded by o/y.
- Small residual spill-over into the rest of line 1: any-gallows-in-word 59.4% vs 49-50% in later lines; gallows letters per char 0.115 vs 0.101-0.103; within-folio shuffle null 50.9% +- 0.6%, z = +15 (ZL3b); RF1b 55.9% vs null 51.7%, z = +3.6. About +10 points; an order of magnitude weaker than the first word. The non-gallows paragraph-first words (128) also contain more gallows later in the word (59% vs 49%).
- Second word of the first line has normal y/d rate (7.6% vs 8.4%): no whole-line change in the start slot.

### H3b  Gallows stripping
Reference types = all P-line words except the paragraph-first ones (ZL3b). Matching = remainder (non-empty) exists in the reference (>=1 token) or is common (>=5).
| set | match >= 1 | match >= 5 | mean log10(1+freq) |
|---|---|---|---|
| paragraph-first gallows words, gallows stripped (n=612) | 70.4% | 55.7% | 1.05 |
| null A: length-matched random word, first glyph stripped | 68.1 +- 1.6 | 54.1 +- 1.8 | 1.02 |
| null B: length-matched non-paragraph gallows word, gallows stripped | 67.6 +- 1.8 | 52.3 +- 2.0 | 1.08 |
| null C: length-matched random word, random glyph stripped | 57.1 +- 1.9 | 40.2 +- 1.8 | 0.73 |
| (unstripped paragraph-first words) | 43.5 | 21.8 | |
| RF1b stripped (n=186) / null A / null B | 60.8 / 65.0+-3.1 / 63.8+-3.3 | 43.0 / 49.6 / 48.9 | |
Split k,t vs p,f: 70.7 / 70.2 (no difference). Most frequent remainders: ol, chedy, chor, chol, chedar, cheol, shol, shedy. Remainder first glyph: ch 35%, o 34%, sh 15%, a 6%, e 3%, d 3%, y 3%, **q 0%** (versus q 17%, d 7%, y 3.4% in a normal word-initial slot).
Reading: stripping makes 70% of paragraph-first words into attested, mostly common types, which is more than the unstripped words (44%), but it is no better than stripping the first glyph of any random word (68%, +1.4 sd) or a gallows from any other gallows-initial word (68%, +1.6 sd). In RF1b the stripped rate is even below the nulls. So the test is non-discriminating: Voynich words are compositional enough that prefix removal always yields frequent types. The only structured signal is that the remainder is never q-, and rarely d-/y-: the gallows occupies the slot that q/d/y occupy elsewhere, plus a small ch/sh/o stem set. The `Pch -> ch` and `Po -> o` readings (remainder ch 35%, sh 15%, o 34%) are the dominant stems.

### H3c  Which gallows (share of gallows-initial words)
| position | k | t | p | f | bench forms (cXh) |
|---|---|---|---|---|---|
| paragraph-first (ZL3b) | 13% | 28% | 54% | 5% | rare (<1% of words) |
| paragraph-first (RF1b) | 19% | 27% | 45% | 8% | |
| later line-initial (ZL3b) | 9% | 75% | 15% | 1% | |
| mid-line (ZL3b) | 58% | 30% | 8% | 4% | cth+ckh+cph ~2.4% of words |
Chi-square (k/t/p/f mix, paragraph-first vs rest) = 543 vs shuffle null 2.9 +- 2.4 (ZL3b), 90 vs 3.2 (RF1b), p<0.001. Paragraph starts are p/t-dominated, and k, which is the commonest gallows mid-line, is rare there (the contrast is p 54% vs 8%). In B p is 62% of paragraph starts (A 39%); Herbal p 43%, Stars/recipes 61%, Balneo 71%, Text 85%, Cosmo t 71% (n=23). Line-initial gallows in continuation lines are t (75%).

## Verdicts
**H2: SUPPORTED (strong).** Line-final -m 15.3% vs 1.0% mid (z +51), -g x30, y-/d-/t-/p- at line start, c- avoided at line start (x0.19), all absent in a within-folio shuffle (z 9 to 51) and replicated in RF1b and in every stratum with adequate n (Currier A/B, hands 1-3, sections Herbal/Stars/Cosmo/Pharma/Text). The effect is positional: confined to the first and last word of each line (no gradient), present on every continuation line (not only line 1) and only partially in circular text/labels. The final-m words are ordinary stems with a line-end ending (stems otherwise carry -l/-r/-n), the rate rises with line length and is depleted on the paragraph's last line. This rules out "continuous prose merely wrapped at the margin": at least the first and last word of a line are produced or written under line awareness. Consistent with a scribal convention (line-end ending/space-fitting, or margin-driven choices, possibly modulated by hand) or with a generator that treats line boundaries as states (reset/start and stop tokens). What it does not show is which of these is the case: weak fill-dependence (r = -0.18) hints at a copying/fitting factor but cannot exclude generator-side line states; magnitude varies 2-4x with hand, language A/B and section, so it is not one universal rule.

**H3: SUPPORTED as a position-conditioned (layout/marking) phenomenon; "not a sound value" NOT established.** 82.7% of paragraph-first words are gallows-initial vs 8.0 +- 1.0% under shuffle (z +79; 71% in RF1b), replicated in the strata with n > 40 (A/B, hands 1-3, Herbal/Stars/Balneo/Text), weaker in Cosmo/Pharma, and not seen in hand 4/Astronomical (n small). The effect is first-word-only (word 2 at 6.5%), with a weak residual elevation of gallows density over the rest of line 1 (+10 points, z +15 ZL / +3.6 RF). The paragraph-first letter mix differs radically from mid-line (p 54% vs 8%; k 13% vs 58%), so the same glyph set is not sampled from the same distribution; this favours "a position-bound start class (like the y/d class at line starts) over lexical gallows". But the stripping test is non-discriminating (70% match vs 68% for random first-glyph removal), so it can neither confirm a removable decorative prefix nor a lexically meaningful letter. Constraint on any generator or reading: the paragraph start must be modeled as a distinct start state (gallows-p/t + o/ch/sh stem; never q), and cannot be read as an ordinary word-initial letter drawn from the global distribution.

## Caveats
- Single transcription family: ZL3b and RF1b are both derived from the same underlying readings; replication shows robustness to the transcriber's conventions, not independence from the manuscript.
- Line breaks in the transcription follow the physical line, but lines interrupted by drawings (`<->` intrusions are removed in the parser) and words broken at line ends are not specially handled. Those could produce some -m/-g or lexical boundary signals; unlikely to explain a 15-30x effect. The `-m` and `-g` glyphs also reflect transcription decisions (e.g. the ligature m vs in/iin) that I did not re-check against images.
- RF1b has no `<%>`, so only `@P` lines count as paragraph-first (n=263); all "later line-initial" RF1b figures include some unlabeled paragraph starts, and the first-line RF1b numbers (gallows 70.7%) are a lower bound for the true figure.
- Paragraph/strata counts: Hand 4, Astronomical, Cosmological and Pharma strata have 17-60 paragraphs; treat percentages there as indicative only. Strata overlap strongly (hand 1 = mostly Herbal A; hand 3 = mostly B), so they are not independent replications.
- Permutation nulls preserve folio vocabulary and line lengths but not paragraph structure; permutation p values saturate at 1/(B+1), so z-scores are used. Whole-word tables were screened at a fixed frequency (>=25) and not corrected for multiple comparisons; the glyph-level effects are large enough (z > 10) to survive any such correction.
- The "paragraph" construct (`<%>`/`<$>`) is an editorial decision of the transcription; in non-herbal sections it may cover labels/circular text and dilute the gallows rate.
