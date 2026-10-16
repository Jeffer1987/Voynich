import sys, json, re, unicodedata, random, math, collections, os
import numpy as np
parsed_zl, basedir, outjson = sys.argv[1], sys.argv[2], sys.argv[3]
N = 40000; NCH = 8
rng = random.Random(1)

def H(counts):
    t = sum(counts.values()); return -sum(c/t*math.log2(c/t) for c in counts.values())
def stats(sym, words_only=None):
    """sym: list of symbols (' ' = space). returns h0,h1,h2"""
    u = collections.Counter(sym); b = collections.Counter(zip(sym, sym[1:]))
    return math.log2(len(u)), H(u), H(b) - H(u)
def nospace(sym): return [s for s in sym if s != ' ']

# ---- Voynich
d = json.load(open(parsed_zl))
def vwords(filt=None):
    out = []
    for l in d:
        if filt and not filt(l): continue
        out += [w for w in l['words'] if w]
    return out
SEGS = {
 'raw':  [],
 'S1':   ['ckh','cth','cph','cfh','ch','sh'],
 'S2':   ['ckh','cth','cph','cfh','ch','sh','iiin','iin','iii','ii','in'],
 'S3':   ['ckh','cth','cph','cfh','ch','sh','iiin','iin','iii','ii','in','eee','ee'],
 'S4':   ['ckh','cth','cph','cfh','ch','sh','aiin','aiir','ain','aii','ai','iiin','iin','iii','ii','in','eee','ee','dy','ol','or','al','ar'],
}
def seg_word(w, units):
    out = []; i = 0
    us = sorted(units, key=lambda x: -len(x))
    while i < len(w):
        for u in us:
            if w.startswith(u, i): out.append(u); i += len(u); break
        else: out.append(w[i]); i += 1
    return out
def to_stream(words, units):
    s = []
    for k, w in enumerate(words):
        if k: s.append(' ')
        s += seg_word(w, units)
    return s
def bpe_stream(words, nmerge):
    # words as lists of chars; greedy most frequent adjacent pair within words
    ws = [list(w) for w in words]
    for _ in range(nmerge):
        c = collections.Counter()
        for w in ws:
            for a, b in zip(w, w[1:]): c[(a, b)] += 1
        if not c: break
        (a, b), _n = c.most_common(1)[0]
        for w in ws:
            i = 0
            while i < len(w)-1:
                if w[i] == a and w[i+1] == b: w[i:i+2] = [a+b]
                else: i += 1
    s = []
    for k, w in enumerate(ws):
        if k: s.append(' ')
        s += w
    return s

def chunks(sym, n=N, k=NCH):
    if len(sym) <= n: return [sym]
    return [sym[st:st+n] for st in (rng.randrange(0, len(sym)-n) for _ in range(k))]
def agg(sym, label, res):
    cs = chunks(sym)
    r = [stats(c) for c in cs]; rn = [stats(nospace(c)) for c in cs]
    wl = [ (len(c) - c.count(' ')) / (c.count(' ')+1) for c in cs]
    # alphabet incl space on the full stream
    a = len(set(sym))
    row = dict(label=label, alpha=a, wl=float(np.mean(wl)), n=len(sym), nchunks=len(cs))
    for i, nm in enumerate(['h0','h1','h2']):
        row[nm] = float(np.mean([x[i] for x in r])); row[nm+'_sd'] = float(np.std([x[i] for x in r]))
        row[nm+'_ns'] = float(np.mean([x[i] for x in rn])); row[nm+'_ns_sd'] = float(np.std([x[i] for x in rn]))
    res.append(row); return row

res = []
allw = vwords()
for nm, u in SEGS.items(): agg(to_stream(allw, u), 'VMS-ZL all '+nm, res)
for cur in 'AB':
    w = vwords(lambda l, cur=cur: l['L'] == cur)
    for nm in ['raw','S2','S4']: agg(to_stream(w, SEGS[nm]), f'VMS Currier {cur} '+nm, res)
# BPE to match alphabet sizes
for nm in [8, 15, 25]:
    agg(bpe_stream(allw, nm), f'VMS BPE{nm}', res)

# ---- baselines
def load(ids):
    txt = ''
    for i in ids:
        t = open(os.path.join(basedir, f'pg{i}.txt'), encoding='utf-8', errors='replace').read()
        a = t.find('*** START'); a = t.find('\n', a)
        b = t.find('*** END')
        txt += '\n' + t[a:b]
    txt = unicodedata.normalize('NFD', txt.lower().replace('ß','ss').replace('æ','ae').replace('œ','oe'))
    txt = ''.join(c for c in txt if not unicodedata.combining(c))
    return re.findall(r'[a-z]+', txt)
LANG = {'Latin (Caesar BG, PG218+18837)': [218, 18837], 'Italian (Dante, PG1000)': [1000],
        'German (Faust I, PG2229)': [2229], 'English (P&P, PG1342)': [1342]}
CIPH = {}
for nm, ids in LANG.items():
    w = load(ids)
    st = to_stream(w, [])
    print(nm, len(w), 'words', len(st), 'symbols', file=sys.stderr)
    agg(st, nm + ' plain', res)
    # verbose cipher: each letter -> 2 glyphs, fixed random code over 5-glyph x 5-glyph grid (25 cells >= 26? use 6x5)
    letters = sorted(set(c for c in st if c != ' '))
    r2 = random.Random(7)
    g1 = list('abcdef'); g2 = list('ghijk')
    cells = [(a, b) for a in g1 for b in g2]; r2.shuffle(cells)
    code = dict(zip(letters, cells))
    vs = []
    for c in st:
        if c == ' ': vs.append(' ')
        else: vs += list(code[c])
    agg(vs, nm + ' VERBOSE glyph-level(2 per letter)', res)
    # same cipher but with a 'natural' small alphabet: 3x3 digit pairs? skip. Also cipher read as 2-glyph units:
    vu = []
    for c in st: vu.append(' ' if c == ' ' else ''.join(code[c]))
    agg(vu, nm + ' VERBOSE unit-level (=plain)', res)
    # BPE of plaintext to Voynich-like alphabet isn't needed; also plain with 12 BPE merges
    agg(bpe_stream(w, 12), nm + ' plain BPE12', res)
json.dump(res, open(outjson, 'w'), indent=1)
print(f"{'label':58s} alpha  wl   h0   h1   h2(sp)  h2(nospace)")
for r in res:
    print(f"{r['label']:58s} {r['alpha']:3d} {r['wl']:5.2f} {r['h0']:.2f} {r['h1']:.2f} {r['h2']:.3f}±{r['h2_sd']:.3f} {r['h2_ns']:.3f}±{r['h2_ns_sd']:.3f}")
