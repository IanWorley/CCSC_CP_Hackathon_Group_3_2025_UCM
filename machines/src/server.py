import os

from flask import Flask, jsonify, request, abort
import machine

buildings = [
    "Ellis_Residence_Hall",
    "Fitz_Hall",
    "Foster_Apartments",
    "Housey_Hall",
    "Houts_Hall",
    "Nickerson_Hall",
    "Panhellenic_Hall",
    "South_Todd_Hall",
    "South_Yeater_Hall",
    "Crossing_Apartments",
    "Todd_Apartments",
]

all_machines = []

used_ids = set()
def createId():
    id = machine.createId()
    while id in used_ids:
        id = machine.createId()
    used_ids.add(id)
    return id

def generate_machines(num_washers: int, num_dryers: int) -> list:
    database = []
    for building in buildings:
        database.append({"building": building, "machines": []})
        for i in range(num_washers):
            database[-1]["machines"].append(machine.create_random_machine(createId(), machine.MachineType.WASHER))
        for i in range(num_dryers):
            database[-1]["machines"].append(machine.create_random_machine(createId(), machine.MachineType.DRYER))

    return database

def find_machine_by_id(id: int) -> machine.Machine:
    for db in all_machines:
        for m in db["machines"]:
            if m.id == id:
                return m
    return None

app = Flask(__name__)

# GET /buildings
@app.route('/buildings')
def hello_world():
    return jsonify(buildings), 200

# GET /machines
# GET /machines?building=<building>
@app.route('/machines')
def machines():
    if request.args.get('building') == None:
        return jsonify(all_machines), 200
    else:
        building = request.args.get('building')
        for db in all_machines:
            if db["building"] == building:
                return jsonify(db), 200
        return jsonify({"message": "Building not found"}), 404
        
# GET /machines/<id>
@app.route('/machines/<int:id>')
def machine_by_id(id):
    m = find_machine_by_id(id)
    if m != None:
        machine.update(m)
        return jsonify(m), 200
    return jsonify({"message": "Machine not found"}), 404

@app.route('/reserve/<int:id>')
def reserve_machine(id):
    m = find_machine_by_id(id)
    if m != None:
        if m.state == machine.MachineState.WASHING:
            m.will_reserve = True
            return jsonify({"message": "machine reserved"}), 200
        return jsonify({"message": "Machine not reservable"}), 400
    return jsonify({"message": "Machine not found"}), 404

if __name__ == '__main__':
    all_machines = generate_machines(2, 2)
    app.run(port=os.environ.get("MACHINE_PORT", 5000), host=os.environ.get("MACHINE_HOST", "0.0.0.0"), debug=os.environ.get("DEBUG", False))