import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


def api_address():
    return f"http://{os.environ.get('MACHINE_HOST', 'localhost')}:{os.environ.get('MACHINE_PORT', 8081)}"


@app.route("/login", methods=["POST"])
def login():
    data: dict = request.get_json()

    # Check if the JSON payload is valid
    if len(data.keys()) != 2 or "username" not in data or "password" not in data:
        return jsonify({"message": "Bad JSON payload"}), 400

    if data["username"] == "admin" and data["password"] == "admin":
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Login failed"}), 401


@app.route("/get_machines")
def get_machines():
    response = requests.get(f"{api_address()}/machines")
    return response.json(), response.status_code


@app.route("/get_machine/<int:id>")
def get_machine(id):
    response = requests.get(f"{api_address()}/machines/{id}")
    return response.json(), response.status_code


@app.route("/reserve/<int:id>")
def reserve_machine(id):
    response = requests.get(f"{api_address()}/reserve/{id}")
    return response.json(), response.status_code


if __name__ == "__main__":
    print("Starting server...")
    app.run(
        port=os.environ.get("BACKEND_PORT", 8080),
        host=os.environ.get("BACKEND_HOST", "0.0.0.0"),
        debug=os.environ.get("DEBUG", False),
    )
