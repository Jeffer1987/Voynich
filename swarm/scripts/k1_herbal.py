"""Wave 5A: K1 on medieval/technical Latin herbal sources. Reuses k1_sim.py definitions via exec (k1_sim.py not modified).
usage: python -I k1_herbal.py parsed_zl3b.json herbal_dir classical_dir out.json [quick]"""
import sys, json, re, unicodedata, os, random, collections
parsed, hdir, cdir, outjson = sys.argv[1:5]
quick = len(sys.argv) > 5
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'k1_sim.py'), encoding='utf-8').read()
src = src[:src.index('d = json.load(open(parsed))')]
ns = {'__name__': 'k1'}
sys.argv = ['k1_sim.py', parsed, cdir, outjson]
exec(compile(src, 'k1_sim.py', 'exec'), ns)
fingerprint, dist, enc_E3, run_E5 = ns['fingerprint'], ns['dist'], ns['enc_E3'], ns['run_E5']
ABBRS = [dict(pv=pv, L=L, ends=e, short=sh) for pv in (0.0, 0.5, 0.9, 1.0) for L in (0, 3, 4, 6) for e in (False, True) for sh in (False, True)]


def tok(f, words):
    try: m = f()
    except ValueError: return None
    return [m[w] for w in words]

abbreviate, KEYS = ns['abbreviate'], ns['KEYS']
C = collections


def clean(raw):
    t = re.sub(r'\{\{[^}]*\}\}', ' ', raw)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'==[^=\n]*==', ' ', t)
    t = re.sub(r'\d+\.\d+[A-D]?\|', ' ', t)
    t = re.sub(r'\bp\.[IVXL]+\b', ' ', t)
    t = unicodedata.normalize('NFD', t.lower().replace('ß', 'ss').replace('æ', 'ae').replace('œ', 'oe'))
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = t.replace('j', 'i').replace('v', 'u').replace('k', 'c')
    return re.findall(r'[a-z]+', t)


def loadcls(ids):
    txt = ''
    for i in ids:
        t = open(os.path.join(cdir, f'pg{i}.txt'), encoding='utf-8', errors='replace').read()
        a = t.find('*** START'); a = t.find('\n', a); b = t.find('*** END'); txt += '\n' + t[a:b]
    return clean(txt)


S = {}
for name, f in [('Macer', 'macer.raw'), ('Hortulus', 'hortulus.raw'), ('Apicius', 'apicius.raw')]:
    S[name] = clean(open(os.path.join(hdir, f), encoding='utf-8', errors='replace').read())
S['HerbMix'] = S['Macer'] + S['Hortulus'] + S['Apicius']
S['Caesar'] = loadcls([218, 18837])
S['Dante'] = loadcls([1000])

d = json.load(open(parsed))
ok = lambda w: w and re.fullmatch(r'[a-z]+', w)
vall = [w for l in d for w in l['words'] if ok(w)]
vherb = [w for l in d if l['I'] == 'H' and l['L'] == 'A' for w in l['words'] if ok(w)]
vherbB = [w for l in d if l['I'] == 'H' and l['L'] == 'B' for w in l['words'] if ok(w)]
print({k: len(v) for k, v in S.items()}, 'V all', len(vall), 'V herbal A', len(vherb), 'V herbal B', len(vherbB))
for k in ['Macer', 'Hortulus', 'Apicius']:
    print(k, C.Counter(S[k]).most_common(12))

fmt = lambda f: {k: round(v, 2) for k, v in f.items()}
N1, N2 = 13000, 30000
out = dict(sizes={k: len(v) for k, v in S.items()})


def fp_at(words, n):
    ns['NTOK'] = n
    return fingerprint([tuple(w) for w in words[:n]])


rawfp = {}
for n, names in [(N1, ['Macer', 'Hortulus', 'Apicius', 'Caesar', 'Dante']), (N2, ['HerbMix', 'Caesar', 'Dante'])]:
    rawfp[n] = {'VMS_all': fp_at(vall, n)}
    for nm in names:
        rawfp[n][nm] = fp_at(S[nm], n)
nh = len(vherb)
rawfp['herbA'] = {'VMS_herbA': fp_at(vherb, nh), 'VMS_all_same_n': fp_at(vall, nh)}
for nm in ['Macer', 'Apicius', 'HerbMix', 'Caesar', 'Dante']:
    rawfp['herbA'][nm + '_same_n'] = fp_at(S[nm], min(nh, len(S[nm])))
rr = random.Random(5); ws = []
for _ in range(10):
    s = rr.randrange(0, len(vall) - N1); ws.append(fp_at(vall[s:s + N1], N1))
rawfp['vms_windows'] = {k: [round(x[k], 3) for x in ws] for k in ['hapax', 'ttr', 'wl', 'h2']}
out['rawfp'] = rawfp
for k, v in rawfp.items():
    print('\n##', k)
    if k == 'vms_windows':
        print(v); continue
    for nm, f in v.items():
        print(f'{nm:18s}', fmt(f))


def run_all(name, words, n, tgt):
    ns['NTOK'] = n; words = words[:n]
    res = []

    def rec(fam, params, toks):
        if toks is None: return
        fp = fingerprint(toks); s, z = dist(fp, tgt)
        core = (abs(fp['h2'] - tgt['h2']) <= .3 and abs(fp['wl'] - tgt['wl']) <= .75 and abs(fp['hapax'] - tgt['hapax']) <= .07 and abs(fp['ttr'] - tgt['ttr']) <= .07)
        strict = core and all(abs(z[k]) <= 2 for k in KEYS)
        res.append(dict(src=name, fam=fam, params=params, score=s, core=core, strict=strict, fp=fp, z=z))
    SEEDS = [1] if quick else [1, 2, 3]
    ab_list = ABBRS[::5] if quick else ABBRS
    for ab in ab_list:
        for (a, b) in [(5, 5), (6, 4), (8, 4), (11, 11)]:
            for sd in SEEDS[:2]:
                rec('E3', dict(ab=ab, a=a, b=b, seed=sd), tok(lambda: enc_E3(words, a, b, sd, ab), words))
    for (a, b) in [(6, 6), (8, 8), (11, 11)]:
        for nbig in (0, 10, 30):
            for nhom in (0, 20, 60):
                rec('E5', dict(a=a, b=b, nbig=nbig, nhom=nhom), run_E5(words, a, b, nbig, nhom, 1))

    def enc_E7(G, m, seed, abbr):
        types = set(words); ab = {w: abbreviate(w, abbr) for w in types}
        cnt = C.Counter(); tc = C.Counter(words)
        for w, v in ab.items():
            for c in v: cnt[c] += tc[w]
        syms = [c for c, _ in cnt.most_common()]
        r = random.Random(seed); glyphs = [f'g{i}' for i in range(G)]
        mm = min(m, G, len(syms)); g1 = glyphs[:]; r.shuffle(g1)
        cells = [(x, y) for x in glyphs for y in glyphs]; r.shuffle(cells)
        if len(cells) < len(syms) - mm: raise ValueError('small')
        code = {s_: (g,) for s_, g in zip(syms[:mm], g1)}
        code.update({s_: c for s_, c in zip(syms[mm:], cells)})
        return {w: tuple(g for c in ab[w] for g in code[c]) for w in types}
    rs_ = random.Random(99)
    for _ in range(40 if quick else 450):
        ab = dict(pv=rs_.choice([0, .3, .6, .8, .9, 1.0]), L=rs_.choice([0, 3, 4, 5, 6]), ends=rs_.random() < .5, short=rs_.random() < .5)
        G = rs_.choice([10, 14, 18, 22]); m = rs_.choice([0, 4, 8, 12, 16, 22]); sd = rs_.choice([1, 2, 3, 4])
        rec('E7', dict(ab=ab, G=G, m=m, seed=sd), tok(lambda: enc_E7(G, m, sd, ab), words))
    return res


runs = [('Macer', N1, 'all'), ('Apicius', N1, 'all'), ('HerbMix', N2, 'all'), ('Macer', N1, 'herbA')]
allres = []
for name, n, tgtname in runs:
    words = S[name]
    tgt = fp_at(vall, n) if tgtname == 'all' else fp_at(vherb, min(n, len(vherb)))
    res = run_all(name, words, n, tgt)
    for r in res: r['tgt'] = tgtname
    allres += res
    print(f'\n=== {name} n={n} target={tgtname} (VMS hapax {tgt["hapax"]:.2f} h2 {tgt["h2"]:.2f} wl {tgt["wl"]:.2f} ttr {tgt["ttr"]:.2f}); configs {len(res)}; core-pass {sum(r["core"] for r in res)}; strict {sum(r["strict"] for r in res)}')
    print('max hapax over all configs', round(max(r['fp']['hapax'] for r in res), 3), '; plain', round(fp_at(words, n)['hapax'], 3))
    for fam in ['E3', 'E5', 'E7']:
        rs = sorted([r for r in res if r['fam'] == fam], key=lambda r: r['score'])
        for r in rs[:2]: print(fam, round(r['score'], 2), r['core'], json.dumps(r['params']), fmt(r['fp']))
    for r in sorted([r for r in res if r['core']], key=lambda r: r['score'])[:3]:
        print('CORE', r['fam'], round(r['score'], 2), json.dumps(r['params']), fmt(r['fp']))
out['results'] = allres
json.dump(out, open(outjson, 'w'), indent=1)
