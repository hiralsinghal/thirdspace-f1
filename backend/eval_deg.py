import numpy as np, pandas as pd, json, warnings
warnings.filterwarnings("ignore")
from .data import bal, cff
from .degradation import trw, DM, CMAP

def run():
    rs = bal()
    rw, fs=trw(rs)
    mb = {m["session_key"]: m for _, m in rs}
    cs = rw.circuit.unique()
    ra = []
    for sk in rw.session_key.unique():
        m = mb[sk]
        if m["year"]<2024:
            continue
        tr, te = rw[rw.date < m["date"]], rw[rw.session_key == sk]
        md = DM(cs).fit(tr)
        pg= md.predict(te, "gbm")
        pl = md.predict(te, "lin")
        pv = [(mm["date"], k) for k, mm in mb.items() if mm["circuit"]==m["circuit"] and mm["date"]< m["date"] and k in fs and fs[k]['ref']=="MEDIUM"]
        if pv: 
            f = fs[max(pv)[1]]
            iv={v:k for k,v in CMAP.items()}
            pp=np.array([cff(f,iv[c])[int(min(a,80))] if iv[c] in f["comps"]else q for c,a,q in zip(te.comp,te.age,pl)])
        else:
            pp=pl
        y=te.y.values
        ra.append(dict(year=m["year"], circuit=m["circuit"], n=len(te),gbm=np.mean(np.abs(y-pg)), lin=np.mean(np.abs(y-pl)), prev=np.mean(np.abs(y-pp))))
    r = pd.DataFrame(ra)
    w = r.n/r.n.sum()
    sm = {k: float((r[k]*w).sum()) for k in ["gbm", "lin", "prev"]}
    sm["races"]= len(r)
    sm["laps"]=int(r.n.sum())
    sm["gbm_beats_lin_pct"]=float((r.gbm < r.lin).mean()*100)
    sm["gbm_bears_prev_pct"]=float((r.gbm < r.prev).mean()*100)
    return r, sm

if __name__=="__main__":
    r, s=run()
    r.to_csv("results/deg_eval.csv", index=False)
    json.dump(s, open("results/deg_eval.json", "w"), indent=1)
    