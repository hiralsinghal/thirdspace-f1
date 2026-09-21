"use client"
import { useState } from "react";
import data from "../../../public/data/dashboard_data.json";

export default function PastRaces() {
    const [selectedID, setSelectedID] = useState(data.races[0].id);
    const race = data.races.find((race) => race.id === selectedID)!;

    return (
        <div>
            <h1 className="mt-10 mx-auto text-center font-heading text-8xl">Past Races</h1>
            <p className="mt-0 text-center italic font-body text-xl">Data of a race!</p>

            <main>
                <div className="my-5 flex justify-center items-center mx-auto text-xl select-floatin w-fit border-4 border-gray-700">
                    <label htmlFor="race" className="mx-1 py-2 pl-5">Race</label>
                    <select 
                    className="text-center select-floating-label"
                    value={selectedID} onChange={(e) => setSelectedID(e.target.value)}>
                        {data.races.map((race) => (
                            <option key={race.id} value={race.id}>{race.title}</option>
                        ))}
                    </select>
                </div>

                <div className="text-center">
                    <h2 className="text-center font-bold text-4xl">{race.title}</h2>
                    <p><b>Race Track:</b> {race.circuit}</p>
                    <p><b>Laps:</b> {race.laps} Laps</p>
                    <p><b>Compounds Allowed:</b> {race.allowed}</p>
                </div>

                <div className="text-center">
                    <h3 className="font-bold">Result</h3>
                    <ul>
                        {race.drivers.map((driver) => (
                            <li key={driver.code}>P{driver.pos} {driver.code}</li>
                        ))}
                    </ul>
                </div>

            </main>
        </div>
    );
}