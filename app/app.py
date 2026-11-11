
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "application": "AWS DevOps CI/CD Project",
        "developer": "Niranjan Chanal",
        "status": "Running Successfully",
        "environment": os.getenv("APP_ENV", "Development")
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "Healthy"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
