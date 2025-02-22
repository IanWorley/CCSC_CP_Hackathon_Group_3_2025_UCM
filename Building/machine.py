from flask import Flask, jsonify, abort
from random import random
from time import time
from enum import Enum

#constants for the machine states
class MachineStates(Enum):
    IDLE = 0
    WASHING = 1
    FINISHED = 2
    RESERVED = 3
    LOCKED = 4

#constants for machine type
class MachineType(Enum):
    WASHER = 0
    DRYER = 1

class MachineStyle(Enum):
    REGULAR = 29
    DELUXE = 31
    ULTRA = 39

app = Flask(__name__)

# Machine class
class Machine:
    def __init__(self, machine_type, machine_id, state, machine_style, state_time):
        self.machine_type = machine_type
        self.machine_id = machine_id
        self.state = state
        self.machine_style = machine_style
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
                machine_type=MachineType.WASHER.value,  # Type of the machine (washer or dryer, 0 or 1 respectively)
                machine_id=machine_id,
                state=MachineStates.IDLE.value,  # Initial state is idle, aka 0
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
