import numpy as np, pandas as pd, warnings, lightgbm as lgb
warnings.filterwarnings("ignore")
from .data import bal
from .degradation import trw, CMAP
rcs = bal()
rws,fts = trw(rcs)
mta = {m["session_key"]: m for _,m in rcs}
rws["stint_key"]=rws.session_key.astype(str)+"_"+rws.index.astype(str)
st=[]

for laps,m in rcs:
    l=laps[laps.clean][["driver","lap","stint"]].copy()
    l["session_key"]=m["session_key"]
    st.append(l)
st =pd.concat(st)
rw2=[]
for laps,m in rcs:
    sk=m["session_key"]
    if sk not in fts or fts[sk]["ref"]!="MEDIUM" or m["wet"]:
        continue
    f=fts[sk]
    d=laps[laps.clean & laps.compound.isin(f["comps"])&laps.driver.isin(f["driver"].keys())].copy()
    d["y"]=d.t-f["fuel"]*d.lap-d.driver.map(f["driver"])
    d=d[np.abs(d.y-d.y.median())<4]
    d["comp"]=d.compound.map(CMAP)
    d["track_temp"]=m["track_temp"]
    d["air_temp"]=m["air_temp"]
    d["session_key"]=sk
    d["date"]=m["date"]
    d["sid"]=d.driver.astype(str)+"_"+d.stint.astype(str)
    rw2.append(d)
R=pd.concat(rw2,ignore_index=True)
cid={c:i for i,c in enumerate(sorted(R.circuit.unique()))}
R["cid"]=R.circuit.map(cid)



def gbm(tr, te,fs, mn):
    g=lgb.LGBMRegressor(n_estimators=300, learning_rate=0.03, num_leaves=7, min_child_samples=200,reg_lambda=10, subsample=0.8, subsample_freq=1, monotone_constraints=mn, verbose=-1)
    g.fit(tr[fs], tr.y)
    return g.predict(te[fs])
def lin(tr,te,temp=False):
    p=np.zeros(len(te))
    for c in range(3):
        a=tr[tr.comp==c]
        b=te.comp==c
        if not b.any():
            continue
        cf = lambda d: [np.ones(len(d)), d.age]+([d.age*(d.track_temp-35)] if temp else [])
        w=np.linalg.lstsq(np.column_stack(cf(a)),a.y,rcond=None)[0]
        p[b.values]=np.column_stack(cf(te[b]))@w
    return p
def shk(tr,te,k=400):
    bs=lin(tr,te)
    p=bs.copy()
    for c in range(3):
        g=tr[(tr.comp==c)]
        A=np.column_stack([np.ones(len(g)),g.age])
