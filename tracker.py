import requests
import json
import os
from datetime import datetime
import time

# 👉 PONÉ ACÁ LOS USER IDS QUE QUIERAS TRACKEAR
USER_IDS = [
    "68292fccf55f9440c28c67e8",
    # "otro_user_id",
]

BASE_URL = "https://api2.warera.io/trpc/user.getUserLite?batch=1&input="


def build_url(user_id):
    return f'{BASE_URL}{{"0":{{"userId":"{user_id}"}}}}'


def fetch_user(user_id):
    url = build_url(user_id)
    response = requests.get(url)
    data = response.json()[0]["result"]["data"]

    return {
        "fecha": datetime.utcnow().isoformat(),
        "usuario": data["username"],
        "userId": user_id,
        "userDamages": data["rankings"]["userDamages"]["value"],
        "userWealth": data["rankings"]["userWealth"]["value"]
    }


def save_data():
    results = []

    for user_id in USER_IDS:
        try:
            user_data = fetch_user(user_id)
            results.append(user_data)
            print("OK:", user_data["usuario"])
        except Exception as e:
            print("ERROR con", user_id, e)

    file_path = "data.json"

    # Leer datos existentes
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                file_data = json.load(f)
            except:
                file_data = []
    else:
        file_data = []

    # Agregar nuevos datos
    file_data.extend(results)

    # Guardar
    with open(file_path, "w") as f:
        json.dump(file_data, f, indent=2)

    print(f"Guardado batch: {len(results)} usuarios a las {datetime.utcnow().isoformat()}")


# 🚀 LOOP cada 12 horas
if __name__ == "__main__":
    while True:
        save_data()
        time.sleep(12 * 60 * 60)  # 12 horas
