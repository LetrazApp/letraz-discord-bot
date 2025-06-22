from flask import Flask
import threading
from discord.ext import commands
from config import Config
from api.routes import create_routes

def create_app(bot: commands.Bot) -> Flask:
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Register API routes
    api_bp = create_routes(bot)
    app.register_blueprint(api_bp)
    
    # Add health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {"status": "healthy", "service": "letraz-discord-bot"}, 200
    
    return app

def run_flask_app(bot: commands.Bot):
    """Run Flask app in a separate thread"""
    app = create_app(bot)
    app.run(
        host=Config.FLASK_HOST, 
        port=Config.FLASK_PORT,
        debug=False
    )

def start_flask_thread(bot: commands.Bot):
    """Start Flask app in a daemon thread"""
    flask_thread = threading.Thread(target=run_flask_app, args=(bot,))
    flask_thread.daemon = True
    flask_thread.start()
    print(f"Flask API server started on {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    return flask_thread 