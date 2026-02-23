from flask import Flask, request, jsonify
import requests
import os
import datetime

app = Flask(__name__)

# Load environment variables
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TOKEN_URL = "https://connect-sandbox.gocardless.com/oauth/token"

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


@app.route("/exchange", methods=["POST"])
def exchange():
    if not request.is_json:
    return jsonify({"error": "JSON required"}), 400

code = request.json.get("code")

    if not code:
        return jsonify({"error": "Missing code"}), 400

    token_response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": os.environ.get("REDIRECT_URI")
        }
    )

    log_data("TOKEN_EXCHANGE", {
        "code": code,
        "response": token_response.json()
    })

    return jsonify(token_response.json())


def log_data(event_type, data):
    timestamp = datetime.datetime.utcnow().isoformat()

    with open("oauth_logs.txt", "a") as f:
        f.write(f"\n[{timestamp}] {event_type}\n")
        f.write(f"{data}\n")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
