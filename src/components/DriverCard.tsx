import { Driver } from "@/types/driver";

export default function DriverCard({ driver }: {driver: Driver}) {
    return (
        <div className="relative border-4 p-5" style={{backgroundColor:driver.teamColor}}>
            <span className="absolute -z-1 inset-x-0 text-5xl text-center opacity-50 text-shadow-black-300" style={{ color:`color-mix(in srgb, ${driver.teamColor} 100%, white 60%)` }}>{driver.number}</span>
            <h2 className="text-center font-bold">{driver.firstName} {driver.lastName}</h2>
            <p>Wins: {driver.wins}</p>
        </div>  

    );
}