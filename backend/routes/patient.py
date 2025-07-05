"""
Patient Routes - All patient-related endpoints
Handles appointments, medical records, payments, and patient profile management
"""
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from datetime import datetime
import json

from auth.jwt import verify_token, require_role
from services.s3 import S3Service
from services.stripe import StripeService
from database import Database

# Router setup
patient_router = APIRouter()
security = HTTPBearer()

# Services
db = Database()
s3_service = S3Service()
stripe_service = StripeService()

# Dependency to get current patient
async def get_current_patient(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current patient from JWT token"""
    payload = verify_token(credentials.credentials)
    require_role(payload, "patient")
    
    user_id = payload.get("user_id")
    user = await db.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return user

@patient_router.get("/profile")
async def get_patient_profile(current_patient = Depends(get_current_patient)):
    """Get patient profile information"""
    try:
        profile = await db.get_patient_profile(str(current_patient["_id"]))
        return {
            "id": str(current_patient["_id"]),
            "email": current_patient["email"],
            "name": current_patient["name"],
            "profile": profile or {}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile: {str(e)}"
        )

@patient_router.put("/profile")
async def update_patient_profile(
    profile_data: dict,
    current_patient = Depends(get_current_patient)
):
    """Update patient profile information"""
    try:
        updated_profile = await db.update_patient_profile(
            str(current_patient["_id"]),
            profile_data
        )
        return {
            "message": "Profile updated successfully",
            "profile": updated_profile
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )

@patient_router.post("/upload-medical-record")
async def upload_medical_record(
    file: UploadFile = File(...),
    description: str = "",
    current_patient = Depends(get_current_patient)
):
    """
    Upload medical record to AWS S3
    
    - **file**: Medical record file (PDF, JPG, PNG)
    - **description**: Optional description of the record
    """
    try:
        # Validate file type
        allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File type not supported. Only PDF, JPG, and PNG files are allowed."
            )
        
        # Validate file size (10MB limit)
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:  # 10MB in bytes
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds 10MB limit"
            )
        
        # Upload to S3
        file_url = await s3_service.upload_file(
            file_content,
            file.filename,
            file.content_type,
            f"medical-records/{current_patient['_id']}"
        )
        
        # Save record metadata to database
        record_data = {
            "patient_id": str(current_patient["_id"]),
            "filename": file.filename,
            "file_url": file_url,
            "file_type": file.content_type,
            "file_size": len(file_content),
            "description": description,
            "upload_date": datetime.now(),
            "uploaded_by": "patient"
        }
        
        record = await db.create_medical_record(record_data)
        
        return {
            "message": "Medical record uploaded successfully",
            "record": {
                "id": str(record["_id"]),
                "filename": record["filename"],
                "file_url": record["file_url"],
                "upload_date": record["upload_date"].isoformat(),
                "description": record["description"]
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload medical record: {str(e)}"
        )

@patient_router.get("/medical-records")
async def get_patient_medical_records(current_patient = Depends(get_current_patient)):
    """Get all medical records for the patient"""
    try:
        records = await db.get_patient_medical_records(str(current_patient["_id"]))
        
        formatted_records = []
        for record in records:
            formatted_records.append({
                "id": str(record["_id"]),
                "filename": record["filename"],
                "file_url": record["file_url"],
                "file_type": record["file_type"],
                "file_size": record["file_size"],
                "description": record["description"],
                "upload_date": record["upload_date"].isoformat(),
                "uploaded_by": record["uploaded_by"]
            })
        
        return {
            "records": formatted_records,
            "total": len(formatted_records)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get medical records: {str(e)}"
        )

@patient_router.get("/medical-records/{record_id}/download")
async def download_medical_record(
    record_id: str,
    current_patient = Depends(get_current_patient)
):
    """Generate signed URL for downloading medical record"""
    try:
        # Get record from database
        record = await db.get_medical_record(record_id)
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical record not found"
            )
        
        # Verify ownership
        if str(record["patient_id"]) != str(current_patient["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Generate signed URL
        download_url = await s3_service.generate_download_url(record["file_url"])
        
        return {
            "download_url": download_url,
            "filename": record["filename"],
            "expires_in": 3600  # 1 hour
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate download URL: {str(e)}"
        )

@patient_router.get("/doctors")
async def get_available_doctors():
    """Get list of available doctors for appointment booking"""
    try:
        doctors = await db.get_available_doctors()
        
        formatted_doctors = []
        for doctor in doctors:
            formatted_doctors.append({
                "id": str(doctor["_id"]),
                "name": doctor["name"],
                "email": doctor["email"],
                "specialization": doctor.get("specialization", "General Medicine"),
                "experience": doctor.get("experience", "Not specified"),
                "consultation_fee": doctor.get("consultation_fee", 100),
                "rating": doctor.get("rating", 0),
                "availability": doctor.get("availability", [])
            })
        
        return {
            "doctors": formatted_doctors,
            "total": len(formatted_doctors)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get doctors: {str(e)}"
        )

@patient_router.post("/book-appointment")
async def book_appointment(
    appointment_data: dict,
    current_patient = Depends(get_current_patient)
):
    """
    Book an appointment with a doctor
    
    Body:
    - doctor_id: str
    - appointment_date: str (ISO format)
    - appointment_time: str
    - reason: str (optional)
    """
    try:
        # Validate required fields
        required_fields = ["doctor_id", "appointment_date", "appointment_time"]
        for field in required_fields:
            if field not in appointment_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}"
                )
        
        # Verify doctor exists
        doctor = await db.get_user_by_id(appointment_data["doctor_id"])
        if not doctor or doctor["role"] != "doctor":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )
        
        # Check appointment slot availability
        is_available = await db.check_appointment_availability(
            appointment_data["doctor_id"],
            appointment_data["appointment_date"],
            appointment_data["appointment_time"]
        )
        
        if not is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Appointment slot is not available"
            )
        
        # Create appointment
        appointment = {
            "patient_id": str(current_patient["_id"]),
            "doctor_id": appointment_data["doctor_id"],
            "appointment_date": appointment_data["appointment_date"],
            "appointment_time": appointment_data["appointment_time"],
            "reason": appointment_data.get("reason", ""),
            "status": "scheduled",
            "created_at": datetime.now(),
            "consultation_fee": doctor.get("consultation_fee", 100)
        }
        
        created_appointment = await db.create_appointment(appointment)
        
        return {
            "message": "Appointment booked successfully",
            "appointment": {
                "id": str(created_appointment["_id"]),
                "doctor_name": doctor["name"],
                "appointment_date": created_appointment["appointment_date"],
                "appointment_time": created_appointment["appointment_time"],
                "consultation_fee": created_appointment["consultation_fee"],
                "status": created_appointment["status"]
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to book appointment: {str(e)}"
        )

@patient_router.post("/appointments/{appointment_id}/payment")
async def process_appointment_payment(
    appointment_id: str,
    payment_data: dict,
    current_patient = Depends(get_current_patient)
):
    """
    Process payment for an appointment using Stripe
    
    Body:
    - payment_method_id: str (Stripe payment method ID)
    """
    try:
        # Get appointment
        appointment = await db.get_appointment(appointment_id)
        
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
        
        # Verify ownership
        if str(appointment["patient_id"]) != str(current_patient["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Check if already paid
        if appointment.get("payment_status") == "paid":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment already paid"
            )
        
        # Process payment with Stripe
        payment_intent = await stripe_service.create_payment_intent(
            amount=int(appointment["consultation_fee"] * 100),  # Convert to cents
            currency="usd",
            payment_method=payment_data["payment_method_id"],
            description=f"Consultation fee for appointment {appointment_id}"
        )
        
        # Update appointment with payment info
        await db.update_appointment(appointment_id, {
            "payment_status": "paid",
            "payment_intent_id": payment_intent.id,
            "payment_date": datetime.now()
        })
        
        return {
            "message": "Payment processed successfully",
            "payment_intent_id": payment_intent.id,
            "status": "paid"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process payment: {str(e)}"
        )

@patient_router.get("/appointments")
async def get_patient_appointments(current_patient = Depends(get_current_patient)):
    """Get all appointments for the patient"""
    try:
        appointments = await db.get_patient_appointments(str(current_patient["_id"]))
        
        formatted_appointments = []
        for appointment in appointments:
            # Get doctor info
            doctor = await db.get_user_by_id(appointment["doctor_id"])
            
            formatted_appointments.append({
                "id": str(appointment["_id"]),
                "doctor_name": doctor["name"] if doctor else "Unknown",
                "doctor_specialization": doctor.get("specialization", "General Medicine") if doctor else "Unknown",
                "appointment_date": appointment["appointment_date"],
                "appointment_time": appointment["appointment_time"],
                "reason": appointment.get("reason", ""),
                "status": appointment["status"],
                "consultation_fee": appointment["consultation_fee"],
                "payment_status": appointment.get("payment_status", "unpaid"),
                "created_at": appointment["created_at"].isoformat()
            })
        
        return {
            "appointments": formatted_appointments,
            "total": len(formatted_appointments)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get appointments: {str(e)}"
        )

@patient_router.get("/appointments/{appointment_id}")
async def get_appointment_details(
    appointment_id: str,
    current_patient = Depends(get_current_patient)
):
    """Get detailed information about a specific appointment"""
    try:
        appointment = await db.get_appointment(appointment_id)
        
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
        
        # Verify ownership
        if str(appointment["patient_id"]) != str(current_patient["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Get doctor info
        doctor = await db.get_user_by_id(appointment["doctor_id"])
        
        # Get diagnosis if available
        diagnosis = await db.get_appointment_diagnosis(appointment_id)
        
        return {
            "id": str(appointment["_id"]),
            "doctor": {
                "id": str(doctor["_id"]),
                "name": doctor["name"],
                "specialization": doctor.get("specialization", "General Medicine")
            },
            "appointment_date": appointment["appointment_date"],
            "appointment_time": appointment["appointment_time"],
            "reason": appointment.get("reason", ""),
            "status": appointment["status"],
            "consultation_fee": appointment["consultation_fee"],
            "payment_status": appointment.get("payment_status", "unpaid"),
            "created_at": appointment["created_at"].isoformat(),
            "diagnosis": diagnosis
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get appointment details: {str(e)}"
        )