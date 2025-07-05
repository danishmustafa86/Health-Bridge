"""
FastAPI Medical App - Main Entry Point
Comprehensive medical/healthcare application with JWT authentication
"""
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import route modules
from routes.patient import patient_router
from routes.doctor import doctor_router
from auth.jwt import verify_token, create_access_token
from models.user import User
from database import Database

# Initialize FastAPI app
app = FastAPI(
    title="MedCare API",
    description="A comprehensive medical/healthcare application with role-based access control",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()

# Database instance
db = Database()

# Include routers
app.include_router(patient_router, prefix="/api/patient", tags=["Patient"])
app.include_router(doctor_router, prefix="/api/doctor", tags=["Doctor"])

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "MedCare API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/auth/register")
async def register_user(user_data: dict):
    """
    Register a new user (Patient or Doctor)
    
    Body:
    - email: str
    - password: str
    - name: str
    - role: str ("patient" or "doctor")
    """
    try:
        # Validate required fields
        required_fields = ["email", "password", "name", "role"]
        for field in required_fields:
            if field not in user_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}"
                )
        
        # Validate role
        if user_data["role"] not in ["patient", "doctor"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role must be either 'patient' or 'doctor'"
            )
        
        # Check if user already exists
        existing_user = await db.get_user_by_email(user_data["email"])
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        # Create new user
        new_user = await db.create_user(user_data)
        
        # Generate JWT token
        access_token = create_access_token(data={"user_id": str(new_user["_id"]), "role": new_user["role"]})
        
        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(new_user["_id"]),
                "email": new_user["email"],
                "name": new_user["name"],
                "role": new_user["role"]
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/api/auth/login")
async def login_user(credentials: dict):
    """
    Login user with email and password
    
    Body:
    - email: str
    - password: str
    """
    try:
        # Validate required fields
        if "email" not in credentials or "password" not in credentials:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email and password are required"
            )
        
        # Authenticate user
        user = await db.authenticate_user(credentials["email"], credentials["password"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Generate JWT token
        access_token = create_access_token(data={"user_id": str(user["_id"]), "role": user["role"]})
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user["_id"]),
                "email": user["email"],
                "name": user["name"],
                "role": user["role"]
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@app.get("/api/auth/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user information from JWT token"""
    try:
        # Verify token
        payload = verify_token(credentials.credentials)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get user from database
        user = await db.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "id": str(user["_id"]),
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected" if db.is_connected() else "disconnected"
    }

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )