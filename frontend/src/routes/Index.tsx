import MachineCard from "@/components/MachineCard";

function index() {
    return (
        <div>
            <h1 className="text-lg font-bold">Index</h1>
            <div className="grid grid-cols-2 gap-4">
                <MachineCard />
                <MachineCard />
                <MachineCard />
                <MachineCard />
            </div>
        </div>
    );
}

export default index;