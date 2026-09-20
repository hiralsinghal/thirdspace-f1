from __future__ import annotations
import glob, json, os
import numpy as np
import pandas as pd

DRY = ["SOFT", "MEDIUM", "HARD"]
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

def lrc(y=None):
    rs= []
    for fp in sorted(glob.glob(os.path.join(RAW, "*.json"))):
        yr = int(os.path.basename(fp)[:4])
        if y and yr not in y:
            continue
        rs.append(fp)
    return rs

def load(p):
    return json.load(open(p))

def tst(rc, n):
    st =np.array(["GREEN"]*(n+2), dtype=object)
    ms = sorted(rc["race_control"], key=lambda x: x["date"])
    rd = any(x.get("flag")=="RED"for x in ms)
    ok, ol = None, None
    for x in ms:
        tx= x["message"].upper()
        lp=x.get("lap_number") or 1
        if x["category"] != "SafetyCar":
            continue
        if "VIRTUAL SAFETY CAR DEPLOYED"in tx:
            ok, ol = "VSC", lp
        elif "SAFETY CAR DEPLOYED" in tx:
            ok, ol = "SC", lp
        elif ("ENDING"in tx or "IN THIS LAP" in tx) and ok:
            st[ol:lp+1]=ok
            ok=None
    if ok:
        st[ol:min(ol+4, n)+1] = ok
    return st[: n+1], rd

def ntp(status):
    o, i = [], 1
    while i < len(status):
        if status[i] != "GREEN":
            j = i
            while j + 1 < len(status) and status[j+1] == status[i]:
                j += 1
            o.append((status[i], i, j))
            i = j + 1
        else:
            i += 1
    return o





def ltb(rc):
    ss = rc["session"]
    rs = {rw["driver_number"]: rw for rw in rc.get("session_result") or {}}
    L = pd.DataFrame(rc["laps"])
    if L.empty:
        return None, {}
    nl = int(max([rw.get("number_of_laps") or 0 for rw in rs.values()] + [L.lap_number.max()]))
    st, rd = tst(rc, nl)

    L = L[["driver_number", "lap_number", "is_pit_out_lap"]].rename(
        columns={"driver_number": "driver", "lap_number":"lap", "lap_duration": 
                 "t", "is_pit_out_lap": "pit_out"})
    L["pit_out"] = L["pit_out"].fillna(False).astype(bool)
    L = L.sort_values(["driver", "lap"]).reset_index(drop=True)

    sd = pd.DataFrame(rc["stints"])
    L["compound"], L["age"], L["stint"] = None, np.nan, np.nan
    for _, rw in sd.iterrows():
        if rw.lap_start is None or rw.lap_end is None:
            continue
        mk = (L.driver == rw.driver_number) & L.lap.between(rw.lap_start, rw.lap_end)
        L.loc[mk, "compound"] = (rw.compound or "UNKNOW").upper()
        L.loc[mk,"age"] = (rw.tyre_age_at_start or 0) + L.loc[mk, "lap"] - rw.lap_start + 1
        L.loc[mk, "stint"] = rw.stint_number

    no = L.groupby("driver")["pit_out"].shift(-1).astype("boolean").fillna(False).astype(bool)
    L["in_lap"]=no
    L["status"] = L.lap.map(lambda x: st[x] if x < len(st) else "GREEN")
    an = {e+1 for _, _, e in ntp(st)}
    L["restart"] = L.lap.isin(an)
    wt = bool(L.compound.isin(["INTERMEDIATE", "WET"]).mean()>0.02) or \
        any((wd.get("rainfall") or 0)> 0 for wd in rc["weather"])
    wd = pd.DataFrame(rc["weather"])
    md = dict(
        year=ss["year"], circuit=ss["circuit_short_name"], country=ss["country_name"],
        session_key=ss["session_key"], date=ss["date_start"], n_laps=nl, red=rd, wet=wt, 
        status=st, track_temp=float(wd.track_temperature.mean()) if len(wd) else np.nan,
        air_temp=float(wd.air_temperature.mean()) if len(wd) else np.nan,
        results=rs, drivers={d["driver_number"]: d for d in rc["drivers"]},

    )
    gl = L[(L.status=="GREEN") & L.t.notna()]
    mt = gl.t.median()
    L["clean"] = (
        (L.status == "GREEN") & ~L.pit_out & ~L.in_lap & ~L.restart & (L.lap > 1)
        & L.compound.isin(DRY) & L.t.between(0.97 * mt, 1.07 * mt) & (L.age >= 1)
    )
    return L, md



def frc(l, f=None):
    d = l[l.clean].copy()
    cs = [c for c in DRY if (d.compound == c).sum() >= 40]
    d = d[d.compound.isin(cs)]
    if len(cs) < 2 or len(d) < 150:
        return None
    rf = "MEDIUM" if "MEDIUM" in cs else cs[0]
    dv = sorted(d.driver.unique())

    def dsg(df):
        cl = [(df.driver == dr).astype(float).values for dr in dv]
        nm = [f"drv_{dr}" for dr in dv]
        for c in cs:
            m = (df.compound==c).astype(float).values
            if c != rf:
                cl.append(m)
                nm.append(f"off_{c}")
            cl += [m * df.age.values, m*df.age.values**2]
            nm += [f"b_{c}", f"q_{c}"]
        if f is None:
            cl.append(df.lap.values.astype(float).values)
            nm.append("lap")
        return np.column_stack(cl), nm


    kp = np.ones(len(d), bool)
    for _ in range(2):
        X, nm = dsg(d[kp])
        y = d.t.values[kp] - (0 if f is None else f * d.lap.values[kp])

        bt, *_ = np.linalg.lstsq(X, y, rcond=None)
        Xa, _ = dsg(d)
        ya = d.t.values - (0 if f is None else f * d.lap.values)
        r = ya - Xa @ bt
        ma = np.median(np.abs(r-np.median(r))) * 1.4826
        kp = np.abs(r) < 3 * ma
    cf = dict(zip(nm, bt))
    o = dict(ref=rf, comps=cs, fuel=cf.get("fuel", f), resid_sd=float(np.std(r[kp])), driver={dr: cf[f"drv_{dr}"] for dr in dv}, n=int(kp.sum()), support={c: int(d[d.compound == c].age.quantile(0.97) ) for c in cs})


    for c in cs:
        o[c] = dict(off=cf.get("off_{c}", 0.0), b=cf[f"b_{c}"], q=cf[f"q_{c}"])
    return o



def cff(ft, comp, ma=80):
    p = ft[comp]
    a = np.arrange(ma +1, dtype=float)
    y = p["off"] + p["b"] * a + p["q"] * a ** 2
    s = max(ft["support"][comp], 5)
    sl = max(p["b"] + 2*p["q"] * 5, 0.02)
    y[a>s]=y[s]+sl * (a[a>s]-s)
    return np.maximum.accumulate(y-y[0]+y[0])




def pls(l, m):
    o = {"GREEN": [], "SC": [], "VSC": []}
    sp = l[l.in_lap]
    for _, r in sp.iterrows():
        L = r.l
        pr = l[l.lap.isin([L,L+1])]
        tt = pr.groupby("driver").t.sum(min_count=2)
        pt = set(l[(l.lap.isin([L,L+1])) & (l.in_lap | l.pit_out)].driver)
        rf = tt[~tt.index.isin(pt)].dropna()
        ow = tt.get(r.driver, np.nan)
        if len(rf)<5 or np.isnan(ow) or L<2:
            continue
        ls = ow - rf.median()
        kd = m["status"][L] if L < len(m["status"]) else "GREEN"
        if 8 < ls < 60:
            o[kd].append(ls)
    return {k: (float(np.median(v)) if v else None, len(v)) for k, v in o.items()
}






def acs(l, dri, n):
    d = l[l.driver == dri].sort_values("lap")
    if d.empty:
        return None
    cs, ps = [], []
    for sn, g in d.groupby("stint", sort=True):
        cs.append(g.compound.iloc[0])
        ps.append(int(g.lap.max()))
    ps = ps[:-1]
    return cs, ps



def bal(years=None, verbose=False):
    rs = []
    for f in lrc(years):
        rc = load(f)
        L, md = ltb(rc)
        if L is None:
            continue
        L["year"], L["circuit"] = md["year"], md["circuit"]
        rs.append((L, md))
    rs.sort(key=lambda x: x[1]["date"])
    return rs



