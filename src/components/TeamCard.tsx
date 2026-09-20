import Image from "next/image";
import { Team } from "@/types/team";

export default function TeamCard({ team }:{ team: Team }) {
    return (
        <div className="relative z-0 border-4 p-0 m-0 overflow-hidden font-body" style={{backgroundColor:team.teamColor, borderColor:`color-mix(in srgb, ${team.teamColor} 30%, black 30%)`, color:team.color}}>
            <h2 className="text-center p-5 text-4xl font-bold">{team.teamName}</h2>
            <Image
                src={team.image}
                alt={team.teamName}
                fill
                className="-z-1 opacity-20 object-contain"
            />
            <div className="p-5 text-xl">
                <p>Constructors' Championships: {team.constructorsChampionships}</p>
                <p>Drivers' Championships: {team.driversChampionships}</p>
                <p>Race Wins: {team.raceWins}</p>
                <p>Podiums: {team.podiums}</p>
                <p>Pole Positions: {team.polePositions}</p>
                <p>Fastest Laps: {team.fastestLaps}</p>
            </div>
            
        </div>
    );
}