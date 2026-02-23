from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "OAuth Lab Running."

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    print("Received Code:", code)
    print("Received State:", state)

    return jsonify({
        "message": "OAuth code received",
        "code": code,
        "state": state
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
