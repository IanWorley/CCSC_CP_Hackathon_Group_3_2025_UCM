import { Button } from "@/components/ui/button";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectGroup, SelectLabel, SelectItem } from "@/components/ui/select";
import { useParams } from "react-router";

//takes in an id and displays the machine with that id
function MachinePage() {
    const { id } = useParams();

    return (
        <div className="w-full">
            <h1 className="font-bold text-3xl">Machine {id}</h1>
            <Button className="mt-4">Reserve</Button>
            <div className="flex justify-center">
                <Select>
                    <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Select a time" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectGroup>
                            <SelectLabel>Times</SelectLabel>
                            {[...Array(12).keys()].map((i) => (
                                <SelectItem value={`${i + 1}:00`} key={i}>{i + 1}:00</SelectItem>
                            ))}
                        </SelectGroup>
                    </SelectContent>
                </Select>
                <Select>
                    <SelectTrigger className="w-[90px] ml-4">
                        <SelectValue placeholder="AM/PM" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectGroup>
                            <SelectLabel>AM/PM</SelectLabel>
                            <SelectItem value="AM">AM</SelectItem>
                            <SelectItem value="PM">PM</SelectItem>
                        </SelectGroup>
                    </SelectContent>
                </Select>
            </div>
        </div>
    );
}

export default MachinePage;