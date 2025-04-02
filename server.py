import os
from flask import Flask  # or another framework if you're using a different one

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Render!"

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if no PORT is provided
    app.run(host='0.0.0.0', port=port)
