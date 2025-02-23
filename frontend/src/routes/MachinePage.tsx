import { Button } from "@/components/ui/button";
import { useParams } from "react-router";

//takes in an id and displays the machine with that id
function MachinePage() {
  const { id } = useParams();

  return (
    <div className="">
      <h1 className="font-bold text-3xl">Machine {id}</h1>
      <div className=" flex justify-center h-svh gap-4 items-center">
        <Button className="items-center">Reserve</Button>
      </div>
    </div>
  );
}

export default MachinePage;
