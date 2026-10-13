# Code audit: voynich_analysis.py, voynich_linguistics.py, quevedo_validation.py

Checks run read-only with `python -I` on voynich_ZL3b.txt. No repo files were modified.

## Shared parser (identical in analysis.py and quevedo_validation.py)
Mostly works, with these defects:
- Locus tags, `#` comments, `{...}`, `<...>` markup, and splitting on `.` and `,` are handled. Page headers (`<f1r>  <! $Q=...>`) are not caught by the page regex, so they fall into the locus branch and strip to empty. This gives 10 empty "lines" in analysis.py (5386 vs 5376 real lines) and an `current_page` that is never set. Harmless to word counts, sloppy.
- `[a:b]` alternatives are deleted entirely (676 of them). Any word holding one loses that segment and becomes a fragment, e.g. `[cth:oto]res` becomes `res`. The correct handling is to pick the first reading.
- `@NNN;` ligature codes are deleted (143), which also leaves fragments such as `@163;s` becoming `s`.
- `?` is kept inside words. 93 words contain `?` and 151 `?` characters are counted as a "letter". Apostrophes (26) and one `I` also leak into the alphabet.
- `<->` is stripped, so words split across a line break are glued together. That is arguably correct, but it is undocumented.
- Hardcoded absolute paths (`C:\Users\Jeffrey\.gemini\...`) mean the scripts will not run elsewhere.
- Net effect: the leakage is small (under 1% of tokens) but real. "28 unique letters" is inflated by `?`, `'` and `I`. The true EVA alphabet is about 22-25 symbols.
- Metadata (headers, comments) does NOT leak into word counts.

## voynich_analysis.py (Track A)
- Letter entropy 3.870 reproduced exactly. Word entropy 10.47 and the other counts are consistent with the code. These are descriptive numbers and are trustworthy as such, with the caveats above.
- Entropy is per EVA character. EVA digraphs (ch, sh, and so on) are single glyphs, so this is not comparable to per-letter entropy of Latin or English.
- Zipf: the code only prints the ratio freq/(f1/rank) for the top 50 ranks. There is no log-log fit, no exponent, and no comparison with a natural-language or shuffled text. "Deviation" is judged by eye.
- The JSON stores only the top 50 words and top 30 letters, bigrams and trigrams. Downstream scripts see only that truncated data.
- No null baseline anywhere. Severity: medium (not wrong, but unsupported as evidence of anything).

## voynich_linguistics.py (Track B)
This is the least trustworthy script.
- It reads voynich_statistics.json, which contains only the top 50 words. All prefix, suffix, positional and "grammar pattern" counts are computed on 50 word types, not the corpus. Example: `qo_prefix` = 2040 is the sum of the top-50 qo-words only. `root_families_count: 20` is a count over those 50 words. Severity: high.
- The reference language values are hardcoded literals, not computed and not cited: Voynich 3.87, English 4.5, Latin 4.0, Italian 4.2, "Constructed (avg) 3.5", Random 4.7 and so on. They mix unit definitions (Voynich EVA glyph entropy vs per-letter entropy of natural languages), and "Constructed avg 3.5" has no source. Random 4.7 is also not log2 of any stated alphabet size. Treat as invented. Severity: high.
- `hypothesis_generator` is a text template. H1's only gate is `3.87 < 4.0`, which is the hardcoded value itself. H2, H3 and H4 are emitted unconditionally. Evidence strings are hardcoded: "daiin (799x)", "ch=11007, he=8198", "28 letters", "8381 words". No function computes "Zipf deviation suggests artificial", "highly regular morphology", "syntactic shifts" or "Currier A/B found". H1 is labelled confidence HIGH with no computation behind it, and it contradicts its own counter-evidence. H4 reports "entropy significantly lower than Italian" using the invented 4.2. Severity: critical for any conclusions drawn from the JSON.
- The `compare_with_languages` word-length figures (Latin 5.8, German 6.3 and so on) are also uncited.
- Trustworthy: nothing, other than the top-50 list that is passed through from Track A.

## quevedo_validation.py
- Jaccard is computed correctly as the mean over consecutive lines (mean 0.0226, median 0.0). Lines average 7.1 words, so most pairs share nothing, and low values are expected.
- The code has no null baseline. I tested this directly:

  | Text | Mean consecutive-line Jaccard |
  |---|---|
  | Real Voynich | 0.0226 |
  | Same words, shuffled across lines (20 runs, same line lengths) | 0.0104 (range 0.0097-0.0111) |
  | i.i.d. Zipf text (8381 types, same line lengths) | 0.0415 |
  | Real text, lag-50 lines | 0.0130 |

  - Real adjacent lines are about 2x more similar than shuffled, and more similar than lines 50 apart. Adjacent-line similarity therefore exists, which is the opposite of "line independence". The claim "validates Quevedo / mechanical independence" is unsupported and arguably contradicted.
  - A synthetic Zipf text gives a higher Jaccard than the Voynich text, so 0.02 is not anomalous for ~7-word lines.
- The thresholds are invented. "Natural language J = 0.25-0.35" and "Quevedo J = 0.08" appear as literals, with no natural-language computation. For 7-word lines, 0.25-0.35 is implausible. The output `validation: 'CONFIRMED'` is decided by `avg < 0.15`, which any short-line text passes. Severity: critical.
- The "gallow correlation" test is not a correlation test:
  - It keys on the first letter of the first word of the line, and assigns that to every word in the line. It does not look at gallows within words.
  - It takes `word[1:4]` roots and just lists the top 10 per class. `non_gallow_vocab` is computed and never used. There is no statistical test. The JSON holds only top-10 counts, which are dominated by group size (p and t have many more lines than f and k).
  - The p-vs-f overlap ratio printed to the console is not saved to the JSON. It would be biased by the different sample sizes anyway.
  - The top roots (che, oke, heo, aii, cho) are the same across all four gallow classes, which is evidence against distinct vocabularies, not for them.
  - The first-letter-of-first-word statistic is also confounded with paragraph-initial gallow effects, which are known features of the text.
- Line-end entropy: first-word entropy 10.31 vs last-word entropy 10.24, a 0.07-bit gap. There is no significance test or bootstrap, and the code prints "SUPPORTS QUEVEDO" whenever last < first. Noise-level difference. The actual notable signal (line-final `dy`, `am`, `dam`) is a known positional effect and is unrelated to the entropy claim. Severity: high.
- Pages and paragraphs are not separated, so consecutive-line pairs cross page and section boundaries. This is minor.

## Overall
- Reliably computed: raw counts, letter/word entropy, n-gram counts, the Jaccard mean value.
- Not trustworthy: every conclusion, verdict, confidence label and comparison to other languages. No result in these scripts is a significant departure from a null model, because no null model is run.
- Hardcoded or invented content: the language entropy and word-length tables, the Quevedo and natural-language Jaccard ranges, the hypothesis texts and confidences, and the numbers embedded in the evidence strings.
