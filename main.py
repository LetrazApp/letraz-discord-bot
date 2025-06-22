import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import threading
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
DEFAULT_CHANNEL_ID = os.getenv('DEFAULT_CHANNEL_ID')
ROLE_ID = os.getenv('ROLE_ID')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    activity = discord.Activity(
        name="with my server 💪",
        type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)

@bot.event
async def on_member_join(member):
    guild = member.guild
    role = guild.get_role(int(ROLE_ID))
    await member.add_roles(role)

app = Flask(__name__)

@app.route('/main/announcement', methods=['POST'])
def webhook():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"status": "Unauthorized", "reason": "You are not authorized."}), 401

    token = auth_header.split(' ')[1]
    if token != BEARER_TOKEN:
        return jsonify({"status": "Unauthorized", "reason": "Invalid Bearer token"}), 401

    data = request.get_json()

    channel_id = data.get("channel_id")
    channel = bot.get_channel(int(channel_id)) if channel_id else bot.get_channel(DEFAULT_CHANNEL_ID)

    if not channel:
        return jsonify({"status": "Failed", "reason": "Invalid channel ID"}), 400

    title = data.get("title")
    if not title:
        return jsonify({"status": "Failed", "reason": "Title is required"}), 400

    embed = discord.Embed(title=title, colour=discord.Colour(0xF4421F))

    message_content = data.get("message_content")
    if not message_content:
        return jsonify({"status": "Failed", "reason": "Message content is required"}), 400

    learn_more = data.get("learn_more")
    embed.description = f"{message_content}\n\n[Learn More]({learn_more})" if learn_more else message_content

    image_url = data.get("image_url")
    if image_url:
        embed.set_image(url=image_url)

    bot.loop.create_task(channel.send(embed=embed))
    return jsonify({"status": "Success"}), 200

def run_flask():
    app.run(host="0.0.0.0", port=4000)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

bot.run(DISCORD_BOT_TOKEN)