import requests
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

firebase_json = json.loads(os.environ["FIREBASE_KEY"])
cred = credentials.Certificate(firebase_json)

firebase_admin.initialize_app(cred)
db = firestore.client()

USER_IDS = [
    "68292fccf55f9440c28c67e8",
]

BASE_URL = "https://api2.warera.io/trpc/user.getUserLite?batch=1&input="

def build_url(user_id):
    return f'{BASE_URL}{{"0":{{"userId":"{user_id}"}}}}'

def fetch_user(user_id):
    res = requests.get(build_url(user_id))
    data = res.json()[0]["result"]["data"]

    return {
        "fecha": datetime.utcnow().isoformat(),
        "usuario": data["username"],
        "userId": user_id,
        "userDamages": data["rankings"]["userDamages"]["value"],
        "userWealth": data["rankings"]["userWealth"]["value"]
    }

def save_data():
    for user_id in USER_IDS:
        entry = fetch_user(user_id)
        db.collection("stats").add(entry)
        print("Guardado:", entry["usuario"])

if __name__ == "__main__":
    save_data()