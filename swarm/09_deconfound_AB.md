# 09 Deconfounding Currier A/B, Davis hand, section

Script: `swarm/scripts/deconfound_ab.py <parsed_zl3b.json> 80` (python -I; seeded). Unit = page; paragraph lines only (type P); pages with >=80 tokens (131 of 227, 4130 P-lines parsed). Features on raw EVA words: h2 (page-level conditional char entropy incl. word boundary), mean word length, word-initial qo/ch/sh, word-final edy/aiin/ol/dy, line-final -m, paragraph-initial gallows (ktpf), type/token ratio. Permutation = shuffle labels across pages within the compared cell, 5000x. Page-level h2 is biased by page size; only compare it across similar-size groups, and treat it as weak evidence.

## 1. Design limits (cross-tab, all 227 pages)
Hand 1 = Currier A for every labelled page (112 A, 0 B). Hands 2, 3, 5 = B (except 2 hand-3 stars pages = A). Hand 4 = unlabelled. So **language and hand are nearly collinear**; they can be separated in only one cell (hand 3, stars: A n=2 vs B n=22). Cells where one factor is truly fixed:
- section fixed (herbal): hand1/A (37) vs hand2/B (18); also within B: hand2 (18) vs hand3 (3) vs hand5 (5)
- hand+language fixed: hand2/B herbal (18) vs bio (19); hand1/A herbal (37) vs pharma (15)
- language fixed, section and hand vary: B bio(h2) vs stars(h3)

## 2. Feature results (d = standardised difference, p = permutation)
| contrast | what moves (p<0.01) | what does not |
|---|---|---|
| herbal, A/hand1 vs B/hand2 | **edy 0.001 vs 0.128 (d -2.7)**, **dy 0.047 vs 0.248 (d -3.2)**, **ol 0.151 vs 0.043 (d +2.4)**, final-m 0.108 vs 0.210 (p .004) | h2 (1.87 vs 1.90, p .27), word length (4.93 vs 4.94), qo, aiin, par-gallows (p .075) |
| hand2/B, herbal vs bio (section only) | qo .088 vs .245, edy .13 vs .27, ol .04 vs .12, aiin, final-m .21 vs .08, **h2 1.90 vs 1.71**, TTR .80 vs .55, par-gallows | wlen |
| hand1/A, herbal vs pharma (section only) | qo .079 vs .130, dy .047 vs .095, ol, TTR | h2, wlen, final-m, edy (stays ~0.00) |
| herbal, B fixed, hand2 vs hand5 (n 18/5) | wlen 4.94 vs 5.56 (p .002), TTR, aiin (p .012) | edy, ol, qo, h2 |
| herbal, B fixed, hand2 vs hand3 (n 18/3) | wlen, qo, TTR at p .02-.04, n=3 | everything else |
| hand3 stars, A (n=2) vs B (22) | edy .008 vs .144, dy .059 vs .197 (p .004/.003) | rest (n too small) |
| B fixed: bio/h2 vs stars/h3 | nearly everything (h2 1.71 vs 1.90 d -2.4; final-m .075 vs .234 d -2.7) | - |

Reading: (i) edy/dy/ol is the A/B signature and it survives holding section fixed and, in the n=2 cell, holding hand fixed (the two hand-3 A pages look like hand-1 A: edy ~0). (ii) h2 and mean word length do **not** separate A from B once section is fixed; the h2 differences seen globally are section effects (bio is low-h2, TTR .55). (iii) Section effects are as large as the A/B effect on qo, ol, final-m, TTR, h2, and are present inside a single hand and language. (iv) Hand differences among B scribes (2/3/5) are small, mainly word length/TTR, with n=3-5 pages; not robust. Line-final -m and paragraph-initial gallows both move with section (bio low -m, low gallows) and with A/B in herbal, i.e. not clean language markers. Note final-m and par-gallows rates rest on few lines/paragraphs per page (noisy).

## 3. Classifiers (leave-one-page-out, 300 glyph-bigram features, naive Bayes / logistic)
Overall: language A/B 0.99/0.98 (majority .57); section 0.73/0.70 (maj .48); hand 0.79/0.78 (maj .40; hands 2/3/5 confused).
Conditioned (NB acc vs majority): section | hand2&B (herbal vs bio) **0.97** vs .51; section | hand1&A (herbal vs pharma) 0.94 vs .71 (LR 0.75 = fails); hand | herbal&B (2/3/5) 0.62 vs .69 = **not predictable**; hand 2 vs 3 | B, H/B/S 0.77 vs .60 (but hand 3 = stars, section-confounded; LR 0.65); language | hand3 stars 1.00 vs .92 (2 A pages, uninformative).
Transfer: trained hand1-vs-hand2 on herbal -> bio(h2) 19/19 -> "hand 2", pharma(h1) 13/15 -> "hand 1": the A/B-hand axis is stable across section. Trained herbal-vs-bio in hand 2 -> applied to hand-1 herbal vs pharma: 0.73 (pharma mostly called herbal): section direction transfers only partly across the A/B boundary (section vocabulary is system-specific).
Ranking of predictability: language (circular: Currier defined it from these same words) > section (survives conditioning on hand+language) > hand (does not survive conditioning on language+section).

## 4. Continuum vs discrete
Out-of-fold A/B axis score (logistic) shows no overlap between A and B pages and a trough in the histogram (6,6 pages in the middle bins). Group means: A herbal -1.15, A pharma -0.49, B herbal +1.15, B stars +1.21, B bio +1.85. So the two clusters are separated, but position within each cluster is set by section (bio most extreme-B, pharma moves toward the middle). Hand-1 axis score rises with folio order (rho +0.47, p .0004) but **within hand-1 herbal rho +0.09 (p .60)**: the drift is the herbal->pharma section transition, not smooth scribe drift. Hand-1 herbal edy rises with folio (+0.41, p .013) from a ~0 base (tiny absolute change). Hand 2 overall drifts (qo +.58, ch -.55, TTR -.59) but within hand-2 herbal nothing is significant (n=18). Unlabelled pages f67r2 (-0.02) and f70r2 (-0.58) fall at the A end/middle. Evidence for a pure A-to-B gradient: weak.

## Conclusion
- **Topic/section vocabulary alone: rejected.** A and B herbal pages differ by d of 2.4-3.2 in edy/dy/ol while same-hand/same-language herbal vs non-herbal differ in different features (qo, TTR, h2, final-m) and A keeps edy ~0 in every section.
- **A/B is a two-state difference (not a smooth gradient)** with an additive section modulation inside each state. It is not an entropy/word-length difference (h2, wlen equal within herbal).
- **Scribe habit vs "two system settings" cannot be separated with this manuscript**: hand 1 == A, so the factors are collinear; the only cell breaking it (hand-3 A pages, n=2, edy~0 like hand 1) supports a language/system label independent of hand but is far too small. Hands 2/3/5 inside B are not reliably distinguishable once section is fixed, so "five scribes, five languages" is not supported, while a single hand-1 vs rest dichotomy is the strongest-looking story. Best description: two settings (affix/ending preferences -edy/-dy vs -ol) correlated with hand 1 vs others, overlaid by a section topic axis; scribe habit remains live for the settings.
- Rules out: A/B as topic-driven; A/B as an h2 or word-length phenomenon; hand 2/3/5 as separate languages; a smooth continuum along folio order (the apparent drift in hand 1 is section order).
- Caveats: Currier labels are page-level and derived from the very features tested (circular); section is coarse; small cells (n 2-6); EVA-only parsing, no second parsing run; quire (a further confound) not controlled.
