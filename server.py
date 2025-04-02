import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "P DIDDY LOVER OVER HERE, GUYS TAKE A PICTURE!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use the port provided by Render
    app.run(host="0.0.0.0", port=port)
