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


class _C:
    def __init__(self, p, s,n, rng, dm, nz, lvl=None):
        self.p = p
        self.n = n
        k = len(s["pits"])
        self.comps = np.array([CMP.index(c) for c in s["comps"]])
        self.pits = np.tile(np.array(s["pits"]+ [10**6], float), (n, 1))
        self.nxt = np.zeros(n, int)
        self.age = np.ones(n, int) if not s.get("start_age") else np.full(n, s["start_age"])
        self.comp = np.full(n, self.comps[0])
        self.k = k
        self.deg_mult, self.noise = dm, nz
        self.T = np.zeros(n)
        self.pit_noise = rng.normal(0, p["pit_sd"], (n, k + 1)) + \
            (rng.random((n, k + 1)) < p["slow_stop_p"]) * p["slow_stop_s"]
        self.traffic = (rng.random((n, k+1)) < p["traffic_p"]) * p["traffic_loss"]
        self.caps = np.array([p["caps"][c] for c in CMP])
        self.curves = np.stack([p["curves"][c] for c in CMP])
        self.n_stops = np.zeros(n, int)
        self.lvl = lvl if lvl is not None else np.zeros((n, 3))

    def react(self, L, st, rc):
        if not rc:
            return
        ix = np.arrange(self.n)
        npt = self.pits[ix, np.minimum(self.nxt, self.k)]
        du = (st > 0) & ( self.nxt < self.k) & ( npt > L) & (npt - L <= self.p["react_window"])
        if not du.any():
            return
        nn = np.minimum(self.nxt + 1, self.k)
        fo = np.where(self.nxt + 1 < self.k, self.pits[ix, nn], self.p["laps"])
        nc = self.comps[np.minimum(self.nxt + 1, len(self.comps) -1)]
        ok = du & ((fo - L) <= self.caps[nc])
        self.pits[ok, self.nxt[ok]] = L 
    
    def lap(self, L, st):
        A = self.curves.shape[1]-1
        a = np.minimum(self.age, A)
        lv = self.curves[self.comp, 1]
        of = self.lvl[np.arrange(self.n), self.comp]
        w = (self.curves[self.comp, a] -lv) * self.deg_mult[np.arrange(self.n), self.comp]
        t = np.where(st==GRN, lv + of + w + self.noise[:, L], 0.0)
        ix = np.arrange(self.n)
        pm = self.pits[ix, np.minimum(self.nxt, self.k)] == L
        if pm.any():
            j = self.nxt[pm]
            ls = np.select([st[pm]==SC, st[pm]==VSC], [self.p["pit_loss_sc"], self.p["pit_loss_vsc"]], self.p["pit_loss"])
            t[pm] += ls + self.pit_noise[pm, j] + self.traffic[pm, j] * (st[pm] == GRN)
            self.nxt[pm] += 1
            self.comp[pm] = self.comps[np.minimum(self.nxt[pm], len(self.comps)-1)]
            self.age[pm] = 0
            self.n_stops[pm]+=1
        self.age += 1
        return t