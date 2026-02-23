from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "OAuth Lab Running."

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    log_data("CALLBACK_RECEIVED", {
        "code": code,
        "state": state,
        "headers": dict(request.headers)
    })

    return jsonify({
        "message": "Authorization code received",
        "code": code,
        "state": state
    })


def log_data(event_type, data):
    timestamp = datetime.datetime.utcnow().isoformat()
    with open("oauth_logs.txt", "a") as f:
        f.write(f"\n[{timestamp}] {event_type}\n")
        f.write(f"{data}\n")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
