import { Driver } from "@/types/driver";

export default function DriverCard({ driver }: {driver: Driver}) {
    return (
        <div className="@container relative z-0 border-4 p-0 m-0 w-full h-120 overflow-hidden" style={{ backgroundColor:driver.teamColor, borderColor:`color-mix(in srgb, ${driver.teamColor} 30%, black 30%)` }}>
            <span className="absolute -z-1 inset-0 flex items-end justify-center text-[90cqw] tabular-nums font-data" style={{ color:`color-mix(in srgb, ${driver.teamColor} 100%, white 90%)` }}>{driver.number}</span>
            <div className="p-5 font-body text-xl">
                <h2 className="text-center font-bold text-4xl mb-5">{driver.firstName} {driver.lastName}</h2>
                <p className="">{driver.nationality}</p>
                <p>{driver.team}</p>
                <p>{driver.championships}</p>
                <p>Wins: {driver.wins}</p>
                <p>{driver.podiums}</p>
                <p>{driver.careerPoints}</p>
            </div>
        </div>  

    );
}