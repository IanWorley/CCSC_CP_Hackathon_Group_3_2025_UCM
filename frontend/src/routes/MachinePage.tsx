import { useParams } from "react-router";

//takes in an id and displays the machine with that id
function MachinePage() {
    const { id } = useParams();
    return (
        <div>
            <h1>Machine {id}</h1>
        </div>
    );
}

export default MachinePage;