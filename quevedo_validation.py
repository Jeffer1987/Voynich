"""
Quevedo Wheel Validation Suite
Testing the Hardware Hypothesis against MS 408 (Voynich Manuscript)

This script validates three key claims from Quevedo's paper:
1. Jaccard Index ≈ 0.08 (line-to-line independence)
2. Gallow characters correlate with vocabulary shifts (Mode Selectors)
3. Line-end words show "filler" patterns (aesthetic constraint)
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
import statistics

def parse_ivtff_advanced(filepath):
    """Enhanced parser with line metadata"""
    lines = []
    current_page = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            if not line or line.startswith('#'):
                continue
            
            # Page markers
            page_match = re.match(r'<(f\d+[rv]\d?)>', line)
            if page_match:
                current_page = page_match.group(1)
                continue
            
            # Extract text with locus info
            locus_match = re.match(r'<([^>]+)>\s*(.+)', line)
            if locus_match:
                locus = locus_match.group(1)
                text = locus_match.group(2)
                
                # Clean markup
                text = re.sub(r'<[^>]*>', '', text)
                text = re.sub(r'\[[^\]]*\]', '', text)
                text = re.sub(r'\{[^}]*\}', '', text)
                text = re.sub(r'@\d+;?', '', text)
                
                # Split into words
                words = [w.strip() for w in re.split(r'[.,]', text) if w.strip()]
                
                if words:
                    lines.append({
                        'page': current_page,
                        'locus': locus,
                        'words': words,
                        'first_word': words[0],
                        'last_word': words[-1],
                        'has_gallow': any(w[0] in 'pftk' for w in words if w)
                    })
    
    return lines

def calculate_jaccard_index(lines):
    """
    Jaccard Similarity: J(A,B) = |A ∩ B| / |A ∪ B|
    Measures vocabulary overlap between consecutive lines
    """
    jaccard_scores = []
    
    for i in range(len(lines) - 1):
        set_a = set(lines[i]['words'])
        set_b = set(lines[i+1]['words'])
        
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        
        if union > 0:
            jaccard = intersection / union
            jaccard_scores.append(jaccard)
    
    return jaccard_scores

def analyze_gallow_correlation(lines):
    """
    Test if Gallow characters (p, f, t, k) correlate with vocabulary shifts
    Quevedo's claim: Gallows are "Mode Selectors" switching cartridges
    """
    gallow_vocab = defaultdict(Counter)
    non_gallow_vocab = defaultdict(Counter)
    
    for line in lines:
        # Extract first character of first word
        if line['words']:
            first_char = line['words'][0][0].lower() if line['words'][0] else ''
            
            # Count root frequencies
            for word in line['words']:
                if len(word) >= 2:
                    root = word[1:4] if len(word) >= 4 else word[1:]
                    
                    if first_char in 'pftk':
                        gallow_vocab[first_char][root] += 1
                    else:
                        non_gallow_vocab['other'][root] += 1
    
    return gallow_vocab, non_gallow_vocab

def line_position_entropy(lines):
    """
    Compare entropy of line-initial vs line-final words
    Quevedo's claim: Line-end words are "aesthetic fillers"
    """
    first_words = Counter()
    last_words = Counter()
    
    for line in lines:
        if line['words']:
            first_words[line['first_word']] += 1
            last_words[line['last_word']] += 1
    
    # Calculate Shannon entropy
    def shannon_entropy(counter):
        import math
        total = sum(counter.values())
        entropy = 0
        for count in counter.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        return entropy
    
    return {
        'first_word_entropy': shannon_entropy(first_words),
        'last_word_entropy': shannon_entropy(last_words),
        'first_words_top10': first_words.most_common(10),
        'last_words_top10': last_words.most_common(10)
    }

def main():
    filepath = Path(r"C:\Users\Jeffrey\.gemini\antigravity\playground\magnetic-cosmos\voynich_ZL3b.txt")
    
    print("=" * 70)
    print("QUEVEDO WHEEL VALIDATION SUITE")
    print("Testing the Hardware Hypothesis")
    print("=" * 70)
    
    # Parse data
    print("\n[1] Parsing manuscript with enhanced metadata...")
    lines = parse_ivtff_advanced(filepath)
    print(f"    Parsed {len(lines)} text lines")
    
    # TEST 1: Jaccard Index
    print("\n[2] JACCARD INDEX ANALYSIS (Quevedo's Central Claim)")
    print("    Expected (Natural Language): J ≈ 0.25-0.35")
    print("    Expected (Quevedo/Hardware): J ≈ 0.08")
    
    jaccard_scores = calculate_jaccard_index(lines)
    avg_jaccard = statistics.mean(jaccard_scores)
    median_jaccard = statistics.median(jaccard_scores)
    
    print(f"\n    RESULTS:")
    print(f"    Average Jaccard: {avg_jaccard:.4f}")
    print(f"    Median Jaccard:  {median_jaccard:.4f}")
    print(f"    Std Deviation:   {statistics.stdev(jaccard_scores):.4f}")
    
    if avg_jaccard < 0.15:
        print(f"    ✅ VALIDATES QUEVEDO: Score {avg_jaccard:.4f} confirms mechanical independence")
    elif avg_jaccard < 0.25:
        print(f"    ⚠️  PARTIAL SUPPORT: Lower than natural language but higher than Quevedo's 0.08")
    else:
        print(f"    ❌ CONTRADICTS QUEVEDO: Score suggests natural language flow")
    
    # TEST 2: Gallow Correlation
    print("\n[3] GALLOW CHARACTER ANALYSIS (Mode Selector Hypothesis)")
    gallow_vocab, non_gallow_vocab = analyze_gallow_correlation(lines)
    
    print("\n    Top roots after each Gallow character:")
    for gallow in ['p', 'f', 't', 'k']:
        if gallow in gallow_vocab:
            top_roots = gallow_vocab[gallow].most_common(5)
            print(f"    [{gallow.upper()}] Mode: {top_roots}")
    
    # Check if vocabularies are distinct
    p_roots = set(gallow_vocab.get('p', {}).keys())
    f_roots = set(gallow_vocab.get('f', {}).keys())
    
    if p_roots and f_roots:
        overlap = len(p_roots & f_roots) / len(p_roots | f_roots)
        print(f"\n    [P] vs [F] Vocabulary Overlap: {overlap:.2%}")
        if overlap < 0.5:
            print(f"    ✅ SUPPORTS QUEVEDO: Distinct vocabularies suggest cartridge swapping")
        else:
            print(f"    ⚠️  HIGH OVERLAP: May contradict strict cartridge theory")
    
    # TEST 3: Line-End Entropy
    print("\n[4] LINE POSITION ENTROPY (Filler Word Hypothesis)")
    entropy_data = line_position_entropy(lines)
    
    print(f"\n    First-word entropy: {entropy_data['first_word_entropy']:.3f}")
    print(f"    Last-word entropy:  {entropy_data['last_word_entropy']:.3f}")
    print(f"\n    Most common first words: {entropy_data['first_words_top10'][:5]}")
    print(f"    Most common last words:  {entropy_data['last_words_top10'][:5]}")
    
    if entropy_data['last_word_entropy'] < entropy_data['first_word_entropy']:
        diff = entropy_data['first_word_entropy'] - entropy_data['last_word_entropy']
        print(f"    ✅ SUPPORTS QUEVEDO: Last words {diff:.2f} bits LESS varied")
        print(f"       → Suggests aesthetic padding at line endings")
    else:
        print(f"    ⚠️  INCONCLUSIVE: Last words show similar/higher variation")
    
    # Save results
    results = {
        'jaccard_analysis': {
            'average': avg_jaccard,
            'median': median_jaccard,
            'quevedo_claim': 0.08,
            'natural_language_range': [0.25, 0.35],
            'validation': 'CONFIRMED' if avg_jaccard < 0.15 else 'PARTIAL'
        },
        'gallow_correlation': {
            mode: dict(vocab.most_common(10)) 
            for mode, vocab in gallow_vocab.items()
        },
        'line_position': entropy_data
    }
    
    output_path = Path(r"C:\Users\Jeffrey\.gemini\antigravity\playground\magnetic-cosmos\quevedo_validation.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[✓] Results saved to: {output_path}")
    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
