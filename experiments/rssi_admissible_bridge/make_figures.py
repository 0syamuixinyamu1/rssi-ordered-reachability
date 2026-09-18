#!/usr/bin/env python3
"""Scientific figures from saved F CSV only; no classification logic."""
import csv,json,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
H=Path(__file__).resolve().parent;R=H/'results';OUT=H/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':130})
BLUE='#2677ae';RED='#c5553a';GOLD='#bf8a2f';GREEN='#438b6f'
def read(n):return list(csv.DictReader((R/n).open()))
ss=read('bridge_summary.csv');tt=read('trajectories.csv');ee=read('events.csv')
def rows(cid,seed=7):return [r for r in tt if r['run_id']==f'{cid}_seed{seed}' and r['phase']=='normal']
def path(ax,cid,label,seed=7,**kw):
    a=rows(cid,seed);ax.plot([0]+[int(r['step']) for r in a],[1]+[float(r['belief']) for r in a],label=label,**kw)
def finish(fig,name):fig.tight_layout(rect=(0,0,1,.86) if fig._suptitle else None);fig.savefig(OUT/name,bbox_inches='tight');plt.close(fig)
# 1 actual state-input gate decisions
fig,ax=plt.subplots(figsize=(7.5,6));x=np.linspace(0,1,400);ax.fill_between(x,np.maximum(0,x-.05),np.minimum(1,x+.05),color=GREEN,alpha=.14,label='Nominal admissible band')
for flag,col,label in [('False',RED,'Rejected'),('True',BLUE,'Accepted')]:
    r=[e for e in ee if e['phase']=='normal' and e['seed']=='7' and e['accepted']==flag]
    ax.scatter([float(e['belief_before']) for e in r],[float(e['input_value']) for e in r],s=13,alpha=.45,color=col,label=label)
ax.plot(x,x,color='gray',lw=.6);ax.set(xlabel='Belief before input',ylabel='Offered input',title='Actual accepted / rejected transitions (seed 7)',xlim=(-.02,1.02),ylim=(-.02,1.02));ax.legend(loc='upper left');finish(fig,'admissible_transitions.png')
# 2 categorical spacing preserves nextafter neighbors
ids=['delta_0.025','delta_0.049','delta_0.0499','delta_nextbelow','delta_0.05','delta_nextabove','delta_0.0501','delta_0.051'];labels=['.025','.049','.0499','nextdown\n(.05)','.05','nextup\n(.05)','.0501','.051']
rates=[sum(s['target_reached']=='True' for s in ss if s['condition_id']==c)/5 for c in ids]
fig,ax=plt.subplots(figsize=(10,4.5));ax.bar(range(8),rates,color=[BLUE if r else RED for r in rates]);ax.set_xticks(range(8),labels);ax.set(ylim=(0,1.18),ylabel='Observed exact-target rate (5 seeds)',xlabel='Nominal delta; x[k] = max(0, 1 - k*delta)',title='Step size and exact target reachability')
for i,r in enumerate(rates):ax.text(i,r+.03,f'{round(5*r)}/5',ha='center')
finish(fig,'delta_reachability.png')
# 3 shortest witness
fig,ax=plt.subplots(figsize=(9,5));path(ax,'minimum_float_frontier','Binary64 frontier: 21 inputs',color=BLUE,marker='o',markersize=3);path(ax,'minimum_uniform21','Uniform 21 inputs',color=GREEN,ls='--');path(ax,'minimum_uniform20','Uniform 20: first input rejected',color=RED,ls=':')
ax.plot(range(21),[1-k/20 for k in range(21)],color=GOLD,ls='-.',label='Exact-real ideal: 20 steps')
ax.annotate('Frontier b[20] = 7.3205e-16 > 0\nb[21] = 0 exactly',xy=(20,0),xytext=(9,.33),arrowprops={'arrowstyle':'->'},bbox={'facecolor':'white','alpha':.9,'edgecolor':'gray'})
ax.set(xlim=(0,24),ylim=(-.03,1.06),xlabel='Ordinary input step',ylabel='Belief',title='Real lower bound vs binary64 minimum');ax.legend(loc='upper right',fontsize=9);finish(fig,'shortest_bridge.png')
# 4 deletion
fig,ax=plt.subplots(figsize=(9,5))
for cid,label,color in [('bridge_valid04','Complete .04 bridge',BLUE),('broken_early','Early deletion: final b=.96',RED),('broken_middle','Middle deletion: final b=.52',GOLD),('broken_late','Late deletion: final b=.08 (mixed)',GREEN),('broken_redundant_middle','Redundant .02 point removed: reaches 0','#8266a2')]:path(ax,cid,label,color=color)
ax.set(xlabel='Post-injection clock step (empty holds included)',ylabel='Belief',title='A point deletion blocks only when the remaining gap is inadmissible',xlim=(0,120),ylim=(-.03,1.03));ax.legend();finish(fig,'broken_bridges.png')
# 5 same multiset
fig,axs=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={'width_ratios':[1.5,1]})
for cid,label,col in [('control_E_gradual','Descending',BLUE),('order_ascending','Ascending',RED),('order_alternating','High / low alternating',GOLD),('order_shuffled','Seeded shuffle',GREEN)]:path(axs[0],cid,label,color=col)
axs[0].set(xlabel='Input step',ylabel='Belief',title='Identical 120-value multiset, seed 7');axs[0].legend()
w=next(r for r in read('order_acceptability.csv') if r['seed']=='7' and r['order_a']=='descending' and r['order_b']=='ascending')
axs[1].axis('off');axs[1].text(.02,.92,'Same input token: x = 0.95',fontsize=13,weight='bold',va='top')
axs[1].text(.02,.77,'Descending, step 2\nPrevious belief = 0.975\nGap < 0.05: accepted\n\nAscending, step 119\nPrevious belief = 1.0\nRounded gap = 0.050000000000000044\nGate rejects\n\nFirst aligned-step divergence: step 1',va='top',linespacing=1.55)
finish(fig,'same_multiset_order.png')
# 6 exposures
fig,axs=plt.subplots(2,1,figsize=(9,6.7),sharex=True)
for cid,label,col in [('control_abrupt0','120 zero inputs, no bridge',RED),('minimum_float_frontier','21-input complete bridge',BLUE)]:
    es=[r for r in ee if r['run_id']==f'{cid}_seed7' and r['phase']=='normal'];axs[0].plot([int(r['step']) for r in es],[float(r['input_value']) for r in es],'.-',color=col,label=label);path(axs[1],cid,label,color=col)
axs[0].set(ylabel='Offered input',title='Exposure count and reachable paths give different outcomes');axs[0].legend();axs[1].set(xlabel='Post-injection clock step',ylabel='Belief',xlim=(0,120));axs[1].text(34,.16,'Bridge ends at step 21; remaining steps have no inputs',fontsize=9);finish(fig,'exposure_vs_bridge.png')
# 7 graph: equal-angle node positions, not metric distances
allnodes=read('graph_nodes.csv');alledges=read('graph_edges.csv');gs=read('reachability_graph.csv');fig,axs=plt.subplots(1,3,figsize=(14,5))
for ax,gid in zip(axs,['uniform_n20_tol0.05','uniform_n40_tol0.05','witness_augmented_n40_tol0.05']):
    ns=[r for r in allnodes if r['graph_id']==gid];es=[r for r in alledges if r['graph_id']==gid];g=next(r for r in gs if r['graph_id']==gid);n=len(ns);theta=np.arange(n)*2*np.pi/n;coords=np.column_stack((np.cos(theta),np.sin(theta)));vs=[float(r['value']) for r in ns]
    for e in es:
        a,b=int(e['source']),int(e['target']);ax.plot(coords[[a,b],0],coords[[a,b],1],color='#b7c5ce',lw=.8,zorder=1)
    witness=json.loads(g['witness'])
    for a,b in zip(witness,witness[1:]):
        i,j=vs.index(a),vs.index(b);ax.plot(coords[[i,j],0],coords[[i,j],1],color=GOLD,lw=2,zorder=2)
    ax.scatter(coords[:,0],coords[:,1],s=15,color=BLUE,zorder=3)
    for val in [0.,1.]:
        i=vs.index(val);ax.scatter(*coords[i],s=40,color=RED,zorder=4);ax.text(*(coords[i]*1.15),str(int(val)),ha='center',va='center',weight='bold')
    title=f"{n} nodes, {g['component_count']} components\nShortest = {g['shortest_path_length'] or 'unreachable'}; count = {g['shortest_path_count']}"
    ax.set_title(title,fontsize=10);ax.set_aspect('equal');ax.axis('off')
fig.suptitle('Discrete graphs at tol=.05; gold = shortest witness\nNode placement is schematic, not a metric embedding',fontsize=12);finish(fig,'reachability_graph.png')
# supplementary geometry and noise
fig,axs=plt.subplots(1,2,figsize=(12,4.5))
for cid,label,col in [('geometry_monotone','Monotone: TV=1',BLUE),('geometry_detour','Detour: TV=1.5',GOLD),('geometry_oscillatory','Oscillatory: TV=2',GREEN),('geometry_random_connected','Random + endpoint connector',RED)]:path(axs[0],cid,label,color=col)
axs[0].set(xlabel='Clock step',ylabel='Belief',title='Admissible geometries, seed 7');axs[0].legend(fontsize=8)
lev=[0.,.001,.004,.006,.012];rr=[];cc=[]
for eta in lev:
    rows2=[s for s in ss if s['noise'] and float(s['noise'])==eta];rr.append(sum(s['target_reached']=='True' for s in rows2)/5);cc.append(sum(s['unordered_graph_path_exists']=='True' for s in rows2)/5)
axs[1].plot(lev,rr,'o-',color=BLUE,label='Exact target hit');axs[1].plot(lev,cc,'x--',color=GOLD,label='Offered-set graph connected');axs[1].set(xlabel='Interior noise amplitude',ylabel='Observed rate (5 seeds)',ylim=(-.05,1.1),title='Noise: edge loss and target reachability');axs[1].legend();finish(fig,'geometry_and_noise.png')
print(json.dumps({'figures':sorted(p.name for p in OUT.glob('*.png'))},indent=2))
