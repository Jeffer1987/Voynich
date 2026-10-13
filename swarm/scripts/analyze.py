import json,sys,re,math,random,collections,statistics as st
from collections import Counter
random.seed(1)
def H(c):
    n=sum(c.values());return -sum(v/n*math.log2(v/n) for v in c.values())
def entropies(words):
    s=' '+' '.join(words)+' '
    c1=Counter(s);c2=Counter(zip(s,s[1:]))
    h1=H(c1);h2=H(c2)-H(Counter(s[:-1]))
    return math.log2(len(c1)),h1,h2,len(c1)
def jac(a,b):
    a=set(a);b=set(b);return len(a&b)/len(a|b) if a|b else None
def pairs_from(lines):
    out=[]
    for i in range(len(lines)-1):
        if lines[i][0] is not None and lines[i][0]==lines[i+1][0]:
            out.append(jac(lines[i][1],lines[i+1][1]))
    return out
def summ(x):
    x=[v for v in x if v is not None];return round(st.mean(x),4),round(st.median(x),4),len(x)
def ed1(a,b):
    if len(a)==len(b):return sum(x!=y for x,y in zip(a,b))==1
    if abs(len(a)-len(b))>1:return False
    if len(a)>len(b):a,b=b,a
    for i in range(len(b)):
        if b[:i]+b[i+1:]==a:return True
    return False
def rep(seq_lines):
    t=s1=ed=0
    for ws_ in seq_lines:
        for a,b in zip(ws_,ws_[1:]):
            t+=1
            if a==b:s1+=1
            elif ed1(a,b):ed+=1
    return s1/t,ed/t
def dist(ws,f):return Counter(f(x) for x in ws)
def jsd(a,b):
    ka=set(a)|set(b);na=sum(a.values());nb=sum(b.values())
    p={k:a[k]/na for k in ka};q={k:b[k]/nb for k in ka};m={k:(p[k]+q[k])/2 for k in ka}
    kl=lambda x:sum(x[k]*math.log2(x[k]/m[k]) for k in ka if x[k]>0)
    return (kl(p)+kl(q))/2
def run(path):
    L=json.load(open(path))
    P=[l for l in L if l['par'] is not None]
    res={}
    allw=[w for l in L for w in l['words']]
    res['tokens']=len(allw);res['types']=len(set(allw))
    res['hapax_frac_types']=round(sum(1 for v in Counter(allw).values() if v==1)/len(set(allw)),3)
    res['ent(h0,h1,h2,alphabet)']=entropies(allw)
    lc=Counter(len(w) for w in allw);n=len(allw)
    res['wlen']={k:round(lc[k]/n,4) for k in range(1,13)};res['wlen_mean']=sum(len(w) for w in allw)/n
    lines=[(l['par'],l['words'],l['folio']) for l in P]
    res['jac_real(mean,median,n)']=summ(pairs_from(lines))
    ws=[x[1] for x in lines];vals=[]
    for _ in range(20):
        sh=ws[:];random.shuffle(sh);vals.append(summ(pairs_from([(lines[i][0],sh[i],0) for i in range(len(lines))]))[:2])
    res['jac_shuf_lines_global']=(round(st.mean(v[0] for v in vals),4),round(st.mean(v[1] for v in vals),4))
    byf=collections.defaultdict(list)
    for i,x in enumerate(lines):byf[x[2]].append(i)
    vals=[]
    for _ in range(20):
        sh=[None]*len(lines)
        for f,idx in byf.items():
            p=idx[:];random.shuffle(p)
            for a,b in zip(idx,p):sh[a]=ws[b]
        vals.append(summ(pairs_from([(lines[i][0],sh[i],0) for i in range(len(lines))]))[:2])
    res['jac_shuf_lines_within_folio']=(round(st.mean(v[0] for v in vals),4),round(st.mean(v[1] for v in vals),4))
    pool=allw[:];vals=[]
    for _ in range(20):
        random.shuffle(pool);k=0;nl=[]
        for (par,w,f) in lines:
            nl.append((par,pool[k:k+len(w)],0));k+=len(w)
        vals.append(summ(pairs_from(nl))[:2])
    res['jac_iid_words_unigram']=(round(st.mean(v[0] for v in vals),4),round(st.mean(v[1] for v in vals),4))
    V=res['types'];wts=[1/(r+1) for r in range(V)];vals=[]
    for _ in range(5):
        nl=[(par,random.choices(range(V),wts,k=len(w)),0) for (par,w,f) in lines]
        vals.append(summ(pairs_from(nl))[:2])
    res['jac_zipf_synth_s1']=(round(st.mean(v[0] for v in vals),4),round(st.mean(v[1] for v in vals),4))
    import pydoc_data.topics as T
    ew=re.findall(r'[a-z]+',' '.join(T.topics.values()).lower())
    res['eng_tokens']=len(ew);res['eng_types']=len(set(ew));res['eng_ent']=entropies(ew[:200000])
    res['eng_wlen_mean']=sum(len(w) for w in ew)/len(ew)
    k=0;nl=[]
    for (par,w,f) in lines:
        if k+len(w)>len(ew):break
        nl.append((par,ew[k:k+len(w)],0));k+=len(w)
    res['jac_english_sequential']=summ(pairs_from(nl));res['eng_tokens_used']=k;res['eng_types_in_used']=len(set(ew[:k]))
    pr=[(len(lines[i][1]),jac(lines[i][1],lines[i+1][1])) for i in range(len(lines)-1) if lines[i][0] is not None and lines[i][0]==lines[i+1][0]]
    res['jac_by_len']={}
    for lo,hi in [(1,4),(5,8),(9,12),(13,99)]:
        v=[j for n_,j in pr if lo<=n_<=hi];res['jac_by_len'][f'{lo}-{hi}']=(round(st.mean(v),3),len(v)) if v else None
    def strat(key):
        out={};g=collections.defaultdict(list)
        for l in L:g[l[key]].append(l)
        for k,ls in sorted(g.items(),key=lambda x:str(x[0])):
            w=[x for l in ls for x in l['words']]
            if len(w)<500:continue
            e=entropies(w);c=Counter(w)
            lw=[l['words'] for l in ls if l['ltype']=='P']
            fc=Counter(x[0][0] for x in lw);ec=Counter(x[-1][-1] for x in lw);ft=sum(fc.values())
            out[str(k)]=dict(tok=len(w),typ=len(c),h1=round(e[1],3),h2=round(e[2],3),top=[a for a,_ in c.most_common(6)],
              line_init=[(a,round(b/ft,3)) for a,b in fc.most_common(4)],line_final=[(a,round(b/ft,3)) for a,b in ec.most_common(4)])
        return out
    res['strat_L']=strat('L');res['strat_H']=strat('H');res['strat_I']=strat('I')
    first=[];mid=[];last=[]
    for l in P:
        w=l['words']
        if len(w)>=3:first.append(w[0]);last.append(w[-1]);mid+=w[1:-1]
    pos={}
    for name,f in [('first_glyph',lambda w:w[0]),('last_glyph',lambda w:w[-1]),('wordlen',lambda w:min(len(w),10))]:
        for nm,grp in [('first',first),('last',last)]:
            real=jsd(dist(grp,f),dist(mid,f));allp=grp+mid;nulls=[]
            for _ in range(100):
                random.shuffle(allp);nulls.append(jsd(dist(allp[:len(grp)],f),dist(allp[len(grp):],f)))
            pos[f'{nm}:{name}']=(round(real,4),round(st.mean(nulls),4),round(max(nulls),4))
    res['pos_effect_jsd(real,nullmean,nullmax)']=pos
    res['mean_len_first_mid_last']=tuple(round(sum(map(len,g))/len(g),3) for g in (first,mid,last))
    res['first_glyph_top']=[(a,round(b/len(first),3)) for a,b in dist(first,lambda w:w[0]).most_common(6)]
    res['mid_glyph_top']=[(a,round(b/len(mid),3)) for a,b in dist(mid,lambda w:w[0]).most_common(6)]
    res['last_final_top']=[(a,round(b/len(last),3)) for a,b in dist(last,lambda w:w[-1]).most_common(6)]
    res['mid_final_top']=[(a,round(b/len(mid),3)) for a,b in dist(mid,lambda w:w[-1]).most_common(6)]
    G=set('ktpf')
    pfirst=[l['words'][0] for l in P if l['pstart']]
    others=[l['words'][0] for l in P if not l['pstart']]
    midw=[w for l in P for w in l['words'][1:]]
    isg=lambda w:w[0] in G
    res['par_init_gallows(init glyph in ktpf)']=dict(n=len(pfirst),par_first_word=round(sum(map(isg,pfirst))/max(1,len(pfirst)),3),nonpar_line_first_word=round(sum(map(isg,others))/len(others),3),midline_words=round(sum(map(isg,midw))/len(midw),3))
    slot=re.compile(r'^(?:qo|q|o|y|d|s)?(?:cth|ckh|cph|cfh|[ktpf])?(?:ch|sh)?(?:e{1,3})?(?:o|a)?(?:dy|aiin|ain|iin|in|ol|or|ar|al|am|y|l|r|s|m|n|d|g)?$')
    res['slot_fit_tokens']=round(sum(1 for w in allw if slot.match(w))/len(allw),3)
    res['slot_fit_types']=round(sum(1 for w in set(allw) if slot.match(w))/len(set(allw)),3)
    res['slot_fit_letter_shuffled_within_word']=round(st.mean(sum(1 for w in allw if slot.match(''.join(random.sample(w,len(w)))))/len(allw) for _ in range(5)),3)
    res['slot_fit_english_tokens']=round(sum(1 for w in ew[:20000] if slot.match(w))/20000,3)
    ec=Counter()
    for w in allw:
        for e in ['aiin','dy','in','ol','ar','or','al','y']:
            if w.endswith(e):ec[e]+=1;break
        else:ec['other']+=1
    res['ending_frac']={k:round(v/len(allw),3) for k,v in ec.most_common()}
    res['prefix_frac']={p:round(sum(1 for w in allw if w.startswith(p))/len(allw),3) for p in ['q','qo','o','ch','sh','d','s','y']}
    LW=[l['words'] for l in L]
    r=rep(LW);res['consec(identical,edit1)']=(round(r[0],4),round(r[1],4))
    nul=[];nul2=[]
    byfo=collections.defaultdict(list)
    for l in L:byfo[l['folio']].append(l)
    for _ in range(5):
        pool=allw[:];random.shuffle(pool);k=0;nl=[]
        for w in LW:nl.append(pool[k:k+len(w)]);k+=len(w)
        nul.append(rep(nl))
        nl=[]
        for f,ls in byfo.items():
            pw=[x for l in ls for x in l['words']];random.shuffle(pw);k=0
            for l in ls:nl.append(pw[k:k+len(l['words'])]);k+=len(l['words'])
        nul2.append(rep(nl))
    res['consec_null_global']=tuple(round(st.mean(x[i] for x in nul),4) for i in (0,1))
    res['consec_null_within_folio']=tuple(round(st.mean(x[i] for x in nul2),4) for i in (0,1))
    k=0;nl=[]
    for w in LW:
        if k+len(w)>len(ew):break
        nl.append(ew[k:k+len(w)]);k+=len(w)
    r=rep(nl);res['consec_english']=(round(r[0],4),round(r[1],4))
    return res
if __name__=='__main__':
    print(json.dumps(run(sys.argv[1]),indent=1,default=str))
