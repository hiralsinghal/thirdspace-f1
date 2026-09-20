"use client"
import { useState } from "react";
import data from "../../../public/data/dashboard_data.json";

export default function PastRaces() {
    const [selectedID, setSelectedID] = useState(data.races[0].id);
    const race = data.races.find((race) => race.id === selectedID)!;

    return (
        <div>
            <h1>Past Races</h1>
            <p>Select a race. Get the Data.</p>

            <main>
                <div>
                    <label htmlFor="race">Race</label>
                    <select value={selectedID} onChange={(e) => setSelectedID(e.target.value)}>
                        {data.races.map((race) => (
                            <option key={race.id} value={race.id}>{race.title}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <h2>{race.title}</h2>
                    <p>{race.circuit} - {race.laps} Laps</p>
                    <p>{race.allowed}</p>
                </div>

                <div>
                    <h3>Result</h3>
                    <ul>
                        {race.drivers.map((driver) => (
                            <li>P{driver.pos} {driver.code}</li>
                        ))}
                    </ul>
                </div>

            </main>
        </div>
    );
}