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