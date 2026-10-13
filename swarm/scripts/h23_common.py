import json,re,numpy as np,collections as C
SP=r'C:/Users/Jeffrey/AppData/Local/Temp/claude/J--Mijn-Drive-00-Voynich-Red-team-magnetic-cosmos--claude-worktrees-voynich-subagents-hypotheses-593993/194b83ce-2de0-4696-8833-e22ebb22ff7d/scratchpad'
GAL='ktpf'
GL=re.compile(r'c[ktpf]h|ch|sh|[a-z]')
def glyphs(w): return GL.findall(w)
def load(name,pstart_mode='marker'):
    d=json.load(open(SP+'/parsed_%s.json'%name))
    # paragraph-first line: ZL marker pstart; RF has none -> only @P lines
    for i,l in enumerate(d):
        if pstart_mode=='at': l['pf']= (l['lt']=='@' and l['ltype']=='P')
        else: l['pf']=bool(l['pstart']) and l['ltype']=='P'
    # line index within paragraph
    cur=None;k=0
    for l in d:
        if l['ltype']=='P':
            if l['pf'] or cur is None or l['folio']!=cur: k=0;cur=l['folio']
            else: k+=1
            l['pli']=k
        else: l['pli']=None; cur=None
    return d
def words(d):
    """flat word table (list of dicts)"""
    W=[]
    for li,l in enumerate(d):
        n=len(l['words'])
        for p,w in enumerate(l['words']):
            W.append(dict(w=w,li=li,pos=p+1,n=n,lt=l['lt'],ty=l['ltype'],pf=l['pf'],pli=l['pli'],
                folio=l['folio'],L=l['L'],H=l['H'],I=l['I'],pend=l['pend']))
    return W
def pct(x): return '%.1f%%'%(100*x)
