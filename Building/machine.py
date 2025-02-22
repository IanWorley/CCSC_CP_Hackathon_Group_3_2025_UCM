from flask import Flask, jsonify, abort
from enum import Enum
import json
import os
import time
import random

#file for saving machine data
MACHINE_FILE = "machines.json"

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
    DRYER = 60

app = Flask(__name__)

# Machine class
class Machine:
    def __init__(self, machine_type, machine_id, building_code, state, machine_style, state_time):
        self.machine_type = machine_type
        self.machine_id = machine_id
        self.state = state
        self.building_code = building_code
        self.machine_style = machine_style if state == MachineStates.WASHING.value else None #only set the machine style if the machine is actually currently washing something
        self.state_time = state_time

def generate_id(building_code):
    return f"building_code_{building_code}{random.randint(100000000, 999999999)}"

def load_building_codes(filename):
    buildings={}
    with open(filename) as f:
        for line in f:
            parts = line.strip().split(' - ')
            if len(parts) == 2:
                buildings[parts[0]] = parts[1] #should come out like {"Ellis Residence Hall": "312"} for example
    return buildings

def init_washing_machines():
    buildings = load_building_codes("codes_for_buildings.txt")
    machines = []

    for building, code in buildings.items():
        for i in range(4): #4 washers
            machines.append(Machine(
                                    machine_type=MachineType.WASHER.value,
                                    machine_id=generate_id(code),
                                    building_code=code,
                                    state = MachineStates.IDLE.value,
                                    machine_style=None,#set to none since its just initialized
                                    state_time=int(time.time())
                                    ))
        for i in range(4): #4 dryers
            machines.append(Machine(
                                    machine_type=MachineType.DRYER.value,
                                    machine_id=generate_id(code),
                                    building_code=code,
                                    state=MachineStates.IDLE.value,
                                    machine_style=None,  # set to none since its just initialized
                                    state_time=int(time.time())
                                    ))
        return machines

def save_machines(machines):
    with open(MACHINE_FILE, "w") as f:
        json.dump([machine.__dict__ for machine in machines], f, indent=4)

def load_machines():
    if os.path.exists(MACHINE_FILE):
        with open(MACHINE_FILE) as f:
            try:
                machine_data = json.load(f)
                machines = []
                for data in machine_data:
                    machines.append(Machine(
                        machine_type=data["machine_type"],
                        machine_id=data["machine_id"],
                        building_code=data["building_code"],
                        state=data["state"],
                        state_time=data["state_time"],
                        machine_style=data["machine_style"],
                    ))
                return machines
            except json.JSONDecodeError:
                print("Error reading machines.json 'reinitalizing machines")
                return init_washing_machines()
    return init_washing_machines()

    #load machines at startup
machines = load_machines()

if not os.path.exists(MACHINE_FILE):
    save_machines(machines)

@app.route('/print_machines', methods=['GET'])
def print_machines():
    for machine in machines:
        print(vars(machine))
    return jsonify([vars(machine) for machine in machines])

    '''random.seed(time.time())  # Seed the random number generator
    for building in range(10):  # Simulate 10 buildings
        random_number = random.randint(0, 100)  # Generate a random number for the building
        for machine in range(10):  # Simulate 10 machines per building
            machine_id = f"{random_number}0{machine}"  # Combine building and machine number
            machines.append(Machine(
                machine_type=MachineType.WASHER.value,  # Type of the machine (washer or dryer, 0 or 1 respectively)
                machine_id=machine_id,
                state=MachineStates.IDLE.value,  # Initial state is idle, aka 0
                state_time=int(time.time())  # Timestamp of state change
            ))'''

'''# Routes
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
'''