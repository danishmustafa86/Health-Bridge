# MedCare Backend API

A comprehensive medical/healthcare FastAPI application with JWT authentication, role-based access control, and integration with AWS services and Stripe payments.

## Features

### 🔐 Authentication & Authorization
- JWT-based authentication with access and refresh tokens
- Role-based access control (Patient/Doctor)
- Secure password hashing with bcrypt
- Token expiration and refresh mechanisms

### 👥 User Management
- Patient and Doctor registration/login
- Profile management for both user types
- Email validation and verification

### 🏥 Patient Features
- Medical record upload to AWS S3
- Appointment booking with available doctors
- Stripe payment integration for consultations
- View appointment history and medical records
- Download medical documents

### 👨‍⚕️ Doctor Features
- Patient management and assignment
- Medical record review and approval
- Diagnosis creation and management
- Appointment scheduling and status updates
- Email notifications via AWS SES

### 💾 Data Management
- MongoDB with async operations
- Comprehensive data models with Pydantic
- File storage on AWS S3 with signed URLs
- Secure data validation and sanitization

## Technology Stack

- **Framework**: FastAPI 0.104.1
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT with python-jose
- **File Storage**: AWS S3 with boto3
- **Payments**: Stripe API integration
- **Email**: AWS SES for notifications
- **Security**: bcrypt for password hashing

## Installation & Setup

### Prerequisites
- Python 3.10+
- MongoDB (local or Atlas)
- AWS Account (for S3 and SES)
- Stripe Account (for payments)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your actual configuration values
```

### 3. Required Environment Variables
```env
# Database
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=medcare

# JWT
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# AWS
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET_NAME=medcare-files
FROM_EMAIL=noreply@yourdomain.com
```

### 4. Database Setup
```bash
# Start MongoDB locally or use MongoDB Atlas
# The application will automatically create indexes on startup
```

### 5. AWS Setup
```bash
# Create S3 bucket for file storage
aws s3 mb s3://medcare-files

# Verify SES email addresses for sending notifications
aws ses verify-email-identity --email-address noreply@yourdomain.com
```

### 6. Run the Application
```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Authentication Endpoints
```
POST /api/auth/register - Register new user
POST /api/auth/login - User login
GET /api/auth/me - Get current user info
```

### Patient Endpoints
```
GET /api/patient/profile - Get patient profile
PUT /api/patient/profile - Update patient profile
POST /api/patient/upload-medical-record - Upload medical record
GET /api/patient/medical-records - Get patient's medical records
GET /api/patient/doctors - Get available doctors
POST /api/patient/book-appointment - Book appointment
GET /api/patient/appointments - Get patient appointments
POST /api/patient/appointments/{id}/payment - Process payment
```

### Doctor Endpoints
```
GET /api/doctor/profile - Get doctor profile
PUT /api/doctor/profile - Update doctor profile
GET /api/doctor/patients - Get assigned patients
GET /api/doctor/medical-records - Get patient medical records
POST /api/doctor/diagnosis - Create diagnosis
GET /api/doctor/diagnosis - Get doctor's diagnoses
GET /api/doctor/appointments - Get doctor appointments
PUT /api/doctor/appointments/{id}/status - Update appointment status
```

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── routes/
│   ├── patient.py         # Patient-related endpoints
│   └── doctor.py          # Doctor-related endpoints
├── auth/
│   └── jwt.py             # JWT authentication logic
├── services/
│   ├── stripe.py          # Stripe payment service
│   ├── s3.py              # AWS S3 file service
│   └── ses.py             # AWS SES email service
├── models/
│   └── user.py            # Pydantic data models
├── utils/
│   └── helpers.py         # Utility functions
├── database.py            # MongoDB operations
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Security Features

### Data Protection
- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control
- Input validation with Pydantic
- SQL injection prevention (NoSQL)

### File Security
- Secure file upload to AWS S3
- File type validation
- Size limitations (10MB max)
- Signed URLs for downloads
- Access control based on ownership

### API Security
- CORS configuration
- Request rate limiting
- Input sanitization
- Error handling without data leakage

## Testing

### Sample Data
The application includes sample users for testing:

**Patient Account:**
- Email: patient@demo.com
- Password: password

**Doctor Account:**
- Email: doctor@demo.com
- Password: password

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

## Deployment

### Docker Deployment
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations
- Use environment-specific configuration
- Set up proper logging and monitoring
- Configure reverse proxy (nginx)
- Set up SSL/TLS certificates
- Use production database (MongoDB Atlas)
- Configure backup strategies
- Set up health checks and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the code comments and docstrings

## Changelog

### Version 1.0.0
- Initial release with core functionality
- JWT authentication and authorization
- Patient and doctor management
- Medical record upload/download
- Appointment booking and payment
- Email notifications
- Comprehensive API documentation