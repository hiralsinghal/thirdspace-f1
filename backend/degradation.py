from __future__ import annotations
import numpy as np, pandas as pd, lightgbm as lgb
from .data import frc, cff

CMAP = {"SOFT":0, "MEDIUM":1, "HARD":2}




def trw(races):
    rw, fs = [], {}
    for L, md in races:
        if md["wet"] or md["red"]:
            pass
        if md["wet"]:
            continue
        ft = frc(L)
        if ft is None:
            continue
        fs[md["session_key"]] = ft
        if ft["ref"] != "MEDIUM":
            continue
        d = L[L.clean & L.compound.isin(ft["comps"]) & L.driver.isin(ft["driver"].keys())].copy()
        d["y"] = d.t - ft["fuel"] * d.lap - d.driver.map(ft["driver"])
        d = d[np.abs(d.y - d.y.median())<4]
        d["comp"]=d.compound.map(CMAP)
        d["track_temp"] = md["track_temp"]

        d["air_temp"] = md["air_temp"]
        d["session_key"] = md["session_key"]
        d["date"] = md["date"]
        rw.append(d[["session_key", "date", "circuit", "year", "comp","age","track_temp","air_temp","y"]])
    return pd.concat(rw, ignore_index=True), fs


class DM:
    def __init__(self, cs, kind="hybrid"):
        self.cid = {c:i for i,c in enumerate(sorted(cs))}
        self.kind = kind
    def _X(self, dx):
        X = dx.copy()
        X["circuit_id"] = X.circuit.map(self.cid).fillna(-1).astype(int)
        return X[self.FEATS]
    def fit(self,tr):
        self.train = tr
        self.gbm = lgb.LGBMRegressor(n_estimators=300, learning_rate=0.03, num_leaves=7, min_child_samples=200, subsample=0.8, subsample_freq=1, reg_lambda=10.0, monotone_constraints=[0,1,0,0,0], verbose=-1)
        self.gbm.fit(self._X(tr), tr.y)
        self.lin = {}
        for c, g in tr.groupby("comp"):
            self.lin[c] = np.linalg.lstsq(np.column_stack([np.ones(len(g)), g.age]), g.y, rcond=None)[0]
        self.support = tr.groupby("comp").age.quantile(0.97).to_dict()
        return self
    def _lin_w(self,c, circuit):
        wg = self.lin[c]
        g = self.train[(self.train.comp==c)&(self.train.circuit==circuit)]
        if len(g)<30:
            return wg
        wc = np.linalg.lstsq(np.column_stack([np.ones(len(g)), g.age]), g.y, rcond=None)[0]
        lm = len(g)/(len(g) + self.SHRINK_K)
        return lm*wc + (1-lm)*wg