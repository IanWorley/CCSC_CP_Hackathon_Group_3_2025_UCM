import { useEffect, useState } from "react";
import MachineCard from "./MachineCard";

function Machines() {
    const [buildings, setBuildings] = useState([]);

    const loadMachines = () => {
        // Fetch machines from the backend
        fetch('/api/get_machines')
            .then(res => res.json())
            .then(data => {
                setBuildings(data);
            })
            .catch(err => {
                console.log("BIG ERROR: ", err);
            });
    };

    const sortMachines = (machines: any) => {
        const sortedMachines: any[] = [];
        //sort by state so idle appear first
        machines.forEach((m: any) => {
            if (m.state == "idle") {
                sortedMachines.unshift(m);
            } else {
                sortedMachines.push(m);
            }
        });

        return sortedMachines;
    }

    const replaceUnderscores = (str: string) => {
        return str.replace(/_/g, " ");
    }

    useEffect(() => {
        loadMachines();
    }, []);

    return (
        <div className="flex flex-col items-center justify-center mt-8">
            {buildings.flatMap((b: any) => [
                <h1 key={b.building} className="text-2xl font-bold">{replaceUnderscores(b.building)}</h1>,
                <div className="m-2 grid grid-cols-2 gap-4">
                    {sortMachines(b.machines).map((m: any) => (
                        <MachineCard key={m.id} id={m.id} state={m.state} />
                    ))}
                </div>
            ])}
        </div>
    );
}

export default Machines;