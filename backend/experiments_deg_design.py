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


