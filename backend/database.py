"""
Database Module
Handles MongoDB operations and data management
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from typing import Optional, Dict, Any, List
from datetime import datetime
from bson import ObjectId
import hashlib
import bcrypt

class Database:
    """Database class for MongoDB operations"""
    
    def __init__(self):
        """Initialize database connection"""
        self.database_url = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
        self.database_name = os.getenv("DATABASE_NAME", "medcare")
        
        try:
            self.client = AsyncIOMotorClient(self.database_url)
            self.db = self.client[self.database_name]
            
            # Create indexes
            self._create_indexes()
            
        except ConnectionFailure as e:
            raise ConnectionError(f"Failed to connect to database: {str(e)}")
    
    def _create_indexes(self):
        """Create database indexes for better performance"""
        # Users collection indexes
        self.db.users.create_index("email", unique=True)
        self.db.users.create_index("role")
        
        # Appointments collection indexes
        self.db.appointments.create_index([("patient_id", 1), ("doctor_id", 1)])
        self.db.appointments.create_index("appointment_date")
        self.db.appointments.create_index("status")
        
        # Medical records collection indexes
        self.db.medical_records.create_index("patient_id")
        self.db.medical_records.create_index("upload_date")
        
        # Diagnoses collection indexes
        self.db.diagnoses.create_index([("patient_id", 1), ("doctor_id", 1)])
        self.db.diagnoses.create_index("created_at")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        try:
            self.client.admin.command('ping')
            return True
        except ConnectionFailure:
            return False
    
    # User operations
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            # Hash password
            user_data["password"] = self._hash_password(user_data["password"])
            user_data["created_at"] = datetime.now()
            user_data["updated_at"] = datetime.now()
            
            result = await self.db.users.insert_one(user_data)
            user_data["_id"] = result.inserted_id
            
            return user_data
            
        except DuplicateKeyError:
            raise ValueError("User with this email already exists")
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        return await self.db.users.find_one({"email": email})
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return await self.db.users.find_one({"_id": ObjectId(user_id)})
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        user = await self.get_user_by_email(email)
        
        if user and self._verify_password(password, user["password"]):
            return user
        
        return None
    
    # Patient operations
    async def get_patient_profile(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get patient profile"""
        return await self.db.patient_profiles.find_one({"patient_id": patient_id})
    
    async def update_patient_profile(self, patient_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update patient profile"""
        profile_data["updated_at"] = datetime.now()
        
        result = await self.db.patient_profiles.update_one(
            {"patient_id": patient_id},
            {"$set": profile_data},
            upsert=True
        )
        
        return await self.get_patient_profile(patient_id)
    
    # Doctor operations
    async def get_doctor_profile(self, doctor_id: str) -> Optional[Dict[str, Any]]:
        """Get doctor profile"""
        return await self.db.doctor_profiles.find_one({"doctor_id": doctor_id})
    
    async def update_doctor_profile(self, doctor_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update doctor profile"""
        profile_data["updated_at"] = datetime.now()
        
        result = await self.db.doctor_profiles.update_one(
            {"doctor_id": doctor_id},
            {"$set": profile_data},
            upsert=True
        )
        
        return await self.get_doctor_profile(doctor_id)
    
    async def get_available_doctors(self) -> List[Dict[str, Any]]:
        """Get list of available doctors"""
        doctors = []
        async for user in self.db.users.find({"role": "doctor"}):
            # Get doctor profile
            profile = await self.get_doctor_profile(str(user["_id"]))
            if profile:
                user.update(profile)
            doctors.append(user)
        
        return doctors
    
    async def get_doctor_patients(self, doctor_id: str) -> List[Dict[str, Any]]:
        """Get patients assigned to a doctor"""
        # Get unique patient IDs from appointments
        patient_ids = await self.db.appointments.distinct("patient_id", {"doctor_id": doctor_id})
        
        patients = []
        for patient_id in patient_ids:
            patient = await self.get_user_by_id(patient_id)
            if patient:
                patients.append(patient)
        
        return patients
    
    # Medical records operations
    async def create_medical_record(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new medical record"""
        record_data["created_at"] = datetime.now()
        result = await self.db.medical_records.insert_one(record_data)
        record_data["_id"] = result.inserted_id
        return record_data
    
    async def get_medical_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Get medical record by ID"""
        return await self.db.medical_records.find_one({"_id": ObjectId(record_id)})
    
    async def get_patient_medical_records(self, patient_id: str) -> List[Dict[str, Any]]:
        """Get all medical records for a patient"""
        records = []
        async for record in self.db.medical_records.find({"patient_id": patient_id}).sort("upload_date", -1):
            records.append(record)
        return records
    
    async def get_doctor_patient_records(self, doctor_id: str) -> List[Dict[str, Any]]:
        """Get medical records for all patients of a doctor"""
        # Get patient IDs for this doctor
        patient_ids = await self.db.appointments.distinct("patient_id", {"doctor_id": doctor_id})
        
        records = []
        async for record in self.db.medical_records.find({"patient_id": {"$in": patient_ids}}).sort("upload_date", -1):
            records.append(record)
        
        return records
    
    async def update_medical_record(self, record_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update medical record"""
        update_data["updated_at"] = datetime.now()
        
        await self.db.medical_records.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": update_data}
        )
        
        return await self.get_medical_record(record_id)
    
    # Appointment operations
    async def create_appointment(self, appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new appointment"""
        appointment_data["created_at"] = datetime.now()
        result = await self.db.appointments.insert_one(appointment_data)
        appointment_data["_id"] = result.inserted_id
        return appointment_data
    
    async def get_appointment(self, appointment_id: str) -> Optional[Dict[str, Any]]:
        """Get appointment by ID"""
        return await self.db.appointments.find_one({"_id": ObjectId(appointment_id)})
    
    async def update_appointment(self, appointment_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update appointment"""
        update_data["updated_at"] = datetime.now()
        
        await self.db.appointments.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": update_data}
        )
        
        return await self.get_appointment(appointment_id)
    
    async def get_patient_appointments(self, patient_id: str) -> List[Dict[str, Any]]:
        """Get all appointments for a patient"""
        appointments = []
        async for appointment in self.db.appointments.find({"patient_id": patient_id}).sort("created_at", -1):
            appointments.append(appointment)
        return appointments
    
    async def get_doctor_appointments(self, doctor_id: str) -> List[Dict[str, Any]]:
        """Get all appointments for a doctor"""
        appointments = []
        async for appointment in self.db.appointments.find({"doctor_id": doctor_id}).sort("appointment_date", 1):
            appointments.append(appointment)
        return appointments
    
    async def check_appointment_availability(self, doctor_id: str, date: str, time: str) -> bool:
        """Check if appointment slot is available"""
        existing = await self.db.appointments.find_one({
            "doctor_id": doctor_id,
            "appointment_date": date,
            "appointment_time": time,
            "status": {"$ne": "cancelled"}
        })
        
        return existing is None
    
    async def get_latest_appointment(self, patient_id: str, doctor_id: str) -> Optional[Dict[str, Any]]:
        """Get latest appointment between patient and doctor"""
        return await self.db.appointments.find_one(
            {"patient_id": patient_id, "doctor_id": doctor_id},
            sort=[("created_at", -1)]
        )
    
    async def count_patient_appointments(self, patient_id: str, doctor_id: str) -> int:
        """Count appointments between patient and doctor"""
        return await self.db.appointments.count_documents({
            "patient_id": patient_id,
            "doctor_id": doctor_id
        })
    
    async def get_patient_appointments_with_doctor(self, patient_id: str, doctor_id: str) -> List[Dict[str, Any]]:
        """Get all appointments between patient and doctor"""
        appointments = []
        async for appointment in self.db.appointments.find({
            "patient_id": patient_id,
            "doctor_id": doctor_id
        }).sort("created_at", -1):
            appointments.append(appointment)
        return appointments
    
    async def check_doctor_patient_relationship(self, doctor_id: str, patient_id: str) -> bool:
        """Check if doctor has treated this patient"""
        appointment = await self.db.appointments.find_one({
            "doctor_id": doctor_id,
            "patient_id": patient_id
        })
        
        return appointment is not None
    
    # Diagnosis operations
    async def create_diagnosis(self, diagnosis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new diagnosis"""
        diagnosis_data["created_at"] = datetime.now()
        diagnosis_data["updated_at"] = datetime.now()
        
        result = await self.db.diagnoses.insert_one(diagnosis_data)
        diagnosis_data["_id"] = result.inserted_id
        return diagnosis_data
    
    async def get_diagnosis(self, diagnosis_id: str) -> Optional[Dict[str, Any]]:
        """Get diagnosis by ID"""
        return await self.db.diagnoses.find_one({"_id": ObjectId(diagnosis_id)})
    
    async def update_diagnosis(self, diagnosis_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update diagnosis"""
        update_data["updated_at"] = datetime.now()
        
        await self.db.diagnoses.update_one(
            {"_id": ObjectId(diagnosis_id)},
            {"$set": update_data}
        )
        
        return await self.get_diagnosis(diagnosis_id)
    
    async def get_patient_diagnoses(self, patient_id: str, doctor_id: str = None) -> List[Dict[str, Any]]:
        """Get diagnoses for a patient"""
        query = {"patient_id": patient_id}
        if doctor_id:
            query["doctor_id"] = doctor_id
        
        diagnoses = []
        async for diagnosis in self.db.diagnoses.find(query).sort("created_at", -1):
            diagnoses.append(diagnosis)
        return diagnoses
    
    async def get_doctor_diagnoses(self, doctor_id: str) -> List[Dict[str, Any]]:
        """Get all diagnoses created by a doctor"""
        diagnoses = []
        async for diagnosis in self.db.diagnoses.find({"doctor_id": doctor_id}).sort("created_at", -1):
            diagnoses.append(diagnosis)
        return diagnoses
    
    async def get_appointment_diagnosis(self, appointment_id: str) -> Optional[Dict[str, Any]]:
        """Get diagnosis for a specific appointment"""
        return await self.db.diagnoses.find_one({"appointment_id": appointment_id})