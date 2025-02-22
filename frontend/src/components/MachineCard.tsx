import { useNavigate } from "react-router";
import { Card, CardContent } from "./ui/card";
import MachineSVG from "@/assets/machine.svg";

function MachineCard({ id }: { id: number }) {
    const navigate = useNavigate();

    return (
        <Card className="bg-white shadow-md p-2" onClick={() => navigate(`/machine/${id}`)}>
            <CardContent>
                <img src={MachineSVG} alt="Machine" />
                <div className="mt-2 flex items-center justify-center">
                    <div className="w-4 h-4 mr-4 rounded-full bg-green-500" />
                    <p className="font-bold">Available</p>
                </div>
            </CardContent>
        </Card >
    );
}

export default MachineCard;