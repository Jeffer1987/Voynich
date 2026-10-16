# 13 Generators G1-G4 vs the K1 fingerprint (wave 6)

Script: `swarm/scripts/gen_models.py` (python -I; args parsed_zl3b.json baselines_dir out.json; ~3 min). It exec's the unmodified heads of `k1_sim.py` and `k1_positional.py` (fingerprint, `dist`, `t1/t2/ab_metrics`, `Enc`, Voynich data). Raw output: scratchpad `gen.txt/gen.json`.
All models: 35,000 words, laid out in lines/paragraphs by resampling Voynich paragraph structures (same layout seed). Fingerprint at EVA-character level (as `VMS_FP`); layout/positional metrics at EVA-glyph level. d10 = the K1 distance (10 features, same tolerances). d13 = d10 plus 3 layout features (Jaccard ratio, identical-neighbour ratio, edit-1-neighbour ratio; tolerances .5/.3/.3). "Core pass" = h2 +-.3, wl +-.75, hapax +-.07, TTR +-.07.

## Models and free parameters
- **G1 self-citation** (Timm & Schinner style): 10 random seed words (glyphs drawn by Voynich glyph frequency, Voynich length distribution). Each word: with prob pnew a new seed word, else copy a uniformly chosen word from the last W words, and with prob pm apply one edit (sub .5 / ins .25 / del .25) inside a 7-class glyph system (gallows, ch/sh, a/o/e/y, i, d/l/r/s/n/m, q). **5 parameters** (pnew, pm, W, 2 op weights) plus glyph frequencies, length distribution and classes taken from Voynich (~25 numbers, partly circular). Grid 18 configs.
- **G2 table + grille** (Rugg): 3 columns (prefix = pre+gallows+ch, midfix = e+core, suffix = ending), R rows each, filled by i.i.d. draws from the Voynich slot frequencies; the grille moves by fixed row steps per word and jumps randomly with prob pj. **6 parameters** (R, 3 steps, pj, seed) **plus table content (3R entries from fitted slot frequencies, circular)**. Grid 24 configs.
- **G3 slot sampler**: word = pre(9 values) + gallows(9) + ch/sh(3) + e-run(4) + core(231, freq>=5) + ending(27), regex-parsed from Voynich (100% coverage), slots independent, words i.i.d. **283 fitted probabilities** (strongly circular). **G3j**: two joint blocks (pre-gal-ch, e-core-end) = 2160 fitted entries, close to a lookup of Voynich's own word structure.
- **G4 = G3 + local copy**: with prob pc copy a word from the last W words (+1 edit with prob pm), else draw from G3 (G4j: from G3j). G4: 286 params; G4j: ~2160+3.

## Voynich reference (same code)
h2 2.17, wl 5.07, alphabet 18, TTR .23, hapax .713, Zipf -1.02, h2 within/cross 2.13/3.02. Layout (P-text, 34k words): consecutive-line Jaccard .0319 vs shuffle .0132 (ratio 2.4); identical neighbours 1.19x and edit-1 neighbours 1.29x a within-paragraph shuffle (my null is stricter than the folio null in note 03, hence lower than 1.4/1.5). T1 top-glyph shift (final minus mid) = +.143 (m: 15.3% vs 1.0%); T2 top-4 initial glyphs 82% of paragraph-first words vs 25% elsewhere; T3: 2 suffixes with |d|>2.4 (A vs B), 0 prefixes.

## Results (best config per family; G1/G2/G4/G4j = best of grid by d13, re-run on 3 seeds; G3/G3j 3 seeds)
| model | free par | d10 | d13 | h2 | wl | TTR | hapax | Zipf | h2 within/cross | Jaccard ratio | ident / ed1 nb | core pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Voynich | - | 0 | 0 | 2.17 | 5.07 | .23 | .71 | -1.02 | 2.13/3.02 | 2.4 | 1.19 / 1.29 | - |
| K1 E3 (note 10; re-evaluated here) | ~6-7 | 1.21 | 1.72 | 2.10 | 6.09 | .17 | .60 | -1.04 | 1.85/2.75 | 1.1 | .06 / .76 | no |
| K1 E7 / K1+M1a+M1b (notes 10, 12) | 7 / ~13 | 1.07 / 1.01 | - | 2.44 | 4.87 | .16 | .60 | | | | | no |
| **G1** self-citation | 5 (+25 circ.) | 3.72 | 3.91 | 3.35 | 7.17 | .44 | .64 | -.66 | 3.17/3.78 | 6.1 | .9 / 1.0 | no |
| **G2** table+grille | 6 (+table) | 1.46 | 1.58 | 2.29 | 4.87 | .23 | .56 | -.85 | 2.35/3.07 | 0.95 | .95 / .93 | no (hapax) |
| **G3** slot iid | 283 | 1.42 | 1.51 | 2.45 | 4.83 | .34 | .73 | -.84 | 2.53/3.33 | 1.0 | 1.06 / 1.02 | no (TTR, h2) |
| **G3j** joint slots | 2160 | **.85** | 1.14 | 2.28 | 4.88 | .24 | .65 | -.93 | 2.30/3.19 | 1.0 | 1.07 / 1.01 | yes |
| **G4** G3 + copy (pc .3, pm 1, W 40) | 286 | 1.99 | 1.78 | 2.66 | 4.83 | .40 | .74 | -.81 | 2.71/3.41 | 2.6 | 1.0 / 1.0 | no |
| **G4j** G3j + copy (pc .15, pm 1, W 25) | ~2160 | **.95** | **.96** | 2.39 | 4.85 | .28 | .68 | -.92 | 2.41/3.24 | 1.6 | 1.18 / 1.09 | yes |

Within the G4j grid, pc .3 / W 12 gives Jaccard .037/.006 (ratio 6), identical 1.7x, ed1 1.4x (overshoot) while d10 stays 1.2; pc .15 / W 25 hits ident/ed1 (1.2/1.1) but Jaccard only 1.6x. So neighbour structure is tunable by the copy window, but Jaccard and the neighbour ratios did not match simultaneously.

## Positional signatures (emerge without extra rules?)
- **T1 (line-final -am)**: no. Top-glyph shift (final minus mid) <= .02 in every model (Voynich .143); no stem-pair signature. K1 also needed an explicit glyph-level rule (note 12).
- **T2 (paragraph-initial p-gallows)**: no. Top-4 first glyphs 55-66% of paragraph-first words vs 55-66% elsewhere (Voynich 82% vs 25%). Needs an explicit marker rule, as in K1.
- **T3 (A/B)**: no. With random page labels or first-half vs second-half of the stream: 0 suffixes and 0 prefixes with |d|>2.4 in all models (Voynich 2/0). The generators have no topic or drift layer. A/B as two settings (two tables/grilles for G2, two slot distributions for G3) is a natural extra layer but was **not tested here**; it would cost another set of probabilities.
Conclusion: the three positional signatures are no cheaper under generators than under K1.

## What each family explains per parameter
- **Slot family (G3j, G4j)** reaches d10 .85-.95 and passes the core test, which no K1 config did. Slot-iid (283 params) already gives hapax .73 and right wl/alphabet, but TTR .34 (too many types) and h2 2.45: the independent product space is too uniform. Joint blocks fix this at the price of 2160 fitted entries. This is **largely circular**: the model is estimated from the text it is scored on, so a good d10 says "word-internal structure plus frequencies carry the fingerprint", not that a mechanism was found. The low-parameter, useful content is the slot decomposition itself (6 slots with small inventories plus a long tail of cores), i.e. a descriptive grammar of Voynich words.
- **Non-circular generators** (G1 with 5 parameters, G2 with 6 + table) do worse than K1: G1 fails h2 (3.3-3.6; random seeds plus class edits randomise too much) and wl; G2 with R<=60 fails hapax badly (.10-.30), R=250 reaches .56 (with fitted table content).
- **Local copy** (G1/G4) is the only mechanism that reproduces above-chance Jaccard and near-identical neighbours (ident 1.7x, ed1 1.4x at W=12) without hurting wl/hapax; K1 and the i.i.d. models give ratios ~1 or below. Cost: 2-3 parameters. Pure G1 cannot supply the low h2, so copying is an add-on to a slot grammar, not a standalone generator.
- **K1 vs generators**: K1 explains h2/wl/within-cross gap with 2-3 parameters but misses hapax (.60 vs .71), TTR, neighbour structure and Jaccard. Slot generators match hapax/TTR/neighbours only after fitting hundreds to thousands of numbers from the target. K1 is cheaper for h2+wl; G4j covers more features but at 2-3 orders of magnitude more fitted values.

## Overfitting / limits
Selection on d13 over small grids (18-24 configs, 1 seed) with a 3-seed re-run; seed spread of d10 is ~.02-.05. G2/G3/G4 use Voynich-estimated frequencies; ZL3b transcription and the regex slot parse are the only Voynich inputs. Zipf slope is matched by no generator (-.84 to -.93 vs -1.02; head too flat). K1 numbers are earlier single-codebook runs (no variance over codebooks). Neighbour ratios use my within-paragraph shuffle null (Voynich 1.19/1.29), not the folio null of note 03.

## Verdict
Slot structure + local copy (G4j) reproduces the distributional fingerprint (d10 .95, core test passed, hapax .68, identical/ed1 neighbours right) better than any K1 configuration (d10 >= 1.01, core never passed), but only because its parameters are fitted from Voynich itself. The non-circular generators (G1, G2) are worse than K1. So neither family wins in a parameter-fair way: K1 wins on parsimony for h2+wl, the slot+copy family wins on hapax/TTR/neighbours. This supports the wave-5 hint that word forms are composed internally (slot or combinatorial system) plus local copying, but it does not prove a generator.

**Not reproduced by any model**: T1 (line-final -am), T2 (paragraph-initial p-gallows), T3 (A/B suffix settings and the section/hand layer); Zipf slope -1.02 together with hapax .71 (generators too flat, K1 too few hapaxes); Jaccard 2.4x and identical/ed1 at the right size simultaneously with low h2 (G1 has Jaccard but loses h2; G4j loses Jaccard when ident/ed1 are right); all line- and paragraph-position effects, which need explicit rules in both families.
