import MachineSVG from "@/assets/machine.svg";
import { useNavigate } from "react-router";

function MachineCard({ id, state }: { id: number; state: string }) {
  const navigate = useNavigate();

  const getStateColor = () => {
    switch (state) {
      case "idle":
        return "bg-green-500";
      case "washing":
        return "bg-blue-500";
      case "reserved":
        return "bg-yellow-500";
      default:
        return "bg-red-500";
    }
  };

  const getStateText = () => {
    switch (state) {
      case "idle":
        return "available";
      default:
        return state;
    }
  };

  return (
    <div
      className="bg-white shadow-xl outline-4 outline-slate-500 p-2 rounded-2xl"
      onClick={() => navigate(`/machine/${id}`)}
    >
      <div>
        <img src={MachineSVG} alt="Machine" />
        <div className="mt-2 flex items-center justify-center">
          <div className={`w-4 h-4 mr-4 rounded-full ${getStateColor()}`} />
          <div className="text-nowrap overflow-clip">
            <p className="font-bold text-sm">{`${getStateText()} (N${id})`}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MachineCard;
