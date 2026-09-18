#!/usr/bin/env python3
"""Analysis-only graph and binary64 frontier; no engine or policy changes."""
from collections import deque
from fractions import Fraction
import argparse,json,math,struct,sys
from pathlib import Path
sys.dont_write_bytecode=True

def bits(x):return struct.unpack('>Q',struct.pack('>d',x))[0]
def value(i):return struct.unpack('>d',struct.pack('>Q',i))[0]

def frontier(gate,tol):
    b=1.;rows=[]
    for k in range(1,1001):
        lo,hi=0,bits(b)
        while lo<hi:
            mid=(lo+hi)//2
            if gate(b,value(mid),tol):hi=mid
            else:lo=mid+1
        y=value(lo);previous=value(lo-1) if lo else None
        assert gate(b,y,tol) and (previous is None or not gate(b,previous,tol))
        rows.append(dict(step=k,belief_before=b,belief_after=y,before_hex=b.hex(),after_hex=y.hex(),exact_gap=str(Fraction(b)-Fraction(y)),rounded_gap=abs(b-y),lower_neighbor=previous,lower_neighbor_gap=abs(b-previous) if previous is not None else None))
        b=y
        if b==0:return rows
    raise RuntimeError('Float frontier did not hit0 within declared1000 steps')

def graph(values,tol,gate):
    vs=sorted(set([0.,1.,*values]));adj=[[] for _ in vs];edges=[]
    for i,a in enumerate(vs):
        for j in range(i+1,len(vs)):
            if gate(a,vs[j],tol):
                adj[i].append(j);adj[j].append(i);edges.append((i,j))
    start=vs.index(1.);target=vs.index(0.);dist={start:0};count={start:1};parent={};queue=deque([start])
    while queue:
        i=queue.popleft()
        for j in adj[i]:
            if j not in dist:dist[j]=dist[i]+1;count[j]=0;parent[j]=i;queue.append(j)
            if dist[j]==dist[i]+1:count[j]+=count[i]
    components={};component=0
    for i in range(len(vs)):
        if i in components:continue
        components[i]=component;queue=deque([i])
        while queue:
            for j in adj[queue.popleft()]:
                if j not in components:components[j]=component;queue.append(j)
        component+=1
    path=[]
    if target in dist:
        at=target;path=[vs[at]]
        while at!=start:at=parent[at];path.append(vs[at])
        path.reverse()
    return dict(nodes=vs,edges=edges,components=components,component_count=component,path_exists=target in dist,shortest_length=dist.get(target),shortest_path_count=count.get(target,0),witness=path,distances=dist)

def main():
    import run_experiment as F
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=F.HERE/'results');a=ap.parse_args();out=a.output_dir;out.mkdir(exist_ok=True,parents=True)
    fr=frontier(F.gate,F.C.TOL);F.D.dump(out/'float_frontier.csv',fr)
    cases=[(f'uniform_n{n}_tol{t}',[i/n for i in range(n+1)],t,'uniform',n) for n in F.CFG['graph_denominators'] for t in F.CFG['graph_tolerances']]
    cases.append(('witness_augmented_n40_tol0.05',[i/40 for i in range(41)]+[r['belief_after'] for r in fr],.05,'witness_augmented',40))
    summaries=[];edges=[];nodes=[];witness_events=[]
    for gid,vs,t,kind,n in cases:
        g=graph(vs,t,F.gate);b=1.
        for step,x in enumerate(g['witness'][1:],1):
            beliefs={'known':b};accepted,_,_=F.C.BASE.offer(beliefs,'known',x,False,'gated',t)
            witness_events.append(dict(graph_id=gid,tol=t,step=step,belief_before=b,input_value=x,accepted=accepted,belief_after=beliefs['known']));assert accepted;b=beliefs['known']
        assert not g['path_exists'] or b==0
        summaries.append(dict(graph_id=gid,kind=kind,denominator=n,tol=t,node_count=len(g['nodes']),edge_count=len(g['edges']),component_count=g['component_count'],path_exists=g['path_exists'],shortest_path_length=g['shortest_length'],shortest_path_count=g['shortest_path_count'],witness=json.dumps(g['witness']),witness_replayed=g['path_exists'],primary_tol=t==.05))
        for i,x in enumerate(g['nodes']):nodes.append(dict(graph_id=gid,node_id=i,value=x,value_hex=x.hex(),component=g['components'][i],distance_from1=g['distances'].get(i)))
        for i,j in g['edges']:edges.append(dict(graph_id=gid,source=i,target=j,source_value=g['nodes'][i],target_value=g['nodes'][j],rounded_gap=abs(g['nodes'][i]-g['nodes'][j]),tol=t))
    F.D.dump(out/'reachability_graph.csv',summaries);F.D.dump(out/'graph_nodes.csv',nodes);F.D.dump(out/'graph_edges.csv',edges);F.D.dump(out/'graph_witness_events.csv',witness_events)
    meta=dict(command=[sys.executable,*sys.argv],real_tau='1/20',real_lower_bound=20,float_tol_hex=(.05).hex(),float_tol_exact=str(Fraction(.05)),float_L_min=len(fr),frontier_step20=fr[19]['belief_after'],last_step=fr[-1],graph_cases=len(cases),analysis_tolerances_only=F.CFG['graph_tolerances'])
    (out/'analysis.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2))
if __name__=='__main__':main()
