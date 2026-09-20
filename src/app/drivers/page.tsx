import drivers from "@/data/drivers.json";
import {Driver} from "@/types/driver";
import DriverCard from "@/components/DriverCard";

export default function Drivers() {
    return (
        <div className="mx-auto">
            <h1 className="mt-10 mx-auto text-center font-heading text-5xl">Drivers</h1>
            
            <div className="grid grid-cols-2 gap-10 mx-10">
                {(drivers as Driver[]).map((driver) => (
                    <DriverCard key={driver.id} driver={driver} />
                ))}
            </div>
        </div>
    );
}