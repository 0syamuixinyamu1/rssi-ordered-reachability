#!/usr/bin/env python3
"""Exp D orchestration. All RSSI transitions and outcome rules come from Exp C."""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util, json, platform, random, shlex, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CPATH=HERE.parent/'rssi_attractor_escape'
spec=importlib.util.spec_from_file_location('rssi_exp_c',CPATH/'run_experiment.py')
C=importlib.util.module_from_spec(spec);sys.modules[spec.name]=C;spec.loader.exec_module(C)
CONFIG=json.loads((HERE/'config.json').read_text())
LABELS=('C_rejection','E_relapse','A_genuine_revision_candidate')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def schedule(f):
    if f==0:return ()
    if f==1:return (0,)
    end=CONFIG['injection_window_end']
    seq=tuple((end*i+(f-1)//2)//(f-1) for i in range(f))
    if len(set(seq))!=f:raise ValueError('Duplicate injection steps')
    return seq
def dump(path,rows,fields=None):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
class Stream:
    def __init__(self,path):self.f=path.open('w',newline='');self.writer=None;self.count=0
    def add(self,rows):
        if not rows:return
        if self.writer is None:self.writer=csv.DictWriter(self.f,fieldnames=list(rows[0]));self.writer.writeheader()
        self.writer.writerows(rows);self.count+=len(rows)
    def close(self):self.f.close()
def mean(xs):return sum(xs)/len(xs) if xs else None

def boundary_scan(cells,axis,fixed_name,target):
    ordered=sorted(cells,key=lambda r:r[axis])
    present=[i for i,r in enumerate(ordered) if r[target]>0]
    i=present[0] if present else None
    row=dict(regime=ordered[0]['regime'],axis=axis,fixed_variable=fixed_name,fixed_value=ordered[0][fixed_name],target=target,
        lower_tested=ordered[i-1][axis] if i is not None and i>0 else None,
        first_observed=ordered[i][axis] if i is not None else None,
        status='not_observed_in_range' if i is None else 'already_at_minimum_sample' if i==0 else 'bracketed',
        monotone_observed_presence=not any(ordered[j][target]>0 and ordered[j+1][target]==0 for j in range(len(ordered)-1)))
    changes=[]
    for a,b in zip(ordered,ordered[1:]):
        if a['outcome_counts']!=b['outcome_counts']:
            changes.append(dict(regime=a['regime'],axis=axis,fixed_variable=fixed_name,fixed_value=a[fixed_name],lower=a[axis],upper=b[axis],from_distribution=a['outcome_counts'],to_distribution=b['outcome_counts']))
    return row,changes

def aggregate(summaries):
    groups=defaultdict(list)
    for r in summaries:
        if r['group']=='primary':groups[r['regime'],r['evidence_strength'],r['frequency']].append(r)
    grid=[]
    for (regime,strength,f),rs in sorted(groups.items()):
        counts=Counter(r['classification'] for r in rs);eligible=[r for r in rs if r['qualifying_revision_count']]
        times=[r['time_to_relapse'] for r in rs if r['time_to_relapse'] is not None]
        grid.append(dict(regime=regime,strength=strength,frequency=f,seeds=len(rs),outcome_counts=json.dumps(dict(sorted(counts.items())),sort_keys=True),
            outcome=next(iter(counts)) if len(counts)==1 else 'mixed_across_seeds',
            rejection_rate=counts['C_rejection']/len(rs),relapse_rate=counts['E_relapse']/len(rs),
            persistent_escape_rate=counts['A_genuine_revision_candidate']/len(rs),
            qualifying_revision_rate=len(eligible)/len(rs),conditional_relapse_rate=counts['E_relapse']/len(eligible) if eligible else None,
            mean_T_relapse=mean(times),min_T_relapse=min(times) if times else None,max_T_relapse=max(times) if times else None,
            mean_D_pre=mean([r['D_pre'] for r in rs]),mean_D_immediate=mean([r['D_immediate_first'] for r in rs]),mean_D_final=mean([r['D_final'] for r in rs]),
            mean_D_post=mean([r['D_post'] for r in rs]),mean_delta_D=mean([r['delta_D'] for r in rs]),
            mean_acceptance_rate=mean([r['acceptance_rate'] for r in rs]),mean_rejection_rate=mean([r['rejection_rate'] for r in rs])))
    boundaries=[];transitions=[]
    for regime in CONFIG['regimes']:
        for axis,fixed,values in [('strength','frequency',CONFIG['frequencies']),('frequency','strength',CONFIG['strengths'])]:
            for value in values:
                cells=[r for r in grid if r['regime']==regime and r[fixed]==value]
                for target in ('qualifying_revision_rate','persistent_escape_rate'):
                    row,changes=boundary_scan(cells,axis,fixed,target);boundaries.append(row)
                    if target=='qualifying_revision_rate':transitions.extend(changes)
    return grid,boundaries,transitions

def coherence_diagnostic(features):
    rows=[]
    for scope in ('all_cells','boundary_0.58_0.59'):
        ss=[r for r in features if scope=='all_cells' or r['strength'] in CONFIG['coherence_boundary_strengths']]
        for regime in [*CONFIG['regimes'],'pooled']:
            subset=[r for r in ss if regime=='pooled' or r['regime']==regime]
            for feature in ('C_baseline_last20','C_early20','C_final20','C_early20_vector'):
                def key(r):return json.dumps(r[feature]) if isinstance(r[feature],list) else str(round(r[feature],12)) if r[feature] is not None else 'NA'
                def majority(rs):return sorted(Counter(r['classification'] for r in rs).items(),key=lambda x:(-x[1],x[0]))[0][0]
                correct=base_correct=0
                for seed in CONFIG['seeds']:
                    train=[r for r in subset if r['seed']!=seed];test=[r for r in subset if r['seed']==seed]
                    fallback=majority(train);mapping=defaultdict(list)
                    for r in train:mapping[key(r)].append(r)
                    for r in test:
                        predicted=majority(mapping[key(r)]) if key(r) in mapping else fallback
                        correct+=predicted==r['classification'];base_correct+=fallback==r['classification']
                labels=defaultdict(set)
                for r in subset:labels[key(r)].add(r['classification'])
                rows.append(dict(scope=scope,regime=regime,feature=feature,runs=len(subset),observed_accuracy=correct/len(subset),majority_baseline_accuracy=base_correct/len(subset),distinct_feature_values=len(labels),feature_values_with_multiple_outcomes=sum(len(x)>1 for x in labels.values()),interpretation='descriptive same-grid seed holdout; not independent generalization'))
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE/'results');args=ap.parse_args();out=args.output_dir;out.mkdir(exist_ok=True,parents=True)
    assert CONFIG['horizon']==C.HORIZON==120
    ref=C.load_reference();refhash=sha(CPATH/'reference.json')
    summaries=[];features=[];probe_rows=[]
    ts=Stream(out/'trajectories.csv');es=Stream(out/'events.csv')
    for regime in CONFIG['regimes']:
        for seed in CONFIG['seeds']:
            conditions=[('primary','grid',strength,f,'evidence_revision') for strength in CONFIG['strengths'] for f in CONFIG['frequencies']]
            conditions += [('control','C0_no_injection',None,0,None),('control','C1_ordinary_reference',None,3,'ordinary_gate')]
            for group,arm,strength,f,route in conditions:
                rid=f'{regime}_{seed}_{arm}_S{strength}_F{f}'
                rec=C.Recorder(rid,regime,seed,arm,strength,ref,random.Random(seed).uniform(.005,.04))
                rec.labels.update(group=group,frequency=f)
                n,anchor,probes,w=C.reach_attractor(rec)
                if arm=='C0_no_injection':
                    probe_rows.extend(dict(regime=regime,seed=seed,baseline_steps=n,**p) for p in probes)
                times=schedule(f)
                rec.snapshot('pre_injection',0,[],rec.beliefs['known'])
                for step in range(C.HORIZON+1):
                    if step>0:rec.normal_step('normal',step,n+step)
                    if step in times:
                        before=rec.beliefs['known']
                        event=rec.event('injection',step,ref.values[0],'independent_reference',route,strength)
                        rec.snapshot('injection',step,[event],before)
                row=C.summarize(rec,n,anchor,w,probes,times)
                row['schedule']=json.dumps(times);summaries.append(row)
                if group=='primary':
                    normal=[r for r in rec.trajectories if r['phase']=='normal'];baseline=[r for r in rec.trajectories if r['phase']=='baseline']
                    def cm(rs):return mean([r['C_internal'] for r in rs if r['C_internal'] is not None])
                    features.append(dict(run_id=rid,regime=regime,seed=seed,strength=strength,frequency=f,classification=row['classification'],
                        C_baseline_last20=cm(baseline[-20:]),C_early20=cm(normal[:20]),C_final20=cm(normal[-20:]),
                        C_early20_vector=[round(r['C_internal'],12) if r['C_internal'] is not None else None for r in normal[:20]]))
                ts.add(rec.trajectories);es.add(rec.events)
    ts.close();es.close()
    grid,boundaries,transitions=aggregate(summaries)
    dump(out/'summary.csv',summaries);dump(out/'phase_grid.csv',grid);dump(out/'boundary_estimates.csv',boundaries)
    dump(out/'adjacent_transitions.csv',transitions,['regime','axis','fixed_variable','fixed_value','lower','upper','from_distribution','to_distribution'])
    dump(out/'relapse_times.csv',[{k:r[k] for k in ('run_id','group','regime','seed','evidence_strength','frequency','classification','qualifying_revision_count','relapse_start_step','relapse_confirmation_step','time_to_relapse','time_to_relapse_from_last_injection','steps_after_last_injection')} for r in summaries])
    dump(out/'coherence_features.csv',[{**r,'C_early20_vector':json.dumps(r['C_early20_vector'])} for r in features])
    dump(out/'coherence_diagnostic.csv',coherence_diagnostic(features));dump(out/'attractor_checks.csv',probe_rows)
    assert sha(CPATH/'reference.json')==refhash
    execution=dict(command=shlex.join([sys.executable,*sys.argv]),python=platform.python_version(),native_julia=False,
        config=CONFIG,protocol_sha256=sha(HERE/'PROTOCOL.md'),config_sha256=sha(HERE/'config.json'),runner_sha256=sha(Path(__file__)),
        c_runner_sha256=sha(CPATH/'run_experiment.py'),reference_sha256=refhash,
        primary_cells=len(grid),primary_runs=sum(r['group']=='primary' for r in summaries),control_runs=sum(r['group']=='control' for r in summaries),
        runs=len(summaries),trajectory_rows=ts.count,events=es.count,
        baseline_steps=sum(r['baseline_steps'] for r in summaries),post_steps=sum(r['normal_post_steps'] for r in summaries),
        total_normal_steps=sum(r['baseline_steps']+r['normal_post_steps'] for r in summaries),
        primary_classifications=dict(Counter(r['classification'] for r in summaries if r['group']=='primary')),
        csv_sha256={p.name:sha(p) for p in sorted(out.glob('*.csv'))})
    (out/'execution.json').write_text(json.dumps(execution,indent=2)+'\n')
    print(json.dumps({k:execution[k] for k in ('primary_cells','primary_runs','control_runs','runs','trajectory_rows','events','total_normal_steps','primary_classifications')},indent=2))
if __name__=='__main__':main()
