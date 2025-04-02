import os
from flask import Flask
from discord.ext import commands

app = Flask(__name__)

# Create bot instance with intents
bot = commands.Bot(command_prefix='/', intents=commands.Intents.default())

@app.route('/')
def index():
    return "Reset HWID bot is running!"

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)  # Ensure Flask binds to the correct port
