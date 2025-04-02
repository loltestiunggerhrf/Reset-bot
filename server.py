import discord
from discord.ext import commands
from flask import Flask
import os

# Initialize Flask
app = Flask(__name__)

# Initialize Discord bot with Intents from discord module
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

# Route for Flask server
@app.route('/')
def index():
    return "Bot is running!"

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run Flask app in the background and the Discord bot concurrently
if __name__ == '__main__':
    from threading import Thread
    
    def run_flask():
        app.run(host='0.0.0.0', port=5000)  # Make sure the port is open and change if necessary
    
    # Start Flask server in a background thread
    Thread(target=run_flask).start()
    
    # Start Discord bot
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
