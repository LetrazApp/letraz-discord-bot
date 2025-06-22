from flask import request, jsonify
from functools import wraps
from config import Config

def require_bearer_token(f):
    """Decorator to require valid Bearer token authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "status": "Unauthorized", 
                "reason": "You are not authorized."
            }), 401

        token = auth_header.split(' ')[1]
        if token != Config.BEARER_TOKEN:
            return jsonify({
                "status": "Unauthorized", 
                "reason": "Invalid Bearer token"
            }), 401

        return f(*args, **kwargs)
    
    return decorated_function 