from flask import Flask, jsonify, abort
import random
import time

app = Flask(__name__)

# Define constants
IDLE = "idle"
WASHING = "washing"
FINISHED = "finished"
RESERVED = "reserved"
LOCKED = "locked"

WASHER = "washer"
DRYER = "dryer"

# Machine class
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
    for building in range(10):  # Simulate 10 buildings
        random_number = random.randint(0, 100)  # Generate a random number for the building
        for machine in range(10):  # Simulate 10 machines per building
            machine_id = f"{random_number}0{machine}"  # Combine building and machine number
            machines.append(Machine(
                machine_type=WASHER,  # Type of the machine (washer or dryer)
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
