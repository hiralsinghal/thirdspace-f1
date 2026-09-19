import json, os, sys
import fastf1, pandas as pd
RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")



def rec(y,rnd):
    s = fastf1.get_session(y, rnd, "R")
    s.load(laps=True, telemetry=False, weather=False, messages=False)
    L = s.laps
    dn = lambda x: int(x)
    laps = [dict(driver_number=dn(r.DriverNumber), lap_number=int(r.LapNumber),lap_duration=r.LapTime.total_seconds() if pd.notna(r.LapTime) else None, is_pit_out_lap=bool(pd.notna(r.PitOutTime))) for r in L.itertuples()]
    stints = []
    for (d, st), g in L.groupby(["DriverNumber", "Stint"]):
        stints.append(dict(driver_number=dn(d), stint_number=int(st), lap_start=int(g.LapNumber.min()), 
                           lap_end=int(g.LapNumber.max()),
                           compound=str(g.Compound.iloc[0]),
                           tyre_age_at_start=int(g.TyreLife.iloc[0]-1) if pd.notna(g.TyreLife.iloc[0]) else 0))
        rc = [dict(date=str(m.Time), lap_number=int(m.Lap) if pd.notna(m.Lap) else None, category=m.Category, message=m.Message, flag=m.Flag) for m in s.race_control_messages.itertuples()]
        w = s.weather_data
        wx = [dict(date=str(r.time), air_temperature=r.AirTemp, track_temperature=r.TrackTemp, rainfall=int(r.Rainfall)) for r in w.itertuples()]

        res = s.results

        rr = [dict(driver_number=dn(r.DriverNumber), position=int(r.Position), number_of_laps=int(L[L.DriverNumber==r.DriverNumber].LapNumber.max() or 0), dnf = not str(r.Status).startswith(("Finished", "+")), dns=False, dsq=r.Status=="Disqualified") for r in res.itertuples()]

        dv = [dict(driver_number=dn(r.DriverNumber), name_acronym=r.Abbrevation, team_name=r.TeamName, team_colour=r.TeamColour) for r in res.itertuples()]
        ev = s.event


        se = dict(session_key=int(f"{y}{ev.RoundNumber:02d}"), year=y, circuit_short_name=ev.Location,country_name=ev.Country, date_start=str(ev.EventDate))

        return dict(sessions=se, laps=laps, stints=stints, pit=[], race_control=rc, weather=wx, drivers=dv, session_result=rr)


if __name__ == "__main__":
    fastf1.Cache.enable_cache(os.path.join(RAW, "..", "fastf1_cache"))
    for y in map(int, sys.argv[1:]):
        sched = fastf1.get_event_schedule(y, include_testing=False)
        for rnd in sched.RoundNumber:
            out = os.path.join(RAW, f"{y}_{y}{rnd:02d}.json")
            if not os.path.exists(out):
                json.dump(rec(y, int(rnd)), open(out, "w"))