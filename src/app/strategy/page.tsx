import data from "../../../public/data/dashboard_data.json";

export default function Strategy() {
    return (
        <div className="ml-5 mr-5">
            <h1 className="float mt-10 mx-auto font-heading text-center text-8xl">Pit Wall Strategy</h1>
            <p className="float text-center italic">Plan a race strategy.</p>

            <main>
                <div className="controls">
                    <label htmlFor="race">Race</label>
                    <select id="race">
                        {data.races.map((race) => (
                            <option key={race.id} value={race.id}>{race.title}</option>
                        ))}
                    </select>
                </div>
            </main>

            <div>
                <button>Pre Race Odds</button>
                <button>Replay the Real Race</button>
            </div>

            <div>
                <p>Your Plan</p>
            </div>

            <div>
                <p className="bold">Rival</p>
                <label htmlFor="rival">Race Against</label>
                <select id="rival">
                    {data.races[0].drivers.map((driver) => (
                        <option key={driver.code}>{driver.code}</option>
                    ))}
                </select>
            </div>
        </div>
    );
}