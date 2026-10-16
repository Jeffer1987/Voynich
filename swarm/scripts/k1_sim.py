"""K1 simulation: verbose cipher / syllabary / abbreviation encodings of Latin & Italian vs Voynich fingerprint.
usage: python -I k1_sim.py parsed_zl3b.json baselines_dir out.json [quick]"""
import sys, json, re, unicodedata, random, math, collections, os, zlib
import numpy as np
parsed, basedir, outjson = sys.argv[1:4]
NTOK = 35000
VOW = set('aeiouy')

def H(c):
    t = sum(c.values()); return -sum(v/t*math.log2(v/t) for v in c.values())

def wseed(w): return zlib.crc32(w.encode())

def fingerprint(toks):
    """toks: list of tuples of glyph symbols."""
    toks = toks[:NTOK]
    n = len(toks)
    uni = collections.Counter(); wb = collections.Counter(); cb = collections.Counter()
    prev = None; tot_g = 0
    for w in toks:
        if not w: continue
        for g in w: uni[g] += 1
        tot_g += len(w)
        for a, b in zip(w, w[1:]): wb[(a, b)] += 1
        if prev is not None: cb[(prev[-1], w[0])] += 1
        prev = w
    def hcond(bg):
        fa = collections.Counter()
        for (a, b), v in bg.items(): fa[a] += v
        return H(bg) - H(fa)
    sp_u = collections.Counter(uni); sp_u[' '] = n - 1
    sp_b = collections.Counter(wb)
    for (a, b), v in cb.items():
        sp_b[(a, ' ')] += v; sp_b[(' ', b)] += v
    h1 = H(uni)
    h2sp = H(sp_b) - H(sp_u)
    tc = collections.Counter(toks); types = len(tc)
    hap = sum(1 for v in tc.values() if v == 1)
    freqs = sorted(tc.values(), reverse=True)[:1000]
    x = np.log(np.arange(1, len(freqs)+1)); y = np.log(freqs)
    slope = float(np.polyfit(x, y, 1)[0])
    alpha = sum(1 for v in uni.values() if v/tot_g >= 0.001)
    pos = collections.defaultdict(list)
    for w in toks:
        if len(w) >= 2:
            for i, g in enumerate(w): pos[g].append(i/(len(w)-1))
    mp = {g: float(np.mean(v)) for g, v in pos.items()}
    ok = 0
    for w in toks:
        r = [mp.get(g, 0.5) for g in w]
        if all(a <= b for a, b in zip(r, r[1:])): ok += 1
    return dict(h1=h1, h2=h2sp, h2_within=hcond(wb), h2_cross=hcond(cb), wl=tot_g/n, alpha=alpha,
                ttr=types/n, hapax=hap/types, zipf=slope, slot=ok/n)

KEYS = ['h1','h2','wl','alpha','ttr','hapax','zipf','slot','h2_within','h2_cross']
TOL = dict(h1=0.25, h2=0.2, wl=0.5, alpha=3, ttr=0.04, hapax=0.05, zipf=0.1, slot=0.08, h2_within=0.2, h2_cross=0.3)

def dist(fp, tgt):
    z = {k: (fp[k]-tgt[k])/TOL[k] for k in KEYS}
    return math.sqrt(sum(v*v for v in z.values())/len(z)), z

def load(ids):
    txt = ''
    for i in ids:
        t = open(os.path.join(basedir, f'pg{i}.txt'), encoding='utf-8', errors='replace').read()
        a = t.find('*** START'); a = t.find('\n', a); b = t.find('*** END')
        txt += '\n' + t[a:b]
    txt = unicodedata.normalize('NFD', txt.lower().replace('ß','ss').replace('æ','ae').replace('œ','oe'))
    txt = ''.join(c for c in txt if not unicodedata.combining(c))
    txt = txt.replace('j','i').replace('v','u').replace('k','c')   # scribal merges
    return re.findall(r'[a-z]+', txt)

ONSET2 = {'br','cr','dr','gr','pr','tr','fr','bl','cl','gl','pl','fl','ch','ph','th','qu'}
def syllabify(w):
    i = 0; nuc = []
    while i < len(w):
        if w[i] in VOW:
            j = i+1
            if j < len(w) and w[i:j+1] in ('ae','au','oe','eu'): j += 1
            nuc.append((i, j)); i = j
        else: i += 1
    if not nuc: return [w]
    cuts = [0]
    for (s1, e1), (s2, e2) in zip(nuc, nuc[1:]):
        c = w[e1:s2]
        if len(c) <= 1: cut = e1 if len(c) == 0 else e1
        elif c[-2:] in ONSET2: cut = s2-2
        else: cut = s2-1
        cuts.append(cut)
    cuts.append(len(w))
    return [w[a:b] for a, b in zip(cuts, cuts[1:]) if b > a]

ENDS = {'us':'1','um':'2','que':'3','bus':'4','rum':'5','tur':'6'}
SHORT = {'et':'7','est':'8','non':'9','quod':'0','cum':'@','per':'#','pro':'$','ut':'%'}
def abbreviate(w, p):
    """p: pv=prob drop each non-initial vowel (fixed per word type), L=max letters before suspension mark (0=off), ends, short"""
    if p.get('short') and w in SHORT: return [SHORT[w]]
    rng = random.Random(wseed(w))
    tail = []
    if p.get('ends'):
        for e in sorted(ENDS, key=len, reverse=True):
            if w.endswith(e) and len(w) > len(e)+1:
                w = w[:-len(e)]; tail = [ENDS[e]]; break
    s = list(w)
    if p.get('L') and len(s) > p['L']:
        s = s[:p['L']]; tail = ['*']
    out = [c for i, c in enumerate(s) if not (i > 0 and c in VOW and rng.random() < p['pv'])]
    return out + tail

def make_verbose(symbols, a, b, seed, structured=False):
    r = random.Random(seed)
    syms = sorted(symbols)
    if structured:   # first glyph = letter class (vowel / consonant groups), second = within-class index
        cls = collections.defaultdict(list)
        for k, s in enumerate(syms): cls[(0 if s in VOW else 1 + (k % max(1, a-1)))].append(s)
        code = {}
        for c, ss in sorted(cls.items()):
            cols = r.sample(range(b), min(b, len(ss)))
            for s, col in zip(ss, cols): code[s] = ('A%d' % c, 'B%d' % col)
        for s in syms:
            if s not in code: code[s] = ('A%d' % (zlib.crc32(s.encode()) % a), 'B%d' % (zlib.crc32(s.encode()) % b))
        return code
    cells = [(f'A{i}', f'B{j}') for i in range(a) for j in range(b)]
    r.shuffle(cells)
    if len(cells) < len(syms): raise ValueError('grid too small')
    return dict(zip(syms, cells[:len(syms)]))

def enc_E1(words, a, b, seed, structured=False):
    letters = set(c for w in words for c in w)
    code = make_verbose(letters, a, b, seed, structured)
    return {w: tuple(g for c in w for g in code[c]) for w in set(words)}

def enc_syll(words, G, K, seed, abbr=None):
    """syllabary: top K syllables -> 1 glyph, rest -> 2-glyph codes from a G-glyph set"""
    r = random.Random(seed)
    types = set(words); wsyl = {}
    for w in types:
        sw = ''.join(abbreviate(w, abbr)) if abbr else w
        parts = []; cur = ''
        for c in sw:
            if c.isalpha(): cur += c
            else:
                if cur: parts += syllabify(cur); cur = ''
                parts.append(c)
        if cur: parts += syllabify(cur)
        wsyl[w] = parts
    cnt = collections.Counter(); tc = collections.Counter(words)
    for w, parts in wsyl.items():
        for p in parts: cnt[p] += tc[w]
    ranked = [s for s, _ in cnt.most_common()]
    glyphs = [f'g{i}' for i in range(G)]
    code = {}
    K = min(K, G)   # only G distinct single-glyph codes exist
    g1 = glyphs[:]; r.shuffle(g1)
    for s, g in zip(ranked[:K], g1): code[s] = (g,)
    cells = [(x, y) for x in glyphs for y in glyphs]; r.shuffle(cells)
    rest = ranked[K:]
    for s, cell in zip(rest, cells): code[s] = cell
    for s in rest[len(cells):]: code[s] = (glyphs[zlib.crc32(s.encode()) % G],)
    return {w: tuple(g for p in parts for g in code[p]) for w, parts in wsyl.items()}

def enc_E3(words, a, b, seed, abbr):
    types = set(words)
    ab = {w: abbreviate(w, abbr) for w in types}
    syms = set(c for v in ab.values() for c in v)
    code = make_verbose(syms, a, b, seed)
    return {w: tuple(g for c in ab[w] for g in code[c]) for w in types}

def enc_E6(words, pm, nmarks):
    """abjad: consonant -> 1 glyph; vowel kept with prob pm (fixed per word type) as one of nmarks mark glyphs; initial vowel always kept"""
    types = set(words); out = {}
    cons = sorted(set(c for w in types for c in w if c not in VOW))
    cg = {c: f'c{i}' for i, c in enumerate(cons)}
    vm = {v: f'm{i % nmarks}' for i, v in enumerate(sorted(VOW))}
    for w in types:
        rr = random.Random(wseed(w)); o = []
        for i, c in enumerate(w):
            if c in VOW:
                if i == 0 or rr.random() < pm: o.append(vm[c])
            else: o.append(cg[c])
        out[w] = tuple(o)
    return out

def run_E5(words, a, b, nbig, nhom, seed):
    """homophonic verbose: units = letters + top-nbig digrams; each unit gets 1 + proportional share of nhom extra 2-glyph codes; random homophone per occurrence"""
    r = random.Random(seed)
    big = collections.Counter()
    for w in set(words):
        for x, y in zip(w, w[1:]): big[x+y] += 1
    bigs = set(k for k, _ in big.most_common(nbig))
    def units(w):
        o = []; i = 0
        while i < len(w):
            if w[i:i+2] in bigs: o.append(w[i:i+2]); i += 2
            else: o.append(w[i]); i += 1
        return o
    uc = collections.Counter()
    for w in words: uc.update(units(w))
    ul = [u for u, _ in uc.most_common()]
    cells = [(f'A{i}', f'B{j}') for i in range(a) for j in range(b)]; r.shuffle(cells)
    extra = max(0, min(nhom, len(cells) - len(ul))); tot = sum(uc.values())
    code = {}; idx = 0
    for u in ul:
        k = 1 + int(round(extra * uc[u] / tot)); code[u] = cells[idx: idx+k]; idx += k
        if idx >= len(cells): idx = 0
    r2 = random.Random(seed+1)
    return [tuple(g for u in units(w) for g in r2.choice(code[u])) for w in words]

d = json.load(open(parsed))
vw = [w for l in d for w in l['words'] if w and re.fullmatch(r'[a-z]+', w)]
VMS = fingerprint([tuple(w) for w in vw])
LANG = {'Latin': [218, 18837], 'Italian': [1000]}
texts = {k: load(v)[:NTOK] for k, v in LANG.items()}
plain_fp = {k: fingerprint([tuple(w) for w in t]) for k, t in texts.items()}

quick = len(sys.argv) > 4
SEEDS = [1, 2, 3] if not quick else [1]
results = []
def record(lang, fam, params, toks):
    if toks is None: return
    fp = fingerprint(toks); s, z = dist(fp, VMS)
    core = (abs(fp['h2']-VMS['h2']) <= 0.3 and abs(fp['wl']-VMS['wl']) <= 0.75 and abs(fp['hapax']-VMS['hapax']) <= 0.07 and abs(fp['ttr']-VMS['ttr']) <= 0.07)
    results.append(dict(lang=lang, fam=fam, params=params, score=s, core=core, fp=fp, z=z))

def tok(f, words):
    try: m = f()
    except ValueError: return None
    return [m[w] for w in words]
ABBRS = [dict(pv=pv, L=L, ends=e, short=sh) for pv in (0.0, 0.5, 0.9, 1.0) for L in (0, 3, 4, 6) for e in (False, True) for sh in (False, True)]
if quick: ABBRS = ABBRS[::5]
for lang, words in texts.items():
    for (a, b) in [(5,5),(6,4),(8,4),(10,3),(11,11),(4,12),(3,9)]:
        for st in (False, True):
            for sd in SEEDS:
                record(lang, 'E1', dict(a=a, b=b, structured=st, seed=sd), tok(lambda: enc_E1(words, a, b, sd, st), words))
    for G in (8, 12, 16, 22):
        for K in (0, 8, 20, 50):
            for sd in SEEDS[:2]:
                record(lang, 'E2', dict(G=G, K=K, seed=sd), tok(lambda: enc_syll(words, G, K, sd), words))
    for ab in ABBRS:
        for (a, b) in [(5,5),(6,4),(8,4),(11,11)]:
            for sd in SEEDS[:2]:
                record(lang, 'E3', dict(ab=ab, a=a, b=b, seed=sd), tok(lambda: enc_E3(words, a, b, sd, ab), words))
        for G, K in [(12,0),(16,20),(22,50)]:
            record(lang, 'E4', dict(ab=ab, G=G, K=K), tok(lambda: enc_syll(words, G, K, 1, abbr=ab), words))
    for pm in (0.0, 0.3, 0.6, 1.0):
        for nm in (1, 3, 5):
            record(lang, 'E6', dict(pm=pm, nmarks=nm), tok(lambda: enc_E6(words, pm, nm), words))
    for (a, b) in [(6,6),(8,8),(11,11)]:
        for nbig in (0, 10, 30):
            for nhom in (0, 20, 60):
                record(lang, 'E5', dict(a=a, b=b, nbig=nbig, nhom=nhom), run_E5(words, a, b, nbig, nhom, 1))

def enc_E7(words, G, m, seed, abbr):
    # hybrid: abbreviation -> top-m symbols get 1 glyph, others 2-glyph codes over G glyphs
    types = set(words); ab = {w: abbreviate(w, abbr) for w in types}
    cnt = collections.Counter(); tc = collections.Counter(words)
    for w, v in ab.items():
        for c in v: cnt[c] += tc[w]
    syms = [c for c, _ in cnt.most_common()]
    r = random.Random(seed); glyphs = [f'g{i}' for i in range(G)]
    m = min(m, G, len(syms)); g1 = glyphs[:]; r.shuffle(g1)
    cells = [(x, y) for x in glyphs for y in glyphs]; r.shuffle(cells)
    if len(cells) < len(syms) - m: raise ValueError('small')
    code = {s_: (g,) for s_, g in zip(syms[:m], g1)}
    code.update({s_: c for s_, c in zip(syms[m:], cells)})
    return {w: tuple(g for c in ab[w] for g in code[c]) for w in types}
rs_ = random.Random(99); NS = 40 if quick else 450
for lang, words in texts.items():
    for _ in range(NS):
        ab = dict(pv=rs_.choice([0, .3, .6, .8, .9, 1.0]), L=rs_.choice([0, 3, 4, 5, 6]), ends=rs_.random() < .5, short=rs_.random() < .5)
        G = rs_.choice([10, 14, 18, 22]); m = rs_.choice([0, 4, 8, 12, 16, 22]); sd = rs_.choice([1, 2, 3, 4])
        record(lang, 'E7', dict(ab=ab, G=G, m=m, seed=sd), tok(lambda: enc_E7(words, G, m, sd, ab), words))
json.dump(dict(vms=VMS, plain=plain_fp, results=results), open(outjson, 'w'), indent=1)

fmt = lambda f: {k: round(v, 2) for k, v in f.items()}
print('VMS', fmt(VMS))
for k, v in plain_fp.items(): print('PLAIN', k, fmt(v), round(dist(v, VMS)[0], 2))
for lang in texts:
    for fam in ['E1','E2','E3','E4','E5','E6','E7']:
        rs = sorted([r for r in results if r['lang'] == lang and r['fam'] == fam], key=lambda r: r['score'])
        print(f'\n== {lang} {fam}: n={len(rs)} core-pass={sum(r["core"] for r in rs)}')
        for r in rs[:3]:
            print(round(r['score'], 2), r['core'], json.dumps(r['params']), fmt(r['fp']))

cp = [r for r in results if r['core']]
print('CORE PASS total', len(cp))
for r in sorted(cp, key=lambda r: r['score'])[:8]: print(r['lang'], r['fam'], round(r['score'],2), json.dumps(r['params']), fmt(r['fp']))
