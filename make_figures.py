import csv,argparse,statistics
from pathlib import Path
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('--input',default='results/episodes.csv');a=p.parse_args()
with open(a.input) as f:rows=list(csv.DictReader(f))
labels=['none','fifo','endpoints','singleton','portfolio','persistent']; scenarios=['standard','sparse','cold']
fig,ax=plt.subplots(figsize=(10,5))
x=list(range(len(labels)))
for j,s in enumerate(scenarios):
    values=[statistics.mean(float(r['msmi']) for r in rows if r['scenario']==s and r['policy']==policy) for policy in labels]
    ax.plot(x,values,marker='o',label=s)
ax.set_xticks(x,labels,rotation=25);ax.set_ylabel('Mean synthetic proxy-MSMI per 100 members');ax.set_title('Independent RAVEN research sandbox (not official evaluator)');ax.legend();ax.grid(alpha=.2)
fig.tight_layout();out=Path(a.input).parent/'proxy_msmi.png';fig.savefig(out,dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(10,5))
for s in scenarios:
    values=[statistics.mean(float(r['clarification_cost']) for r in rows if r['scenario']==s and r['policy']==policy) for policy in labels]
    ax.plot(x,values,marker='o',label=s)
ax.set_xticks(x,labels,rotation=25);ax.set_ylabel('Mean clarification units over 60 days');ax.set_title('Question usage across synthetic scenarios');ax.legend();ax.grid(alpha=.2);fig.tight_layout();out2=Path(a.input).parent/'clarification_cost.png';fig.savefig(out2,dpi=160);plt.close(fig)
print(out,out2)
