import { Card, CardContent } from "./ui/card";
import MachineSVG from "@/assets/machine.svg";

function MachineCard() {
    return (
        <Card>
            <CardContent>
                <img src={MachineSVG} alt="Machine" />
                <div>
                    <p className="font-bold"> Card Content</p>
                </div>
            </CardContent>
        </Card >
    );
}

export default MachineCard;