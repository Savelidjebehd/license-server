from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "licenses.json"

# password -> pc_id
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        licenses = json.load(f)
else:
    licenses = {
        "ROBIN2005": None
    }

def save():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(licenses, f, indent=2, ensure_ascii=False)

@app.route("/check", methods=["POST"])
def check():
    data = request.json or {}
    password = data.get("password")
    pc_id = data.get("pc_id")

    if not password or not pc_id:
        return jsonify(ok=False, msg="no data")

    # первая активация
    if password in licenses and licenses[password] is None:
        licenses[password] = pc_id
        save()
        return jsonify(ok=True, first=True)

    # повторный запуск на том же ПК
    if licenses.get(password) == pc_id:
        return jsonify(ok=True, first=False)

    return jsonify(ok=False, msg="license already used")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
