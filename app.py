from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def get_data():
    if not os.path.exists(DATA_FILE):
        return jsonify([])

    with open(DATA_FILE, "r") as f:
        try:
            raw_data = json.load(f)
        except:
            return jsonify([])

    # 👉 Agrupar por usuario
    users = {}

    for entry in raw_data:
        user = entry["usuario"]

        if user not in users:
            users[user] = {
                "fechas": [],
                "damages": [],
                "wealth": []
            }

        users[user]["fechas"].append(entry["fecha"])
        users[user]["damages"].append(entry["userDamages"])
        users[user]["wealth"].append(entry["userWealth"])

    return jsonify(users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
