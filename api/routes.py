from fastapi import APIRouter, HTTPException, Depends, status
from discord.ext import commands
from api.auth import require_auth
from api.models import AnnouncementRequest, AnnouncementResponse, EmbedBuilder
from config import Config

def create_routes(bot: commands.Bot) -> APIRouter:
    """Create FastAPI routes with access to the Discord bot instance"""
    
    router = APIRouter()
    
    @router.post(
        "/main/announcement",
        response_model=AnnouncementResponse,
        status_code=status.HTTP_200_OK,
        summary="Send Discord Announcement",
        description="Send a rich embed announcement to a Discord channel",
        responses={
            200: {"description": "Announcement sent successfully"},
            400: {"description": "Invalid request data"},
            401: {"description": "Unauthorized - Invalid bearer token"},
            404: {"description": "Channel not found"},
            500: {"description": "Internal server error"},
        }
    )
    async def send_announcement(
        announcement: AnnouncementRequest,
        _: str = require_auth()
    ) -> AnnouncementResponse:
        """Handle announcement webhook requests"""
        try:
            # Get target channel
            channel_id = announcement.channel_id or Config.DEFAULT_CHANNEL_ID
            channel = bot.get_channel(int(channel_id))
            
            if not channel:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Invalid channel ID - channel not found"
                )
            
            # Create and send embed
            embed = EmbedBuilder.create_announcement_embed(announcement)
            bot.loop.create_task(channel.send(embed=embed))
            
            return AnnouncementResponse(
                status="Success",
                message="Announcement sent successfully"
            )
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid data: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
    
    return router 