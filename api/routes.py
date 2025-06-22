from flask import request, jsonify, Blueprint
from discord.ext import commands
from api.auth import require_bearer_token
from api.models import AnnouncementRequest, EmbedBuilder
from config import Config

# Create Blueprint for API routes
api_bp = Blueprint('api', __name__)

def create_routes(bot: commands.Bot):
    """Create API routes with access to the Discord bot instance"""
    
    @api_bp.route('/main/announcement', methods=['POST'])
    @require_bearer_token
    def webhook():
        """Handle announcement webhook requests"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    "status": "Failed", 
                    "reason": "Invalid JSON data"
                }), 400
            
            # Parse and validate request
            announcement = AnnouncementRequest.from_json(data)
            is_valid, error_message = announcement.validate()
            
            if not is_valid:
                return jsonify({
                    "status": "Failed", 
                    "reason": error_message
                }), 400
            
            # Get target channel
            channel_id = announcement.channel_id or Config.DEFAULT_CHANNEL_ID
            channel = bot.get_channel(int(channel_id))
            
            if not channel:
                return jsonify({
                    "status": "Failed", 
                    "reason": "Invalid channel ID"
                }), 400
            
            # Create and send embed
            embed = EmbedBuilder.create_announcement_embed(announcement)
            bot.loop.create_task(channel.send(embed=embed))
            
            return jsonify({"status": "Success"}), 200
            
        except ValueError as e:
            return jsonify({
                "status": "Failed", 
                "reason": f"Invalid data: {str(e)}"
            }), 400
        except Exception as e:
            return jsonify({
                "status": "Failed", 
                "reason": f"Internal server error: {str(e)}"
            }), 500
    
    return api_bp 