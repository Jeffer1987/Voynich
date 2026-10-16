import re,json,numpy as np,collections as C
from scipy import stats
R=r'J:/Mijn Drive/00 Voynich Red-team/magnetic-cosmos/.claude/worktrees/voynich-subagents-hypotheses-593993/'
GL=re.compile(r'c[ktpf]h|ch|sh|[a-z]')
GAL='ktpf'
def glyphs(w): return GL.findall(w)
def parse(path,mode):
    """lines with words and seps (seps[i] = separator before word i+1: '.' certain, ',' uncertain)"""
    L=[];pg={};pid=0;k=0;cur=None
    for raw in open(path,encoding='utf8'):
        raw=raw.rstrip('\n')
        if not raw or raw[0]=='#':continue
        m=re.match(r'<(f\w+)>\s+<!(.*)>',raw)
        if m:
            pg={a:b for a,b in re.findall(r'\$(\w)=(\S+)',m.group(2))};pg['folio']=m.group(1);continue
        m=re.match(r'<(f\w+)\.(\d+)[^,]*,(.)(\w*)>\s+(.*)',raw)
        if not m:continue
        fol,ln,lt,pt,t=m.groups()
        start='<%>' in t;end='<$>' in t
        t=re.sub(r'<[^>]*>','',t)
        t=re.sub(r'\[([^\]:]*):[^\]]*\]',r'\1',t)
        t=t.replace('{','').replace('}','').replace("'",'')
        toks=re.split(r'([.,])',t)
        words=[];seps=[];sep='.'
        for i,x in enumerate(toks):
            if x in '.,' and x!='' :
                sep=x;continue
            if x and not re.search(r'[?@!;0-9\-]',x):
                words.append(x);seps.append(sep)
            elif x: # damaged token: word break uncertain
                sep='?'
        if not words:continue
        ty=pt[:1] if pt else ''
        pf=(start and ty=='P') if mode=='marker' else (lt=='@' and ty=='P')
        if ty=='P':
            if pf or cur!=fol: k=0;cur=fol
            else:k+=1
            pli=k
        else: pli=None;cur=None
        L.append(dict(folio=fol,line=int(ln),ty=ty,lt=lt,pend=end,pf=pf,pli=pli,I=pg.get('I'),L=pg.get('L'),H=pg.get('H'),words=words,seps=seps))
    return L
def load(name):
    return parse(R+('voynich_ZL3b.txt' if name=='zl3b' else 'voynich_RF1b.txt'),'marker' if name=='zl3b' else 'at')
def cont(L,minw=3):
    return [l for l in L if l['ty']=='P' and not l['pf'] and len(l['words'])>=minw]
def last(w): return glyphs(w)[-1]
def first(w): return glyphs(w)[0]
