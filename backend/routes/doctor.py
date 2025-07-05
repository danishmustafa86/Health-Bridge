"""
Doctor Routes - All doctor-related endpoints
Handles patient management, medical records review, diagnosis notes, and doctor profile
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from datetime import datetime
import json

from auth.jwt import verify_token, require_role
from services.s3 import S3Service
from services.ses import SESService
from database import Database

# Router setup
doctor_router = APIRouter()
security = HTTPBearer()

# Services
db = Database()
s3_service = S3Service()
ses_service = SESService()

# Dependency to get current doctor
async def get_current_doctor(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current doctor from JWT token"""
    payload = verify_token(credentials.credentials)
    require_role(payload, "doctor")
    
    user_id = payload.get("user_id")
    user = await db.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    return user

@doctor_router.get("/profile")
async def get_doctor_profile(current_doctor = Depends(get_current_doctor)):
    """Get doctor profile information"""
    try:
        profile = await db.get_doctor_profile(str(current_doctor["_id"]))
        return {
            "id": str(current_doctor["_id"]),
            "email": current_doctor["email"],
            "name": current_doctor["name"],
            "role": current_doctor["role"],
            "profile": profile or {}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile: {str(e)}"
        )

@doctor_router.put("/profile")
async def update_doctor_profile(
    profile_data: dict,
    current_doctor = Depends(get_current_doctor)
):
    """Update doctor profile information"""
    try:
        updated_profile = await db.update_doctor_profile(
            str(current_doctor["_id"]),
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

@doctor_router.get("/patients")
async def get_doctor_patients(current_doctor = Depends(get_current_doctor)):
    """Get list of patients assigned to this doctor"""
    try:
        patients = await db.get_doctor_patients(str(current_doctor["_id"]))
        
        formatted_patients = []
        for patient in patients:
            # Get patient profile
            profile = await db.get_patient_profile(str(patient["_id"]))
            
            # Get latest appointment
            latest_appointment = await db.get_latest_appointment(
                str(patient["_id"]),
                str(current_doctor["_id"])
            )
            
            formatted_patients.append({
                "id": str(patient["_id"]),
                "name": patient["name"],
                "email": patient["email"],
                "profile": profile or {},
                "latest_appointment": latest_appointment,
                "total_appointments": await db.count_patient_appointments(
                    str(patient["_id"]),
                    str(current_doctor["_id"])
                )
            })
        
        return {
            "patients": formatted_patients,
            "total": len(formatted_patients)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get patients: {str(e)}"
        )

@doctor_router.get("/patients/{patient_id}")
async def get_patient_details(
    patient_id: str,
    current_doctor = Depends(get_current_doctor)
):
    """Get detailed information about a specific patient"""
    try:
        # Verify patient exists and has appointments with this doctor
        patient = await db.get_user_by_id(patient_id)
        if not patient or patient["role"] != "patient":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        # Check if doctor has treated this patient
        has_appointment = await db.check_doctor_patient_relationship(
            str(current_doctor["_id"]),
            patient_id
        )
        
        if not has_appointment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No treatment relationship with this patient"
            )
        
        # Get patient profile
        profile = await db.get_patient_profile(patient_id)
        
        # Get appointment history
        appointments = await db.get_patient_appointments_with_doctor(
            patient_id,
            str(current_doctor["_id"])
        )
        
        return {
            "id": str(patient["_id"]),
            "name": patient["name"],
            "email": patient["email"],
            "profile": profile or {},
            "appointments": appointments,
            "total_appointments": len(appointments)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get patient details: {str(e)}"
        )

@doctor_router.get("/medical-records")
async def get_patient_medical_records(
    patient_id: Optional[str] = None,
    current_doctor = Depends(get_current_doctor)
):
    """Get medical records for doctor to review"""
    try:
        if patient_id:
            # Get records for specific patient
            # Verify doctor-patient relationship
            has_relationship = await db.check_doctor_patient_relationship(
                str(current_doctor["_id"]),
                patient_id
            )
            
            if not has_relationship:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No treatment relationship with this patient"
                )
            
            records = await db.get_patient_medical_records(patient_id)
        else:
            # Get all records from doctor's patients
            records = await db.get_doctor_patient_records(str(current_doctor["_id"]))
        
        formatted_records = []
        for record in records:
            # Get patient info
            patient = await db.get_user_by_id(record["patient_id"])
            
            formatted_records.append({
                "id": str(record["_id"]),
                "patient_name": patient["name"] if patient else "Unknown",
                "patient_id": record["patient_id"],
                "filename": record["filename"],
                "file_type": record["file_type"],
                "file_size": record["file_size"],
                "description": record["description"],
                "upload_date": record["upload_date"].isoformat(),
                "uploaded_by": record["uploaded_by"],
                "reviewed": record.get("reviewed", False),
                "reviewed_by": record.get("reviewed_by"),
                "reviewed_at": record.get("reviewed_at")
            })
        
        return {
            "records": formatted_records,
            "total": len(formatted_records)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get medical records: {str(e)}"
        )

@doctor_router.get("/medical-records/{record_id}/download")
async def download_patient_medical_record(
    record_id: str,
    current_doctor = Depends(get_current_doctor)
):
    """Generate signed URL for downloading patient medical record"""
    try:
        # Get record from database
        record = await db.get_medical_record(record_id)
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical record not found"
            )
        
        # Verify doctor-patient relationship
        has_relationship = await db.check_doctor_patient_relationship(
            str(current_doctor["_id"]),
            record["patient_id"]
        )
        
        if not has_relationship:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No treatment relationship with this patient"
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

@doctor_router.put("/medical-records/{record_id}/review")
async def mark_record_reviewed(
    record_id: str,
    current_doctor = Depends(get_current_doctor)
):
    """Mark a medical record as reviewed by the doctor"""
    try:
        # Get record from database
        record = await db.get_medical_record(record_id)
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical record not found"
            )
        
        # Verify doctor-patient relationship
        has_relationship = await db.check_doctor_patient_relationship(
            str(current_doctor["_id"]),
            record["patient_id"]
        )
        
        if not has_relationship:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No treatment relationship with this patient"
            )
        
        # Update record
        await db.update_medical_record(record_id, {
            "reviewed": True,
            "reviewed_by": str(current_doctor["_id"]),
            "reviewed_at": datetime.now()
        })
        
        return {
            "message": "Medical record marked as reviewed",
            "record_id": record_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark record as reviewed: {str(e)}"
        )

@doctor_router.post("/diagnosis")
async def create_diagnosis(
    diagnosis_data: dict,
    current_doctor = Depends(get_current_doctor)
):
    """
    Create a new diagnosis for a patient
    
    Body:
    - patient_id: str
    - appointment_id: str (optional)
    - diagnosis: str
    - symptoms: str
    - treatment_plan: str
    - notes: str (optional)
    - prescriptions: list[str] (optional)
    - follow_up_date: str (optional)
    """
    try:
        # Validate required fields
        required_fields = ["patient_id", "diagnosis", "symptoms", "treatment_plan"]
        for field in required_fields:
            if field not in diagnosis_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}"
                )
        
        # Verify doctor-patient relationship
        has_relationship = await db.check_doctor_patient_relationship(
            str(current_doctor["_id"]),
            diagnosis_data["patient_id"]
        )
        
        if not has_relationship:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No treatment relationship with this patient"
            )
        
        # Create diagnosis
        diagnosis = {
            "patient_id": diagnosis_data["patient_id"],
            "doctor_id": str(current_doctor["_id"]),
            "appointment_id": diagnosis_data.get("appointment_id"),
            "diagnosis": diagnosis_data["diagnosis"],
            "symptoms": diagnosis_data["symptoms"],
            "treatment_plan": diagnosis_data["treatment_plan"],
            "notes": diagnosis_data.get("notes", ""),
            "prescriptions": diagnosis_data.get("prescriptions", []),
            "follow_up_date": diagnosis_data.get("follow_up_date"),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        created_diagnosis = await db.create_diagnosis(diagnosis)
        
        # Send notification email to patient (optional)
        try:
            patient = await db.get_user_by_id(diagnosis_data["patient_id"])
            if patient:
                await ses_service.send_diagnosis_notification(
                    patient["email"],
                    patient["name"],
                    current_doctor["name"],
                    diagnosis_data["diagnosis"]
                )
        except Exception as e:
            # Email notification failure should not break the diagnosis creation
            print(f"Failed to send email notification: {str(e)}")
        
        return {
            "message": "Diagnosis created successfully",
            "diagnosis": {
                "id": str(created_diagnosis["_id"]),
                "diagnosis": created_diagnosis["diagnosis"],
                "created_at": created_diagnosis["created_at"].isoformat()
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create diagnosis: {str(e)}"
        )

@doctor_router.get("/diagnosis")
async def get_doctor_diagnoses(
    patient_id: Optional[str] = None,
    current_doctor = Depends(get_current_doctor)
):
    """Get all diagnoses created by this doctor"""
    try:
        if patient_id:
            # Verify doctor-patient relationship
            has_relationship = await db.check_doctor_patient_relationship(
                str(current_doctor["_id"]),
                patient_id
            )
            
            if not has_relationship:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No treatment relationship with this patient"
                )
            
            diagnoses = await db.get_patient_diagnoses(patient_id, str(current_doctor["_id"]))
        else:
            diagnoses = await db.get_doctor_diagnoses(str(current_doctor["_id"]))
        
        formatted_diagnoses = []
        for diagnosis in diagnoses:
            # Get patient info
            patient = await db.get_user_by_id(diagnosis["patient_id"])
            
            formatted_diagnoses.append({
                "id": str(diagnosis["_id"]),
                "patient_name": patient["name"] if patient else "Unknown",
                "patient_id": diagnosis["patient_id"],
                "diagnosis": diagnosis["diagnosis"],
                "symptoms": diagnosis["symptoms"],
                "treatment_plan": diagnosis["treatment_plan"],
                "notes": diagnosis["notes"],
                "prescriptions": diagnosis["prescriptions"],
                "follow_up_date": diagnosis.get("follow_up_date"),
                "created_at": diagnosis["created_at"].isoformat(),
                "updated_at": diagnosis["updated_at"].isoformat()
            })
        
        return {
            "diagnoses": formatted_diagnoses,
            "total": len(formatted_diagnoses)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get diagnoses: {str(e)}"
        )

@doctor_router.put("/diagnosis/{diagnosis_id}")
async def update_diagnosis(
    diagnosis_id: str,
    diagnosis_data: dict,
    current_doctor = Depends(get_current_doctor)
):
    """Update an existing diagnosis"""
    try:
        # Get existing diagnosis
        existing_diagnosis = await db.get_diagnosis(diagnosis_id)
        
        if not existing_diagnosis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnosis not found"
            )
        
        # Verify ownership
        if str(existing_diagnosis["doctor_id"]) != str(current_doctor["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Update diagnosis
        diagnosis_data["updated_at"] = datetime.now()
        updated_diagnosis = await db.update_diagnosis(diagnosis_id, diagnosis_data)
        
        return {
            "message": "Diagnosis updated successfully",
            "diagnosis": {
                "id": str(updated_diagnosis["_id"]),
                "diagnosis": updated_diagnosis["diagnosis"],
                "updated_at": updated_diagnosis["updated_at"].isoformat()
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update diagnosis: {str(e)}"
        )

@doctor_router.get("/appointments")
async def get_doctor_appointments(current_doctor = Depends(get_current_doctor)):
    """Get all appointments for this doctor"""
    try:
        appointments = await db.get_doctor_appointments(str(current_doctor["_id"]))
        
        formatted_appointments = []
        for appointment in appointments:
            # Get patient info
            patient = await db.get_user_by_id(appointment["patient_id"])
            
            formatted_appointments.append({
                "id": str(appointment["_id"]),
                "patient_name": patient["name"] if patient else "Unknown",
                "patient_id": appointment["patient_id"],
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

@doctor_router.put("/appointments/{appointment_id}/status")
async def update_appointment_status(
    appointment_id: str,
    status_data: dict,
    current_doctor = Depends(get_current_doctor)
):
    """Update appointment status (e.g., completed, cancelled)"""
    try:
        # Get appointment
        appointment = await db.get_appointment(appointment_id)
        
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
        
        # Verify ownership
        if str(appointment["doctor_id"]) != str(current_doctor["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Validate status
        valid_statuses = ["scheduled", "completed", "cancelled", "no-show"]
        if status_data.get("status") not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status"
            )
        
        # Update appointment
        await db.update_appointment(appointment_id, {
            "status": status_data["status"],
            "notes": status_data.get("notes", ""),
            "updated_at": datetime.now()
        })
        
        return {
            "message": "Appointment status updated successfully",
            "appointment_id": appointment_id,
            "status": status_data["status"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update appointment status: {str(e)}"
        )