from __future__ import annotations
import numpy as np

CMP = ["SOFT", "MEDIUM", "HARD"]
GRN, SC, VSC = 0, 1, 2

DFT = dict(
    noise_sd=0.35,
    deg_unc=0.25,
    pit_sd=0.6,
    slow_stop_p=0.03,
    slow_stop_s=4.0,
    sc_len=4.0,
    vsc_len=2.0,
    traffic_p=0.25,
    traffic_loss=2.5,
    overtake_delta=0.8,
    sc_comppres=0.25,
    react_window=8,
    deg_unc_shared=0.0,
    level_unc=0.0,
)
def _sd(p,n,rng):
    N=p["laps"]
    st=np.zeros((n, N+2), np.int8)
    rm = np.zeros(n, int)
    kd = np.zeros(n, np.int8)
    u = rng.random((n, N+2))
    lsc = 2 + rng.poisson(max(p["sc_len"] - 2, 0.1), (n, N+2))
    lvs = 1 + rng.poisson(max(p["vsc_len"] - 1, 0.1), (n, N+2))
    for L in range(1, N+1):
        ac = rm > 0
        st[ac, L] = kd[ac]
        rm[ac] -= 1
        fr = ~ac & (L<N-1)
        nsc = fr & (u[:, L] < p["sc_hazard"]) 
        nvs = fr & ~nsc & (u[:, L] < p["sc_hazard"] + p["vsc_hazard"])
        for m, k, ln in ((nsc, SC, lsc), (nvs, VSC,  lvs)):
            st[m, L]=k
            kd[m]=k
            rm[m] = ln[m, L]-1
    return st
