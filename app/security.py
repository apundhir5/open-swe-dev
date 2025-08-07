"""
Security module for password hashing and session token management.
"""
import os
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Session token serializer
APP_SECRET = os.getenv("APP_SECRET", "dev-secret-change-in-production")
session_serializer = URLSafeTimedSerializer(APP_SECRET)

# In-memory user store with hashed passwords
USERS: Dict[str, Dict[str, Any]] = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123")
    }
}


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_session_token(username: str) -> str:
    """
    Create a signed session token for a user.
    
    Args:
        username: Username to create token for
        
    Returns:
        Signed session token string
    """
    return session_serializer.dumps({"username": username})


def verify_session_token(token: str, max_age: int = 3600) -> Optional[str]:
    """
    Verify and decode a session token.
    
    Args:
        token: Session token to verify
        max_age: Maximum age of token in seconds (default: 3600 = 1 hour)
        
    Returns:
        Username if token is valid, None otherwise
    """
    try:
        data = session_serializer.loads(token, max_age=max_age)
        return data.get("username")
    except (BadSignature, SignatureExpired):
        return None


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user with username and password.
    
    Args:
        username: Username to authenticate
        password: Plain text password
        
    Returns:
        User dict if authentication successful, None otherwise
    """
    user = USERS.get(username)
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None
