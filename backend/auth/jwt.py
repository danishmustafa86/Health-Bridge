"""
JWT Authentication Module
Handles JWT token creation, verification, and role-based access control
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import os

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Dictionary containing user data (user_id, role, etc.)
        expires_delta: Optional expiration time delta
    
    Returns:
        str: JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        Dict containing decoded token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a refresh token with longer expiration
    
    Args:
        data: Dictionary containing user data
    
    Returns:
        str: Refresh token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)  # 7 days for refresh token
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def require_role(payload: Dict[str, Any], required_role: str) -> None:
    """
    Check if user has required role
    
    Args:
        payload: Decoded JWT payload
        required_role: Required role ("patient" or "doctor")
    
    Raises:
        HTTPException: If user doesn't have required role
    """
    user_role = payload.get("role")
    
    if user_role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. Required role: {required_role}"
        )

def get_user_from_token(token: str) -> Dict[str, Any]:
    """
    Extract user information from JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        Dict containing user information
    """
    payload = verify_token(token)
    
    return {
        "user_id": payload.get("user_id"),
        "role": payload.get("role"),
        "exp": payload.get("exp")
    }

def is_token_expired(token: str) -> bool:
    """
    Check if token is expired
    
    Args:
        token: JWT token string
    
    Returns:
        bool: True if token is expired, False otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        
        if exp is None:
            return True
        
        return datetime.utcnow() > datetime.fromtimestamp(exp)
    
    except jwt.InvalidTokenError:
        return True

def refresh_access_token(refresh_token: str) -> str:
    """
    Create new access token from refresh token
    
    Args:
        refresh_token: Valid refresh token
    
    Returns:
        str: New access token
    
    Raises:
        HTTPException: If refresh token is invalid
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role = payload.get("role")
        
        if not user_id or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new access token
        new_token = create_access_token(data={"user_id": user_id, "role": role})
        return new_token
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )