#!/usr/bin/env python3
"""Exact static scientific figures from Exp E CSVs; not outcome classifiers."""
import csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
H=Path(__file__).resolve().parent;R=H/'results';O=H/'figures';O.mkdir(exist_ok=True)
with (R/'summary.csv').open() as f:rows=list(csv.DictReader(f))
with (R/'sequence_summary.csv').open() as f:agg=list(csv.DictReader(f))
with (R/'trajectories.csv').open() as f:traj=list(csv.DictReader(f))
cfg=json.loads((H/'config.json').read_text());P='#397cab';L='#c58935'
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def save(fig,name):fig.savefig(O/name,dpi=175);plt.close(fig)
families=sorted({r['family'] for r in rows});pers=[];rel=[];labels=[]
for fam in families:
 rs=[r for r in rows if r['family']==fam];labels.append(f'{fam} (n={len(rs)})');pers.append(sum(r['classification']=='A_genuine_revision_candidate' for r in rs));rel.append(sum(r['classification']=='E_relapse' for r in rs))
fig,ax=plt.subplots(figsize=(10,5.5),layout='constrained');y=np.arange(len(families))
ax.barh(y,pers,color=P,label='Persistent escape');ax.barh(y,rel,left=pers,color=L,label='Relapse');ax.set_yticks(y,labels);ax.set_xlabel('Observed trajectories (configured cells, not population samples)');ax.set_title('Exp E: sequence family outcomes');ax.legend();save(fig,'family_outcomes.png')
fig,axs=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
for v in cfg['v_values']:
 rs=sorted([r for r in agg if r['family']=='gradual_drift' and float(r['drift_v'])==v],key=lambda r:float(r['q_nominal']))
 for ax,metric in zip(axs,['persistent_escape_rate','relapse_rate']):ax.plot([float(r['q_nominal']) for r in rs],[float(r[metric]) for r in rs],marker='o',label=f'v={v:g}',alpha=.85)
for ax,title in zip(axs,['Persistent escape','Relapse']):ax.set(xlabel='q: old-directed offered input ratio',ylabel='Observed rate (5 seeds / cell)',title=title,ylim=(-.05,1.05));ax.grid(alpha=.2)
axs[1].legend(ncol=2,fontsize=9);fig.suptitle('Gradual drift: exposure boundaries depend on drift speed');save(fig,'q_outcome_rates.png')
fig,ax=plt.subplots(figsize=(9,4.5),layout='constrained')
for q in [.9,1.]:
 rs=sorted([r for r in agg if r['family']=='gradual_drift' and float(r['q_nominal'])==q and r['mean_time_to_relapse']],key=lambda r:float(r['drift_v']))
 ax.plot([float(r['drift_v']) for r in rs],[float(r['mean_time_to_relapse']) for r in rs],marker='o',label=f'q={q:g}')
ax.set(xlabel='v: input drift per clock step',ylabel='Time to relapse (steps)',title='Recapture accelerates until jumps stop being admitted');ax.text(.98,.95,'At q=1: no observed relapse for v=.051 or 1\nNA is not plotted as zero',transform=ax.transAxes,ha='right',va='top');ax.grid(alpha=.2);ax.legend();save(fig,'v_relapse_time.png')
# Condition selection uses declared parameters, not best-performing trajectory search.
def select(family,q='',v='',order=''):
 return next(r for r in rows if r['seed']=='7' and r['family']==family and r['q_nominal']==q and r['drift_v']==v and r['order']==order)
def path(row):return [r for r in traj if r['run_id']==row['run_id'] and r['phase']!='baseline']
def draw(ax,row,label,color=None,ls='-',metric='D'):
 rs=[r for r in path(row) if r[metric] and (metric=='D' or r['phase']=='normal')]
 ax.plot([int(r['step']) for r in rs],[float(r[metric]) for r in rs],label=label,color=color,ls=ls,lw=2)
fig,ax=plt.subplots(figsize=(10,5),layout='constrained')
for r,label,color,ls in [(select('stationary'),'Stationary',P,'--'),(select('descending_bridge'),'Original descending bridge',L,'-'),(select('no_input'),'No post inputs','#777777',':'),(select('gradual_drift','1.0','0.01'),'Slow drift v=.01, q=1','#8d59a2','-'),(select('gradual_drift','1.0','1.0'),'Abrupt path v=1, q=1','#328c67','--')]:draw(ax,r,label,color,ls)
ax.set(xlabel='Post-injection clock step',ylabel='D: distance to fixed reference',ylim=(-.04,1.04),title='Representative D trajectories (seed 7, S=1, single injection)');ax.legend();ax.grid(alpha=.2);save(fig,'representative_D.png')
fig,axs=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
for row,label in [(select('abrupt_return','0.5'),'O first'),(select('endpoint_order','0.5',order='R_first'),'R first'),(select('alternating','0.5'),'Alternating')]:draw(axs[0],row,label)
for row,label in [(select('gradual_drift','1.0','0.025'),'Descending'),(select('bridge_order','1.0','0.025','ascending'),'Ascending'),(select('bridge_order','1.0','0.025','shuffled'),'Shuffled')]:draw(axs[1],row,label)
for ax,title in zip(axs,['Endpoint multiset: q=.5','Bridge multiset: q=1']):ax.set(xlabel='Post-injection clock step',ylabel='D',title=title,ylim=(-.04,1.04));ax.grid(alpha=.2);ax.legend()
fig.suptitle('Identical values and counts; different order (seed 7)');save(fig,'order_effects.png')
fig,axs=plt.subplots(2,1,figsize=(10,7),sharex=True,layout='constrained')
for r,label,color in [(select('gradual_drift','1.0','0.01'),'Slow drift: missed early alarm','#8d59a2'),(select('gradual_drift','1.0','0.025'),'Bridge: early alarm',L),(select('noisy_corrective'),'Noisy corrective: false alarm',P)]:
 draw(axs[0],r,label,color,metric='D');draw(axs[1],r,label,color,metric='C_internal')
axs[0].set(ylabel='D',ylim=(-.04,1.04),title='Coherence can remain high during recapture (seed 7)');axs[1].set(ylabel='C (defined steps only)',xlabel='Post-injection clock step',ylim=(.94,1.005));axs[1].axhline(.99,color='gray',ls=':',label='Early mean alarm threshold .99')
for ax in axs:ax.grid(alpha=.2);ax.legend(loc='best',fontsize=9)
save(fig,'coherence_and_distance.png')
a=np.empty((len(cfg['v_values']),len(cfg['q_values'])))
for i,v in enumerate(cfg['v_values']):
 for j,q in enumerate(cfg['q_values']):a[i,j]=float(next(r for r in agg if r['family']=='gradual_drift' and float(r['drift_v'])==v and float(r['q_nominal'])==q)['relapse_rate'])
fig,ax=plt.subplots(figsize=(9,5),layout='constrained');im=ax.imshow(a,origin='lower',aspect='auto',cmap=ListedColormap([P,L]),vmin=0,vmax=1)
for i in range(len(cfg['v_values'])):
 for j in range(len(cfg['q_values'])):ax.text(j,i,'L' if a[i,j] else 'P',ha='center',va='center',color='white')
ax.set_xticks(range(len(cfg['q_values'])),cfg['q_values']);ax.set_yticks(range(len(cfg['v_values'])),cfg['v_values']);ax.set(xlabel='q',ylabel='v (sampled levels equally spaced)',title='Gradual drift: P = persistent, L = relapse (5/5 in every cell)');save(fig,'drift_q_outcomes.png')
print('Saved 7 figures')
