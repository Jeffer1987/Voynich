"""
Voynich Manuscript Statistical Analysis
AIDols Finale Challenge - Track A: Statistical Cryptanalysis
"""

import re
from collections import Counter
from pathlib import Path
import json
import math

def parse_ivtff(filepath):
    """Parse IVTFF format transcription file"""
    words = []
    lines_data = []
    current_page = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Extract page markers
            page_match = re.match(r'<(f\d+[rv]\d?)>', line)
            if page_match:
                current_page = page_match.group(1)
                continue
            
            # Extract text content (between locus marker and end)
            # Format: <f1r.1,@P0>       text.here.with.words
            locus_match = re.match(r'<([^>]+)>\s*(.+)', line)
            if locus_match:
                locus = locus_match.group(1)
                text = locus_match.group(2)
                
                # Remove markup tags like <%>, <$>, <->, <! ... >
                text = re.sub(r'<[^>]*>', '', text)
                # Remove uncertain markers [x:y]
                text = re.sub(r'\[[^\]]*\]', '', text)
                # Remove curly brace annotations {xxx}
                text = re.sub(r'\{[^}]*\}', '', text)
                # Remove @ references
                text = re.sub(r'@\d+;?', '', text)
                
                # Split by word separators (. and ,)
                line_words = re.split(r'[.,]', text)
                line_words = [w.strip() for w in line_words if w.strip()]
                
                words.extend(line_words)
                lines_data.append({
                    'page': current_page,
                    'locus': locus,
                    'words': line_words,
                    'raw': text
                })
    
    return words, lines_data

def letter_frequency(words):
    """Calculate letter frequency"""
    all_letters = ''.join(words)
    return Counter(all_letters)

def word_frequency(words):
    """Calculate word frequency"""
    return Counter(words)

def calculate_entropy(freq_dict, total):
    """Calculate Shannon entropy"""
    entropy = 0
    for count in freq_dict.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy

def ngram_analysis(words, n=2):
    """Calculate n-gram frequency"""
    all_text = '.'.join(words)  # Keep word boundaries
    ngrams = []
    for i in range(len(all_text) - n + 1):
        ngram = all_text[i:i+n]
        if '.' not in ngram:  # Skip word boundaries
            ngrams.append(ngram)
    return Counter(ngrams)

def word_length_distribution(words):
    """Analyze word length distribution"""
    lengths = [len(w) for w in words]
    return Counter(lengths)

def zipf_analysis(word_freq):
    """Check Zipf's law compliance"""
    sorted_freq = sorted(word_freq.values(), reverse=True)
    results = []
    for rank, freq in enumerate(sorted_freq[:50], 1):
        expected_zipf = sorted_freq[0] / rank
        ratio = freq / expected_zipf if expected_zipf > 0 else 0
        results.append({
            'rank': rank,
            'frequency': freq,
            'expected_zipf': round(expected_zipf, 2),
            'ratio': round(ratio, 2)
        })
    return results

def main():
    filepath = Path(r"C:\Users\Jeffrey\.gemini\antigravity\playground\magnetic-cosmos\voynich_ZL3b.txt")
    output_dir = Path(r"C:\Users\Jeffrey\.gemini\antigravity\playground\magnetic-cosmos")
    
    print("=" * 60)
    print("VOYNICH MANUSCRIPT STATISTICAL ANALYSIS")
    print("AIDols Finale - Track A: Statistical Cryptanalysis")
    print("=" * 60)
    
    # Parse transcription
    print("\n[1] Parsing IVTFF transcription...")
    words, lines_data = parse_ivtff(filepath)
    print(f"    Total words extracted: {len(words):,}")
    print(f"    Total lines parsed: {len(lines_data):,}")
    
    # Letter frequency analysis
    print("\n[2] Letter frequency analysis...")
    letter_freq = letter_frequency(words)
    total_letters = sum(letter_freq.values())
    print(f"    Total letters: {total_letters:,}")
    print(f"    Unique letters: {len(letter_freq)}")
    print(f"    Top 10 letters: {letter_freq.most_common(10)}")
    
    # Word frequency analysis
    print("\n[3] Word frequency analysis...")
    word_freq = word_frequency(words)
    print(f"    Unique words: {len(word_freq):,}")
    print(f"    Top 15 most common words:")
    for word, count in word_freq.most_common(15):
        pct = (count / len(words)) * 100
        print(f"        '{word}': {count} ({pct:.2f}%)")
    
    # Entropy calculation
    print("\n[4] Entropy analysis...")
    letter_entropy = calculate_entropy(letter_freq, total_letters)
    word_entropy = calculate_entropy(word_freq, len(words))
    print(f"    Letter entropy: {letter_entropy:.3f} bits")
    print(f"    Word entropy: {word_entropy:.3f} bits")
    print(f"    (English: ~4.5 bits/letter, Latin: ~4.0 bits/letter)")
    
    # N-gram analysis
    print("\n[5] Bigram analysis...")
    bigrams = ngram_analysis(words, 2)
    print(f"    Top 10 bigrams: {bigrams.most_common(10)}")
    
    print("\n[6] Trigram analysis...")
    trigrams = ngram_analysis(words, 3)
    print(f"    Top 10 trigrams: {trigrams.most_common(10)}")
    
    # Word length distribution
    print("\n[7] Word length distribution...")
    word_lengths = word_length_distribution(words)
    print(f"    Distribution: {dict(sorted(word_lengths.items()))}")
    avg_len = sum(len(w) for w in words) / len(words)
    print(f"    Average word length: {avg_len:.2f} characters")
    
    # Zipf's law analysis
    print("\n[8] Zipf's law compliance...")
    zipf = zipf_analysis(word_freq)
    print(f"    Rank 1: '{word_freq.most_common(1)[0][0]}' = {zipf[0]['frequency']}")
    print(f"    Rank 2 ratio: {zipf[1]['ratio']:.2f} (ideal: 1.0)")
    print(f"    Rank 10 ratio: {zipf[9]['ratio']:.2f} (ideal: 1.0)")
    
    # Compile results
    results = {
        'metadata': {
            'source': str(filepath),
            'analysis_type': 'Statistical Cryptanalysis',
            'track': 'A'
        },
        'summary': {
            'total_words': len(words),
            'unique_words': len(word_freq),
            'total_letters': total_letters,
            'unique_letters': len(letter_freq),
            'average_word_length': round(avg_len, 2),
            'letter_entropy': round(letter_entropy, 3),
            'word_entropy': round(word_entropy, 3)
        },
        'letter_frequency': dict(letter_freq.most_common(30)),
        'word_frequency': dict(word_freq.most_common(50)),
        'bigrams': dict(bigrams.most_common(30)),
        'trigrams': dict(trigrams.most_common(30)),
        'word_length_distribution': dict(sorted(word_lengths.items())),
        'zipf_analysis': zipf[:20]
    }
    
    # Save results
    output_file = output_dir / "voynich_statistics.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[✓] Results saved to: {output_file}")
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    main()
