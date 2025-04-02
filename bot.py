import os
import threading
import discord
from discord.ext import commands
from flask import Flask
from pymongo import MongoClient

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["key_system"]
hwid_collection = db["hwids"]

# Set up Flask web server
app = Flask(__name__)

@app.route('/')
def hello():
    return "HWID Reset Server is Running"

# Function to run Flask server in the background
def run_flask():
    port = int(os.getenv('PORT', 5000))  # Use Render's provided port
    app.run(host='0.0.0.0', port=port)

# Start Flask server in a separate thread
threading.Thread(target=run_flask, daemon=True).start()

# Load Discord bot token from environment variables
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="/", intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()  # Sync slash commands
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Slash Command: /reset_hwid (Resets HWID for the user)
@bot.tree.command(name="reset_hwid", description="Reset your HWID to 'None'")
async def reset_hwid(interaction: discord.Interaction):
    user_id = interaction.user.id

    # Reset HWID in MongoDB
    hwid_collection.update_one(
        {"user_id": user_id},
        {"$set": {"hwid": "None"}},
        upsert=True
    )

    await interaction.response.send_message(f"{interaction.user.mention}, your HWID has been reset to 'None'!", ephemeral=True)

# Slash Command: /panel (Displays a control panel to reset HWID)
@bot.tree.command(name="panel", description="View the panel to reset HWID.")
async def panel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="HWID Reset Panel",
        description="Use the buttons below to reset your HWID.",
        color=discord.Color.blue()
    )
    
    # You can add buttons and other interactive elements here if needed
    await interaction.response.send_message(embed=embed)

load_dotenv()

app = Flask(__name__)

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["key_system"]
keys_collection = db["keys"]
hwid_collection = db["hwids"]

@app.route("/validate_key", methods=["GET"])
def validate_key():
    key = request.args.get("key")  # Get key from request
    if not key:
        return jsonify({"status": "error", "message": "No key provided."}), 400

    key_data = keys_collection.find_one({"key": key})
    if not key_data:
        return jsonify({"status": "error", "message": "Invalid key."}), 403

    return jsonify({"status": "success", "message": "Key is valid."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

# Run the bot
bot.run(TOKEN)
