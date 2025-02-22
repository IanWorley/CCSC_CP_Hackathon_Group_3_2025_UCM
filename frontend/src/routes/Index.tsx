import MachineCard from "@/components/MachineCard";

function index() {
    return (
        <div>
            <h1 className="text-lg font-bold">Index</h1>
            <div className="grid grid-cols-2 gap-4 m-4">
                {[1, 2, 3, 4, 5, 6].map((id) => (
                    <MachineCard key={id} id={id} />
                ))}
            </div>
        </div>
    );
}

export default index;