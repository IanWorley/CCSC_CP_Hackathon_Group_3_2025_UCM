import { createFileRoute } from "@tanstack/react-router";
import MachineCard from "../components/MachineCard";

export const Route = createFileRoute("/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <>
      <main className="container mx-auto p-4">
        <h2 className="text-2xl font-bold">Machines</h2>
        <div className="grid grid-cols-2 gap-4 mt-4">
          <MachineCard />
          <MachineCard />
          <MachineCard />
          <MachineCard />
        </div>
      </main>
    </>
  );
}
