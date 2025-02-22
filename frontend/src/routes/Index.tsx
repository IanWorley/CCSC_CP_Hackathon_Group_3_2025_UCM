import MachineCard from "@/components/MachineCard";
import { useEffect, useState } from "react";

function Index() {
  const [machines, setMachines] = useState([]);

  useEffect(() => {
    fetch("/api/machines")
      .then((res) => res.json())
      .then((data) => setMachines(data));
  }, []);

  return (
    <div>
      <h1 className="ml-3 text-lg font-bold">Building Name</h1>
      <div className="grid grid-cols-2 gap-4 m-4">
        {machines.map(({ id, state }) => (
          <MachineCard key={id} id={id} state={state} />
        ))}
      </div>
    </div>
  );
}

export default Index;
