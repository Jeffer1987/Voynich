# 11 K1 on herbal/technical Latin (wave 5A)

Script: `swarm/scripts/k1_herbal.py` (execs the definitions of `k1_sim.py`, which is unmodified; args: parsed_zl3b.json, herbal dir, classical dir, out json). Raw: scratchpad `k1h_full.txt/.json`. Runtime ~7.5 min.

## Sources (Latin Wikisource, raw wikitext via `action=raw`, markup stripped; public domain; same normalization as 4C: NFD, j=i, u=v, k=c)
- Macer Floridus / Odo Magdunensis, *De viribus herbarum* (11th c., verse herbal): https://la.wikisource.org/wiki/De_viribus_herbarum — 13,967 words.
- Walahfrid Strabo, *Hortulus* (9th c., verse garden poem): https://la.wikisource.org/wiki/Hortulus — only 2,990 words, so fingerprints at equal N are not valid (TTR 0.69 is a small-N artefact); excluded from K1 runs, included in the HerbMix.
- Apicius, *De re coquinaria* books I-X (recipes, prose; late antique, not medieval): https://la.wikisource.org/wiki/De_re_coquinaria (/Liber_I .. /Liber_X) — 14,614 words.
- HerbMix = Macer + Hortulus + Apicius, 31,571 words.
- Not obtained: Latin Library has no herbal (checked its medieval index; /macer.html, /walafrid.html are 404); no medieval vernacular herbal fetched (no easy plaintext source found). Hildegard's *Physica*, Circa instans etc. not found on Wikisource. Verified by sample: content is Latin herbal/recipe text (top words: si, et, cum, uino, piper, liquamen, oleum, ligusticum).
- Voynich: ZL3b a-z words; all = 37,953; herbal Currier A (I=H, L=A) = 7,497; herbal B = 3,306.

## Part 2: raw fingerprints at equal token counts
| N | text | h2 | wl | TTR | hapax/type | Zipf | slot |
|---|---|---|---|---|---|---|---|
| 13000 | **Voynich all** | 2.26 | 4.95 | 0.32 | **0.73** | -0.97 | 0.31 |
| 13000 | Macer | 3.30 | 5.84 | 0.29 | 0.58 | -0.79 | 0.10 |
| 13000 | Apicius | 3.19 | 5.71 | 0.19 | 0.54 | -0.98 | 0.18 |
| 13000 | Caesar (ref) | 3.29 | 5.97 | 0.32 | 0.63 | -0.85 | 0.13 |
| 13000 | Dante (ref) | 3.10 | 3.97 | 0.25 | 0.65 | -0.98 | 0.37 |
| 30000 | Voynich all | 2.19 | 5.05 | 0.24 | 0.72 | -1.01 | 0.29 |
| 30000 | HerbMix | 3.31 | 5.80 | 0.24 | 0.59 | -0.83 | 0.13 |
| 7497 | **Voynich herbal A** | 2.16 | 5.04 | 0.35 | **0.74** | -1.02 | 0.42 |
| 7497 | Macer / Apicius / HerbMix | 3.30 / 3.18 / 3.30 | 5.8 / 5.7 / 5.8 | 0.35 / 0.25 / 0.35 | 0.61 / 0.59 / 0.61 | | |

Voynich hapax across ten random 13k windows: 0.70-0.74 (stable). Smaller N pushes hapax up in all texts, but at equal N the gap persists: **herbal/recipe Latin does not close the hapax gap** (0.54-0.61 vs 0.72-0.74; classical Latin at the same N is 0.59-0.63). Macer is slightly higher in TTR than Apicius (plant names, varied inflection) but its hapax is no higher than Caesar's at 30k. The within-section target (herbal A) is, if anything, higher (0.74) and further away. h2 and word length of the herbal sources are the same as classical Latin (h2 about 3.3), so the source itself brings nothing toward the Voynich entropy profile.

## Part 3: K1 rerun (same 3 families and grids as 4C: E3 abbreviation+verbose, E5 homophonic digram-verbose, E7 hybrid; 765 configs per run, no new parameters)
Targets are the Voynich fingerprint at the same N. Core pass = h2 within .3, wl .75, hapax .07, TTR .07; strict = core and all 10 |z| <= 2.

| run | core-pass | strict | best score (family) | max hapax over any config | plain hapax |
|---|---|---|---|---|---|
| Macer, N=13k, target all | 0 | 0 | 1.86 (E7) | 0.965 | 0.58 |
| Apicius, N=13k, target all | 0 | 0 | 2.04 (E7) | 0.964 | 0.54 |
| HerbMix, N=30k, target all | 0 | 0 | 1.76 (E7) | 0.967 | 0.59 |
| Macer, N=13k, target herbal A | 0 | 0 | 2.26 (E7) | 0.965 | 0.58 |

(4C on Caesar/Dante, N=35k: best 1.07 Italian E7, 1.73 Latin E7, 0 core passes. The herbal Latin best scores, 1.76-2.04, are the same as 4C Latin, not better.)

Observations:
- Configs that match h2 and wl (E3/E7 with heavy vowel loss, 2-glyph codes) keep hapax at 0.51-0.54, i.e. below even the plain text (abbreviation merges types), so the miss is -0.2 on hapax.
- Hapax is reached or exceeded only by E5 with per-occurrence homophones (14 configs per run with hapax >= 0.66, e.g. Macer a=b=8, nbig=30, nhom=20: hapax 0.74). These simultaneously have wl 8.4-8.8, h2 2.8-2.9, TTR 0.39-0.50 and slot 0.01-0.09: they fail wl, h2, TTR and the slot structure. None has h2 and wl near target (0 of the high-hapax configs). So hapax can be bought only by breaking the types-per-token and length profile.
- Best E3/E7 fits again reproduce h2 within-word / cross-boundary gap (h2_within 1.8-1.9 vs 2.2; cross 3.1-3.2 vs 3.0) but with wl about 7 (E3) or h2 2.5-2.7 (E7).

## Verdict: herbal Latin does NOT rescue K1 (status: still partial, weaker than 4C suggested)
- The hypothesis that the hapax miss was a baseline artefact is refuted for two technical/herbal Latin sources: raw hapax of 0.54-0.61 at equal N vs 0.73 (0.74 for herbal A).
- No config passes the core test on any source (0 of 3,060 runs of the three families), and none is within 2 sigma on all features. Parameter count unchanged from 4C (6-7 free choices), so no further overfitting was introduced.
- A deterministic per-type encoding cannot raise the hapax fraction; per-occurrence variation can, but then wl/h2/TTR break. A rescued K1 would need an extra mechanism (e.g. context-dependent glyph variation that preserves the short word length and h2), not a different plaintext genre.
- Caveats: only verse herbal (Macer) and a recipe text (Apicius, late antique) were tested; no abbreviation-heavy manuscript transcription, no vernacular herbal; N is only 13k-30k so tolerances are rougher than in 4C; the abbreviation model is still synthetic. A real abbreviated medieval Latin transcription could behave differently, but a hapax gain of +0.15-0.20 from genre alone looks unlikely given Macer's and Apicius's values.
