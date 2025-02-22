from flask import Flask, jsonify, abort
import random
import time

app = Flask(__name__)

locations = [
    "Ellis Residence Hall – 312",
    "Fitz Hall – 527",
    "Foster Apartments – 684",
    "Housey Hall – 159",
    "Houts Hall – 426",
    "Nickerson Hall – 738",
    "Panhellenic Hall – 893",
    "South Todd Hall – 241",
    "South Yeater Hall – 675",
    "Crossing South – 508",
    "Todd Apartments – 369"
]

IDLE = "idle"
WASHING = "washing"
FINISHED = "finished"
RESERVED = "reserved"
LOCKED = "locked"
WASHER = "washer"
DRYER = "dryer"


class Machine:
    def __init__(self, machine_type, machine_id, state, state_time):
        self.type = machine_type
        self.id = machine_id
        self.state = state
        self.state_time = state_time

# Initialize machines
machines = []

def init_washing_machines():
    random.seed(time.time())  # Seed the random number generator
    for location in locations:
        building_name, building_number = location.split(" – ")
        for machine_num in range(random.randint(1, 10)):  # Random number of machines per location
            machine_id = f"{building_number}0{machine_num}"  # Combine building number and machine number
            machines.append(Machine(
                machine_type=WASHER,  # Type of the machine (washer)
                machine_id=machine_id,
                state=IDLE,  # Initial state is idle
                state_time=int(time.time())  # Timestamp of state change
            ))

# Routes
@app.route('/machines', methods=['GET'])
def get_washing_machines():
    return jsonify([vars(machine) for machine in machines])

@app.route('/machine/<id>', methods=['GET'])
def get_washing_machine(id):
    # Search for machine by ID
    machine = next((machine for machine in machines if machine.id == id), None)
    if machine is None:
        abort(404, description="Machine not found")
    return jsonify(vars(machine))

@app.route('/')
def default_route():
    abort(404, description="Page not found")

if __name__ == '__main__':
    init_washing_machines()  # Initialize washing machines
    app.run(port=8080)
