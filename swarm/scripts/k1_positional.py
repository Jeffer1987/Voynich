"""K1 positional: can the best K1 model (abbreviation + verbose cipher) reproduce T1 (line-final -m allograph),
T2 (paragraph-initial gallows), T3 (Currier A/B settings)?  Uses k1_sim.py functions (exec of its header, unmodified).
usage: python -I k1_positional.py parsed_zl3b.json baselines_dir out.json"""
import sys, os, re, json, math, random, collections, unicodedata
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
parsed, basedir, outjson = sys.argv[1:4]
src = open(os.path.join(HERE, 'k1_sim.py'), encoding='utf8').read()
src = src[:src.index("d = json.load(open(parsed))")]
exec(compile(src, 'k1_sim_head', 'exec'))     # defines fingerprint, abbreviate, make_verbose, load, dist, KEYS...
GL = re.compile(r'c[ktpf]h|ch|sh|[a-z]')
def evaglyphs(w): return tuple(GL.findall(w))

# ---------------------------------------------------------------- Voynich data
D = json.load(open(parsed))
P = [l for l in D if l['ltype'] == 'P']
vparas = []   # list of paragraphs; paragraph = list of lines (each list of glyph tuples) + meta
cur = None
for l in P:
    ws = [evaglyphs(w) for w in l['words'] if re.fullmatch('[a-z]+', w)]
    if l['pstart'] or cur is None:
        cur = dict(lines=[], L=l['L'], H=l['H'], I=l['I'], folio=l['folio']); vparas.append(cur)
    cur['lines'].append(ws)
VSTRUCT = [[len(x) for x in p['lines'] if len(x) > 0] for p in vparas]
VSTRUCT = [s for s in VSTRUCT if s]
VWORDS = [w for l in D for w in l['words'] if re.fullmatch('[a-z]+', w)]
VMS_FP = fingerprint([tuple(w) for w in VWORDS])

# ---------------------------------------------------------------- metrics (generic over glyph-tuple lines)
def t1_metrics(paras):
    """paras: list of paragraphs, each a list of lines (list of glyph tuples). continuation lines with >=3 words."""
    lines = [ln for p in paras for ln in p[1:] if len(ln) >= 3]
    fin = collections.Counter(); mid = collections.Counter(); nf = nm = 0
    for ln in lines:
        fin[ln[-1][-1]] += 1; nf += 1
        for w in ln[1:-1]: mid[w[-1]] += 1; nm += 1
    gl = set(fin) | set(mid)
    shift = {g: fin[g]/nf - mid[g]/nm for g in gl}
    M = max(shift, key=shift.get)
    out = dict(n_lines=len(lines), M=M if isinstance(M, str) else str(M), fin_rate=fin[M]/nf, mid_rate=mid[M]/nm,
               top_shift=shift[M])
    srt = sorted(shift.items(), key=lambda x: x[1])
    out['neg_top2'] = [g for g, _ in srt[:2]]
    out['neg_shifts'] = [round(v, 3) for _, v in srt[:3]]
    neg = [-v for _, v in srt if v < 0]
    out['neg_conc2'] = sum(neg[:2])/sum(neg) if neg else None
    out['pos_conc1'] = shift[M]/sum(v for v in shift.values() if v > 0)
    # gradient
    g2 = g3 = n2 = n3 = 0
    for ln in lines:
        if len(ln) >= 4:
            g2 += ln[-2][-1] == M; n2 += 1; g3 += ln[-3][-1] == M; n3 += 1
    out['grad'] = [round(out['fin_rate'], 3), round(g2/max(n2, 1), 3), round(g3/max(n3, 1), 3)]
    # words-per-line dependence
    bins = {'3-5': (3, 5), '6-8': (6, 8), '9+': (9, 99)}
    rb = {}
    for k, (a, b) in bins.items():
        s = [ln for ln in lines if a <= len(ln) <= b]
        rb[k] = (sum(ln[-1][-1] == M for ln in s)/len(s) if s else None, len(s))
    out['by_n'] = {k: (round(v[0], 3) if v[0] is not None else None, v[1]) for k, v in rb.items()}
    xs = np.array([len(ln) for ln in lines], float); ys = np.array([ln[-1][-1] == M for ln in lines], float)
    out['r_n'] = float(np.corrcoef(xs, ys)[0, 1]) if ys.std() > 0 else 0.0
    # paired stems
    midst = collections.defaultdict(collections.Counter)
    for ln in lines:
        for w in ln[1:-1]: midst[w[:-1]][w[-1]] += 1
    finst = [ln[-1] for ln in lines if ln[-1][:-1] in midst]
    fs = collections.Counter(w[-1] for w in finst)
    ms = collections.Counter();
    for st in set(w[:-1] for w in finst): ms.update(midst[st])
    tf, tm = sum(fs.values()), sum(ms.values())
    psh = {g: fs[g]/tf - ms[g]/tm for g in set(fs) | set(ms)}
    pM = max(psh, key=psh.get)
    psrt = sorted(psh.items(), key=lambda x: x[1])
    out['pair'] = dict(n_final=len(finst), top_pos=(str(pM), round(psh[pM], 3)), neg=[(str(g), round(v, 3)) for g, v in psrt[:3]])
    # source specificity: among tokens ending in neg_top2 + M
    S2 = set(out['neg_top2']) | {M}
    fm = sum(1 for ln in lines if ln[-1][-1] in S2); fM = fin[M]
    mm = sum(mid[g] for g in S2); mM = mid[M]
    out['among_S2'] = (round(fM/max(fm, 1), 3), round(mM/max(mm, 1), 3))
    # stems of final-M tokens attested mid with last glyph in neg_top2
    def att(w):
        c = midst.get(w[:-1]); return bool(c) and any(c[g] for g in out['neg_top2'])
    fM_t = [ln[-1] for ln in lines if ln[-1][-1] == M]; fo = [ln[-1] for ln in lines if ln[-1][-1] != M]
    out['stem_att_M'] = round(sum(att(w) for w in fM_t)/max(len(fM_t), 1), 3)
    out['stem_att_other'] = round(sum(att(w) for w in fo)/max(len(fo), 1), 3)
    # stem overdispersion
    per = collections.defaultdict(lambda: [0, 0])
    for ln in lines:
        st = ln[-1][:-1]; per[st][0] += 1; per[st][1] += ln[-1][-1] == M
    pool = fin[M]/nf
    sel = [(n, k) for n, k in per.values() if n >= 4]
    if len(sel) >= 5:
        var = np.mean([(k/n - pool)**2 for n, k in sel]); ex = np.mean([pool*(1-pool)/n for n, k in sel])
        out['overdisp'] = float(var/ex)
    else: out['overdisp'] = None
    out['n_stems_overdisp'] = len(sel)
    return out

def t2_metrics(paras):
    first = [p[0][0] for p in paras if p and p[0]]
    second = [p[0][1] for p in paras if p and len(p[0]) > 1]
    rest = [w for p in paras for i, ln in enumerate(p) for j, w in enumerate(ln) if not (i == 0 and j == 0)]
    linei = [ln[0] for p in paras for ln in p[1:] if ln]
    fg = lambda ws: collections.Counter(w[0] for w in ws)
    res = []
    for half in (0, 1):
        tr = fg(first[half::2]); top = [g for g, _ in tr.most_common(4)]
        te = first[1-half::2]
        res.append((sum(1 for w in te if w[0] in top)/len(te), top))
    top = [g for g, _ in fg(first).most_common(4)]
    sh = lambda ws, tp: sum(1 for w in ws if w[0] in tp)/max(len(ws), 1)
    # split-half validated: top set chosen on one half, evaluated on other, with rest-rate for the chosen set
    vals = []
    for half in (0, 1):
        tr = fg(first[half::2]); tp = [g for g, _ in tr.most_common(4)]
        te = first[1-half::2]
        vals.append((sh(te, tp), sh(rest, tp), sh(second, tp), sh(linei, tp)))
    v = np.mean(vals, axis=0)
    c = fg(first); n = len(first)
    return dict(n_par=n, top4_share_first=round(float(v[0]), 3), same4_in_rest=round(float(v[1]), 3),
                same4_word2=round(float(v[2]), 3), same4_lineinit=round(float(v[3]), 3),
                top_glyphs=[(str(g), round(k/n, 3), round(sh(rest, [g]), 3)) for g, k in c.most_common(4)])

def suffix_set(words_by_page, kmax=3, top=60):
    cnt = collections.Counter()
    for pg in words_by_page:
        for w in pg:
            for k in range(1, kmax+1):
                if len(w) >= k: cnt[w[-k:]] += 1
    return [s for s, _ in cnt.most_common(top)]

def ab_metrics(pagesA, pagesB, sufs=None):
    """pages: list of lists of words (glyph tuples). d = standardised difference of page-level suffix prevalence."""
    sufs = sufs or suffix_set(pagesA + pagesB)
    def prev(pg, s): return sum(1 for w in pg if w[-len(s):] == s)/len(pg)
    out = []
    for s in sufs:
        a = np.array([prev(p, s) for p in pagesA]); b = np.array([prev(p, s) for p in pagesB])
        sd = math.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2)) or 1e-9
        out.append((s, (a.mean()-b.mean())/sd, a.mean(), b.mean()))
    big = [x for x in out if abs(x[1]) > 2.4]
    # prefix leakage (first 1-2 glyphs)
    def prevp(pg, s): return sum(1 for w in pg if w[:len(s)] == s)/len(pg)
    pc = collections.Counter(w[:k] for pg in pagesA + pagesB for w in pg for k in (1, 2) if len(w) >= k)
    pre = [s for s, _ in pc.most_common(40)]
    pd_ = []
    for s in pre:
        a = np.array([prevp(p, s) for p in pagesA]); b = np.array([prevp(p, s) for p in pagesB])
        sd = math.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2)) or 1e-9
        pd_.append(abs((a.mean()-b.mean())/sd))
    wa = [w for p in pagesA for w in p]; wb = [w for p in pagesB for w in p]
    n = min(len(wa), len(wb), 6000)
    fa = fingerprint(wa[:n]); fb = fingerprint(wb[:n])
    return dict(nA=len(pagesA), nB=len(pagesB), n_suf_d24=len(big),
                top_suf=[(''.join(s) if all(isinstance(g, str) for g in s) else str(s), round(d, 2)) for s, d, _, _ in sorted(out, key=lambda x: -abs(x[1]))[:6]],
                n_pre_d24=sum(1 for x in pd_ if x > 2.4), maxd_pre=round(max(pd_), 2),
                dh2=round(fa['h2']-fb['h2'], 3), dwl=round(fa['wl']-fb['wl'], 3), dhapax=round(fa['hapax']-fb['hapax'], 3))

# ---------------------------------------------------------------- plaintext with line/paragraph structure
def load_lines(ids):
    """as k1_sim.load but keeps line structure: returns list of paragraphs (blank-line separated) of lists of word-lists"""
    paras = []; allw = []
    for i in ids:
        t = open(os.path.join(basedir, f'pg{i}.txt'), encoding='utf-8', errors='replace').read()
        a = t.find('*** START'); a = t.find('\n', a); b = t.find('*** END')
        t = t[a:b]
        cur = []
        for ln in ('\n' + t).split('\n'):
            x = unicodedata.normalize('NFD', ln.lower().replace('ß', 'ss').replace('æ', 'ae').replace('œ', 'oe'))
            x = ''.join(c for c in x if not unicodedata.combining(c)).replace('j', 'i').replace('v', 'u').replace('k', 'c')
            ws = re.findall(r'[a-z]+', x)
            if ws: cur.append(ws)
            elif cur: paras.append(cur); cur = []
        if cur: paras.append(cur)
    return paras

def reflow(words, rng):
    """cut word list into paragraphs/lines by sampling Voynich paragraph structures (independent of text)"""
    paras = []; i = 0
    while i < len(words):
        st = rng.choice(VSTRUCT); p = []
        for n in st:
            if i >= len(words): break
            p.append(list(range(i, min(i+n, len(words))))); i += n
        paras.append(p)
    return paras

def verse_layout(paras_txt, ntok):
    out = []; i = 0
    for p in paras_txt:
        pp = []
        for ln in p:
            idx = [j for j in range(i, i+len(ln)) if j < ntok]; i += len(ln)
            if idx: pp.append(idx)
        if pp: out.append(pp)
        if i >= ntok: break
    return out

# ---------------------------------------------------------------- encoder with rule hooks
class Enc:
    """abbr -> verbose grid. base codes identical to k1_sim E3 (extra symbols get cells after the base ones)."""
    def __init__(self, words, ab, a, b, seed, setting=None):
        self.ab = ab; self.types = set(words)
        self.sym = {w: abbreviate(w, ab) for w in self.types}
        syms = set(c for v in self.sym.values() for c in v)
        r = random.Random(seed); S = sorted(syms)
        cells = [(f'A{i}', f'B{j}') for i in range(a) for j in range(b)]; r.shuffle(cells)
        self.code = dict(zip(S, cells[:len(S)]))
        self.free = cells[len(S):]
        self.code['*'] = self.free[0]        # suspension mark (new symbol)
        self.cells = cells; self.S = S
        self.setting = setting or {}
        if setting:   # codebook variant: some symbols get other cells
            kind = setting['kind']
            if kind == 'swap_end':     # alternate spelling of the k most frequent word-final symbols
                fin = collections.Counter(v[-1] for v in self.sym.values())
                tgt = [s for s, _ in fin.most_common(setting['k'])]
                alt = self.free[1:1+len(tgt)]
                self.alt = dict(zip(tgt, alt))
            elif kind == 'swap_any':
                cnt = collections.Counter(c for v in self.sym.values() for c in v)
                tgt = [s for s, _ in cnt.most_common(setting['k'])]
                self.alt = dict(zip(tgt, self.free[1:1+len(tgt)]))
            elif kind == 'full':
                r2 = random.Random(seed+1000); c2 = cells[:]; r2.shuffle(c2)
                self.alt_full = dict(zip(S, c2[:len(S)])); self.alt_full['*'] = c2[len(S)]
            elif kind == 'pv':
                self.sym_alt = {w: abbreviate(w, dict(ab, pv=setting['pv'])) for w in self.types}
                extra = sorted(set(c for v in self.sym_alt.values() for c in v) - set(self.code))
                for k_, c_ in zip(extra, self.free[1:]): self.code[k_] = c_
            elif kind == 'ends':
                ab2 = dict(ab, ends=True)
                self.sym_alt = {w: abbreviate(w, ab2) for w in self.types}
                extra = sorted(set(c for v in self.sym_alt.values() for c in v) - set(self.code))
                for k_, c_ in zip(extra, self.free[1:]): self.code[k_] = c_
        self.cache = {}
    def rowshare(self, F):
        f1, f2 = F
        A = self.code[f1][0]
        used = {c[1] for c in self.code.values() if c[0] == A}
        freeB = [b for b in sorted({c[1] for c in self.cells}) if b not in used]
        self.code[f2] = (A, freeB[0]); self.code['*'] = (A, freeB[1]); self.cache = {}
    def word(self, w, alt=False, suspend=False, suspF=None):
        key = (w, alt, suspend)
        if key in self.cache: return self.cache[key]
        st = self.setting.get('kind') if alt else None
        sy = list(self.sym_alt[w]) if st in ('pv', 'ends') else list(self.sym[w])
        if suspend and len(sy) > 1 and (suspF is None or sy[-1] in suspF): sy[-1] = '*'
        out = []
        for c in sy:
            if alt and st == 'swap_end' and c == sy[-1] and c in self.alt: out += list(self.alt[c])   # only word-final position
            elif alt and st == 'swap_any' and c in self.alt: out += list(self.alt[c])
            elif alt and st == 'full': out += list(self.alt_full[c])
            else: out += list(self.code[c])
        res = tuple(out); self.cache[key] = res; return res

def render(words, layout, enc, rng, rule=None, alt_pages=None):
    """layout: list of paragraphs -> lines -> word indices. rule dict: lastw {'kind':'letter'|'glyph','p0':..,'scale':bool,'S':set,'M':glyph,'F':set},
    para {'q':..,'mark':[glyphs],'w':[weights],'mode':'prepend'|'replace'}"""
    paras = []
    for pi, p in enumerate(layout):
        lines = []
        for li, ln in enumerate(p):
            ws = [enc.word(words[i]) for i in ln]
            if rule and 'lastw' in rule and len(ln) >= 1:
                R = rule['lastw']; n = len(ln)
                prob = R['p0'] * (min(n, 12)/8.0 if R.get('scale') else 1.0)
                prob = min(prob, 1.0)
                el = R.get('elig'); ok = el is None or (zlib.crc32(words[ln[-1]].encode()) % 100) < 100*el
                if li > 0 and ok and rng.random() < prob:
                    if R['kind'] == 'letter':
                        ws[-1] = enc.word(words[ln[-1]], suspend=True, suspF=R.get('F'))
                    else:
                        w = ws[-1]
                        if w[-1] in R['S']: ws[-1] = w[:-1] + (R['M'],)
            if rule and 'para' in rule and li == 0 and pi >= 0:
                R = rule['para']
                if rng.random() < R['q']:
                    g = rng.choices(R['mark'], weights=R['w'])[0]
                    ws[0] = (g,) + (ws[0][1:] if R['mode'] == 'replace' else ws[0])
            lines.append(ws)
        paras.append(lines)
    return paras

def flat(paras): return [w for p in paras for ln in p for w in ln]

def short_t1(m):
    return (f"M={m['M']} fin {m['fin_rate']:.3f} mid {m['mid_rate']:.3f} | grad {m['grad']} | byN {m['by_n']} | r_n {m['r_n']:.2f} | "
            f"pairNeg {m['pair']['neg'][:2]} negConc2 {m['neg_conc2'] and round(m['neg_conc2'], 2)} | amongS2 {m['among_S2']} | stemAtt {m['stem_att_M']}/{m['stem_att_other']} | overdisp {m['overdisp'] and round(m['overdisp'], 2)} (n={m['n_stems_overdisp']})")

# ================================================================ run
RES = {}
def log(*a):
    print(*a, flush=True)

# Voynich targets (same functions)
vp = [p['lines'] for p in vparas]
V_T1 = t1_metrics(vp); V_T2 = t2_metrics(vp)
log('VOYNICH fp', {k: round(v, 2) for k, v in VMS_FP.items()})
log('VOYNICH T1', short_t1(V_T1)); log('VOYNICH T2', V_T2)
RES['voy_T1'] = V_T1; RES['voy_T2'] = V_T2

# Voynich A/B (herbal and all), pages = folios with >=80 P tokens
def vpages(sel):
    by = collections.defaultdict(list)
    for p in vparas:
        if sel(p): by[p['folio']].extend(w for ln in p['lines'] for w in ln)
    return [v for v in by.values() if len(v) >= 80]
ALLA = vpages(lambda p: p['L'] == 'A'); ALLB = vpages(lambda p: p['L'] == 'B')
HA = vpages(lambda p: p['L'] == 'A' and p['I'] == 'H'); HB = vpages(lambda p: p['L'] == 'B' and p['I'] == 'H')
V_AB_all = ab_metrics(ALLA, ALLB); V_AB_herb = ab_metrics(HA, HB)
log('VOYNICH A/B all', V_AB_all); log('VOYNICH A/B herbal', V_AB_herb)
RES['voy_AB_all'] = V_AB_all; RES['voy_AB_herb'] = V_AB_herb
PAGE_SIZES = [len(v) for v in ALLA + ALLB]

BEST = dict(pv=0.5, L=0, ends=False, short=True)
paras_txt = {'Italian': load_lines([1000]), 'Latin': load_lines([218, 18837])}
for lang in ('Italian', 'Latin'):
    flatw = [w for p in paras_txt[lang] for ln in p for w in ln]
    ref = load([1000] if lang == 'Italian' else [218, 18837])
    log(lang, 'line-aware loader matches k1_sim load:', flatw[:NTOK] == ref[:NTOK], len(flatw))
LANGCFG = {'Italian': dict(ab=BEST, a=11, b=11, seed=2), 'Latin': dict(ab=dict(pv=1.0, L=0, ends=True, short=True), a=11, b=11, seed=1)}

def run_cfg(lang, name, layout_kind, rule, nrep, ntok=NTOK, extra=None, rowF=None):
    cfg = LANGCFG[lang]
    words = [w for p in paras_txt[lang] for ln in p for w in ln][:ntok]
    enc = Enc(words, cfg['ab'], cfg['a'], cfg['b'], cfg['seed'])
    if rowF: enc.rowshare(rowF)
    t1s = []; t2s = []; fps = []
    for rep in range(nrep):
        rng = random.Random(100+rep)
        layout = reflow(words, rng) if layout_kind == 'reflow' else verse_layout(paras_txt[lang], len(words))
        paras = render(words, layout, enc, rng, rule)
        t1s.append(t1_metrics(paras)); t2s.append(t2_metrics(paras))
        if rep == 0: fps.append(fingerprint(flat(paras)))
        if layout_kind != 'reflow': break
    fp = fps[0]; s, z = dist(fp, VMS_FP)
    def avg(key, sub=None):
        v = [(m[key] if sub is None else m[key][sub]) for m in t1s]; v = [x for x in v if x is not None]
        return (float(np.mean(v)), float(np.std(v))) if v else None
    rec = dict(lang=lang, name=name, layout=layout_kind, rule=str(rule), fp={k: round(fp[k], 3) for k in KEYS}, dist=round(s, 2),
               T1_fin=avg('fin_rate'), T1_mid=avg('mid_rate'), T1_r_n=avg('r_n'), T1_overdisp=avg('overdisp'), T1_negconc=avg('neg_conc2'),
               T1_first=t1s[0], T2_first=t2s[0],
               T2_top4=(float(np.mean([m['top4_share_first'] for m in t2s])), float(np.mean([m['same4_in_rest'] for m in t2s])), float(np.mean([m['same4_word2'] for m in t2s]))))
    log(f"[{lang}/{name}/{layout_kind}] dist {rec['dist']} h2 {fp['h2']:.2f} wl {fp['wl']:.2f} hapax {fp['hapax']:.2f} alpha {fp['alpha']} | T1 fin {rec['T1_fin'][0]:.3f}+-{rec['T1_fin'][1]:.3f} mid {rec['T1_mid'][0]:.3f} r_n {rec['T1_r_n'][0]:.2f}")
    log('    T1', short_t1(t1s[0])); log('    T2 top4 first/rest/word2', [round(x, 3) for x in rec['T2_top4']], t2s[0]['top_glyphs'][:3])
    RES.setdefault('runs', []).append(rec)
    return rec, enc, words

# ---- M0
for lang in ('Italian', 'Latin'):
    run_cfg(lang, 'M0', 'reflow', None, 5)
    run_cfg(lang, 'M0', 'verse', None, 1)

# ---- M1a: final-word rule. determine S (two most frequent final glyphs) and M (rare final glyph) from the Italian encoding
lang = 'Italian'
rec0, enc, words = run_cfg(lang, 'M0-ref', 'reflow', None, 1)
finc = collections.Counter(enc.word(w)[-1] for w in words)
allg = collections.Counter(g for w in set(words) for g in enc.word(w))
S2 = {g for g, _ in finc.most_common(2)}
Mglyph = min((g for g in allg if g not in S2 and g.startswith('B') and finc[g] > 0), key=lambda g: abs(finc[g]/len(words)-0.01))
log('final-glyph freq top5', finc.most_common(5), 'S2', S2, 'M', Mglyph, 'M final count', finc[Mglyph])
flet = collections.Counter(enc.sym[w][-1] for w in words)
F2 = {s for s, _ in flet.most_common(2)}
log('final plaintext symbols top5', flet.most_common(5))
for p0 in (0.3, 0.5, 0.8):
    run_cfg(lang, f'M1a-glyph p={p0} const', 'reflow', dict(lastw=dict(kind='glyph', p0=p0, S=S2, M=Mglyph)), 5)
for p0 in (0.3, 0.5, 0.8):
    run_cfg(lang, f'M1a-glyph p={p0} scaled', 'reflow', dict(lastw=dict(kind='glyph', p0=p0, S=S2, M=Mglyph, scale=True)), 5)
for p0 in (0.3, 0.6):
    run_cfg(lang, f'M1a-letter(all) p={p0} const', 'reflow', dict(lastw=dict(kind='letter', p0=p0)), 5)
    run_cfg(lang, f'M1a-letter(F2) p={p0} const', 'reflow', dict(lastw=dict(kind='letter', p0=p0, F=F2)), 5)
    run_cfg(lang, f'M1a-letter(F2) p={p0} scaled', 'reflow', dict(lastw=dict(kind='letter', p0=p0, F=F2, scale=True)), 5)

for f_, p_ in ((0.5, 0.6), (0.3, 0.9)):
    run_cfg(lang, f'M1a-glyph elig={f_} p={p_} scaled', 'reflow', dict(lastw=dict(kind='glyph', p0=p_*0.6, S=S2, M=Mglyph, scale=True, elig=f_)), 5)
Fl = sorted(F2, key=lambda x: -flet[x])
run_cfg(lang, 'M1a-letter(F2) rowshare p=0.6 scaled', 'reflow', dict(lastw=dict(kind='letter', p0=0.6, F=F2, scale=True)), 5, rowF=Fl)
run_cfg(lang, 'M1a-letter(F2) rowshare p=0.6 const', 'reflow', dict(lastw=dict(kind='letter', p0=0.6, F=F2)), 5, rowF=Fl)
# ---- M1b: paragraph initial marker. marker set = 4 most common word-initial glyphs? use 4 existing A-glyphs of medium frequency
initc = collections.Counter(enc.word(w)[0] for w in words)
MK = [g for g, _ in initc.most_common(20)][3:7]
log('marker glyphs', MK, [round(initc[g]/len(words), 3) for g in MK])
for q in (0.83, 0.95):
    for mode in ('prepend', 'replace'):
        run_cfg(lang, f'M1b q={q} {mode}', 'reflow', dict(para=dict(q=q, mark=MK, w=[.54, .28, .13, .05], mode=mode)), 5)
RARE = [g for g, _ in sorted(initc.items(), key=lambda x: x[1])][:4]
log('rare marker glyphs', RARE, [round(initc[g]/len(words), 3) for g in RARE])
for q in (0.83,):
    run_cfg(lang, f'M1b q={q} prepend RARE', 'reflow', dict(para=dict(q=q, mark=RARE, w=[.54, .28, .13, .05], mode='prepend')), 5)
# combined (a-glyph scaled + b)
run_cfg(lang, 'M1ab combined', 'reflow', dict(lastw=dict(kind='glyph', p0=0.5, S=S2, M=Mglyph, scale=True), para=dict(q=0.9, mark=MK, w=[.54, .28, .13, .05], mode='prepend')), 5)

# ---- T3 / M1c: two settings
rng = random.Random(7)
def make_pages(words, enc, nA, setting_B=True, mode='interleave'):
    """pages of ~Voynich sizes, alternately drawn; page type A or B random (50/50)"""
    pg = []; i = 0
    r = random.Random(11)
    while i < len(words):
        n = r.choice(PAGE_SIZES); seg = words[i:i+n]; i += n
        if len(seg) < 80: break
        typ = 'B' if r.random() < 0.5 else 'A'
        pg.append((typ, seg, i))
    return pg
words = [w for p in paras_txt['Italian'] for ln in p for w in ln][:NTOK]
pagesdef = make_pages(words, None, 0)
def ab_run(name, setting):
    e = Enc(words, BEST, 11, 11, 2, setting)
    A = [[e.word(w) for w in seg] for t, seg, _ in pagesdef if t == 'A']
    B = [[e.word(w, alt=True) for w in seg] for t, seg, _ in pagesdef if t == 'B']
    m = ab_metrics(A, B); m['name'] = name
    log('A/B', name, {k: m[k] for k in ('nA', 'nB', 'n_suf_d24', 'top_suf', 'n_pre_d24', 'maxd_pre', 'dh2', 'dwl', 'dhapax')})
    RES.setdefault('ab', []).append(m); return m
ab_run('null (A=B same setting)', dict(kind='swap_end', k=0))
# topic analogue: first vs second half of plaintext, same codebook
e0 = Enc(words, BEST, 11, 11, 2)
A = [[e0.word(w) for w in seg] for t, seg, i in pagesdef if i < len(words)//2]
B = [[e0.word(w) for w in seg] for t, seg, i in pagesdef if i >= len(words)//2]
m = ab_metrics(A, B); m['name'] = 'topic analogue (text half 1 vs 2, same codebook)'; RES['ab'].append(m)
log('A/B', m['name'], {k: m[k] for k in ('n_suf_d24', 'top_suf', 'n_pre_d24', 'maxd_pre', 'dh2', 'dwl', 'dhapax')})
for k in (1, 2, 3, 5):
    ab_run(f'swap word-final symbol codes k={k}', dict(kind='swap_end', k=k))
for k in (2, 4):
    ab_run(f'swap any symbol codes k={k}', dict(kind='swap_any', k=k))
ab_run('different abbreviation intensity pv .5 vs .8', dict(kind='pv', pv=0.8))
ab_run('ending-suspension on (B) vs off (A)', dict(kind='ends'))
ab_run('independent full grid', dict(kind='full'))

json.dump(RES, open(outjson, 'w'), indent=1, default=str)
