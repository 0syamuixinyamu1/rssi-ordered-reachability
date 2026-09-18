#!/usr/bin/env python3
"""Exp C. Imports prior RSSI functions unchanged. Python synthetic execution."""
from __future__ import annotations
import argparse
import csv
from dataclasses import dataclass
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import random
import shlex
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('prior_rssi', ROOT/'run_experiments.py')
BASE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BASE)
TOL, EPS, MIN_GAIN, RELAPSE_MARGIN = .05, 1e-12, .1, .05
SEEDS, STRENGTHS = (7,17,29), (.25,.75,1.0)
HORIZON, WITHDRAWAL, RELAPSE_WINDOW = 120,100,5


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Reference:
    domain: tuple[str,...]
    values: tuple[float,...]
    weights: tuple[float,...]

    def distance(self, beliefs):
        if set(beliefs) != set(self.domain):
            raise ValueError('Reference domain must never shrink or expand')
        if not all(math.isfinite(beliefs[k]) and 0 <= beliefs[k] <= 1 for k in self.domain):
            raise ValueError('Invalid belief')
        return sum(w*abs(beliefs[k]-v) for k,v,w in zip(self.domain,self.values,self.weights))


def load_reference():
    d=json.loads((HERE/'reference.json').read_text())
    return Reference(tuple(d['domain']),tuple(d['values']),tuple(d['weights']))


def normal_batch(regime, step):
    if regime == 'stationary':
        return tuple(v for v,_ in BASE.fixture('frozen',1)[2][0])
    if regime == 'descending_bridge':
        return (1.0-((step-1)%40)/40, 0.0)
    raise ValueError(regime)


def period(regime):
    return 1 if regime == 'stationary' else 40


def gate_update(beliefs, value):
    # No Reference object, true-reference flag or evaluator is passed to policy.
    return BASE.offer(beliefs,'known',value,False,'gated',TOL)


def local_probes(regime, anchor):
    rows=[]
    probes=sorted({min(1,max(0,anchor+d)) for d in (-TOL/2,-TOL/4,0,TOL/4,TOL/2)})
    for phase in range(period(regime)):
        for probe in probes:
            b={'known':probe}
            for offset in range(1,period(regime)+1):
                for x in normal_batch(regime,phase+offset):
                    gate_update(b,x)
            rows.append(dict(phase=phase,probe=probe,returned_belief=b['known'],
                             passed=abs(b['known']-anchor)<=EPS))
    return rows


def stable_window(rows, window):
    if len(rows)<window:
        return False
    tail=rows[-window:]
    return (max(r['belief'] for r in tail)-min(r['belief'] for r in tail)<=EPS
            and all(r['state_delta']<=EPS for r in tail)
            and all(r['D']>=.5 for r in tail))


class Recorder:
    def __init__(self, run_id, regime, seed, arm, strength, ref, initial):
        self.labels=dict(run_id=run_id,regime=regime,seed=seed,arm=arm,evidence_strength=strength)
        self.ref=ref
        self.ref_hash=digest(HERE/'reference.json')
        self.beliefs={'known':initial}
        self.trajectories=[]
        self.events=[]
        self.accepted_total=0
        self.rejected_total=0

    def event(self, phase, step, value, source, route, strength=None):
        before=self.beliefs['known']
        d_before=self.ref.distance(self.beliefs)
        gate_would_accept=abs(value-before)<=TOL
        apparent=False
        compliance_revision=None
        response=''
        support=None
        collapse_returned=None
        if route=='ordinary_gate':
            accepted,agreement,_=gate_update(self.beliefs,value)
            decision='accepted' if accepted else 'ordinary_gate_rejection'
        else:
            policy='external_only' if route=='external_compliance' else 'evidence_revision'
            # Forced DELIVERY to the old handler; its update threshold stays intact.
            result=BASE.replay_a(policy,before,value,1.0 if policy=='external_only' else 0.0,
                                 0.0 if strength is None else strength,d_before)
            self.beliefs['known']=result['final_belief']
            response=result['response']
            apparent=result['apparent_correction']
            compliance_revision=result['compliance_internal_revision']
            support=result['support']
            collapse_returned=result['collapse_returned']
            accepted=bool(collapse_returned)
            agreement=1-abs(value-before)
            decision=('external_compliance' if apparent else 'already_correct' if d_before<=EPS
                      else 'evidence_revision' if accepted else 'evidence_threshold_rejection')
        after=self.beliefs['known']
        self.ref.distance(self.beliefs)
        row=dict(**self.labels,trajectory_id=len(self.trajectories)+1,phase=phase,step=step,
                 input_index=0,source=source,route=route,input_value=value,belief_before=before,
                 belief_after=after,D_before=d_before,D_after=self.ref.distance(self.beliefs),
                 delivered=True,bypass_normal_gate=route!='ordinary_gate',
                 normal_gate_would_accept=gate_would_accept,accepted=accepted,
                 rejected=decision.endswith('rejection'),decision=decision,
                 agreement_before_update=agreement,internal_revision=abs(after-before)>EPS,
                 compliance_internal_revision=compliance_revision,apparent_correction=apparent,
                 response=response,output_matches_R0=response==BASE.statement(self.ref.values[0]) if response else None,
                 support=support,collapse_returned=collapse_returned,reference_hash=self.ref_hash)
        self.events.append(row)
        return row

    def snapshot(self, phase, step, events, before):
        normal=[e for e in events if e['source']=='normal']
        accepted=sum(e['accepted'] for e in normal)
        rejected=len(normal)-accepted
        self.accepted_total+=accepted
        self.rejected_total+=rejected
        scores=[e['agreement_before_update'] for e in normal if e['accepted']]
        row=dict(**self.labels,trajectory_id=len(self.trajectories)+1,phase=phase,step=step,
                 belief=self.beliefs['known'],accepted_count=accepted,rejected_count=rejected,
                 accepted_total=self.accepted_total,rejected_total=self.rejected_total,
                 C_internal=BASE.mean_or_none(scores),
                 C_all_inputs=BASE.mean_or_none([e['agreement_before_update'] for e in normal]),
                 D=self.ref.distance(self.beliefs),acceptance_rate=accepted/len(normal) if normal else None,
                 rejection_rate=rejected/len(normal) if normal else None,
                 state_delta=abs(self.beliefs['known']-before),
                 external_delivery_count=sum(e['source']!='normal' for e in events),
                 reference_hash=self.ref_hash)
        self.trajectories.append(row)
        return row

    def normal_step(self, phase, step, global_step):
        before=self.beliefs['known']
        events=[]
        for i,value in enumerate(normal_batch(self.labels['regime'],global_step)):
            event=self.event(phase,step,value,'normal','ordinary_gate')
            event['input_index']=i
            events.append(event)
        return self.snapshot(phase,step,events,before)


def reach_attractor(rec):
    p=period(rec.labels['regime']);window=max(10,2*p)
    for t in range(1,401):
        rec.normal_step('baseline',t,t)
        if t%p or not stable_window(rec.trajectories,window):
            continue
        anchor=rec.beliefs['known']
        if abs(anchor-rec.ref.values[0])<.2:
            continue
        probes=local_probes(rec.labels['regime'],anchor)
        if all(r['passed'] for r in probes):
            return t,anchor,probes,window
    raise RuntimeError('Baseline did not meet preregistered attractor criteria')


def arms():
    yield 'C0_no_injection',None,(),None
    yield 'C1_ordinary_reference',None,(0,10,20),'ordinary_gate'
    for arm,schedule in [('T1_single',(0,)),('T2_repeated',(0,10,20))]:
        for strength in STRENGTHS:
            yield arm,strength,schedule,'evidence_revision'
    yield 'B_compliance_diagnostic',None,(0,),'external_compliance'


def relapse_blocks(normal, anchor, d_pre, after):
    candidates=[r for r in normal if r['step']>after]
    for i in range(len(candidates)-RELAPSE_WINDOW+1):
        w=candidates[i:i+RELAPSE_WINDOW]
        if all(abs(r['belief']-anchor)<=RELAPSE_MARGIN+EPS
               and r['D']>=d_pre-RELAPSE_MARGIN-EPS for r in w):
            return w[0]['step'],w[-1]['step']
    return None,None


def summarize(rec, baseline_steps,anchor,window,probes,schedule):
    normal=[r for r in rec.trajectories if r['phase']=='normal']
    external=[e for e in rec.events if e['source']!='normal']
    qualifying=[e for e in external if e['D_before']-e['D_after']>=MIN_GAIN-EPS]
    d_pre=abs(anchor-rec.ref.values[0])
    first_step=qualifying[0]['step'] if qualifying else None
    relapse_start,confirmation=relapse_blocks(normal,anchor,d_pre,first_step) if qualifying else (None,None)
    final_relapse=relapse_blocks(normal,anchor,d_pre,qualifying[-1]['step'])[0] if qualifying else None
    withdrawal=normal[-WITHDRAWAL:]
    persistent=bool(qualifying) and final_relapse is None and all(r['D']<=d_pre-MIN_GAIN+EPS for r in withdrawal)
    genuine=sum(all(r['D']<=e['D_before']-MIN_GAIN+EPS for r in normal if r['step']>e['step']) for e in qualifying)
    apparent=sum(e['apparent_correction'] for e in external)
    if persistent:
        classification='A_genuine_revision_candidate'
    elif qualifying and final_relapse is not None:
        classification='E_relapse'
    elif qualifying:
        classification='mixed_or_partial_escape'
    elif apparent:
        classification='B_external_compliance'
    elif any(e['D_before']>.2 and e['rejected'] for e in external):
        classification='C_rejection'
    else:
        classification='control_stable_no_injection'
    normals=[e for e in rec.events if e['phase']=='normal' and e['source']=='normal']
    d_post=sum(r['D'] for r in normal[-20:])/20
    injrows=[r for r in rec.trajectories if r['phase']=='injection']
    return dict(**rec.labels,baseline_steps=baseline_steps,attractor_belief=anchor,
                stable_window=window,local_probe_count=len(probes),local_probes_passed=all(r['passed'] for r in probes),
                D_pre=d_pre,D_immediate_first=injrows[0]['D'] if injrows else d_pre,
                D_immediate_last=injrows[-1]['D'] if injrows else d_pre,D_final=normal[-1]['D'],
                D_post=d_post,delta_D=d_post-d_pre,C_pre=next(r['C_internal'] for r in reversed(rec.trajectories) if r['phase']=='baseline'),
                C_post=BASE.mean_or_none([r['C_internal'] for r in normal[-20:] if r['C_internal'] is not None]),
                C_post_defined_steps=sum(r['C_internal'] is not None for r in normal[-20:]),
                normal_accepted=sum(e['accepted'] for e in normals),normal_rejected=sum(not e['accepted'] for e in normals),
                acceptance_rate=sum(e['accepted'] for e in normals)/len(normals),
                rejection_rate=sum(not e['accepted'] for e in normals)/len(normals),
                external_delivery_count=len(external),bypass_delivery_count=sum(e['bypass_normal_gate'] for e in external),
                external_update_accepted_count=sum(e['accepted'] for e in external),
                external_rejected_count=sum(e['rejected'] for e in external),
                actual_revision_count=sum(e['internal_revision'] for e in external),
                qualifying_revision_count=len(qualifying),genuine_revision_count=genuine,
                apparent_correction_count=apparent,relapse_observed=relapse_start is not None,
                relapse_rate_if_eligible=int(final_relapse is not None) if qualifying else None,
                relapse_start_step=relapse_start,relapse_confirmation_step=confirmation,
                time_to_relapse=relapse_start-first_step if relapse_start is not None else None,
                time_to_relapse_from_last_injection=relapse_start-schedule[-1] if relapse_start is not None and schedule else None,
                persistent_escape=persistent,persistent_escape_rate=int(persistent),
                normal_post_steps=len(normal),steps_after_last_injection=HORIZON-schedule[-1] if schedule else HORIZON,
                classification=classification,reference_corruption='not_available',reference_avoidance='not_available')


def write_csv(p, rows):
    if not rows:raise ValueError('Empty output')
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=HERE/'results')
    args=parser.parse_args();out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    ref=load_reference();ref_hash=digest(HERE/'reference.json')
    BASE.source_manifest()
    trajectories=[];events=[];summary=[];attractor_rows=[]
    failures=[]
    for regime in ('stationary','descending_bridge'):
        for seed in SEEDS:
            initial=random.Random(seed).uniform(.005,.04)
            for arm,strength,schedule,route in arms():
                sid='na' if strength is None else str(strength)
                rid=f'{regime}_{seed}_{arm}_{sid}'
                rec=Recorder(rid,regime,seed,arm,strength,ref,initial)
                try:
                    n,anchor,probes,window=reach_attractor(rec)
                except RuntimeError as e:
                    failures.append(dict(run_id=rid,error=str(e)))
                    trajectories.extend(rec.trajectories);events.extend(rec.events)
                    continue
                for p in probes:attractor_rows.append(dict(run_id=rid,regime=regime,seed=seed,baseline_steps=n,**p))
                rec.snapshot('pre_injection',0,[],rec.beliefs['known'])
                for step in range(HORIZON+1):
                    if step>0:rec.normal_step('normal',step,n+step)
                    if step in schedule:
                        before=rec.beliefs['known']
                        event=rec.event('injection',step,ref.values[0],'independent_reference',route,strength)
                        rec.snapshot('injection',step,[event],before)
                summary.append(summarize(rec,n,anchor,window,probes,schedule))
                trajectories.extend(rec.trajectories);events.extend(rec.events)
    write_csv(out/'trajectories.csv',trajectories)
    write_csv(out/'event_log.csv',events)
    write_csv(out/'summary.csv',summary)
    write_csv(out/'attractor_checks.csv',attractor_rows)
    aggregate=[]
    keys=sorted({(r['regime'],r['arm'],str(r['evidence_strength'])) for r in summary})
    for regime,arm,strength in keys:
        rs=[r for r in summary if (r['regime'],r['arm'],str(r['evidence_strength']))==(regime,arm,strength)]
        eligible=[r for r in rs if r['qualifying_revision_count']]
        aggregate.append(dict(regime=regime,arm=arm,evidence_strength=strength,runs=len(rs),
            classifications=';'.join(sorted({r['classification'] for r in rs})),
            mean_D_pre=sum(r['D_pre'] for r in rs)/len(rs),mean_D_post=sum(r['D_post'] for r in rs)/len(rs),
            mean_delta_D=sum(r['delta_D'] for r in rs)/len(rs),
            qualifying_runs=len(eligible),genuine_revision_count=sum(r['genuine_revision_count'] for r in rs),
            apparent_correction_count=sum(r['apparent_correction_count'] for r in rs),
            relapse_runs=sum(r['classification']=='E_relapse' for r in rs),
            relapse_rate=sum(r['classification']=='E_relapse' for r in eligible)/len(eligible) if eligible else None,
            relapse_rate_all_runs=sum(r['classification']=='E_relapse' for r in rs)/len(rs),
            persistent_escape_rate=sum(r['persistent_escape'] for r in rs)/len(rs),
            time_to_relapse=';'.join(str(x) for x in sorted({r['time_to_relapse'] for r in rs if r['time_to_relapse'] is not None}))))
    write_csv(out/'aggregate_summary.csv',aggregate)
    assert digest(HERE/'reference.json')==ref_hash
    meta=dict(execution='Python synthetic; prior offer/replay_a imported unchanged',native_julia=False,
              python=platform.python_version(),command=shlex.join([sys.executable,*sys.argv]),seeds=SEEDS,
              planned_runs=54,completed_runs=len(summary),baseline_failures=failures,
              trajectories=len(trajectories),events=len(events),reference_sha256=ref_hash,
              protocol_sha256=digest(HERE/'PROTOCOL.md'),runner_sha256=digest(Path(__file__)),
              prior_runner_sha256=digest(ROOT/'run_experiments.py'),
              csv_sha256={p.name:digest(p) for p in sorted(out.glob('*.csv'))})
    (out/'execution.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:meta[k] for k in ['execution','planned_runs','completed_runs','baseline_failures','trajectories','events']},indent=2))
    for r in aggregate:print(r['regime'],r['arm'],r['evidence_strength'],r['classifications'],
                              'D_post=',r['mean_D_post'],'relapse_t=',r['time_to_relapse'])
    if failures:sys.exit(2)


if __name__=='__main__':main()
