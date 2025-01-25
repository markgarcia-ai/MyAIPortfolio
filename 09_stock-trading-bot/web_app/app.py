from flask import Flask, render_template, jsonify
import json
import os
import sys

app = Flask(__name__)

# Path to the JSON file
JSON_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

@app.route("/")
def index():
    """Render the table from JSON data."""
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"error": "JSON file not found"}
    return render_template("table.html", data=data)

@app.route("/api/data")
def get_data():
    """Provide JSON data via API."""
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"error": "JSON file not found"}
    return jsonify(data)

if __name__ == "__main__":
    port = 5006
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 5000.")
    app.run(debug=True, port=port)
