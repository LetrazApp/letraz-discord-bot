from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import Config

# Initialize the security scheme
security = HTTPBearer()

async def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    FastAPI dependency to verify Bearer token authentication
    
    Args:
        credentials: HTTP Authorization credentials from request header
        
    Returns:
        The valid token string
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    if credentials.credentials != Config.BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials

# For backward compatibility and ease of use
def require_auth():
    """Shorthand dependency for requiring authentication"""
    return Depends(verify_bearer_token) 