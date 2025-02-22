
from flask import Flask, request, jsonify
from Seeding import Seeding
from Login import login , Adduser



app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    login = login(username, password)
    return jsonify({'login': login.login()})
@app.route('/adduser', methods=['POST'])
def adduser():
    data = request.get_json()
    username = data['username']
    password = data['password']
    Adduser(username, password)
    return jsonify({'success': True})

@app.route('/machines', methods=['GET'])
def get_washing_machines():
    return jsonify([vars(machine) for machine in machines])


def main():
    Seeding()
    app.run(port=443)
    

if __name__ == '__main__':
    main()