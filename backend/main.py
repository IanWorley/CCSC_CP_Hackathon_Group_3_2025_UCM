from flask import Flask, request, jsonify
import sqlite3
import requests
import os

app = Flask(__name__)

# Get the absolute path to the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    login_success = login_user(username, password)
    return jsonify({'login': login_success})

@app.route('/adduser', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    add_user_to_db(username, password)
    return jsonify({'status': 'success'})

@app.route('/machines', methods=['GET'])
def get_machines():
    location = request.args.get('location')
    machines = fetch_washing_machines(location)
    return jsonify(machines)

@app.route('/machine', methods=['GET'])
def get_machine():
    # Get the location query parameter from the URL
    location = request.args.get('location')
    
    if not location:
        return jsonify({"error": "Location parameter is required"}), 400
    
    # Fetch the machines for the given location (implement the logic in fetch_washing_machines)
    machines = fetch_washing_machines(location)
    
    return jsonify(machines)

def main():
    seeding()
    app.run(port=443)

def seeding():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS machines (type TEXT, id TEXT, state TEXT, state_time INTEGER, location TEXT)''')
    c.execute('''INSERT INTO users (username, password) VALUES ('admin', 'admin')''')

    response = requests.get('http://127.0.0.1:8080/machines')
    machines = response.json()

    for machine in machines:
        c.execute('''INSERT INTO machines (type, id, state, state_time, location) VALUES (?, ?, ?, ?, ?)''', 
                  (machine['machine_type'], machine['machine_id'], machine['state'], machine['state_time'], machine['building_code']))
        
        
    conn.commit()
    conn.close()

def login_user(username: str, password: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def fetch_washing_machines(location=None):
    conn = get_db_connection()
    c = conn.cursor()
    if location:
        c.execute('''SELECT * FROM machines WHERE location = ?''', (location,))
    else:
        c.execute('''SELECT * FROM machines''')
    machines = c.fetchall()
    
    # Convert the tuple results into a list of dictionaries
    machine_list = []
    for machine in machines:
        machine_list.append({
            'type': machine['type'],
            'id': machine['id'],
            'state': machine['state'],
            'state_time': machine['state_time'],
            'location': machine['location']
        })
    conn.close()
    return machine_list

def add_user_to_db(username: str, password: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()