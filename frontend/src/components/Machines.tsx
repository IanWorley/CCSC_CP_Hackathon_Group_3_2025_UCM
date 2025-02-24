import { useEffect, useState } from "react";
import { Building } from "../model/Building";
import { Machine } from "../model/Machine";
import MachineCard from "./MachineCard";

function Machines() {
  const [buildings, setBuildings] = useState([]);

  const loadMachines = () => {
    // Fetch machines from the backend
    fetch("/api/get_machines")
      .then((res) => res.json())
      .then((data) => {
        setBuildings(data);
      })
      .catch((err) => {
        console.log("BIG ERROR: ", err);
      });
  };

  const sortMachines = () => {
    const sortedMachines: Machine[] = [];
    //sort by state so idle appear first
    buildings.forEach((building: Building) => {
      building.machines.forEach((m: Machine) => {
        if (m.state == "idle") {
          sortedMachines.unshift(m);
        } else {
          sortedMachines.push(m);
        }
      });
    });

    return sortedMachines;
  };

  const replaceUnderscores = (str: string) => {
    return str.replace(/_/g, " ");
  };

  useEffect(() => {
    loadMachines();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center mt-8">
      {buildings.flatMap((b: Building) => [
        <h1 key={b.building} className="text-2xl font-bold">
          {replaceUnderscores(b.building)}
        </h1>,
        <div className="m-2 grid grid-cols-2 gap-4">
          {sortMachines().map((m: Machine) => (
            <MachineCard key={m.id} id={m.id} state={m.state} />
          ))}
        </div>,
      ])}
    </div>
  );
}

export default Machines;
