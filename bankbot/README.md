# 🏦 BankBot - AI-Powered Banking Assistant

A modern, full-stack banking application built with **FastAPI** and **Next.js 14**, featuring an intelligent AI chatbot for banking assistance.

## ✨ Features

### 🎨 **Modern UI/UX**
- **Glassmorphism Design**: Beautiful glass-like effects and gradients
- **Responsive Layout**: Works perfectly on all devices
- **Smooth Animations**: Framer Motion powered interactions
- **Dark Theme**: Eye-friendly dark color scheme

### 🤖 **AI Chatbot**
- **Intelligent Responses**: Pattern-based intent recognition
- **Banking Knowledge**: Built-in banking FAQ responses
- **Context Awareness**: Personalized responses based on user data
- **Quick Actions**: Suggested actions for common queries

### 🏦 **Banking Features**
- **Account Management**: View balances and account details
- **Transaction History**: Track spending and income
- **Secure Authentication**: JWT-based authentication
- **Real-time Updates**: Live data from backend

### 🔒 **Security & Performance**
- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Bcrypt encryption
- **CORS Protection**: Secure cross-origin requests
- **SQLite Database**: Fast, reliable data storage

## 🚀 Tech Stack

### **Frontend**
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client

### **Backend**
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation
- **JWT** - JSON Web Tokens
- **Passlib** - Password hashing
- **Uvicorn** - ASGI server

### **Database**
- **SQLite** - Lightweight, serverless database

## 🛠️ Quick Start

### **Prerequisites**
- Python 3.8+
- Node.js 18+
- npm or yarn

### **1. Clone & Setup**
```bash
git clone <repository-url>
cd bankbot
```

### **2. Start Everything**
```bash
./start.sh
```

This script will:
- ✅ Start the FastAPI backend
- ✅ Create demo user automatically
- ✅ Start the Next.js frontend
- ✅ Verify both servers are running

### **3. Access the App**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### **4. Login with Demo Account**
- **Email**: `demo@bankbot.com`
- **Password**: `demo123`

## 📁 Project Structure

```
bankbot/
├── backend/                 # FastAPI backend
│   ├── main.py            # Main application
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── auth.py            # Authentication utilities
│   ├── chatbot.py         # AI chatbot logic
│   ├── create_demo_user.py # Demo user creation
│   └── venv/              # Python virtual environment
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   │   ├── page.tsx   # Landing page
│   │   │   └── dashboard/ # Dashboard pages
│   │   └── components/    # React components
│   └── package.json
├── start.sh               # Startup script
└── README.md              # This file
```

## 🔌 API Endpoints

### **Authentication**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### **Banking**
- `GET /api/banking/accounts` - Get user accounts
- `GET /api/banking/balance` - Get total balance
- `GET /api/banking/transactions` - Get transaction history

### **Chatbot**
- `POST /api/chat` - Chat with AI assistant

## 🤖 Chatbot Capabilities

The AI chatbot can help with:
- **Balance Inquiries**: Check account balances
- **Transfer Information**: How to transfer money
- **Transaction History**: View recent activity
- **Account Details**: Account information
- **General Help**: Banking assistance

## 🎨 Design System

### **Colors**
- **Primary**: Blue (#3B82F6) to Purple (#8B5CF6)
- **Secondary**: Cyan (#06B6D4) to Teal (#14B8A6)
- **Accent**: Orange (#F97316) to Red (#EF4444)

### **Components**
- **Glassmorphism**: Translucent, blurred backgrounds
- **Gradients**: Smooth color transitions
- **Shadows**: Subtle depth and elevation
- **Rounded Corners**: Modern, friendly appearance

## 🔧 Development

### **Backend Development**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### **Frontend Development**
```bash
cd frontend
npm run dev
```

### **Database Management**
```bash
cd backend
source venv/bin/activate
python create_demo_user.py
```

## 🚀 Deployment

### **Backend Deployment**
1. Set up production environment
2. Configure environment variables
3. Use production ASGI server (Gunicorn + Uvicorn)
4. Set up reverse proxy (Nginx)

### **Frontend Deployment**
1. Build production version: `npm run build`
2. Deploy to Vercel, Netlify, or static hosting
3. Configure environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **FastAPI** team for the amazing framework
- **Next.js** team for the React framework
- **Tailwind CSS** for the utility-first CSS
- **Framer Motion** for the animation library

---

**Built with ❤️ and AI** 🚀✨