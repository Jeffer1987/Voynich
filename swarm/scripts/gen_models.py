"""Wave 6: generator hypotheses G1-G4 vs the K1 fingerprint.  usage: python -I gen_models.py parsed_zl3b.json baselines_dir out.json
Reuses (unmodified, via exec) k1_sim.py head and k1_positional.py head (fingerprint, dist, t1/t2/ab metrics, Enc, Voynich data)."""
import sys, os, re, json, math, random, collections, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]] + sys.argv[1:4]
parsed, basedir, outjson = sys.argv[1:4]
src = open(os.path.join(HERE, 'k1_positional.py'), encoding='utf8').read()
src = src[:src.index("BEST = dict(")]
src = src.replace("__file__", repr(os.path.join(HERE, 'k1_positional.py')))
RES = {}
import io, contextlib
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(src, 'k1_positional_head', 'exec'))
def log(*a): print(*a, flush=True)
NT = NTOK
ENV = dict(globals())

# ------------------------------------------------------------------ extra layout metrics
def ed1(a, b):
    la, lb = len(a), len(b)
    if a == b: return False
    if la == lb: return sum(x != y for x, y in zip(a, b)) == 1
    if abs(la-lb) != 1: return False
    s, l = (a, b) if la < lb else (b, a)
    i = 0
    while i < len(s) and s[i] == l[i]: i += 1
    return s[i:] == l[i+1:]

def jacc(paras, rng):
    lines = [ln for p in paras for ln in p]
    def J(plist):
        v = []
        for p in plist:
            for a, b in zip(p, p[1:]):
                sa, sb = set(a), set(b)
                if sa and sb: v.append(len(sa & sb)/len(sa | sb))
        return float(np.mean(v))
    real = J(paras)
    allw = [w for ln in lines for w in ln]; vals = []
    for _ in range(2):
        rng.shuffle(allw); i = 0; sp = []
        for p in paras:
            q = []
            for ln in p: q.append(allw[i:i+len(ln)]); i += len(ln)
            sp.append(q)
        vals.append(J(sp))
    return real, float(np.mean(vals))

def neigh(paras, rng):
    def rates(pl):
        n = idn = e1 = 0
        for p in pl:
            for ln in p:
                for a, b in zip(ln, ln[1:]):
                    n += 1; idn += a == b; e1 += ed1(a, b)
        return idn/n, e1/n
    ri, re_ = rates(paras)
    ni = ne = 0; R = 2
    for _ in range(R):
        sp = []
        for p in paras:
            flat_ = [w for ln in p for w in ln]; rng.shuffle(flat_); i = 0; q = []
            for ln in p: q.append(flat_[i:i+len(ln)]); i += len(ln)
            sp.append(q)
        a, b = rates(sp); ni += a/R; ne += b/R
    return ri, ni, re_, ne

def layout(words, seed=0):
    rng = random.Random(seed); paras = []; i = 0
    while i < len(words):
        st = rng.choice(VSTRUCT); p = []
        for n in st:
            if i >= len(words): break
            p.append(words[i:i+n]); i += n
        paras.append(p)
    return paras

TOLX = dict(jr=0.5, idr=0.3, edr=0.3)
def evaluate(words, tag='', vref=None, chars=True):
    """words: list of glyph tuples (len NT). chars=True: fingerprint on EVA characters (as VMS_FP), layout/T metrics on glyphs."""
    fp = fingerprint([tuple(''.join(w)) for w in words[:NT]] if chars else words[:NT])
    d10, z = dist(fp, VMS_FP)
    paras = layout(words)
    rng = random.Random(5)
    jr, jn = jacc(paras, rng); ri, ni, re_, ne = neigh(paras, rng)
    m = dict(fp=fp, d10=d10, jac=jr, jac_null=jn, jac_ratio=jr/jn, id_ratio=ri/max(ni, 1e-9), ed_ratio=re_/max(ne, 1e-9),
             id_rate=ri, ed_rate=re_)
    if vref:
        zz = [(m['jac_ratio']-vref['jac_ratio'])/TOLX['jr'], (m['id_ratio']-vref['id_ratio'])/TOLX['idr'], (m['ed_ratio']-vref['ed_ratio'])/TOLX['edr']]
        m['d13'] = math.sqrt((d10**2*10 + sum(x*x for x in zz))/13)
    t1 = t1_metrics(paras); t2 = t2_metrics(paras)
    m['T1'] = dict(M=t1['M'], fin=round(t1['fin_rate'], 3), mid=round(t1['mid_rate'], 3), top_shift=round(t1['top_shift'], 3), stem_att=(t1['stem_att_M'], t1['stem_att_other']))
    m['T2'] = dict(first=t2['top4_share_first'], rest=t2['same4_in_rest'])
    # T3: consecutive pages; null = random labels; drift = first half vs second half
    pages = []; i = 0; r = random.Random(11)
    while i < len(words):
        n = r.choice(PAGE_SIZES); seg = words[i:i+n]; i += n
        if len(seg) >= 80: pages.append(seg)
    lab = [r.random() < .5 for _ in pages]
    A = [p for p, l in zip(pages, lab) if l]; B = [p for p, l in zip(pages, lab) if not l]
    a1 = ab_metrics(A, B); h = len(pages)//2; a2 = ab_metrics(pages[:h], pages[h:])
    m['T3'] = dict(null_suf=a1['n_suf_d24'], null_pre=a1['n_pre_d24'], drift_suf=a2['n_suf_d24'], drift_pre=a2['n_pre_d24'], drift_dh2=a2['dh2'], drift_dwl=a2['dwl'])
    return m
def short(m):
    f = m['fp']
    return (f"d10 {m['d10']:.2f}" + (f" d13 {m['d13']:.2f}" if 'd13' in m else '') + f" | h2 {f['h2']:.2f} wl {f['wl']:.2f} al {f['alpha']} ttr {f['ttr']:.2f} hap {f['hapax']:.2f} zipf {f['zipf']:.2f} "
            f"h2w {f['h2_within']:.2f} h2x {f['h2_cross']:.2f} slot {f['slot']:.2f} | jac {m['jac']:.3f}/{m['jac_null']:.3f} id {m['id_ratio']:.1f}x ed1 {m['ed_ratio']:.1f}x")
def corepass(f):
    return abs(f['h2']-VMS_FP['h2']) <= .3 and abs(f['wl']-VMS_FP['wl']) <= .75 and abs(f['hapax']-VMS_FP['hapax']) <= .07 and abs(f['ttr']-VMS_FP['ttr']) <= .07

# ------------------------------------------------------------------ Voynich reference
vw_str = VWORDS
vwords = [tuple(evaglyphs(w)) for w in vw_str]
Pw = [w for p in vparas for ln in p['lines'] for w in ln]
VREF = dict(); 
vparas_l = [p['lines'] for p in vparas]
rng0 = random.Random(5)
jr, jn = jacc(vparas_l, rng0); ri, ni, re_, ne = neigh(vparas_l, rng0)
VREF.update(jac=jr, jac_null=jn, jac_ratio=jr/jn, id_ratio=ri/ni, ed_ratio=re_/ne, id_rate=ri, ed_rate=re_)
log('VOY fp', {k: round(v, 3) for k, v in VMS_FP.items()})
log('VOY layout: jaccard %.4f shuffle %.4f ratio %.2f | identical nb %.4f null %.4f ratio %.2f | ed1 %.4f null %.4f ratio %.2f | P-words %d tokens(all) %d' % (jr, jn, jr/jn, ri, ni, ri/ni, re_, ne, re_/ne, len(Pw), len(vwords)))
VT1 = t1_metrics(vparas_l); VT2 = t2_metrics(vparas_l)
log('VOY T1', short_t1(VT1)); log('VOY T2', VT2['top4_share_first'], VT2['same4_in_rest'])
log('VOY AB all: n_suf', V_AB_all['n_suf_d24'], 'n_pre', V_AB_all['n_pre_d24'], 'herb n_suf', V_AB_herb['n_suf_d24'])
voy_eval = dict(fp=VMS_FP, T1=dict(fin=round(VT1['fin_rate'], 3), mid=round(VT1['mid_rate'], 3)), T2=dict(first=VT2['top4_share_first'], rest=VT2['same4_in_rest']))
RES['voy'] = dict(fp=VMS_FP, ref=VREF, T1={k: VT1[k] for k in ('M', 'fin_rate', 'mid_rate', 'top_shift', 'stem_att_M', 'stem_att_other')}, T2=VT2, AB_all=V_AB_all, AB_herb=V_AB_herb)

# ------------------------------------------------------------------ G3 slot grammar (fit from Voynich)
END = ['aiin', 'aiir', 'ain', 'air', 'iin', 'iir', 'in', 'ir', 'edy', 'eedy', 'dy', 'eey', 'ey', 'am', 'ar', 'al', 'or', 'ol', 'an', 'y', 's', 'r', 'l', 'm', 'n', 'd', '']
ENDRX = '|'.join(END)
RX = re.compile(r'^(qo|q|o|y|d|s|l|r|)(cth|ckh|cph|cfh|t|k|p|f|)(ch|sh|)(e{0,3})(.*?)(' + ENDRX + r')$')
def parse_word(w):
    m = RX.match(w)
    return m.groups() if m else None
parsed_w = [parse_word(w) for w in vw_str]
parsed_w = [p for p in parsed_w if p]
log('G3 slot parse coverage', len(parsed_w)/len(vw_str))
SLOTN = ['pre', 'gal', 'ch', 'e', 'core', 'end']
def fit_slots(minc=5):
    dist_ = []
    for k in range(6):
        c = collections.Counter(p[k] for p in parsed_w)
        if k == 4: c = collections.Counter({a: b for a, b in c.items() if b >= minc})
        dist_.append(c)
    return dist_
SL = fit_slots()
NPAR_G3 = sum(len(c) for c in SL)
log('G3 slot values:', {n: len(c) for n, c in zip(SLOTN, SL)}, 'total probs', NPAR_G3)
def sampler(counter, rng):
    keys = list(counter); w = [counter[k] for k in keys]
    return lambda: rng.choices(keys, weights=w)[0]
def g3_words(n, seed, joint=False):
    rng = random.Random(seed)
    if joint:
        c1 = collections.Counter((p[0], p[1], p[2]) for p in parsed_w); c2 = collections.Counter((p[3], p[4], p[5]) for p in parsed_w if p[4] in SL[4])
        s1, s2 = sampler(c1, rng), sampler(c2, rng)
        out = []
        while len(out) < n:
            w = ''.join(s1()) + ''.join(s2())
            if w: out.append(tuple(evaglyphs(w)))
        return out
    ss = [sampler(c, rng) for c in SL]
    out = []
    while len(out) < n:
        w = ''.join(s() for s in ss)
        if w: out.append(tuple(evaglyphs(w)))
    return out

# ------------------------------------------------------------------ G1 self-citation
GCLASS = [['k', 't', 'p', 'f', 'cth', 'ckh', 'cph', 'cfh'], ['ch', 'sh'], ['a', 'o', 'e', 'y'], ['i'], ['d', 'l', 'r', 's', 'n', 'm'], ['q']]
GFREQ = collections.Counter(g for w in vwords for g in w)
CLS_OF = {}
for ci, cl in enumerate(GCLASS):
    for g in cl: CLS_OF[g] = ci
for g in GFREQ:
    CLS_OF.setdefault(g, len(GCLASS))
CLASS_MEM = collections.defaultdict(list)
for g, c in CLS_OF.items(): CLASS_MEM[c].append(g)
GLY = [g for g in GFREQ if GFREQ[g]/sum(GFREQ.values()) >= 0.001]; GW = [GFREQ[g] for g in GLY]
LENS = collections.Counter(len(w) for w in vwords)
def pick_in_class(c, rng):
    mem = [g for g in CLASS_MEM[c] if GFREQ[g] > 0] or GLY
    return rng.choices(mem, weights=[GFREQ[g] for g in mem])[0]
def modify(w, rng, pops=(.5, .25, .25)):
    w = list(w); op = rng.choices(['sub', 'ins', 'del'], weights=pops)[0]
    if op == 'del' and len(w) <= 1: op = 'sub'
    if op == 'sub':
        i = rng.randrange(len(w)); w[i] = pick_in_class(CLS_OF[w[i]], rng)
    elif op == 'ins':
        i = rng.randrange(len(w)+1); ref = w[min(i, len(w)-1)]
        w.insert(i, pick_in_class(CLS_OF[ref] if rng.random() < .5 else rng.choice(list(CLASS_MEM)), rng))
    else:
        del w[rng.randrange(len(w))]
    return tuple(w)
def new_seed_word(rng):
    L = rng.choices(list(LENS), weights=list(LENS.values()))[0]
    return tuple(rng.choices(GLY, weights=GW)[0] for _ in range(max(L, 1)))
def g1_words(n, seed, pnew=.03, pm=.85, Wc=30, base=None, pc=1.0):
    """base: callable giving a fresh word (G4) else random seed word. pc = probability to copy (G4)."""
    rng = random.Random(seed); out = [new_seed_word(rng) for _ in range(10)] if base is None else [base() for _ in range(10)]
    while len(out) < n:
        if rng.random() < (pnew if base is None else 1-pc):
            out.append(new_seed_word(rng) if base is None else base())
            continue
        src = out[-1-rng.randrange(min(Wc, len(out)))]
        out.append(modify(src, rng) if rng.random() < pm else src)
    return out[:n]

# ------------------------------------------------------------------ G2 table + grille (Rugg)
def g2_words(n, seed, R=60, steps=(1, 2, 3), pj=0.2):
    rng = random.Random(seed)
    c1 = collections.Counter(p[0]+p[1]+p[2] for p in parsed_w)
    c2 = collections.Counter(p[3]+p[4] for p in parsed_w if p[4] in SL[4]); c3 = collections.Counter(p[5] for p in parsed_w)
    cols = []
    for c in (c1, c2, c3):
        s = sampler(c, rng); cols.append([s() for _ in range(R)])
    pos = [rng.randrange(R) for _ in range(3)]; out = []
    while len(out) < n:
        w = cols[0][pos[0]] + cols[1][pos[1]] + cols[2][pos[2]]
        if w: out.append(tuple(evaglyphs(w)))
        if rng.random() < pj: pos = [rng.randrange(R) for _ in range(3)]
        else: pos = [(p+s) % R for p, s in zip(pos, steps)]
    return out

# ------------------------------------------------------------------ run
RESULTS = {}
def run(name, fn, seeds, params, npar):
    t0 = time.time(); ms = []
    for s in seeds:
        ws = fn(NT, s); ms.append(evaluate(ws, vref=VREF))
    avg = lambda f: float(np.mean([f(m) for m in ms]))
    agg = dict(name=name, params=params, npar=npar, d10=avg(lambda m: m['d10']), d13=avg(lambda m: m['d13']),
               fp={k: avg(lambda m, k=k: m['fp'][k]) for k in KEYS}, jac=avg(lambda m: m['jac']), jac_null=avg(lambda m: m['jac_null']),
               jac_ratio=avg(lambda m: m['jac_ratio']), id_ratio=avg(lambda m: m['id_ratio']), ed_ratio=avg(lambda m: m['ed_ratio']),
               corepass=all(corepass(m['fp']) for m in ms), T1=ms[0]['T1'], T2=ms[0]['T2'], T3=ms[0]['T3'], nseeds=len(seeds))
    RESULTS.setdefault(name.split(' ')[0], []).append(agg)
    log(f"{name:<40} d10 {agg['d10']:.2f} d13 {agg['d13']:.2f} | h2 {agg['fp']['h2']:.2f} wl {agg['fp']['wl']:.2f} al {agg['fp']['alpha']:.0f} ttr {agg['fp']['ttr']:.2f} hap {agg['fp']['hapax']:.2f} zipf {agg['fp']['zipf']:.2f} h2w {agg['fp']['h2_within']:.2f} h2x {agg['fp']['h2_cross']:.2f} | jac {agg['jac']:.3f}/{agg['jac_null']:.3f} id {agg['id_ratio']:.1f}x ed1 {agg['ed_ratio']:.1f}x | pass {agg['corepass']} | T1 {agg['T1']['fin']}/{agg['T1']['mid']} T2 {agg['T2']['first']}/{agg['T2']['rest']} T3 null {agg['T3']['null_suf']} drift {agg['T3']['drift_suf']}/{agg['T3']['drift_pre']} ({time.time()-t0:.0f}s)")
    return agg

vm = evaluate(vwords[:NT], vref=VREF); log('VOY (35k tokens, same evaluate)', short(vm), vm['T1'], vm['T2'], vm['T3'])
RES['voy_eval'] = vm
BEST = dict(pv=0.5, L=0, ends=False, short=True)
ptxt = load_lines([1000]); itw = [w for p in ptxt for ln in p for w in ln][:NTOK]
enc = Enc(itw, BEST, 11, 11, 2)
k1w = [enc.word(w) for w in itw]
k1m = evaluate(k1w, vref=VREF, chars=False); log('K1 E3 Italian', short(k1m), k1m['T1'], k1m['T2'], k1m['T3'])
RES['k1'] = k1m

S3 = [1, 2, 3]
log('--- G3 slot sampler'); run('G3 slot-iid', lambda n, s: g3_words(n, s), S3, 'none', NPAR_G3)
run('G3j joint-slot-iid', lambda n, s: g3_words(n, s, True), S3, 'none', len(set((p[0], p[1], p[2]) for p in parsed_w)) + len(set((p[3], p[4], p[5]) for p in parsed_w if p[4] in SL[4])))
log('--- G1 self-citation grid')
for pnew in (.01, .04):
    for pm in (.6, .85, 1.0):
        for Wc in (12, 40, 150):
            run(f'G1 pnew{pnew} pm{pm} W{Wc}', lambda n, s, a=pnew, b=pm, c=Wc: g1_words(n, s, a, b, c), [1], dict(pnew=pnew, pm=pm, W=Wc), 5)
log('--- G2 table+grille grid')
for R in (30, 60, 120, 250):
    for steps in ((1, 2, 3), (1, 5, 11)):
        for pj in (0.0, .3, 1.0):
            run(f'G2 R{R} st{steps[0]}-{steps[1]}-{steps[2]} pj{pj}', lambda n, s, R=R, st=steps, pj=pj: g2_words(n, s, R, st, pj), [1], dict(R=R, steps=steps, pj=pj), 6)
log('--- G4 slot sampler + local copy grid')
def g4(n, s, pc, pm, Wc, joint=False):
    b_ = g3_words(n + 50, s + 7, joint); it = iter(b_)
    return g1_words(n, s, pnew=0, pm=pm, Wc=Wc, base=lambda: next(it), pc=pc)
for pc in (.3, .6, .85):
    for pm in (.6, 1.0):
        for Wc in (12, 40):
            run(f'G4 pc{pc} pm{pm} W{Wc}', lambda n, s, pc=pc, pm=pm, Wc=Wc: g4(n, s, pc, pm, Wc), [1], dict(pc=pc, pm=pm, W=Wc), NPAR_G3 + 3)

log('--- G4j: joint-slot base + local copy')
for pc in (.15, .3, .45):
    for pm in (.8, 1.0):
        for Wc in (12, 25, 60):
            run(f'G4j pc{pc} pm{pm} W{Wc}', lambda n, s, pc=pc, pm=pm, Wc=Wc: g4(n, s, pc, pm, Wc, True), [1], dict(pc=pc, pm=pm, W=Wc), 600)
best = {fam: min(lst, key=lambda a: a['d13']) for fam, lst in RESULTS.items() if fam in ('G1', 'G2', 'G4', 'G4j')}
log('--- best per family (single seed) -> rerun 3 seeds')
FINAL = {}
for fam, b in best.items():
    p = b['params']
    if fam == 'G1': fn = lambda n, s, p=p: g1_words(n, s, p['pnew'], p['pm'], p['W'])
    elif fam == 'G2': fn = lambda n, s, p=p: g2_words(n, s, p['R'], p['steps'], p['pj'])
    else: fn = lambda n, s, p=p, j=(fam == 'G4j'): g4(n, s, p['pc'], p['pm'], p['W'], j)
    FINAL[fam] = run(f'{fam}-BEST3 {p}', fn, [11, 12, 13], p, b['npar'])
FINAL['G3'] = RESULTS['G3'][0]; FINAL['G3j'] = RESULTS['G3j'][0]
RES['all'] = RESULTS; RES['final'] = FINAL
json.dump(RES, open(outjson, 'w'), default=str)
log('DONE')
