from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/reset_hwid', methods=['POST'])
def reset_hwid():
    # Handle HWID reset logic
    return jsonify({"status": "success", "message": "HWID reset successful!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Use 8080 or your platform's default
    app.run(host="0.0.0.0", port=port)  # Ensure Flask binds to port 8080
