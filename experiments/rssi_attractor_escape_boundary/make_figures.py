#!/usr/bin/env python3
"""Static figures from saved D results. Never used for outcome decisions."""
import csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap,BoundaryNorm
H=Path(__file__).resolve().parent;R=H/'results';O=H/'figures';O.mkdir(exist_ok=True)
config=json.loads((H/'config.json').read_text());S=config['strengths'];F=config['frequencies'];regimes=config['regimes']
with (R/'phase_grid.csv').open() as f:grid=list(csv.DictReader(f))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
colors=['#b85252','#e0a136','#26887a'];names=['Rejection','Relapse','Persistent escape']
codes=dict(zip(['C_rejection','E_relapse','A_genuine_revision_candidate'],range(3)))
def matrix(regime,field):
 a=np.full((len(S),len(F)),np.nan)
 for r in grid:
  if r['regime']==regime:a[S.index(float(r['strength'])),F.index(int(r['frequency']))]=codes[r[field]] if field=='outcome' else float(r[field]) if r[field] else np.nan
 return a
def maps(field,title,filename,kind='rate'):
 fig,axs=plt.subplots(1,2,figsize=(11,7),layout='constrained')
 for ax,regime in zip(axs,regimes):
  a=matrix(regime,field)
  if kind=='outcome':im=ax.imshow(a,origin='lower',aspect='auto',cmap=ListedColormap(colors),norm=BoundaryNorm([-.5,.5,1.5,2.5],3))
  else:
   cm=plt.colormaps['viridis'].copy();cm.set_bad('#dddddd')
   im=ax.imshow(a,origin='lower',aspect='auto',cmap=cm,vmin=0 if kind=='rate' else 39,vmax=1 if kind=='rate' else 79)
  for i in range(len(S)):
   for j in range(len(F)):
    value=a[i,j];text='NA' if np.isnan(value) else ['R','L','P'][int(value)] if kind=='outcome' else f'{value:g}'
    ax.text(j,i,text,ha='center',va='center',fontsize=9,color='black' if np.isnan(value) or kind=='outcome' else 'white' if value<(0.55 if kind=='rate' else 65) else 'black')
  ax.set_xticks(range(len(F)),F);ax.set_yticks(range(len(S)),[f'{s:g}' for s in S]);ax.set_xlabel('F: deliveries in steps 0-20');ax.set_ylabel('S: evidence strength');ax.set_title(regime.replace('_',' ').title())
 if kind=='outcome':
  cb=fig.colorbar(im,ax=axs,ticks=range(3),shrink=.65);cb.ax.set_yticklabels(names)
 else:fig.colorbar(im,ax=axs,shrink=.7,label='Observed rate (5 seeds)' if kind=='rate' else 'Steps from first qualifying revision')
 fig.suptitle(title+'\nSampled S levels shown with equal spacing',fontsize=13)
 fig.savefig(O/filename,dpi=170);plt.close(fig)
maps('outcome','Exp D: outcome map','outcome_map.png','outcome')
maps('persistent_escape_rate','Exp D: persistent escape rate','persistent_escape_rate.png')
maps('relapse_rate','Exp D: relapse rate (all runs per cell)','relapse_rate.png')
maps('mean_T_relapse','Exp D: time to relapse (NA = not observed)','relapse_time_map.png','time')
fig,ax=plt.subplots(figsize=(9,4.5),layout='constrained')
for f in F:
 rs=sorted([r for r in grid if r['regime']=='descending_bridge' and int(r['frequency'])==f and r['mean_T_relapse']],key=lambda r:float(r['strength']))
 ax.plot([float(r['strength']) for r in rs],[float(r['mean_T_relapse']) for r in rs],marker='o',label=f'F={f}',alpha=.85)
ax.set(title='Descending bridge: delay is not persistent escape',xlabel='S: evidence strength',ylabel='Time to relapse (steps)',ylim=(30,90));ax.grid(alpha=.2);ax.legend(ncol=3)
fig.savefig(O/'relapse_time_curves.png',dpi=170);plt.close(fig)
# Keep only declared representative trajectories while streaming the large CSV.
selected=[(.58,3,'S=.58, F=3','#b85252','--'),(.59,3,'S=.59, F=3','#26887a','-'),(1.,1,'S=1, F=1','#4879b3',':'),(1.,16,'S=1, F=16','#8b4a9e','-')]
paths={}
with (R/'trajectories.csv').open() as f:
 for r in csv.DictReader(f):
  if r['group']!='primary' or r['seed']!='7' or r['phase']=='baseline':continue
  key=(r['regime'],float(r['evidence_strength']),int(r['frequency']))
  if any(key[1]==s and key[2]==fr for s,fr,*_ in selected):paths.setdefault(key,[]).append(r)
fig,axs=plt.subplots(2,2,figsize=(12,7),sharex=True,layout='constrained')
for j,regime in enumerate(regimes):
 for s,f,label,color,ls in selected:
  rs=paths[(regime,s,f)];axs[0,j].plot([int(r['step']) for r in rs],[float(r['D']) for r in rs],color=color,ls=ls,label=label,lw=2)
  ns=[r for r in rs if r['phase']=='normal' and r['C_internal']]
  axs[1,j].plot([int(r['step']) for r in ns],[float(r['C_internal']) for r in ns],color=color,ls=ls,lw=2)
 axs[0,j].set_title(regime.replace('_',' ').title());axs[1,j].set_xlabel('Post-injection ordinary steps')
 for k in range(2):axs[k,j].grid(alpha=.2);axs[k,j].set_ylim(-.04,1.04);axs[k,j].axvspan(0,20,color='gray',alpha=.07)
axs[0,0].set_ylabel('D: reference distance');axs[1,0].set_ylabel('C: accepted-input agreement')
axs[0,0].legend(fontsize=9,loc='center right');fig.suptitle('Boundary trajectories and coherence (seed 7; shading = injection window)')
fig.savefig(O/'boundary_trajectories.png',dpi=170);plt.close(fig)
with (R/'coherence_diagnostic.csv').open() as f:diag=list(csv.DictReader(f))
fig,ax=plt.subplots(figsize=(10,4.8),layout='constrained')
features=['C_baseline_last20','C_early20','C_final20','C_early20_vector'];x=np.arange(4)
for j,regime in enumerate(regimes):
 vals=[float(next(r for r in diag if r['scope']=='boundary_0.58_0.59' and r['regime']==regime and r['feature']==feature)['observed_accuracy']) for feature in features]
 ax.bar(x+(j-.5)*.34,vals,width=.34,label=regime.replace('_',' '))
ax.axhline(.5,color='gray',ls='--',label='Majority baseline');ax.set_xticks(x,['Baseline C mean','Early C mean','Final C mean','Early C vector']);ax.set_ylim(0,1.12);ax.set_ylabel('Observed label agreement');ax.set_title('Near-boundary coherence diagnostic: S=.58/.59\nSeed holdout repeats the same grid; not an independent generalization test');ax.legend(loc='lower right')
fig.savefig(O/'coherence_diagnostic.png',dpi=170);plt.close(fig)
print('Saved 7 figures')
