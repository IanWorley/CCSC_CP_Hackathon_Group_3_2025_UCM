from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)

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
    return jsonify(get_washing_machines())

def main():
    conn = sqlite3.connect('./backend/database.db')
    seeding()
    app.run(port=443)

def seeding():
    conn = sqlite3.connect('./backend/database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS machines (type TEXT, id TEXT, state TEXT, state_time INTEGER)''')
    c.execute('''INSERT INTO users (username, password) VALUES ('admin', 'admin')''')

    response = requests.get('http://127.0.0.1:5000/machines')
    machines = response.json()

    # Insert machine data into the database
    for machine in machines:
        c.execute('''INSERT INTO machines (type, id, state, state_time) VALUES (?, ?, ?, ?)''', 
                  (machine['type'], machine['id'], machine['state'], machine['state_time']))
        
    conn.commit()
    conn.close()

def login_user(username: str, password: str):
    conn = sqlite3.connect('./backend/database.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def get_washing_machines():
    conn = sqlite3.connect('./backend/database.db')
    c = conn.cursor()
    machines = c.execute('''SELECT * FROM machines''').fetchall()
    
    # Convert the tuple results into a list of dictionaries
    machine_list = []
    for machine in machines:
        machine_list.append({
            'type': machine[0],
            'id': machine[1],
            'state': machine[2],
            'state_time': machine[3]
        })
    conn.close()
    return machine_list

def add_user_to_db(username: str, password: str):
    conn = sqlite3.connect('./backend/database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
