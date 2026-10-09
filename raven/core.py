"""Independent research simulator (NOT the competition's official simulator)."""
from dataclasses import dataclass, replace
from itertools import combinations
from functools import lru_cache
import random, math

@dataclass(frozen=True)
class Member:
    id:int; age:int; zone:int; gender:int; goal:int; style:int
    lo:int; hi:int; zones:tuple; genders:tuple
    status:str; arrives:int; leaves:int


def world(seed,n=24,sparse=False,cold=False):
    rng=random.Random(seed); members=[]
    for i in range(n):
        age=rng.randrange(23,41); zone=rng.randrange(5 if sparse else 3)
        width=rng.choice((5,7,10,13)); lo=max(18,age-width); hi=min(65,age+width)
        zones=(zone,) if rng.random()<(0.85 if sparse else .58) else tuple(range(5 if sparse else 3))
        g=rng.randrange(2)
        genders=(1-g,) if rng.random()<.70 else (0,1)
        z=rng.random(); status='declined' if z<.06 else 'recoverable' if z<(.82 if cold else .65) else 'complete'
        day=rng.randrange(0,27); members.append(Member(i,age,zone,g,rng.randrange(3),rng.randrange(3),lo,hi,zones,genders,status,day,min(60,day+rng.randrange(20,42))))
    return members

def real_feasible(a,b):
    return (a.lo<=b.age<=a.hi and b.lo<=a.age<=b.hi and b.gender in a.genders and a.gender in b.genders and b.zone in a.zones and a.zone in b.zones)

def reward_est(a,b):
    return .07 + .17*(a.goal==b.goal)+.10*(a.style==b.style)+.08*(a.zone==b.zone)+.06*max(0,1-abs(a.age-b.age)/20)

def is_known(m, asked):return m.status=='complete' or (m.status=='recoverable' and m.id in asked)

def exact_match(ids, weights):
    """Exact max-weight match for <=18 active vertices; greedy safe fallback above."""
    if len(ids)>18:return greedy_match(weights)
    ix={v:i for i,v in enumerate(ids)}; neighbours={i:[] for i in range(len(ids))}
    for (a,b),w in weights.items():
        if a in ix and b in ix:neighbours[ix[a]].append((ix[b],w,a,b));neighbours[ix[b]].append((ix[a],w,a,b))
    @lru_cache(None)
    def dp(mask):
        if not mask:return (0.,())
        bit=mask & -mask; i=bit.bit_length()-1; rest=mask^bit; best=dp(rest)
        for j,w,a,b in neighbours[i]:
            if rest>>j&1:
                score,pairs=dp(rest^(1<<j))
                if score+w>best[0]+1e-11:best=(score+w,pairs+((min(a,b),max(a,b)),))
        return best
    return dp((1<<len(ids))-1)

def greedy_match(weights):
    used=set();pairs=[];value=0.
    for (a,b),w in sorted(weights.items(),key=lambda kv:kv[1],reverse=True):
        if w<=0 or a in used or b in used:continue
        used.add(a);used.add(b);pairs.append((a,b));value+=w
    return value,tuple(pairs)

def edges(members,active,asked,prior=None):
    m={x.id:x for x in members}; out={}
    for a,b in combinations(active,2):
        x,y=m[a],m[b]
        if not (is_known(x,asked) and is_known(y,asked)):continue
        if real_feasible(x,y):out[(a,b)]=reward_est(x,y)
    return out

def sample_profiles(members,asked,seed,prior):
    rng=random.Random(seed); sampled=[]
    for m in members:
        if m.id in asked and m.status=='recoverable':
            pool=[p for p in prior if p.gender==m.gender and abs(p.age-m.age)<=5 and p.zone==m.zone]
            if not pool:pool=prior
            x=rng.choice(pool)
            sampled.append(replace(m,lo=x.lo,hi=x.hi,zones=x.zones,genders=x.genders))
        else:sampled.append(m)
    return sampled

def clarification(members,active,asked,policy,prior,seed,budget=4):
    m={x.id:x for x in members}; candidates=[i for i in active if m[i].status=='recoverable' and i not in asked]
    if not candidates:return set()
    if policy=='none':return set()
    if policy=='fifo':return set(candidates[:budget])
    ranked=sorted(((reward_est(m[a],m[b]),a,b) for a,b in combinations(active,2) if m[a].status!='declined' and m[b].status!='declined'),reverse=True)
    if policy=='endpoints':
        selected=set()
        for _,a,b in ranked:
            required={i for i in (a,b) if i in candidates}-selected
            if len(selected)+len(required)<=budget:selected|=required
            if len(selected)>=min(len(candidates),budget):break
        return selected
    # A shallow-then-deep complementarity-aware portfolio search, with common random scenarios.
    def proxy(q):
        score=0.
        for w,a,b in ranked:
            if all(m[k].status=='complete' or k in asked or k in q for k in (a,b)):
                score+=w*.21
        return score
    shortlist=set(candidates)
    for _,a,b in ranked[:12]:shortlist.update(i for i in (a,b) if i in candidates)
    shortlist=sorted(shortlist,key=lambda i:sum(w for w,a,b in ranked if i in (a,b)),reverse=True)[:10]
    portfolios=[]
    for size in range(0,min(budget,len(shortlist))+1):
        portfolios.extend(combinations(shortlist,size))
    if policy=='singleton':
        selected=set()
        for _ in range(budget):
            base=proxy(selected)
            gains=sorted(((proxy(selected|{i})-base,i) for i in shortlist if i not in selected),reverse=True)
            if not gains or gains[0][0]<1e-10:break
            selected.add(gains[0][1])
        return selected
    portfolios.sort(key=lambda q:proxy(set(q)),reverse=True)
    shortlist_sets=[()] + portfolios[:8]
    # Force include complementary two-endpoint candidates missed by proxy.
    shortlist_sets+= [tuple(i for i in (a,b) if i in candidates) for _,a,b in ranked[:5]]
    best=(-1.,())
    for q in shortlist_sets:
        q=tuple(sorted(set(q)))
        if len(q)>budget:continue
        vals=[]
        for k in range(3):
            hypo=sample_profiles(members,set(q)|asked,seed+177*k+11,prior)
            vals.append(greedy_match(edges(hypo,active,asked|set(q)))[0])
        score=sum(vals)/len(vals)
        if policy=='persistent':
            # Light 7-day arrival opportunity approximation; no hidden future profiles.
            remaining=max(0,60-max(m[i].arrives for i in active))
            score+=.015*min(7,remaining)*sum(1 for i in q if m[i].leaves>min(60,m[i].arrives+7))
        if score>best[0]+1e-9:best=(score,q)
    return set(best[1])

def episode(seed,policy,n=24,sparse=False,cold=False):
    members=world(seed,n=n,sparse=sparse,cold=cold); prior=world(70000,n=500,sparse=sparse)
    rng=random.Random(seed+54321); asked=set(); occupied={}; used_pairs=set();qualifying=0;intros=0;spent=0;days_active=0
    for t in range(60):
        active=[x.id for x in members if x.arrives<=t<x.leaves and occupied.get(x.id,-1)<=t and x.status!='declined']
        if not active:continue
        days_active+=1
        chosen=clarification(members,active,asked,policy,prior,seed+19*t)
        asked|=chosen;spent+=3*len(chosen)
        candidates={pair:w for pair,w in edges(members,active,asked).items() if pair not in used_pairs}
        _,pairs=greedy_match(candidates)
        for a,b in pairs:
            p=candidates[(a,b)];success=rng.random()<p
            qualifying+=success;intros+=1;used_pairs.add((a,b))
            # Occupancy is delayed; a coarse proxy, NOT official timing dynamics.
            downtime=rng.randrange(4,11) if not success else rng.randrange(12,24)
            occupied[a]=t+downtime;occupied[b]=t+downtime
    return dict(seed=seed,policy=policy,scenario=('sparse' if sparse else 'cold' if cold else 'standard'),members=n,msmi=100*qualifying/n,qualified=qualifying,introductions=intros,clarification_cost=spent,days_active=days_active)
