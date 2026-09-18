#!/usr/bin/env python3
"""Plot preserved trajectories; no simulation or parameter changes."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
with (HERE/'results/trajectories.csv').open() as f:rows=list(csv.DictReader(f))
fig,ax=plt.subplots(2,2,figsize=(12,7),sharex=True)
styles=[('C0_no_injection','','No injection','#656565','--'),('T1_single','0.75','Single, strength .75','#087f8c','-'),('T2_repeated','0.75','Repeated, strength .75','#da8b00',':'),('T2_repeated','1.0','Repeated, strength 1','#8b4a9e','-')]
for j,regime in enumerate(('stationary','descending_bridge')):
 for arm,strength,label,color,ls in styles:
  rs=[r for r in rows if r['regime']==regime and r['seed']=='7' and r['arm']==arm and r['evidence_strength']==strength and r['phase']!='baseline']
  ax[0,j].plot([int(r['step']) for r in rs],[float(r['D']) for r in rs],color=color,ls=ls,label=label,lw=2)
  ns=[r for r in rs if r['phase']=='normal' and r['C_internal']]
  ax[1,j].plot([int(r['step']) for r in ns],[float(r['C_internal']) for r in ns],color=color,ls=ls,lw=1.5)
 ax[0,j].set_title(regime.replace('_',' ').title())
 for k in range(2):
  ax[k,j].set_ylim(-.04,1.04);ax[k,j].grid(alpha=.2)
  for x in (0,10,20):ax[k,j].axvline(x,color='black',alpha=.12,lw=1)
 ax[1,j].set_xlabel('Ordinary steps after initial injection')
ax[0,0].set_ylabel('D: distance to independent R0')
ax[1,0].set_ylabel('C: accepted-input agreement')
fig.suptitle('Exp C: correction can persist or relapse under the unchanged gate',fontsize=14)
fig.legend(*ax[0,0].get_legend_handles_labels(),loc='lower center',ncol=4,frameon=False)
fig.tight_layout(rect=(0,.07,1,.95))
fig.savefig(HERE/'results/trajectories.png',dpi=180)
