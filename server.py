from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    # Get the port from the environment variable, default to 5000 if not set
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
