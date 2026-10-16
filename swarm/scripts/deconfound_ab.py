"""Wave 4B: deconfound Currier language / Davis hand / section.
Run: python -I deconfound_ab.py <parsed_zl3b.json>"""
import json, sys, math, collections
import numpy as np
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

np.random.seed(1)
MINTOK = int(sys.argv[2]) if len(sys.argv) > 2 else 80
d = json.load(open(sys.argv[1]))
order = []
P = {}
for r in d:
    f = r['folio']
    if f not in P:
        order.append(f)
        P[f] = dict(f=f, I=r['I'], L=r['L'], H=r['H'], Q=r['Q'], lines=[])
    if r['ltype'] == 'P' and r['words']:
        P[f]['lines'].append((r['words'], r['pstart']))
pages = []
for i, f in enumerate(order):
    p = P[f]
    p['idx'] = i
    p['toks'] = [w for ws, _ in p['lines'] for w in ws]
    if len(p['toks']) >= MINTOK and p['H'] != '@':
        pages.append(p)
print("pages>=MINTOK tokens:", len(pages), "of", len(order))


def ent2(toks):
    c = collections.Counter()
    a = collections.Counter()
    for w in toks:
        s = '^' + w + '$'
        for x, y in zip(s, s[1:]):
            c[(x, y)] += 1
            a[x] += 1
    n = sum(c.values())
    return -sum(v / n * math.log2(v / a[k[0]]) for k, v in c.items())


GAL = set('ktpf')


def feats(p):
    t = p['toks']
    n = len(t)

    def fr(fn):
        return sum(1 for w in t if fn(w)) / n
    lf = [ws[-1] for ws, _ in p['lines']]
    ps = [ws[0] for ws, st in p['lines'] if st]
    return dict(h2=ent2(t), wlen=sum(map(len, t)) / n,
                qo=fr(lambda w: w.startswith('qo')), ch=fr(lambda w: w.startswith('ch')),
                sh=fr(lambda w: w.startswith('sh')),
                edy=fr(lambda w: w.endswith('edy')), aiin=fr(lambda w: w.endswith('aiin')),
                ol=fr(lambda w: w.endswith('ol')), dy=fr(lambda w: w.endswith('dy')),
                final_m=(sum(w.endswith('m') for w in lf) / len(lf)) if lf else np.nan,
                par_gal=(sum(w[0] in GAL for w in ps) / len(ps)) if len(ps) >= 2 else np.nan,
                ttr=len(set(t)) / n)


for p in pages:
    p['F'] = feats(p)
FN = list(pages[0]['F'])


def sel(**kw):
    return [p for p in pages if all((p[k] in v) if isinstance(v, set) else p[k] == v for k, v in kw.items())]


def perm(A, B, fn, nperm=5000):
    xa = np.array([p['F'][fn] for p in A])
    xb = np.array([p['F'][fn] for p in B])
    xa = xa[~np.isnan(xa)]
    xb = xb[~np.isnan(xb)]
    if len(xa) < 2 or len(xb) < 2:
        return None
    obs = xa.mean() - xb.mean()
    allx = np.concatenate([xa, xb])
    k = len(xa)
    c = 0
    for _ in range(nperm):
        np.random.shuffle(allx)
        if abs(allx[:k].mean() - allx[k:].mean()) >= abs(obs) - 1e-12:
            c += 1
    sd = math.sqrt((xa.var(ddof=1) + xb.var(ddof=1)) / 2)
    return xa.mean(), xb.mean(), obs / sd if sd else 0, (c + 1) / (nperm + 1)


out = []


def cmp(title, A, B, la, lb):
    out.append(f"\n### {title}  (n {la}={len(A)}, {lb}={len(B)})")
    out.append("| feat | " + la + " | " + lb + " | d | p |\n|---|---|---|---|---|")
    for fn in FN:
        r = perm(A, B, fn)
        if r:
            out.append(f"| {fn} | {r[0]:.3f} | {r[1]:.3f} | {r[2]:+.2f} | {r[3]:.4f} |")


ct = collections.Counter((p['I'], p['L'], p['H']) for p in P.values())
out.append("crosstab (section,lang,hand): " + str(sorted(ct.items(), key=lambda x: -x[1])))
out.append("\n## T1/T2 fixed-factor comparisons (page-level permutation, 5000)")
cmp("herbal: hand1(A) vs hand2(B) [hand+lang vary, section fixed]", sel(I='H', H='1'), sel(I='H', H='2'), 'H1A', 'H2B')
cmp("herbal, lang B fixed: hand2 vs hand3", sel(I='H', H='2'), sel(I='H', H='3', L='B'), 'H2', 'H3')
cmp("herbal, lang B fixed: hand2 vs hand5", sel(I='H', H='2'), sel(I='H', H='5'), 'H2', 'H5')
cmp("hand2/B fixed: herbal vs biological", sel(I='H', H='2'), sel(I='B', H='2'), 'herb', 'bio')
cmp("hand1/A fixed: herbal vs pharma", sel(I='H', H='1'), sel(I='P', H='1'), 'herb', 'pharma')
cmp("hand3 stars fixed: lang A vs B", sel(I='S', H='3', L='A'), sel(I='S', H='3', L='B'), 'A', 'B')
cmp("lang B fixed: bio(h2) vs stars(h3) [section+hand vary]", sel(I='B', H='2'), sel(I='S', H='3', L='B'), 'bio-h2', 'star-h3')


def vec(p):
    c = collections.Counter()
    for w in p['toks']:
        s = '^' + w + '$'
        for x, y in zip(s, s[1:]):
            c['bg_' + x + y] += 1
    return c


VOC = None


def build(ps, top=300):
    global VOC
    tot = collections.Counter()
    vs = [vec(p) for p in ps]
    for v in vs:
        tot.update(v)
    VOC = [k for k, _ in tot.most_common(top)]
    return np.array([[v[k] for k in VOC] for v in vs], float)


def lopo(ps, labels, model):
    X = build(ps)
    y = np.array(labels)
    pred = []
    Z = X / X.sum(1, keepdims=True)
    for i in range(len(ps)):
        tr = np.arange(len(ps)) != i
        if len(set(y[tr])) < 2:
            pred.append(y[tr][0])
            continue
        if model == 'nb':
            m = MultinomialNB(alpha=0.5).fit(X[tr], y[tr])
            pred.append(m.predict(X[i:i + 1])[0])
        else:
            m = LogisticRegression(C=30, max_iter=3000).fit(Z[tr], y[tr])
            pred.append(m.predict(Z[i:i + 1])[0])
    return np.array(pred), y


def report(title, ps, labels):
    out.append(f"\n**{title}** (n={len(ps)})")
    for model in ('nb', 'lr'):
        pr, y = lopo(ps, labels, model)
        acc = (pr == y).mean()
        maj = max(collections.Counter(y).values()) / len(y)
        cls = sorted(set(y))
        bal = np.mean([(pr[y == c] == c).mean() for c in cls])
        cm = {c: dict(collections.Counter(pr[y == c])) for c in cls}
        out.append(f"- {model}: acc {acc:.2f} (majority {maj:.2f}), balanced {bal:.2f}; true->pred {cm}")


def SEC(p):
    return p['I'] if p['I'] in ('H', 'B', 'S', 'P') else 'other'


out.append("\n## T3 classifiers (leave-one-page-out, 300 most frequent glyph bigrams)")
known = [p for p in pages if p['L'] in ('A', 'B')]
report("Overall hand", pages, [p['H'] for p in pages])
report("Overall language A/B", known, [p['L'] for p in known])
report("Overall section (H,B,S,P,other)", pages, [SEC(p) for p in pages])
out.append("\n### Conditioned")
s = sel(I='H', L='B')
report("hand | herbal & lang B (hands 2,3,5)", s, [p['H'] for p in s])
s = sel(I='H', H={'1', '2'})
report("hand 1 vs 2 | herbal (language co-varies)", s, [p['H'] for p in s])
s = sel(H='2', L='B', I={'H', 'B'})
report("section | hand 2 & lang B (herbal vs bio)", s, [p['I'] for p in s])
s = sel(H='1', L='A', I={'H', 'P'})
report("section | hand 1 & lang A (herbal vs pharma)", s, [p['I'] for p in s])
s = sel(I='S', H='3')
report("lang | hand 3 & stars (A vs B)", s, [p['L'] for p in s])
s = [p for p in pages if p['L'] == 'B' and p['I'] in ('H', 'B', 'S') and p['H'] in ('2', '3')]
report("hand (2 vs 3) | lang B, section H/B/S", s, [p['H'] for p in s])
s = [p for p in pages if p['L'] == 'B' and p['I'] in ('H', 'B', 'S')]
report("section | lang B (H,B,S; hands vary)", s, [p['I'] for p in s])

out.append("\n### Transfer tests")


def transfer(name, trp, trl, tep, tel):
    X = build(trp + tep)
    m = MultinomialNB(alpha=0.5).fit(X[:len(trp)], trl)
    pr = m.predict(X[len(trp):])
    out.append(f"- {name}: acc {(pr == np.array(tel)).mean():.2f} {dict(collections.Counter(zip(tel, pr)))}")


tr = sel(I='H', H={'1', '2'})
a = sel(I='P', H='1')
b = sel(I='B', H='2')
transfer("train hand1 vs hand2 on herbal -> test pharma(h1) + bio(h2)", tr, [p['H'] for p in tr], a + b, ['1'] * len(a) + ['2'] * len(b))
tr = sel(H='2', I={'H', 'B'})
te = sel(H='1', I={'H', 'P'})
transfer("train herbal-vs-bio in hand2 -> test herbal-vs-pharma in hand1 (H vs N)", tr, ['H' if p['I'] == 'H' else 'N' for p in tr], te, ['H' if p['I'] == 'H' else 'N' for p in te])

out.append("\n## T4 drift: Spearman rho of feature vs folio order")


def drift(title, ps):
    ps = sorted(ps, key=lambda p: p['idx'])
    row = []
    for fn in FN:
        x = [(p['idx'], p['F'][fn]) for p in ps if not np.isnan(p['F'][fn])]
        if len(x) < 8:
            continue
        r, pv = spearmanr(*zip(*x))
        row.append(f"{fn} {r:+.2f}(p={pv:.3f})")
    out.append(f"- {title} n={len(ps)}: " + "; ".join(row))


drift("hand1 all", sel(H='1'))
drift("hand1 herbal", sel(H='1', I='H'))
drift("hand2 all", sel(H='2'))
drift("hand2 herbal", sel(H='2', I='H'))
drift("all pages", pages)

X = build(pages)
Z = X / X.sum(1, keepdims=True)
kn = [i for i, p in enumerate(pages) if p['L'] in ('A', 'B')]
fold = np.arange(len(kn)) % 10
np.random.shuffle(fold)
sc = np.zeros(len(pages))
lab = lambda i: 1 if pages[i]['L'] == 'B' else 0
for f in range(10):
    trn = [kn[j] for j in range(len(kn)) if fold[j] != f]
    tst = [kn[j] for j in range(len(kn)) if fold[j] == f]
    m = LogisticRegression(C=30, max_iter=3000).fit(Z[trn], [lab(i) for i in trn])
    sc[tst] = m.decision_function(Z[tst])
m = LogisticRegression(C=30, max_iter=3000).fit(Z[kn], [lab(i) for i in kn])
kns = set(kn)
unk = [i for i in range(len(pages)) if i not in kns]
if unk:
    sc[unk] = m.decision_function(Z[unk])
out.append("\n### A/B axis score (out-of-fold logistic; higher = more B), by group: mean [min,max] n")
groups = collections.defaultdict(list)
for i, p in enumerate(pages):
    groups[(p['L'] or '?', p['H'], p['I'])].append(sc[i])
for k, v in sorted(groups.items(), key=lambda x: -len(x[1])):
    if len(v) >= 3:
        out.append(f"- lang {k[0]} hand {k[1]} sect {k[2]}: {np.mean(v):+.2f} [{min(v):+.2f},{max(v):+.2f}] n={len(v)}")
A = sc[[i for i in kn if pages[i]['L'] == 'A']]
B = sc[[i for i in kn if pages[i]['L'] == 'B']]
out.append(f"- overlap: A pages above B 5th pct {(A > np.percentile(B, 5)).mean():.2f}; B pages below A 95th pct {(B < np.percentile(A, 95)).mean():.2f}")
h = np.histogram(sc, bins=10)
out.append(f"- score histogram (all pages) {h[0].tolist()} edges {np.round(h[1], 1).tolist()}")
for name, cond in (("hand 1", lambda p: p['H'] == '1'), ("hand 2", lambda p: p['H'] == '2'),
                   ("hand 1 herbal", lambda p: p['H'] == '1' and p['I'] == 'H'),
                   ("hand 2 herbal", lambda p: p['H'] == '2' and p['I'] == 'H')):
    ii = [i for i, p in enumerate(pages) if cond(p)]
    r, pv = spearmanr([pages[i]['idx'] for i in ii], sc[ii])
    out.append(f"- axis score vs folio order, {name}: rho {r:+.2f} p={pv:.3g} n={len(ii)}")
# unlabeled-page placement
ul = [(pages[i]['f'], pages[i]['H'], pages[i]['I'], round(sc[i], 2)) for i in unk]
out.append(f"- unlabelled-language pages (folio,hand,sect,score): {ul}")
print("\n".join(out))
