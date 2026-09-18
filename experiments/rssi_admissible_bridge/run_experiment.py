#!/usr/bin/env python3
"""Exp F paths replayed through unchanged A/C/D/E utilities."""
from __future__ import annotations
import argparse,importlib.util,json,math,random,sys
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];EPATH=HERE.parent/'rssi_recapture_dynamics'
spec=importlib.util.spec_from_file_location('exp_e_reused',EPATH/'run_experiment.py');E=importlib.util.module_from_spec(spec);sys.modules[spec.name]=E;spec.loader.exec_module(E);D=E.D;C=D.C
import analyze_reachability as G
CFG=json.loads((HERE/'config.json').read_text())

def gate(b,x,tol):return C.BASE.offer({'known':b},'known',x,False,'gated',tol)[0]
def fixed_delta(delta):return [max(0.,1-k*delta) for k in range(1,math.ceil(1/delta)+1)]
def e_cond(family,q=None,v=None,order=None):return next(c for c in E.conditions() if (c['family'],c['q_nominal'],c['drift_v'],c['order'])==(family,q,v,order))
def e_values(cond,seed):return [x for batch in E.sequence(cond,seed,11) for x in batch]

def plans(seed):
    rows=[]
    def add(cid,family,values,**kw):
        rows.append(dict(condition_id=cid,family=family,values=values,delta=None,noise=None,order=None,order_group=None,tokens=None,deleted_original_position=None,**{k:v for k,v in kw.items() if k not in ('delta','noise','order','order_group','tokens','deleted_original_position')}))
        rows[-1].update(kw)
    add('control_no_input','control',[])
    add('control_abrupt0','control',e_values(e_cond('abrupt_return',1.),seed))
    ev=e_values(e_cond('gradual_drift',1.,.025),seed)
    add('control_E_gradual','control',ev,order='descending',order_group='E_bridge',tokens=list(range(120)))
    add('control_E_fast','control',e_values(e_cond('gradual_drift',1.,1.),seed))
    add('minimum_float_frontier','minimum',[r['belief_after'] for r in G.frontier(gate,.05)])
    for n in CFG['uniform_lengths']:add(f'minimum_uniform{n}','minimum',[1-k/n for k in range(1,n+1)])
    deltas=[(str(d),d) for d in CFG['delta_decimal_values']]+[('nextbelow',math.nextafter(.05,0.)),('nextabove',math.nextafter(.05,math.inf))]
    for name,d in deltas:add('delta_'+name,'step_size',fixed_delta(d),delta=d)
    base=fixed_delta(.04);add('bridge_valid04','broken_bridge',base,noise=0.)
    for name,pos in [('early',2),('middle',13),('late',24)]:add('broken_'+name,'broken_bridge',base[:pos-1]+base[pos:],deleted_original_position=pos)
    redundant=fixed_delta(.02);add('bridge_valid02','broken_bridge',redundant)
    add('broken_redundant_middle','broken_bridge',redundant[:24]+redundant[25:],deleted_original_position=25)
    add('geometry_monotone','geometry',[1-i/32 for i in range(1,33)])
    add('geometry_detour','geometry',[1-i/32 for i in range(1,17)]+[.5+i/32 for i in range(1,9)]+[.75-i/32 for i in range(1,25)])
    vals=[]
    for i in range(32):
        b=1-i/32;vals.extend([b-1/32,b-1/64,b-1/32])
    add('geometry_oscillatory','geometry',vals)
    rng=random.Random(f'exp_f_random_{seed}');b=1.;prefix=[]
    for _ in range(CFG['random_prefix_steps']):b=max(0.,min(1.,b+rng.choice([-1,1])/32));prefix.append(b)
    add('geometry_random_connected','geometry',prefix+[b-i/32 for i in range(1,round(b*32)+1)])
    add('geometry_random_free','geometry',prefix)
    ascending=sorted(range(120),key=lambda i:(ev[i],i));highlow=[];lo,hi=0,119
    while lo<=hi:
        highlow.append(ascending[hi]);hi-=1
        if lo<=hi:highlow.append(ascending[lo]);lo+=1
    shuffled=list(range(120));random.Random(f'exp_e_order_{seed}').shuffle(shuffled)
    for name,indices in [('ascending',ascending),('alternating',highlow),('shuffled',shuffled)]:add('order_'+name,'order',[ev[i] for i in indices],order=name,order_group='E_bridge',tokens=indices)
    rng=random.Random(f'exp_f_noise_{seed}');z=[rng.uniform(-1,1) for _ in base[:-1]]
    for eta in CFG['noise_levels'][1:]:add(f'noise_{eta}','noise',[max(0.,min(1.,x+eta*n)) for x,n in zip(base[:-1],z)]+[0.],noise=eta)
    assert len(rows)==34 and all(len(r['values'])<=120 for r in rows)
    return rows

def measures(rec,row,plan,float_min):
    events=[e for e in rec.events if e['phase']=='normal'];vals=plan['values'];states=[t for t in rec.trajectories if t['phase']=='normal']
    pairs=list(zip([1.]+vals,vals));gaps=[abs(b-x) for b,x in pairs];bad=[i+1 for i,(b,x) in enumerate(pairs) if not gate(b,x,.05)]
    rejected=[e for e in events if not e['accepted']];hits=[e['step'] for e in events if e['belief_after']==0];g=G.graph(vals,.05,gate)
    row.update(path_length=len(vals),L_actual=len(vals),L_min_real=20,L_min_binary64=float_min,accepted_step_count=sum(e['accepted'] for e in events),rejected_step_count=len(rejected),accepted_moves=sum(e['accepted'] and e['belief_before']!=e['belief_after'] for e in events),first_rejection_step=rejected[0]['step'] if rejected else None,first_rejection_gap=abs(rejected[0]['input_value']-rejected[0]['belief_before']) if rejected else None,disconnected_gap_size=max([abs(e['input_value']-e['belief_before']) for e in rejected],default=None),max_rejection_excess=max([abs(e['input_value']-e['belief_before'])-.05 for e in rejected],default=None),TV=sum(gaps),TV_input_only=sum(abs(a-b) for a,b in zip(vals,vals[1:])),actual_state_TV=sum(abs(e['belief_after']-e['belief_before']) for e in events),requested_max_gap=max(gaps,default=None),first_requested_gap_step=bad[0] if bad else None,requested_disconnected_edges=len(bad),all_requested_edges_admissible=not bad,first_target_step=hits[0] if hits else None,target_reached=bool(hits),target_reached_final=states[-1]['belief']==0,final_belief=states[-1]['belief'],bridge_completion=bool(vals) and vals[-1]==0 and not rejected and states[-1]['belief']==0,unordered_graph_path_exists=g['path_exists'],unordered_shortest_path_length=g['shortest_length'],target_in_offered_values=0. in vals,sequence_sha256=E.input_hash(vals),multiset_sha256=E.input_hash(vals,True),empty_hold_steps=120-len(vals))
    return row

def compare_orders(run_data):
    pairs=[];witnesses=[]
    for seed in CFG['seeds']:
        rows=[r for r in run_data if r['seed']==seed and r['plan']['order_group']=='E_bridge']
        for i,a in enumerate(rows):
            for b in rows[i+1:]:
                ea=a['events'];eb=b['events'];assert sorted(a['plan']['values'])==sorted(b['plan']['values'])
                first_b=next((x['step'] for x,y in zip(ea,eb) if x['belief_after']!=y['belief_after']),None)
                first_a=next((x['step'] for x,y in zip(ea,eb) if x['accepted']!=y['accepted']),None)
                by_token={e['input_token']:e for e in eb};ws=[]
                for x in ea:
                    y=by_token[x['input_token']];assert x['input_value']==y['input_value']
                    if x['accepted']!=y['accepted']:
                        w=dict(seed=seed,run_a=a['run_id'],run_b=b['run_id'],order_a=a['plan']['order'],order_b=b['plan']['order'],token=x['input_token'],input_value=x['input_value'],step_a=x['step'],step_b=y['step'],belief_before_a=x['belief_before'],belief_before_b=y['belief_before'],accepted_a=x['accepted'],accepted_b=y['accepted'],gap_a=abs(x['input_value']-x['belief_before']),gap_b=abs(y['input_value']-y['belief_before']))
                        ws.append(w);witnesses.append(w)
                first=ws[0] if ws else {}
                pairs.append(dict(seed=seed,run_a=a['run_id'],run_b=b['run_id'],order_a=a['plan']['order'],order_b=b['plan']['order'],same_multiset=True,first_divergence_step=first_b,first_acceptance_flag_divergence_step=first_a,shared_token_decision_differences=len(ws),first_shared_witness_token=first.get('token'),first_shared_witness_value=first.get('input_value'),first_shared_witness_step_a=first.get('step_a'),first_shared_witness_step_b=first.get('step_b'),classification_a=a['summary']['classification'],classification_b=b['summary']['classification']))
    return pairs,witnesses

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE/'results');args=ap.parse_args();out=args.output_dir;out.mkdir(exist_ok=True,parents=True)
    # Materialize every path before any trajectory starts.
    allplans=[dict(seed=s,**p) for s in CFG['seeds'] for p in plans(s)]
    (out/'path_manifest.json').write_text(json.dumps(allplans,indent=2)+'\n')
    fr=G.frontier(gate,C.TOL);ts=D.Stream(out/'trajectories.csv');es=D.Stream(out/'events.csv');summaries=[];run_data=[]
    for plan in allplans:
        seed=plan['seed'];cid=plan['condition_id'];rid=f'{cid}_seed{seed}'
        rec=C.Recorder(rid,'stationary',seed,'admissible_bridge',1.,C.load_reference(),random.Random(seed).uniform(.005,.04))
        rec.labels.update(condition_id=cid,family=plan['family'],delta=plan['delta'],noise=plan['noise'],order=plan['order'])
        n,anchor,probes,w=C.reach_attractor(rec);assert anchor==0
        rec.snapshot('pre_injection',0,[],rec.beliefs['known']);before=rec.beliefs['known'];e=rec.event('injection',0,1.,'independent_reference','evidence_revision',1.);rec.snapshot('injection',0,[e],before);assert rec.beliefs['known']==1
        for t in range(1,121):
            before=rec.beliefs['known'];events=[]
            if t<=len(plan['values']):
                e=rec.event('normal',t,plan['values'][t-1],'normal','ordinary_gate');events.append(e)
                e['input_token']=plan['tokens'][t-1] if plan['tokens'] is not None else None
            rec.snapshot('normal',t,events,before)
        row=E.no_input_summary(rec,n,anchor,w,probes) if not plan['values'] else C.summarize(rec,n,anchor,w,probes,(0,))
        summaries.append(measures(rec,row,plan,len(fr)))
        for e in rec.events:e.setdefault('input_token',None)
        ts.add(rec.trajectories);es.add(rec.events)
        run_data.append(dict(seed=seed,run_id=rid,plan=plan,events=[e for e in rec.events if e['phase']=='normal'],summary=row))
    ts.close();es.close();D.dump(out/'bridge_summary.csv',summaries)
    minimum=[{k:r[k] for k in ('run_id','condition_id','seed','L_min_real','L_min_binary64','L_actual','accepted_step_count','rejected_step_count','first_rejection_step','final_belief','target_reached','first_target_step','bridge_completion')} for r in summaries if r['family']=='minimum']
    D.dump(out/'minimum_paths.csv',minimum);divergences,witnesses=compare_orders(run_data);D.dump(out/'order_divergence.csv',divergences);D.dump(out/'order_acceptability.csv',witnesses)
    meta=dict(command=[sys.executable,*sys.argv],config=CFG,conditions=34,runs=len(summaries),events=es.count,trajectory_rows=ts.count,total_steps=sum(r['baseline_steps']+120 for r in summaries),post_steps=120*len(summaries),post_inputs=sum(r['path_length'] for r in summaries),outcomes=dict(Counter(r['classification'] for r in summaries)),target_reached=sum(r['target_reached'] for r in summaries),float_L_min=len(fr),protocol_sha256=D.sha(HERE/'PROTOCOL.md'),config_sha256=D.sha(HERE/'config.json'),source_sha256={p.name:D.sha(p) for p in [HERE/'run_experiment.py',HERE/'analyze_reachability.py']},reference_sha256=D.sha(D.CPATH/'reference.json'),path_manifest_sha256=D.sha(out/'path_manifest.json'),csv_sha256={p.name:D.sha(p) for p in sorted(out.glob('*.csv'))},native_julia=False)
    (out/'execution.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({k:meta[k] for k in ('conditions','runs','events','trajectory_rows','total_steps','post_inputs','outcomes','target_reached','float_L_min')},indent=2))
if __name__=='__main__':main()
