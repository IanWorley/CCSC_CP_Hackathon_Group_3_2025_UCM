import { Card, CardContent } from "./ui/card";
import { useNavigate } from "@tanstack/react-router";
import WashingMahineSVG from "@/assets/washing-machine.svg";

export default function MachineCard() {
    const navigate = useNavigate();

    return (
        <Card className="bg-white shadow-lg rounded-lg overflow-hidden" onClick={() => navigate({ to: "/machine/$id", params: { id: "1" } })}>
            <CardContent className="flex items-center justify-center flex-col p-2">
                <img src={WashingMahineSVG} alt="Washing Machine" className="" />
                <div className="flex items-center justify-between">
                    <div className="w-4 h-4 rounded-full mr-2 bg-green-400" />
                    <p className="font-bold">Available</p>
                </div>
            </CardContent>
        </Card>
    )
};
