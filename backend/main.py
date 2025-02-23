import os
import sqlite3

import requests
from flask import Flask, jsonify, request

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
    return jsonify({"login": login_success})


@app.route("/register", methods=["POST"])
def add_user():
    data = request.get_json()
    add_user_to_db(
        data["username"],
        data["password"],
        data["studentId"],
        data["studentEmail"],
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
                "run_time": machine["run_time"],
                "location": machine["location"],
            }
        )
    else:
        return jsonify({"error": "Machine not found"}), 404


@app.route("/users", methods=["GET"])
def show_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT * FROM users""")
    users = c.fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])


def main():
    seeding()
    app.run(port=os.environ.get("BACKEND_SERVER_PORT", 8080))


def seeding():
    conn = get_db_connection()
    c = conn.cursor()

    # Corrected the CREATE TABLE statement for the users table
    c.execute(
        """CREATE TABLE IF NOT EXISTS users 
                 (username TEXT, password TEXT, student_id INTEGER, email TEXT)"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS machines 
                 (type TEXT, id TEXT, state TEXT, state_time INTEGER, location TEXT, run_time TEXT)"""
    )

    # Insert a default admin user
    c.execute(
        """INSERT INTO users (username, password, student_id, email) VALUES ('admin', 'admin', 0, 'admin@example.com')"""
    )

    # Fetch machines from the external API
<<<<<<< HEAD

    try:
         response = requests.get('http://127.0.0.1:8081/machines')
    except requests.exceptions.RequestException as e:
        print("Failed to fetch machines from the API")
        print("Exception:", e)
        return
   
=======
    response = requests.get(
        f"http://127.0.0.1:{os.environ.get('WASHER_PORT', 8081)}/machines"
    )

>>>>>>> 12589c4e34874e72227ba9f804ed0025a0377f14
    # Print the API response to inspect its structure
    print("API Response:", response.json())

    machines = response.json()

    # Insert fetched machines into the machines table
    for machine in machines:
        try:
            c.execute(
                """INSERT INTO machines (type, id, state, state_time, location, run_time) 
                         VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    machine["machine_type"],
                    machine["machine_id"],
                    machine["state"],
                    machine["state_time"],
                    machine["building_code"],
                    machine["run_time"],
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
                "run_time": machine["run_time"],
                "location": machine["location"],
            }
        )
    conn.close()
    return machine_list


def add_user_to_db(username: str, password: str, student_id: int, email: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO users (username, password, student_id, email) VALUES (?, ?, ?, ?)""",
        (username, password, student_id, email),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
