import argparse,csv,statistics,time
from pathlib import Path
from raven.core import episode

def main():
    p=argparse.ArgumentParser();p.add_argument('--seeds',type=int,default=12);p.add_argument('--members',type=int,default=24);p.add_argument('--output',default='results/episodes.csv');a=p.parse_args()
    policies=('none','fifo','endpoints','singleton','portfolio','persistent'); rows=[];start=time.perf_counter()
    for scenario in ('standard','sparse','cold'):
        for seed in range(a.seeds):
            for policy in policies:
                rows.append(episode(20261009+seed,policy,n=a.members,sparse=scenario=='sparse',cold=scenario=='cold'))
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    print('Independent synthetic simulator; results are NOT official MSMI benchmark scores.')
    print('scenario        policy       mean proxy-MSMI    mean introductions   mean ask cost')
    for scenario in ('standard','sparse','cold'):
        for policy in policies:
            z=[r for r in rows if r['scenario']==scenario and r['policy']==policy]
            print(f'{scenario:14s} {policy:12s} {statistics.mean(r["msmi"] for r in z):8.3f} {statistics.mean(r["introductions"] for r in z):15.2f} {statistics.mean(r["clarification_cost"] for r in z):13.2f}')
    print('Saved:',path,'elapsed_s=',round(time.perf_counter()-start,1))
if __name__=='__main__':main()
