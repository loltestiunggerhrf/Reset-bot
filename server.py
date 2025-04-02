import threading
import discord
from discord.ext import commands
from flask import Flask
import os

# Flask App Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Discord Bot Setup
intents = discord.Intents.default()  # Initialize intents, allowing your bot to receive events
intents.message_content = True  # Make sure this is enabled if you need to listen to message content

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

def run_bot():
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))

# Start Flask server and Discord bot in separate threads
threading.Thread(target=run_flask).start()
threading.Thread(target=run_bot).start()
