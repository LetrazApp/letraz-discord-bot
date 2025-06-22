from dataclasses import dataclass
from typing import Optional
import discord
from config import Config

@dataclass
class AnnouncementRequest:
    """Data class for announcement API request"""
    title: str
    message_content: str
    channel_id: Optional[str] = None
    learn_more: Optional[str] = None
    image_url: Optional[str] = None
    
    @classmethod
    def from_json(cls, data: dict):
        """Create AnnouncementRequest from JSON data"""
        return cls(
            title=data.get("title"),
            message_content=data.get("message_content"),
            channel_id=data.get("channel_id"),
            learn_more=data.get("learn_more"),
            image_url=data.get("image_url")
        )
    
    def validate(self) -> tuple[bool, str]:
        """Validate the announcement request data"""
        if not self.title:
            return False, "Title is required"
        
        if not self.message_content:
            return False, "Message content is required"
        
        return True, ""

class EmbedBuilder:
    """Helper class to build Discord embeds for announcements"""
    
    @staticmethod
    def create_announcement_embed(request: AnnouncementRequest) -> discord.Embed:
        """Create a Discord embed from an announcement request"""
        embed = discord.Embed(
            title=request.title, 
            colour=discord.Colour(Config.EMBED_COLOR)
        )
        
        # Set description with optional learn more link
        if request.learn_more:
            embed.description = f"{request.message_content}\n\n[Learn More]({request.learn_more})"
        else:
            embed.description = request.message_content
        
        # Set image if provided
        if request.image_url:
            embed.set_image(url=request.image_url)
        
        return embed 