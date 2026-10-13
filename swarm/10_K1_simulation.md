# 10 K1 simulation: verbose cipher / syllabary + abbreviation vs Voynich fingerprint

Script: `swarm/scripts/k1_sim.py` (python -I; args: parsed_zl3b.json, baselines dir, out json [quick]). Raw: scratchpad `k1_full.json/.txt`. Runtime ~8 min.
Plaintext: first 35,000 tokens of Latin (Caesar, PG218+PG18837) and Italian (Dante, PG1000); classical/literary, not medieval abbreviation-heavy text (limitation). All fingerprints on 35k tokens, plug-in entropy; h2 counts space as a symbol.

## Voynich fingerprint (ZL3b, a-z words, 35k tokens)
h2 2.17 | h2 within word 2.13 | h2 across word boundary 3.02 | mean wl 5.07 | alphabet (freq>=0.1%) 18 | TTR 0.23 | hapax/type 0.71 | h1 3.86 | Zipf slope -1.02 | monotone-slot fraction 0.30.
Plain Latin: h2 3.30, wl 6.07, TTR 0.24, hapax 0.59. Plain Italian: h2 3.11, wl 3.93, TTR 0.19, hapax 0.61.
Distance = RMS of z-scores over 10 features (tolerances ad hoc: h2 .2, wl .5, TTR .04, hapax .05, ...). "Core pass" = h2 within .3, wl within .75, hapax within .07, TTR within .07 simultaneously.

## Encodings and grids (configs tested, per language)
- E1 verbose cipher (letter -> 2 glyphs, random or class-structured grids 5x5..11x11): 42
- E2 syllabary (syllable -> 1-2 glyphs, 8-22 base glyphs, top-K 1-glyph): 32
- E3 abbreviation (vowel drop pv 0-1, truncation L 3-6, suspension endings, short-word table) then verbose: 288-432
- E4 abbreviation then syllabary: 192
- E5 homophonic verbose with digram units: 27
- E6 abjad (consonant skeleton + vowel marks): 12
- E7 hybrid (abbreviation then 1-glyph for top-m symbols, 2-glyph rest): 450

## Results
Core pass: **0 of ~1,500 configs per language** (Latin and Italian). Best (lowest-distance) config per family:

| family | best lang | dist | h2 | wl | hapax | TTR | fails |
|---|---|---|---|---|---|---|---|
| plain Italian (ref) | - | 2.46 | 3.11 | 3.93 | .61 | .19 | h2 |
| E1 verbose 11x11 | It | 2.10 | 1.95-2.0 | 7.86 | .61 | .19 | wl (2x), hapax, slot |
| E2 syllabary | It | 2.78 | 2.9 | 3.3 | .57 | .14 | h2, wl, alpha(8) |
| E3 abbr+verbose (pv .5, short words, 11x11) | It | **1.21** | 2.10 | 6.09 | .60 | .17 | wl (+1), hapax (-.11), h2_cross |
| E4 abbr+syllabary | It | 2.95 | 3.2 | 3.6 | .59 | .17 | h2 never below 2.8 |
| E5 homophonic digram-verbose | It | 1.28 | 2.49 | 6.19 | .61 | .19 | h2 (+.3), wl, hapax |
| E6 abjad | It | 2.03 | 2.4-2.9 | 3.3-3.9 | .55-.6 | .13-.17 | h2, wl |
| E7 hybrid (pv .6, G=18, m=4) | It | **1.07** | 2.44 | 4.87 | .60 | .16 | h2 (+.27), hapax (-.11), within/cross |

Latin best overall 1.73 (E7), because Latin words are long (wl 6) so doubling or abbreviation overshoots less cleanly and hapax stays 0.52-0.59.

## Which constraints each family fails
- **Hapax fraction 0.71** is failed by every config in both languages (max ~0.61, i.e. the plaintext value; encodings are deterministic per word type so cannot raise it; abbreviation merges types and lowers it). It is the most robust miss. Plain 35k-token natural text has hapax 0.59-0.61. A cipher that is one-to-one on word types cannot reach 0.71; Voynich needs either more distinct types (morphological/positional variation, nulls, homophony per occurrence) or non-linguistic generation. Note E5/homophones (random choice per occurrence) did not help here because only 6-60 extra codes were used at letter level and tokens differ only if the homophone differs; a stronger homophone scheme would inflate hapax but also h2.
- **Syllabaries (E2, E4)** keep h2 near 3 (2.8-3.4): syllable-to-glyph mapping preserves the transition information; they cannot reach 2.2 with an alphabet of 8-22 glyphs.
- **Verbose (E1/E3)** reproduce low h2 (about 2.0-2.1) and the large within-word / across-boundary gap (1.7-1.9 vs 2.8-3.2; Voynich 2.13 vs 3.02), a genuine hit for the verbose idea: bigrams inside a 2-glyph unit are fully determined. But E1 doubles word length (7.9 Italian, 12 Latin). Only with strong abbreviation (E3/E7) does wl come down to 5-6 without losing the low h2. In E7, h2 rises to 2.4-2.8 when single-glyph codes are added.
- **Abjad (E6)** lowers wl but h2 stays 2.4-3.1; fails.
- **Slot structure** (monotone glyph position, 0.30 in Voynich): reached incidentally (0.2-0.46) by several configs, so it does not discriminate.

## Overfitting / parameters
The best E3 config uses ~6 free choices (language, pv, truncation, ends, short-word table, grid shape, seed) and the best E7 uses ~7, tuned to 4 targets (h2, wl, TTR, alpha). Even so, hapax and h2 or wl stay out of tolerance. Matching h2+wl+TTR is therefore cheap (a 2-3 parameter combination of heavy abbreviation and 2-glyph letter codes); the extra constraints (hapax, h2_cross gap shape, slot structure) are what the model fails. Italian beats Latin only because its plain word length (3.9) happens to leave room for the doubling; this is a baseline choice, not evidence for the cipher.

## Verdict: K1 partially viable (under simple models, not accepted)
- Refuted as stated for syllabary and abjad variants (cannot reach h2 2.2 with correct wl).
- Verbose cipher + abbreviation (E3/E7, Italian-like source) reproduces h2, wl, TTR, alphabet size and the within/cross-boundary entropy gap together, but **none** also reproduces hapax 0.71, so no config passes the core test. The fit is a near miss tuned with several parameters, i.e. weak support.
- Caveats: baselines are classical literary text (no scribal abbreviation habits, no medieval vocabulary); tolerances are ad hoc; hapax may depend on token-count and text type (herbal/recipe vocabulary with many rare names would raise hapax), so the hapax miss is partly a baseline problem and should be rechecked on a medieval herbal/pharmacopoeia Latin text.

## What a viable K1 model must additionally reproduce (not tested here)
1. Line-final -ar/-al -> -am allograph (a position-dependent substitution; needs an explicit line-end rule in the encoder).
2. Paragraph-initial p-gallows excess (a null/ornament or distinct initial-letter code at paragraph start).
3. Currier A/B as two settings (e.g. two code tables or abbreviation habits; the encoder must make A and B differ in h2/wl/hapax with the same plaintext source; see wave 4B for how much is section/hand).
4. Hapax 0.71 and Zipf slope -1.02, with the same equal-token sample.
5. Positional glyph slot grammar with a far lower variance than random verbose grids give.
