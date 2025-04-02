import os
import discord
from discord.ext import commands
from discord import app_commands
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["key_system"]
hwid_collection = db["hwids"]

# Discord Bot Setup
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# Cooldown dictionary
user_cooldowns = {}

# Slash Command: /reset_hwid (Resets the user's HWID)
@bot.tree.command(name="reset_hwid", description="Reset your HWID in the system.")
async def reset_hwid(interaction: discord.Interaction):
    user_id = interaction.user.id

    # Reset HWID in the database
    hwid_collection.update_one(
        {"user_id": user_id},
        {"$set": {"hwid": "None"}},
        upsert=True
    )
    await interaction.response.send_message("Your HWID has been reset!", ephemeral=True)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()  # Sync slash commands
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Run the bot
bot.run(TOKEN)
