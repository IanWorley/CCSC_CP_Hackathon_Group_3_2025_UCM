import { useNavigate } from "react-router";
import { Card, CardContent } from "./ui/card";
import MachineSVG from "@/assets/machine.svg";

function MachineCard({ id, state }: { id: number, state: string }) {
    const navigate = useNavigate();

    const getStateColor = () => {
        switch (state) {
            case "idle":
                return "bg-green-500";
            default:
                return "bg-red-500";
        }
    }

    const getStateText = () => {
        switch (state) {
            case "idle":
                return "Available";
            default:
                return state;
        }
    }

    return (
        <Card className="bg-white shadow-md p-2" onClick={() => navigate(`/machine/${id}`)}>
            <CardContent>
                <img src={MachineSVG} alt="Machine" />
                <div className="mt-2 flex items-center justify-center">
                    <div className={`w-4 h-4 mr-4 rounded-full ${getStateColor()}`} />
                    <p className="font-bold">{getStateText()}</p>
                </div>
            </CardContent>
        </Card >
    );
}

export default MachineCard;