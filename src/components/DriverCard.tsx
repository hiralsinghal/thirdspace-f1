import { Driver } from "@/types/driver";

export default function DriverCard({ driver }: {driver: Driver}) {
    return (
        <div>
            <h2>{driver.firstName} {driver.lastName}</h2>
            <p>{driver.number}</p>
            <p>Wins: {driver.wins}</p>
        </div>
    );
}