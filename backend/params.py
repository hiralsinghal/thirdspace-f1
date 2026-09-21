from __future__ import annotations
import numpy as np
from .data import frc, ntp,pls,cff, DRY
from .sim import GRN, SC, VSC

TIER = {"Monte Carlo":3, "Hungaroring": 2, "Singpaore":2, "Imola":2,"Zandvoort": 2, "Suzuka": 2,
        "Catalunya": 1, "Melbourne": 1, "Silverstone": 1, "Montreal": 1, "Yas Marina Circuit": 1,
        "Mexico City": 1, "Spielberg": 1, "Lusail": 1, "Miami": 1, "Austin": 1, "Interlagos": 0,
        "Monza": 0, "Baku": 0, "Jeddah": 0, "Sakhir": 0, "Las Vegas": 0, "Spa-Francorchamps": 0, "Shanghai": 0}

OVT = [0.4, 0.8, 1.3, 2.5]
TFP = [0.15, 0.25, 0.35, 0.5]
TFL = [1.5, 2.5, 3.5, 5.0]
MSR = {(2023, "Lusail"):18, (2025, "Lusail"):25}
STC = {"GREEN": GRN, "SC": SC, "VSC": VSC}


def his(bef):
    per = {}
    g = dict(sc=0, vsc=0, laps=0, sc_len=[], vsc_len=[], pit=[], r_sc=[], r_vsc=[])
    for l, m in bef:
        c = per.setdefault(m["circuit"], dict(sc=0, vsc=0, laps=0, pit=[]))
        per_ = ntp(m["status"])
        for k, a, b in per_:
            key = k.lower()
            c[key]+=1
            g[key]+=1
            g[key+"_len"].append(b-a+1)
        c["laps"]+=m["n_laps"]
        g["laps"]+=m["n_laps"]
        if m["wet"]:
            continue
        pl = pls(l, m)
        if pl["GREEN"][0]:
            c["pit"].append(pl["GREEN"][0])
            g["pit"].append(pl["GREEN"][0])
            for k in ("SC","VSC"):
                if pl[k][0]:
                    g["r_"+k.lower()].append(pl[k][0]/pl["GREEN"][0])

def _shrink(vals, p, k=20):
    return (len(vals) * float(np.median(vals))+k * p)/ (len(vals)+k) if vals else p



sc_ratio = lambda g: float(np.clip(_shrink(g["r_sc"], 0.55), 0.35, 0.9))
vsc_ratio = lambda g: float(np.clip(_shrink(g["r_vsc"], 0.65), 0.4, 0.95))


def ex_ante(m, per, g, deg ):
    N, circ = m["n_laps"], m["circuit"]
    c = per.get(circ, dict(sc=0, vsc=0, laps=0, pit=[]))
    r = MSR.get((m["year"], circ))
    if r :
        caps = {c:min(v, r) for c,v in caps.items()}
    pit = float(np.median(c["pit"])) if c["pit"] else 0
    tier = TIER.get(circ,1)
    return dict(
        laps=N, curve=c, caps=caps, pit_loss=pit, pit_loss_sc=pit*sc_ratio(g), pit_loss_vsc=pit*vsc_ratio(g),sc_hazard=r("sc"),vsc_hazard=r("vsc"), sc_len=float(np.mean(g["sc_len"])) if g["sc_len"] else 4.0, vsc_len=float(np.mean(g["vsc_len"])) if g["vsc_len"] else 2.0, OVT_delta=OVT[tier], TFP=TFP[tier], TFL=TFL[tier],tier=tier)




def tru(laps, md, ante):
    ft=frc(laps)
    if ft is None:
        return None
    cv, im = {}, []
    for c in DRY:
        if c in ft["comps"]:
            cv[c] = cff(ft, c)
    rf = ft["ref"]
    for c in DRY:
        if c not in cv:
            cv[c] = ante["curves"][c] - ante["curves"][rf][1] + cv[rf][1]
            im.append(c)
    pl = pls(laps, md)
    gr = pl["GREEN"][0] or ante["pit_loss"]
    st= np.array([STC[s] for s in md["status"]]+[GRN], np.int8)
    return dict(ante, curves=cv, pit_loss=gr, pit_loss_sc=gr*float(np.clip(pl["SC"][0]/ gr if pl["SC"][1]>=3 else ante["pit_loss_sc"]/ante["pit_loss"], 0.35, 0.9)),
                pit_loss_vsc=gr*float(np.clip(pl["VSC"][0]/ gr if pl["VSC"][1]>=3 else ante["pit_loss_vsc"]/ante["pit_loss"], 0.4, 0.95)), caps={c:80 for c in DRY}), st, ft, im