import { Driver } from "@/types/driver";

export default function DriverCard({ driver }: {driver: Driver}) {
    return (
        <div className="relative z-0 border-4 p-5" style={{backgroundColor:driver.teamColor, borderColor:`color-mix(in srgb, ${driver.teamColor} 30%, black 30%`}}>
            <span className="absolute -z-1 inset-0 flex items-center justify-center text-[10cqw]" style={{ color:`color-mix(in srgb, ${driver.teamColor} 100%, white 90%)` }}>{driver.number}</span> {/**/}
            <h2 className="text-center font-bold">{driver.firstName} {driver.lastName}</h2>
            <p>{driver.nationality}</p>
            <p>{driver.team}</p>
            <p>{driver.championships}</p>
            <p>Wins: {driver.wins}</p>
            <p>{driver.podiums}</p>
            <p>{driver.careerPoints}</p>
        </div>  

    );
}