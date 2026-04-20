from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Dummy license store
licenses = {
    "TEST123": {
        "hwid": "36a194963c3ba3e68f2d647782c1cb6fff533fd370ade1179dc59d1bc74fe9fb"
    }
}

logs = []

@app.route("/")
def home():
    return "License Server Running"

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json

    key = data.get("licenseKey")
    hwid = data.get("hwid")

    if key in licenses and licenses[key]["hwid"] == hwid:
        return jsonify({"valid": True})

    return jsonify({"valid": False})

@app.route("/log", methods=["POST"])
def log():
    data = request.json

    logs.append({
        "hwid": data.get("hwid"),
        "status": data.get("status"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%I:%M %p")
    })

    return "OK"

@app.route("/logs", methods=["GET"])
def get_logs():

    device_map = {}

    for log in logs:
        hwid = log["hwid"]

        short_device = hwid[:8] + "..." + hwid[-5:]

        if short_device not in device_map:
            device_map[short_device] = {
                "device": short_device,
                "currentStatus": log["status"],
                "history": []
            }

        device_map[short_device]["history"].append({
            "status": log["status"],
            "date": datetime.strptime(log["date"], "%Y-%m-%d").strftime("%d-%m-%Y"),
            "time": log["time"]
        })

        # latest status update
        device_map[short_device]["currentStatus"] = log["status"]

    return jsonify(list(device_map.values()))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)