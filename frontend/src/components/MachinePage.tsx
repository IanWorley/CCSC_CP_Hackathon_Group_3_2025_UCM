import { useEffect, useState } from "react";
import { useParams } from "react-router";

interface MachineState {
  id: number;
  state: string;
  type: string;
  will_reserve: boolean;
  state_init_time: number;
}

function MachinePage() {
  const { id } = useParams();

  const [machine, setMachine] = useState<MachineState>({
    id: 0,
    state: "",
    type: "",
    will_reserve: false,
    state_init_time: 0,
  });

  const loadMachine = () => {
    fetch(`/api/get_machine/${id}`)
      .then((res) => res.json())
      .then((data) => {
        setMachine(data);
      })
      .catch((err) => {
        console.log("BIG ERROR: ", err);
      });
  };

  const reserve = () => {
    fetch(`/api/reserve/${id}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.message === "machine reserved") {
          loadMachine();
        } else {
          console.log(data.message);
        }
      })
      .catch((err) => {
        console.log("BIG ERROR: ", err);
      });
  };

  useEffect(() => {
    loadMachine();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center mt-52">
      <h1 className="font-extrabold text-5xl">
        {machine.type} - {machine.id}
      </h1>
      <h2 className="font-extrabold text-3xl mt-8">{machine.state}</h2>
      <h2 className="font-extrabold text-3xl">
        Reserved: {machine.will_reserve ? "Yes" : "No"}
      </h2>
      <div className="w-3/4 mt-8">
        <button
          className="bg-black text-white p-3 w-full font-bold rounded-xl"
          onClick={reserve}
        >
          Reserve
        </button>
      </div>
    </div>
  );
}

export default MachinePage;
