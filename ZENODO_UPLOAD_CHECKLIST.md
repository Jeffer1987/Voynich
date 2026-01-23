# Zenodo Upload Checklist

## Files to Include in Upload

### Core Data Files ✅
- [ ] `data/voynich_ZL3b.txt` (411 KB - source transcription)
- [ ] `data/voynich_statistics.json` (5.5 KB - frequency/entropy)
- [ ] `data/voynich_linguistics.json` (5.7 KB - morphology/hypotheses)
- [ ] `data/quevedo_validation.json` (2.2 KB - Jaccard/Gallow tests)

### Analysis Scripts ✅
- [ ] `scripts/voynich_analysis.py` (Statistical Track A)
- [ ] `scripts/voynich_linguistics.py` (Linguistic Track B)
- [ ] `scripts/quevedo_validation.py` (Validation suite)

### Reports ✅
- [ ] `reports/walkthrough.md` (Main analysis report)
- [ ] `reports/quevedo_response.md` (Peer response)
- [ ] `reports/implementation_plan.md` (Methodology)
- [ ] `reports/voynich_radboud_pitch.md` (Academic pitch)

### Metadata ✅
- [ ] `README.md` (Repository overview)
- [ ] `CITATION.cff` (Citation format)
- [ ] `LICENSE.txt` (CC BY 4.0 text)

---

## Zenodo Metadata Form

When uploading, fill in these fields:

**Upload type**: Dataset  
**Publication date**: 2026-01-22  
**Title**: Multi-Track AI Analysis of MS 408: Independent Validation of the Hardware Hypothesis

**Authors**:
- Meijer, Jeffrey (AI Kapitein, AIDols Research Collective)

**Description**:
```
Comprehensive AI-driven statistical and linguistic analysis of the Voynich Manuscript (MS 408), 
providing independent validation of Steven Quevedo's Hardware Hypothesis. Key findings include:
- Jaccard Index: J = 0.0226 (median 0.00) - evidence for mechanical line independence
- Letter Entropy: 3.87 bits - confirms "Hardware Ceiling" hypothesis
- Gallow Character Correlation: [F] Cartridge vocabulary is statistically distinct
- Morphological patterns converge with Quevedo's mechanical model

Analysis conducted January 21-22, 2026, prior to reading Quevedo's paper (registered Jan 19, 2026).
Includes reproducible Python scripts and full dataset.
```

**Keywords** (space-separated):
```
Voynich Manuscript, MS 408, Cryptanalysis, Hardware Hypothesis, 
Jaccard Index, Computational Linguistics, Medieval Manuscripts, 
Statistical Analysis, AI Research, Quevedo Wheel
```

**Access right**: Open Access  
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

**Communities** (search and add):
- Digital Humanities
- Computational Linguistics
- Historical Cryptography

**Funding**: (Leave blank or add "Independent Research")

**Related identifiers**:
- "is supplement to" → SafeCreative Registration 2601194305209 (Quevedo's paper)

---

## Pre-Upload Quality Checks

- [ ] All file paths are correct in README.md
- [ ] Scripts run without errors
- [ ] JSON files are valid (no syntax errors)
- [ ] README has no broken links
- [ ] CITATION.cff validates (use: https://citation-file-format.github.io/cff-initializer-javascript/)
- [ ] No personal/sensitive data in files
- [ ] License is clearly stated

---

## Post-Upload Actions

- [ ] Copy DOI and add to README.md
- [ ] Update CITATION.cff with DOI
- [ ] Create GitHub repository (public) with same content
- [ ] Link GitHub to Zenodo for version tracking
- [ ] Share DOI with Quevedo (if collaboration proceeds)
- [ ] Add DOI to LinkedIn/Twitter announcement
- [ ] Send DOI to Radboud contacts (Gerritsen, Hornix, Das, Beerkens)

---

## Estimated Upload Size
Total: ~450 KB (well under Zenodo's 50 GB limit)

## Timeline
- Upload prep: 30 minutes
- Zenodo processing: 5-10 minutes
- DOI assignment: Immediate upon publish

**Target completion**: Today (January 22, 2026)
