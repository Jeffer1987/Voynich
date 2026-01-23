# Statistical Validation of Structure in MS 408: Independent Confirmation of the Jaccard Anomaly

**Authors**: Jeffrey Meijer (AI Kapitein), AIDols Research Collective  
**Date**: January 21-22, 2026  
**License**: CC BY 4.0 (Creative Commons Attribution)  
**DOI**: 10.5281/zenodo.18346527
**GitHub**: https://github.com/Jeffer1987/Voynich

---

## Abstract

This repository presents a rigorous AI-driven statistical analysis of the Voynich Manuscript (MS 408), identifying a fundamental structural anomaly that differentiates the text from natural language. Conducted as the proposed finale of the "AIDols" research project (January 19-22, 2026), this study provides **independent statistical confirmation** of the "Jaccard Anomaly" first observed by S.A. Quevedo (2026).

Our analysis isolates the statistical signature (Jaccard Index J ≈ 0.02, Entropy ≈ 3.87 bits) which suggests a non-natural, algorithmic, or mechanical generation process. This repository validates the **data observation** without endorsing specific mechanical reconstructions or historical interpretations.

**Key Finding**: The text exhibits extreme line-to-line vocabulary independence (median Jaccard Index = 0.00), a statistical impossibility in natural narrative prose, confirming the presence of a generative constraint or algorithm.

---

## Repository Structure

```
voynich-aidols-analysis/
├── data/                          # Raw transcription and analysis results
│   ├── voynich_ZL3b.txt          # Zandbergen-Landini EVA transcription (source)
│   ├── voynich_statistics.json    # Frequency, entropy, Zipf analysis
│   ├── voynich_linguistics.json   # Morphology, grammar patterns, hypotheses
│   └── quevedo_validation.json    # Jaccard Index, Gallow correlation tests
│
├── scripts/                       # Reproducible analysis code
│   ├── voynich_analysis.py       # Statistical cryptanalysis (Track A)
│   ├── voynich_linguistics.py    # Comparative linguistics (Track B)
│   └── quevedo_validation.py     # Hardware Hypothesis validation suite
│
├── reports/                       # Human-readable analysis documents
│   ├── walkthrough.md            # Complete analysis report with ranked hypotheses
│   ├── quevedo_response.md       # Peer response to Quevedo's paper
│   ├── implementation_plan.md    # Multi-track analysis framework
│   └── Voynich_Forensic_Case_Study.md # AI-driven forensic analysis case study
│
└── README.md                      # This file
```

---

## Methodology

### Phase 1: Multi-Track Analysis (Pre-Quevedo)
We employed a parallel analysis framework inspired by the "Move 37" strategy (identifying patterns outside human intuition):

- **Track A: Statistical Cryptanalysis** - Letter/word frequency, entropy calculations, n-gram analysis, Zipf's law compliance
- **Track B: Comparative Linguistics** - Morphological patterns, language comparison, grammar detection, hypothesis generation
- **Track E: Novel AI Approaches** - Cross-validation, anomaly detection, "vocabulary explosion paradox"

### Phase 2: Quevedo Validation (Post-Quevedo)
Upon encountering Quevedo's paper, we designed a targeted validation suite:

1. **Jaccard Similarity Index** - Measuring line-to-line vocabulary independence
2. **Gallow Character Correlation** - Testing the "Mode Selector" hypothesis
3. **Line Position Entropy** - Analyzing "filler word" patterns

---

## Key Results

| Metric | Our Finding | Quevedo's Claim | Interpretation |
|--------|-------------|-----------------|----------------|
| **Jaccard Index (avg)** | **0.0226** | ≈ 0.08 | ✅ Exceeds expectation - stronger evidence for mechanical independence |
| **Jaccard Index (median)** | **0.00** | - | ✅ 50% of lines have zero vocabulary overlap |
| **Letter Entropy** | **3.87 bits** | - | Confirms "Hardware Ceiling" (vs. natural 4.0-4.5) |
| **Zipf Ratio (rank 10)** | **4.12** | - | "Slot Machine" saturation pattern |
| **Gallow [F] Vocabulary** | Statistically distinct | Mode selector | ✅ Supports Cartridge swapping |

---

## Novel Contributions

1. **The "Vocabulary Explosion Paradox"**: Only 28 unique letters generate 8,381 unique words (ratio: 299 words/letter) - evidence for a combinatorial engine with limited components but high permutation output.

2. **Rigorous Jaccard Measurement**: First quantitative measurement of line-to-line independence (J = 0.0226), validating the "Amnesiac Author" anomaly.

3. **Morphological-Mechanical Convergence**: What we independently identified as "agglutinative suffixes" precisely matches Quevedo's "Inner Ring positions" - convergent evidence from orthogonal methodologies.

4. **Cross-Section Framework**: Methodology for measuring entropy shifts across manuscript sections (Herbal vs. Astronomical) to detect Cartridge swapping events.

---

## Reproducibility

All analysis scripts are written in Python 3.x and require only standard libraries:
- `collections` (Counter, defaultdict)
- `statistics`
- `json`
- `re` (regex)
- `pathlib`

To replicate our findings:

```bash
# Clone or download this repository
cd voynich-aidols-analysis

# Run statistical analysis
python scripts/voynich_analysis.py

# Run linguistic analysis
python scripts/voynich_linguistics.py

# Run Quevedo validation suite
python scripts/quevedo_validation.py
```

All outputs will be saved to the `data/` directory as JSON files.

---

## Citation

If you use this work in your research, please cite:

```
Meijer, J. (2026). Multi-Track AI Analysis of MS 408: Independent Validation 
of the Hardware Hypothesis. AIDols Research Collective. 
Zenodo. https://doi.org/[DOI_WILL_BE_ASSIGNED]
```

For the original Hardware Hypothesis, please cite:

```
Quevedo Vinueza, S. A. (2026). The Quevedo Wheel Mechanism: Engineering 
Blueprints for the Hardware-Generated Syntax of MS 408. 
SafeCreative Registration: 2601194305209.
```

---

## Acknowledgments

- **Steven Quevedo** for the pioneering Hardware Hypothesis and the Quevedo Wheel reconstruction
- **Rene Zandbergen** for the EVA transcription (voynich.nu)
- **The Voynich research community** for decades of foundational work

---

## License

This work is licensed under **CC BY 4.0** (Creative Commons Attribution 4.0 International).

You are free to:
- **Share** — copy and redistribute the material
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.

The Voynich manuscript itself is in the public domain. The transcription (EVA) is provided by the Voynich research community. Our analysis, code, and interpretations are original work.

---

## Contact

For collaboration, questions, or data requests:
- GitHub Issues: [https://github.com/Jeffer1987/Voynich]
- Email: jeffrey@aikapitein.com

---

**Last Updated**: January 22, 2026  
**Version**: 1.0.0  
**Status**: Deposited for permanent archival and DOI assignment
