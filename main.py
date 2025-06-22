"""
Letraz Discord Bot - Main Entry Point

A Discord bot that provides announcement webhooks and automated member role assignment.
"""

from bot.discord_bot import create_bot
from api.flask_app import start_flask_thread
from config import Config

def main():
    """Main entry point for the Letraz Discord Bot"""
    try:
        # Validate configuration
        Config.validate()
        print("Configuration validated successfully")
        
        # Create Discord bot
        bot = create_bot()
        print("Discord bot created successfully")
        
        # Start Flask API server in background thread
        start_flask_thread(bot)
        
        # Start Discord bot (this blocks)
        print("Starting Discord bot...")
        bot.run(Config.DISCORD_BOT_TOKEN)
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        exit(1)
    except Exception as e:
        print(f"Failed to start bot: {e}")
        exit(1)

if __name__ == "__main__":
    main()