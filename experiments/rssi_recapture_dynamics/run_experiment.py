#!/usr/bin/env python3
"""Exp E: new input schedules, unchanged C/D state updates and nonempty outcomes."""
from __future__ import annotations
import argparse,csv,hashlib,importlib.util,json,random,shlex,sys
from collections import Counter,defaultdict
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('exp_d_reused',HERE.parent/'rssi_attractor_escape_boundary/run_experiment.py')
D=importlib.util.module_from_spec(spec);sys.modules[spec.name]=D;spec.loader.exec_module(D);C=D.C
CFG=json.loads((HERE/'config.json').read_text());EPS=C.EPS

def conditions():
 rows=[]
 def add(family,q=None,v=None,order=None):
  name=f'{family}_q{q}_v{v}_order{order}'
  rows.append(dict(condition_id=name,family=family,q_nominal=q,drift_v=v,order=order))
 for f in ('stationary','descending_bridge','no_input','noisy_corrective'):add(f)
 for q in CFG['q_values']:add('abrupt_return',q)
 for v in CFG['v_values']:
  for q in CFG['q_values']:add('gradual_drift',q,v)
 for q in CFG['q_values']:add('alternating',q)
 for q in CFG['sparse_q_values']:add('sparse_corrective',q)
 add('endpoint_order',.5,None,'R_first')
 add('bridge_order',1.,.025,'ascending');add('bridge_order',1.,.025,'shuffled')
 assert len(rows)==66
 return rows

def sequence(cond,seed,baseline_steps):
 family=cond['family'];n=C.HORIZON;q=cond['q_nominal'];v=cond['drift_v']
 if family in ('stationary','descending_bridge'):return [C.normal_batch(family,baseline_steps+t) for t in range(1,n+1)]
 if family=='no_input':return [() for _ in range(n)]
 if family=='noisy_corrective':
  rng=random.Random(f'exp_e_noise_{seed}');a=CFG['noise_amplitude'];return [(max(0.,min(1.,1+rng.uniform(-a,a))),) for _ in range(n)]
 n_o=round(q*n)
 if family=='endpoint_order':return [(1.,)]*(n-n_o)+[(0.,)]*n_o
 if family=='bridge_order':
  vals=[max(0.,1-.025*t) for t in range(1,n+1)]
  if cond['order']=='ascending':vals.sort()
  else:random.Random(f'exp_e_order_{seed}').shuffle(vals)
  return [(x,) for x in vals]
 rows=[]
 for t in range(1,n+1):
  old=(t<=n_o) if family=='abrupt_return' else ((n-n_o)*t//n==(n-n_o)*(t-1)//n) if family=='sparse_corrective' else n_o*t//n>n_o*(t-1)//n
  rows.append(((max(0.,1-v*t) if family=='gradual_drift' else 0.) if old else 1.,))
 return rows

def no_input_summary(rec,n,anchor,w,probes):
 """Only undefined-rate control; no dummy inputs. State criteria are unchanged."""
 normal=[r for r in rec.trajectories if r['phase']=='normal'];external=[e for e in rec.events if e['phase']=='injection']
 assert len(normal)==C.HORIZON and not any(e['phase']=='normal' for e in rec.events)
 assert len(external)==1 and all(r['belief']==external[0]['belief_after'] for r in normal)
 e=external[0];d_pre=abs(anchor-1);qual=e['D_before']-e['D_after']>=C.MIN_GAIN-C.EPS
 relapse,confirmation=C.relapse_blocks(normal,anchor,d_pre,0)
 persistent=qual and relapse is None and all(r['D']<=d_pre-C.MIN_GAIN+C.EPS for r in normal[-C.WITHDRAWAL:])
 return dict(**rec.labels,baseline_steps=n,attractor_belief=anchor,stable_window=w,local_probe_count=len(probes),local_probes_passed=all(p['passed'] for p in probes),
 D_pre=d_pre,D_immediate_first=e['D_after'],D_immediate_last=e['D_after'],D_final=normal[-1]['D'],D_post=D.mean([r['D'] for r in normal[-20:]]),delta_D=D.mean([r['D'] for r in normal[-20:]])-d_pre,
 C_pre=next(r['C_internal'] for r in reversed(rec.trajectories) if r['phase']=='baseline'),C_post=None,C_post_defined_steps=0,
 normal_accepted=0,normal_rejected=0,acceptance_rate=None,rejection_rate=None,external_delivery_count=1,bypass_delivery_count=1,external_update_accepted_count=int(e['accepted']),external_rejected_count=int(e['rejected']),actual_revision_count=int(e['internal_revision']),qualifying_revision_count=int(qual),genuine_revision_count=int(qual and all(r['D']<=e['D_before']-.1+EPS for r in normal)),apparent_correction_count=0,
 relapse_observed=relapse is not None,relapse_rate_if_eligible=int(relapse is not None) if qual else None,relapse_start_step=relapse,relapse_confirmation_step=confirmation,time_to_relapse=relapse,time_to_relapse_from_last_injection=relapse,persistent_escape=persistent,persistent_escape_rate=int(persistent),normal_post_steps=len(normal),steps_after_last_injection=C.HORIZON,
 classification='A_genuine_revision_candidate' if persistent else 'E_relapse' if relapse is not None else 'mixed_or_partial_escape',reference_corruption='not_available',reference_avoidance='not_available')

def input_hash(vals,sorted_values=False):
 return hashlib.sha256(json.dumps(sorted(vals) if sorted_values else vals,separators=(',',':')).encode()).hexdigest()

def enrich(rec,row,seq):
 ns=[r for r in rec.trajectories if r['phase']=='normal'];es=[e for e in rec.events if e['phase']=='normal'];vals=[e['input_value'] for e in es];t=row['relapse_start_step']
 old=lambda e:e['input_value']<1-EPS
 row.update(post_inputs=len(es),corrective_offered=sum(not old(e) for e in es),contradictory_offered=sum(old(e) for e in es),
 q_actual=sum(old(e) for e in es)/len(es) if es else None,q_old_halfspace=sum(e['input_value']<.5 for e in es)/len(es) if es else None,exact_old_count=sum(abs(e['input_value'])<=EPS for e in es),input_mean=D.mean(vals),last_input=vals[-1] if vals else None,sequence_sha256=input_hash(vals),multiset_sha256=input_hash(vals,True),
 D_min=min([row['D_immediate_first']]+[r['D'] for r in ns]),recapture_latency=t,
 recapture_slope_net=(ns[int(t)-1]['D']-row['D_immediate_first'])/t if t else None,
 recapture_slope_active=None,corrective_before_failure=None,contradictory_before_failure=None,corrective_accepted_before_failure=None,contradictory_accepted_before_failure=None,
 C_at_relapse=ns[int(t)-1]['C_internal'] if t else None,
 early_C_mean=D.mean([r['C_internal'] for r in ns[:10] if r['C_internal'] is not None]),early_C_defined_steps=sum(r['C_internal'] is not None for r in ns[:10]),
 early_C_alarm=None,alarm_is_prospective=t is None or t>10,high_C_at_relapse=None)
 if row['early_C_mean'] is not None:row['early_C_alarm']=row['early_C_mean']<.99-EPS
 if t:
  previous=row['D_immediate_first'];positive=[]
  for r in ns[:int(t)]:
   if r['D']-previous>EPS:positive.append(r['D']-previous)
   previous=r['D']
  before=[e for e in es if e['step']<=t]
  row.update(recapture_slope_active=D.mean(positive),corrective_before_failure=sum(not old(e) for e in before),contradictory_before_failure=sum(old(e) for e in before),corrective_accepted_before_failure=sum(not old(e) and e['accepted'] for e in before),contradictory_accepted_before_failure=sum(old(e) and e['accepted'] for e in before),high_C_at_relapse=row['C_at_relapse'] is not None and row['C_at_relapse']>=.95-EPS)
 return row

def aggregate(rows):
 groups=defaultdict(list)
 for r in rows:groups[r['condition_id']].append(r)
 aggregates=[]
 for key,rs in groups.items():
  r=rs[0];counts=Counter(x['classification'] for x in rs)
  means={f'mean_{k}':D.mean([x[k] for x in rs if x[k] is not None]) for k in ('q_actual','D_final','D_min','time_to_relapse','recapture_slope_net','recapture_slope_active','early_C_mean','C_post','corrective_before_failure','contradictory_before_failure')}
  aggregates.append(dict(condition_id=key,family=r['family'],q_nominal=r['q_nominal'],drift_v=r['drift_v'],order=r['order'],runs=len(rs),outcome_counts=json.dumps(dict(sorted(counts.items())),sort_keys=True),persistent_escape_rate=counts['A_genuine_revision_candidate']/len(rs),relapse_rate=counts['E_relapse']/len(rs),rejection_rate=counts['C_rejection']/len(rs),mixed_rate=counts['mixed_or_partial_escape']/len(rs),**means))
 thresholds=[]
 def scan(cells,axis,fixed):
  cells=sorted(cells,key=lambda x:x[axis]);hit=[i for i,x in enumerate(cells) if x['relapse_rate']>0];i=hit[0] if hit else None
  thresholds.append(dict(family=cells[0]['family'],axis=axis,fixed=fixed,kind='first_relapse',lower=cells[i-1][axis] if i is not None and i>0 else None,upper=cells[i][axis] if i is not None else None,from_distribution=cells[i-1]['outcome_counts'] if i is not None and i>0 else None,to_distribution=cells[i]['outcome_counts'] if i is not None else None,status='not_observed' if i is None else 'already_at_minimum' if i==0 else 'bracketed',lower_all_persistent=cells[i-1]['persistent_escape_rate']==1 if i is not None and i>0 else None))
  for a,b in zip(cells,cells[1:]):
   if a['outcome_counts']!=b['outcome_counts']:
    thresholds.append(dict(family=a['family'],axis=axis,fixed=fixed,kind='adjacent_change',lower=a[axis],upper=b[axis],from_distribution=a['outcome_counts'],to_distribution=b['outcome_counts'],status='observed_distribution_change',lower_all_persistent=a['persistent_escape_rate']==1))
 for fam in sorted({r['family'] for r in aggregates}):
  fs=[r for r in aggregates if r['family']==fam]
  if fam=='gradual_drift':
   for v in CFG['v_values']:scan([r for r in fs if r['drift_v']==v],'q_nominal',f'v={v}')
   for q in CFG['q_values']:scan([r for r in fs if r['q_nominal']==q],'drift_v',f'q={q}')
  elif fam in ('abrupt_return','alternating','sparse_corrective'):scan(fs,'q_nominal','none')
  else:thresholds.append(dict(family=fam,axis='q_actual',fixed='fixed family or order comparison',kind='availability',lower=None,upper=None,from_distribution=None,to_distribution=None,status='not_estimated_q_not_manipulated',lower_all_persistent=None))
 return aggregates,thresholds

def comparisons(rows,paths):
 effects=[];pairpaths=[]
 def find(seed,fam,q=None,v=None,order=None):return next(r for r in rows if r['seed']==seed and (r['family'],r['q_nominal'],r['drift_v'],r['order'])==(fam,q,v,order))
 for seed in CFG['seeds']:
  groups={'endpoints':[find(seed,'abrupt_return',.5),find(seed,'endpoint_order',.5,None,'R_first'),find(seed,'alternating',.5)],'bridge_values':[find(seed,'gradual_drift',1.,.025),find(seed,'bridge_order',1.,.025,'ascending'),find(seed,'bridge_order',1.,.025,'shuffled')]}
  for group,rs in groups.items():
   for i,a in enumerate(rs):
    for b in rs[i+1:]:
     same=a['multiset_sha256']==b['multiset_sha256'];assert same
     effects.append(dict(seed=seed,multiset_group=group,condition_a=a['condition_id'],condition_b=b['condition_id'],same_multiset=same,q_a=a['q_actual'],q_b=b['q_actual'],outcome_a=a['classification'],outcome_b=b['classification'],D_final_a=a['D_final'],D_final_b=b['D_final'],outcome_changed=a['classification']!=b['classification'],D_path_changed=paths[a['run_id']]!=paths[b['run_id']]))
  a=find(seed,'gradual_drift',1.,1.);b=find(seed,'gradual_drift',1.,.025)
  assert a['last_input']==b['last_input']==0
  pairpaths.append(dict(seed=seed,fast_run=a['run_id'],slow_run=b['run_id'],same_final_input=True,final_input=0,fast_D_final=a['D_final'],slow_D_final=b['D_final'],fast_outcome=a['classification'],slow_outcome=b['classification'],outcome_changed=a['classification']!=b['classification']))
 return effects,pairpaths

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE/'results');args=ap.parse_args();out=args.output_dir;out.mkdir(exist_ok=True,parents=True)
 manifest=conditions();(out/'condition_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 ts=D.Stream(out/'trajectories.csv');ev=D.Stream(out/'events.csv');rows=[];paths={};probes_saved=[]
 for cond in manifest:
  for seed in CFG['seeds']:
   regime='descending_bridge' if cond['family']=='descending_bridge' else 'stationary';rid=f"{cond['condition_id']}_seed{seed}"
   rec=C.Recorder(rid,regime,seed,'post_input_dynamics',1.,C.load_reference(),random.Random(seed).uniform(.005,.04));rec.labels.update(**cond)
   n,anchor,probes,w=C.reach_attractor(rec)
   if cond['family'] in ('stationary','descending_bridge'):probes_saved.extend(dict(family=cond['family'],seed=seed,**p) for p in probes)
   seq=sequence(cond,seed,n);assert len(seq)==120
   rec.snapshot('pre_injection',0,[],rec.beliefs['known']);before=rec.beliefs['known'];e=rec.event('injection',0,1.,'independent_reference','evidence_revision',1.);rec.snapshot('injection',0,[e],before)
   for step,batch in enumerate(seq,1):
    before=rec.beliefs['known'];events=[]
    for i,x in enumerate(batch):
     e=rec.event('normal',step,x,'normal','ordinary_gate');e['input_index']=i;events.append(e)
    rec.snapshot('normal',step,events,before)
   row=no_input_summary(rec,n,anchor,w,probes) if cond['family']=='no_input' else C.summarize(rec,n,anchor,w,probes,(0,))
   rows.append(enrich(rec,row,seq));paths[rid]=[r['D'] for r in rec.trajectories if r['phase']=='normal']
   for e in rec.events:
    e.update(input_direction='corrective' if abs(e['input_value']-1)<=EPS else 'old_directed',generator_role=cond['family'] if e['phase']=='normal' else e['source'])
   ts.add(rec.trajectories);ev.add(rec.events)
 ts.close();ev.close();aggregates,thresholds=aggregate(rows);effects,pairpaths=comparisons(rows,paths)
 D.dump(out/'summary.csv',rows);D.dump(out/'sequence_summary.csv',aggregates);D.dump(out/'recapture_thresholds.csv',thresholds);D.dump(out/'order_effects.csv',effects);D.dump(out/'path_dependence.csv',pairpaths);D.dump(out/'attractor_checks.csv',probes_saved)
 keys=('run_id','family','q_nominal','drift_v','q_actual','classification','D_min','D_final','relapse_start_step','relapse_confirmation_step','time_to_relapse','recapture_latency','recapture_slope_net','recapture_slope_active','corrective_before_failure','contradictory_before_failure','corrective_accepted_before_failure','contradictory_accepted_before_failure')
 D.dump(out/'relapse_times.csv',[{k:r[k] for k in keys} for r in rows])
 alarm=[]
 for fam in [*sorted({r['family'] for r in rows}),'all']:
  rs=[r for r in rows if fam=='all' or r['family']==fam];valid=[r for r in rs if r['early_C_alarm'] is not None and r['alarm_is_prospective']]
  alarm.append(dict(family=fam,runs=len(rs),available_prospective=len(valid),unavailable=sum(r['early_C_alarm'] is None for r in rs),too_early=sum(not r['alarm_is_prospective'] for r in rs),TP=sum(r['early_C_alarm'] and r['classification']=='E_relapse' for r in valid),FP=sum(r['early_C_alarm'] and r['classification']!='E_relapse' for r in valid),FN=sum(not r['early_C_alarm'] and r['classification']=='E_relapse' for r in valid),TN=sum(not r['early_C_alarm'] and r['classification']!='E_relapse' for r in valid),high_C_at_relapse=sum(r['high_C_at_relapse'] is True for r in rs)))
 D.dump(out/'coherence_diagnostic.csv',alarm)
 meta=dict(command=shlex.join([sys.executable,*sys.argv]),config=CFG,conditions=len(manifest),runs=len(rows),trajectory_rows=ts.count,events=ev.count,baseline_steps=sum(r['baseline_steps'] for r in rows),post_steps=sum(r['normal_post_steps'] for r in rows),total_steps=sum(r['baseline_steps']+r['normal_post_steps'] for r in rows),post_inputs=sum(r['post_inputs'] for r in rows),outcomes=dict(Counter(r['classification'] for r in rows)),native_julia=False,protocol_sha256=D.sha(HERE/'PROTOCOL.md'),config_sha256=D.sha(HERE/'config.json'),runner_sha256=D.sha(Path(__file__)),c_runner_sha256=D.sha(D.CPATH/'run_experiment.py'),d_runner_sha256=D.sha(D.HERE/'run_experiment.py'),reference_sha256=D.sha(D.CPATH/'reference.json'),csv_sha256={p.name:D.sha(p) for p in sorted(out.glob('*.csv'))})
 (out/'execution.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({k:meta[k] for k in ('conditions','runs','trajectory_rows','events','total_steps','outcomes')},indent=2))
if __name__=='__main__':main()
