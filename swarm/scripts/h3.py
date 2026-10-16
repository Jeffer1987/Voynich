import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np,collections as C
from h23_common import *
name=sys.argv[1]; B=int(sys.argv[2]) if len(sys.argv)>2 else 1000
mode='at' if name=='rf1b' else 'marker'
d=load(name,mode); W=words(d)
rng=np.random.default_rng(3)
P=[x for x in W if x['ty']=='P']
first=[x for x in P if x['pf'] and x['pos']==1]
lnstart=[x for x in P if (not x['pf']) and x['pos']==1]
midw=[x for x in P if x['pos']>1 and x['pos']<x['n']]
isg=lambda s:s[0] in GAL
rate=lambda xs:np.mean([isg(x['w']) for x in xs])
print('=== %s : paragraph-first words %d, later-line-initial %d, mid-line %d'%(name,len(first),len(lnstart),len(midw)))
print('gallows-initial rate: para-first %.3f | later line-initial %.3f | mid-line %.3f | line-final %.3f'%(rate(first),rate(lnstart),rate(midw),rate([x for x in P if x['pos']==x['n'] and x['n']>1])))
# permutation null: shuffle words within folio over P-lines, rate in para-first slots
fol=np.unique([x['folio'] for x in P],return_inverse=True)[1]
g=np.array([isg(x['w']) for x in P]);pfs=np.array([x['pf'] and x['pos']==1 for x in P])
nul=np.array([g[np.lexsort((rng.random(len(P)),fol))][pfs].mean() for _ in range(B)])
print('null para-first slot rate %.3f +- %.3f ; obs %.3f ; z=%.0f ; p<%.4f'%(nul.mean(),nul.std(),g[pfs].mean(),(g[pfs].mean()-nul.mean())/nul.std(),1/(B+1)))
# strata
print('\n### strata: para-first gallows-initial rate (n) vs mid-line rate')
def st(key,vals):
    for v in vals:
        f=[x for x in first if x[key]==v]; m=[x for x in midw if x[key]==v]
        if len(f)>=15: print('| %s=%s | %d | %.3f | %.3f |'%(key,v,len(f),rate(f),rate(m)))
st('L',['A','B']);st('H',['1','2','3','4']);st('I',['H','S','B','P','C','Z','T','A'])
if name!='rf1b':
    f1=[x for x in first if d[x['li']]['lt']=='@'];f2=[x for x in first if d[x['li']]['lt']!='@']
    print('| page-first paragraph (@P) | %d | %.3f |'%(len(f1),rate(f1)));print('| later paragraph on page (+P with <%%>) | %d | %.3f |'%(len(f2),rate(f2)))
# H3a position profile
print('\n### H3a: gallows-initial rate by word position, para-first line vs later lines (n>=8 word lines)')
for lab,sel in [('line1',lambda x:x['pf']),('line2',lambda x:x['pli']==1),('line3+',lambda x:(x['pli'] or 0)>=2)]:
    r=[]
    for j in range(1,9):
        xs=[x for x in P if sel(x) and x['pos']==j and x['n']>=8]; r.append('%.3f'%rate(xs) if xs else 'na')
    print('| %s | %s |'%(lab,' '.join(r)))
anyg=lambda s:any(c in GAL for c in s)
print('\nany-gallows-in-word rate & gallows letters per char (excluding word 1):')
for lab,sel in [('line1',lambda x:x['pf']),('line2',lambda x:x['pli']==1),('line3+',lambda x:(x['pli'] or 0)>=2)]:
    xs=[x for x in P if sel(x) and x['pos']>1]
    nch=sum(len(x['w']) for x in xs);ng=sum(sum(c in GAL for c in x['w']) for x in xs)
    print('| %s | words %d | any-gallows %.3f | gallows/char %.4f | gallows-initial %.3f |'%(lab,len(xs),np.mean([anyg(x['w']) for x in xs]),ng/nch,rate(xs)))
# gallows at 2nd glyph in first word vs others
gl2=lambda s:(len(glyphs(s))>1 and glyphs(s)[1][0] in GAL) or (len(glyphs(s))>1 and glyphs(s)[1] in ('cth','ckh','cph','cfh'))
print('first-word: gallows 2nd glyph %.3f | mid-line words %.3f | later-line-initial %.3f'%(np.mean([gl2(x['w']) for x in first]),np.mean([gl2(x['w']) for x in midw]),np.mean([gl2(x['w']) for x in lnstart])))
print('first-word (not gallows-initial, n=%d) any-gallows later in word: %.3f ; mid %.3f'%(sum(not isg(x['w']) for x in first),np.mean([anyg(x['w']) for x in first if not isg(x['w'])]),np.mean([anyg(x['w']) for x in midw if not isg(x['w'])])))
# non-gallows para-first words: what are they?
ng_first=C.Counter(x['w'][0] for x in first if not isg(x['w']))
print('non-gallows para-first words initial letters:',ng_first.most_common(8))
print('second word of para-first line: y/d initial %.3f (later-line pos2 %.3f) ; gallows-initial %.3f'%(
    np.mean([x['w'][0] in 'yd' for x in P if x['pf'] and x['pos']==2]),np.mean([x['w'][0] in 'yd' for x in P if (not x['pf']) and x['pos']==2]),rate([x for x in P if x['pf'] and x['pos']==2])))
# H3c
print('\n### H3c: initial glyph distribution among gallows-initial words (k,t,p,f + benched forms)')
def gdist(xs):
    c=C.Counter()
    for x in xs:
        gs=glyphs(x['w'])[0]
        if gs in ('cth','ckh','cph','cfh'): c['b'+gs[1]]+=1
        elif gs in GAL: c[gs]+=1
    return c
for lab,xs in [('para-first',first),('later line-initial',lnstart),('mid-line',midw)]:
    c=gdist(xs);tot=sum(c.values())
    print('| %s | n_words %d | '%(lab,len(xs))+' '.join('%s %.3f'%(k,c[k]/len(xs)) for k in ['k','t','p','f','bk','bt','bp','bf'])+' | share of simple gallows: '+' '.join('%s %.2f'%(k,c[k]/max(1,sum(c[j] for j in 'ktpf'))) for k in 'ktpf')+' |')
for key,vals in [('L',['A','B']),('I',['H','S','B','P','C','Z','T','A'])]:
    for v in vals:
        f=[x for x in first if x[key]==v]
        if len(f)>=15:
            c=gdist(f);t=max(1,sum(c[j] for j in 'ktpf'));print('| para-first %s=%s | %d | share k %.2f t %.2f p %.2f f %.2f |'%(key,v,len(f),c['k']/t,c['t']/t,c['p']/t,c['f']/t))
# chi2 permutation: para-first vs mid distribution of first simple-gallows letter
def chi(codes,msk,K=5):
    a=np.bincount(codes[msk],minlength=K);b=np.bincount(codes[~msk&Pmask],minlength=K)
    return a,b
codes=np.array(['ktpf'.index(x['w'][0])+1 if isg(x['w']) else 0 for x in P])
Pmask=np.ones(len(P),bool)
gm=codes>0
a=np.bincount(codes[pfs&gm],minlength=5)[1:];b=np.bincount(codes[(~pfs)&gm],minlength=5)[1:]
def c2(a,b):
    ea=a.sum()*(a+b)/(a+b).sum();return (((a-ea)**2)/np.maximum(ea,1e-9)).sum()
obs=c2(a,b);nulc=[]
for _ in range(B):
    o=np.lexsort((rng.random(len(P)),fol));cc=codes[o];gm2=cc>0
    nulc.append(c2(np.bincount(cc[pfs&gm2],minlength=5)[1:],np.bincount(cc[(~pfs)&gm2],minlength=5)[1:]))
nulc=np.array(nulc)
print('letter-mix chi2 para-first vs rest (gallows-initial only): obs %.1f null mean %.1f sd %.1f p=%.4f'%(obs,nulc.mean(),nulc.std(),(1+(nulc>=obs).sum())/(B+1)))
# H3b stripping
print('\n### H3b stripping')
ref=C.Counter()
fset=set(id(x) for x in first)
for x in P:
    if id(x) not in fset: ref[x['w']]+=1
# also whole corpus incl labels as alt ref
def strip_first(s):
    g=glyphs(s); return ''.join(g[1:])
def match(r,thr): return len(r)>0 and ref.get(r,0)>=thr
def evalset(ws,lab,fn=strip_first):
    rs=[fn(s) for s in ws]
    m1=np.mean([match(r,1) for r in rs]);m5=np.mean([match(r,5) for r in rs]);mf=np.mean([np.log10(ref.get(r,0)+1) for r in rs])
    return m1,m5,mf
fw=[x['w'] for x in first if isg(x['w'])]
print('stripped para-first gallows words n=%d'%len(fw))
r_first=evalset(fw,'first')
# null A: random mid-line words (any), strip random-length... strip first glyph
midws=[x['w'] for x in midw];mgal=[x['w'] for x in midw+lnstart if isg(x['w'])]
def sample(pool,k,B_):
    return [list(rng.choice(pool,k)) for _ in range(B_)]
# length-matched null for A
bylen=C.defaultdict(list)
for s in midws: bylen[len(s)].append(s)
lens=[len(s) for s in fw]
res={'A random word, strip 1st glyph (len-matched)':[], 'B mid/line-initial gallows word, strip gallows (len-matched)':[], 'C random word, strip a random glyph (len-matched)':[]}
bygal=C.defaultdict(list)
for s in mgal: bygal[len(s)].append(s)
for _ in range(300):
    ws=[bylen[l][rng.integers(len(bylen[l]))] for l in lens if bylen[l]]
    res['A random word, strip 1st glyph (len-matched)'].append(evalset(ws,'A'))
    ws=[bygal[l][rng.integers(len(bygal[l]))] for l in lens if bygal[l]]
    res['B mid/line-initial gallows word, strip gallows (len-matched)'].append(evalset(ws,'B'))
    ws=[bylen[l][rng.integers(len(bylen[l]))] for l in lens if bylen[l]]
    rs=[]
    outs=[]
    for s in ws:
        g=glyphs(s);k=rng.integers(len(g));outs.append(''.join(g[:k]+g[k+1:]))
    m1=np.mean([match(r,1) for r in outs]);m5=np.mean([match(r,5) for r in outs]);mf=np.mean([np.log10(ref.get(r,0)+1) for r in outs])
    res['C random word, strip a random glyph (len-matched)'].append((m1,m5,mf))
print('| set | match>=1 | match>=5 | mean log10(1+freq) |')
print('| para-first gallows words, gallows stripped | %.3f | %.3f | %.2f |'%r_first)
for k,v in res.items():
    v=np.array(v);print('| null %s | %.3f+-%.3f | %.3f+-%.3f | %.2f |'%(k,v[:,0].mean(),v[:,0].std(),v[:,1].mean(),v[:,1].std(),v[:,2].mean()))
for L_ in 'kt','pf':
    ws=[x['w'] for x in first if x['w'][0] in L_]
    print('  subset %s n=%d: match>=1 %.3f match>=5 %.3f'%(L_,len(ws),*evalset(ws,'s')[:2]))
# unstripped control: para-first words exactly as is, match in ref
print('  unstripped para-first words matching ref type: %.3f (>=1), %.3f (>=5)'%(np.mean([ref.get(x['w'],0)>=1 for x in first]),np.mean([ref.get(x['w'],0)>=5 for x in first])))
print('  unstripped mid/line-initial gallows words matching ref: %.3f'%np.mean([ref.get(s,0)>=2 for s in mgal]))
# top remainders
cc=C.Counter(strip_first(s) for s in fw)
print('  top remainders:',[(r,n,ref.get(r,0)) for r,n in cc.most_common(10)])
# which fraction of stripped remainders that match have the *original* (gallows-less) word beginning with y/d/o/s etc? Does stripped word equal typical line-start word?
lsw=C.Counter(x['w'] for x in lnstart)
print('  remainder matches a word type that occurs line-initial (later lines) >=3 times: %.3f'%np.mean([lsw.get(strip_first(s),0)>=3 for s in fw]))
print('  random line-initial word stripped, same: %.3f'%np.mean([lsw.get(strip_first(x['w']),0)>=3 for x in lnstart if len(x['w'])>1]))
# Pch->ch variant: remainder starts with ch/sh/other
cs=C.Counter(glyphs(strip_first(s))[0] if strip_first(s) else '' for s in fw)
print('  initial glyph of remainder:',cs.most_common(8))
print('  remainder first-glyph distribution of mid-line words:',C.Counter(glyphs(s)[0] for s in midws).most_common(8))
# first-line density beyond word 1: within-folio shuffle of words at pos>1 (P lines)
Q=[x for x in P if x['pos']>1]
fq=np.unique([x['folio'] for x in Q],return_inverse=True)[1]
ag=np.array([anyg(x['w']) for x in Q]);ss=np.array([x['pf'] for x in Q])
nl=np.array([ag[np.lexsort((rng.random(len(Q)),fq))][ss].mean() for _ in range(B)])
print('\nline1 words 2+ any-gallows rate: obs %.3f, within-folio null %.3f +- %.3f, z=%.1f'%(ag[ss].mean(),nl.mean(),nl.std(),(ag[ss].mean()-nl.mean())/nl.std()))
