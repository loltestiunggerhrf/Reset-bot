import os
import threading
from flask import Flask
from discord.ext import commands
from discord import Intents
from pymongo import MongoClient
import time

# Initialize Flask app
app = Flask(__name__)

# Initialize MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["key_system"]
hwid_collection = db["hwids"]

# Initialize Discord bot with correct Intents import
intents = Intents.default()  # Fixed this line
bot = commands.Bot(command_prefix='/', intents=intents)

# Flask route to check if the bot is running
@app.route('/')
def index():
    return "Reset HWID bot is running!"  # Display status on the Flask webpage

# Function to start the Discord bot
def run_bot():
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Slash command to reset HWID for the user
@bot.tree.command(name="reset_hwid", description="Reset your HWID to 'None'")
async def reset_hwid(interaction: discord.Interaction):
    hwid_collection.update_one(
        {"user_id": interaction.user.id},
        {"$set": {"hwid": "None"}},
        upsert=True
    )
    await interaction.response.send_message("Your HWID has been reset!", ephemeral=True)

# Slash command to get bot's status
@bot.tree.command(name="status", description="Get the current bot status")
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("The Reset HWID bot is running fine!", ephemeral=True)

# Start Flask and Discord bot together
if __name__ == '__main__':
    # Start the Discord bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Start the Flask server
    port = int(os.environ.get("PORT", 5000))  # Render uses dynamic port for hosting
    app.run(host='0.0.0.0', port=port)
