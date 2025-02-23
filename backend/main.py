import os
import sqlite3

import requests
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# Get the absolute path to the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    login_success = login_user(username, password)
    if login_success:
        return make_response('', 204)
    else:
        return make_response('', 401)


@app.route("/register", methods=["POST"])
def add_user():
    data = request.get_json()
    add_user_to_db(
        data["username"],
        data["password"],
        data["studentId"],
        data["studentEmail"],
        data["buildingId"],
    )
    return jsonify({"status": "success"})


@app.route("/machines", methods=["GET"])  # http://127.0.0.1:8080/machines?location=312
def get_machines():
    location = request.args.get("location")
    machines = fetch_washing_machines(location)
    return jsonify(machines)


@app.route("/machine/<id>", methods=["GET"])
def get_status(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT * FROM machines WHERE id = ?""", (id,))
    machine = c.fetchone()
    conn.close()
    if machine:
        return jsonify(
            {
                "type": machine["type"],
                "id": machine["id"],
                "state": machine["state"],
                "state_time": machine["state_time"],
            }
        )
    else:
        return jsonify({"error": "Machine not found"}), 404

@app.route("/user", methods=["GET"])
def user():
    try:
        username = request.args.get("username")
        if not username:
            return jsonify({"error": "Username is required"}), 400
        
        user_info = get_user_info(username)
        if user_info:
            return jsonify(user_info)
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    

@app.route("/users", methods=["GET"])
def show_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT * FROM users""")
    users = c.fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route('/reserve/<id>', methods=['GET'])
def reserve_machine(machine_id):
    response = requests.get(f'http://127.0.0.1:8081/machine/{machine_id}/reserve')

def main():
    seeding()
    app.run(port=os.environ.get("BACKEND_SERVER_PORT", 8080))

def seeding():
    conn = get_db_connection()
    c = conn.cursor()

    # Corrected the CREATE TABLE statement for the users table
    c.execute(
        """CREATE TABLE IF NOT EXISTS users 
                 (username TEXT, password TEXT, student_id INTEGER, email TEXT , location TEXT)"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS machines 
                 (type TEXT, id TEXT, state TEXT, state_time INTEGER, location TEXT)"""
    )

    # Insert a default admin user
    c.execute(
        """INSERT INTO users (username, password, student_id, email,location) VALUES ('admin', 'admin1234', 0, 'admin@example.com','312')"""
    )

    # Fetch machines from the external API
    response = requests.get(
        f"http://127.0.0.1:{os.environ.get('WASHER_PORT', 8081)}/machines"
    )

    machines = response.json()

    # Insert fetched machines into the machines table
    for machine in machines:
        print(machine)
        print("\n---\n")
        try:
            c.execute(
                """INSERT INTO machines (type, id, state, state_time, location) 
                         VALUES (?, ?, ?, ?, ?)""",
                (
                    machine["machine_type"],
                    machine["machine_id"],
                    machine["state"],
                    machine["state_time"],
                    int(str(machine["machine_id"])[:3]),
                ),
            )
        except KeyError as e:
            print(f"KeyError: Missing key in machine data - {e}")
            print("Problematic machine data:", machine)
            continue  # Skip this machine and continue with the next one

    # Fetch and print all machines from the database
    c.execute("""SELECT * FROM machines""")
    machines = c.fetchall()
    for machine in machines:
        print(machine)

    conn.commit()
    conn.close()

def get_user_info(username: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """SELECT * FROM users WHERE username = ?""",
        (username,),
    )
    user = c.fetchone()
    conn.close()
    if user:
        return {
            "username": user["username"],
            "student_id": user["student_id"],
            "email": user["email"],
            "location": user["location"]
        }
    else:
        return None

def login_user(username: str, password: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """SELECT * FROM users WHERE username = ? AND password = ?""",
        (username, password),
    )
    user = c.fetchone()
    conn.close()
    return user is not None


def fetch_washing_machines(location=None):
    conn = get_db_connection()
    c = conn.cursor()
    if location:
        c.execute("""SELECT * FROM machines WHERE location = ?""", (location,))
    else:
        c.execute("""SELECT * FROM machines""")
    machines = c.fetchall()
    
    # Convert the tuple results into a list of dictionaries
    machine_list = []
    for machine in machines:
        machine_list.append(
            {
                "type": machine["type"],
                "id": machine["id"],
                "state": machine["state"],
                "state_time": machine["state_time"],
            }
        )
    conn.close()
    return machine_list


def add_user_to_db(username: str, password: str, student_id: int, email: str, location: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO users (username, password, student_id, email,location) VALUES (?, ?, ?, ?,?)""",
        (username, password, student_id, email, location),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
