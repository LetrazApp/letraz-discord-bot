from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
import discord
from config import Config

class AnnouncementRequest(BaseModel):
    """Pydantic model for announcement API request"""
    title: str = Field(..., min_length=1, max_length=256, description="The announcement title")
    message_content: str = Field(..., min_length=1, max_length=4096, description="The main announcement message")
    channel_id: Optional[str] = Field(None, description="Discord channel ID (uses default if not provided)")
    learn_more: Optional[HttpUrl] = Field(None, description="Optional URL for 'Learn More' link")
    image_url: Optional[HttpUrl] = Field(None, description="Optional image URL for the embed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Important Announcement",
                "message_content": "This is an important message for the community.",
                "channel_id": "123456789012345678",
                "learn_more": "https://example.com/details",
                "image_url": "https://example.com/image.png"
            }
        }

class AnnouncementResponse(BaseModel):
    """Response model for announcement API"""
    status: str = Field(..., description="Status of the request")
    message: Optional[str] = Field(None, description="Additional information")

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")

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
            embed.description = f"{request.message_content}\n\n[Learn More]({str(request.learn_more)})"
        else:
            embed.description = request.message_content
        
        # Set image if provided
        if request.image_url:
            embed.set_image(url=str(request.image_url))
        
        return embed 