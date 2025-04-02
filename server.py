from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["key_system"]
keys_collection = db["keys"]

@app.route("/validate_key", methods=["GET"])
def validate_key():
    key = request.args.get("key")  # Get the key from request
    if not key:
        return jsonify({"status": "error", "message": "No key provided."}), 400

    key_data = keys_collection.find_one({"key": key})
    if not key_data:
        return jsonify({"status": "error", "message": "Invalid key."}), 403

    return jsonify({"status": "success", "message": "Key is valid."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
