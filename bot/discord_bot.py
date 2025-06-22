import discord
from discord.ext import commands
from config import Config
from bot.events import setup_events

def create_bot() -> commands.Bot:
    """Create and configure the Discord bot"""
    # Set up intents
    intents = discord.Intents.default()
    intents.members = True
    
    # Create bot instance
    bot = commands.Bot(command_prefix=Config.BOT_PREFIX, intents=intents)
    
    # Setup event handlers
    setup_events(bot)
    
    return bot

def run_bot():
    """Create and run the Discord bot"""
    Config.validate()
    bot = create_bot()
    bot.run(Config.DISCORD_BOT_TOKEN) 