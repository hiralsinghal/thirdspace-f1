import json, time, os, sys, urllib.request, urllib.error
BASE = "https://api.openf1.org/v1/"
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

ENDPOINTS = ["laps", "stints", "pit", "race_control", "weather", "drivers","session_resul"]
def get(path, t=6):
    for i in range(t):
        try:
            with urllib.request.urlopen(BASE+path,timeout=67) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2**i)
                continue
            if e.code == 404:
                return []
            raise
        except Exception:
            time.sleep(2**i)
    raise RuntimeError(path)

def fet_y(y):
    ss = [s for s in get(f"sessions?year={y}&session_name=Race")  if not s.get("is_cancelled")]
    for s in ss:
        out = os.path.join(RAW, f"{y}_{s['session_key']}.json")
        if os.path.exists(out):
            continue
        rec = {'sessions':s}
        for e in ENDPOINTS:
            rec[e] = get(f"{e}?session_key={s['session_key']}")
            time.sleep(0.4)
        if not rec['laps']:
            continue
        json.dump(rec, open(out,"w"))

if __name__ == "__main__":
    for y in map(int, sys.argv[1:] or [2023, 2024, 2025]):
        fet_y(y)