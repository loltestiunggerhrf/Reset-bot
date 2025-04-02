import threading
import discord
from discord.ext import commands
from flask import Flask

# Flask App Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Discord Bot Setup
bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

def run_bot():
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))

# Start Flask server and Discord bot in separate threads
threading.Thread(target=run_flask).start()
threading.Thread(target=run_bot).start()
