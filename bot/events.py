import discord
from discord.ext import commands
from config import Config

def setup_events(bot: commands.Bot):
    """Register all event handlers with the bot"""
    
    @bot.event
    async def on_ready():
        """Event handler for when the bot is ready"""
        print(f'Logged in as {bot.user}')
        activity = discord.Activity(
            name=Config.BOT_ACTIVITY_NAME,
            type=discord.ActivityType.playing
        )
        await bot.change_presence(activity=activity)

    @bot.event
    async def on_member_join(member: discord.Member):
        """Event handler for when a new member joins the server"""
        guild = member.guild
        role = guild.get_role(int(Config.ROLE_ID))
        
        if role:
            await member.add_roles(role)
            print(f"Assigned role {role.name} to {member.display_name}")
        else:
            print(f"Warning: Could not find role with ID {Config.ROLE_ID}") 