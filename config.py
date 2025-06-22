import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class to manage environment variables and settings"""
    
    # Discord Bot Configuration
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    DEFAULT_CHANNEL_ID = os.getenv('DEFAULT_CHANNEL_ID')
    ROLE_ID = os.getenv('ROLE_ID')
    
    # API Configuration
    BEARER_TOKEN = os.getenv('BEARER_TOKEN')
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', '4000'))
    
    # Bot Settings
    BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
    BOT_ACTIVITY_NAME = os.getenv('BOT_ACTIVITY_NAME', 'with my server 💪')

    # Embed Settings
    EMBED_COLOR = 0xF4421F
    
    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        required_vars = [
            'DISCORD_BOT_TOKEN',
            'BEARER_TOKEN',
            'DEFAULT_CHANNEL_ID',
            'ROLE_ID'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True 