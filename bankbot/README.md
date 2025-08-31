# 🚀 BankBot - AI Banking Assistant

A modern, AI-powered banking application built with cutting-edge technologies and beautiful design.

## ✨ Features

### 🎨 **Modern UI/UX**
- **Glassmorphism Design**: Beautiful translucent effects and modern aesthetics
- **Smooth Animations**: Framer Motion powered animations and transitions
- **Responsive Design**: Works perfectly on all devices
- **Dark Theme**: Elegant dark mode with gradient accents

### 🤖 **AI-Powered Chatbot**
- **Intelligent Responses**: Context-aware banking assistance
- **Intent Detection**: Understands user queries and provides relevant answers
- **Personalized Experience**: Tailored responses based on user context
- **Quick Actions**: Suggested actions for common banking tasks

### 💳 **Banking Features**
- **Account Management**: Multiple account types (checking, savings, investment)
- **Transaction History**: Detailed transaction tracking with categories
- **Balance Overview**: Real-time balance monitoring with privacy toggle
- **Quick Actions**: Transfer money, pay bills, open accounts

### 🔒 **Security & Performance**
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt encryption for user passwords
- **FastAPI Backend**: High-performance Python backend
- **SQLite Database**: Lightweight, reliable data storage

## 🛠️ Tech Stack

### **Frontend**
- **Next.js 14**: Latest React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations and transitions
- **Lucide React**: Beautiful icon set

### **Backend**
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Token authentication
- **Uvicorn**: Lightning-fast ASGI server

### **Database**
- **SQLite**: Lightweight, serverless database
- **SQLAlchemy ORM**: Object-relational mapping

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- Node.js 18+
- npm or yarn

### **1. Clone and Setup**
```bash
git clone <repository-url>
cd bankbot
```

### **2. Backend Setup**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Frontend Setup**
```bash
cd ../frontend
npm install
```

### **4. Start Everything**
```bash
cd ..
chmod +x start.sh
./start.sh
```

### **5. Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📱 Screenshots

### Landing Page
- Modern hero section with animated background
- Feature highlights with glassmorphism cards
- Statistics and call-to-action sections

### Dashboard
- Account overview with balance privacy toggle
- Multiple account cards with trend indicators
- Tabbed navigation (Overview, Transactions, Analytics, Goals, Settings)
- Recent activity and quick actions

### Chatbot
- Modal-based chat interface
- Quick reply suggestions
- Intent detection display
- Beautiful message bubbles

## 🔧 API Endpoints

### **Authentication**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### **Banking**
- `GET /api/banking/accounts` - Get user accounts
- `GET /api/banking/balance` - Get account balances
- `GET /api/banking/transactions` - Get transaction history

### **Chatbot**
- `POST /api/chat` - Chat with BankBot AI

### **Health**
- `GET /` - API status and endpoints
- `GET /health` - Health check

## 🎯 Chatbot Capabilities

The AI chatbot can handle:
- **Balance Inquiries**: Check account balances
- **Transfer Information**: How to transfer money
- **Transaction History**: View recent transactions
- **Account Information**: Account details and types
- **General Banking Help**: Banking hours, support

## 🎨 Design System

### **Color Palette**
- **Primary**: Blue gradients (#3B82F6 to #8B5CF6)
- **Secondary**: Purple and cyan accents
- **Background**: Dark slate with blue undertones
- **Text**: White and blue variations

### **Typography**
- **Headings**: Bold, gradient text with background clipping
- **Body**: Clean, readable fonts
- **Accents**: Colored text for important information

### **Components**
- **Cards**: Glassmorphism with backdrop blur
- **Buttons**: Gradient backgrounds with hover effects
- **Inputs**: Modern form controls with focus states
- **Modals**: Smooth animations and backdrop blur

## 🔒 Security Features

- **JWT Authentication**: Secure token-based sessions
- **Password Hashing**: Bcrypt encryption
- **CORS Protection**: Cross-origin request handling
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM

## 📊 Performance Features

- **FastAPI**: High-performance async framework
- **Uvicorn**: Lightning-fast ASGI server
- **SQLite**: Serverless, fast database
- **Next.js**: Optimized React framework
- **Image Optimization**: Next.js built-in image optimization

## 🚀 Deployment

### **Backend (FastAPI)**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### **Frontend (Next.js)**
```bash
cd frontend
npm run build
npm start
```

### **Environment Variables**
Create `.env` files for production:
```bash
# Backend
SECRET_KEY=your-production-secret-key
DATABASE_URL=your-database-url

# Frontend
NEXT_PUBLIC_API_URL=your-backend-url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI** for the amazing Python web framework
- **Next.js** for the React framework
- **Tailwind CSS** for the utility-first CSS framework
- **Framer Motion** for the smooth animations
- **Lucide** for the beautiful icons

---

## 🎉 **Ready to Transform Your Banking Experience?**

BankBot combines cutting-edge technology with beautiful design to create the future of banking. Start building your AI-powered banking application today!

**Get Started**: Run `./start.sh` and experience the future of banking! 🚀✨