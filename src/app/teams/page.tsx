import teams from "@/data/teams.json";
import { Team } from "@/types/team";
import TeamCard from "@/components/TeamCard";

export default function Teams() {
    return (
        <div>
            <h1 className="mt-10 mx-auto text-center font-heading text-5xl">Teams</h1>

            <div className="grid grid-cols-1 gap-y-20">
                {(teams as Team[]).map((team) => (
                    <TeamCard key={team.id} team={team} />
                ))}
            </div>
        </div>
       
    );
}