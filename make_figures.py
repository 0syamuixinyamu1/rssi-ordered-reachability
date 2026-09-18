"""Optional static research figure; requires matplotlib, not needed for experiments."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
with (ROOT/'results/b_trajectories.csv').open() as f:
    rows = list(csv.DictReader(f))

def select(name, tol=.05):
    return [r for r in rows if r['fixture'] == name and r['policy'] == 'gated' and float(r['tol']) == tol]

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'axes.titleweight':'bold'})
fig, axes = plt.subplots(1, 3, figsize=(13,4.6))
for ax,name,title in zip(axes,['frozen','drift_away','bridge'],
                        ['A frozen belief can look consistent','Agreement rises while error grows','Small steps can escape the gate']):
    sub=select(name)
    x=[int(r['step']) for r in sub]
    ax.plot(x,[float(r['accepted_agreement']) for r in sub],color='#2563eb',label='Accepted agreement (higher)')
    ax.plot(x,[float(r['reference_error']) for r in sub],color='#dc2626',linestyle='--',label='Reference error (lower)')
    ax.plot(x,[float(r['coverage']) for r in sub],color='#6b7280',linestyle=':',label='Coverage')
    ax.set_title(title,fontsize=10,pad=13)
    ax.set_xlabel('Step')
    ax.set_ylim(-.03,1.05)
    ax.set_xlim(1,80)
    ax.grid(axis='y',alpha=.2)
axes[0].set_ylabel('Score / fraction')
handles,labels=axes[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='lower center',ncol=3,bbox_to_anchor=(.5,.05),frameon=False)
fig.suptitle('Experiment B | Fixed reference, declared gate model, tolerance = 0.05',fontsize=14,y=.99)
fig.text(.5,.015,'Synthetic trajectories. Accepted agreement is defined by this experiment; it is not a native Hoho coherence metric.',ha='center',fontsize=9,color='#555555')
fig.subplots_adjust(left=.065,right=.985,bottom=.26,top=.8,wspace=.3)
fig.savefig(ROOT/'results/experiment_b.png',dpi=180)
