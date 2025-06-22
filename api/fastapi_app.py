from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
import uvicorn
from discord.ext import commands
from config import Config
from api.routes import create_routes
from api.models import HealthResponse

def create_app(bot: commands.Bot) -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Letraz Discord Bot API",
        description="API for sending announcements to Discord channels and managing bot functionality",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    api_router = create_routes(bot)
    app.include_router(api_router, tags=["announcements"])
    
    # Add health check endpoint
    @app.get(
        "/health",
        response_model=HealthResponse,
        summary="Health Check",
        description="Check if the API service is running",
        tags=["health"]
    )
    async def health_check() -> HealthResponse:
        return HealthResponse(status="healthy", service="letraz-discord-bot")
    
    return app

def run_fastapi_app(bot: commands.Bot):
    """Run FastAPI app with Uvicorn"""
    app = create_app(bot)
    uvicorn.run(
        app,
        host=Config.FLASK_HOST,  # Keep same config name for backward compatibility
        port=Config.FLASK_PORT,
        log_level="info",
        access_log=True
    )

def start_fastapi_thread(bot: commands.Bot):
    """Start FastAPI app in a daemon thread"""
    api_thread = threading.Thread(target=run_fastapi_app, args=(bot,))
    api_thread.daemon = True
    api_thread.start()
    print(f"FastAPI server started on {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    print(f"API documentation available at: http://{Config.FLASK_HOST}:{Config.FLASK_PORT}/docs")
    return api_thread 