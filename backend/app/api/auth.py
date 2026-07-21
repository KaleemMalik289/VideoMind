from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Placeholder JWT Authentication Dependency.
    In a real production environment, this would decode the JWT, verify the signature,
    and look up the user in the database.
    """
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
        
    # For MVP purposes, any token passes and returns a mock user ID
    return {"user_id": "mock_user_123"}
