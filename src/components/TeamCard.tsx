import { Team } from "@/types/team";

export default function TeamCard({ team }:{ team: Team }) {
    return (
        <div>
            <h2>{team.teamName}</h2>
            <p>Constructors' Championships: {team.constructorsChampionships}</p>
            <p>Drivers' Championships: {team.driversChampionships}</p>
            <p>Race Wins: {team.raceWins}</p>
            <p>Podiums: {team.podiums}</p>
            <p>Pole Positions: {team.polePositions}</p>
            <p>Fastest Laps: {team.fastestLaps}</p>
        </div>
    );
}