# MedCare 🏥💻🤖

*A Full-Stack Medical Healthcare Application with AI-Powered Diagnostics and Role-Based Access Control*

---

## 📖 Description

**MedCare** is a comprehensive healthcare platform that connects patients with verified doctors through a modern web interface enhanced with cutting-edge AI technology. Our platform leverages **Groq AI** and **LLaMA models** to provide intelligent symptom analysis, preliminary diagnostics, and treatment recommendations, while maintaining secure appointment booking, medical record management, and consultation services with role-based access control.

Whether you're a patient seeking AI-enhanced healthcare insights or a doctor utilizing advanced AI tools for better patient care, MedCare offers an intuitive, secure, and intelligent platform for all your healthcare needs.

## ✨ Key Features

### 🤖 **AI-Powered Healthcare Intelligence**
- **Groq AI Integration**: Ultra-fast AI inference for real-time medical analysis
- **LLaMA Model Support**: Advanced language models for medical text understanding
- **Intelligent Symptom Checker**: AI-powered preliminary diagnosis based on symptoms
- **Medical Report Analysis**: Automated analysis of uploaded medical documents
- **Treatment Recommendations**: AI-generated treatment suggestions for doctors
- **Drug Interaction Checker**: AI-powered medication safety analysis
- **Medical Literature Search**: AI-enhanced search through medical databases

### 👨‍⚕️ **For Doctors (AI-Enhanced)**
- **AI Diagnostic Assistant**: Get AI-powered insights for patient diagnosis
- **Patient Management**: View and manage assigned patients with AI-generated summaries
- **Medical Records Review**: AI-enhanced analysis of patient medical records
- **Diagnosis Notes**: Create comprehensive diagnosis records with AI suggestions
- **Appointment Management**: AI-optimized scheduling and patient prioritization
- **Professional Profile**: Manage credentials, specializations, and consultation fees
- **Clinical Decision Support**: AI-powered treatment recommendations

### 🏥 **For Patients (AI-Powered)**
- **AI Symptom Checker**: Get preliminary AI analysis of your symptoms
- **Smart Appointment Booking**: AI-recommended doctor matching based on symptoms
- **Medical Records Upload**: AI-powered document analysis and categorization
- **Appointment History**: Track appointments with AI-generated health insights
- **Secure Payments**: Process consultation fees through integrated payment system
- **Health Insights**: AI-powered health trend analysis and recommendations
- **Medication Reminders**: AI-optimized medication scheduling

### 🔐 **Security & Authentication**
- JWT-based authentication with role-based access control
- Secure password hashing with bcrypt
- Protected routes based on user roles
- Session management with token refresh
- HIPAA-compliant data handling for AI processing

### 💾 **Data Management & AI Processing**
- MongoDB integration for scalable data storage
- File upload to AWS S3 with secure access
- Email notifications via AWS SES
- Stripe payment processing integration
- **Groq AI API** for lightning-fast inference
- **LLaMA model deployment** for advanced medical NLP
- Secure AI data processing with privacy protection

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

### AI & Machine Learning
| Technology | Purpose |
|------------|---------|
| **Groq AI** | Ultra-fast AI inference engine |
| **LLaMA Models** | Advanced language models for medical NLP |
| **Transformers** | Hugging Face transformers for model deployment |
| **OpenAI API** | Additional AI capabilities (optional) |
| **scikit-learn** | Traditional ML algorithms for health analytics |
| **pandas** | Data processing for AI model inputs |

## 🤖 AI Integration Details

### Groq AI Implementation
- **Real-time Inference**: Sub-second response times for medical queries
- **Symptom Analysis**: Instant preliminary diagnosis suggestions
- **Medical Text Processing**: Fast analysis of patient reports and notes
- **Drug Interaction Checking**: Rapid medication safety verification

### LLaMA Model Applications
- **Medical Literature Understanding**: Advanced comprehension of medical texts
- **Patient Communication**: Natural language processing for patient queries
- **Clinical Note Generation**: AI-assisted medical documentation
- **Treatment Planning**: Intelligent treatment recommendation generation

### AI Workflow
```
Patient Input → Groq AI Processing → LLaMA Analysis → Medical Insights → Doctor Review
```

## 📸 Screenshots

### AI Symptom Checker
![AI Symptom Checker](./assets/screenshots/ai-symptom-checker.png)

### AI-Enhanced Doctor Dashboard
![AI Doctor Dashboard](./assets/screenshots/ai-doctor-dashboard.png)

### Landing Page
![Landing Page](./assets/screenshots/landing.png)

### Patient Dashboard
![Patient Dashboard](./assets/screenshots/patient-dashboard.png)

### Appointment Booking
![Appointment Booking](./assets/screenshots/appointment-booking.png)

### Medical Records with AI Analysis
![Medical Records](./assets/screenshots/medical-records-ai.png)

## 🚀 Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- MongoDB (local or Atlas)
- AWS Account (for S3 and SES)
- Stripe Account (for payments)
- **Groq AI API Key**
- **Hugging Face Account** (for LLaMA models)

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

4. **Install AI dependencies**
   ```bash
   pip install groq transformers torch huggingface-hub
   ```

5. **Set up environment variables**
   - Copy `backend/.env.example` to `backend/.env`
   - Fill in your API keys and configuration (including AI keys)

6. **Run the backend server**
   ```bash
   python main.py
   ```

7. **API Documentation**
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

# AI Configuration
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_API_TOKEN=your_huggingface_token_here
LLAMA_MODEL_NAME=meta-llama/Llama-2-7b-chat-hf
OPENAI_API_KEY=your_openai_key_here  # Optional

# Application Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### How to Get AI API Keys:

1. **Groq AI**: Sign up at [Groq Console](https://console.groq.com) for ultra-fast inference
2. **Hugging Face**: Create account at [Hugging Face](https://huggingface.co) for LLaMA models
3. **MongoDB**: Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
4. **Stripe**: Create account at [Stripe Dashboard](https://dashboard.stripe.com)
5. **AWS S3 & SES**: Set up at [AWS Console](https://console.aws.amazon.com)

## 📁 Project Structure

```
medcare/
├── src/                           # Frontend React application
│   ├── components/               # React components
│   │   ├── auth/                # Authentication components
│   │   ├── patient/             # Patient-specific components
│   │   ├── doctor/              # Doctor-specific components
│   │   ├── ai/                  # AI-powered components
│   │   └── ui/                  # Reusable UI components
│   ├── contexts/                # React contexts (Auth, AI, etc.)
│   └── main.tsx                 # Application entry point
├── 
├── backend/                      # FastAPI backend
│   ├── routes/                  # API route handlers
│   │   ├── patient.py          # Patient endpoints
│   │   ├── doctor.py           # Doctor endpoints
│   │   └── ai.py               # AI-powered endpoints
│   ├── auth/                    # Authentication logic
│   ├── services/                # External service integrations
│   │   ├── stripe.py           # Payment processing
│   │   ├── s3.py               # File storage
│   │   ├── ses.py              # Email service
│   │   ├── groq_ai.py          # Groq AI integration
│   │   └── llama_service.py    # LLaMA model service
│   ├── models/                  # Data models
│   ├── ai/                      # AI model configurations
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

### AI-Powered Endpoints
- `POST /api/ai/symptom-check` - AI symptom analysis
- `POST /api/ai/analyze-report` - AI medical report analysis
- `POST /api/ai/drug-interaction` - AI drug interaction check
- `GET /api/ai/health-insights` - AI-generated health insights
- `POST /api/ai/treatment-suggestions` - AI treatment recommendations

### Patient Endpoints
- `GET /api/patient/profile` - Get patient profile
- `PUT /api/patient/profile` - Update patient profile
- `POST /api/patient/upload-medical-record` - Upload medical record
- `GET /api/patient/medical-records` - Get patient's records
- `GET /api/patient/doctors` - Get AI-recommended doctors
- `POST /api/patient/book-appointment` - Book appointment
- `GET /api/patient/appointments` - Get patient appointments

### Doctor Endpoints
- `GET /api/doctor/profile` - Get doctor profile
- `PUT /api/doctor/profile` - Update doctor profile
- `GET /api/doctor/patients` - Get assigned patients
- `GET /api/doctor/medical-records` - Get patient records with AI insights
- `POST /api/doctor/diagnosis` - Create AI-enhanced diagnosis
- `GET /api/doctor/appointments` - Get doctor appointments

## 🧪 Demo Accounts

### Patient Account
- **Email**: `patient@demo.com`
- **Password**: `password`

### Doctor Account
- **Email**: `doctor@demo.com`
- **Password**: `password`

## 🤖 AI Model Information

### Groq AI Features
- **Speed**: Sub-second inference times
- **Accuracy**: High-precision medical analysis
- **Scalability**: Handles multiple concurrent requests
- **Cost-Effective**: Optimized pricing for healthcare applications

### LLaMA Model Capabilities
- **Medical NLP**: Specialized in healthcare language understanding
- **Multilingual**: Support for multiple languages
- **Context Awareness**: Understanding of medical context and terminology
- **Privacy-Focused**: Can be deployed locally for sensitive data

## 🔒 Security Features

- **Authentication**: JWT tokens with role-based access
- **Data Protection**: Encrypted passwords with bcrypt
- **File Security**: Secure S3 uploads with signed URLs
- **Input Validation**: Comprehensive data validation
- **CORS Protection**: Configured for secure cross-origin requests
- **AI Privacy**: Secure AI processing with data anonymization
- **HIPAA Compliance**: Healthcare data protection standards

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

### AI Model Deployment
```bash
# For local LLaMA deployment
python -m transformers.models.llama.convert_llama_weights_to_hf \
  --input_dir /path/to/llama/weights \
  --model_size 7B \
  --output_dir ./models/llama-7b-hf
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-ai-feature`)
3. Commit your changes (`git commit -m 'Add amazing AI feature'`)
4. Push to the branch (`git push origin feature/amazing-ai-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the AI model documentation
- Check Groq AI documentation for inference optimization

---

<div align="center">

**Built with ❤️ for AI-Enhanced Modern Healthcare**

*Connecting Patients and Doctors Through Advanced AI Technology*

[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![Groq AI](https://img.shields.io/badge/Groq-AI-orange.svg)](https://groq.com/)
[![LLaMA](https://img.shields.io/badge/LLaMA-Models-red.svg)](https://ai.meta.com/llama/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-blue.svg)](https://tailwindcss.com/)

</div>