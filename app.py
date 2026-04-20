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
    if not logs:
        return """
        <html>
        <head>
            <title>Device Logs</title>
            <style>
                body { font-family: Arial; background:#111; color:white; text-align:center; padding:40px; }
            </style>
        </head>
        <body>
            <h2>No Logs Found</h2>
        </body>
        </html>
        """

    html = """
    <html>
    <head>
        <title>Device Logs</title>
        <style>
            body {
                font-family: Arial;
                background:#111;
                color:white;
                padding:20px;
            }
            h2 {
                text-align:center;
                color:#00ff99;
            }
            table {
                width:100%;
                border-collapse:collapse;
                margin-top:20px;
                background:#1c1c1c;
            }
            th, td {
                padding:12px;
                border:1px solid #333;
                text-align:center;
            }
            th {
                background:#00aa66;
                color:white;
            }
            tr:nth-child(even) {
                background:#222;
            }
            tr:hover {
                background:#333;
            }
        </style>
    </head>
    <body>
        <h2>🖥 Device Status Logs</h2>
        <table>
            <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Device</th>
                <th>Status</th>
            </tr>
    """

    for row in reversed(logs):
        html += f"""
        <tr>
            <td>{row['Date']}</td>
            <td>{row['Time']}</td>
            <td>{row['Device']}</td>
            <td>{row['Status']}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)