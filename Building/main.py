from flask import Flask, jsonify, abort
from enum import Enum, StrEnum
import json
import os
import time
import random

#file for saving machine data
MACHINE_FILE = "machines.json"

#constants for the machine states
class MachineStates(StrEnum):
    IDLE = "idle"
    WASHING = "washing"
    FINISHED = "finished"
    RESERVED = "reserved"

#constants for machine type
class MachineType(StrEnum):
    WASHER = "washer"
    DRYER = "dryer"

class MachineStyle(StrEnum):
    REGULAR = "regular"
    DELUXE = "deluxe"
    ULTRA = "ultra"
    DRYER = "dryer"

app = Flask(__name__)
#Machine class
class Machine:
    def __init__(self, machine_type, machine_id, building_code, state, machine_style, state_time):
        self.machine_type = machine_type
        self.machine_id = machine_id
        self.state = state
        self.building_code = building_code
        self.machine_style = machine_style if state == MachineStates.WASHING else None #only set the machine style if the machine is actually currently washing something
        self.state_time = state_time

def generate_id(building_code):
    return int(f"{building_code}{random.randint(100000000, 999999999)}")

def load_building_codes(filename):
    print('loading_building_codes')
    buildings={}
    codes = []
    if(os.path.exists(filename)):
        with open(filename) as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    building_name = parts[0].strip()
                    building_code = parts[1].strip()

                    buildings[building_name] = building_code
                    codes.append(building_code)

        print(f"DEBUG: Loaded {len(buildings)} buildings.")
        return buildings
    else:
        print(f'Error {filename} not found!')

load_building_codes('codes_for_buildings.txt')
def init_washing_machines():
    buildings = load_building_codes("codes_for_buildings.txt")
    machines = []

    for building, code in buildings.items():
        code = int(code)
        for i in range(4): #4 washers
            machines.append(Machine(
                                    machine_type=MachineType.WASHER,
                                    machine_id=generate_id(code),
                                    building_code=code,
                                    state = MachineStates.IDLE,
                                    machine_style=None,#set to none since its just initialized
                                    state_time=int(time.time())
                                    ))
        for i in range(4): #4 dryers
            machines.append(Machine(
                                    machine_type=MachineType.DRYER,
                                    machine_id=generate_id(code),
                                    building_code=code,
                                    state=MachineStates.IDLE,
                                    machine_style=None,  #set to none since its just initialized
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
                print("Error reading machines.json, Reinitalizing machines")
    #if it fails, reinitialize machines
    machines = init_washing_machines()
    save_machines(machines)
    return machines

#load machines at startup
machines = init_washing_machines()

if not os.path.exists(MACHINE_FILE):
    save_machines(machines)

@app.route('/machines', methods=['GET'])
def get_washing_machines():
    return jsonify([vars(machine) for machine in machines])

@app.route('/machine/<id>', methods=['GET'])
def get_washing_machine(id):
    # Search for machine by ID
    machine = next((m for m in machines if m.machine_id == id), None)
    if machine is None:
        abort(404, description="Machine not found")
    return jsonify({
        "machine_type": machine.machine_type,
        "machine_id": machine.machine_id,
        "state": machine.state,
        "building_code": machine.building_code,
        "machine_style": machine.machine_style,
        "state_time": machine.state_time
    })

@app.route('/')
def default_route():
    abort(404, description="Page not found")

@app.route('/machine/<id>/set_state/<state>', methods=['POST'])
def set_machine_state(id, state):
    # Search for machine by ID
    machine = next((m for m in machines if m.machine_id == id), None)
    if machine is None:
        abort(404, description="Machine not found")

    # Update machine state
    machine.state = state
    machine.state_time = int(time.time())
    save_machines(machines)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(port=8081)