"""
User Models - Pydantic models for user data validation
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """User roles enumeration"""
    PATIENT = "patient"
    DOCTOR = "doctor"

class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr
    name: str
    role: UserRole

class UserCreate(UserBase):
    """User creation model"""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """User response model"""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int

class PatientProfile(BaseModel):
    """Patient profile model"""
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    emergency_contact: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None
    insurance_info: Optional[str] = None

class DoctorProfile(BaseModel):
    """Doctor profile model"""
    phone: Optional[str] = None
    address: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    certifications: Optional[str] = None
    consultation_fee: Optional[float] = None
    working_hours: Optional[str] = None
    bio: Optional[str] = None
    rating: Optional[float] = None
    availability: Optional[List[str]] = None

class MedicalRecord(BaseModel):
    """Medical record model"""
    patient_id: str
    filename: str
    file_url: str
    file_type: str
    file_size: int
    description: Optional[str] = None
    upload_date: datetime
    uploaded_by: str
    reviewed: bool = False
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None

class Appointment(BaseModel):
    """Appointment model"""
    patient_id: str
    doctor_id: str
    appointment_date: str
    appointment_time: str
    reason: Optional[str] = None
    status: str = "scheduled"
    consultation_fee: float
    payment_status: str = "unpaid"
    payment_intent_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class Diagnosis(BaseModel):
    """Diagnosis model"""
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    diagnosis: str
    symptoms: str
    treatment_plan: str
    notes: Optional[str] = None
    prescriptions: Optional[List[str]] = None
    follow_up_date: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class PaymentIntent(BaseModel):
    """Payment intent model"""
    appointment_id: str
    amount: int
    currency: str = "usd"
    payment_method_id: str
    description: Optional[str] = None