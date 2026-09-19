from __future__ import annotations
import numpy as np
from .data import neutral_periods, pit_losses, fit_race, curve_from_fit, DRY
from .sim import GREEN, SC, VSC

TIER = {"Monte Carlo":3, "Hungaroring": 2, "Singpaore":2, "Imola":2,"Zandvoort": 2, "Suzuka": 2,
        "Catalunya": 1, "Melbourne": 1, "Silverstone": 1, "Montreal": 1, "Yas Marina Circuit": 1,
        "Mexico City": 1, "Spielberg": 1, "Lusail": 1, "Miami": 1, "Austin": 1, "Interlagos": 0,
        "Monza": 0, "Baku": 0, "Jeddah": 0, "Sakhir": 0, "Las Vegas": 0, "Spa-Francorchamps": 0, "Shanghai": 0}

OVERTAKE = [0.4, 0.8, 1.3, 2.5]
TRAFFIC_P = [0.15, 0.25, 0.35, 0.5]
TRAFFIC_LOSS = [1.5, 2.5, 3.5, 5.0]
MAX_STINT_RULE = {(2023, "Lusail"):18, (2025, "Lusail"):25}
STATUS_CODE = {"GREEN": GREEN, "SC": SC, "VSC": VSC}

def his(bef):
    per = {}
    g = dict(sc=0, vsc=0, laps=0, sc_len=[], vsc_len=[], pit=[], r_sc=[], r_vsc=[])
    for l, m in bef:
        c = per.setdefault(m["circuit"], dict(sc=0, vsc=0, laps=0, pit=[]))
        per_ = neutral_periods(m["status"])
        for k, a, b in per_:
            key = k.lower()
            c[key]+=1
            g[key]+=1
            g[key+"_len"].append(b-a+1)
        c["laps"]+=m["n_laps"]
        g["laps"]+=m["n_laps"]
        if m["wet"]:
            continue
        pl = pit_losses(l, m)
        if pl["GREEN"][0]:
            c["pit"].append(pl["GREEN"][0])
            g["pit"].append(pl["GREEN"][0])
            for k in ("SC","VSC"):
                if pl[k][0]:
                    g["r_"+k.lower()].append(pl[k][0]/pl["GREEN"][0])
def _shrink(vals, p, k=20):
    return (len(vals) * float(np.median(vals))+k * p)/ (len(vals)+k) if vals else p