import { Team } from "@/types/team";

export default function TeamCard({ team }:{ team: Team }) {
    return (
        <div className="border-4 p-0 m-0 overflow-hidden" style={{backgroundColor:team.teamColor}}>
            <h2 className="text-center p-5">{team.teamName}</h2>
            <div className="p-5">
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