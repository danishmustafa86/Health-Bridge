# MedCare 🏥💻

*A Full-Stack Medical Healthcare Application with Role-Based Access Control*

---

## 📖 Description

**MedCare** is a comprehensive healthcare platform that connects patients with verified doctors through a modern web interface. Our platform provides secure appointment booking, medical record management, and consultation services with role-based access control for both patients and healthcare professionals.

Whether you're a patient seeking quality healthcare or a doctor managing your practice, MedCare offers an intuitive and secure platform for all your healthcare needs.

## ✨ Key Features

### 👨‍⚕️ **For Doctors**
- **Patient Management**: View and manage assigned patients with detailed profiles
- **Medical Records Review**: Access and review patient medical records securely
- **Diagnosis Notes**: Create comprehensive diagnosis records with prescriptions
- **Appointment Management**: View and update appointment statuses
- **Professional Profile**: Manage credentials, specializations, and consultation fees

### 🏥 **For Patients**
- **Easy Appointment Booking**: Book appointments with qualified doctors
- **Medical Records Upload**: Securely upload and manage medical documents
- **Appointment History**: Track past and upcoming appointments with ratings
- **Secure Payments**: Process consultation fees through integrated payment system
- **Profile Management**: Maintain personal and medical information

### 🔐 **Security & Authentication**
- JWT-based authentication with role-based access control
- Secure password hashing with bcrypt
- Protected routes based on user roles
- Session management with token refresh

### 💾 **Data Management**
- MongoDB integration for scalable data storage
- File upload to AWS S3 with secure access
- Email notifications via AWS SES
- Stripe payment processing integration

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | Modern UI framework with hooks |
| **TypeScript** | Type-safe development |
| **Tailwind CSS** | Utility-first CSS framework |
| **React Router** | Client-side routing |
| **Lucide React** | Beautiful icon library |
| **Vite** | Fast build tool and dev server |

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance Python web framework |
| **MongoDB** | NoSQL database with Motor async driver |
| **JWT** | Secure authentication tokens |
| **AWS S3** | File storage and management |
| **AWS SES** | Email notification service |
| **Stripe** | Payment processing |
| **bcrypt** | Password hashing |

## 📸 Screenshots

### Landing Page
![Landing Page](./assets/screenshots/landing.png)

### Patient Dashboard
![Patient Dashboard](./assets/screenshots/patient-dashboard.png)

### Doctor Dashboard
![Doctor Dashboard](./assets/screenshots/doctor-dashboard.png)

### Appointment Booking
![Appointment Booking](./assets/screenshots/appointment-booking.png)

### Medical Records
![Medical Records](./assets/screenshots/medical-records.png)

## 🚀 Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- MongoDB (local or Atlas)
- AWS Account (for S3 and SES)
- Stripe Account (for payments)

### Frontend Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

3. **Access the application**
   - Open your browser and go to `http://localhost:5173`

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `backend/.env.example` to `backend/.env`
   - Fill in your API keys and configuration

5. **Run the backend server**
   ```bash
   python main.py
   ```

6. **API Documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## 🔐 Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=medcare

# JWT Authentication
SECRET_KEY=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=medcare-files
FROM_EMAIL=noreply@yourdomain.com

# Application Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### How to Get API Keys:

1. **MongoDB**: Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) or use local MongoDB
2. **Stripe**: Create account at [Stripe Dashboard](https://dashboard.stripe.com)
3. **AWS S3 & SES**: Set up at [AWS Console](https://console.aws.amazon.com)

## 📁 Project Structure

```
medcare/
├── src/                           # Frontend React application
│   ├── components/               # React components
│   │   ├── auth/                # Authentication components
│   │   ├── patient/             # Patient-specific components
│   │   ├── doctor/              # Doctor-specific components
│   │   └── ui/                  # Reusable UI components
│   ├── contexts/                # React contexts (Auth, etc.)
│   └── main.tsx                 # Application entry point
├── 
├── backend/                      # FastAPI backend
│   ├── routes/                  # API route handlers
│   │   ├── patient.py          # Patient endpoints
│   │   └── doctor.py           # Doctor endpoints
│   ├── auth/                    # Authentication logic
│   ├── services/                # External service integrations
│   │   ├── stripe.py           # Payment processing
│   │   ├── s3.py               # File storage
│   │   └── ses.py              # Email service
│   ├── models/                  # Data models
│   ├── database.py             # Database operations
│   └── main.py                 # FastAPI application
├── 
├── package.json                 # Frontend dependencies
├── tailwind.config.js          # Tailwind CSS configuration
├── vite.config.ts              # Vite build configuration
└── README.md                   # This file
```

## 🔮 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Patient Endpoints
- `GET /api/patient/profile` - Get patient profile
- `PUT /api/patient/profile` - Update patient profile
- `POST /api/patient/upload-medical-record` - Upload medical record
- `GET /api/patient/medical-records` - Get patient's records
- `GET /api/patient/doctors` - Get available doctors
- `POST /api/patient/book-appointment` - Book appointment
- `GET /api/patient/appointments` - Get patient appointments

### Doctor Endpoints
- `GET /api/doctor/profile` - Get doctor profile
- `PUT /api/doctor/profile` - Update doctor profile
- `GET /api/doctor/patients` - Get assigned patients
- `GET /api/doctor/medical-records` - Get patient records
- `POST /api/doctor/diagnosis` - Create diagnosis
- `GET /api/doctor/appointments` - Get doctor appointments

## 🧪 Demo Accounts

### Patient Account
- **Email**: `patient@demo.com`
- **Password**: `password`

### Doctor Account
- **Email**: `doctor@demo.com`
- **Password**: `password`

## 🔒 Security Features

- **Authentication**: JWT tokens with role-based access
- **Data Protection**: Encrypted passwords with bcrypt
- **File Security**: Secure S3 uploads with signed URLs
- **Input Validation**: Comprehensive data validation
- **CORS Protection**: Configured for secure cross-origin requests

## 🚀 Deployment

### Frontend (Netlify/Vercel)
```bash
npm run build
# Deploy dist/ folder to your hosting provider
```

### Backend (Production)
```bash
# Using gunicorn for production
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the code comments and documentation

---

<div align="center">

**Built with ❤️ for Modern Healthcare**

*Connecting Patients and Doctors Through Technology*

[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-blue.svg)](https://tailwindcss.com/)

</div>