import { Driver } from "@/types/driver";

export default function DriverCard({ driver }: {driver: Driver}) {
    return (
        <div className="@container relative z-0 border-4 p-0 m-0 w-full h-120 overflow-hidden" style={{ backgroundColor:driver.teamColor, borderColor:`color-mix(in srgb, ${driver.teamColor} 30%, black 30%)`, color:driver.color }}>
            <span className="absolute -z-1 inset-0 flex items-center justify-center text-[90cqw] tabular-nums font-data" style={{ color:`color-mix(in srgb, ${driver.teamColor} 100%, white 40%)` }}>{driver.number}</span>
            <div className="p-5 font-body text-xl">
                <h2 className="text-center font-bold text-4xl mb- pb-0">{driver.firstName} {driver.lastName}</h2>
                <p className="italic text-center mt-0 pt-0 pb-5">{driver.nationality}</p>
                <p><b>Team:</b> {driver.team}</p>
                <p><b>Championship(s):</b> {driver.championships}</p>
                <p><b>Win(s):</b> {driver.wins}</p>
                <p><b>Podium(s):</b> {driver.podiums}</p>
                <p><b>Career Points:</b> {driver.careerPoints}</p>
            </div>
        </div>  

    );
}